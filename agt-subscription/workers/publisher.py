"""
AGT Subscription Service v1.0 - Publisher RabbitMQ.

Émet les événements sortants vers :
- Payment : subscription.payment_required, subscription.overage_billing
- Notification : subscription.lifecycle (alertes cycle de vie et quotas)

Chaque event porte :
- event_id (UUID v4 unique) — pour déduplication côté consommateur
- idempotency_key (UUID v4) — clé idempotente pour Payment
- timestamp ISO8601
- source = "subscription"
"""
import json
import logging
import uuid
from datetime import datetime, timezone

import kombu

from django.conf import settings

logger = logging.getLogger(__name__)


def _get_connection():
    """Retourne une connexion RabbitMQ depuis les settings."""
    rabbitmq_url = getattr(settings, "RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
    return kombu.Connection(rabbitmq_url)


def _publish(exchange_name: str, routing_key: str, payload: dict) -> bool:
    """
    Publie un message sur RabbitMQ.
    Retourne True si succès, False si échec (le caller décide du retry).
    """
    try:
        with _get_connection() as conn:
            exchange = kombu.Exchange(exchange_name, type="topic", durable=True)
            producer = conn.Producer(serializer="json")
            producer.publish(
                payload,
                exchange=exchange,
                routing_key=routing_key,
                declare=[exchange],
                retry=True,
                retry_policy={
                    "interval_start": 0,
                    "interval_step": 2,
                    "interval_max": 10,
                    "max_retries": 3,
                },
            )
        logger.info(f"[PUBLISH] {routing_key} → {exchange_name} | event_id={payload.get('event_id')}")
        return True
    except Exception as exc:
        logger.error(f"[PUBLISH] Échec {routing_key}: {exc}")
        return False


def publish_payment_required(subscription, reason: str = "new") -> bool:
    """
    Émet subscription.payment_required vers Payment.
    Déclenché lors d'une nouvelle souscription payante ou d'un renouvellement.
    """
    payload = {
        "event_id": str(uuid.uuid4()),
        "idempotency_key": str(uuid.uuid4()),
        "source": "subscription",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subscription_id": str(subscription.id),
        "platform_id": str(subscription.platform_id),
        "subscriber_type": subscription.subscriber_type,
        "subscriber_id": str(subscription.subscriber_id),
        "amount": float(subscription.plan_price.price),
        "currency": subscription.plan_price.currency,
        "reason": reason,  # new | renewal | upgrade
    }
    return _publish("subscription", "subscription.payment_required", payload)


def publish_overage_billing(subscription, quota_key: str, overage_amount: int,
                            unit_price: float, quota_snapshot: dict) -> bool:
    """
    Émet subscription.overage_billing vers Payment.
    Déclenché lors de la fermeture d'un cycle avec dépassement de quota (overage policy).
    """
    total = overage_amount * unit_price
    payload = {
        "event_id": str(uuid.uuid4()),
        "idempotency_key": str(uuid.uuid4()),
        "source": "subscription",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subscription_id": str(subscription.id),
        "platform_id": str(subscription.platform_id),
        "quota_key": quota_key,
        "overage_amount": overage_amount,
        "unit_price": unit_price,
        "total": total,
        "currency": subscription.plan_price.currency,
        "quota_snapshot": quota_snapshot,
    }
    return _publish("subscription", "subscription.overage_billing", payload)


def publish_subscription_activated(subscription) -> bool:
    """
    Émet subscription.activated vers tous les consommateurs intéressés.

    Déclenché lors de l'activation d'un abonnement (paiement confirmé,
    plan gratuit, ou activation manuelle). Permet aux backends métier
    de réagir : mise à jour des permissions, onboarding, notifications.

    Consommateurs attendus : backends métier (AGT-Bot, AGT-Market, etc.)
    """
    payload = {
        "event_id": str(uuid.uuid4()),
        "event_type": "subscription.activated",
        "source": "subscription",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": {
            "subscription_id": str(subscription.id),
            "platform_id": str(subscription.platform_id),
            "subscriber_type": subscription.subscriber_type,
            "subscriber_id": str(subscription.subscriber_id),
            "plan_id": str(subscription.plan.id),
            "plan_name": subscription.plan.name,
            "billing_cycle": subscription.plan_price.billing_cycle,
            "current_period_end": subscription.current_period_end.isoformat(),
        },
    }
    return _publish("subscription", "subscription.activated", payload)


def publish_subscription_cancelled(subscription) -> bool:
    """
    Émet subscription.cancelled vers tous les consommateurs intéressés.

    Déclenché lors de l'annulation d'un abonnement (cancel_at_period_end=True).
    Permet aux backends métier de réagir : restriction des droits à terme,
    notifications de fin d'abonnement.

    Consommateurs attendus : backends métier (AGT-Bot, AGT-Market, etc.)
    """
    payload = {
        "event_id": str(uuid.uuid4()),
        "event_type": "subscription.cancelled",
        "source": "subscription",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": {
            "subscription_id": str(subscription.id),
            "platform_id": str(subscription.platform_id),
            "subscriber_type": subscription.subscriber_type,
            "subscriber_id": str(subscription.subscriber_id),
            "plan_id": str(subscription.plan.id),
            "plan_name": subscription.plan.name,
            "current_period_end": subscription.current_period_end.isoformat(),
            "cancelled_at": subscription.cancelled_at.isoformat() if subscription.cancelled_at else None,
        },
    }
    return _publish("subscription", "subscription.cancelled", payload)


def publish_subscription_expired(subscription) -> bool:
    """
    Émet subscription.expired vers tous les consommateurs intéressés.

    Déclenché par le cron Celery Beat (process_expired_subscriptions)
    quand un abonnement passe à l'état 'expired'. Permet aux backends
    métier de couper les accès immédiatement.

    Consommateurs attendus : backends métier (AGT-Bot, AGT-Market, etc.)
    """
    payload = {
        "event_id": str(uuid.uuid4()),
        "event_type": "subscription.expired",
        "source": "subscription",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": {
            "subscription_id": str(subscription.id),
            "platform_id": str(subscription.platform_id),
            "subscriber_type": subscription.subscriber_type,
            "subscriber_id": str(subscription.subscriber_id),
            "plan_id": str(subscription.plan.id),
            "plan_name": subscription.plan.name,
            "expired_at": datetime.now(timezone.utc).isoformat(),
        },
    }
    return _publish("subscription", "subscription.expired", payload)


def publish_notification_event(data: dict) -> bool:
    """
    Émet un event vers Notification Service (alertes cycle de vie, quotas).
    data doit contenir : event, platform_id, subscriber_id, et les données spécifiques.
    """
    payload = {
        "event_id": str(uuid.uuid4()),
        "source": "subscription",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **data,
    }
    return _publish("notification", f"subscription.{data.get('event', 'lifecycle')}", payload)