"""AGT Subscription Service v1.0 - Modeles Subscriptions, Events, Usage, Config."""
import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta


class SubscriptionStatus(models.TextChoices):
    PENDING_PAYMENT = "pending_payment", "Pending Payment"
    TRIAL = "trial", "Trial"
    ACTIVE = "active", "Active"
    GRACE = "grace", "Grace"
    EXPIRED = "expired", "Expired"
    SUSPENDED = "suspended", "Suspended"
    CANCELLED = "cancelled", "Cancelled"


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    subscriber_type = models.CharField(max_length=20)  # user or organization
    subscriber_id = models.UUIDField(db_index=True)
    plan = models.ForeignKey("plans.Plan", on_delete=models.PROTECT, related_name="subscriptions")
    plan_price = models.ForeignKey("plans.PlanPrice", on_delete=models.PROTECT, related_name="subscriptions")
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.PENDING_PAYMENT, db_index=True)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    trial_end = models.DateTimeField(null=True, blank=True)
    grace_end = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscriptions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subscriber_type}:{self.subscriber_id} -> {self.plan.name} [{self.status}]"

    def is_usable(self):
        return self.status in [SubscriptionStatus.TRIAL, SubscriptionStatus.ACTIVE, SubscriptionStatus.GRACE]

    def days_remaining(self):
        delta = self.current_period_end - timezone.now()
        return max(0, delta.days)

    def cancel(self):
        self.cancelled_at = timezone.now()
        self.cancel_at_period_end = True
        self.save(update_fields=["cancelled_at", "cancel_at_period_end", "updated_at"])

    def activate(self):
        self.status = SubscriptionStatus.ACTIVE
        self.save(update_fields=["status", "updated_at"])

    def suspend(self):
        self.status = SubscriptionStatus.SUSPENDED
        self.save(update_fields=["status", "updated_at"])


class SubscriptionQuotaUsage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="quota_usage")
    quota_key = models.CharField(max_length=50)
    used = models.IntegerField(default=0)
    overage = models.IntegerField(default=0)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscription_quotas_usage"
        unique_together = [("subscription", "quota_key", "period_start")]


class QuotaReservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="reservations")
    quota_key = models.CharField(max_length=50)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="pending")  # pending, confirmed, released
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "quota_reservations"


class SubscriptionEvent(models.Model):
    EVENT_TYPES = [
        ("created", "Created"), ("activated", "Activated"), ("renewed", "Renewed"),
        ("upgraded", "Upgraded"), ("downgraded", "Downgraded"), ("cancelled", "Cancelled"),
        ("expired", "Expired"), ("suspended", "Suspended"), ("reactivated", "Reactivated"),
        ("cycle_closed", "Cycle Closed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    from_plan = models.ForeignKey("plans.Plan", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    to_plan = models.ForeignKey("plans.Plan", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    prorate_credit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    prorate_debit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "subscription_events"
        ordering = ["-created_at"]


class PlatformSubscriptionConfig(models.Model):
    POST_TRIAL_CHOICES = [("downgrade_to_free", "Downgrade"), ("suspend", "Suspend"), ("expire", "Expire")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(unique=True)
    default_trial_days = models.IntegerField(default=0)
    grace_period_days = models.IntegerField(default=0)
    post_trial_behavior = models.CharField(max_length=20, choices=POST_TRIAL_CHOICES, default="suspend")
    default_currency = models.CharField(max_length=3, default="XAF")
    allowed_cycles = models.JSONField(default=list)
    require_default_plan = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platform_subscription_config"

    @classmethod
    def get_for_platform(cls, platform_id):
        try:
            return cls.objects.get(platform_id=platform_id)
        except cls.DoesNotExist:
            return cls(platform_id=platform_id, default_trial_days=0, grace_period_days=0, allowed_cycles=["monthly", "yearly"])
