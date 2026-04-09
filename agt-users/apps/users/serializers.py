"""
AGT Users Service v1.0 - Serializers.
CDC v2.1 : email/phone read-only (seul Auth peut modifier via sync).
"""
from rest_framework import serializers
from apps.users.models import UserProfile, Address, UserMetadata


class UserProfileCreateSerializer(serializers.Serializer):
    auth_user_id = serializers.UUIDField()
    first_name = serializers.CharField(max_length=100, required=False, default="")
    last_name = serializers.CharField(max_length=100, required=False, default="")
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)

    def validate_auth_user_id(self, value):
        if UserProfile.objects.filter(auth_user_id=value).exists():
            raise serializers.ValidationError("Profil existant pour ce auth_user_id.")
        return value


class UserProfileUpdateSerializer(serializers.Serializer):
    """CDC v2.1 : email et phone NON modifiables ici."""
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    birth_date = serializers.DateField(required=False, allow_null=True)
    gender = serializers.CharField(max_length=20, required=False, allow_null=True)


class UserProfileResponseSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id", "auth_user_id", "first_name", "last_name", "full_name",
            "email", "phone", "avatar_url", "birth_date", "gender",
            "status", "created_at", "updated_at",
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserProfileMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "auth_user_id", "first_name", "last_name", "email", "status", "created_at"]


class StatusSyncSerializer(serializers.Serializer):
    auth_user_id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=["active", "inactive", "deleted"])


class CredentialsSyncSerializer(serializers.Serializer):
    auth_user_id = serializers.UUIDField()
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)


class AddressCreateSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20, required=False, allow_null=True)
    is_default = serializers.BooleanField(default=False)


class AddressUpdateSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50, required=False)
    street = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=100, required=False)
    country = serializers.CharField(max_length=100, required=False)
    postal_code = serializers.CharField(max_length=20, required=False, allow_null=True)


class AddressResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "type", "street", "city", "country", "postal_code", "is_default", "created_at"]


class UserMetadataResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMetadata
        fields = ["key", "value", "updated_at"]


class PhotoUpdateSerializer(serializers.Serializer):
    media_id = serializers.UUIDField()
