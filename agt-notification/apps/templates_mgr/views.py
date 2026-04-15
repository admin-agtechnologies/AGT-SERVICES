"""AGT Notification Service v1.0 - Views Templates CRUD."""
import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.templates_mgr.models import Template, TemplateVersion
from apps.notifications.pagination import StandardPagination

from apps.notifications.serializers import (
    TemplateCreateSerializer, TemplateUpdateSerializer, TemplatePreviewSerializer,
)

logger = logging.getLogger(__name__)


class TemplateListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Templates"], summary="Creer un template", request=TemplateCreateSerializer)
    def post(self, request):
        data = request.data
        name, channel, body = data.get("name"), data.get("channel"), data.get("body", "")
        platform_id = data.get("platform_id")
        if not all([name, channel, body]):
            return Response({"detail": "name, channel et body requis."}, status=status.HTTP_400_BAD_REQUEST)

        if Template.objects.filter(name=name, platform_id=platform_id).exists():
            return Response({"detail": f"Template '{name}' existe deja."}, status=status.HTTP_409_CONFLICT)

        tpl = Template.objects.create(name=name, channel=channel, platform_id=platform_id,
                                       category=data.get("category", "transactional"),
                                       created_by=getattr(request.user, "auth_user_id", None))
        TemplateVersion.objects.create(template=tpl, version=1, locale=data.get("locale", "fr"),
                                        subject=data.get("subject"), body=body, is_current=True)
        return Response({"id": str(tpl.id), "name": tpl.name, "channel": tpl.channel}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Templates"], summary="Lister les templates")
    def get(self, request):
        qs = Template.objects.filter(is_active=True)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(t.id), "name": t.name, "channel": t.channel, "platform_id": str(t.platform_id) if t.platform_id else None, "category": t.category} for t in page]
        return paginator.get_paginated_response(data)


class TemplateDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Templates"], summary="Detail template")
    def get(self, request, template_id):
        try:
            tpl = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)
        version = tpl.get_current_version()
        return Response({"id": str(tpl.id), "name": tpl.name, "channel": tpl.channel,
                         "subject": version.subject if version else None, "body": version.body if version else ""})

    @extend_schema(tags=["Templates"], summary="Modifier template (nouvelle version)", request=TemplateUpdateSerializer)
    def put(self, request, template_id):
        try:
            tpl = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        last_version = tpl.versions.order_by("-version").first()
        new_version_num = (last_version.version + 1) if last_version else 1
        tpl.versions.filter(is_current=True).update(is_current=False)
        TemplateVersion.objects.create(template=tpl, version=new_version_num, locale=data.get("locale", "fr"),
                                        subject=data.get("subject"), body=data.get("body", ""), is_current=True)
        tpl.save()
        return Response({"message": "Template mis a jour.", "version": new_version_num})

    @extend_schema(tags=["Templates"], summary="Desactiver template")
    def delete(self, request, template_id):
        try:
            tpl = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)
        tpl.is_active = False
        tpl.save(update_fields=["is_active"])
        return Response({"message": "Template desactive."})


class TemplatePreviewView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Templates"], summary="Preview avec variables", request=TemplatePreviewSerializer)
    def post(self, request, template_id):
        try:
            tpl = Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)
        variables = request.data.get("variables", {})
        locale = request.data.get("locale", "fr")
        try:
            rendered = tpl.render(variables, locale=locale)
            return Response(rendered)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TemplateVersionsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Templates"], summary="Historique versions")
    def get(self, request, template_id):
        versions = TemplateVersion.objects.filter(template_id=template_id)
        data = [{"version": v.version, "locale": v.locale, "is_current": v.is_current, "created_at": v.created_at.isoformat()} for v in versions]
        return Response({"data": data})
