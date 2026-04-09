"""
AGT Auth Service v1.0 — Permissions DRF customisées.
"""
from rest_framework.permissions import BasePermission
from apps.authentication.authentication import AdminAPIKeyAuthentication


class IsAdminAPIKey(BasePermission):
    message = {"detail": "Clé API admin invalide ou absente.", "code": "unauthorized"}

    def has_permission(self, request, view):
        return AdminAPIKeyAuthentication.verify(request)


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if AdminAPIKeyAuthentication.verify(request):
            return True
        return request.user and request.user.is_authenticated
