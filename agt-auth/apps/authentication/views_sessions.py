"""
AGT Auth Service v1.0 — Views : Sessions, Tokens, 2FA, Password, Profile, Audit.
"""
import logging
from datetime import timedelta, datetime

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import Session, RefreshToken, VerificationToken, LoginHistory, UserAuth
from apps.authentication.pagination import StandardPagination
from apps.authentication.serializers import (
    ChangePasswordSerializer, ResetPasswordSerializer, ForgotPasswordSerializer,
    TwoFAConfirmSerializer, TwoFAVerifySerializer, TwoFADisableSerializer,
    SessionResponseSerializer, LoginHistoryResponseSerializer, UserAuthResponseSerializer,
)
from apps.authentication.services import JWTService, TokenService, TOTPService, SessionService, NotificationClient, UsersServiceClient
from apps.authentication.utils import get_client_ip, set_refresh_cookie, clear_refresh_cookie, clear_access_cookie
from apps.authentication.swagger import (
    refresh_schema, logout_schema, session_list_schema, session_revoke_schema,
    verify_token_schema, token_exchange_schema, forgot_password_schema, reset_password_schema,
    change_password_schema, twofa_enable_schema, twofa_confirm_schema, twofa_verify_schema,
    twofa_disable_schema, me_schema, login_history_schema, user_stats_schema,
)

logger = logging.getLogger(__name__)



@refresh_schema
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        raw_refresh = request.COOKIES.get("refresh_token")
        if not raw_refresh:
            return Response({"detail": "Refresh token manquant."}, status=status.HTTP_401_UNAUTHORIZED)

        token_hash = TokenService.hash_refresh_token(raw_refresh)
        try:
            rt = RefreshToken.objects.select_related("user", "session", "session__platform").get(token_hash=token_hash, is_revoked=False)
        except RefreshToken.DoesNotExist:
            return Response({"detail": "Refresh token invalide ou révoqué."}, status=status.HTTP_401_UNAUTHORIZED)

        if rt.is_expired():
            return Response({"detail": "Refresh token expiré."}, status=status.HTTP_401_UNAUTHORIZED)

        user = rt.user
        available, reason = user.is_available_for_login
        if not available:
            return Response({"valid": False, "reason": reason}, status=status.HTTP_403_FORBIDDEN)

        session = rt.session
        if not session.is_active or session.is_expired():
            return Response({"detail": "Session expirée."}, status=status.HTTP_401_UNAUTHORIZED)

        rt.revoke()
        new_raw_refresh = SessionService.create_refresh_token(user, session)
        access_token = JWTService.generate_access_token(user, str(session.platform_id), str(session.id))

        response = Response({"access_token": access_token, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL})
        set_refresh_cookie(response, new_raw_refresh)
        return response



@logout_schema
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = request.auth
        session_id = payload.get("session_id") if payload else None
        if session_id:
            try:
                session = Session.objects.get(id=session_id)
                SessionService.revoke_session(session)
            except Session.DoesNotExist:
                pass

        response = Response({"message": "Logged out successfully"})
        clear_refresh_cookie(response)
        return response



@session_list_schema
class SessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = request.auth
        current_session_id = payload.get("session_id") if payload else None
        sessions = Session.objects.filter(user_id=request.user.auth_user_id, is_active=True).select_related("platform")
        paginator = StandardPagination()
        page = paginator.paginate_queryset(sessions, request)
        serializer = SessionResponseSerializer(page, many=True, context={"current_session_id": current_session_id})
        return paginator.get_paginated_response(serializer.data)



@session_revoke_schema
class SessionRevokeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, session_id):
        try:
            session = Session.objects.get(id=session_id, user_id=request.user.auth_user_id, is_active=True)
        except Session.DoesNotExist:
            return Response({"detail": "Session introuvable."}, status=status.HTTP_404_NOT_FOUND)
        SessionService.revoke_session(session)
        return Response({"message": "Session revoked"})



