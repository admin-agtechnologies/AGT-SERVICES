from django.urls import path
from apps.roles.views import (
    RoleListCreateView, RoleDetailView,
    PermissionListCreateView, RolePermissionView,
    UserRoleListCreateView, UserRoleDeleteView, PermissionCheckView,
)

urlpatterns = [
    # Roles
    path("platforms/<uuid:platform_id>/roles", RoleListCreateView.as_view(), name="roles-list-create"),
    path("platforms/<uuid:platform_id>/roles/<uuid:role_id>", RoleDetailView.as_view(), name="roles-detail"),

    # Permissions
    path("platforms/<uuid:platform_id>/permissions", PermissionListCreateView.as_view(), name="permissions-list-create"),

    # Attacher/détacher une permission à un rôle — perm_id obligatoire dans l'URL
    path("platforms/<uuid:platform_id>/roles/<uuid:role_id>/permissions/<uuid:perm_id>", RolePermissionView.as_view(), name="role-permission-detail"),

    # User Roles
    path("users/<uuid:user_id>/roles", UserRoleListCreateView.as_view(), name="user-roles"),
    path("users/<uuid:user_id>/roles/<uuid:role_id>", UserRoleDeleteView.as_view(), name="user-role-delete"),

    # Permission Check
    path("users/<uuid:user_id>/permissions/check", PermissionCheckView.as_view(), name="permission-check"),
]
