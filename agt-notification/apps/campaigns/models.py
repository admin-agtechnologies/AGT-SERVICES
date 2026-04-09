"""AGT Notification Service v1.0 - Modeles : Campaign, CampaignRecipient."""
import uuid
from django.db import models


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    platform_id = models.UUIDField()
    template = models.ForeignKey("templates_mgr.Template", on_delete=models.SET_NULL, null=True, blank=True, related_name="campaigns")
    channel = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="draft", db_index=True)
    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    throttle_per_second = models.IntegerField(default=10)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "campaigns"
        ordering = ["-created_at"]

    @property
    def progress_percent(self):
        if not self.total_recipients:
            return 0.0
        return round((self.sent_count + self.failed_count) / self.total_recipients * 100, 1)

    def cancel(self):
        self.status = "cancelled"
        self.save(update_fields=["status"])


class CampaignRecipient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="recipients")
    user_id = models.UUIDField()
    notification = models.ForeignKey("notifications.Notification", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default="pending")
    variables = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "campaign_recipients"
        ordering = ["created_at"]
