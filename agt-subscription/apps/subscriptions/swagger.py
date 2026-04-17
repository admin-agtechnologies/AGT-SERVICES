"""
AGT Subscription Service v1.0 - Annotations Swagger/OpenAPI (drf-spectacular).
Chaque décorateur documente : request body + responses + summary + tags.
À importer et appliquer via @extend_schema sur chaque view dans views.py.
"""
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers


# ===========================================================================
# SERIALIZERS REQUEST — body des endpoints POST/PUT
# ===========================================================================

# --- Plans ---

class PlanPriceInputSerializer(serializers.Serializer):
    """Un prix pour un cycle de facturation donné."""
    billing_cycle = serializers.ChoiceField(
        choices=["monthly", "yearly", "custom"],
        help_text="Cycle de facturation : monthly, yearly ou custom"
    )
    price = serializers.DecimalField(
        max_digits=12, decimal_places=2,
        help_text="Prix pour ce cycle. Ex: 5000.00"
    )
    currency = serializers.CharField(
        default="XAF",
        help_text="Devise ISO 4217. Ex: XAF, EUR, USD"
    )
    cycle_days = serializers.IntegerField(
        required=False, allow_null=True,
        help_text="Nombre de jours si billing_cycle=custom"
    )


class PlanQuotaInputSerializer(serializers.Serializer):
    """Un quota attaché au plan."""
    quota_key = serializers.CharField(
        help_text="Clé du quota. Ex: api_calls, storage_mb, messages"
    )
    limit_value = serializers.IntegerField(
        help_text="Limite maximale pour ce quota par cycle"
    )
    is_cyclical = serializers.BooleanField(
        default=True,
        help_text="Si True, le quota se remet à zéro à chaque nouveau cycle"
    )
    overage_policy = serializers.ChoiceField(
        choices=["hard", "overage"],
        default="hard",
        help_text="hard = bloqué au dépassement, overage = facturation à l'unité"
    )
    overage_unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Prix par unité en cas de dépassement (si overage_policy=overage)"
    )


class PlanCreateSerializer(serializers.Serializer):
    """Body pour créer un plan avec ses prix et quotas."""
    platform_id = serializers.UUIDField(
        help_text="UUID de la plateforme propriétaire du plan"
    )
    name = serializers.CharField(
        max_length=100,
        help_text="Nom du plan. Ex: Starter, Pro, Enterprise"
    )
    slug = serializers.CharField(
        max_length=100,
        help_text="Identifiant URL unique par plateforme. Ex: starter, pro"
    )
    description = serializers.CharField(
        required=False, allow_blank=True,
        help_text="Description du plan (optionnel)"
    )
    is_free = serializers.BooleanField(
        default=False,
        help_text="True si le plan est gratuit (prix = 0)"
    )
    is_default = serializers.BooleanField(
        default=False,
        help_text="True si ce plan est attribué par défaut aux nouveaux abonnés"
    )
    tier_order = serializers.IntegerField(
        default=0,
        help_text="Ordre d'affichage (0 = premier). Utile pour le tri des plans"
    )
    prices = PlanPriceInputSerializer(
        many=True, required=False,
        help_text="Liste des prix par cycle de facturation"
    )
    quotas = PlanQuotaInputSerializer(
        many=True, required=False,
        help_text="Liste des quotas associés au plan"
    )


class PlanUpdateSerializer(serializers.Serializer):
    """Body pour modifier un plan (champs limités si abonnements actifs)."""
    name = serializers.CharField(
        required=False, max_length=100,
        help_text="Nouveau nom du plan"
    )
    description = serializers.CharField(
        required=False, allow_blank=True,
        help_text="Nouvelle description"
    )
    metadata = serializers.JSONField(
        required=False, allow_null=True,
        help_text="Métadonnées libres au format JSON"
    )


# --- Subscriptions ---

