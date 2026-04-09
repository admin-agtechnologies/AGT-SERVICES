"""AGT Subscription Service v1.0 - Tests."""
import uuid
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from apps.plans.models import Plan, PlanPrice, PlanQuota
from apps.subscriptions.models import Subscription, SubscriptionEvent, SubscriptionQuotaUsage, PlatformSubscriptionConfig
from apps.organizations.models import Organization, OrganizationMember
from apps.subscriptions.service import SubscriptionService
from apps.quotas.service import QuotaService


def make_plan(platform_id=None, name="Pro", slug=None, is_free=False, tier_order=1):
    pid = platform_id or uuid.uuid4()
    plan = Plan.objects.create(platform_id=pid, name=name, slug=slug or f"plan-{uuid.uuid4().hex[:6]}",
                                is_free=is_free, tier_order=tier_order)
    PlanPrice.objects.create(plan=plan, billing_cycle="monthly", price=15000, currency="XAF")
    PlanQuota.objects.create(plan=plan, quota_key="messages", limit_value=1000, is_cyclical=True, overage_policy="hard")
    PlanQuota.objects.create(plan=plan, quota_key="storage_mb", limit_value=500, is_cyclical=False, overage_policy="overage")
    return plan


class TestPlanModel(TestCase):
    def test_create_plan(self):
        plan = make_plan()
        self.assertTrue(plan.is_active)
        self.assertEqual(plan.prices.count(), 1)
        self.assertEqual(plan.quotas.count(), 2)

    def test_price_per_day(self):
        plan = make_plan()
        price = plan.prices.first()
        self.assertAlmostEqual(float(price.price_per_day()), 500.0, places=0)


class TestSubscriptionService(TestCase):
    def setUp(self):
        self.pid = uuid.uuid4()
        self.uid = uuid.uuid4()
        self.plan = make_plan(platform_id=self.pid)

    def test_create_subscription(self):
        sub, err = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        self.assertIsNone(err)
        self.assertEqual(sub.status, "pending_payment")

    def test_create_with_trial(self):
        PlatformSubscriptionConfig.objects.create(platform_id=self.pid, default_trial_days=14, allowed_cycles=["monthly"])
        sub, err = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly", with_trial=True)
        self.assertIsNone(err)
        self.assertEqual(sub.status, "trial")
        self.assertIsNotNone(sub.trial_end)

    def test_no_duplicate_active(self):
        SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        _, err = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        self.assertEqual(err, "active_subscription_exists")

    def test_cancel(self):
        sub, _ = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        sub.status = "active"
        sub.save()
        cancelled, err = SubscriptionService.cancel(sub.id)
        self.assertIsNone(err)
        self.assertTrue(cancelled.cancel_at_period_end)

    def test_change_plan_prorata(self):
        sub, _ = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        sub.status = "active"
        sub.save()
        premium = make_plan(platform_id=self.pid, name="Premium", tier_order=2)
        PlanPrice.objects.filter(plan=premium).update(price=30000)
        result, err = SubscriptionService.change_plan(sub.id, premium.id, "monthly")
        self.assertIsNone(err)
        self.assertEqual(result["event_type"], "upgraded")
        self.assertGreater(result["amount_due"], 0)


class TestQuotaService(TestCase):
    def setUp(self):
        self.pid = uuid.uuid4()
        self.uid = uuid.uuid4()
        self.plan = make_plan(platform_id=self.pid)
        sub, _ = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        sub.status = "active"
        sub.save()
        self.sub = sub

    def test_check_quota(self):
        result = QuotaService.check(self.pid, "user", self.uid, "messages", 1)
        self.assertTrue(result["allowed"])
        self.assertEqual(result["limit"], 1000)

    def test_increment_quota(self):
        result, err = QuotaService.increment(self.pid, "user", self.uid, "messages", 5)
        self.assertIsNone(err)
        self.assertEqual(result["used"], 5)

    def test_hard_limit(self):
        QuotaService.increment(self.pid, "user", self.uid, "messages", 1000)
        _, err = QuotaService.increment(self.pid, "user", self.uid, "messages", 1)
        self.assertEqual(err, "hard_limit_exceeded")

    def test_reserve_confirm(self):
        res, err = QuotaService.reserve(self.pid, "user", self.uid, "messages", 5)
        self.assertIsNone(err)
        result, err = QuotaService.confirm_reservation(res["reservation_id"])
        self.assertIsNone(err)
        self.assertEqual(result["used"], 5)


class TestHealthEndpoint(TestCase):
    def test_health(self):
        client = APIClient()
        resp = client.get("/api/v1/subscriptions/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")


class TestPlanEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())

    def test_create_plan(self):
        resp = self.client.post("/api/v1/subscriptions/plans", data={
            "platform_id": str(uuid.uuid4()), "name": "Starter", "slug": "starter",
            "prices": [{"billing_cycle": "monthly", "price": 5000}],
            "quotas": [{"quota_key": "max_items", "limit_value": 10}],
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_list_plans(self):
        make_plan()
        resp = self.client.get("/api/v1/subscriptions/plans")
        self.assertEqual(resp.status_code, 200)


class TestOrganization(TestCase):
    def test_create_org(self):
        pid = uuid.uuid4()
        org = Organization.objects.create(platform_id=pid, name="ACME", owner_user_id=uuid.uuid4())
        self.assertEqual(org.name, "ACME")

    def test_add_member(self):
        org = Organization.objects.create(platform_id=uuid.uuid4(), name="Corp", owner_user_id=uuid.uuid4())
        OrganizationMember.objects.create(organization=org, user_id=uuid.uuid4())
        self.assertEqual(org.members.count(), 1)
