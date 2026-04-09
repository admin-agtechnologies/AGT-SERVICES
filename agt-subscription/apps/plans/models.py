"""AGT Subscription Service v1.0 - Modeles Plans, Prices, Quotas."""
import uuid
from django.db import models


class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    tier_order = models.IntegerField(default=0)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "plans"
        unique_together = [("platform_id", "slug")]
        ordering = ["tier_order", "name"]

    def __str__(self):
        return f"{self.name} @ {self.platform_id}"

    def has_active_subscriptions(self):
        return self.subscriptions.exclude(status__in=["expired", "cancelled"]).exists()


class PlanPrice(models.Model):
    CYCLE_CHOICES = [("monthly", "Monthly"), ("yearly", "Yearly"), ("custom", "Custom")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="prices")
    billing_cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES)
    cycle_days = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="XAF")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plan_prices"
        unique_together = [("plan", "billing_cycle", "currency")]

    def get_cycle_days(self):
        if self.billing_cycle == "monthly":
            return 30
        elif self.billing_cycle == "yearly":
            return 365
        return self.cycle_days or 30

    def price_per_day(self):
        return self.price / self.get_cycle_days()


class PlanQuota(models.Model):
    OVERAGE_CHOICES = [("hard", "Hard Limit"), ("overage", "Overage Allowed")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="quotas")
    quota_key = models.CharField(max_length=50)
    limit_value = models.IntegerField()
    is_cyclical = models.BooleanField(default=True)
    overage_policy = models.CharField(max_length=10, choices=OVERAGE_CHOICES, default="hard")
    overage_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plan_quotas"
        unique_together = [("plan", "quota_key")]

    def __str__(self):
        return f"{self.quota_key}: {self.limit_value} ({self.overage_policy})"