class SubscriptionCreateSerializer(serializers.Serializer):
    """Body pour créer un abonnement."""
    platform_id = serializers.UUIDField(
        help_text="UUID de la plateforme"
    )
    subscriber_type = serializers.ChoiceField(
        choices=["user", "organization"],
        default="user",
        help_text="Type d'abonné : user (B2C) ou organization (B2B)"
    )
    subscriber_id = serializers.UUIDField(
        help_text="UUID de l'utilisateur ou de l'organisation abonnée"
    )
    plan_id = serializers.UUIDField(
        help_text="UUID du plan auquel souscrire"
    )
    billing_cycle = serializers.ChoiceField(
        choices=["monthly", "yearly", "custom"],
        default="monthly",
        help_text="Cycle de facturation souhaité"
    )
    with_trial = serializers.BooleanField(
        default=False,
        help_text="True pour démarrer avec une période d'essai (si le plan en a une)"
    )


class SubscriptionChangePlanSerializer(serializers.Serializer):
    """Body pour changer de plan (upgrade/downgrade avec prorata)."""
    new_plan_id = serializers.UUIDField(
        help_text="UUID du nouveau plan cible"
    )
    billing_cycle = serializers.ChoiceField(
        choices=["monthly", "yearly", "custom"],
        default="monthly",
        help_text="Cycle de facturation pour le nouveau plan"
    )


# --- Quotas ---

class QuotaCheckSerializer(serializers.Serializer):
    """Body pour vérifier un quota (chemin critique < 50ms)."""
    platform_id = serializers.UUIDField(help_text="UUID de la plateforme")
    subscriber_type = serializers.ChoiceField(
        choices=["user", "organization"], default="user",
        help_text="Type d'abonné"
    )
    subscriber_id = serializers.UUIDField(help_text="UUID de l'utilisateur ou de l'organisation")
    quota_key = serializers.CharField(help_text="Clé du quota. Ex: api_calls, storage_mb")
    amount = serializers.IntegerField(default=1, help_text="Quantité à vérifier")


class QuotaIncrementSerializer(serializers.Serializer):
    """Body pour incrémenter un quota directement."""
    platform_id = serializers.UUIDField(help_text="UUID de la plateforme")
    subscriber_type = serializers.ChoiceField(
        choices=["user", "organization"], default="user"
    )
    subscriber_id = serializers.UUIDField(help_text="UUID de l'utilisateur ou de l'organisation")
    quota_key = serializers.CharField(help_text="Clé du quota à incrémenter")
    amount = serializers.IntegerField(default=1, help_text="Quantité à ajouter")


class QuotaReserveSerializer(serializers.Serializer):
    """Body pour réserver un quota (pattern reserve/confirm/release)."""
    platform_id = serializers.UUIDField(help_text="UUID de la plateforme")
    subscriber_type = serializers.ChoiceField(
        choices=["user", "organization"], default="user"
    )
    subscriber_id = serializers.UUIDField(help_text="UUID de l'utilisateur ou de l'organisation")
    quota_key = serializers.CharField(help_text="Clé du quota à réserver")
    amount = serializers.IntegerField(default=1, help_text="Quantité à réserver")


class QuotaConfirmSerializer(serializers.Serializer):
    """Body pour confirmer une réservation de quota."""
    reservation_id = serializers.UUIDField(
        help_text="UUID de la réservation à confirmer (obtenu via /quotas/reserve)"
    )


class QuotaReleaseSerializer(serializers.Serializer):
    """Body pour libérer une réservation de quota."""
    reservation_id = serializers.UUIDField(
        help_text="UUID de la réservation à annuler/libérer"
    )


# --- Organizations ---

class OrganizationCreateSerializer(serializers.Serializer):
    """Body pour créer une organisation B2B."""
    platform_id = serializers.UUIDField(
        help_text="UUID de la plateforme"
    )
    name = serializers.CharField(
        max_length=150,
        help_text="Nom de l'organisation. Doit être unique par plateforme"
    )
    owner_user_id = serializers.UUIDField(
        help_text="UUID de l'utilisateur propriétaire de l'organisation"
    )


class OrganizationMemberAddSerializer(serializers.Serializer):
    """Body pour ajouter un membre à une organisation."""
    user_id = serializers.UUIDField(
        help_text="UUID de l'utilisateur à ajouter"
    )
    role = serializers.ChoiceField(
        choices=["owner", "member"],
        default="member",
        help_text="Rôle du membre : owner ou member"
    )


