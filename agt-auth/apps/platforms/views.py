from apps.authentication.swagger import platform_list_create_schema, platform_detail_schema
"""
AGT Auth Service v1.0 — Platforms : Views CRUD admin.
"""
import secrets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import Platform
from apps.authentication.permissions import IsAdminAPIKey
from apps.platforms.serializers import PlatformCreateSerializer, PlatformUpdateSerializer, PlatformResponseSerializer



@platform_list_create_schema
class PlatformListCreateView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def post(self, request):
        serializer = PlatformCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        raw_secret = secrets.token_urlsafe(48)

        platform = Platform.objects.create(
            name=data["name"],
            slug=data["slug"],
            allowed_auth_methods=data["allowed_auth_methods"],
            allowed_redirect_urls=data.get("allowed_redirect_urls", []),
            client_secret_hash=Platform.hash_client_secret(raw_secret),
        )

        response_data = PlatformResponseSerializer(platform).data
        response_data["client_secret"] = raw_secret  # Affiché uniquement à la création

        return Response(response_data, status=status.HTTP_201_CREATED)

    def get(self, request):
        platforms = Platform.objects.all()
        return Response({"data": PlatformResponseSerializer(platforms, many=True).data})



@platform_detail_schema
class PlatformDetailView(APIView):
    permission_classes = [IsAdminAPIKey]
    authentication_classes = []

    def put(self, request, platform_id):
        try:
            platform = Platform.objects.get(id=platform_id)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlatformUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for field, value in serializer.validated_data.items():
            setattr(platform, field, value)
        platform.save()

        return Response(PlatformResponseSerializer(platform).data)

    def delete(self, request, platform_id):
        try:
            platform = Platform.objects.get(id=platform_id)
        except Platform.DoesNotExist:
            return Response({"detail": "Plateforme introuvable."}, status=status.HTTP_404_NOT_FOUND)

        platform.is_active = False
        platform.save(update_fields=["is_active", "updated_at"])

        return Response({"message": "Platform deactivated", "is_active": False})
