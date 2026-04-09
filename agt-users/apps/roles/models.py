"""
AGT Users Service v1.0 - Modeles : Role, Permission, UserRole, RolePermission.
RBAC 100% dynamique. platform_id = UUID Auth directement (pas de table locale).
"""
import uuid
from django.db import models


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "roles"
        unique_together = [("platform_id", "name")]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} @ {self.platform_id}"


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "permissions"
        unique_together = [("platform_id", "name")]
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} @ {self.platform_id}"


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="role_permissions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "role_permissions"
        unique_together = [("role", "permission")]


class UserRole(models.Model):
    """CDC v2.1 : unique_together = (user, role). platform_id retire car redondant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")
    assigned_by = models.UUIDField(null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_roles"
        unique_together = [("user", "role")]
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.user} -> {self.role.name}"
