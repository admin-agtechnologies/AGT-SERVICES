"""AGT Payment Service v1.2 - Payment initiation, lifecycle et publisher RabbitMQ.

Publisher pattern identique à agt-subscription/workers/publisher.py :
- Exchange type "topic", durable=True
- Chaque event porte : event_id (UUID v4), timestamp ISO8601, source="payment"
- Les consommateurs déduplicent sur event_id
- Retry automatique kombu (3 tentatives, backoff 0/2/10s)

Events émis :
- payment.confirmed → consommé par Wallet, Subscription, Notification
- payment.failed    → consommé par Subscription, Notification
- payment.cancelled → consommé par Subscription, Notification
- payment.expired   → consommé par Subscription, Notification
"""
import logging
import uuid
from datetime import datetime, timezone as dt_timezone, timedelta

import kombu
from django.conf import settings
from django.utils import timezone

from apps.payments.models import Transaction, TransactionStatus, WebhookLog, TransactionStatusHistory


logger = logging.getLogger(__name__)

# TTL par provider avant expiration automatique (en secondes)
PROVIDER_TTL = {
    "orange_money": 300,   # 5 min — USSD push expire vite
    "mtn_momo": 300,       # 5 min — idem
    "stripe": 1800,        # 30 min — session Stripe Checkout
    "paypal": 3600,        # 1h — session PayPal
}


# ===========================================================================
# PUBLISHER RABBITMQ
# Pattern identique à agt-subscription/workers/publisher.py
# ===========================================================================

def _get_rabbitmq_connection():
    """Retourne une connexion RabbitMQ depuis les settings Django."""
    broker_url = getattr(settings, "BROKER_URL", "amqp://guest:guest@localhost:5672//")
    return kombu.Connection(broker_url)


def _publish_event(routing_key: str, payload: dict) -> bool:
    """
    Publie un événement sur l'exchange RabbitMQ 'payments' (type topic).

    Pourquoi topic ? Permet aux consommateurs de s'abonner sélectivement :
    - Wallet s'abonne à 'payment.confirmed' uniquement
    - Subscription s'abonne à 'payment.confirmed', 'payment.failed', 'payment.cancelled'
    - Notification s'abonne à tous les events payment.*

    Retourne True si succès, False si échec (non bloquant — le paiement
    est déjà enregistré en base, l'event est best-effort).
    """
    try:
        with _get_rabbitmq_connection() as conn:
            exchange = kombu.Exchange("payments", type="topic", durable=True)
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
        logger.info(
            f"[PUBLISH] {routing_key} | event_id={payload.get('event_id')} | "
            f"transaction_id={payload.get('data', {}).get('payment_reference_id')}"
        )
        return True
    except Exception as exc:
        # Non bloquant : le paiement est enregistré, l'event est best-effort
        logger.error(f"[PUBLISH] Échec émission {routing_key}: {exc}")
        return False


def publish_payment_confirmed(tx: Transaction) -> bool:
    """
    Émet payment.confirmed après confirmation du provider via webhook.
    Consommateurs : Wallet (crédit), Subscription (activation), Notification (reçu).
    """
    payload = {
        "event_id": str(uuid.uuid4()),
        "event_type": "payment.confirmed",
        "timestamp": datetime.now(dt_timezone.utc).isoformat(),
        "source": "payment-service",
        "idempotency_key": str(tx.idempotency_key),
        "data": {
            "payment_reference_id": str(tx.id),
            "platform_id": str(tx.platform_id),
            "user_id": str(tx.user_id) if tx.user_id else None,
            "provider": tx.provider,
            "amount": float(tx.amount),
            "currency": tx.currency,
            "source": tx.source,
            "source_reference_id": str(tx.source_reference_id) if tx.source_reference_id else None,
            "metadata": tx.metadata,
            "confirmed_at": tx.confirmed_at.isoformat() if tx.confirmed_at else None,
        },
    }
    return _publish_event("payment.confirmed", payload)


