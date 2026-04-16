"""AGT Wallet Service v1.0 - Modeles. Double-entry ledger, append-only."""
import uuid
from django.db import models
from django.utils import timezone


class AccountType(models.TextChoices):
    USER = "user", "User"
    ORGANIZATION = "organization", "Organization"
    PLATFORM_SYSTEM = "platform_system", "Platform System"
    ESCROW = "escrow", "Escrow"
    EXTERNAL = "external", "External"


class AccountStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    FROZEN = "frozen", "Frozen"
    CLOSED = "closed", "Closed"


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    owner_type = models.CharField(max_length=20)  # user, organization, system
    owner_id = models.UUIDField(null=True, blank=True, db_index=True)
    currency = models.CharField(max_length=3, default="XAF")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    hold_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    label = models.CharField(max_length=100, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "accounts"
        ordering = ["-created_at"]

    @property
    def available_balance(self):
        return self.balance - self.hold_amount

    def is_frozen(self):
        return self.status == AccountStatus.FROZEN

    def can_debit(self, amount):
        # Les comptes externes peuvent avoir un solde négatif (représente les entrées/sorties réelles)
        if self.account_type == AccountType.EXTERNAL:
            return True
        return self.available_balance >= amount


class LedgerTransaction(models.Model):
    TX_TYPES = [
        ("cashin", "Cash In"), ("cashout", "Cash Out"), ("transfer", "Transfer"),
        ("split", "Split"), ("hold_capture", "Hold Capture"), ("hold_release", "Hold Release"),
        ("adjustment", "Adjustment"), ("reversal", "Reversal"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ledger_reference_id = models.CharField(max_length=30, unique=True)
    idempotency_key = models.UUIDField(unique=True)
    transaction_type = models.CharField(max_length=30, choices=TX_TYPES)
    platform_id = models.UUIDField()
    source = models.CharField(max_length=30)  # payment, platform, admin, cron
    source_reference_id = models.UUIDField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default="completed")  # completed, reversed
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ledger_transactions"
        ordering = ["-created_at"]

    @staticmethod
    def generate_reference():
        from django.utils.timezone import now
        year = now().year
        last = LedgerTransaction.objects.filter(ledger_reference_id__startswith=f"LTX-{year}").count()
        return f"LTX-{year}-{str(last + 1).zfill(6)}"


class LedgerEntry(models.Model):
    DIRECTION_CHOICES = [("debit", "Debit"), ("credit", "Credit")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(LedgerTransaction, on_delete=models.CASCADE, related_name="entries")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="entries")
    direction = models.CharField(max_length=6, choices=DIRECTION_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ledger_entries"
        ordering = ["created_at"]
        indexes = [models.Index(fields=["account", "created_at"])]


class HoldStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CAPTURED = "captured", "Captured"
    RELEASED = "released", "Released"
    EXPIRED = "expired", "Expired"


class Hold(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="holds")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=HoldStatus.choices, default=HoldStatus.PENDING)
    reason = models.CharField(max_length=50)
    reference_id = models.UUIDField(null=True, blank=True)
    idempotency_key = models.UUIDField(unique=True)
    expires_at = models.DateTimeField()
    captured_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "holds"
        ordering = ["-created_at"]


class CashoutRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"), ("processing", "Processing"),
        ("completed", "Completed"), ("failed", "Failed"), ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cashout_requests")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default="XAF")
    destination_provider = models.CharField(max_length=30)
    destination_details = models.JSONField()
    status = models.CharField(max_length=20, default="pending")
    hold = models.ForeignKey(Hold, on_delete=models.SET_NULL, null=True, blank=True)
    payment_tx_id = models.UUIDField(null=True, blank=True)
    idempotency_key = models.UUIDField(unique=True)
    failure_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cashout_requests"
        ordering = ["-created_at"]


class SplitRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField()
    name = models.CharField(max_length=100)
    # Définition des parts : [{"target": "seller", "percent": 85}, {"target": "platform", "percent": 15}]
    rules = models.JSONField()
    is_active = models.BooleanField(default=True)  # Permet de désactiver sans supprimer
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "split_rules"
        unique_together = [("platform_id", "name")]