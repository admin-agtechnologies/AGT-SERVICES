import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTPayload:
    def __init__(self, p):
        self.payload = p
        self.id = p.get("sub")
        self.auth_user_id = p.get("sub")
        self.platform_id = p.get("platform_id")
        self.is_authenticated = True

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "):
            return None
        token = h.split(" ", 1)[1]
        ck = f"jwt:{token[:32]}"
        cached = cache.get(ck)
        if cached:
            return JWTPayload(cached), cached
        pk = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not pk:
            raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")
        try:
            payload = jwt.decode(token, pk, algorithms=["RS256"], audience="agt-ecosystem", issuer="agt-auth")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})
        cache.set(ck, payload, timeout=30)
        return JWTPayload(payload), payload
    def authenticate_header(self, request):
        return "Bearer"
