"""AGT Notification Service v1.0 - Modele DeviceToken (push FCM/APNs)."""
import uuid
from django.db import models


class DeviceToken(models.Model):
    DEVICE_TYPES = [("android", "Android"), ("ios", "iOS"), ("web", "Web")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(db_index=True)
    platform_id = models.UUIDField()
    token = models.TextField()
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    device_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "device_tokens"
        constraints = [models.UniqueConstraint(fields=["user_id", "token"], name="unique_user_token")]
        indexes = [models.Index(fields=["user_id", "is_active"])]

    @classmethod
    def deactivate_all_for_user(cls, user_id):
        return cls.objects.filter(user_id=user_id, is_active=True).update(is_active=False)
