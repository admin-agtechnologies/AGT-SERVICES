"""
AGT Auth Service v1.0 — Services : JWT, Token, TOTP, Session, inter-services clients.
"""
import hashlib
import hmac
import secrets
import uuid
import logging
from datetime import timedelta
from typing import Optional

import jwt
import pyotp
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class JWTService:
    @staticmethod
    def generate_access_token(user, platform_id: str, session_id: str) -> str:
        now = timezone.now()
        payload = {
            "sub": str(user.id),
            "iss": settings.JWT_ISSUER,
            "aud": settings.JWT_AUDIENCE,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=settings.JWT_ACCESS_TTL)).timestamp()),
            "jti": str(uuid.uuid4()),
            "session_id": str(session_id),
            "platform_id": str(platform_id),
            "email": user.email,
            "email_verified": user.email_verified,
            "two_fa_verified": False,
        }
        return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="RS256")

    @staticmethod
    def generate_access_token_2fa(user, platform_id: str, session_id: str) -> str:
        now = timezone.now()
        payload = {
            "sub": str(user.id),
            "iss": settings.JWT_ISSUER,
            "aud": settings.JWT_AUDIENCE,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=settings.JWT_ACCESS_TTL)).timestamp()),
            "jti": str(uuid.uuid4()),
            "session_id": str(session_id),
            "platform_id": str(platform_id),
            "email": user.email,
            "email_verified": user.email_verified,
            "two_fa_verified": True,
        }
        return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="RS256")

    @staticmethod
    def generate_temp_token(user_id: str, platform_id: str, session_id: str) -> str:
        now = timezone.now()
        payload = {
            "sub": str(user_id), "type": "2fa_challenge",
            "session_id": str(session_id), "platform_id": str(platform_id),
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=5)).timestamp()),
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="RS256")

    @staticmethod
    def generate_s2s_token(platform_id: str, platform_name: str) -> str:
        now = timezone.now()
        payload = {
            "sub": str(platform_id), "type": "s2s", "service_name": platform_name,
            "iss": settings.JWT_ISSUER, "aud": settings.JWT_AUDIENCE,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(hours=1)).timestamp()),
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm="RS256")

    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=["RS256"],
                          audience=settings.JWT_AUDIENCE, issuer=settings.JWT_ISSUER)

    @staticmethod
    def decode_token_unverified(token: str) -> dict:
        return jwt.decode(token, options={"verify_signature": False})


class TokenService:
    @staticmethod
    def generate_raw_token(length: int = 64) -> str:
        return secrets.token_urlsafe(length)

    @staticmethod
    def generate_otp(digits: int = 6) -> str:
        return str(secrets.randbelow(10 ** digits)).zfill(digits)

    @staticmethod
    def hash_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    @staticmethod
    def hash_refresh_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    @staticmethod
    def constant_time_compare(val1: str, val2: str) -> bool:
        return hmac.compare_digest(val1.encode(), val2.encode())


class TOTPService:
    @staticmethod
    def generate_secret() -> str:
        return pyotp.random_base32()

    @staticmethod
    def get_totp_uri(secret: str, email: str) -> str:
        return pyotp.TOTP(secret).provisioning_uri(name=email, issuer_name="AGT")

    @staticmethod
    def verify_code(secret: str, code: str) -> bool:
        return pyotp.TOTP(secret).verify(code, valid_window=1)

    @staticmethod
    def encrypt_secret(raw_secret: str) -> str:
        import base64
        return base64.b64encode(raw_secret.encode()).decode()

    @staticmethod
    def decrypt_secret(encrypted_secret: str) -> str:
        import base64
        return base64.b64decode(encrypted_secret.encode()).decode()


class SessionService:
    @staticmethod
    def create_session(user, platform, ip_address: str, user_agent: str = None):
        from apps.authentication.models import Session
        return Session.objects.create(
            user=user, platform=platform, ip_address=ip_address, user_agent=user_agent,
            expires_at=timezone.now() + timedelta(seconds=settings.JWT_REFRESH_TTL),
        )

    @staticmethod
    def create_refresh_token(user, session) -> str:
        from apps.authentication.models import RefreshToken
        max_tokens = getattr(settings, "MAX_REFRESH_TOKENS", 5)
        active_tokens = RefreshToken.objects.filter(user=user, is_revoked=False).order_by("created_at")
        count = active_tokens.count()
        if count >= max_tokens:
            to_revoke = active_tokens[: count - max_tokens + 1]
            RefreshToken.objects.filter(id__in=[t.id for t in to_revoke]).update(is_revoked=True)

        raw_token = TokenService.generate_raw_token()
        token_hash = TokenService.hash_refresh_token(raw_token)
        RefreshToken.objects.create(
            user=user, session=session, token_hash=token_hash,
            expires_at=timezone.now() + timedelta(seconds=settings.JWT_REFRESH_TTL),
        )
        return raw_token

    @staticmethod
    def revoke_all_sessions(user, except_session_id=None) -> int:
        from apps.authentication.models import Session, RefreshToken
        qs = Session.objects.filter(user=user, is_active=True)
        if except_session_id:
            qs = qs.exclude(id=except_session_id)
        session_ids = list(qs.values_list("id", flat=True))
        RefreshToken.objects.filter(session_id__in=session_ids).update(is_revoked=True)
        return qs.update(is_active=False)

    @staticmethod
    def revoke_session(session) -> None:
        from apps.authentication.models import RefreshToken
        RefreshToken.objects.filter(session=session).update(is_revoked=True)
        session.is_active = False
        session.save(update_fields=["is_active"])
