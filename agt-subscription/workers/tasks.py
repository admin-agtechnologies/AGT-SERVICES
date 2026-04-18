"""
AGT Subscription Service v1.0 - Tâches Celery.

Ce fichier contient :
1. Les crons Beat (cycle de vie des abonnements, quotas)
2. Les tâches déclenchées par les events RabbitMQ entrants (payment.confirmed, payment.failed)
3. Les émetteurs d'events RabbitMQ sortants (subscription.payment_required)
"""
import logging
import uuid
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


# ===========================================================================
# CRONS — Cycle de vie des abonnements
# ===========================================================================

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def renew_expiring_subscriptions(self):
    """
    Cron horaire : identifie les abonnements actifs dont la période expire
    dans moins de 24h et émet subscription.payment_required vers Payment.
    Retry : 3x avec backoff 1min, 5min, 15min (CDC NF-12).
    """
    from apps.subscriptions.models import Subscription
    from workers.publisher import publish_payment_required

    now = timezone.now()
    horizon = now + timedelta(hours=24)

    # Abonnements actifs (non gratuits, non annulés) qui expirent bientôt
    expiring = Subscription.objects.select_related("plan", "plan_price").filter(
        status="active",
        cancel_at_period_end=False,
        current_period_end__lte=horizon,
        current_period_end__gt=now,
        plan__is_free=False,
    )

    count = 0
    for sub in expiring:
        try:
            # Vérifie qu'on n'a pas déjà émis un event pour ce cycle
            from apps.subscriptions.models import SubscriptionEvent
            already_requested = SubscriptionEvent.objects.filter(
                subscription=sub,
                event_type="payment_requested",
                created_at__gte=sub.current_period_start,
            ).exists()

            if not already_requested:
                publish_payment_required(sub, reason="renewal")
                SubscriptionEvent.objects.create(
                    subscription=sub,
                    event_type="payment_requested",
                    metadata={"reason": "renewal", "amount": float(sub.plan_price.price)},
                )
                count += 1
                logger.info(f"[RENEW] Emission payment_required pour sub {sub.id}")

        except Exception as exc:
            logger.error(f"[RENEW] Erreur sub {sub.id}: {exc}")
            # Retry avec backoff exponentiel
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

    logger.info(f"[RENEW] {count} abonnements traités")
    return {"renewed": count}


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_expired_subscriptions(self):
    """
    Cron horaire : passe les abonnements expirés en grace ou expired
    selon la config plateforme (grace_period_days).
    """
    from apps.subscriptions.models import Subscription, PlatformSubscriptionConfig

    now = timezone.now()

    # 1. Abonnements actifs dont la période est dépassée → grace ou expired
    overdue = Subscription.objects.filter(
        status="active",
        current_period_end__lte=now,
    )

    for sub in overdue:
        try:
            config = PlatformSubscriptionConfig.objects.filter(
                platform_id=sub.platform_id
            ).first()
            grace_days = config.grace_period_days if config else 0

            if grace_days > 0:
                sub.status = "grace"
                sub.grace_end = sub.current_period_end + timedelta(days=grace_days)
                logger.info(f"[EXPIRE] Sub {sub.id} → grace (fin: {sub.grace_end})")
            else:
                sub.status = "expired"
                logger.info(f"[EXPIRE] Sub {sub.id} → expired")

            sub.save(update_fields=["status", "grace_end", "updated_at"])

            from apps.subscriptions.models import SubscriptionEvent
            SubscriptionEvent.objects.create(
                subscription=sub,
                event_type="expired" if sub.status == "expired" else "grace_started",
            )
            # Émettre l'event lifecycle si directement expired (sans grace)
            if sub.status == "expired":
                from workers.publisher import publish_subscription_expired
                publish_subscription_expired(sub)

        except Exception as exc:
            logger.error(f"[EXPIRE] Erreur sub {sub.id}: {exc}")

    # 2. Abonnements en grace dont la période de grâce est dépassée → expired
    grace_overdue = Subscription.objects.filter(
        status="grace",
        grace_end__lte=now,
    )

    for sub in grace_overdue:
        try:
            sub.status = "expired"
            sub.save(update_fields=["status", "updated_at"])
            logger.info(f"[EXPIRE] Sub {sub.id} grace → expired")

            from apps.subscriptions.models import SubscriptionEvent
            SubscriptionEvent.objects.create(
                subscription=sub,
                event_type="expired",
            )
            # Émettre l'event lifecycle — accès à couper immédiatement
            from workers.publisher import publish_subscription_expired
            publish_subscription_expired(sub)
        except Exception as exc:
            logger.error(f"[EXPIRE] Erreur grace sub {sub.id}: {exc}")

    return {"processed": overdue.count() + grace_overdue.count()}


@shared_task
def expire_stale_quota_reservations():
    """
    Cron toutes les 10 minutes : expire les quota_reservations
    en statut 'pending' dont expires_at est dépassé.
    """
    from apps.subscriptions.models import QuotaReservation

    now = timezone.now()
    stale = QuotaReservation.objects.filter(
        status="pending",
        expires_at__lte=now,
    )

    count = stale.count()
    stale.update(status="expired", resolved_at=now)
    logger.info(f"[RESERVATIONS] {count} réservations expirées")
    return {"expired": count}


