"""AGT Subscription Service v1.0 - Quotas service (chemin critique < 50ms)."""
import logging
from django.core.cache import cache
from django.utils import timezone
from apps.subscriptions.models import Subscription, SubscriptionQuotaUsage, QuotaReservation, SubscriptionStatus
from apps.plans.models import PlanQuota

logger = logging.getLogger(__name__)


class QuotaService:
    CACHE_TTL = 30

    @classmethod
    def _cache_key(cls, sub_id, quota_key):
        return f"quota:{sub_id}:{quota_key}"

    @classmethod
    def _get_active_sub(cls, platform_id, subscriber_type, subscriber_id):
        return Subscription.objects.filter(
            platform_id=platform_id, subscriber_type=subscriber_type,
            subscriber_id=subscriber_id, status__in=[
                SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIAL, SubscriptionStatus.GRACE
            ]
        ).select_related("plan").first()

    @classmethod
    def check(cls, platform_id, subscriber_type, subscriber_id, quota_key, requested=1):
        sub = cls._get_active_sub(platform_id, subscriber_type, subscriber_id)
        if not sub:
            return {"allowed": False, "reason": "no_active_subscription"}

        # Cache Redis
        ck = cls._cache_key(sub.id, quota_key)
        cached = cache.get(ck)
        if cached:
            remaining = cached["limit"] - cached["used"]
            allowed = remaining >= requested if cached["overage_policy"] == "hard" else True
            return {**cached, "remaining": max(0, remaining), "allowed": allowed, "requested": requested}

        plan_quota = PlanQuota.objects.filter(plan=sub.plan, quota_key=quota_key).first()
        if not plan_quota:
            return {"allowed": True, "reason": "quota_not_defined", "quota_key": quota_key}

        usage = SubscriptionQuotaUsage.objects.filter(
            subscription=sub, quota_key=quota_key,
            period_start=sub.current_period_start
        ).first()
        used = usage.used if usage else 0
        overage = usage.overage if usage else 0

        # Compter reservations pending
        reserved = QuotaReservation.objects.filter(
            subscription=sub, quota_key=quota_key, status="pending", expires_at__gt=timezone.now()
        ).count()

        effective_used = used + reserved
        remaining = plan_quota.limit_value - effective_used
        allowed = remaining >= requested if plan_quota.overage_policy == "hard" else True

        result = {
            "allowed": allowed, "quota_key": quota_key,
            "limit": plan_quota.limit_value, "used": effective_used,
            "remaining": max(0, remaining), "overage": overage,
            "overage_policy": plan_quota.overage_policy,
        }
        cache.set(ck, result, timeout=cls.CACHE_TTL)
        return result

    @classmethod
    def increment(cls, platform_id, subscriber_type, subscriber_id, quota_key, amount=1):
        sub = cls._get_active_sub(platform_id, subscriber_type, subscriber_id)
        if not sub:
            return None, "no_active_subscription"

        plan_quota = PlanQuota.objects.filter(plan=sub.plan, quota_key=quota_key).first()
        if not plan_quota:
            return None, "quota_not_defined"

        usage, _ = SubscriptionQuotaUsage.objects.get_or_create(
            subscription=sub, quota_key=quota_key, period_start=sub.current_period_start,
            defaults={"period_end": sub.current_period_end, "used": 0, "overage": 0}
        )

        new_used = usage.used + amount
        if plan_quota.overage_policy == "hard" and new_used > plan_quota.limit_value:
            return None, "hard_limit_exceeded"

        if new_used > plan_quota.limit_value:
            usage.overage += (new_used - plan_quota.limit_value) - usage.overage
            usage.overage = max(0, new_used - plan_quota.limit_value)

        usage.used = new_used
        usage.save(update_fields=["used", "overage", "updated_at"])

        # Invalider cache
        cache.delete(cls._cache_key(sub.id, quota_key))

        return {
            "quota_key": quota_key, "used": usage.used,
            "limit": plan_quota.limit_value, "overage": usage.overage,
        }, None

    @classmethod
    def reserve(cls, platform_id, subscriber_type, subscriber_id, quota_key, amount=1, ttl_seconds=300):
        sub = cls._get_active_sub(platform_id, subscriber_type, subscriber_id)
        if not sub:
            return None, "no_active_subscription"

        check_result = cls.check(platform_id, subscriber_type, subscriber_id, quota_key, amount)
        if not check_result.get("allowed"):
            return None, "quota_exceeded"

        reservation = QuotaReservation.objects.create(
            subscription=sub, quota_key=quota_key, amount=amount,
            expires_at=timezone.now() + timezone.timedelta(seconds=ttl_seconds),
        )
        cache.delete(cls._cache_key(sub.id, quota_key))
        return {"reservation_id": str(reservation.id), "amount": amount, "expires_at": reservation.expires_at.isoformat()}, None

    @classmethod
    def confirm_reservation(cls, reservation_id):
        try:
            r = QuotaReservation.objects.select_related("subscription").get(id=reservation_id, status="pending")
        except QuotaReservation.DoesNotExist:
            return None, "reservation_not_found"

        result, err = cls.increment(
            r.subscription.platform_id, r.subscription.subscriber_type,
            r.subscription.subscriber_id, r.quota_key, r.amount
        )
        r.status = "confirmed"
        r.resolved_at = timezone.now()
        r.save(update_fields=["status", "resolved_at"])
        return result, err

    @classmethod
    def release_reservation(cls, reservation_id):
        try:
            r = QuotaReservation.objects.select_related("subscription").get(id=reservation_id, status="pending")
        except QuotaReservation.DoesNotExist:
            return None, "reservation_not_found"

        r.status = "released"
        r.resolved_at = timezone.now()
        r.save(update_fields=["status", "resolved_at"])
        cache.delete(cls._cache_key(r.subscription.id, r.quota_key))
        return {"released": True}, None
