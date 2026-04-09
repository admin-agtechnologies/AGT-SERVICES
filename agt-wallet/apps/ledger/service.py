"""AGT Wallet Service v1.0 - Ledger service. Double-entry bookkeeping. Append-only."""
import logging
from decimal import Decimal
from django.db import transaction as db_transaction
from django.utils import timezone
from apps.accounts.models import Account, LedgerTransaction, LedgerEntry, Hold, HoldStatus

logger = logging.getLogger(__name__)


class LedgerService:

    @classmethod
    def credit(cls, account_id, amount, currency, platform_id, source, source_reference_id, idempotency_key, description=None):
        return cls._single_entry("cashin", account_id, Decimal(str(amount)), currency, platform_id, source, source_reference_id, idempotency_key, description, direction="credit")

    @classmethod
    def debit(cls, account_id, amount, currency, platform_id, source, source_reference_id, idempotency_key, description=None):
        return cls._single_entry("cashout", account_id, Decimal(str(amount)), currency, platform_id, source, source_reference_id, idempotency_key, description, direction="debit")

    @classmethod
    def transfer(cls, from_account_id, to_account_id, amount, currency, platform_id, idempotency_key, description=None):
        existing = LedgerTransaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        amount = Decimal(str(amount))
        with db_transaction.atomic():
            from_acc = Account.objects.select_for_update().get(id=from_account_id)
            to_acc = Account.objects.select_for_update().get(id=to_account_id)

            if from_acc.is_frozen() or to_acc.is_frozen():
                return None, "account_frozen"
            if not from_acc.can_debit(amount):
                return None, "insufficient_balance"

            ltx = LedgerTransaction.objects.create(
                ledger_reference_id=LedgerTransaction.generate_reference(),
                idempotency_key=idempotency_key, transaction_type="transfer",
                platform_id=platform_id, source="platform", description=description,
            )

            from_acc.balance -= amount
            from_acc.save(update_fields=["balance", "updated_at"])
            LedgerEntry.objects.create(transaction=ltx, account=from_acc, direction="debit", amount=amount, balance_after=from_acc.balance)

            to_acc.balance += amount
            to_acc.save(update_fields=["balance", "updated_at"])
            LedgerEntry.objects.create(transaction=ltx, account=to_acc, direction="credit", amount=amount, balance_after=to_acc.balance)

        return ltx, None

    @classmethod
    def split(cls, source_account_id, amount, currency, platform_id, targets, idempotency_key, source_reference_id=None, description=None):
        existing = LedgerTransaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        amount = Decimal(str(amount))
        total_credit = sum(Decimal(str(t["amount"])) for t in targets)
        if total_credit != amount:
            return None, "split_unbalanced"

        with db_transaction.atomic():
            source_acc = Account.objects.select_for_update().get(id=source_account_id)
            if source_acc.is_frozen():
                return None, "account_frozen"
            if not source_acc.can_debit(amount):
                return None, "insufficient_balance"

            ltx = LedgerTransaction.objects.create(
                ledger_reference_id=LedgerTransaction.generate_reference(),
                idempotency_key=idempotency_key, transaction_type="split",
                platform_id=platform_id, source="platform",
                source_reference_id=source_reference_id, description=description,
            )

            source_acc.balance -= amount
            source_acc.save(update_fields=["balance", "updated_at"])
            LedgerEntry.objects.create(transaction=ltx, account=source_acc, direction="debit", amount=amount, balance_after=source_acc.balance)

            for t in targets:
                target_acc = Account.objects.select_for_update().get(id=t["account_id"])
                t_amount = Decimal(str(t["amount"]))
                target_acc.balance += t_amount
                target_acc.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=target_acc, direction="credit", amount=t_amount, balance_after=target_acc.balance)

        return ltx, None

    @classmethod
    def create_hold(cls, account_id, amount, reason, idempotency_key, expires_seconds=3600, reference_id=None):
        existing = Hold.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        amount = Decimal(str(amount))
        with db_transaction.atomic():
            acc = Account.objects.select_for_update().get(id=account_id)
            if acc.is_frozen():
                return None, "account_frozen"
            if not acc.can_debit(amount):
                return None, "insufficient_balance"

            acc.hold_amount += amount
            acc.save(update_fields=["hold_amount", "updated_at"])

            hold = Hold.objects.create(account=acc, amount=amount, reason=reason, reference_id=reference_id,
                                        idempotency_key=idempotency_key, expires_at=timezone.now() + timezone.timedelta(seconds=expires_seconds))
        return hold, None

    @classmethod
    def capture_hold(cls, hold_id, capture_amount=None):
        with db_transaction.atomic():
            try:
                hold = Hold.objects.select_for_update().get(id=hold_id, status=HoldStatus.PENDING)
            except Hold.DoesNotExist:
                return None, "hold_not_found"
            amount = Decimal(str(capture_amount)) if capture_amount else hold.amount
            acc = Account.objects.select_for_update().get(id=hold.account_id)
            hold.status = HoldStatus.CAPTURED
            hold.captured_amount = amount
            hold.resolved_at = timezone.now()
            hold.save(update_fields=["status", "captured_amount", "resolved_at"])
            acc.hold_amount -= hold.amount
            acc.balance -= amount
            acc.save(update_fields=["hold_amount", "balance", "updated_at"])
        return hold, None

    @classmethod
    def release_hold(cls, hold_id):
        with db_transaction.atomic():
            try:
                hold = Hold.objects.select_for_update().get(id=hold_id, status=HoldStatus.PENDING)
            except Hold.DoesNotExist:
                return None, "hold_not_found"
            acc = Account.objects.select_for_update().get(id=hold.account_id)
            acc.hold_amount -= hold.amount
            acc.save(update_fields=["hold_amount", "updated_at"])
            hold.status = HoldStatus.RELEASED
            hold.resolved_at = timezone.now()
            hold.save(update_fields=["status", "resolved_at"])
        return hold, None

    @classmethod
    def _single_entry(cls, tx_type, account_id, amount, currency, platform_id, source, source_reference_id, idempotency_key, description, direction):
        existing = LedgerTransaction.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            return existing, "idempotent_hit"

        with db_transaction.atomic():
            acc = Account.objects.select_for_update().get(id=account_id)
            if acc.is_frozen():
                return None, "account_frozen"
            if direction == "debit" and not acc.can_debit(amount):
                return None, "insufficient_balance"

            external = Account.objects.filter(account_type="external", currency=currency).first()
            if not external:
                external = Account.objects.create(account_type="external", owner_type="system", currency=currency, label=f"External {currency}")

            ltx = LedgerTransaction.objects.create(
                ledger_reference_id=LedgerTransaction.generate_reference(),
                idempotency_key=idempotency_key, transaction_type=tx_type,
                platform_id=platform_id, source=source, source_reference_id=source_reference_id, description=description,
            )

            if direction == "credit":
                external.balance -= amount
                external.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=external, direction="debit", amount=amount, balance_after=external.balance)
                acc.balance += amount
                acc.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=acc, direction="credit", amount=amount, balance_after=acc.balance)
            else:
                acc.balance -= amount
                acc.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=acc, direction="debit", amount=amount, balance_after=acc.balance)
                external.balance += amount
                external.save(update_fields=["balance", "updated_at"])
                LedgerEntry.objects.create(transaction=ltx, account=external, direction="credit", amount=amount, balance_after=external.balance)

        return ltx, None

    @classmethod
    def verify_integrity(cls):
        from django.db.models import Sum
        debits = LedgerEntry.objects.filter(direction="debit").aggregate(s=Sum("amount"))["s"] or 0
        credits = LedgerEntry.objects.filter(direction="credit").aggregate(s=Sum("amount"))["s"] or 0
        return {"balanced": debits == credits, "total_debits": float(debits), "total_credits": float(credits)}
