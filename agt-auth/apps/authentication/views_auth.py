"""
AGT Auth Service v1.0 - Views : Health, Register, Verify, Login, MagicLink.
"""
import logging
from datetime import timedelta

from django.conf import settings
from django.shortcuts import redirect as django_redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import Platform, UserAuth, VerificationToken, LoginHistory
from apps.authentication.serializers import (
    RegisterSerializer, VerifyEmailSerializer, VerifyOTPSerializer,
    LoginSerializer, LoginPhoneSerializer, MagicLinkSerializer,
)
from apps.authentication.services import (
    JWTService, TokenService, SessionService, NotificationClient, UsersServiceClient,
)
from apps.authentication.utils import get_client_ip, set_refresh_cookie, set_access_cookie
from apps.authentication.swagger import (
    health_schema, register_schema, verify_email_schema, verify_otp_schema,
    login_schema, login_phone_schema, magic_link_schema, magic_link_callback_schema,
)

logger = logging.getLogger(__name__)



@health_schema
class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        db_ok = redis_ok = True
        try:
            from django.db import connection
            connection.ensure_connection()
        except Exception:
            db_ok = False
        try:
            from django.core.cache import cache
            cache.set("health_ping", "pong", 5)
            redis_ok = cache.get("health_ping") == "pong"
        except Exception:
            redis_ok = False

        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({
            "status": "healthy" if db_ok and redis_ok else "degraded",
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
            "version": "1.0.0",
        }, status=code)



