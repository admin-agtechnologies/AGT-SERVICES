"""
AGT Auth Service v1.0 — Platforms : Serializers.
"""
import secrets
import bcrypt
from rest_framework import serializers
from apps.authentication.models import Platform


class PlatformCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    slug = serializers.SlugField(max_length=50)
    allowed_auth_methods = serializers.ListField(
        child=serializers.ChoiceField(choices=["email", "phone", "google", "facebook", "magic_link"]),
        min_length=1,
    )
    allowed_redirect_urls = serializers.ListField(child=serializers.URLField(), required=False, default=list)

    def validate_slug(self, value):
        if Platform.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Ce slug est déjà utilisé.")
        return value

    def validate_name(self, value):
        if Platform.objects.filter(name=value).exists():
            raise serializers.ValidationError("Ce nom est déjà utilisé.")
        return value


class PlatformUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=False)
    allowed_auth_methods = serializers.ListField(
        child=serializers.ChoiceField(choices=["email", "phone", "google", "facebook", "magic_link"]),
        required=False,
    )
    allowed_redirect_urls = serializers.ListField(child=serializers.URLField(), required=False)
    is_active = serializers.BooleanField(required=False)


class PlatformResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ["id", "name", "slug", "allowed_auth_methods", "allowed_redirect_urls", "is_active", "created_at", "updated_at"]
