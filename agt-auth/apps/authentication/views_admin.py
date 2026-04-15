"""
AGT Auth Service v1.0 — Views : Administration, OAuth, S2S tokens.
"""
import logging
import secrets as sec

import httpx
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import redirect as django_redirect
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import (
    UserAuth, Session, RefreshToken, OAuthProvider,
    LoginHistory, VerificationToken, Platform,
)
from apps.authentication.permissions import IsAdminAPIKey
from apps.authentication.serializers import DeactivateAccountSerializer
from apps.authentication.services import (
    JWTService, TokenService, SessionService, UsersServiceClient,
)
from apps.authentication.utils import get_client_ip, set_refresh_cookie, set_access_cookie
from apps.authentication.swagger import (
    block_schema, unblock_schema, deactivate_self_schema, deactivate_admin_schema,
    purge_schema, oauth_google_init_schema, oauth_google_callback_schema,
    oauth_facebook_init_schema, oauth_facebook_callback_schema,
    s2s_token_schema, s2s_introspect_schema,
)

logger = logging.getLogger(__name__)


# ─── Block / Unblock ─────────────────────────────────────────────────────────


@block_schema
class AdminBlockUserView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def post(self, request, user_id):
        try:
            user = UserAuth.objects.get(id=user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user.is_blocked = True
        user.save(update_fields=["is_blocked", "updated_at"])
        SessionService.revoke_all_sessions(user)
        return Response({"message": "User blocked", "user_id": str(user.id), "is_blocked": True})



@unblock_schema
class AdminUnblockUserView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def post(self, request, user_id):
        try:
            user = UserAuth.objects.get(id=user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user.is_blocked = False
        user.save(update_fields=["is_blocked", "updated_at"])
        return Response({"message": "User unblocked", "user_id": str(user.id), "is_blocked": False})


# ─── Deactivate ──────────────────────────────────────────────────────────────


@deactivate_self_schema
class AccountDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeactivateAccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserAuth.objects.get(id=request.user.auth_user_id)
        if not user.check_password(serializer.validated_data["password"]):
            return Response({"detail": "Mot de passe incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_deactivated = True
        user.save(update_fields=["is_deactivated", "updated_at"])
        SessionService.revoke_all_sessions(user)

        # Propager status-sync vers Users (CDC: POST /api/v1/users/status-sync)
        UsersServiceClient.sync_status(str(user.id), "inactive")

        return Response({"message": "Account deactivated", "is_deactivated": True})



@deactivate_admin_schema
class AdminDeactivateUserView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def post(self, request, auth_user_id):
        try:
            user = UserAuth.objects.get(id=auth_user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user.is_deactivated = True
        user.save(update_fields=["is_deactivated", "updated_at"])
        SessionService.revoke_all_sessions(user)

        UsersServiceClient.sync_status(str(user.id), "inactive")

        return Response({"message": "User deactivated", "user_id": str(user.id), "is_deactivated": True})


# ─── Purge RGPD ──────────────────────────────────────────────────────────────


@purge_schema
class AdminPurgeUserView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def delete(self, request, auth_user_id):
        try:
            user = UserAuth.objects.get(id=auth_user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        try:
            with transaction.atomic():
                VerificationToken.objects.filter(user=user).delete()
                LoginHistory.objects.filter(user=user).delete()
                OAuthProvider.objects.filter(user=user).delete()
                RefreshToken.objects.filter(user=user).delete()
                Session.objects.filter(user=user).delete()
                user.delete()
        except Exception as e:
            logger.error(f"Purge partielle échouée pour {auth_user_id}: {e}")
            return Response({"detail": "Échec de purge."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "User purged", "user_id": str(auth_user_id), "purged": True})


# ─── OAuth Google ────────────────────────────────────────────────────────────


@oauth_google_init_schema
class OAuthGoogleInitView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        platform_id = request.GET.get("platform_id", "")
        redirect_uri = request.GET.get("redirect_uri", settings.GOOGLE_REDIRECT_URI)
        state = sec.token_urlsafe(32)

        cache.set(f"oauth_state:{state}", {"platform_id": platform_id, "redirect_uri": redirect_uri}, timeout=600)

        params = (
            f"https://accounts.google.com/o/oauth2/v2/auth"
            f"?client_id={settings.GOOGLE_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
            f"&response_type=code"
            f"&scope=openid+email+profile"
            f"&state={state}"
            f"&access_type=offline"
        )
        return django_redirect(params)



@oauth_google_callback_schema
class OAuthGoogleCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")

        cached_state = cache.get(f"oauth_state:{state}")
        if not cached_state:
            return Response({"detail": "State OAuth invalide."}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(f"oauth_state:{state}")
        platform_id = cached_state.get("platform_id")

        try:
            platform = Platform.objects.get(id=platform_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # Échanger le code contre un token Google
        try:
            token_resp = httpx.post("https://oauth2.googleapis.com/token", data={
                "code": code, "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }, timeout=10.0)
            google_token = token_resp.json().get("access_token")
        except Exception as e:
            logger.error(f"Google token exchange failed: {e}")
            return Response({"detail": "Erreur OAuth Google."}, status=status.HTTP_502_BAD_GATEWAY)

        # Récupérer le profil Google
        try:
            profile_resp = httpx.get("https://www.googleapis.com/oauth2/v2/userinfo",
                                     headers={"Authorization": f"Bearer {google_token}"}, timeout=10.0)
            profile = profile_resp.json()
            google_id = profile.get("id")
            google_email = profile.get("email")
        except Exception as e:
            logger.error(f"Google profile fetch failed: {e}")
            return Response({"detail": "Erreur profil Google."}, status=status.HTTP_502_BAD_GATEWAY)

        # Trouver ou créer l'utilisateur
        try:
            oauth = OAuthProvider.objects.select_related("user").get(provider="google", provider_user_id=google_id)
            user = oauth.user
        except OAuthProvider.DoesNotExist:
            user = UserAuth.objects.filter(email=google_email).first()
            if not user:
                user = UserAuth.objects.create(
                    email=google_email, email_verified=True,
                    registration_method="google", registration_platform=platform,
                )
                UsersServiceClient.provision_user(str(user.id), email=google_email)
            OAuthProvider.objects.create(user=user, provider="google", provider_user_id=google_id, email=google_email)

        available, reason = user.is_available_for_login
        if not available:
            return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

        ip = get_client_ip(request)
        session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
        raw_refresh = SessionService.create_refresh_token(user, session)
        access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))

        LoginHistory.objects.create(user=user, platform=platform, method="google", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

        final_redirect = cached_state.get("redirect_uri", "/")
        response = django_redirect(final_redirect)
        set_access_cookie(response, access_token)
        set_refresh_cookie(response, raw_refresh)
        return response


# ─── OAuth Facebook ──────────────────────────────────────────────────────────


@oauth_facebook_init_schema
class OAuthFacebookInitView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        platform_id = request.GET.get("platform_id", "")
        redirect_uri = request.GET.get("redirect_uri", settings.FACEBOOK_REDIRECT_URI)
        state = sec.token_urlsafe(32)
        cache.set(f"oauth_state:{state}", {"platform_id": platform_id, "redirect_uri": redirect_uri}, timeout=600)

        params = (f"https://www.facebook.com/v19.0/dialog/oauth"
                  f"?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
                  f"&scope=email&state={state}")
        return django_redirect(params)



@oauth_facebook_callback_schema
class OAuthFacebookCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")
        cached_state = cache.get(f"oauth_state:{state}")
        if not cached_state:
            return Response({"detail": "State OAuth invalide."}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(f"oauth_state:{state}")
        platform_id = cached_state.get("platform_id")

        try:
            platform = Platform.objects.get(id=platform_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_resp = httpx.get(
                f"https://graph.facebook.com/v19.0/oauth/access_token"
                f"?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={settings.FACEBOOK_REDIRECT_URI}"
                f"&client_secret={settings.FACEBOOK_APP_SECRET}&code={code}", timeout=10.0)
            fb_token = token_resp.json().get("access_token")
            profile_resp = httpx.get(f"https://graph.facebook.com/me?fields=id,email&access_token={fb_token}", timeout=10.0)
            profile = profile_resp.json()
            fb_id = profile.get("id")
            fb_email = profile.get("email")
        except Exception as e:
            logger.error(f"Facebook OAuth failed: {e}")
            return Response({"detail": "Erreur OAuth Facebook."}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            oauth = OAuthProvider.objects.select_related("user").get(provider="facebook", provider_user_id=fb_id)
            user = oauth.user
        except OAuthProvider.DoesNotExist:
            user = UserAuth.objects.filter(email=fb_email).first() if fb_email else None
            if not user:
                user = UserAuth.objects.create(
                    email=fb_email, email_verified=bool(fb_email),
                    registration_method="facebook", registration_platform=platform,
                )
                UsersServiceClient.provision_user(str(user.id), email=fb_email)
            OAuthProvider.objects.create(user=user, provider="facebook", provider_user_id=fb_id, email=fb_email)

        available, reason = user.is_available_for_login
        if not available:
            return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

        ip = get_client_ip(request)
        session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
        raw_refresh = SessionService.create_refresh_token(user, session)
        access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))

        LoginHistory.objects.create(user=user, platform=platform, method="facebook", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

        response = django_redirect(cached_state.get("redirect_uri", "/"))
        set_access_cookie(response, access_token)
        set_refresh_cookie(response, raw_refresh)
        return response


# ─── S2S Tokens ──────────────────────────────────────────────────────────────


@s2s_token_schema
class S2STokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        client_id = request.data.get("client_id")
        client_secret = request.data.get("client_secret")
        if not client_id or not client_secret:
            return Response({"detail": "client_id et client_secret requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            platform = Platform.objects.get(id=client_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        if not platform.verify_client_secret(client_secret):
            return Response({"detail": "Secret invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        token = JWTService.generate_s2s_token(str(platform.id), platform.name)
        return Response({"access_token": token, "token_type": "Bearer", "expires_in": 3600, "service_name": platform.name})



@s2s_introspect_schema
class S2SIntrospectView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "token requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = JWTService.decode_token(token)
            if payload.get("type") != "s2s":
                return Response({"active": False})
            return Response({"active": True, "client_id": payload["sub"], "service_name": payload.get("service_name"), "exp": payload["exp"]})
        except Exception:
            return Response({"active": False})
