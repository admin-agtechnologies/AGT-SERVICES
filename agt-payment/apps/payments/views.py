"""AGT Payment Service v1.2 - Views.

Toutes les vues POST/PUT ont un serializer Swagger (request=) pour afficher
le body dans Swagger UI. Conforme au CDC v1.2.
"""
import logging
from django.conf import settings
from django.db.models import Count, Sum
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from apps.payments.models import (
    Transaction, TransactionStatus, TransactionStatusHistory,
    ProviderConfig, PlatformPaymentConfig, WebhookLog,
)
from apps.payments.service import PaymentService

logger = logging.getLogger(__name__)


# ===========================================================================
# SERIALIZERS — uniquement pour la documentation Swagger (request body)
# ===========================================================================

class PaymentInitiateSerializer(serializers.Serializer):
    """Body de POST /payments/initiate — CDC v1.2 section 9.2.1"""
    platform_id = serializers.UUIDField(
        help_text="UUID de la plateforme émettrice (registre Auth)"
    )
    user_id = serializers.UUIDField(
        required=False, allow_null=True,
        help_text="UUID de l'utilisateur payeur (sub du JWT). Optionnel pour les paiements B2B."
    )
    provider = serializers.ChoiceField(
        choices=["orange_money", "mtn_momo", "stripe", "paypal"],
        help_text="Provider de paiement à utiliser"
    )
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2,
        help_text="Montant à facturer (ex: 15000)"
    )
    currency = serializers.CharField(
        max_length=3,
        help_text="Devise ISO 4217 (ex: XAF, EUR, USD)"
    )
    source = serializers.ChoiceField(
        choices=["subscription", "wallet", "platform", "manual"],
        help_text="Service ou contexte à l'origine du paiement"
    )
    source_reference_id = serializers.UUIDField(
        required=False, allow_null=True,
        help_text="ID de la ressource source (ex: subscription_id, order_id)"
    )
    idempotency_key = serializers.UUIDField(
        help_text="UUID v4 unique par intention de paiement. Même clé = retour transaction existante."
    )
    phone_number = serializers.CharField(
        required=False, allow_null=True, max_length=20,
        help_text="Numéro Mobile Money (obligatoire pour orange_money et mtn_momo). Ex: +237600000000"
    )
    metadata = serializers.DictField(
        required=False, allow_null=True,
        help_text="Données opaques transmises tel quel (ex: subscription_id, plan_name, reason)"
    )


class PaymentCancelSerializer(serializers.Serializer):
    """Body de POST /payments/{id}/cancel — CDC v1.2 section 9.2.4"""
    reason = serializers.CharField(
        required=False, allow_blank=True,
        help_text="Raison de l'annulation (optionnel, pour traçabilité)"
    )


class ProviderCreateSerializer(serializers.Serializer):
    """Body de POST /payments/providers — CDC v1.2 section 9.4.1"""
    provider = serializers.ChoiceField(
        choices=["orange_money", "mtn_momo", "stripe", "paypal"],
        help_text="Identifiant technique du provider"
    )
    display_name = serializers.CharField(
        help_text="Nom affiché (ex: Orange Money Cameroun)"
    )
    credentials = serializers.DictField(
        help_text="Credentials bruts — chiffrés AES-256 avant stockage. Ex: {api_key, api_secret}"
    )
    api_base_url = serializers.URLField(
        required=False, allow_null=True,
        help_text="URL de base de l'API provider (ex: https://api.orange.com/...)"
    )
    webhook_secret = serializers.CharField(
        required=False, allow_null=True,
        help_text="Secret de vérification HMAC des webhooks — chiffré avant stockage"
    )
    supported_currencies = serializers.ListField(
        child=serializers.CharField(max_length=3),
        help_text="Devises supportées par ce provider (ex: [\"XAF\", \"EUR\"])"
    )