def publish_payment_failed(tx: Transaction) -> bool:
    """
    Émet payment.failed après échec provider ou rejet.
    Consommateurs : Subscription (marquer en échec), Notification (alerte utilisateur).
    """
    payload = {
        "event_id": str(uuid.uuid4()),
        "event_type": "payment.failed",
        "timestamp": datetime.now(dt_timezone.utc).isoformat(),
        "source": "payment-service",
        "idempotency_key": str(tx.idempotency_key),
        "data": {
            "payment_reference_id": str(tx.id),
            "platform_id": str(tx.platform_id),
            "user_id": str(tx.user_id) if tx.user_id else None,
            "provider": tx.provider,
            "amount": float(tx.amount),
            "currency": tx.currency,
            "source": tx.source,
            "source_reference_id": str(tx.source_reference_id) if tx.source_reference_id else None,
            "failure_reason": tx.failure_reason,
            "failed_at": datetime.now(dt_timezone.utc).isoformat(),
        },
    }
    return _publish_event("payment.failed", payload)


def publish_payment_cancelled(tx: Transaction) -> bool:
    """
    Émet payment.cancelled après annulation via API.
    Consommateurs : Subscription (annuler tentative), Notification (info utilisateur).
    """
    payload = {
        "event_id": str(uuid.uuid4()),
        "event_type": "payment.cancelled",
        "timestamp": datetime.now(dt_timezone.utc).isoformat(),
        "source": "payment-service",
        "idempotency_key": str(tx.idempotency_key),
        "data": {
            "payment_reference_id": str(tx.id),
            "platform_id": str(tx.platform_id),
            "user_id": str(tx.user_id) if tx.user_id else None,
            "source": tx.source,
            "source_reference_id": str(tx.source_reference_id) if tx.source_reference_id else None,
            "cancelled_at": datetime.now(dt_timezone.utc).isoformat(),
        },
    }
    return _publish_event("payment.cancelled", payload)


def publish_payment_expired(tx: Transaction) -> bool:
    """
    Émet payment.expired après expiration du TTL (cron).
    Consommateurs : Subscription (marquer comme non payé), Notification (alerte).
    """
    payload = {
        "event_id": str(uuid.uuid4()),
        "event_type": "payment.expired",
        "timestamp": datetime.now(dt_timezone.utc).isoformat(),
        "source": "payment-service",
        "idempotency_key": str(tx.idempotency_key),
        "data": {
            "payment_reference_id": str(tx.id),
            "platform_id": str(tx.platform_id),
            "user_id": str(tx.user_id) if tx.user_id else None,
            "provider": tx.provider,
            "amount": float(tx.amount),
            "currency": tx.currency,
            "source": tx.source,
            "source_reference_id": str(tx.source_reference_id) if tx.source_reference_id else None,
            "expired_at": datetime.now(dt_timezone.utc).isoformat(),
        },
    }
    return _publish_event("payment.expired", payload)


# ===========================================================================
# SERVICE MÉTIER
# ===========================================================================

