"""
AGT Auth Service v1.0 — Tests unitaires et d'intégration.
"""
import uuid
from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.authentication.models import (
    Platform, UserAuth, Session, RefreshToken, VerificationToken, LoginHistory,
)
from apps.authentication.services import JWTService, TokenService, TOTPService, SessionService


# ─── Helpers ──────────────────────────────────────────────────────────────────

def make_platform(**kwargs):
    defaults = {
        "name": f"Platform-{uuid.uuid4().hex[:6]}",
        "slug": f"plat-{uuid.uuid4().hex[:6]}",
        "allowed_auth_methods": ["email", "phone", "google", "magic_link"],
        "allowed_redirect_urls": ["http://localhost:3000/callback"],
        "client_secret_hash": Platform.hash_client_secret("test-secret"),
        "is_active": True,
    }
    defaults.update(kwargs)
    return Platform.objects.create(**defaults)


def make_user(platform, **kwargs):
    defaults = {
        "email": f"user-{uuid.uuid4().hex[:6]}@agt.com",
        "registration_method": "email",
        "registration_platform": platform,
    }
    defaults.update(kwargs)
    user = UserAuth(**defaults)
    user.set_password(kwargs.get("password", "SecureP@ss123!"))
    user.save()
    return user


# ─── Tests Modèles ────────────────────────────────────────────────────────────

class TestUserAuthModel(TestCase):
    def setUp(self):
        self.platform = make_platform()

    def test_set_and_check_password(self):
        user = make_user(self.platform)
        self.assertTrue(user.check_password("SecureP@ss123!"))
        self.assertFalse(user.check_password("Wrong"))

    def test_password_not_plain_text(self):
        user = make_user(self.platform)
        self.assertNotEqual(user.password_hash, "SecureP@ss123!")
        self.assertTrue(user.password_hash.startswith("$2b$"))

    def test_is_available_blocked(self):
        user = make_user(self.platform)
        user.is_blocked = True
        user.save()
        available, reason = user.is_available_for_login
        self.assertFalse(available)
        self.assertEqual(reason, "user_blocked")

    def test_is_available_deactivated(self):
        user = make_user(self.platform)
        user.is_deactivated = True
        user.save()
        available, reason = user.is_available_for_login
        self.assertFalse(available)
        self.assertEqual(reason, "user_deactivated")

    def test_brute_force_lockout(self):
        user = make_user(self.platform)
        for _ in range(5):
            user.increment_failed_attempts()
        user.refresh_from_db()
        self.assertTrue(user.is_locked())


# ─── Tests Services ───────────────────────────────────────────────────────────

class TestJWTService(TestCase):
    def setUp(self):
        self.platform = make_platform()
        self.user = make_user(self.platform)

    def test_generate_and_decode_token(self):
        token = JWTService.generate_access_token(self.user, str(self.platform.id), str(uuid.uuid4()))
        payload = JWTService.decode_token(token)
        self.assertEqual(payload["sub"], str(self.user.id))
        self.assertEqual(payload["iss"], "agt-auth")

    def test_s2s_token(self):
        token = JWTService.generate_s2s_token(str(self.platform.id), self.platform.name)
        payload = JWTService.decode_token(token)
        self.assertEqual(payload["type"], "s2s")


class TestTokenService(TestCase):
    def test_hash_deterministic(self):
        token = "test-token-123"
        h1 = TokenService.hash_token(token)
        h2 = TokenService.hash_token(token)
        self.assertEqual(h1, h2)

    def test_otp_length(self):
        otp = TokenService.generate_otp(6)
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())


class TestSessionService(TestCase):
    def setUp(self):
        self.platform = make_platform()
        self.user = make_user(self.platform)

    def test_create_session(self):
        session = SessionService.create_session(self.user, self.platform, "127.0.0.1")
        self.assertTrue(session.is_active)
        self.assertFalse(session.is_expired())

    def test_refresh_token_fifo(self):
        session = SessionService.create_session(self.user, self.platform, "127.0.0.1")
        tokens = []
        for _ in range(6):
            tokens.append(SessionService.create_refresh_token(self.user, session))
        active = RefreshToken.objects.filter(user=self.user, is_revoked=False).count()
        self.assertLessEqual(active, 5)

    def test_revoke_all_sessions(self):
        s1 = SessionService.create_session(self.user, self.platform, "127.0.0.1")
        s2 = SessionService.create_session(self.user, self.platform, "127.0.0.2")
        SessionService.revoke_all_sessions(self.user)
        s1.refresh_from_db()
        s2.refresh_from_db()
        self.assertFalse(s1.is_active)
        self.assertFalse(s2.is_active)