@register_schema
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        platform_id = request.headers.get("X-Platform-Id")
        if not platform_id:
            return Response({"detail": "Header X-Platform-Id requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            platform = Platform.objects.get(id=platform_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide ou inactive."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        method = data["method"]

        # Vérifier doublon
        if method == "email" and UserAuth.objects.filter(email=data["email"]).exists():
            return Response({"detail": "Email déjà utilisé."}, status=status.HTTP_409_CONFLICT)
        if method == "phone" and UserAuth.objects.filter(phone=data["phone"]).exists():
            return Response({"detail": "Téléphone déjà utilisé."}, status=status.HTTP_409_CONFLICT)

        # Vérifier méthode autorisée
        if method not in platform.allowed_auth_methods:
            return Response({"detail": f"Méthode '{method}' non autorisée sur cette plateforme."}, status=status.HTTP_400_BAD_REQUEST)

        user = UserAuth(registration_method=method, registration_platform=platform)

        if method == "email":
            user.email = data["email"]
            user.set_password(data["password"])
            user.save()

            # Token de vérification email
            raw_token = TokenService.generate_raw_token()
            VerificationToken.objects.create(
                user=user, token_hash=TokenService.hash_token(raw_token),
                type="email_verification",
                expires_at=timezone.now() + timedelta(hours=1),
            )

            NotificationClient.send(
                notification_type="email_verification",
                recipient={"email": user.email, "phone": None},
                template="auth_verify_email",
                data={"verification_url": f"{request.scheme}://{request.get_host()}/api/v1/auth/verify-email?token={raw_token}", "expires_in_minutes": 60, "platform_name": platform.name},
                priority="high",
            )

            # Provisioning Users
            UsersServiceClient.provision_user(str(user.id), email=user.email)

            return Response({
                "id": str(user.id), "email": user.email, "email_verified": False,
                "registration_method": "email", "registration_platform_id": str(platform.id),
                "message": "Verification email sent",
            }, status=status.HTTP_201_CREATED)

        elif method == "phone":
            user.phone = data["phone"]
            user.save()

            otp = TokenService.generate_otp()
            VerificationToken.objects.create(
                user=user, token_hash=TokenService.hash_token(otp),
                type="phone_otp", payload={"context": "registration"},
                expires_at=timezone.now() + timedelta(seconds=settings.OTP_TTL),
            )

            NotificationClient.send(
                notification_type="phone_otp",
                recipient={"email": None, "phone": user.phone},
                template="auth_otp_sms",
                data={"otp_code": otp, "expires_in_minutes": settings.OTP_TTL // 60, "platform_name": platform.name},
                priority="critical",
            )

            UsersServiceClient.provision_user(str(user.id), phone=user.phone)

            return Response({
                "id": str(user.id), "phone": user.phone, "phone_verified": False,
                "registration_method": "phone", "registration_platform_id": str(platform.id),
                "message": "OTP sent",
            }, status=status.HTTP_201_CREATED)



@verify_email_schema
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token_hash = TokenService.hash_token(serializer.validated_data["token"])
        try:
            vtoken = VerificationToken.objects.select_related("user").get(token_hash=token_hash, type="email_verification")
        except VerificationToken.DoesNotExist:
            return Response({"detail": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not vtoken.is_valid:
            return Response({"detail": "Token expiré ou déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

        vtoken.mark_as_used()
        vtoken.user.email_verified = True
        vtoken.user.save(update_fields=["email_verified", "updated_at"])

        return Response({"message": "Email verified", "email_verified": True})



@verify_otp_schema
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        token_hash = TokenService.hash_token(data["otp_code"])

        try:
            vtoken = VerificationToken.objects.select_related("user").get(token_hash=token_hash, type="phone_otp")
        except VerificationToken.DoesNotExist:
            return Response({"detail": "OTP invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not vtoken.is_valid:
            return Response({"detail": "OTP expiré ou déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

        vtoken.mark_as_used()
        user = vtoken.user

        if data["context"] == "registration":
            user.phone_verified = True
            user.save(update_fields=["phone_verified", "updated_at"])
            return Response({"message": "Phone verified", "phone_verified": True})

        elif data["context"] == "login":
            platform_id = data.get("platform_id")
            try:
                platform = Platform.objects.get(id=platform_id, is_active=True)
            except Platform.DoesNotExist:
                return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

            available, reason = user.is_available_for_login
            if not available:
                return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

            ip = get_client_ip(request)
            session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
            raw_refresh = SessionService.create_refresh_token(user, session)
            access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))

            LoginHistory.objects.create(user=user, platform=platform, method="phone", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

            response = Response({"access_token": access_token, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL})
            set_refresh_cookie(response, raw_refresh)
            return response



@login_schema
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            platform = Platform.objects.get(id=data["platform_id"], is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserAuth.objects.get(email=data["email"])
        except UserAuth.DoesNotExist:
            return Response({"detail": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

        available, reason = user.is_available_for_login
        if not available:
            LoginHistory.objects.create(user=user, platform=platform, method="email", ip_address=get_client_ip(request), user_agent=request.headers.get("User-Agent"), success=False, failure_reason=reason)
            return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(data["password"]):
            user.increment_failed_attempts()
            LoginHistory.objects.create(user=user, platform=platform, method="email", ip_address=get_client_ip(request), user_agent=request.headers.get("User-Agent"), success=False, failure_reason="invalid_password")
            return Response({"detail": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

        user.reset_failed_attempts()
        ip = get_client_ip(request)
        session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
        raw_refresh = SessionService.create_refresh_token(user, session)

        # 2FA check
        if user.two_fa_enabled:
            temp_token = JWTService.generate_temp_token(str(user.id), str(platform.id), str(session.id))
            LoginHistory.objects.create(user=user, platform=platform, method="email", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)
            return Response({"requires_2fa": True, "temp_token": temp_token, "token_type": "Bearer", "expires_in": 300})

        access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))
        LoginHistory.objects.create(user=user, platform=platform, method="email", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

        response = Response({"access_token": access_token, "token_type": "Bearer", "expires_in": settings.JWT_ACCESS_TTL, "requires_2fa": False})
        set_refresh_cookie(response, raw_refresh)
        return response



@login_phone_schema
class LoginPhoneView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginPhoneSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = UserAuth.objects.get(phone=data["phone"])
        except UserAuth.DoesNotExist:
            return Response({"message": "OTP sent", "expires_in": settings.OTP_TTL})

        otp = TokenService.generate_otp()
        VerificationToken.objects.create(
            user=user, token_hash=TokenService.hash_token(otp),
            type="phone_otp", payload={"context": "login", "platform_id": str(data["platform_id"])},
            expires_at=timezone.now() + timedelta(seconds=settings.OTP_TTL),
        )

        NotificationClient.send(
            notification_type="phone_otp",
            recipient={"email": None, "phone": user.phone},
            template="auth_otp_sms",
            data={"otp_code": otp, "expires_in_minutes": settings.OTP_TTL // 60},
            priority="critical",
        )

        return Response({"message": "OTP sent", "expires_in": settings.OTP_TTL})



@magic_link_schema
class MagicLinkRequestView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = MagicLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = UserAuth.objects.get(email=data["email"])
        except UserAuth.DoesNotExist:
            return Response({"message": "Magic link sent", "expires_in": settings.MAGIC_LINK_TTL})

        try:
            platform = Platform.objects.get(id=data["platform_id"], is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier redirect_url dans whitelist
        if data["redirect_url"] not in platform.allowed_redirect_urls:
            return Response({"detail": "redirect_url non autorisée."}, status=status.HTTP_400_BAD_REQUEST)

        raw_token = TokenService.generate_raw_token()
        VerificationToken.objects.create(
            user=user, token_hash=TokenService.hash_token(raw_token),
            type="magic_link",
            payload={"platform_id": str(platform.id), "redirect_url": data["redirect_url"]},
            expires_at=timezone.now() + timedelta(seconds=settings.MAGIC_LINK_TTL),
        )

        callback_url = f"{request.scheme}://{request.get_host()}/api/v1/auth/magic-link/callback?token={raw_token}"

        NotificationClient.send(
            notification_type="magic_link",
            recipient={"email": user.email, "phone": None},
            template="auth_magic_link",
            data={"magic_link_url": callback_url, "expires_in_minutes": settings.MAGIC_LINK_TTL // 60, "platform_name": platform.name},
            priority="high",
        )

        return Response({"message": "Magic link sent", "expires_in": settings.MAGIC_LINK_TTL})



@magic_link_callback_schema
class MagicLinkCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        raw_token = request.GET.get("token")
        if not raw_token:
            return Response({"detail": "Token manquant."}, status=status.HTTP_400_BAD_REQUEST)

        token_hash = TokenService.hash_token(raw_token)
        try:
            vtoken = VerificationToken.objects.select_related("user").get(token_hash=token_hash, type="magic_link")
        except VerificationToken.DoesNotExist:
            return Response({"detail": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not vtoken.is_valid:
            return Response({"detail": "Token expiré ou déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

        user = vtoken.user
        available, reason = user.is_available_for_login
        if not available:
            return Response({"detail": reason}, status=status.HTTP_403_FORBIDDEN)

        payload = vtoken.payload or {}
        platform_id = payload.get("platform_id")
        redirect_url = payload.get("redirect_url", "/")

        try:
            platform = Platform.objects.get(id=platform_id, is_active=True)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme invalide."}, status=status.HTTP_400_BAD_REQUEST)

        vtoken.mark_as_used()
        ip = get_client_ip(request)
        session = SessionService.create_session(user, platform, ip, request.headers.get("User-Agent"))
        raw_refresh = SessionService.create_refresh_token(user, session)
        access_token = JWTService.generate_access_token(user, str(platform.id), str(session.id))

        LoginHistory.objects.create(user=user, platform=platform, method="magic_link", ip_address=ip, user_agent=request.headers.get("User-Agent"), success=True)

        response = django_redirect(redirect_url)
        set_access_cookie(response, access_token)
        set_refresh_cookie(response, raw_refresh)
        return response
