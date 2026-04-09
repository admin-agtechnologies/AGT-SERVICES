"""AGT Notification Service v1.0 - Tests."""
import uuid
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient

from apps.notifications.models import Notification, UserPreference, PlatformChannelConfig
from apps.templates_mgr.models import Template, TemplateVersion
from apps.campaigns.models import Campaign, CampaignRecipient
from apps.devices.models import DeviceToken


def make_template(name="test_tpl", channel="email", body="Hello {{ name }}", platform_id=None):
    tpl = Template.objects.create(name=name, channel=channel, platform_id=platform_id, category="transactional")
    TemplateVersion.objects.create(template=tpl, version=1, locale="fr", subject="Test", body=body, is_current=True)
    return tpl


class TestModels(TestCase):
    def test_notification_lifecycle(self):
        n = Notification.objects.create(user_id=uuid.uuid4(), platform_id=uuid.uuid4(),
                                         channel="email", category="transactional", body="Test")
        self.assertEqual(n.status, "pending")
        n.mark_sent()
        n.refresh_from_db()
        self.assertEqual(n.status, "sent")

    def test_notification_in_app(self):
        n = Notification.objects.create(user_id=uuid.uuid4(), platform_id=uuid.uuid4(),
                                         channel="in_app", category="transactional", body="Test")
        self.assertFalse(n.is_read)
        n.mark_as_read()
        self.assertTrue(n.is_read)

    def test_template_resolve_platform_then_global(self):
        pid = uuid.uuid4()
        make_template(name="order", platform_id=pid)
        make_template(name="order", platform_id=None, body="Global {{ name }}")
        tpl = Template.resolve("order", platform_id=str(pid))
        self.assertEqual(tpl.platform_id, pid)

    def test_template_resolve_fallback_global(self):
        make_template(name="global_tpl", platform_id=None)
        tpl = Template.resolve("global_tpl", platform_id=str(uuid.uuid4()))
        self.assertIsNone(tpl.platform_id)

    def test_template_render(self):
        tpl = make_template(body="Bonjour {{ name }}")
        result = tpl.render({"name": "Jean"})
        self.assertEqual(result["body"], "Bonjour Jean")

    def test_preference_defaults(self):
        pref = UserPreference()
        self.assertTrue(pref.is_channel_enabled("email"))
        self.assertTrue(pref.is_category_enabled("security"))
        self.assertFalse(pref.cat_marketing)

    def test_device_token(self):
        uid = uuid.uuid4()
        DeviceToken.objects.create(user_id=uid, platform_id=uuid.uuid4(), token="fcm123", device_type="android")
        self.assertEqual(DeviceToken.objects.filter(user_id=uid).count(), 1)

    def test_campaign_progress(self):
        c = Campaign.objects.create(name="Test", platform_id=uuid.uuid4(), channel="email", total_recipients=100, sent_count=50)
        self.assertEqual(c.progress_percent, 50.0)


class TestHealthEndpoint(TestCase):
    def test_health(self):
        client = APIClient()
        resp = client.get("/api/v1/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")


class TestSendEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())

    @patch("workers.tasks.send_notification_task.delay")
    def test_send_notification(self, mock_task):
        tpl = make_template(name="test_send")
        resp = self.client.post("/api/v1/notifications/send", data={
            "user_id": str(uuid.uuid4()), "channels": ["email"],
            "template_name": "test_send", "variables": {"name": "Test"},
        }, format="json")
        self.assertEqual(resp.status_code, 202)
        self.assertTrue(mock_task.called)

    def test_send_missing_fields(self):
        resp = self.client.post("/api/v1/notifications/send", data={}, format="json")
        self.assertEqual(resp.status_code, 400)

    @patch("workers.tasks.send_notification_task.delay")
    def test_idempotency(self, mock_task):
        tpl = make_template(name="idemp_test")
        data = {"user_id": str(uuid.uuid4()), "channels": ["email"],
                "template_name": "idemp_test", "idempotency_key": "key123"}
        self.client.post("/api/v1/notifications/send", data=data, format="json")
        resp2 = self.client.post("/api/v1/notifications/send", data=data, format="json")
        self.assertEqual(resp2.status_code, 409)


class TestTemplateEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": None, "auth_user_id": str(uuid.uuid4())})())

    def test_create_template(self):
        resp = self.client.post("/api/v1/templates", data={
            "name": "new_tpl", "channel": "email", "body": "Hello {{ name }}",
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_list_templates(self):
        make_template()
        resp = self.client.get("/api/v1/templates")
        self.assertEqual(resp.status_code, 200)


class TestInApp(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.uid = str(uuid.uuid4())
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": None, "auth_user_id": self.uid})())

    def test_unread_count(self):
        Notification.objects.create(user_id=self.uid, platform_id=uuid.uuid4(), channel="in_app", category="transactional", body="Test")
        resp = self.client.get(f"/api/v1/users/{self.uid}/notifications/unread-count")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["unread_count"], 1)
