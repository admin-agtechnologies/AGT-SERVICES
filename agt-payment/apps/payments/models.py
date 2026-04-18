"""AGT Payment Service v1.0 - Modeles."""
import uuid
from django.db import models
from django.utils import timezone


class TransactionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"


TERMINAL_STATUSES = {TransactionStatus.SUCCEEDED, TransactionStatus.FAILED, TransactionStatus.EXPIRED, TransactionStatus.CANCELLED}

VALID_TRANSITIONS = {
    None: {TransactionStatus.PENDING},
    TransactionStatus.PENDING: {TransactionStatus.PROCESSING, TransactionStatus.SUCCEEDED, TransactionStatus.FAILED, TransactionStatus.EXPIRED, TransactionStatus.CANCELLED},
    TransactionStatus.PROCESSING: {TransactionStatus.SUCCEEDED, TransactionStatus.FAILED, TransactionStatus.EXPIRED},
}


class Transaction(models.Model):
    PROVIDER_CHOICES = [("orange_money", "Orange Money"), ("mtn_momo", "MTN MoMo"), ("stripe", "Stripe"), ("paypal", "PayPal")]
    SOURCE_CHOICES = [
    ("subscription", "Subscription"),
    ("wallet", "Wallet"),
    ("platform", "Platform"),
    ("manual", "Manual"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    provider = models.CharField(max_length=30, choices=PROVIDER_CHOICES)
    provider_tx_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    idempotency_key = models.UUIDField(unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="XAF")
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, default=TransactionStatus.PENDING, db_index=True)
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES)
    source_reference_id = models.UUIDField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    payment_url = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    failure_reason = models.TextField(null=True, blank=True)
    provider_raw_status = models.CharField(max_length=50, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["platform_id", "status"]), models.Index(fields=["source", "source_reference_id"])]

    def can_transition_to(self, new_status):
        allowed = VALID_TRANSITIONS.get(self.status, set())
        return new_status in allowed

    def transition_to(self, new_status, trigger="system", metadata=None):
        if not self.can_transition_to(new_status):
            raise ValueError(f"Transition {self.status} -> {new_status} interdite")
        old = self.status
        self.status = new_status
        if new_status == TransactionStatus.SUCCEEDED:
            self.confirmed_at = timezone.now()
        updates = ["status", "updated_at"]
        if self.confirmed_at:
            updates.append("confirmed_at")
        self.save(update_fields=updates)
        TransactionStatusHistory.objects.create(transaction=self, from_status=old, to_status=new_status, trigger=trigger, metadata=metadata)

    def is_terminal(self):
        return self.status in TERMINAL_STATUSES


class TransactionStatusHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="status_history")
    from_status = models.CharField(max_length=20, null=True, blank=True)
    to_status = models.CharField(max_length=20)
    trigger = models.CharField(max_length=30, default="system")
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transaction_status_history"
        ordering = ["created_at"]


class WebhookLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=30)
    event_id = models.CharField(max_length=255, null=True, blank=True)
    payload = models.JSONField()
    headers = models.JSONField(null=True, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name="webhook_logs")
    processed = models.BooleanField(default=False)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "webhook_logs"
        ordering = ["-created_at"]


class ProviderConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=30, unique=True)
    display_name = models.CharField(max_length=100)
    credentials_encrypted = models.JSONField(default=dict)
    api_base_url = models.TextField(null=True, blank=True)
    webhook_secret_encrypted = models.CharField(max_length=500, null=True, blank=True)
    supported_currencies = models.JSONField(default=list)
    config = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "provider_configs"


class PlatformPaymentConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(unique=True)
    providers_priority = models.JSONField(default=list)
    default_currency = models.CharField(max_length=3, default="XAF")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platform_payment_config"

    @classmethod
    def get_for_platform(cls, platform_id):
        try:
            return cls.objects.get(platform_id=platform_id)
        except cls.DoesNotExist:
            return cls(platform_id=platform_id, providers_priority=["orange_money", "stripe"], default_currency="XAF")
        
        
class ReconciliationReport(models.Model):
    """
    Rapport de réconciliation provider ↔ transactions internes.
    Généré automatiquement par le cron Celery toutes les 6h.
    Permet de détecter les anomalies financières entre ce que Payment
    a enregistré et ce que le provider a réellement traité.
    """
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(
        max_length=30,
        db_index=True,
        help_text="Provider concerné : orange_money, mtn_momo, stripe, paypal"
    )
    period_start = models.DateTimeField(
        help_text="Début de la période analysée"
    )
    period_end = models.DateTimeField(
        help_text="Fin de la période analysée"
    )
    total_internal = models.IntegerField(
        default=0,
        help_text="Nombre de transactions dans notre base sur cette période"
    )
    total_provider = models.IntegerField(
        default=0,
        help_text="Nombre de transactions chez le provider sur cette période"
    )
    matched = models.IntegerField(
        default=0,
        help_text="Transactions concordantes des deux côtés"
    )
    mismatched = models.IntegerField(
        default=0,
        help_text="Transactions présentes des deux côtés mais avec anomalie (montant différent)"
    )
    missing_internal = models.IntegerField(
        default=0,
        help_text="Présentes chez le provider mais absentes dans notre base — anormal"
    )
    missing_provider = models.IntegerField(
        default=0,
        help_text="Présentes dans notre base mais absentes chez le provider — critique"
    )
    details = models.JSONField(
        null=True, blank=True,
        help_text="Détail des anomalies : IDs concernés, montants, descriptions"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="completed",
        help_text="completed = rapport généré avec succès, failed = erreur lors de la génération"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de génération du rapport"
    )

    class Meta:
        db_table = "reconciliation_reports"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["provider", "created_at"]),
        ]

    def __str__(self):
        return f"Reconciliation {self.provider} {self.period_start.date()} → {self.period_end.date()} [{self.status}]"
