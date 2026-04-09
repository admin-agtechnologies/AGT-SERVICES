"""
AGT Users Service v1.0 - Modeles Django
Conforme CDC Users v2.1 : profils, adresses, metadata, audit_logs.
Plus de table platforms locale - platform_id = UUID Auth directement.
"""
import uuid
from django.db import models
from django.utils import timezone


class UserStatusChoice(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    DELETED = "deleted", "Deleted"
    DELETION_IN_PROGRESS = "deletion_in_progress", "Deletion In Progress"


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auth_user_id = models.UUIDField(unique=True, db_index=True)
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=255, null=True, blank=True, db_index=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    avatar_url = models.CharField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=30, choices=UserStatusChoice.choices, default=UserStatusChoice.ACTIVE, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    hard_delete_after = models.DateTimeField(null=True, blank=True)
    purge_auth_pending = models.BooleanField(default=False)
    deletion_error_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_profiles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email or self.auth_user_id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def soft_delete(self, hard_delete_delay_days=None):
        from django.conf import settings
        delay = hard_delete_delay_days or getattr(settings, "DEFAULT_HARD_DELETE_DELAY_DAYS", 30)
        self.status = UserStatusChoice.DELETED
        self.deleted_at = timezone.now()
        self.hard_delete_after = timezone.now() + timezone.timedelta(days=delay)
        self.save(update_fields=["status", "deleted_at", "hard_delete_after", "updated_at"])

    def hard_delete(self):
        self.delete()

    def is_active_user(self):
        return self.status == UserStatusChoice.ACTIVE


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="addresses")
    type = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "addresses"
        ordering = ["-is_default", "-created_at"]

    def set_as_default(self):
        Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        self.is_default = True
        self.save(update_fields=["is_default"])


class UserMetadata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="metadata")
    platform_id = models.UUIDField()
    key = models.CharField(max_length=100)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_metadata"
        unique_together = [("user", "platform_id", "key")]
        ordering = ["key"]


class AuditLog(models.Model):
    ACTOR_TYPE_CHOICES = [
        ("user", "User"), ("service", "Service"), ("system", "System"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.CharField(max_length=50)
    entity_id = models.UUIDField()
    action = models.CharField(max_length=30)
    actor_id = models.UUIDField(null=True, blank=True)
    actor_type = models.CharField(max_length=20, choices=ACTOR_TYPE_CHOICES, default="user")
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["entity_type", "entity_id"]),
            models.Index(fields=["actor_id"]),
            models.Index(fields=["created_at"]),
        ]