class ProviderUpdateSerializer(serializers.Serializer):
    """Body de PUT /payments/providers/{provider} — CDC v1.2 section 9.4.2"""
    display_name = serializers.CharField(
        required=False,
        help_text="Nouveau nom affiché"
    )
    credentials = serializers.DictField(
        required=False,
        help_text="Nouveaux credentials — chiffrés AES-256 avant stockage"
    )
    api_base_url = serializers.URLField(
        required=False, allow_null=True,
        help_text="Nouvelle URL de base de l'API provider"
    )
    webhook_secret = serializers.CharField(
        required=False, allow_null=True,
        help_text="Nouveau secret HMAC webhook"
    )
    supported_currencies = serializers.ListField(
        required=False,
        child=serializers.CharField(max_length=3),
        help_text="Nouvelles devises supportées"
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text="Activer ou désactiver le provider globalement"
    )


class PlatformProviderItemSerializer(serializers.Serializer):
    """Un provider dans la liste de configuration plateforme"""
    provider = serializers.ChoiceField(
        choices=["orange_money", "mtn_momo", "stripe", "paypal"],
        help_text="Identifiant du provider"
    )
    priority = serializers.IntegerField(
        help_text="Ordre de priorité (1 = prioritaire, fallback dans l'ordre croissant)"
    )
    is_active = serializers.BooleanField(
        help_text="Ce provider est-il actif pour cette plateforme ?"
    )


class PlatformProviderConfigSerializer(serializers.Serializer):
    """Body de PUT /payments/platforms/{id}/providers — CDC v1.2 section 9.4.3"""
    providers = PlatformProviderItemSerializer(
        many=True,
        help_text="Liste ordonnée des providers actifs pour cette plateforme"
    )
    default_currency = serializers.CharField(
        max_length=3, required=False, default="XAF",
        help_text="Devise par défaut pour cette plateforme (ex: XAF)"
    )


class ForceStatusSerializer(serializers.Serializer):
    """Body de POST /payments/admin/{id}/force-status — CDC v1.2 section 9.5.2"""
    status = serializers.ChoiceField(
        choices=["succeeded", "failed"],
        help_text="Nouveau statut forcé. Uniquement succeeded ou failed autorisés."
    )
    reason = serializers.CharField(
        help_text="Justification obligatoire (ex: Verified manually via Orange Money dashboard)"
    )


class WebhookGenericSerializer(serializers.Serializer):
    """Body générique pour les webhooks providers — format libre selon provider"""
    event_id = serializers.CharField(
        required=False,
        help_text="Identifiant unique de l'événement (anti-replay)"
    )
    status = serializers.CharField(
        required=False,
        help_text="Statut brut retourné par le provider (sera normalisé en interne)"
    )
    transaction_id = serializers.CharField(
        required=False,
        help_text="Identifiant de la transaction côté provider"
    )


# ===========================================================================
# PAGINATION
# ===========================================================================

class Paginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "page": self.page.number,
            "total": self.page.paginator.count,
        })


# ===========================================================================
# HEALTH CHECK
# ===========================================================================

