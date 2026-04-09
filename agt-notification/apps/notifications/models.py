"""
AGT Notification Service v1.0 - Modeles principaux.
"""
import uuid
from django.db import models
from django.utils import timezone


class ChannelChoice(models.TextChoices):
    EMAIL = "email", "Email"
    SMS = "sms", "SMS"
    PUSH = "push", "Push"
    IN_APP = "in_app", "In-App"
    WHATSAPP = "whatsapp", "WhatsApp"


class CategoryChoice(models.TextChoices):
    TRANSACTIONAL = "transactional", "Transactionnel"
    MARKETING = "marketing", "Marketing"
    SECURITY = "security", "Securite"


class NotificationStatus(models.TextChoices):
    PENDING = "pending", "En attente"
    SENT = "sent", "Envoye"
    DELIVERED = "delivered", "Livre"
    READ = "read", "Lu"
    FAILED = "failed", "Echoue"


class PriorityChoice(models.TextChoices):
    LOW = "low", "Faible"
    NORMAL = "normal", "Normal"
    HIGH = "high", "Haute"
    CRITICAL = "critical", "Critique"


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    platform_id = models.UUIDField(db_index=True)
    template = models.ForeignKey("templates_mgr.Template", on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    channel = models.CharField(max_length=20, choices=ChannelChoice.choices, db_index=True)
    category = models.CharField(max_length=30, choices=CategoryChoice.choices)
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=NotificationStatus.choices, default=NotificationStatus.PENDING, db_index=True)
    priority = models.CharField(max_length=10, choices=PriorityChoice.choices, default=PriorityChoice.NORMAL)
    metadata = models.JSONField(null=True, blank=True)
    idempotency_key = models.CharField(max_length=100, null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["platform_id", "idempotency_key"], name="unique_platform_idempotency", condition=models.Q(idempotency_key__isnull=False))
        ]
        indexes = [models.Index(fields=["user_id", "channel"]), models.Index(fields=["user_id", "status"])]

    @property
    def is_read(self):
        return self.read_at is not None

    def mark_as_read(self):
        self.read_at = timezone.now()
        self.status = NotificationStatus.READ
        self.save(update_fields=["read_at", "status"])

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def mark_sent(self):
        self.status = NotificationStatus.SENT
        self.sent_at = timezone.now()
        self.save(update_fields=["status", "sent_at"])

    def mark_failed(self):
        self.status = NotificationStatus.FAILED
        self.save(update_fields=["status"])


class NotificationLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="logs")
    channel = models.CharField(max_length=20, choices=ChannelChoice.choices)
    provider = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    attempt = models.IntegerField()
    error_message = models.TextField(null=True, blank=True)
    provider_message_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification_logs"
        ordering = ["-created_at"]


class UserPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    platform_id = models.UUIDField()
    channel_email = models.BooleanField(default=True)
    channel_sms = models.BooleanField(default=True)
    channel_push = models.BooleanField(default=True)
    channel_whatsapp = models.BooleanField(default=True)
    channel_in_app = models.BooleanField(default=True)
    cat_transactional = models.BooleanField(default=True)
    cat_marketing = models.BooleanField(default=False)
    cat_security = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_preferences"
        unique_together = [("user_id", "platform_id")]

    def is_channel_enabled(self, channel):
        return getattr(self, f"channel_{channel}", True)

    def is_category_enabled(self, category):
        if category == "security":
            return True
        return getattr(self, f"cat_{category}", True)


class ScheduledNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    platform_id = models.UUIDField()
    template = models.ForeignKey("templates_mgr.Template", on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.CharField(max_length=20, choices=ChannelChoice.choices)
    variables = models.JSONField(null=True, blank=True)
    scheduled_at = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=20, default="pending")
    notification = models.ForeignKey(Notification, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "scheduled_notifications"
        ordering = ["scheduled_at"]


class PlatformChannelConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(unique=True)
    priority_order = models.JSONField(default=list)
    fallback_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platform_channel_config"

    DEFAULT_ORDER = ["email", "push", "in_app", "whatsapp", "sms"]

    @classmethod
    def get_for_platform(cls, platform_id):
        try:
            return cls.objects.get(platform_id=platform_id)
        except cls.DoesNotExist:
            return cls(platform_id=platform_id, priority_order=cls.DEFAULT_ORDER, fallback_enabled=True)
