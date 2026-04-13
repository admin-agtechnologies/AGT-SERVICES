"""AGT Notification Service v1.0 - Views Device Tokens."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.notifications.serializers import DeviceTokenCreateSerializer
from apps.devices.models import DeviceToken


class DeviceTokenListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Devices"], summary="Enregistrer un device token", request=DeviceTokenCreateSerializer)
    def post(self, request, user_id):
        token = request.data.get("token")
        device_type = request.data.get("device_type")
        platform_id = str(getattr(request.user, "platform_id", "") or "")
        if not token or not device_type:
            return Response({"detail": "token et device_type requis."}, status=status.HTTP_400_BAD_REQUEST)

        dt, created = DeviceToken.objects.update_or_create(
            user_id=user_id, token=token,
            defaults={"platform_id": platform_id, "device_type": device_type,
                       "device_name": request.data.get("device_name"), "is_active": True},
        )
        return Response({"id": str(dt.id), "device_type": dt.device_type, "created": created},
                         status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @extend_schema(tags=["Devices"], summary="Lister les devices d'un utilisateur")
    def get(self, request, user_id):
        tokens = DeviceToken.objects.filter(user_id=user_id, is_active=True)
        data = [{"id": str(t.id), "device_type": t.device_type, "device_name": t.device_name, "created_at": t.created_at.isoformat()} for t in tokens]
        return Response({"data": data})


class DeviceTokenDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Devices"], summary="Supprimer un device token")
    def delete(self, request, user_id, token_id):
        deleted, _ = DeviceToken.objects.filter(id=token_id, user_id=user_id).delete()
        if not deleted:
            return Response({"detail": "Token introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Device token supprime."})