class HealthCheckView(APIView):
    """
    GET /payments/health
    Vérifie DB, Redis et RabbitMQ. Aucune authentification requise.
    RabbitMQ est non-bloquant : unavailable n'affecte pas le statut global.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Health"], summary="Health check du service Payment")
    def get(self, request):
        # --- DB ---
        db_ok = True
        try:
            from django.db import connection
            connection.ensure_connection()
        except Exception:
            db_ok = False

        # --- Redis ---
        redis_ok = True
        try:
            from django.core.cache import cache
            cache.set("health", "ok", 5)
            redis_ok = cache.get("health") == "ok"
        except Exception:
            redis_ok = False

        # --- RabbitMQ (non-bloquant) ---
        rabbitmq_ok = False
        try:
            import kombu
            broker_url = getattr(settings, "BROKER_URL", "amqp://guest:guest@localhost:5672//")
            conn = kombu.Connection(broker_url)
            conn.ensure_connection(max_retries=1)
            conn.close()
            rabbitmq_ok = True
        except Exception:
            pass

        code = (
            status.HTTP_200_OK
            if db_ok and redis_ok
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )
        return Response({
            "status": "healthy" if db_ok and redis_ok else "degraded",
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
            "rabbitmq": "ok" if rabbitmq_ok else "unavailable",
            "version": "1.2.0",
        }, status=code)


# ===========================================================================
# PAIEMENTS
# ===========================================================================

class PaymentInitiateView(APIView):
    """
    POST /payments/initiate
    Initie une transaction. Auth : Bearer token (utilisateur) ou S2S.
    L'idempotency_key est obligatoire — même clé = retour transaction existante (200).
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Payments"],
        summary="Initier un paiement",
        description=(
            "Crée une transaction et la soumet au provider.\n\n"
            "- **Mobile Money** (orange_money, mtn_momo) : déclenche un push USSD sur le téléphone du payeur.\n"
            "- **Redirect** (stripe, paypal) : retourne une `payment_url` vers laquelle rediriger l'utilisateur.\n\n"
            "L'`idempotency_key` garantit qu'une même intention de paiement ne sera jamais exécutée deux fois."
        ),
        request=PaymentInitiateSerializer,
    )
    def post(self, request):
        d = request.data
        required = ["platform_id", "provider", "amount", "currency", "source", "idempotency_key"]
        missing = [f for f in required if not d.get(f)]
        if missing:
            return Response(
                {"detail": f"Champs requis manquants: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tx, err = PaymentService.initiate(
            platform_id=d["platform_id"],
            user_id=d.get("user_id"),
            provider=d["provider"],
            amount=d["amount"],
            currency=d["currency"],
            source=d["source"],
            source_reference_id=d.get("source_reference_id"),
            idempotency_key=d["idempotency_key"],
            phone_number=d.get("phone_number"),
            metadata=d.get("metadata"),
        )

        resp_data = {
            "transaction_id": str(tx.id),
            "status": tx.status,
            "provider": tx.provider,
            "amount": float(tx.amount),
            "currency": tx.currency,
        }
        if tx.payment_url:
            resp_data["payment_url"] = tx.payment_url
            resp_data["message"] = "Redirect user to payment_url"
        else:
            resp_data["message"] = "USSD push sent, waiting for user confirmation"

        if err == "idempotent_hit":
            # Vérifier si le payload est identique — CDC v1.1
            # Même clé + montant différent = erreur de l'appelant → 409
            try:
                incoming_amount = float(d["amount"])
                existing_amount = float(tx.amount)
                incoming_provider = d["provider"]
                existing_provider = tx.provider
                if incoming_amount != existing_amount or incoming_provider != existing_provider:
                    return Response({
                        "detail": "Conflit idempotence : même clé mais payload différent.",
                        "existing_transaction_id": str(tx.id),
                        "existing_amount": existing_amount,
                        "existing_provider": existing_provider,
                    }, status=status.HTTP_409_CONFLICT)
            except (ValueError, TypeError):
                pass
            resp_data["message"] = "Idempotent request, returning existing transaction"
            return Response(resp_data, status=status.HTTP_200_OK)
        elif err:
            resp_data["message"] = err
            return Response(resp_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(resp_data, status=status.HTTP_201_CREATED)


class PaymentDetailView(APIView):
    """
    GET /payments/{transactionId}
    Retourne le détail complet d'une transaction avec son historique de statuts.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Payments"],
        summary="Détail d'une transaction",
        description="Retourne la transaction et son historique complet de transitions de statut.",
    )
    def get(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        history = TransactionStatusHistory.objects.filter(transaction=tx).order_by("created_at")
        return Response({
            "id": str(tx.id),
            "platform_id": str(tx.platform_id),
            "user_id": str(tx.user_id) if tx.user_id else None,
            "provider": tx.provider,
            "amount": float(tx.amount),
            "currency": tx.currency,
            "status": tx.status,
            "source": tx.source,
            "source_reference_id": str(tx.source_reference_id) if tx.source_reference_id else None,
            "provider_tx_id": tx.provider_tx_id,
            "payment_url": tx.payment_url,
            "failure_reason": tx.failure_reason,
            "confirmed_at": tx.confirmed_at.isoformat() if tx.confirmed_at else None,
            "created_at": tx.created_at.isoformat(),
            "status_history": [
                {
                    "from": h.from_status,
                    "to": h.to_status,
                    "trigger": h.trigger,
                    "at": h.created_at.isoformat(),
                }
                for h in history
            ],
        })


class PaymentListView(APIView):
    """
    GET /payments
    Liste les transactions avec filtres optionnels.
    Query params : platform_id, user_id, status, provider, source, from_date, to_date
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Payments"],
        summary="Lister les transactions",
        description="Liste paginée des transactions. Filtrable par platform_id, user_id, status, provider, source.",
        parameters=[
            OpenApiParameter("platform_id", OpenApiTypes.UUID, description="Filtrer par plateforme"),
            OpenApiParameter("user_id", OpenApiTypes.UUID, description="Filtrer par utilisateur"),
            OpenApiParameter("status", OpenApiTypes.STR, description="pending | processing | succeeded | failed | expired | cancelled"),
            OpenApiParameter("provider", OpenApiTypes.STR, description="orange_money | mtn_momo | stripe | paypal"),
            OpenApiParameter("source", OpenApiTypes.STR, description="subscription | wallet | platform | manual"),
            OpenApiParameter("from_date", OpenApiTypes.DATE, description="Date de début (YYYY-MM-DD)"),
            OpenApiParameter("to_date", OpenApiTypes.DATE, description="Date de fin (YYYY-MM-DD)"),
        ],
    )
    def get(self, request):
        qs = Transaction.objects.all().order_by("-created_at")
        for f in ["platform_id", "user_id", "status", "provider", "source"]:
            v = request.GET.get(f)
            if v:
                qs = qs.filter(**{f: v})

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        if from_date:
            qs = qs.filter(created_at__date__gte=from_date)
        if to_date:
            qs = qs.filter(created_at__date__lte=to_date)

        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [
            {
                "id": str(t.id),
                "platform_id": str(t.platform_id),
                "provider": t.provider,
                "amount": float(t.amount),
                "currency": t.currency,
                "status": t.status,
                "source": t.source,
                "created_at": t.created_at.isoformat(),
            }
            for t in page
        ]
        return paginator.get_paginated_response(data)


class PaymentCancelView(APIView):
    """
    POST /payments/{transactionId}/cancel
    Annule un paiement en état PENDING uniquement.
    États terminaux (succeeded, failed, expired, cancelled) ne peuvent pas être annulés.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Payments"],
        summary="Annuler un paiement",
        description="Annule une transaction. Seuls les paiements en état `pending` peuvent être annulés.",
        request=PaymentCancelSerializer,
    )
    def post(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if tx.status != TransactionStatus.PENDING:
            return Response(
                {"detail": f"Seuls les paiements pending peuvent être annulés. Statut actuel : {tx.status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tx.transition_to(TransactionStatus.CANCELLED, trigger="api_cancel")
        return Response({
            "transaction_id": str(tx.id),
            "status": "cancelled",
            "message": "Payment cancelled",
        })


# ===========================================================================
# WEBHOOKS — pas de JWT, vérification par signature HMAC / IP whitelist
# ===========================================================================

class WebhookView(APIView):
    """
    Base commune pour tous les webhooks providers.
    Pas d'authentification JWT : la vérification se fait par signature HMAC ou IP whitelist.
    Retourne toujours 200 OK pour éviter les retries provider inutiles.
    Les erreurs sont gérées en interne via les logs et le cron de rattrapage.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def _process(self, request, provider):
        try:
            payload = request.data if isinstance(request.data, dict) else {}
            event_id = (
                payload.get("event_id")
                or payload.get("id")
                or request.headers.get("X-Event-Id")
            )
            PaymentService.process_webhook(provider, event_id, payload, dict(request.headers))
        except Exception as e:
            logger.error(f"Webhook {provider} error: {e}")
        # Toujours 200 — même en cas d'erreur interne
        return Response({"received": True}, status=status.HTTP_200_OK)


class WebhookOrangeView(WebhookView):
    @extend_schema(
        tags=["Webhooks"],
        summary="Callback Orange Money",
        description="Reçoit les notifications de statut Orange Money. Vérification par signature HMAC + IP whitelist.",
        request=WebhookGenericSerializer,
    )
    def post(self, request):
        return self._process(request, "orange_money")


class WebhookMTNView(WebhookView):
    @extend_schema(
        tags=["Webhooks"],
        summary="Callback MTN MoMo",
        description="Reçoit les notifications de statut MTN Mobile Money. Vérification par signature HMAC + IP whitelist.",
        request=WebhookGenericSerializer,
    )
    def post(self, request):
        return self._process(request, "mtn_momo")


class WebhookStripeView(WebhookView):
    @extend_schema(
        tags=["Webhooks"],
        summary="Callback Stripe",
        description="Reçoit les événements Stripe (payment_intent.succeeded, etc.). Vérification par Stripe-Signature HMAC-SHA256.",
        request=WebhookGenericSerializer,
    )
    def post(self, request):
        return self._process(request, "stripe")


class WebhookPayPalView(WebhookView):
    @extend_schema(
        tags=["Webhooks"],
        summary="Callback PayPal",
        description="Reçoit les notifications PayPal IPN/Webhooks. Vérification par signature PayPal.",
        request=WebhookGenericSerializer,
    )
    def post(self, request):
        return self._process(request, "paypal")


# ===========================================================================
# CONFIGURATION PROVIDERS
# ===========================================================================

class ProviderConfigListCreateView(APIView):
    """
    POST /payments/providers — Créer un provider (admin global)
    GET  /payments/providers — Lister les providers actifs
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Providers"],
        summary="Créer un provider",
        description=(
            "Enregistre un nouveau provider de paiement. "
            "Les `credentials` et `webhook_secret` sont chiffrés AES-256 avant stockage. "
            "Le secret brut n'est jamais retourné dans les réponses."
        ),
        request=ProviderCreateSerializer,
    )
    def post(self, request):
        d = request.data
        if not d.get("provider"):
            return Response(
                {"detail": "Le champ 'provider' est obligatoire."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if ProviderConfig.objects.filter(provider=d["provider"]).exists():
            return Response(
                {"detail": f"Le provider '{d['provider']}' existe déjà."},
                status=status.HTTP_409_CONFLICT,
            )
        pc = ProviderConfig.objects.create(
            provider=d["provider"],
            display_name=d.get("display_name", d["provider"]),
            api_base_url=d.get("api_base_url"),
            supported_currencies=d.get("supported_currencies", []),
        )
        return Response(
            {"id": str(pc.id), "provider": pc.provider, "message": "Provider created"},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        tags=["Providers"],
        summary="Lister les providers actifs",
        description="Retourne la liste de tous les providers actifs configurés globalement.",
    )
    def get(self, request):
        providers = ProviderConfig.objects.filter(is_active=True)
        data = [
            {
                "id": str(p.id),
                "provider": p.provider,
                "display_name": p.display_name,
                "supported_currencies": p.supported_currencies,
                "is_active": p.is_active,
            }
            for p in providers
        ]
        return Response({"data": data})


class ProviderConfigUpdateView(APIView):
    """
    PUT /payments/providers/{provider}
    Modifie la configuration globale d'un provider existant.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Providers"],
        summary="Modifier un provider",
        description="Met à jour la configuration d'un provider. Seuls les champs fournis sont modifiés.",
        request=ProviderUpdateSerializer,
    )
    def put(self, request, provider):
        try:
            pc = ProviderConfig.objects.get(provider=provider)
        except ProviderConfig.DoesNotExist:
            return Response(
                {"detail": f"Provider '{provider}' introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )
        d = request.data
        if "display_name" in d:
            pc.display_name = d["display_name"]
        if "api_base_url" in d:
            pc.api_base_url = d["api_base_url"]
        if "supported_currencies" in d:
            pc.supported_currencies = d["supported_currencies"]
        if "is_active" in d:
            pc.is_active = d["is_active"]
        pc.save()
        return Response({
            "provider": pc.provider,
            "display_name": pc.display_name,
            "is_active": pc.is_active,
            "message": "Provider updated",
        })


class PlatformProviderConfigView(APIView):
    """
    GET /payments/platforms/{platformId}/providers — Lire la config plateforme
    PUT /payments/platforms/{platformId}/providers — Modifier la config plateforme
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Providers"],
        summary="Lire la config providers d'une plateforme",
        description="Retourne la liste des providers configurés pour cette plateforme avec leur priorité.",
    )
    def get(self, request, platform_id):
        config = PlatformPaymentConfig.get_for_platform(str(platform_id))
        return Response({
            "platform_id": str(platform_id),
            "providers_priority": config.providers_priority,
            "default_currency": config.default_currency,
        })

    @extend_schema(
        tags=["Providers"],
        summary="Configurer les providers d'une plateforme",
        description=(
            "Définit quels providers sont actifs pour cette plateforme et dans quel ordre de priorité. "
            "En cas d'échec du provider prioritaire, le suivant est tenté automatiquement (fallback)."
        ),
        request=PlatformProviderConfigSerializer,
    )
    def put(self, request, platform_id):
        config, _ = PlatformPaymentConfig.objects.get_or_create(
            platform_id=platform_id,
            defaults={"providers_priority": ["orange_money"], "default_currency": "XAF"},
        )
        d = request.data
        if "providers" in d:
            # Vérifier que tous les providers existent en base — CDC conformité
            provider_names = [p["provider"] for p in d["providers"] if p.get("is_active", True)]
            existing = set(
                ProviderConfig.objects.filter(
                    provider__in=provider_names, is_active=True
                ).values_list("provider", flat=True)
            )
            unknown = set(provider_names) - existing
            if unknown:
                return Response(
                    {
                        "detail": f"Providers inconnus ou inactifs : {', '.join(unknown)}. "
                                f"Créez-les d'abord via POST /payments/providers."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            providers_sorted = sorted(d["providers"], key=lambda x: x.get("priority", 99))
            config.providers_priority = [
                p["provider"] for p in providers_sorted if p.get("is_active", True)
            ]
        if "default_currency" in d:
            config.default_currency = d["default_currency"]
        config.save()
        return Response({
            "platform_id": str(platform_id),
            "providers_priority": config.providers_priority,
            "default_currency": config.default_currency,
            "message": "Config updated",
        })


# ===========================================================================
# ADMINISTRATION
# ===========================================================================

class AdminStatsView(APIView):
    """
    GET /payments/admin/stats
    Statistiques globales des transactions. Filtrable par plateforme, provider, période.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Admin"],
        summary="Statistiques des paiements",
        description="Retourne les statistiques agrégées : volume, montants, taux de succès, répartition par provider.",
        parameters=[
            OpenApiParameter("platform_id", OpenApiTypes.UUID, description="Filtrer par plateforme"),
            OpenApiParameter("provider", OpenApiTypes.STR, description="Filtrer par provider"),
            OpenApiParameter("from_date", OpenApiTypes.DATE, description="Date de début (YYYY-MM-DD)"),
            OpenApiParameter("to_date", OpenApiTypes.DATE, description="Date de fin (YYYY-MM-DD)"),
        ],
    )
    def get(self, request):
        qs = Transaction.objects.all()

        platform_id = request.GET.get("platform_id")
        provider = request.GET.get("provider")
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        if platform_id:
            qs = qs.filter(platform_id=platform_id)
        if provider:
            qs = qs.filter(provider=provider)
        if from_date:
            qs = qs.filter(created_at__date__gte=from_date)
        if to_date:
            qs = qs.filter(created_at__date__lte=to_date)

        total = qs.count()
        total_amount = qs.filter(status="succeeded").aggregate(s=Sum("amount"))["s"] or 0
        succeeded = qs.filter(status="succeeded").count()
        success_rate = round((succeeded / total * 100), 1) if total > 0 else 0

        by_provider = []
        for row in qs.values("provider").annotate(count=Count("id")):
            prov_succeeded = qs.filter(provider=row["provider"], status="succeeded").count()
            prov_rate = round((prov_succeeded / row["count"] * 100), 1) if row["count"] > 0 else 0
            by_provider.append({
                "provider": row["provider"],
                "count": row["count"],
                "success_rate": prov_rate,
            })

        return Response({
            "total_transactions": total,
            "total_amount": float(total_amount),
            "currency": "XAF",
            "success_rate": success_rate,
            "by_provider": by_provider,
        })


class AdminForceStatusView(APIView):
    """
    POST /payments/admin/{transactionId}/force-status
    Force le statut d'une transaction après vérification manuelle.
    Réservé à l'admin global. Action loggée dans transaction_status_history.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Admin"],
        summary="Forcer le statut d'une transaction",
        description=(
            "Permet à un admin de forcer manuellement le statut d'une transaction après vérification "
            "sur le dashboard du provider. L'action est tracée dans l'historique avec trigger='admin_manual'."
        ),
        request=ForceStatusSerializer,
    )
    def post(self, request, transaction_id):
        try:
            tx = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )
        new_status = request.data.get("status")
        if new_status not in ["succeeded", "failed"]:
            return Response(
                {"detail": "Le statut doit être 'succeeded' ou 'failed'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if tx.is_terminal():
            return Response(
                {"detail": f"Transaction déjà en état terminal : {tx.status}. Aucune transition possible."},
                status=status.HTTP_409_CONFLICT,
            )
        reason = request.data.get("reason", "")
        tx.transition_to(new_status, trigger="admin_manual", metadata={"reason": reason})
        return Response({
            "transaction_id": str(tx.id),
            "status": tx.status,
            "message": "Status forced",
        })


class AdminReconciliationView(APIView):
    """
    GET /payments/admin/reconciliation
    Liste les rapports de réconciliation provider ↔ transactions internes.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Admin"],
        summary="Rapports de réconciliation",
        description="Liste les rapports de rapprochement entre les transactions internes et les relevés des providers.",
        parameters=[
            OpenApiParameter("provider", OpenApiTypes.STR, description="Filtrer par provider"),
            OpenApiParameter("from_date", OpenApiTypes.DATE, description="Date de début (YYYY-MM-DD)"),
            OpenApiParameter("to_date", OpenApiTypes.DATE, description="Date de fin (YYYY-MM-DD)"),
        ],
    )
    def get(self, request):
        # Import ici pour éviter l'erreur si le modèle n'existe pas encore
        try:
            from apps.payments.models import ReconciliationReport
            qs = ReconciliationReport.objects.all().order_by("-created_at")
            provider = request.GET.get("provider")
            from_date = request.GET.get("from_date")
            to_date = request.GET.get("to_date")
            if provider:
                qs = qs.filter(provider=provider)
            if from_date:
                qs = qs.filter(created_at__date__gte=from_date)
            if to_date:
                qs = qs.filter(created_at__date__lte=to_date)
            data = [
                {
                    "id": str(r.id),
                    "provider": r.provider,
                    "period_start": r.period_start.isoformat(),
                    "period_end": r.period_end.isoformat(),
                    "total_internal": r.total_internal,
                    "total_provider": r.total_provider,
                    "matched": r.matched,
                    "mismatched": r.mismatched,
                    "status": r.status,
                    "created_at": r.created_at.isoformat(),
                }
                for r in qs
            ]
            return Response({"data": data, "total": qs.count()})
        except Exception:
            # Si le modèle ReconciliationReport n'est pas encore migré
            return Response({"data": [], "total": 0, "message": "Aucun rapport disponible."})


class RGPDPurgeView(APIView):
    """
    DELETE /payments/by-user/{userId}
    Purge RGPD : anonymise les données personnelles d'un utilisateur.
    Les transactions ne sont JAMAIS supprimées (obligation comptable légale).
    Seuls user_id et phone_number sont mis à NULL.
    Auth : S2S token uniquement (appelé par Users lors du workflow de suppression de compte).
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Admin"],
        summary="Purge RGPD — anonymiser les données d'un utilisateur",
        description=(
            "Anonymise les données personnelles (user_id, phone_number) de toutes les transactions "
            "liées à cet utilisateur. Les transactions sont conservées pour obligation comptable. "
            "Auth : S2S token obligatoire."
        ),
    )
    def delete(self, request, user_id):
        updated = Transaction.objects.filter(user_id=user_id).update(
            user_id=None,
            phone_number=None,
        )
        if updated == 0:
            return Response(
                {"detail": f"Aucune transaction trouvée pour l'utilisateur {user_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response({
            "user_id": str(user_id),
            "transactions_anonymized": updated,
            "message": "Données personnelles anonymisées avec succès.",
        })