class PaymentService:

    @classmethod
    def initiate(cls, platform_id, user_id, provider, amount, currency, source,
                 source_reference_id, idempotency_key, phone_number=None, metadata=None):
        """
        Initie une transaction de paiement.

        Flux :
        1. Vérification idempotence — si clé existante, retourne la transaction existante
        2. Création de la transaction en état PENDING
        3. Appel de l'adapter provider (Orange Money, MTN, Stripe, PayPal)
        4. Mise à jour avec payment_url ou provider_tx_id selon le provider
        """
        # --- Idempotence ---
        # Même clé = même intention de paiement → retourner l'existant sans re-exécuter
        existing = Transaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        ttl = PROVIDER_TTL.get(provider, 600)
        tx = Transaction.objects.create(
            platform_id=platform_id,
            user_id=user_id,
            provider=provider,
            idempotency_key=idempotency_key,
            amount=amount,
            currency=currency,
            source=source,
            source_reference_id=source_reference_id,
            phone_number=phone_number,
            metadata=metadata,
            expires_at=timezone.now() + timedelta(seconds=ttl),
        )

        # Enregistrer la création dans l'historique — null → pending
        TransactionStatusHistory.objects.create(
            transaction=tx,
            from_status=None,
            to_status=TransactionStatus.PENDING,
            trigger="api_call",
        )

        # --- Appel provider ---
        from apps.providers.adapters import get_adapter
        adapter = get_adapter(provider)
        if not adapter:
            tx.transition_to(
                TransactionStatus.FAILED,
                trigger="system",
                metadata={"reason": "provider_not_found"},
            )
            publish_payment_failed(tx)
            return tx, "provider_not_found"

        try:
            result = adapter.initiate_payment(tx)
            if result.get("payment_url"):
                tx.payment_url = result["payment_url"]
                tx.save(update_fields=["payment_url"])
            if result.get("provider_tx_id"):
                tx.provider_tx_id = result["provider_tx_id"]
                tx.save(update_fields=["provider_tx_id"])
        except Exception as e:
            logger.error(f"Provider {provider} initiation failed: {e}")
            tx.transition_to(
                TransactionStatus.FAILED,
                trigger="provider_error",
                metadata={"error": str(e)[:200]},
            )
            publish_payment_failed(tx)
            return tx, "provider_error"

        return tx, None

    @classmethod
    def process_webhook(cls, provider, event_id, payload, headers):
        """
        Traite un webhook entrant d'un provider.

        Sécurité (4 couches appliquées ici) :
        1. Replay protection via Redis (TTL 72h sur event_id)
        2. Normalisation du statut via l'adapter
        3. Vérification de la machine à états avant transition
        4. Émission de l'event RabbitMQ correspondant après transition
        """
        log = WebhookLog.objects.create(
            provider=provider,
            event_id=event_id,
            payload=payload,
            headers=headers,
        )

        from apps.providers.adapters import get_adapter
        adapter = get_adapter(provider)
        if not adapter:
            log.error_message = "adapter_not_found"
            log.save(update_fields=["error_message"])
            return

        # --- Replay protection ---
        # Un même event_id ne peut être traité qu'une seule fois (72h)
        if event_id:
            from django.core.cache import cache
            replay_key = f"wh_replay:{provider}:{event_id}"
            if cache.get(replay_key):
                log.processed = True
                log.error_message = "duplicate_ignored"
                log.save(update_fields=["processed", "error_message"])
                return
            cache.set(replay_key, True, timeout=259200)  # 72h

        try:
            normalized = adapter.normalize_webhook(payload)
            provider_tx_id = normalized.get("provider_tx_id")
            new_status = normalized.get("status")
            raw_status = normalized.get("raw_status")

            # Retrouver la transaction par provider_tx_id ou idempotency_key
            tx = Transaction.objects.filter(
                provider=provider,
                provider_tx_id=provider_tx_id,
            ).first()
            if not tx:
                tx = Transaction.objects.filter(
                    provider=provider,
                    idempotency_key=normalized.get("idempotency_key"),
                ).first()

            if not tx:
                log.error_message = f"transaction_not_found: {provider_tx_id}"
                log.save(update_fields=["error_message"])
                return

            log.transaction = tx
            log.processed = True
            log.save(update_fields=["transaction", "processed"])

            # Si déjà terminal, ignorer (idempotence webhook)
            if tx.is_terminal():
                return

            tx.provider_raw_status = raw_status
            if normalized.get("failure_reason"):
                tx.failure_reason = normalized["failure_reason"]
            tx.save(update_fields=["provider_raw_status", "failure_reason", "updated_at"])

            # --- Transition + émission RabbitMQ ---
            if new_status and tx.can_transition_to(new_status):
                tx.transition_to(new_status, trigger="webhook")

                # Émettre l'événement RabbitMQ selon le nouveau statut
                if new_status == TransactionStatus.SUCCEEDED:
                    publish_payment_confirmed(tx)
                elif new_status == TransactionStatus.FAILED:
                    publish_payment_failed(tx)
                elif new_status == TransactionStatus.CANCELLED:
                    publish_payment_cancelled(tx)

        except Exception as e:
            log.error_message = str(e)[:500]
            log.save(update_fields=["error_message"])
            logger.error(f"Webhook processing error: {e}")

    @classmethod
    def expire_pending(cls):
        """
        Passe les transactions PENDING expirées en EXPIRED.
        Appelé par le cron Celery Beat toutes les minutes.
        Émet payment.expired pour chaque transaction expirée.
        """
        now = timezone.now()
        expired = Transaction.objects.filter(
            status=TransactionStatus.PENDING,
            expires_at__lt=now,
        )
        count = 0
        for tx in expired:
            try:
                tx.transition_to(TransactionStatus.EXPIRED, trigger="cron_expiry")
                publish_payment_expired(tx)
                count += 1
            except ValueError:
                pass
        return count