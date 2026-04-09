"""AGT Notification Service v1.0 - Authentication JWT (cle publique Auth)."""
import logging, jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class JWTPayload:
    def __init__(self, payload):
        self.payload = payload
        self.id = payload.get("sub")
        self.auth_user_id = payload.get("sub")
        self.platform_id = payload.get("platform_id")
        self.is_authenticated = True


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ", 1)[1]
        cache_key = f"jwt:{token[:32]}"
        cached = cache.get(cache_key)
        if cached:
            return JWTPayload(cached), cached
        public_key = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not public_key:
            raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")
        try:
            payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="agt-ecosystem", issuer="agt-auth")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})
        cache.set(cache_key, payload, timeout=30)
        return JWTPayload(payload), payload

    def authenticate_header(self, request):
        return "Bearer"
