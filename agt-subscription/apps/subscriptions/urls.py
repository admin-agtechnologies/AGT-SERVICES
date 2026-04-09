from django.urls import path
from apps.subscriptions.views import (
    HealthCheckView, PlanListCreateView, PlanDetailView, PlanArchiveView,
    SubscriptionCreateView, SubscriptionListView, SubscriptionDetailView,
    SubscriptionCancelView, SubscriptionChangePlanView, SubscriptionActivateView,
    SubscriptionReactivateView, QuotaCheckView, QuotaIncrementView,
    QuotaReserveView, QuotaConfirmView, QuotaReleaseView, QuotaUsageView,
    OrganizationListCreateView, OrganizationMemberView,
    PlatformConfigView, AdminStatsView,
)

urlpatterns = [
    path("subscriptions/health", HealthCheckView.as_view()),

    # Plans
    path("subscriptions/plans", PlanListCreateView.as_view()),
    path("subscriptions/plans/<uuid:plan_id>", PlanDetailView.as_view()),
    path("subscriptions/plans/<uuid:plan_id>/archive", PlanArchiveView.as_view()),

    # Subscriptions
    path("subscriptions", SubscriptionCreateView.as_view()),
    path("subscriptions/list", SubscriptionListView.as_view()),
    path("subscriptions/<uuid:sub_id>", SubscriptionDetailView.as_view()),
    path("subscriptions/<uuid:sub_id>/cancel", SubscriptionCancelView.as_view()),
    path("subscriptions/<uuid:sub_id>/change-plan", SubscriptionChangePlanView.as_view()),
    path("subscriptions/<uuid:sub_id>/activate", SubscriptionActivateView.as_view()),
    path("subscriptions/<uuid:sub_id>/reactivate", SubscriptionReactivateView.as_view()),
    path("subscriptions/<uuid:sub_id>/usage", QuotaUsageView.as_view()),

    # Quotas S2S
    path("subscriptions/quotas/check", QuotaCheckView.as_view()),
    path("subscriptions/quotas/increment", QuotaIncrementView.as_view()),
    path("subscriptions/quotas/reserve", QuotaReserveView.as_view()),
    path("subscriptions/quotas/confirm", QuotaConfirmView.as_view()),
    path("subscriptions/quotas/release", QuotaReleaseView.as_view()),

    # Organizations
    path("organizations", OrganizationListCreateView.as_view()),
    path("organizations/<uuid:org_id>/members", OrganizationMemberView.as_view()),
    path("organizations/<uuid:org_id>/members/<uuid:user_id>", OrganizationMemberView.as_view()),

    # Config
    path("subscriptions/config/<str:platform_id>", PlatformConfigView.as_view()),

    # Admin
    path("subscriptions/admin/stats", AdminStatsView.as_view()),
]
