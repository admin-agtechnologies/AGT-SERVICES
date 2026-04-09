"""AGT Payment Service v1.0 - Payment initiation and lifecycle."""
import logging
import uuid
from datetime import timedelta
from django.utils import timezone
from apps.payments.models import Transaction, TransactionStatus, WebhookLog

logger = logging.getLogger(__name__)

PROVIDER_TTL = {"orange_money": 300, "mtn_momo": 300, "stripe": 1800, "paypal": 3600}


class PaymentService:

    @classmethod
    def initiate(cls, platform_id, user_id, provider, amount, currency, source, source_reference_id, idempotency_key, phone_number=None, metadata=None):
        # Idempotency
        existing = Transaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        ttl = PROVIDER_TTL.get(provider, 600)
        tx = Transaction.objects.create(
            platform_id=platform_id, user_id=user_id, provider=provider,
            idempotency_key=idempotency_key, amount=amount, currency=currency,
            source=source, source_reference_id=source_reference_id,
            phone_number=phone_number, metadata=metadata,
            expires_at=timezone.now() + timedelta(seconds=ttl),
        )

        # Appeler le provider
        from apps.providers.adapters import get_adapter
        adapter = get_adapter(provider)
        if not adapter:
            tx.transition_to(TransactionStatus.FAILED, trigger="system", metadata={"reason": "provider_not_found"})
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
            tx.transition_to(TransactionStatus.FAILED, trigger="provider_error", metadata={"error": str(e)[:200]})
            return tx, "provider_error"

        return tx, None

    @classmethod
    def process_webhook(cls, provider, event_id, payload, headers):
        log = WebhookLog.objects.create(provider=provider, event_id=event_id, payload=payload, headers=headers)

        from apps.providers.adapters import get_adapter
        adapter = get_adapter(provider)
        if not adapter:
            log.error_message = "adapter_not_found"
            log.save(update_fields=["error_message"])
            return

        # Replay protection
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

            tx = Transaction.objects.filter(provider=provider, provider_tx_id=provider_tx_id).first()
            if not tx:
                tx = Transaction.objects.filter(provider=provider, idempotency_key=normalized.get("idempotency_key")).first()

            if not tx:
                log.error_message = f"transaction_not_found: {provider_tx_id}"
                log.save(update_fields=["error_message"])
                return

            log.transaction = tx
            log.processed = True
            log.save(update_fields=["transaction", "processed"])

            if tx.is_terminal():
                return

            tx.provider_raw_status = raw_status
            if normalized.get("failure_reason"):
                tx.failure_reason = normalized["failure_reason"]
            tx.save(update_fields=["provider_raw_status", "failure_reason", "updated_at"])

            if new_status and tx.can_transition_to(new_status):
                tx.transition_to(new_status, trigger="webhook")
                # TODO: emit RabbitMQ event payment.confirmed / payment.failed

        except Exception as e:
            log.error_message = str(e)[:500]
            log.save(update_fields=["error_message"])
            logger.error(f"Webhook processing error: {e}")

    @classmethod
    def expire_pending(cls):
        now = timezone.now()
        expired = Transaction.objects.filter(status=TransactionStatus.PENDING, expires_at__lt=now)
        count = 0
        for tx in expired:
            try:
                tx.transition_to(TransactionStatus.EXPIRED, trigger="cron_expiry")
                count += 1
            except ValueError:
                pass
        return count
