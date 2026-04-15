"""
AGT Users Service v1.0 - Views : Profil, Adresses, Metadata, Sync, Stats.
CDC v2.1 : by-auth lookup, leave platform, hard delete securise.
"""
import logging
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import status, serializers as drf_serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.roles.models import UserRole

from apps.users.models import UserProfile, Address, UserMetadata, UserStatusChoice, AuditLog
from apps.users.pagination import StandardPagination
from apps.users.serializers import (
    UserProfileCreateSerializer, UserProfileUpdateSerializer,
    UserProfileResponseSerializer, UserProfileMinimalSerializer,
    AddressCreateSerializer, AddressUpdateSerializer, AddressResponseSerializer,
    UserMetadataResponseSerializer, PhotoUpdateSerializer,
    StatusSyncSerializer, CredentialsSyncSerializer,
)
from apps.users.services import ProfileCacheService, NotificationClient, AuthServiceClient

from drf_spectacular.utils import OpenApiParameter, OpenApiTypes
from drf_spectacular.openapi import AutoSchema

logger = logging.getLogger(__name__)



class MetadataUpsertSerializer(drf_serializers.Serializer):
    """Body libre clé-valeur — exemple : {"theme": "dark", "language": "fr"}"""
    class Meta:
        ref_name = "MetadataUpsert"



class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Health"], summary="Health check")
    def get(self, request):
        db_ok = redis_ok = True
        try:
            from django.db import connection
            connection.ensure_connection()
        except Exception:
            db_ok = False
        try:
            from django.core.cache import cache
            cache.set("health", "ok", 5)
            redis_ok = cache.get("health") == "ok"
        except Exception:
            redis_ok = False

        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({
            "status": "healthy" if db_ok and redis_ok else "degraded",
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
            "version": "1.0.0",
        }, status=code)

# --- Profil CRUD ---

class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Provisioning profil (par Auth)", request=UserProfileCreateSerializer)
    def post(self, request):
        """POST /users - Provisioning (appele par Auth apres inscription)."""
        serializer = UserProfileCreateSerializer(data=request.data)
        if not serializer.is_valid():
            if "auth_user_id" in serializer.errors:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user = UserProfile.objects.create(
            auth_user_id=data["auth_user_id"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email"),
            phone=data.get("phone"),
        )
        return Response(UserProfileResponseSerializer(user).data, status=status.HTTP_201_CREATED)

    @extend_schema(
    tags=["Profile"],
    summary="Listing pagine avec filtres",
    parameters=[
        OpenApiParameter(name="status", type=OpenApiTypes.STR, required=False, description="Filtrer par statut : active, inactive, deleted"),
        OpenApiParameter(name="platform_id", type=OpenApiTypes.UUID, required=False, description="Filtrer par plateforme"),
        OpenApiParameter(name="role", type=OpenApiTypes.STR, required=False, description="Filtrer par nom de role"),
    ]
)
    def get(self, request):
        """GET /users - Listing pagine avec filtres."""
        qs = UserProfile.objects.all()

        status_filter = request.GET.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)

        platform = request.GET.get("platform_id")
        role = request.GET.get("role")
        if platform or role:
            from apps.roles.models import UserRole
            ur_qs = UserRole.objects.all()
            if platform:
                ur_qs = ur_qs.filter(role__platform_id=platform)
            if role:
                ur_qs = ur_qs.filter(role__name=role)
            user_ids = ur_qs.values_list("user_id", flat=True)
            qs = qs.filter(id__in=user_ids)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(UserProfileMinimalSerializer(page, many=True).data)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Consultation profil")
    def get(self, request, user_id):
        """GET /users/{id}"""
        cached = ProfileCacheService.get(str(user_id))
        if cached:
            return Response(cached)

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        data = UserProfileResponseSerializer(user).data
        ProfileCacheService.set(str(user_id), data)
        return Response(data)

    @extend_schema(tags=["Profile"], summary="Mise a jour profil (email/phone read-only)", request=UserProfileUpdateSerializer)
    def put(self, request, user_id):
        """PUT /users/{id} - email/phone NON modifiables (CDC v2.1)."""
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        old_values = {}
        for field, value in serializer.validated_data.items():
            old_values[field] = getattr(user, field)
            setattr(user, field, value)

        user.save(update_fields=list(serializer.validated_data.keys()) + ["updated_at"])
        ProfileCacheService.invalidate(str(user_id))

        # Convertir les valeurs en types JSON-compatibles via DjangoJSONEncoder
        old_json = json.loads(json.dumps(old_values, cls=DjangoJSONEncoder))
        new_json = json.loads(json.dumps(dict(serializer.validated_data), cls=DjangoJSONEncoder))
        AuditLog.objects.create(
            entity_type="users_profiles", entity_id=user.id, action="update",
            actor_id=getattr(request.user, "auth_user_id", None), actor_type="user",
            old_value=old_json, new_value=new_json,
        )

        return Response(UserProfileResponseSerializer(user).data)

    @extend_schema(tags=["Profile"], summary="Soft delete global")
    def delete(self, request, user_id):
        """DELETE /users/{id} - Soft delete global + deactivate Auth."""
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user.soft_delete()
        ProfileCacheService.invalidate(str(user_id))

        # Propager deactivation vers Auth (CDC v2.1 : S2S sans mot de passe)
        AuthServiceClient.deactivate_user(str(user.auth_user_id))

        AuditLog.objects.create(
            entity_type="users_profiles", entity_id=user.id, action="soft_delete",
            actor_id=getattr(request.user, "auth_user_id", None),
        )

        return Response({
            "message": "Account deactivated",
            "status": "deleted",
            "hard_delete_scheduled": user.hard_delete_after.isoformat() if user.hard_delete_after else None,
        })