# --- Config ---

class PlatformConfigUpdateSerializer(serializers.Serializer):
    """Body pour mettre à jour la config d'une plateforme."""
    trial_days = serializers.IntegerField(
        required=False, allow_null=True,
        help_text="Nombre de jours d'essai par défaut pour cette plateforme"
    )
    grace_period_days = serializers.IntegerField(
        required=False, allow_null=True,
        help_text="Nombre de jours de grâce après expiration avant suspension"
    )
    allow_multiple_subscriptions = serializers.BooleanField(
        required=False,
        help_text="Autoriser plusieurs abonnements actifs simultanés"
    )
    default_currency = serializers.CharField(
        required=False, max_length=3,
        help_text="Devise par défaut. Ex: XAF, EUR"
    )


# ===========================================================================
# SERIALIZERS RESPONSE — structure des réponses documentées
# ===========================================================================

class HealthResponseSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="healthy ou degraded")
    database = serializers.CharField(help_text="ok ou error")
    redis = serializers.CharField(help_text="ok ou error")
    version = serializers.CharField(help_text="Version du service")


class PlanResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    is_free = serializers.BooleanField()
    tier_order = serializers.IntegerField()
    prices = serializers.ListField()
    quotas = serializers.ListField()


class SubscriptionResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.CharField(help_text="trial, active, pending, cancelled, expired, grace")
    plan = serializers.CharField(help_text="Nom du plan")
    current_period_start = serializers.DateTimeField()
    current_period_end = serializers.DateTimeField()
    trial_end = serializers.DateTimeField(allow_null=True)
    message = serializers.CharField()


class QuotaCheckResponseSerializer(serializers.Serializer):
    allowed = serializers.BooleanField(help_text="True si le quota autorise l'action")
    quota_key = serializers.CharField()
    used = serializers.IntegerField()
    limit = serializers.IntegerField()
    remaining = serializers.IntegerField()


class QuotaReserveResponseSerializer(serializers.Serializer):
    reservation_id = serializers.UUIDField(help_text="À conserver pour confirm ou release")
    quota_key = serializers.CharField()
    amount = serializers.IntegerField()
    status = serializers.CharField(help_text="reserved")


class OrganizationResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    platform_id = serializers.UUIDField()
    name = serializers.CharField()
    owner_user_id = serializers.UUIDField()
    is_active = serializers.BooleanField()


class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(help_text="Message d'erreur")


# ===========================================================================
# DÉCORATEURS SWAGGER — à appliquer sur chaque view dans views.py
# ===========================================================================

# --- Health ---
health_schema = extend_schema(
    tags=["Health"],
    summary="Health check",
    description="Vérifie l'état du service (DB, Redis). Aucune authentification requise.",
    responses={
        200: HealthResponseSerializer,
        503: ErrorResponseSerializer,
    }
)

# --- Plans ---
plan_create_schema = extend_schema(
    tags=["Plans"],
    summary="Créer un plan avec prix et quotas",
    description="Crée un plan tarifaire pour une plateforme. Le slug doit être unique par plateforme.",
    request=PlanCreateSerializer,
    responses={
        201: PlanResponseSerializer,
        400: ErrorResponseSerializer,
        409: OpenApiResponse(description="Slug déjà existant pour cette plateforme"),
    }
)

plan_list_schema = extend_schema(
    tags=["Plans"],
    summary="Lister les plans",
    description="Retourne la liste des plans actifs. Filtre possible par platform_id.",
    parameters=[
        OpenApiParameter("platform_id", OpenApiTypes.UUID, OpenApiParameter.QUERY,
                         required=False, description="Filtrer par plateforme"),
    ],
    responses={200: PlanResponseSerializer(many=True)}
)

plan_detail_schema = extend_schema(
    tags=["Plans"],
    summary="Détail d'un plan",
    responses={
        200: PlanResponseSerializer,
        404: ErrorResponseSerializer,
    }
)

plan_update_schema = extend_schema(
    tags=["Plans"],
    summary="Modifier un plan (nom/description uniquement si abonnements actifs)",
    description="Si le plan a des abonnements actifs, seuls name, description et metadata sont modifiables.",
    request=PlanUpdateSerializer,
    responses={
        200: PlanResponseSerializer,
        404: ErrorResponseSerializer,
    }
)

