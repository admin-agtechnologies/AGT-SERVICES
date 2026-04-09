from django.urls import path
from apps.users.views import (
    HealthCheckView, UserListCreateView, UserDetailView, UserByAuthView,
    UserLeavePlatformView, UserPermanentDeleteView, UserPhotoView,
    UserSearchView, UserStatsView, StatusSyncView, CredentialsSyncView,
    AddressListCreateView, AddressDetailView, AddressSetDefaultView,
    UserMetadataView, UserMetadataKeyDeleteView,
)

urlpatterns = [
    path("health", HealthCheckView.as_view(), name="health"),

    # Profil
    path("users", UserListCreateView.as_view(), name="users-list-create"),
    path("users/search", UserSearchView.as_view(), name="users-search"),
    path("users/stats", UserStatsView.as_view(), name="users-stats"),
    path("users/status-sync", StatusSyncView.as_view(), name="users-status-sync"),
    path("users/sync", CredentialsSyncView.as_view(), name="users-sync"),
    path("users/by-auth/<uuid:auth_user_id>", UserByAuthView.as_view(), name="users-by-auth"),
    path("users/<uuid:user_id>", UserDetailView.as_view(), name="users-detail"),
    path("users/<uuid:user_id>/permanent", UserPermanentDeleteView.as_view(), name="users-permanent-delete"),
    path("users/<uuid:user_id>/photo", UserPhotoView.as_view(), name="users-photo"),
    path("users/<uuid:user_id>/platforms/<uuid:platform_id>", UserLeavePlatformView.as_view(), name="users-leave-platform"),

    # Adresses
    path("users/<uuid:user_id>/addresses", AddressListCreateView.as_view(), name="users-addresses"),
    path("users/<uuid:user_id>/addresses/<uuid:address_id>", AddressDetailView.as_view(), name="users-address-detail"),
    path("users/<uuid:user_id>/addresses/<uuid:address_id>/default", AddressSetDefaultView.as_view(), name="users-address-default"),

    # Metadata
    path("users/<uuid:user_id>/metadata/<str:platform_id>", UserMetadataView.as_view(), name="users-metadata"),
    path("users/<uuid:user_id>/metadata/<str:platform_id>/<str:key>", UserMetadataKeyDeleteView.as_view(), name="users-metadata-key"),
]
