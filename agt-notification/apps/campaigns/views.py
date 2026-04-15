"""AGT Notification Service v1.0 - Views Campaigns."""
import logging
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.campaigns.models import Campaign, CampaignRecipient
from apps.notifications.pagination import StandardPagination

from apps.notifications.serializers import CampaignCreateSerializer

logger = logging.getLogger(__name__)


class CampaignListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Campaigns"], summary="Creer une campagne", request=CampaignCreateSerializer)
    def post(self, request):
        from apps.templates_mgr.models import Template
        from workers.tasks import process_campaign_task
        data = request.data
        name, template_name, channel = data.get("name"), data.get("template_name"), data.get("channel", "email")
        user_ids = data.get("user_ids", [])
        platform_id = str(getattr(request.user, "platform_id", "") or "")

        if not all([name, template_name, channel, user_ids]):
            return Response({"detail": "name, template_name, channel et user_ids requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            template = Template.resolve(template_name, platform_id=platform_id)
        except Template.DoesNotExist:
            return Response({"detail": "Template introuvable."}, status=status.HTTP_404_NOT_FOUND)

        campaign = Campaign.objects.create(
            name=name, platform_id=platform_id or "00000000-0000-0000-0000-000000000000",
            template=template, channel=channel, total_recipients=len(user_ids),
            throttle_per_second=data.get("throttle_per_second", 10),
            created_by=getattr(request.user, "auth_user_id", None),
        )
        CampaignRecipient.objects.bulk_create([
            CampaignRecipient(campaign=campaign, user_id=uid, variables=data.get("variables", {}))
            for uid in user_ids
        ])
        process_campaign_task.delay(str(campaign.id))
        return Response({"id": str(campaign.id), "name": name, "status": "draft", "total_recipients": len(user_ids)}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Campaigns"], summary="Lister les campagnes")
    def get(self, request):
        qs = Campaign.objects.all()
        if request.GET.get("status"):
            qs = qs.filter(status=request.GET["status"])
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(c.id), "name": c.name, "status": c.status, "sent_count": c.sent_count, "total_recipients": c.total_recipients} for c in page]
        return paginator.get_paginated_response(data)


class CampaignDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Campaigns"], summary="Detail campagne")
    def get(self, request, campaign_id):
        try:
            c = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"detail": "Campagne introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"id": str(c.id), "name": c.name, "status": c.status, "total_recipients": c.total_recipients,
                         "sent_count": c.sent_count, "failed_count": c.failed_count, "progress": c.progress_percent})


class CampaignProgressView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Campaigns"], summary="Progression campagne")
    def get(self, request, campaign_id):
        try:
            c = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"detail": "Campagne introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"progress": c.progress_percent, "sent": c.sent_count, "failed": c.failed_count, "total": c.total_recipients, "status": c.status})


class CampaignCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Campaigns"], summary="Annuler une campagne")
    def post(self, request, campaign_id):
        try:
            c = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"detail": "Campagne introuvable."}, status=status.HTTP_404_NOT_FOUND)

        # On ne peut pas annuler une campagne déjà terminée ou déjà annulée
        if c.status in ["completed", "cancelled"]:
            return Response(
                {"detail": f"Impossible d'annuler une campagne avec le statut '{c.status}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        c.cancel()
        return Response({"message": "Campagne annulee.", "status": "cancelled"})