plan_archive_schema = extend_schema(
    tags=["Plans"],
    summary="Archiver un plan",
    description="Désactive un plan. Impossible si des abonnements actifs y sont attachés.",
    responses={
        200: OpenApiResponse(description="Plan archivé avec succès"),
        404: ErrorResponseSerializer,
        409: OpenApiResponse(description="Plan avec abonnements actifs — ne peut pas être archivé"),
    }
)

# --- Subscriptions ---
subscription_create_schema = extend_schema(
    tags=["Subscriptions"],
    summary="Créer un abonnement",
    description="Crée un abonnement pour un user ou une organisation. Un seul abonnement actif par subscriber.",
    request=SubscriptionCreateSerializer,
    responses={
        201: SubscriptionResponseSerializer,
        400: ErrorResponseSerializer,
        404: OpenApiResponse(description="Plan ou prix introuvable"),
        409: OpenApiResponse(description="Abonnement actif existant pour ce subscriber"),
    }
)

subscription_list_schema = extend_schema(
    tags=["Subscriptions"],
    summary="Lister les abonnements",
    parameters=[
        OpenApiParameter("platform_id", OpenApiTypes.UUID, OpenApiParameter.QUERY, required=False),
        OpenApiParameter("subscriber_id", OpenApiTypes.UUID, OpenApiParameter.QUERY, required=False),
        OpenApiParameter("status", OpenApiTypes.STR, OpenApiParameter.QUERY, required=False,
                         description="trial, active, pending, cancelled, expired, grace"),
    ],
    responses={200: SubscriptionResponseSerializer(many=True)}
)

subscription_detail_schema = extend_schema(
    tags=["Subscriptions"],
    summary="Détail abonnement avec usage quotas",
    responses={
        200: OpenApiResponse(description="Abonnement avec usage quotas courant"),
        404: ErrorResponseSerializer,
    }
)

subscription_activate_schema = extend_schema(
    tags=["Subscriptions"],
    summary="Activer après paiement",
    description="Passe l'abonnement de pending à active. Appelé après confirmation du paiement.",
    responses={
        200: SubscriptionResponseSerializer,
        400: ErrorResponseSerializer,
    }
)

subscription_cancel_schema = extend_schema(
    tags=["Subscriptions"],
    summary="Annuler (actif jusqu'à fin de cycle)",
    description="Marque l'abonnement pour annulation en fin de période courante. Pas de remboursement.",
    responses={
        200: SubscriptionResponseSerializer,
        404: ErrorResponseSerializer,
        409: OpenApiResponse(description="Abonnement déjà annulé ou expiré"),
    }
)

subscription_change_plan_schema = extend_schema(
    tags=["Subscriptions"],
    summary="Upgrade/downgrade avec prorata",
    description="Change le plan d'un abonnement actif. Calcule le prorata entre l'ancien et le nouveau plan.",
    request=SubscriptionChangePlanSerializer,
    responses={
        200: OpenApiResponse(description="Plan changé avec détail du prorata"),
        400: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: OpenApiResponse(description="Abonnement non actif"),
    }
)

subscription_reactivate_schema = extend_schema(
    tags=["Subscriptions"],
    summary="Réactiver un abonnement",
    description="Annule la demande d'annulation en fin de cycle (cancel_at_period_end → False).",
    responses={
        200: SubscriptionResponseSerializer,
        404: ErrorResponseSerializer,
        409: OpenApiResponse(description="L'abonnement n'est pas en état annulable"),
    }
)

# --- Quotas ---
quota_check_schema = extend_schema(
    tags=["Quotas"],
    summary="Vérifier un quota (< 50ms)",
    description="Vérifie si l'action est autorisée selon le quota de l'abonnement. Endpoint critique — ne modifie rien.",
    request=QuotaCheckSerializer,
    responses={
        200: QuotaCheckResponseSerializer,
        404: ErrorResponseSerializer,
    }
)

