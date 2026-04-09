"""AGT Notification Service v1.0 - Views principales."""
import logging
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.notifications.models import (
    Notification, NotificationLog, UserPreference, ScheduledNotification,
    PlatformChannelConfig, ChannelChoice, CategoryChoice, NotificationStatus,
)
from apps.notifications.pagination import StandardPagination
from apps.notifications.services import UserResolverService, PreferenceService, IdempotencyService

logger = logging.getLogger(__name__)
VALID_CHANNELS = [c.value for c in ChannelChoice]
VALID_CATEGORIES = [c.value for c in CategoryChoice]


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Health"], summary="Health check")
    def get(self, request):
        db_ok = redis_ok = broker_ok = True
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
        try:
            from config.celery import app as celery_app
            broker_ok = celery_app.control.inspect(timeout=1).ping() is not None
        except Exception:
            broker_ok = False

        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({"status": "healthy" if db_ok and redis_ok else "degraded",
                         "database": "ok" if db_ok else "error", "redis": "ok" if redis_ok else "error",
                         "broker": "ok" if broker_ok else "degraded", "version": "1.0.0"}, status=code)


class SendNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Send"], summary="Envoi mono ou multi-canal")
    def post(self, request):
        from workers.tasks import send_notification_task
        from apps.templates_mgr.models import Template

        data = request.data
        user_id = data.get("user_id")
        channels = data.get("channels", [])
        template_name = data.get("template_name")
        locale = data.get("locale", "fr")
        variables = data.get("variables", {})
        priority = data.get("priority", "normal")
        category = data.get("category", "transactional")
        idempotency_key = data.get("idempotency_key")
        platform_id = str(getattr(request.user, "platform_id", "") or "")

        if not user_id or not channels or not template_name:
            return Response({"detail": "user_id, channels et template_name requis."}, status=status.HTTP_400_BAD_REQUEST)
        if category not in VALID_CATEGORIES:
            return Response({"detail": f"Categorie invalide. Valeurs: {VALID_CATEGORIES}"}, status=status.HTTP_400_BAD_REQUEST)

        if idempotency_key and platform_id:
            if IdempotencyService.check_and_register(platform_id, idempotency_key):
                return Response({"detail": "Cle d'idempotence deja utilisee."}, status=status.HTTP_409_CONFLICT)

        try:
            template = Template.resolve(template_name, platform_id=platform_id)
        except Template.DoesNotExist:
            return Response({"detail": f"Template '{template_name}' introuvable."}, status=status.HTTP_404_NOT_FOUND)

        try:
            rendered = template.render(variables, locale=locale)
        except Exception as e:
            return Response({"detail": f"Erreur rendu template: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        created = []
        for ch in channels:
            if ch not in VALID_CHANNELS:
                continue
            if not PreferenceService.is_allowed(user_id, platform_id, ch, category):
                continue

            notif = Notification.objects.create(
                user_id=user_id, platform_id=platform_id or "00000000-0000-0000-0000-000000000000",
                template=template, channel=ch, category=category, subject=rendered.get("subject"),
                body=rendered.get("body", ""), priority=priority,
                idempotency_key=idempotency_key if len(channels) == 1 else None,
                metadata={"variables": variables, "locale": locale},
            )
            send_notification_task.delay(str(notif.id))
            created.append({"id": str(notif.id), "channel": ch, "status": "pending"})

        return Response({"notifications": created, "message": "Notifications queued"}, status=status.HTTP_202_ACCEPTED)


class SendBulkNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Send"], summary="Envoi en masse (max 100)")
    def post(self, request):
        from workers.tasks import send_notification_task
        from apps.templates_mgr.models import Template

        data = request.data
        user_ids = data.get("user_ids", [])
        channels = data.get("channels", [])
        template_name = data.get("template_name")
        if not user_ids or not channels or not template_name:
            return Response({"detail": "user_ids, channels et template_name requis."}, status=status.HTTP_400_BAD_REQUEST)
        if len(user_ids) > 100:
            return Response({"detail": "Max 100 user_ids. Utilisez les campagnes pour plus."}, status=status.HTTP_400_BAD_REQUEST)

        platform_id = str(getattr(request.user, "platform_id", "") or "")
        try:
            template = Template.resolve(template_name, platform_id=platform_id)
        except Template.DoesNotExist:
            return Response({"detail": f"Template introuvable."}, status=status.HTTP_404_NOT_FOUND)

        variables = data.get("variables", {})
        locale = data.get("locale", "fr")
        category = data.get("category", "transactional")
        rendered = template.render(variables, locale=locale)

        total = 0
        for uid in user_ids:
            for ch in channels:
                notif = Notification.objects.create(
                    user_id=uid, platform_id=platform_id or "00000000-0000-0000-0000-000000000000",
                    template=template, channel=ch, category=category, subject=rendered.get("subject"),
                    body=rendered.get("body", ""), metadata={"variables": variables},
                )
                send_notification_task.delay(str(notif.id))
                total += 1

        return Response({"message": f"{total} notifications queued", "total": total}, status=status.HTTP_202_ACCEPTED)


class PreferenceView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Preferences"], summary="Lire les preferences")
    def get(self, request, user_id):
        try:
            pref = UserPreference.objects.get(user_id=user_id, platform_id=getattr(request.user, "platform_id", ""))
            return Response({
                "channels": {"email": pref.channel_email, "sms": pref.channel_sms, "push": pref.channel_push, "whatsapp": pref.channel_whatsapp, "in_app": pref.channel_in_app},
                "categories": {"transactional": pref.cat_transactional, "marketing": pref.cat_marketing, "security": True},
            })
        except UserPreference.DoesNotExist:
            return Response({"channels": {"email": True, "sms": True, "push": True, "whatsapp": True, "in_app": True},
                             "categories": {"transactional": True, "marketing": False, "security": True}})

    @extend_schema(tags=["Preferences"], summary="Modifier les preferences")
    def put(self, request, user_id):
        platform_id = str(getattr(request.user, "platform_id", "") or "")
        pref, _ = UserPreference.objects.get_or_create(user_id=user_id, platform_id=platform_id)
        channels = request.data.get("channels", {})
        categories = request.data.get("categories", {})
        for ch in ["email", "sms", "push", "whatsapp", "in_app"]:
            if ch in channels:
                setattr(pref, f"channel_{ch}", channels[ch])
        for cat in ["transactional", "marketing"]:
            if cat in categories:
                setattr(pref, f"cat_{cat}", categories[cat])
        pref.save()
        return Response({"message": "Preferences mises a jour."})


class InAppListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Lister notifications in-app")
    def get(self, request, user_id):
        qs = Notification.objects.filter(user_id=user_id, channel="in_app", deleted_at__isnull=True)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(n.id), "subject": n.subject, "body": n.body, "is_read": n.is_read,
                 "created_at": n.created_at.isoformat()} for n in page]
        return paginator.get_paginated_response(data)


