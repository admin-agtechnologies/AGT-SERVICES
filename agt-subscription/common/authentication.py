"""AGT Subscription Service v1.0 - Authentication JWT.

Supporte deux types de tokens :
- user token : émis pour un utilisateur humain (type != "s2s")
- S2S token  : émis pour un service interne (type == "s2s"), dans ce cas
               platform_id est porté par le champ "sub" du JWT.
"""
import jwt
import logging
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class JWTPayload:
    """Représente le payload décodé d'un JWT AGT (user ou S2S)."""

    def __init__(self, p):
        self.payload = p
        self.id = p.get("sub")
        self.auth_user_id = p.get("sub")
        self.is_authenticated = True

        # Pour les tokens S2S, le champ "sub" contient le platform_id
        # (c'est la convention AGT — le service appelant s'identifie via sub).
        token_type = p.get("type", "")
        if token_type == "s2s":
            self.platform_id = p.get("sub")
        else:
            self.platform_id = p.get("platform_id")


class JWTAuthentication(BaseAuthentication):
    """Authentification JWT RS256 via la clé publique de Auth Service."""

    def authenticate(self, request):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "):
            return None

        token = h.split(" ", 1)[1]

        # Cache court (30s) pour éviter de décoder le même token à chaque requête
        ck = f"jwt:{token[:32]}"
        cached = cache.get(ck)
        if cached:
            return JWTPayload(cached), cached

        pk = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not pk:
            raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")

        try:
            payload = jwt.decode(
                token, pk,
                algorithms=["RS256"],
                audience="agt-ecosystem",
                issuer="agt-auth",
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"valid": False, "reason": "token_expired"})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"valid": False, "reason": "invalid_token"})

        cache.set(ck, payload, timeout=30)
        return JWTPayload(payload), payload

    def authenticate_header(self, request):
        return "Bearer"