@verify_token_schema
class VerifyTokenView(APIView):
    """Endpoint interne — vérifie un JWT utilisateur (6 vérifications CDC)."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return Response({"valid": False, "reason": "missing_token"}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(" ", 1)[1]
        try:
            payload = JWTService.decode_token(token)
        except jwt.ExpiredSignatureError:
            return Response({"valid": False, "reason": "token_expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"valid": False, "reason": "invalid_signature"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = UserAuth.objects.get(id=payload["sub"])
        except UserAuth.DoesNotExist:
            return Response({"valid": False, "reason": "user_not_found"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_blocked:
            return Response({"valid": False, "reason": "user_blocked"}, status=status.HTTP_401_UNAUTHORIZED)
        if user.is_deactivated:
            return Response({"valid": False, "reason": "user_deactivated"}, status=status.HTTP_401_UNAUTHORIZED)

        session_id = payload.get("session_id")
        try:
            session = Session.objects.select_related("platform").get(id=session_id)
        except Session.DoesNotExist:
            return Response({"valid": False, "reason": "session_revoked"}, status=status.HTTP_401_UNAUTHORIZED)

        if not session.is_active or session.is_expired():
            return Response({"valid": False, "reason": "session_revoked"}, status=status.HTTP_401_UNAUTHORIZED)
        if not session.platform.is_active:
            return Response({"valid": False, "reason": "platform_inactive"}, status=status.HTTP_401_UNAUTHORIZED)

        expires_at = datetime.utcfromtimestamp(payload["exp"]).isoformat() + "Z"
        return Response({"valid": True, "user_id": str(user.id), "platform_id": payload.get("platform_id"), "expires_at": expires_at})



@token_exchange_schema
class TokenExchangeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        raw_access = request.COOKIES.get("access_token")
        if not raw_access:
            return Response({"detail": "Cookie access_token absent."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            JWTService.decode_token(raw_access)
        except jwt.InvalidTokenError:
            return Response({"detail": "Token invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response({"access_token": raw_access, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL})
        clear_access_cookie(response)
        return response



@forgot_password_schema
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            user = UserAuth.objects.get(email=email)
            raw_token = TokenService.generate_raw_token()
            VerificationToken.objects.create(
                user=user, token_hash=TokenService.hash_token(raw_token),
                type="password_reset",
                expires_at=timezone.now() + timedelta(hours=1),
            )
           # Récupérer le prénom depuis Users (non bloquant)
            first_name = ""
            try:
                profile = UsersServiceClient.get_profile_by_auth_id(str(user.id))
                first_name = profile.get("first_name", "")
            except Exception:
                pass

            NotificationClient.send(
                notification_type="password_reset",
                recipient={"user_id": str(user.id), "email": email, "phone": None, "platform_id": str(user.registration_platform_id)},
                template="auth_reset_password",
                data={
                    "reset_url": f"{request.scheme}://{request.get_host()}/api/v1/auth/reset-password?token={raw_token}",
                    "expires_in_minutes": 60,
                    "platform_name": user.registration_platform.name if user.registration_platform else "",
                    "first_name": first_name,
                },
                priority="high",
            )
        except UserAuth.DoesNotExist:
            pass

        return Response({"message": "Reset link sent if account exists"})



@reset_password_schema
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        token_hash = TokenService.hash_token(data["token"])

        try:
            vtoken = VerificationToken.objects.select_related("user").get(token_hash=token_hash, type="password_reset")
        except VerificationToken.DoesNotExist:
            return Response({"detail": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not vtoken.is_valid:
            return Response({"detail": "Token expiré ou déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

        vtoken.mark_as_used()
        user = vtoken.user
        user.set_password(data["new_password"])
        user.save(update_fields=["password_hash", "updated_at"])
        SessionService.revoke_all_sessions(user)

        return Response({"message": "Password reset successfully"})



@change_password_schema
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserAuth.objects.get(id=request.user.auth_user_id)
        if not user.check_password(serializer.validated_data["current_password"]):
            return Response({"detail": "Mot de passe actuel incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password_hash", "updated_at"])

        current_session_id = request.auth.get("session_id") if request.auth else None
        SessionService.revoke_all_sessions(user, except_session_id=current_session_id)

        return Response({"message": "Password changed successfully"})



@twofa_enable_schema
class TwoFAEnableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = UserAuth.objects.get(id=request.user.auth_user_id)
        if user.two_fa_enabled:
            return Response({"detail": "2FA déjà activé."}, status=status.HTTP_400_BAD_REQUEST)

        secret = TOTPService.generate_secret()
        user.two_fa_secret = TOTPService.encrypt_secret(secret)
        user.save(update_fields=["two_fa_secret", "updated_at"])

        return Response({
            "secret": secret,
            "qr_code_url": TOTPService.get_totp_uri(secret, user.email or str(user.id)),
            "message": "Scan QR code, then verify with POST /auth/2fa/confirm",
        })



@twofa_confirm_schema
class TwoFAConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TwoFAConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserAuth.objects.get(id=request.user.auth_user_id)
        if not user.two_fa_secret:
            return Response({"detail": "2FA non initialisé."}, status=status.HTTP_400_BAD_REQUEST)

        secret = TOTPService.decrypt_secret(user.two_fa_secret)
        if not TOTPService.verify_code(secret, serializer.validated_data["code"]):
            return Response({"detail": "Code invalide."}, status=status.HTTP_400_BAD_REQUEST)

        user.two_fa_enabled = True
        user.save(update_fields=["two_fa_enabled", "updated_at"])

        return Response({"message": "2FA activated", "two_fa_enabled": True})



@twofa_verify_schema
class TwoFAVerifyView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = TwoFAVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            payload = JWTService.decode_token(data["temp_token"])
        except jwt.InvalidTokenError:
            return Response({"detail": "Temp token invalide."}, status=status.HTTP_401_UNAUTHORIZED)

        if payload.get("type") != "2fa_challenge":
            return Response({"detail": "Token type invalide."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserAuth.objects.get(id=payload["sub"])
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        secret = TOTPService.decrypt_secret(user.two_fa_secret)
        if not TOTPService.verify_code(secret, data["code"]):
            return Response({"detail": "Code 2FA invalide."}, status=status.HTTP_400_BAD_REQUEST)

        access_token = JWTService.generate_access_token_2fa(user, payload["platform_id"], payload["session_id"])
        response = Response({"access_token": access_token, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL})
        return response



@twofa_disable_schema
class TwoFADisableView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TwoFADisableSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserAuth.objects.get(id=request.user.auth_user_id)
        if not user.two_fa_enabled:
            return Response({"detail": "2FA non activé."}, status=status.HTTP_400_BAD_REQUEST)

        secret = TOTPService.decrypt_secret(user.two_fa_secret)
        if not TOTPService.verify_code(secret, serializer.validated_data["code"]):
            return Response({"detail": "Code invalide."}, status=status.HTTP_400_BAD_REQUEST)

        user.two_fa_enabled = False
        user.two_fa_secret = None
        user.save(update_fields=["two_fa_enabled", "two_fa_secret", "updated_at"])

        return Response({"message": "2FA disabled", "two_fa_enabled": False})



@me_schema
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = UserAuth.objects.get(id=request.user.auth_user_id)
        return Response(UserAuthResponseSerializer(user).data)



@login_history_schema
class LoginHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = LoginHistory.objects.filter(user_id=request.user.auth_user_id).select_related("platform")
        platform_slug = request.GET.get("platform")
        if platform_slug:
            history = history.filter(platform__slug=platform_slug)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(history, request)
        return paginator.get_paginated_response(LoginHistoryResponseSerializer(page, many=True).data)



@user_stats_schema
class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = UserAuth.objects.get(id=user_id)
        except UserAuth.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        total_logins = LoginHistory.objects.filter(user=user, success=True).count()
        last_login = LoginHistory.objects.filter(user=user, success=True).order_by("-created_at").values_list("created_at", flat=True).first()
        active_sessions = Session.objects.filter(user=user, is_active=True).count()

        return Response({
            "user_id": str(user.id),
            "total_logins": total_logins,
            "last_login": last_login.isoformat() if last_login else None,
            "active_sessions": active_sessions,
        })
