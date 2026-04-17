"""
AGT Search Service v1.0 - Authentification JWT.

Convention AGT :
- Token utilisateur : platform_id est dans le champ "platform_id" du JWT
- Token S2S        : platform_id est dans le champ "sub" du JWT (l'identité de la plateforme appelante)
"""
import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission



class IsS2SToken(BasePermission):
    """
    Permission AGT : autorise uniquement les tokens S2S (inter-services).
    Utilisé pour les endpoints sensibles comme la purge RGPD.
    """
    message = {"detail": "Cet endpoint est réservé aux appels inter-services (S2S)."}

    def has_permission(self, request, view):
        # request.user est un JWTPayload — on vérifie le type dans le payload brut
        payload = getattr(request.user, "payload", {})
        return payload.get("type") == "s2s"


class JWTPayload:
    def __init__(self, p):
        self.payload = p
        self.id = p.get("sub")
        self.auth_user_id = p.get("sub")
        self.is_authenticated = True

        # Convention AGT validée : pour les tokens S2S, l'identité de la plateforme
        # est dans "sub" (pas dans "platform_id" qui est absent des tokens S2S).
        # Ce pattern est identique à agt-notification et agt-chatbot.
        if p.get("type") == "s2s":
            self.platform_id = p.get("sub")
        else:
            self.platform_id = p.get("platform_id")


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        h = request.headers.get("Authorization", "")
        if not h.startswith("Bearer "):
            return None

        token = h.split(" ", 1)[1]

        # Cache court (30s) pour éviter de décoder le JWT à chaque requête
        ck = f"jwt:{token[:32]}"
        cached = cache.get(ck)
        if cached:
            return JWTPayload(cached), cached

        pk = getattr(settings, "AUTH_PUBLIC_KEY", "")
        if not pk:
            raise AuthenticationFailed("AUTH_PUBLIC_KEY non configure.")

        try:
            payload = jwt.decode(
                token,
                pk,
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