class UserByAuthView(APIView):
    """GET /users/by-auth/{authUserId} - Lookup par auth_user_id (CDC v2.1)."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Lookup par auth_user_id")
    def get(self, request, auth_user_id):
        try:
            user = UserProfile.objects.get(auth_user_id=auth_user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserProfileResponseSerializer(user).data)


class UserLeavePlatformView(APIView):
    """DELETE /users/{id}/platforms/{platformId} - Quitter une plateforme (CDC v2.1)."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Quitter une plateforme")
    def delete(self, request, user_id, platform_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        from apps.roles.models import UserRole
        roles_removed = UserRole.objects.filter(user=user, role__platform_id=platform_id).delete()[0]

        metadata_cleared = UserMetadata.objects.filter(user=user, platform_id=platform_id).delete()[0] > 0

        from apps.documents.models import Document
        docs_archived = Document.objects.filter(user=user, platform_id=platform_id).update(
            status="archived"
        )

        AuditLog.objects.create(
            entity_type="users_profiles", entity_id=user.id, action="leave_platform",
            actor_id=getattr(request.user, "auth_user_id", None),
            new_value={"platform_id": str(platform_id), "roles_removed": roles_removed},
        )

        return Response({
            "message": "Platform left",
            "platform_id": str(platform_id),
            "roles_removed": roles_removed,
            "metadata_cleared": metadata_cleared,
            "documents_archived": docs_archived,
        })


class UserPermanentDeleteView(APIView):
    """DELETE /users/{id}/permanent - Hard delete RGPD securise (CDC v2.1)."""
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Hard delete RGPD")
    def delete(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        # Etape 1 : marquer deletion_in_progress
        user.status = UserStatusChoice.DELETION_IN_PROGRESS
        user.save(update_fields=["status", "updated_at"])

        # Etape 2 : purge Auth
        auth_purged = AuthServiceClient.purge_user(str(user.auth_user_id))

        if not auth_purged:
            user.purge_auth_pending = True
            user.deletion_error_reason = "Auth purge failed - will retry"
            user.save(update_fields=["purge_auth_pending", "deletion_error_reason", "updated_at"])
            return Response({
                "detail": "Purge Auth echouee. Retry planifie.",
                "purge_auth_pending": True,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Etape 3 : purge Users
        ProfileCacheService.invalidate(str(user_id))
        user.hard_delete()

        return Response({"message": "Compte supprime definitivement (RGPD)."})


class UserPhotoView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Mise a jour photo profil", request=PhotoUpdateSerializer)
    def put(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PhotoUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user.avatar_url = f"media://{serializer.validated_data['media_id']}"
        user.save(update_fields=["avatar_url", "updated_at"])
        ProfileCacheService.invalidate(str(user_id))
        return Response(UserProfileResponseSerializer(user).data)


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Profile"], summary="Recherche utilisateurs",
        parameters=[OpenApiParameter(name="q", type=OpenApiTypes.STR, required=True, description="Terme de recherche")]
    )
    def get(self, request):
        q = request.GET.get("q", "").strip()
        if not q:
            return Response({"detail": "Parametre 'q' requis."}, status=status.HTTP_400_BAD_REQUEST)

        qs = UserProfile.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(email__icontains=q) | Q(phone__icontains=q)
        ).exclude(status=UserStatusChoice.DELETED)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(UserProfileMinimalSerializer(page, many=True).data)


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"], summary="Statistiques globales")
    def get(self, request):
        total = UserProfile.objects.count()
        by_status = dict(
            UserProfile.objects.values_list("status")
            .annotate(count=Count("id"))
        )

        return Response({
            "total_users": total,
            "by_status": {
                "active": by_status.get("active", 0),
                "inactive": by_status.get("inactive", 0),
                "deleted": by_status.get("deleted", 0),
                "deletion_in_progress": by_status.get("deletion_in_progress", 0),
            },
        })


# --- Sync endpoints (appeles par Service Auth) ---

class StatusSyncView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Sync"], summary="Sync statut depuis Auth", request=StatusSyncSerializer)
    def post(self, request):
        serializer = StatusSyncSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = UserProfile.objects.get(auth_user_id=data["auth_user_id"])
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        new_status = data["status"]
        if new_status == "inactive":
            user.status = UserStatusChoice.INACTIVE
        elif new_status == "active":
            user.status = UserStatusChoice.ACTIVE
        elif new_status == "deleted":
            user.soft_delete()
            return Response({"message": "Statut synchronise.", "status": new_status})

        user.save(update_fields=["status", "updated_at"])
        ProfileCacheService.invalidate(str(user.id))
        return Response({"message": "Statut synchronise.", "status": new_status})


class CredentialsSyncView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Sync"], summary="Sync email/phone depuis Auth", request=CredentialsSyncSerializer)
    def post(self, request):
        serializer = CredentialsSyncSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = UserProfile.objects.get(auth_user_id=data["auth_user_id"])
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        updated = []
        if data.get("email"):
            user.email = data["email"]
            updated.append("email")
        if data.get("phone"):
            user.phone = data["phone"]
            updated.append("phone")

        if updated:
            user.save(update_fields=updated + ["updated_at"])
            ProfileCacheService.invalidate(str(user.id))

        return Response({"message": "Identifiants synchronises."})


# --- Adresses ---

class AddressListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Addresses"], summary="Ajouter une adresse", request=AddressCreateSerializer)
    def post(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address = Address.objects.create(user=user, **serializer.validated_data)
        if serializer.validated_data.get("is_default"):
            address.set_as_default()

        return Response(AddressResponseSerializer(address).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Addresses"], summary="Lister les adresses")
    def get(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)
        addresses = Address.objects.filter(user=user)
        return Response({"data": AddressResponseSerializer(addresses, many=True).data})


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Addresses"], summary="Modifier une adresse", request=AddressUpdateSerializer)
    def put(self, request, user_id, address_id):
        try:
            address = Address.objects.get(id=address_id, user_id=user_id)
        except Address.DoesNotExist:
            return Response({"detail": "Adresse introuvable."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for field, value in serializer.validated_data.items():
            setattr(address, field, value)
        address.save()
        return Response(AddressResponseSerializer(address).data)

    @extend_schema(tags=["Addresses"], summary="Supprimer une adresse")
    def delete(self, request, user_id, address_id):
        try:
            address = Address.objects.get(id=address_id, user_id=user_id)
        except Address.DoesNotExist:
            return Response({"detail": "Adresse introuvable."}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response({"message": "Adresse supprimee."})


class AddressSetDefaultView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Addresses"], summary="Definir adresse par defaut")
    def put(self, request, user_id, address_id):
        try:
            address = Address.objects.get(id=address_id, user_id=user_id)
        except Address.DoesNotExist:
            return Response({"detail": "Adresse introuvable."}, status=status.HTTP_404_NOT_FOUND)
        address.set_as_default()
        return Response({"message": "Adresse par defaut mise a jour.", "id": str(address.id)})


# --- Metadata ---

class UserMetadataView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
    tags=["Metadata"],
    summary="Upsert metadata",
    request={
        "application/json": {
            "type": "object",
            "additionalProperties": {"type": "string"},
            "example": {"theme": "dark", "language": "fr", "notifications": "true"}
        }
    }
)
    def put(self, request, user_id, platform_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        if not isinstance(request.data, dict):
            return Response({"detail": "Body JSON (objet) requis."}, status=status.HTTP_400_BAD_REQUEST)

        upserted = []
        for key, value in request.data.items():
            UserMetadata.objects.update_or_create(
                user=user, platform_id=platform_id, key=key,
                defaults={"value": str(value)},
            )
            upserted.append({"key": key, "value": str(value)})

        return Response({"platform_id": platform_id, "metadata": upserted})

    @extend_schema(tags=["Metadata"], summary="Lire metadata par plateforme")
    def get(self, request, user_id, platform_id):
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        metadata = UserMetadata.objects.filter(user_id=user_id, platform_id=platform_id)
        result = {m.key: m.value for m in metadata}
        return Response({"user_id": str(user_id), "platform_id": platform_id, "metadata": result})


class UserMetadataKeyDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Metadata"], summary="Supprimer une cle metadata")
    def delete(self, request, user_id, platform_id, key):
        deleted, _ = UserMetadata.objects.filter(user_id=user_id, platform_id=platform_id, key=key).delete()
        if not deleted:
            return Response({"detail": "Cle introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": f"Cle '{key}' supprimee."})
