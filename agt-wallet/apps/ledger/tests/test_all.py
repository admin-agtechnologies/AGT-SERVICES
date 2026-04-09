"""AGT Wallet Service v1.0 - Tests. Double-entry ledger."""
import uuid
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from apps.accounts.models import Account, LedgerEntry, LedgerTransaction, Hold
from apps.ledger.service import LedgerService


def make_account(account_type="user", currency="XAF", balance=0, **kw):
    return Account.objects.create(
        account_type=account_type, owner_type=kw.get("owner_type", "user"),
        owner_id=kw.get("owner_id", uuid.uuid4()), currency=currency,
        balance=Decimal(str(balance)), label=kw.get("label"))


class TestDoubleEntry(TestCase):
    def test_credit_creates_balanced_entries(self):
        acc = make_account(balance=0)
        ltx, err = LedgerService.credit(str(acc.id), 10000, "XAF", uuid.uuid4(), "payment")
        self.assertIsNone(err)
        entries = LedgerEntry.objects.filter(transaction=ltx)
        debits = sum(e.amount for e in entries if e.direction == "debit")
        credits = sum(e.amount for e in entries if e.direction == "credit")
        self.assertEqual(debits, credits)
        acc.refresh_from_db()
        self.assertEqual(acc.balance, Decimal("10000"))

    def test_debit_insufficient_balance(self):
        acc = make_account(balance=100)
        _, err = LedgerService.debit(str(acc.id), 500, "XAF", uuid.uuid4(), "platform")
        self.assertEqual(err, "insufficient_balance")

    def test_debit_success(self):
        acc = make_account(balance=10000)
        ltx, err = LedgerService.debit(str(acc.id), 3000, "XAF", uuid.uuid4(), "platform")
        self.assertIsNone(err)
        acc.refresh_from_db()
        self.assertEqual(acc.balance, Decimal("7000"))

    def test_transfer(self):
        a1 = make_account(balance=5000)
        a2 = make_account(balance=0)
        ltx, err = LedgerService.transfer(str(a1.id), str(a2.id), 2000, "XAF", uuid.uuid4())
        self.assertIsNone(err)
        a1.refresh_from_db()
        a2.refresh_from_db()
        self.assertEqual(a1.balance, Decimal("3000"))
        self.assertEqual(a2.balance, Decimal("2000"))

    def test_split_balanced(self):
        src = make_account(account_type="escrow", balance=10000)
        t1 = make_account(balance=0)
        t2 = make_account(balance=0)
        ltx, err = LedgerService.split(str(src.id), 10000, "XAF", uuid.uuid4(),
                                         [{"account_id": str(t1.id), "amount": 8500},
                                          {"account_id": str(t2.id), "amount": 1500}])
        self.assertIsNone(err)
        src.refresh_from_db()
        t1.refresh_from_db()
        t2.refresh_from_db()
        self.assertEqual(src.balance, Decimal("0"))
        self.assertEqual(t1.balance, Decimal("8500"))
        self.assertEqual(t2.balance, Decimal("1500"))

    def test_split_unbalanced_rejected(self):
        src = make_account(balance=10000)
        t1 = make_account()
        _, err = LedgerService.split(str(src.id), 10000, "XAF", uuid.uuid4(),
                                       [{"account_id": str(t1.id), "amount": 9000}])
        self.assertEqual(err, "split_unbalanced")

    def test_idempotency(self):
        acc = make_account()
        key = uuid.uuid4()
        LedgerService.credit(str(acc.id), 5000, "XAF", uuid.uuid4(), "payment", idempotency_key=key)
        _, err = LedgerService.credit(str(acc.id), 5000, "XAF", uuid.uuid4(), "payment", idempotency_key=key)
        self.assertEqual(err, "idempotent_hit")
        acc.refresh_from_db()
        self.assertEqual(acc.balance, Decimal("5000"))

    def test_frozen_account(self):
        acc = make_account(balance=10000)
        acc.status = "frozen"
        acc.save()
        _, err = LedgerService.credit(str(acc.id), 1000, "XAF", uuid.uuid4(), "payment")
        self.assertEqual(err, "account_frozen")

    def test_hold_and_available_balance(self):
        acc = make_account(balance=10000)
        hold, err = LedgerService.create_hold(str(acc.id), 3000, "XAF", "cashout")
        self.assertIsNone(err)
        acc.refresh_from_db()
        self.assertEqual(acc.hold_amount, Decimal("3000"))
        self.assertEqual(acc.available_balance, Decimal("7000"))

    def test_hold_capture(self):
        acc = make_account(balance=10000)
        hold, _ = LedgerService.create_hold(str(acc.id), 3000, "XAF")
        LedgerService.capture_hold(hold.id, uuid.uuid4())
        hold.refresh_from_db()
        acc.refresh_from_db()
        self.assertEqual(hold.status, "captured")
        self.assertEqual(acc.hold_amount, Decimal("0"))

    def test_hold_release(self):
        acc = make_account(balance=10000)
        hold, _ = LedgerService.create_hold(str(acc.id), 3000, "XAF")
        LedgerService.release_hold(hold.id)
        hold.refresh_from_db()
        acc.refresh_from_db()
        self.assertEqual(hold.status, "released")
        self.assertEqual(acc.hold_amount, Decimal("0"))
        self.assertEqual(acc.available_balance, Decimal("10000"))

    def test_audit_balanced(self):
        acc = make_account()
        LedgerService.credit(str(acc.id), 5000, "XAF", uuid.uuid4(), "payment")
        result = LedgerService.audit_balance()
        self.assertTrue(result["balanced"])
        self.assertEqual(result["anomalies"], 0)


class TestHealthEndpoint(TestCase):
    def test_health(self):
        resp = APIClient().get("/api/v1/wallet/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")