class InAppUnreadCountView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Compteur non lues (badge)")
    def get(self, request, user_id):
        count = Notification.objects.filter(user_id=user_id, channel="in_app", read_at__isnull=True, deleted_at__isnull=True).count()
        return Response({"user_id": str(user_id), "unread_count": count})


class InAppMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Marquer comme lue")
    def put(self, request, user_id, notification_id):
        try:
            notif = Notification.objects.get(id=notification_id, user_id=user_id, channel="in_app")
        except Notification.DoesNotExist:
            return Response({"detail": "Notification introuvable."}, status=status.HTTP_404_NOT_FOUND)
        notif.mark_as_read()
        return Response({"message": "Notification lue."})


class InAppMarkAllReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Tout marquer comme lu")
    def put(self, request, user_id):
        updated = Notification.objects.filter(user_id=user_id, channel="in_app", read_at__isnull=True).update(
            read_at=timezone.now(), status=NotificationStatus.READ)
        return Response({"message": f"{updated} notifications marquees lues."})


class InAppDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["In-App"], summary="Supprimer notification in-app")
    def delete(self, request, user_id, notification_id):
        try:
            notif = Notification.objects.get(id=notification_id, user_id=user_id, channel="in_app")
        except Notification.DoesNotExist:
            return Response({"detail": "Notification introuvable."}, status=status.HTTP_404_NOT_FOUND)
        notif.soft_delete()
        return Response({"message": "Notification supprimee."})


class NotificationStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Stats"], summary="Statistiques globales")
    def get(self, request):
        by_status = dict(Notification.objects.values_list("status").annotate(c=Count("id")))
        by_channel = dict(Notification.objects.values_list("channel").annotate(c=Count("id")))
        return Response({"by_status": by_status, "by_channel": by_channel})


class NotificationLogsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Stats"], summary="Logs d'envoi")
    def get(self, request):
        qs = NotificationLog.objects.all()
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(l.id), "notification_id": str(l.notification_id), "channel": l.channel,
                 "provider": l.provider, "status": l.status, "attempt": l.attempt,
                 "created_at": l.created_at.isoformat()} for l in page]
        return paginator.get_paginated_response(data)


class ChannelConfigView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Config"], summary="Config canaux plateforme")
    def get(self, request, platform_id):
        config = PlatformChannelConfig.get_for_platform(str(platform_id))
        return Response({"platform_id": str(platform_id), "priority_order": config.priority_order, "fallback_enabled": config.fallback_enabled})

    @extend_schema(tags=["Config"], summary="Modifier config canaux")
    def put(self, request, platform_id):
        config, _ = PlatformChannelConfig.objects.get_or_create(platform_id=platform_id, defaults={"priority_order": PlatformChannelConfig.DEFAULT_ORDER})
        if "priority_order" in request.data:
            config.priority_order = request.data["priority_order"]
        if "fallback_enabled" in request.data:
            config.fallback_enabled = request.data["fallback_enabled"]
        config.save()
        return Response({"message": "Config mise a jour."})