quota_increment_schema = extend_schema(
    tags=["Quotas"],
    summary="Incrémenter un quota",
    description="Incrémente directement le compteur d'un quota. À utiliser pour les actions non critiques.",
    request=QuotaIncrementSerializer,
    responses={
        200: OpenApiResponse(description="Quota incrémenté"),
        400: OpenApiResponse(description="Quota dépassé (hard limit)"),
        404: ErrorResponseSerializer,
    }
)

quota_reserve_schema = extend_schema(
    tags=["Quotas"],
    summary="Réserver un quota",
    description="Réserve temporairement une quantité de quota. Retourne un reservation_id à confirmer ou libérer.",
    request=QuotaReserveSerializer,
    responses={
        200: QuotaReserveResponseSerializer,
        400: OpenApiResponse(description="Quota insuffisant pour cette réservation"),
        404: ErrorResponseSerializer,
    }
)

quota_confirm_schema = extend_schema(
    tags=["Quotas"],
    summary="Confirmer une réservation",
    description="Confirme une réservation : le quota réservé est définitivement consommé.",
    request=QuotaConfirmSerializer,
    responses={
        200: OpenApiResponse(description="Réservation confirmée"),
        404: OpenApiResponse(description="Réservation introuvable"),
    }
)

quota_release_schema = extend_schema(
    tags=["Quotas"],
    summary="Libérer une réservation",
    description="Annule une réservation : le quota réservé est restitué à l'abonnement.",
    request=QuotaReleaseSerializer,
    responses={
        200: OpenApiResponse(description="Réservation libérée"),
        404: OpenApiResponse(description="Réservation introuvable"),
    }
)

quota_usage_schema = extend_schema(
    tags=["Quotas"],
    summary="Consultation usage courant",
    description="Retourne l'état de tous les quotas pour la période courante de l'abonnement.",
    responses={
        200: OpenApiResponse(description="Usage quotas de la période courante"),
        404: ErrorResponseSerializer,
    }
)

# --- Organizations ---
organization_create_schema = extend_schema(
    tags=["Organizations"],
    summary="Créer une organisation B2B",
    description="Crée une organisation. Le nom doit être unique par plateforme.",
    request=OrganizationCreateSerializer,
    responses={
        201: OrganizationResponseSerializer,
        400: ErrorResponseSerializer,
        409: OpenApiResponse(description="Nom d'organisation déjà existant sur cette plateforme"),
    }
)

organization_list_schema = extend_schema(
    tags=["Organizations"],
    summary="Lister les organisations",
    parameters=[
        OpenApiParameter("platform_id", OpenApiTypes.UUID, OpenApiParameter.QUERY, required=False),
    ],
    responses={200: OrganizationResponseSerializer(many=True)}
)

member_add_schema = extend_schema(
    tags=["Organizations"],
    summary="Ajouter un membre",
    description="Ajoute un utilisateur à une organisation avec un rôle donné.",
    request=OrganizationMemberAddSerializer,
    responses={
        201: OpenApiResponse(description="Membre ajouté"),
        400: ErrorResponseSerializer,
        404: OpenApiResponse(description="Organisation introuvable"),
        409: OpenApiResponse(description="Utilisateur déjà membre"),
    }
)

member_list_schema = extend_schema(
    tags=["Organizations"],
    summary="Lister les membres",
    responses={
        200: OpenApiResponse(description="Liste des membres de l'organisation"),
        404: ErrorResponseSerializer,
    }
)

member_remove_schema = extend_schema(
    tags=["Organizations"],
    summary="Retirer un membre",
    responses={
        204: OpenApiResponse(description="Membre retiré"),
        404: ErrorResponseSerializer,
    }
)

# --- Config ---
config_get_schema = extend_schema(
    tags=["Config"],
    summary="Lire la config d'une plateforme",
    responses={
        200: OpenApiResponse(description="Configuration de la plateforme"),
        404: ErrorResponseSerializer,
    }
)

config_update_schema = extend_schema(
    tags=["Config"],
    summary="Mettre à jour la config d'une plateforme",
    request=PlatformConfigUpdateSerializer,
    responses={
        200: OpenApiResponse(description="Configuration mise à jour"),
        404: ErrorResponseSerializer,
    }
)