# ─── Tests Endpoints ──────────────────────────────────────────────────────────

class TestHealthEndpoint(TestCase):
    def test_health(self):
        client = APIClient()
        response = client.get("/api/v1/auth/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["version"], "1.0.0")


class TestRegisterEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.platform = make_platform()

    @patch("apps.authentication.services.NotificationClient.send", return_value=True)
    @patch("apps.authentication.services.UsersServiceClient.provision_user", return_value=True)
    def test_register_email(self, mock_users, mock_notif):
        response = self.client.post(
            "/api/v1/auth/register",
            data={"email": "new@agt.com", "password": "SecureP@ss123!", "method": "email"},
            format="json",
            HTTP_X_PLATFORM_ID=str(self.platform.id),
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertTrue(UserAuth.objects.filter(email="new@agt.com").exists())

    def test_register_missing_platform(self):
        response = self.client.post(
            "/api/v1/auth/register",
            data={"email": "x@x.com", "password": "Pass1234!", "method": "email"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    @patch("apps.authentication.services.NotificationClient.send", return_value=True)
    @patch("apps.authentication.services.UsersServiceClient.provision_user", return_value=True)
    def test_register_duplicate_email(self, mock_users, mock_notif):
        make_user(self.platform, email="dup@agt.com")
        response = self.client.post(
            "/api/v1/auth/register",
            data={"email": "dup@agt.com", "password": "SecureP@ss123!", "method": "email"},
            format="json",
            HTTP_X_PLATFORM_ID=str(self.platform.id),
        )
        self.assertEqual(response.status_code, 409)


class TestLoginEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.platform = make_platform()
        self.user = make_user(self.platform, email="login@agt.com")

    def test_login_success(self):
        response = self.client.post("/api/v1/auth/login", data={
            "email": "login@agt.com", "password": "SecureP@ss123!",
            "platform_id": str(self.platform.id),
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_login_wrong_password(self):
        response = self.client.post("/api/v1/auth/login", data={
            "email": "login@agt.com", "password": "WrongPass!",
            "platform_id": str(self.platform.id),
        }, format="json")
        self.assertEqual(response.status_code, 401)

    def test_login_blocked_user(self):
        self.user.is_blocked = True
        self.user.save()
        response = self.client.post("/api/v1/auth/login", data={
            "email": "login@agt.com", "password": "SecureP@ss123!",
            "platform_id": str(self.platform.id),
        }, format="json")
        self.assertEqual(response.status_code, 403)


class TestRefreshEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.platform = make_platform()
        self.user = make_user(self.platform, email="refresh@agt.com")

    def test_refresh_with_valid_cookie(self):
        login_resp = self.client.post("/api/v1/auth/login", data={
            "email": "refresh@agt.com", "password": "SecureP@ss123!",
            "platform_id": str(self.platform.id),
        }, format="json")
        self.assertEqual(login_resp.status_code, 200)

        refresh_cookie = login_resp.cookies.get("refresh_token")
        self.assertIsNotNone(refresh_cookie)

        self.client.cookies["refresh_token"] = refresh_cookie.value
        response = self.client.post("/api/v1/auth/refresh")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_refresh_without_cookie(self):
        response = self.client.post("/api/v1/auth/refresh")
        self.assertEqual(response.status_code, 401)


class TestAdminEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.platform = make_platform()
        self.user = make_user(self.platform, email="admin_target@agt.com")

    def _admin_headers(self):
        return {"HTTP_X_ADMIN_API_KEY": settings.ADMIN_API_KEY}

    def test_block_user(self):
        response = self.client.post(f"/api/v1/auth/admin/block/{self.user.id}", **self._admin_headers())
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_blocked)

    def test_unblock_user(self):
        self.user.is_blocked = True
        self.user.save()
        response = self.client.post(f"/api/v1/auth/admin/unblock/{self.user.id}", **self._admin_headers())
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_blocked)

    @patch("apps.authentication.services.UsersServiceClient.sync_status", return_value=True)
    def test_admin_deactivate(self, mock_sync):
        response = self.client.post(f"/api/v1/auth/admin/deactivate/{self.user.id}", **self._admin_headers())
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_deactivated)
        mock_sync.assert_called_once()

    def test_admin_purge(self):
        response = self.client.delete(f"/api/v1/auth/admin/purge/{self.user.id}", **self._admin_headers())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserAuth.objects.filter(id=self.user.id).exists())

    def test_admin_requires_key(self):
        response = self.client.post(f"/api/v1/auth/admin/block/{self.user.id}")
        self.assertIn(response.status_code, [401, 403])
