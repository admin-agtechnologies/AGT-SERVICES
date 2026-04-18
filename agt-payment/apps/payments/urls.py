from django.urls import path
from apps.payments.views import (
    HealthCheckView,
    PaymentInitiateView, PaymentDetailView, PaymentListView, PaymentCancelView,
    WebhookOrangeView, WebhookMTNView, WebhookStripeView, WebhookPayPalView,
    ProviderConfigListCreateView, ProviderConfigUpdateView, PlatformProviderConfigView,
    AdminStatsView, AdminForceStatusView, AdminReconciliationView,
    RGPDPurgeView,
)

urlpatterns = [
    # Health
    path("payments/health", HealthCheckView.as_view()),

    # Paiements — statiques AVANT paramètres
    path("payments/initiate", PaymentInitiateView.as_view()),
    path("payments", PaymentListView.as_view()),
    path("payments/<uuid:transaction_id>/cancel", PaymentCancelView.as_view()),
    path("payments/<uuid:transaction_id>", PaymentDetailView.as_view()),

    # Webhooks (sans auth JWT)
    path("payments/webhooks/orange-money", WebhookOrangeView.as_view()),
    path("payments/webhooks/mtn-momo", WebhookMTNView.as_view()),
    path("payments/webhooks/stripe", WebhookStripeView.as_view()),
    path("payments/webhooks/paypal", WebhookPayPalView.as_view()),

    # Providers
    path("payments/providers", ProviderConfigListCreateView.as_view()),
    path("payments/providers/<str:provider>", ProviderConfigUpdateView.as_view()),
    path("payments/platforms/<str:platform_id>/providers", PlatformProviderConfigView.as_view()),

    # Admin — statiques AVANT paramètres
    path("payments/admin/stats", AdminStatsView.as_view()),
    path("payments/admin/reconciliation", AdminReconciliationView.as_view()),
    path("payments/admin/<uuid:transaction_id>/force-status", AdminForceStatusView.as_view()),

    # RGPD
    path("payments/by-user/<uuid:user_id>", RGPDPurgeView.as_view()),
]