@shared_task
def send_quota_alerts():
    """
    Cron horaire : détecte les quotas ayant dépassé 80% d'utilisation
    et envoie une alerte via Notification Service.
    """
    from apps.subscriptions.models import Subscription, SubscriptionQuotaUsage
    from apps.plans.models import PlanQuota
    from workers.publisher import publish_notification_event

    active_subs = Subscription.objects.filter(status="active").select_related("plan")
    alerts_sent = 0

    for sub in active_subs:
        usages = SubscriptionQuotaUsage.objects.filter(
            subscription=sub,
            period_start=sub.current_period_start,
        )
        plan_quotas = {
            q.quota_key: q.limit_value
            for q in PlanQuota.objects.filter(plan=sub.plan)
        }

        for usage in usages:
            limit = plan_quotas.get(usage.quota_key, 0)
            if limit <= 0:
                continue

            pct = (usage.used / limit) * 100

            # Alerte à 80% — une seule fois par cycle (vérifié via cache Redis)
            if pct >= 80:
                from django.core.cache import cache
                cache_key = f"quota_alert_80:{sub.id}:{usage.quota_key}:{sub.current_period_start.date()}"

                if not cache.get(cache_key):
                    try:
                        publish_notification_event({
                            "event": "quota_alert",
                            "subscription_id": str(sub.id),
                            "platform_id": str(sub.platform_id),
                            "subscriber_id": str(sub.subscriber_id),
                            "quota_key": usage.quota_key,
                            "used": usage.used,
                            "limit": limit,
                            "percentage": round(pct, 1),
                        })
                        # TTL jusqu'à la fin du cycle pour ne pas ré-alerter
                        ttl = int((sub.current_period_end - timezone.now()).total_seconds())
                        cache.set(cache_key, True, timeout=max(ttl, 3600))
                        alerts_sent += 1
                    except Exception as exc:
                        logger.error(f"[QUOTA ALERT] Erreur sub {sub.id} quota {usage.quota_key}: {exc}")

    logger.info(f"[QUOTA ALERT] {alerts_sent} alertes envoyées")
    return {"alerts_sent": alerts_sent}


# ===========================================================================
# CONSOMMATEURS RabbitMQ — events entrants depuis Payment
# ===========================================================================

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def handle_payment_confirmed(self, payload: dict):
    """
    Consomme l'event payment.confirmed depuis Payment.
    Active ou renouvelle l'abonnement correspondant.
    Idempotent : déduplique sur payment_reference_id.
    """
    from apps.subscriptions.models import Subscription, SubscriptionEvent

    subscription_id = payload.get("subscription_id")
    payment_reference_id = payload.get("payment_reference_id")
    idempotency_key = payload.get("idempotency_key")

    if not subscription_id or not payment_reference_id:
        logger.error(f"[PAYMENT CONFIRMED] Payload invalide: {payload}")
        return

    # Déduplication sur payment_reference_id
    already_processed = SubscriptionEvent.objects.filter(
        subscription_id=subscription_id,
        metadata__payment_reference_id=payment_reference_id,
    ).exists()

    if already_processed:
        logger.warning(f"[PAYMENT CONFIRMED] Déjà traité: {payment_reference_id}")
        return

    try:
        sub = Subscription.objects.get(id=subscription_id)
    except Subscription.DoesNotExist:
        logger.error(f"[PAYMENT CONFIRMED] Abonnement introuvable: {subscription_id}")
        return

    try:
        reason = payload.get("reason", "new")

        if reason == "renewal":
            # Renouvellement : avancer la période
            from apps.subscriptions.service import SubscriptionService
            SubscriptionService.renew(sub)
            event_type = "renewed"
        else:
            # Nouvelle souscription : activation
            sub.status = "active"
            sub.save(update_fields=["status", "updated_at"])
            event_type = "activated"
            # Émettre l'event lifecycle après activation via paiement confirmé
            from workers.publisher import publish_subscription_activated
            publish_subscription_activated(sub)

        SubscriptionEvent.objects.create(
            subscription=sub,
            event_type=event_type,
            metadata={
                "payment_reference_id": payment_reference_id,
                "idempotency_key": idempotency_key,
            },
        )
        logger.info(f"[PAYMENT CONFIRMED] Sub {sub.id} → {event_type}")

    except Exception as exc:
        logger.error(f"[PAYMENT CONFIRMED] Erreur sub {subscription_id}: {exc}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def handle_payment_failed(self, payload: dict):
    """
    Consomme l'event payment.failed depuis Payment.
    Déclenche la logique de grâce ou suspension.
    """
    from apps.subscriptions.models import Subscription, SubscriptionEvent, PlatformSubscriptionConfig

    subscription_id = payload.get("subscription_id")
    payment_reference_id = payload.get("payment_reference_id")

    if not subscription_id:
        logger.error(f"[PAYMENT FAILED] Payload invalide: {payload}")
        return

    # Déduplication
    already_processed = SubscriptionEvent.objects.filter(
        subscription_id=subscription_id,
        event_type="payment_failed",
        metadata__payment_reference_id=payment_reference_id,
    ).exists()

    if already_processed:
        logger.warning(f"[PAYMENT FAILED] Déjà traité: {payment_reference_id}")
        return

    try:
        sub = Subscription.objects.get(id=subscription_id)
    except Subscription.DoesNotExist:
        logger.error(f"[PAYMENT FAILED] Abonnement introuvable: {subscription_id}")
        return

    try:
        config = PlatformSubscriptionConfig.objects.filter(
            platform_id=sub.platform_id
        ).first()
        grace_days = config.grace_period_days if config else 0

        if grace_days > 0:
            sub.status = "grace"
            sub.grace_end = timezone.now() + timedelta(days=grace_days)
        else:
            sub.status = "expired"

        sub.save(update_fields=["status", "grace_end", "updated_at"])

        SubscriptionEvent.objects.create(
            subscription=sub,
            event_type="payment_failed",
            metadata={
                "payment_reference_id": payment_reference_id,
                "failure_reason": payload.get("failure_reason"),
            },
        )
        logger.info(f"[PAYMENT FAILED] Sub {sub.id} → {sub.status}")

    except Exception as exc:
        logger.error(f"[PAYMENT FAILED] Erreur sub {subscription_id}: {exc}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))