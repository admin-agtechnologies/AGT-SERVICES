"""
AGT Auth Service v1.0 — Serializers DRF.
"""
from rest_framework import serializers
from apps.authentication.models import UserAuth, Session, LoginHistory, OAuthProvider


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)
    password = serializers.CharField(min_length=8, required=False, write_only=True, allow_null=True)
    method = serializers.ChoiceField(choices=["email", "phone"])

    def validate(self, data):
        method = data.get("method")
        if method == "email":
            if not data.get("email"):
                raise serializers.ValidationError({"email": "Champ obligatoire pour method=email."})
            if not data.get("password"):
                raise serializers.ValidationError({"password": "Champ obligatoire pour method=email."})
        elif method == "phone":
            if not data.get("phone"):
                raise serializers.ValidationError({"phone": "Champ obligatoire pour method=phone."})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    platform_id = serializers.UUIDField()


class LoginPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    platform_id = serializers.UUIDField()


class MagicLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()
    platform_id = serializers.UUIDField()
    redirect_url = serializers.URLField()


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    otp_code = serializers.CharField(min_length=4, max_length=8)
    context = serializers.ChoiceField(choices=["registration", "login"])
    platform_id = serializers.UUIDField(required=False)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data["current_password"] == data["new_password"]:
            raise serializers.ValidationError("Le nouveau mot de passe doit être différent de l'ancien.")
        return data


class DeactivateAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)


class TwoFAConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)


class TwoFAVerifySerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)
    temp_token = serializers.CharField()


class TwoFADisableSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)


class SessionResponseSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source="platform.slug", read_only=True)
    is_current = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ["id", "platform", "ip_address", "user_agent", "created_at", "is_current"]

    def get_is_current(self, obj):
        current = self.context.get("current_session_id")
        return str(obj.id) == str(current) if current else False


class LoginHistoryResponseSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source="platform.slug", read_only=True)

    class Meta:
        model = LoginHistory
        fields = ["id", "method", "platform", "ip_address", "success", "created_at"]


class UserAuthResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = [
            "id", "email", "phone", "email_verified", "phone_verified",
            "two_fa_enabled", "registration_method", "is_blocked",
            "is_deactivated", "created_at",
        ]
class S2STokenRequestSerializer(serializers.Serializer):
    client_id = serializers.UUIDField(help_text="UUID de la plateforme (= Platform.id)")
    client_secret = serializers.CharField(help_text="Secret de la plateforme")

class S2SIntrospectRequestSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Token S2S a valider")