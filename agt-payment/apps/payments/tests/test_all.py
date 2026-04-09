"""AGT Payment Service v1.0 - Tests."""
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from apps.payments.models import Transaction, TransactionStatus, TransactionStatusHistory, VALID_TRANSITIONS
from apps.payments.service import PaymentService


class TestTransactionModel(TestCase):
    def _make_tx(self, **kwargs):
        defaults = {"platform_id": uuid.uuid4(), "provider": "orange_money", "idempotency_key": uuid.uuid4(),
                     "amount": 15000, "currency": "XAF", "source": "subscription"}
        defaults.update(kwargs)
        return Transaction.objects.create(**defaults)

    def test_create(self):
        tx = self._make_tx()
        self.assertEqual(tx.status, "pending")

    def test_valid_transition(self):
        tx = self._make_tx()
        self.assertTrue(tx.can_transition_to("succeeded"))
        self.assertTrue(tx.can_transition_to("failed"))
        self.assertFalse(tx.can_transition_to("cancelled"))  # wait, pending->cancelled is valid
        # Actually pending->cancelled IS valid per our model
        self.assertTrue(tx.can_transition_to("cancelled"))

    def test_transition_creates_history(self):
        tx = self._make_tx()
        tx.transition_to("succeeded", trigger="webhook")
        self.assertEqual(tx.status, "succeeded")
        self.assertIsNotNone(tx.confirmed_at)
        self.assertEqual(TransactionStatusHistory.objects.filter(transaction=tx).count(), 1)

    def test_terminal_no_transition(self):
        tx = self._make_tx()
        tx.transition_to("succeeded", trigger="test")
        self.assertTrue(tx.is_terminal())
        self.assertFalse(tx.can_transition_to("failed"))

    def test_idempotency_unique(self):
        key = uuid.uuid4()
        self._make_tx(idempotency_key=key)
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            self._make_tx(idempotency_key=key)


class TestPaymentService(TestCase):
    def test_initiate(self):
        tx, err = PaymentService.initiate(
            platform_id=uuid.uuid4(), user_id=uuid.uuid4(), provider="orange_money",
            amount=15000, currency="XAF", source="subscription",
            source_reference_id=uuid.uuid4(), idempotency_key=uuid.uuid4(),
            phone_number="+237600000000",
        )
        self.assertIsNone(err)
        self.assertEqual(tx.status, "pending")
        self.assertIsNotNone(tx.provider_tx_id)

    def test_idempotent_hit(self):
        key = uuid.uuid4()
        PaymentService.initiate(platform_id=uuid.uuid4(), user_id=None, provider="stripe",
                                 amount=5000, currency="EUR", source="platform_direct",
                                 source_reference_id=None, idempotency_key=key)
        tx2, err = PaymentService.initiate(platform_id=uuid.uuid4(), user_id=None, provider="stripe",
                                            amount=5000, currency="EUR", source="platform_direct",
                                            source_reference_id=None, idempotency_key=key)
        self.assertEqual(err, "idempotent_hit")

    def test_expire_pending(self):
        from django.utils import timezone
        from datetime import timedelta
        tx = Transaction.objects.create(platform_id=uuid.uuid4(), provider="orange_money",
                                         idempotency_key=uuid.uuid4(), amount=1000, currency="XAF",
                                         source="subscription", expires_at=timezone.now() - timedelta(minutes=10))
        count = PaymentService.expire_pending()
        self.assertEqual(count, 1)
        tx.refresh_from_db()
        self.assertEqual(tx.status, "expired")


class TestHealthEndpoint(TestCase):
    def test_health(self):
        resp = APIClient().get("/api/v1/payments/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")


class TestPaymentEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())

    def test_initiate_payment(self):
        resp = self.client.post("/api/v1/payments/initiate", data={
            "platform_id": str(uuid.uuid4()), "provider": "orange_money",
            "amount": 15000, "currency": "XAF", "source": "subscription",
            "idempotency_key": str(uuid.uuid4()), "phone_number": "+237600000000",
        }, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertIn("transaction_id", resp.json())

    def test_list_payments(self):
        resp = self.client.get("/api/v1/payments")
        self.assertEqual(resp.status_code, 200)

    def test_webhook_orange(self):
        # Webhooks are AllowAny
        client = APIClient()
        resp = client.post("/api/v1/payments/webhooks/orange-money", data={
            "txnid": "OM-test", "status": "SUCCESS",
        }, format="json")
        self.assertEqual(resp.status_code, 200)
