from django.urls import path
from apps.campaigns.views import CampaignListCreateView, CampaignDetailView, CampaignProgressView, CampaignCancelView

urlpatterns = [
    path("campaigns", CampaignListCreateView.as_view(), name="campaigns-list"),
    path("campaigns/<uuid:campaign_id>", CampaignDetailView.as_view(), name="campaigns-detail"),
    path("campaigns/<uuid:campaign_id>/progress", CampaignProgressView.as_view(), name="campaigns-progress"),
    path("campaigns/<uuid:campaign_id>/cancel", CampaignCancelView.as_view(), name="campaigns-cancel"),
]
