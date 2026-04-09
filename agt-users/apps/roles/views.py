"""
AGT Users Service v1.0 - Views : Roles, Permissions, UserRoles, PermissionCheck.
RBAC 100% dynamique. platform_id = UUID Auth directement.
"""
import logging
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.roles.models import Role, Permission, RolePermission, UserRole
from apps.users.models import UserProfile
from apps.users.services import PermissionCacheService, NotificationClient

logger = logging.getLogger(__name__)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "platform_id", "name", "description", "created_at"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "platform_id", "name", "description", "created_at"]


# --- Roles CRUD ---

class RoleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Roles"], summary="Creer un role pour une plateforme")
    def post(self, request, platform_id):
        name = request.data.get("name")
        description = request.data.get("description", "")
        if not name:
            return Response({"detail": "name requis."}, status=status.HTTP_400_BAD_REQUEST)

        if Role.objects.filter(platform_id=platform_id, name=name).exists():
            return Response({"detail": "Role existe deja."}, status=status.HTTP_409_CONFLICT)

        role = Role.objects.create(platform_id=platform_id, name=name, description=description)
        return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Roles"], summary="Lister les roles d'une plateforme")
    def get(self, request, platform_id):
        roles = Role.objects.filter(platform_id=platform_id)
        return Response({"data": RoleSerializer(roles, many=True).data})


class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Roles"], summary="Modifier un role")
    def put(self, request, platform_id, role_id):
        try:
            role = Role.objects.get(id=role_id, platform_id=platform_id)
        except Role.DoesNotExist:
            return Response({"detail": "Role introuvable."}, status=status.HTTP_404_NOT_FOUND)

        if "name" in request.data:
            role.name = request.data["name"]
        if "description" in request.data:
            role.description = request.data["description"]
        role.save()
        return Response(RoleSerializer(role).data)

    @extend_schema(tags=["Roles"], summary="Supprimer un role")
    def delete(self, request, platform_id, role_id):
        deleted, _ = Role.objects.filter(id=role_id, platform_id=platform_id).delete()
        if not deleted:
            return Response({"detail": "Role introuvable."}, status=status.HTTP_404_NOT_FOUND)
        PermissionCacheService.invalidate_role(str(role_id))
        return Response({"message": "Role supprime."})


# --- Permissions CRUD ---

class PermissionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Permissions"], summary="Creer une permission")
    def post(self, request, platform_id):
        name = request.data.get("name")
        description = request.data.get("description", "")
        if not name:
            return Response({"detail": "name requis."}, status=status.HTTP_400_BAD_REQUEST)

        if Permission.objects.filter(platform_id=platform_id, name=name).exists():
            return Response({"detail": "Permission existe deja."}, status=status.HTTP_409_CONFLICT)

        perm = Permission.objects.create(platform_id=platform_id, name=name, description=description)
        return Response(PermissionSerializer(perm).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Permissions"], summary="Lister les permissions d'une plateforme")
    def get(self, request, platform_id):
        perms = Permission.objects.filter(platform_id=platform_id)
        return Response({"data": PermissionSerializer(perms, many=True).data})


# --- Role-Permission liaison ---

class RolePermissionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Roles"], summary="Attacher une permission a un role")
    def post(self, request, platform_id, role_id):
        perm_id = request.data.get("permission_id")
        if not perm_id:
            return Response({"detail": "permission_id requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            role = Role.objects.get(id=role_id, platform_id=platform_id)
            perm = Permission.objects.get(id=perm_id, platform_id=platform_id)
        except (Role.DoesNotExist, Permission.DoesNotExist):
            return Response({"detail": "Role ou permission introuvable."}, status=status.HTTP_404_NOT_FOUND)

        _, created = RolePermission.objects.get_or_create(role=role, permission=perm)
        PermissionCacheService.invalidate_role(str(role_id))

        if created:
            return Response({"message": "Permission attachee."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Permission deja attachee."})

    @extend_schema(tags=["Roles"], summary="Detacher une permission d'un role")
    def delete(self, request, platform_id, role_id, perm_id):
        deleted, _ = RolePermission.objects.filter(role_id=role_id, permission_id=perm_id).delete()
        if not deleted:
            return Response({"detail": "Liaison introuvable."}, status=status.HTTP_404_NOT_FOUND)
        PermissionCacheService.invalidate_role(str(role_id))
        return Response({"message": "Permission detachee."})


# --- User Roles ---

class UserRoleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["User Roles"], summary="Assigner un role a un utilisateur")
    def post(self, request, user_id):
        role_id = request.data.get("role_id")
        if not role_id:
            return Response({"detail": "role_id requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserProfile.objects.get(id=user_id)
            role = Role.objects.get(id=role_id)
        except (UserProfile.DoesNotExist, Role.DoesNotExist):
            return Response({"detail": "Utilisateur ou role introuvable."}, status=status.HTTP_404_NOT_FOUND)

        assigned_by = getattr(request.user, "auth_user_id", None)
        _, created = UserRole.objects.get_or_create(user=user, role=role, defaults={"assigned_by": assigned_by})

        if created:
            NotificationClient.notify_role_assigned(user.email, role.name, str(role.platform_id))

        return Response({
            "user_id": str(user.id),
            "role": RoleSerializer(role).data,
            "assigned": created,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @extend_schema(tags=["User Roles"], summary="Lister les roles d'un utilisateur")
    def get(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        qs = UserRole.objects.filter(user=user).select_related("role")
        platform_filter = request.GET.get("platform_id")
        if platform_filter:
            qs = qs.filter(role__platform_id=platform_filter)

        roles = []
        for ur in qs:
            roles.append({
                "role": {"id": str(ur.role.id), "name": ur.role.name, "platform_id": str(ur.role.platform_id)},
                "assigned_at": ur.assigned_at.isoformat(),
                "assigned_by": str(ur.assigned_by) if ur.assigned_by else None,
            })

        return Response({"user_id": str(user.id), "roles": roles})


class UserRoleDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["User Roles"], summary="Retirer un role a un utilisateur")
    def delete(self, request, user_id, role_id):
        deleted, _ = UserRole.objects.filter(user_id=user_id, role_id=role_id).delete()
        if not deleted:
            return Response({"detail": "Assignation introuvable."}, status=status.HTTP_404_NOT_FOUND)
        PermissionCacheService.invalidate_user_platform(str(user_id), "")
        return Response({"message": "Role retire."})


# --- Permission Check ---

class PermissionCheckView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Permissions"], summary="Verifier une permission (cache Redis)")
    def get(self, request, user_id):
        platform_id = request.GET.get("platform_id")
        perm_name = request.GET.get("permission")

        if not platform_id or not perm_name:
            return Response({"detail": "platform_id et permission requis."}, status=status.HTTP_400_BAD_REQUEST)

        cached = PermissionCacheService.get(str(user_id), platform_id, perm_name)
        if cached is not None:
            return Response(cached)

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        user_roles = UserRole.objects.filter(user=user, role__platform_id=platform_id).select_related("role")

        granted = False
        via_role = None

        for ur in user_roles:
            has_perm = RolePermission.objects.filter(
                role=ur.role, permission__name=perm_name, permission__platform_id=platform_id,
            ).exists()
            if has_perm:
                granted = True
                via_role = ur.role.name
                break

        result = {
            "user_id": str(user_id), "platform_id": platform_id,
            "permission": perm_name, "granted": granted, "via_role": via_role,
        }
        PermissionCacheService.set(str(user_id), platform_id, perm_name, result)
        return Response(result)
