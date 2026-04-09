from django.urls import path
from apps.devices.views import DeviceTokenListCreateView, DeviceTokenDeleteView

urlpatterns = [
    path("users/<str:user_id>/device-tokens", DeviceTokenListCreateView.as_view(), name="device-tokens"),
    path("users/<str:user_id>/device-tokens/<uuid:token_id>", DeviceTokenDeleteView.as_view(), name="device-token-delete"),
]
