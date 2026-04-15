"""
AGT Auth Service v1.0 — Authentification JWT pour DRF + Admin API Key.
"""
import hmac
import logging

import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.authentication.models import Session, UserAuth
from apps.authentication.services import JWTService

logger = logging.getLogger(__name__)

class JWTPayload:
    def __init__(self, payload):
        self.payload = payload
        self.id = payload.get("sub")
        self.auth_user_id = payload.get("sub")
        self.email = payload.get("email")
        self.platform_id = payload.get("platform_id")
        self.session_id = payload.get("session_id")
        self.is_authenticated = True

    def __str__(self):
        return f"JWTUser({self.auth_user_id})"
    
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ", 1)[1]
        return self._validate_token(token)

    def _validate_token(self, token: str):
        cache_key = f"jwt_valid:{token[:32]}"
        cached = cache.get(cache_key)
        if cached == "invalid":
            raise AuthenticationFailed("Token invalide.")
        if cached and isinstance(cached, dict):
            return JWTPayload(cached), cached

        try:
            payload = JWTService.decode_token(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_signature"})

        try:
            user = UserAuth.objects.select_related("registration_platform").get(id=payload["sub"])
        except UserAuth.DoesNotExist:
            raise AuthenticationFailed({"valid": False, "reason": "user_not_found"})

        if user.is_blocked:
            raise AuthenticationFailed({"valid": False, "reason": "user_blocked"})
        if user.is_deactivated:
            raise AuthenticationFailed({"valid": False, "reason": "user_deactivated"})

        session_id = payload.get("session_id")
        if session_id:
            try:
                session = Session.objects.select_related("platform").get(id=session_id)
                if not session.is_active or session.is_expired():
                    raise AuthenticationFailed({"valid": False, "reason": "session_revoked"})
                if not session.platform.is_active:
                    raise AuthenticationFailed({"valid": False, "reason": "platform_inactive"})
            except Session.DoesNotExist:
                raise AuthenticationFailed({"valid": False, "reason": "session_revoked"})

        cache.set(cache_key, payload, timeout=30)
        return JWTPayload(payload), payload

    def authenticate_header(self, request):
        return "Bearer"


class AdminAPIKeyAuthentication:
    @staticmethod
    def verify(request) -> bool:
        api_key = request.headers.get("X-Admin-API-Key", "")
        expected = settings.ADMIN_API_KEY
        if not expected or not api_key:
            return False
        return hmac.compare_digest(api_key.encode(), expected.encode())
