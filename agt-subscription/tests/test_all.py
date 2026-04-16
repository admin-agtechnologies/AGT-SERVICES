"""AGT Subscription Service v1.0 - Tests.

Structure :
- TestPlanModel             : tests unitaires modèle Plan
- TestSubscriptionService   : tests unitaires lifecycle abonnement
- TestQuotaService          : tests unitaires QuotaService (logique métier)
- TestHealthEndpoint        : test endpoint health
- TestPlanEndpoints         : tests intégration endpoints Plans
- TestQuotaEndpoints        : tests intégration endpoints Quotas (S2S)
- TestOrganizationEndpoints : tests intégration endpoints Organizations
"""
import uuid
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient

from apps.plans.models import Plan, PlanPrice, PlanQuota
from apps.subscriptions.models import (
    Subscription, SubscriptionEvent, SubscriptionQuotaUsage,
    PlatformSubscriptionConfig,
)
from apps.organizations.models import Organization, OrganizationMember
from apps.subscriptions.service import SubscriptionService
from apps.quotas.service import QuotaService


# ─── Helpers ──────────────────────────────────────────────────────────────────

def make_plan(platform_id=None, name="Pro", slug=None, is_free=False, tier_order=1):
    """Crée un plan de test avec un prix mensuel et deux quotas."""
    pid = platform_id or uuid.uuid4()
    plan = Plan.objects.create(
        platform_id=pid, name=name,
        slug=slug or f"plan-{uuid.uuid4().hex[:6]}",
        is_free=is_free, tier_order=tier_order,
    )
    PlanPrice.objects.create(plan=plan, billing_cycle="monthly", price=15000, currency="XAF")
    PlanQuota.objects.create(plan=plan, quota_key="messages", limit_value=1000,
                              is_cyclical=True, overage_policy="hard")
    PlanQuota.objects.create(plan=plan, quota_key="storage_mb", limit_value=500,
                              is_cyclical=False, overage_policy="overage")
    return plan


def make_auth_user():
    """Retourne un objet user simulé pour force_authenticate."""
    return type("U", (), {
        "is_authenticated": True,
        "platform_id": str(uuid.uuid4()),
        "auth_user_id": str(uuid.uuid4()),
    })()


def make_s2s_user(platform_id=None):
    """Retourne un objet user simulé pour un appel S2S."""
    pid = str(platform_id or uuid.uuid4())
    return type("U", (), {
        "is_authenticated": True,
        "platform_id": pid,
        "auth_user_id": pid,  # Pour S2S, sub == platform_id
    })()


# ─── Tests unitaires ──────────────────────────────────────────────────────────

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
        PlatformSubscriptionConfig.objects.create(
            platform_id=self.pid, default_trial_days=14, allowed_cycles=["monthly"]
        )
        sub, err = SubscriptionService.create(
            self.pid, "user", self.uid, self.plan.id, "monthly", with_trial=True
        )
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

    def test_reserve_release(self):
        """Une réservation libérée ne doit pas consommer de quota."""
        res, err = QuotaService.reserve(self.pid, "user", self.uid, "messages", 10)
        self.assertIsNone(err)
        result, err = QuotaService.release_reservation(res["reservation_id"])
        self.assertIsNone(err)
        self.assertTrue(result["released"])
        # Vérifier que le quota n'a pas été consommé
        check = QuotaService.check(self.pid, "user", self.uid, "messages", 1)
        self.assertEqual(check["used"], 0)

    def test_no_active_subscription(self):
        result = QuotaService.check(self.pid, "user", uuid.uuid4(), "messages", 1)
        self.assertFalse(result["allowed"])
        self.assertEqual(result["reason"], "no_active_subscription")


# ─── Tests endpoints ──────────────────────────────────────────────────────────

class TestHealthEndpoint(TestCase):
    def test_health(self):
        client = APIClient()
        resp = client.get("/api/v1/subscriptions/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")


class TestPlanEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=make_auth_user())
        self.platform_id = str(uuid.uuid4())

    def test_create_plan(self):
        resp = self.client.post("/api/v1/subscriptions/plans", data={
            "platform_id": self.platform_id,
            "name": "Starter",
            "slug": "starter",
            "prices": [{"billing_cycle": "monthly", "price": 5000}],
            "quotas": [{"quota_key": "max_items", "limit_value": 10}],
        }, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertIn("id", resp.json())

    def test_list_plans(self):
        make_plan()
        resp = self.client.get("/api/v1/subscriptions/plans")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("data", resp.json())

    def test_create_plan_duplicate_slug(self):
        """Un slug dupliqué pour la même platform doit retourner 409."""
        self.client.post("/api/v1/subscriptions/plans", data={
            "platform_id": self.platform_id, "name": "Plan A", "slug": "plan-a",
            "prices": [{"billing_cycle": "monthly", "price": 5000}],
        }, format="json")
        resp = self.client.post("/api/v1/subscriptions/plans", data={
            "platform_id": self.platform_id, "name": "Plan A bis", "slug": "plan-a",
            "prices": [{"billing_cycle": "monthly", "price": 6000}],
        }, format="json")
        self.assertEqual(resp.status_code, 409)

    def test_get_plan_detail(self):
        plan = make_plan()
        resp = self.client.get(f"/api/v1/subscriptions/plans/{plan.id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["id"], str(plan.id))

    def test_archive_plan(self):
        plan = make_plan()
        resp = self.client.post(f"/api/v1/subscriptions/plans/{plan.id}/archive")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.json()["is_active"])


class TestQuotaEndpoints(TestCase):
    """Tests d'intégration pour les endpoints quotas — appelés en S2S."""

    def setUp(self):
        self.client = APIClient()
        self.pid = uuid.uuid4()
        self.uid = uuid.uuid4()

        # Créer un abonnement actif pour les tests de quotas
        self.plan = make_plan(platform_id=self.pid)
        sub, _ = SubscriptionService.create(self.pid, "user", self.uid, self.plan.id, "monthly")
        sub.status = "active"
        sub.save()
        self.sub = sub

        # Simuler un appelant S2S authentifié
        self.client.force_authenticate(user=make_s2s_user(self.pid))

    def _quota_payload(self, quota_key="messages", amount=1):
        return {
            "platform_id": str(self.pid),
            "subscriber_type": "user",
            "subscriber_id": str(self.uid),
            "quota_key": quota_key,
            "amount": amount,
        }

    def test_quota_check(self):
        resp = self.client.post("/api/v1/subscriptions/quotas/check",
                                data=self._quota_payload(), format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["allowed"])
        self.assertEqual(resp.json()["limit"], 1000)

    def test_quota_increment(self):
        resp = self.client.post("/api/v1/subscriptions/quotas/increment",
                                data=self._quota_payload(amount=10), format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["used"], 10)

    def test_quota_reserve_confirm(self):
        # Réserver
        resp = self.client.post("/api/v1/subscriptions/quotas/reserve",
                                data=self._quota_payload(amount=5), format="json")
        self.assertEqual(resp.status_code, 201)
        reservation_id = resp.json()["reservation_id"]

        # Confirmer
        resp = self.client.post("/api/v1/subscriptions/quotas/confirm",
                                data={"reservation_id": reservation_id}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["used"], 5)

    def test_quota_reserve_release(self):
        # Réserver
        resp = self.client.post("/api/v1/subscriptions/quotas/reserve",
                                data=self._quota_payload(amount=5), format="json")
        self.assertEqual(resp.status_code, 201)
        reservation_id = resp.json()["reservation_id"]

        # Libérer
        resp = self.client.post("/api/v1/subscriptions/quotas/release",
                                data={"reservation_id": reservation_id}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["released"])

    def test_quota_check_no_subscription(self):
        """Un subscriber sans abonnement actif doit recevoir allowed=False."""
        payload = {
            "platform_id": str(self.pid),
            "subscriber_type": "user",
            "subscriber_id": str(uuid.uuid4()),  # inconnu
            "quota_key": "messages",
            "amount": 1,
        }
        resp = self.client.post("/api/v1/subscriptions/quotas/check",
                                data=payload, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.json()["allowed"])

    def test_quota_usage_endpoint(self):
        resp = self.client.get(f"/api/v1/subscriptions/{self.sub.id}/usage")
        self.assertEqual(resp.status_code, 200)


class TestOrganizationEndpoints(TestCase):
    """Tests d'intégration pour les endpoints Organizations B2B."""

    def setUp(self):
        self.client = APIClient()
        self.pid = str(uuid.uuid4())
        self.owner_id = str(uuid.uuid4())
        self.client.force_authenticate(user=make_auth_user())

    def test_create_organization(self):
        resp = self.client.post("/api/v1/organizations", data={
            "platform_id": self.pid,
            "name": "ACME Corp",
            "owner_user_id": self.owner_id,
        }, format="json")
        self.assertEqual(resp.status_code, 201)
        self.assertIn("id", resp.json())
        self.org_id = resp.json()["id"]

    def test_list_organizations(self):
        Organization.objects.create(
            platform_id=self.pid, name="Corp1", owner_user_id=uuid.uuid4()
        )
        resp = self.client.get(f"/api/v1/organizations?platform_id={self.pid}")
        self.assertEqual(resp.status_code, 200)

    def test_add_member(self):
        org = Organization.objects.create(
            platform_id=self.pid, name="Corp", owner_user_id=uuid.uuid4()
        )
        member_id = str(uuid.uuid4())
        resp = self.client.post(f"/api/v1/organizations/{org.id}/members", data={
            "user_id": member_id,
            "role": "member",
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_list_members(self):
        org = Organization.objects.create(
            platform_id=self.pid, name="Corp2", owner_user_id=uuid.uuid4()
        )
        OrganizationMember.objects.create(organization=org, user_id=uuid.uuid4())
        resp = self.client.get(f"/api/v1/organizations/{org.id}/members")
        self.assertEqual(resp.status_code, 200)

    def test_remove_member(self):
        org = Organization.objects.create(
            platform_id=self.pid, name="Corp3", owner_user_id=uuid.uuid4()
        )
        member_id = uuid.uuid4()
        OrganizationMember.objects.create(organization=org, user_id=member_id)
        resp = self.client.delete(f"/api/v1/organizations/{org.id}/members/{member_id}")
        self.assertEqual(resp.status_code, 204)