"""AGT Subscription Service v1.0 - Subscription lifecycle service."""
import logging
from decimal import Decimal
from operator import sub
from django.utils import timezone
from datetime import timedelta
from apps.plans.models import Plan, PlanPrice, PlanQuota
from apps.subscriptions.models import (
    Subscription, SubscriptionStatus, SubscriptionEvent,
    SubscriptionQuotaUsage, PlatformSubscriptionConfig,
)
# Ajout : publisher lifecycle events
from workers.publisher import (
    publish_subscription_activated,
    publish_subscription_cancelled,
)
logger = logging.getLogger(__name__)


class SubscriptionService:

    @classmethod
    def create(cls, platform_id, subscriber_type, subscriber_id, plan_id, billing_cycle, with_trial=False):
        # Verifier pas d'abonnement actif
        existing = Subscription.objects.filter(
            platform_id=platform_id, subscriber_type=subscriber_type,
            subscriber_id=subscriber_id
        ).exclude(status__in=["expired", "cancelled"]).first()
        if existing:
            return None, "active_subscription_exists"

        try:
            plan = Plan.objects.get(id=plan_id, platform_id=platform_id, is_active=True)
        except Plan.DoesNotExist:
            return None, "plan_not_found"

        price = PlanPrice.objects.filter(plan=plan, billing_cycle=billing_cycle, is_active=True).first()
        if not price:
            return None, "price_not_found"

        config = PlatformSubscriptionConfig.get_for_platform(str(platform_id))
        now = timezone.now()
        cycle_days = price.get_cycle_days()
        period_end = now + timedelta(days=cycle_days)

        trial_end = None
        status = SubscriptionStatus.PENDING_PAYMENT

        if plan.is_free:
            status = SubscriptionStatus.ACTIVE
        elif with_trial and config.default_trial_days > 0:
            trial_end = now + timedelta(days=config.default_trial_days)
            status = SubscriptionStatus.TRIAL

        sub = Subscription.objects.create(
            platform_id=platform_id, subscriber_type=subscriber_type,
            subscriber_id=subscriber_id, plan=plan, plan_price=price,
            status=status, current_period_start=now, current_period_end=period_end,
            trial_end=trial_end,
        )

        # Initialiser les quotas usage
        cls._init_quota_usage(sub)

        SubscriptionEvent.objects.create(subscription=sub, event_type="created",
                                          to_plan=plan, metadata={"billing_cycle": billing_cycle, "with_trial": with_trial})

        return sub, None

    @classmethod
    def activate(cls, sub_id):
        try:
            sub = Subscription.objects.get(id=sub_id)
        except Subscription.DoesNotExist:
            return None, "not_found"

        if sub.status not in [SubscriptionStatus.PENDING_PAYMENT, SubscriptionStatus.TRIAL]:
            return None, "cannot_activate"

        sub.status = SubscriptionStatus.ACTIVE
        sub.save(update_fields=["status", "updated_at"])
        SubscriptionEvent.objects.create(subscription=sub, event_type="activated")
        
        # Publier l'événement d'activation    # Émettre l'event lifecycle — les backends métier peuvent réagir (permissions, onboarding)
        publish_subscription_activated(sub)
        return sub, None

    @classmethod
    def change_plan(cls, sub_id, new_plan_id, billing_cycle):
        try:
            sub = Subscription.objects.select_related("plan", "plan_price").get(id=sub_id)
        except Subscription.DoesNotExist:
            return None, "not_found"

        if not sub.is_usable():
            return None, "subscription_not_active"

        if str(sub.plan_id) == str(new_plan_id):
            return None, "same_plan"

        try:
            new_plan = Plan.objects.get(id=new_plan_id, platform_id=sub.platform_id, is_active=True)
        except Plan.DoesNotExist:
            return None, "new_plan_not_found"

        new_price = PlanPrice.objects.filter(plan=new_plan, billing_cycle=billing_cycle, is_active=True).first()
        if not new_price:
            return None, "new_price_not_found"

        # Calcul prorata
        days_remaining = sub.days_remaining()
        old_daily = sub.plan_price.price_per_day()
        new_daily = new_price.price_per_day()

        credit = Decimal(str(days_remaining)) * old_daily
        debit = Decimal(str(days_remaining)) * new_daily
        amount_due = max(Decimal("0"), debit - credit)

        old_plan = sub.plan
        event_type = "upgraded" if new_plan.tier_order > old_plan.tier_order else "downgraded"

        # Mettre a jour
        sub.plan = new_plan
        sub.plan_price = new_price
        sub.save(update_fields=["plan", "plan_price", "updated_at"])

        SubscriptionEvent.objects.create(
            subscription=sub, event_type=event_type,
            from_plan=old_plan, to_plan=new_plan,
            prorate_credit=credit, prorate_debit=debit,
        )

        return {
            "subscription_id": str(sub.id), "old_plan": old_plan.name,
            "new_plan": new_plan.name, "event_type": event_type,
            "prorate_credit": float(credit), "prorate_debit": float(debit),
            "amount_due": float(amount_due),
        }, None

    @classmethod
    def cancel(cls, sub_id):
        try:
            sub = Subscription.objects.get(id=sub_id)
        except Subscription.DoesNotExist:
            return None, "not_found"

        if sub.status in [SubscriptionStatus.CANCELLED, SubscriptionStatus.EXPIRED]:
            return None, "already_terminated"

        sub.cancel()
        SubscriptionEvent.objects.create(subscription=sub, event_type="cancelled")
        # Émettre l'event lifecycle — les backends métier préparent la fin d'accès
        publish_subscription_cancelled(sub)

        return sub, None

    @classmethod
    def _init_quota_usage(cls, sub):
        quotas = PlanQuota.objects.filter(plan=sub.plan)
        for q in quotas:
            SubscriptionQuotaUsage.objects.get_or_create(
                subscription=sub, quota_key=q.quota_key, period_start=sub.current_period_start,
                defaults={"period_end": sub.current_period_end, "used": 0, "overage": 0}
            )
