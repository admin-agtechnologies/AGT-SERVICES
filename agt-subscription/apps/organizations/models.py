"""AGT Subscription Service v1.0 - Organizations B2B."""
import uuid
from django.db import models


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=150)
    owner_user_id = models.UUIDField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organizations"
        unique_together = [("platform_id", "name")]

    def __str__(self):
        return f"{self.name} @ {self.platform_id}"


class OrganizationMember(models.Model):
    ROLE_CHOICES = [("owner", "Owner"), ("member", "Member")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    user_id = models.UUIDField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "organization_members"
        unique_together = [("organization", "user_id")]
