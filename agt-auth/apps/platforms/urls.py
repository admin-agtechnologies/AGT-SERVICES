from django.urls import path
from apps.platforms.views import PlatformListCreateView, PlatformDetailView

urlpatterns = [
    path("auth/platforms", PlatformListCreateView.as_view(), name="platforms-list-create"),
    path("auth/platforms/<uuid:platform_id>", PlatformDetailView.as_view(), name="platforms-detail"),
]
