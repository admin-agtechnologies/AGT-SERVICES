"""AGT Payment Service v1.0 - Provider adapters (Strategy pattern)."""
import logging
import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class BaseAdapter:
    name = "base"

    def initiate_payment(self, transaction):
        raise NotImplementedError

    def normalize_webhook(self, payload):
        raise NotImplementedError


class OrangeMoneyAdapter(BaseAdapter):
    name = "orange_money"

    def initiate_payment(self, tx):
        logger.info(f"[ORANGE] USSD push to {tx.phone_number} for {tx.amount} {tx.currency}")
        # En production: appel API Orange Money
        return {"provider_tx_id": f"OM-{tx.id.hex[:8]}"}

    def normalize_webhook(self, payload):
        status_map = {"SUCCESS": "succeeded", "FAILED": "failed", "EXPIRED": "expired", "INITIATED": "pending", "PENDING": "processing"}
        raw = payload.get("status", "")
        return {
            "provider_tx_id": payload.get("txnid") or payload.get("transaction_id"),
            "status": status_map.get(raw, "pending"),
            "raw_status": raw,
            "failure_reason": payload.get("error_message"),
        }


class MTNMoMoAdapter(BaseAdapter):
    name = "mtn_momo"

    def initiate_payment(self, tx):
        logger.info(f"[MTN] USSD push to {tx.phone_number} for {tx.amount} {tx.currency}")
        return {"provider_tx_id": f"MTN-{tx.id.hex[:8]}"}

    def normalize_webhook(self, payload):
        status_map = {"SUCCESSFUL": "succeeded", "FAILED": "failed", "EXPIRED": "expired", "PENDING": "processing"}
        raw = payload.get("status", "")
        return {
            "provider_tx_id": payload.get("externalId") or payload.get("referenceId"),
            "status": status_map.get(raw, "pending"),
            "raw_status": raw,
            "failure_reason": payload.get("reason"),
        }


class StripeAdapter(BaseAdapter):
    name = "stripe"

    def initiate_payment(self, tx):
        logger.info(f"[STRIPE] Creating checkout session for {tx.amount} {tx.currency}")
        # En production: appel Stripe API
        return {
            "provider_tx_id": f"cs_{tx.id.hex[:12]}",
            "payment_url": f"https://checkout.stripe.com/pay/cs_{tx.id.hex[:12]}",
        }

    def normalize_webhook(self, payload):
        event_type = payload.get("type", "")
        status_map = {
            "payment_intent.succeeded": "succeeded",
            "payment_intent.payment_failed": "failed",
            "payment_intent.canceled": "cancelled",
            "payment_intent.created": "pending",
            "payment_intent.processing": "processing",
        }
        obj = payload.get("data", {}).get("object", {})
        return {
            "provider_tx_id": obj.get("id"),
            "status": status_map.get(event_type, "pending"),
            "raw_status": event_type,
            "failure_reason": obj.get("last_payment_error", {}).get("message") if isinstance(obj.get("last_payment_error"), dict) else None,
        }


class PayPalAdapter(BaseAdapter):
    name = "paypal"

    def initiate_payment(self, tx):
        logger.info(f"[PAYPAL] Creating order for {tx.amount} {tx.currency}")
        return {
            "provider_tx_id": f"PP-{tx.id.hex[:8]}",
            "payment_url": f"https://www.paypal.com/checkoutnow?token=PP-{tx.id.hex[:8]}",
        }

    def normalize_webhook(self, payload):
        event_type = payload.get("event_type", "")
        status_map = {"PAYMENT.CAPTURE.COMPLETED": "succeeded", "PAYMENT.CAPTURE.DENIED": "failed", "CHECKOUT.ORDER.APPROVED": "processing"}
        resource = payload.get("resource", {})
        return {
            "provider_tx_id": resource.get("id"),
            "status": status_map.get(event_type, "pending"),
            "raw_status": event_type,
        }


ADAPTERS = {
    "orange_money": OrangeMoneyAdapter(),
    "mtn_momo": MTNMoMoAdapter(),
    "stripe": StripeAdapter(),
    "paypal": PayPalAdapter(),
}


def get_adapter(provider):
    return ADAPTERS.get(provider)
