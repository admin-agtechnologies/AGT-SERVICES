"""
AGT Users Service v1.0 - Modeles : Document, DocumentHistory.
"""
import uuid
from django.db import models
from django.utils import timezone


class DocumentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    VALIDATED = "validated", "Validated"
    REJECTED = "rejected", "Rejected"


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE, related_name="documents")
    platform_id = models.UUIDField()
    doc_type = models.CharField(max_length=100)
    media_id = models.UUIDField()
    status = models.CharField(max_length=20, choices=DocumentStatus.choices, default=DocumentStatus.PENDING)
    comment = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents"
        ordering = ["-submitted_at"]

    def archive_and_resubmit(self, new_media_id):
        """Archive la version actuelle et met a jour avec le nouveau media."""
        DocumentHistory.objects.create(
            document=self,
            media_id=self.media_id,
            status=self.status,
            comment=self.comment,
            submitted_at=self.submitted_at,
            reviewed_at=self.reviewed_at,
        )
        self.media_id = new_media_id
        self.status = DocumentStatus.PENDING
        self.comment = None
        self.reviewed_at = None
        self.submitted_at = timezone.now()
        self.save()


class DocumentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="history")
    media_id = models.UUIDField()
    status = models.CharField(max_length=20)
    comment = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField()
    reviewed_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document_history"
        ordering = ["-archived_at"]
