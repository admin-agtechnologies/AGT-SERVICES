from django.urls import path
from apps.payments.views import (
    HealthCheckView, PaymentInitiateView, PaymentDetailView, PaymentListView, PaymentCancelView,
    WebhookOrangeView, WebhookMTNView, WebhookStripeView, WebhookPayPalView,
    ProviderConfigListCreateView, PlatformProviderConfigView,
    AdminStatsView, AdminForceStatusView,
)

urlpatterns = [
    path("payments/health", HealthCheckView.as_view()),
    path("payments/initiate", PaymentInitiateView.as_view()),
    path("payments", PaymentListView.as_view()),
    path("payments/<uuid:transaction_id>", PaymentDetailView.as_view()),
    path("payments/<uuid:transaction_id>/cancel", PaymentCancelView.as_view()),

    # Webhooks (no auth)
    path("payments/webhooks/orange-money", WebhookOrangeView.as_view()),
    path("payments/webhooks/mtn-momo", WebhookMTNView.as_view()),
    path("payments/webhooks/stripe", WebhookStripeView.as_view()),
    path("payments/webhooks/paypal", WebhookPayPalView.as_view()),

    # Providers config
    path("payments/providers", ProviderConfigListCreateView.as_view()),
    path("payments/platforms/<str:platform_id>/providers", PlatformProviderConfigView.as_view()),

    # Admin
    path("payments/admin/stats", AdminStatsView.as_view()),
    path("payments/admin/<uuid:transaction_id>/force-status", AdminForceStatusView.as_view()),
]