class NotificationClient:
    @staticmethod
    def _get_s2s_token(platform_id: str = "agt-auth-internal") -> str:
        """Génère un token S2S signé avec le platform_id de la plateforme appelante."""
        return JWTService.generate_s2s_token(
            platform_id=platform_id,
            platform_name="agt-auth"
        )

    @staticmethod
    def send(notification_type: str, recipient: dict, template: str, data: dict, priority: str = "normal") -> bool:
        import httpx
        url = getattr(settings, "NOTIFICATION_SERVICE_URL", "")
        if not url:
            logger.warning("NOTIFICATION_SERVICE_URL non configuré — notification ignorée.")
            return False

        user_id = recipient.get("user_id")
        platform_id = recipient.get("platform_id", "agt-auth-internal")

        if not user_id:
            logger.warning("NotificationClient.send: user_id manquant dans recipient.")
            return False

        try:
            # Le token S2S doit porter le platform_id pour que Notification resolve le bon template
            token = NotificationClient._get_s2s_token(platform_id=platform_id)
            resp = httpx.post(f"{url}/notifications/send", json={
                "user_id": user_id,
                "channels": ["email"],
                "template_name": template,
                "variables": data,
                "idempotency_key": str(uuid.uuid4()),
            }, headers={"Authorization": f"Bearer {token}"}, timeout=5.0)
            if resp.status_code >= 400:
                logger.error(f"Notification échouée ({resp.status_code}): {resp.text}")
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Notification échouée: {e}")
            return False

class UsersServiceClient:
    @staticmethod
    def _get_s2s_token() -> str:
        """Génère un token S2S interne signé par Auth pour appeler les autres services."""
        return JWTService.generate_s2s_token(
            platform_id="agt-auth-internal",
            platform_name="agt-auth"
        )

    @staticmethod
    def provision_user(auth_user_id: str, email: str = None, phone: str = None, first_name: str = "", last_name: str = "") -> bool:
        import httpx
        url = getattr(settings, "USERS_SERVICE_URL", "")
        if not url:
            logger.warning("USERS_SERVICE_URL non configuré — provisioning ignoré.")
            return False
        try:
            token = UsersServiceClient._get_s2s_token()
            resp = httpx.post(f"{url}/users", json={
    "auth_user_id": auth_user_id,
    "email": email,
    "phone": phone,
    "first_name": first_name,
    "last_name": last_name,
}, headers={"Authorization": f"Bearer {token}"}, timeout=5.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Provisioning Users échoué: {e}")
            return False

    @staticmethod
    def sync_status(auth_user_id: str, status: str) -> bool:
        import httpx
        url = getattr(settings, "USERS_SERVICE_URL", "")
        if not url:
            return False
        try:
            token = UsersServiceClient._get_s2s_token()
            resp = httpx.post(f"{url}/users/status-sync", json={
                "auth_user_id": auth_user_id,
                "status": status,
            }, headers={"Authorization": f"Bearer {token}"}, timeout=5.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Status sync Users échoué: {e}")
            return False

    @staticmethod
    def sync_credentials(auth_user_id: str, email: str = None, phone: str = None) -> bool:
        import httpx
        url = getattr(settings, "USERS_SERVICE_URL", "")
        if not url:
            return False
        payload = {"auth_user_id": auth_user_id}
        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        try:
            token = UsersServiceClient._get_s2s_token()
            resp = httpx.post(f"{url}/users/sync", json=payload,
                              headers={"Authorization": f"Bearer {token}"}, timeout=5.0)
            return resp.status_code < 400
        except Exception as e:
            logger.error(f"Credentials sync Users échoué: {e}")
            return False
    @staticmethod
    def get_profile_by_auth_id(auth_user_id: str) -> dict:
        """Récupère le profil Users pour obtenir first_name/last_name."""
        import httpx
        url = getattr(settings, "USERS_SERVICE_URL", "")
        if not url:
            return {}
        try:
            token = UsersServiceClient._get_s2s_token()
            resp = httpx.get(
                f"{url}/users/by-auth/{auth_user_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=3.0,
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.error(f"get_profile_by_auth_id échoué: {e}")
        return {}