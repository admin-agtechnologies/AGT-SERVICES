"""AGT Payment Service v1.0 - Views."""
import logging
from django.db.models import Count, Sum
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from apps.payments.models import Transaction, TransactionStatus, TransactionStatusHistory, ProviderConfig, PlatformPaymentConfig, WebhookLog
from apps.payments.service import PaymentService

logger = logging.getLogger(__name__)


class Paginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"

    def get_paginated_response(self, data):
        return Response({"data": data, "page": self.page.number, "total": self.page.paginator.count})


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Health"], summary="Health check")
    def get(self, request):
        db_ok = redis_ok = True
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
        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({"status": "healthy" if db_ok and redis_ok else "degraded",
                         "database": "ok" if db_ok else "error", "redis": "ok" if redis_ok else "error",
                         "version": "1.0.0"}, status=code)


class PaymentInitiateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"], summary="Initier un paiement")
    def post(self, request):
        d = request.data
        required = ["platform_id", "provider", "amount", "currency", "source", "idempotency_key"]
        if not all(d.get(f) for f in required):
            return Response({"detail": f"Champs requis: {', '.join(required)}"}, status=status.HTTP_400_BAD_REQUEST)

        tx, err = PaymentService.initiate(
            platform_id=d["platform_id"], user_id=d.get("user_id"),
            provider=d["provider"], amount=d["amount"], currency=d["currency"],
            source=d["source"], source_reference_id=d.get("source_reference_id"),
            idempotency_key=d["idempotency_key"], phone_number=d.get("phone_number"),
            metadata=d.get("metadata"),
        )

        resp_data = {
            "transaction_id": str(tx.id), "status": tx.status, "provider": tx.provider,
            "amount": float(tx.amount), "currency": tx.currency,
        }
        if tx.payment_url:
            resp_data["payment_url"] = tx.payment_url

        if err == "idempotent_hit":
            resp_data["message"] = "Idempotent request, returning existing transaction"
            return Response(resp_data, status=status.HTTP_200_OK)
        elif err:
            resp_data["message"] = err
            return Response(resp_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        resp_data["message"] = "Payment initiated"
        return Response(resp_data, status=status.HTTP_201_CREATED)


class PaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"], summary="Detail transaction avec historique statuts")
    def get(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction introuvable."}, status=status.HTTP_404_NOT_FOUND)

        history = TransactionStatusHistory.objects.filter(transaction=tx)
        return Response({
            "id": str(tx.id), "platform_id": str(tx.platform_id),
            "user_id": str(tx.user_id) if tx.user_id else None,
            "provider": tx.provider, "amount": float(tx.amount), "currency": tx.currency,
            "status": tx.status, "source": tx.source,
            "source_reference_id": str(tx.source_reference_id) if tx.source_reference_id else None,
            "provider_tx_id": tx.provider_tx_id, "payment_url": tx.payment_url,
            "failure_reason": tx.failure_reason,
            "confirmed_at": tx.confirmed_at.isoformat() if tx.confirmed_at else None,
            "created_at": tx.created_at.isoformat(),
            "status_history": [{"from": h.from_status, "to": h.to_status, "trigger": h.trigger, "at": h.created_at.isoformat()} for h in history],
        })


class PaymentListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"], summary="Lister transactions")
    def get(self, request):
        qs = Transaction.objects.all()
        for f in ["platform_id", "user_id", "status", "provider", "source"]:
            v = request.GET.get(f)
            if v:
                qs = qs.filter(**{f: v})
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(t.id), "provider": t.provider, "amount": float(t.amount),
                 "currency": t.currency, "status": t.status, "source": t.source,
                 "created_at": t.created_at.isoformat()} for t in page]
        return paginator.get_paginated_response(data)


class PaymentCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Payments"], summary="Annuler un paiement pending")
    def post(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction introuvable."}, status=status.HTTP_404_NOT_FOUND)
        if tx.status != TransactionStatus.PENDING:
            return Response({"detail": "Seuls les paiements pending peuvent etre annules."}, status=status.HTTP_400_BAD_REQUEST)
        tx.transition_to(TransactionStatus.CANCELLED, trigger="api_cancel")
        return Response({"transaction_id": str(tx.id), "status": "cancelled", "message": "Payment cancelled"})


# --- Webhooks ---

class WebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def _process(self, request, provider):
        try:
            payload = request.data if isinstance(request.data, dict) else {}
            event_id = payload.get("event_id") or payload.get("id") or request.headers.get("X-Event-Id")
            PaymentService.process_webhook(provider, event_id, payload, dict(request.headers))
        except Exception as e:
            logger.error(f"Webhook {provider} error: {e}")
        return Response({"received": True}, status=status.HTTP_200_OK)


class WebhookOrangeView(WebhookView):
    @extend_schema(tags=["Webhooks"], summary="Callback Orange Money")
    def post(self, request):
        return self._process(request, "orange_money")


class WebhookMTNView(WebhookView):
    @extend_schema(tags=["Webhooks"], summary="Callback MTN MoMo")
    def post(self, request):
        return self._process(request, "mtn_momo")


class WebhookStripeView(WebhookView):
    @extend_schema(tags=["Webhooks"], summary="Callback Stripe")
    def post(self, request):
        return self._process(request, "stripe")


class WebhookPayPalView(WebhookView):
    @extend_schema(tags=["Webhooks"], summary="Callback PayPal")
    def post(self, request):
        return self._process(request, "paypal")


# --- Provider Config ---

class ProviderConfigListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Providers"], summary="Creer un provider")
    def post(self, request):
        d = request.data
        if ProviderConfig.objects.filter(provider=d.get("provider")).exists():
            return Response({"detail": "Provider existe deja."}, status=status.HTTP_409_CONFLICT)
        pc = ProviderConfig.objects.create(
            provider=d["provider"], display_name=d.get("display_name", d["provider"]),
            api_base_url=d.get("api_base_url"), supported_currencies=d.get("supported_currencies", []),
        )
        return Response({"id": str(pc.id), "provider": pc.provider, "message": "Provider created"}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Providers"], summary="Lister les providers")
    def get(self, request):
        providers = ProviderConfig.objects.filter(is_active=True)
        data = [{"provider": p.provider, "display_name": p.display_name, "supported_currencies": p.supported_currencies} for p in providers]
        return Response({"data": data})


class PlatformProviderConfigView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Providers"], summary="Config providers plateforme")
    def get(self, request, platform_id):
        config = PlatformPaymentConfig.get_for_platform(str(platform_id))
        return Response({"platform_id": str(platform_id), "providers_priority": config.providers_priority, "default_currency": config.default_currency})

    @extend_schema(tags=["Providers"], summary="Modifier config providers plateforme")
    def put(self, request, platform_id):
        config, _ = PlatformPaymentConfig.objects.get_or_create(platform_id=platform_id, defaults={"providers_priority": ["orange_money"]})
        if "providers_priority" in request.data:
            config.providers_priority = request.data["providers_priority"]
        if "default_currency" in request.data:
            config.default_currency = request.data["default_currency"]
        config.save()
        return Response({"message": "Config updated"})


# --- Admin ---

class AdminStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Admin"], summary="Statistiques paiements")
    def get(self, request):
        total = Transaction.objects.count()
        total_amount = Transaction.objects.filter(status="succeeded").aggregate(s=Sum("amount"))["s"] or 0
        succeeded = Transaction.objects.filter(status="succeeded").count()
        success_rate = round((succeeded / total * 100), 1) if total > 0 else 0
        by_provider = list(Transaction.objects.values("provider").annotate(count=Count("id")))
        return Response({
            "total_transactions": total, "total_amount": float(total_amount),
            "success_rate": success_rate, "by_provider": by_provider,
        })


class AdminForceStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Admin"], summary="Forcer statut (verification manuelle)")
    def post(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response({"detail": "Transaction introuvable."}, status=status.HTTP_404_NOT_FOUND)
        new_status = request.data.get("status")
        if new_status not in ["succeeded", "failed"]:
            return Response({"detail": "status doit etre 'succeeded' ou 'failed'."}, status=status.HTTP_400_BAD_REQUEST)
        if tx.is_terminal():
            return Response({"detail": "Transaction deja terminale."}, status=status.HTTP_409_CONFLICT)
        tx.transition_to(new_status, trigger="admin_manual", metadata={"admin_note": request.data.get("note", "")})
        return Response({"transaction_id": str(tx.id), "status": tx.status, "message": "Status forced"})
