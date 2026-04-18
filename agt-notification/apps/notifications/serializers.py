"""
AGT Notification Service v1.0 - Serializers pour Swagger/OpenAPI.
Ces serializers servent uniquement à documenter les body des requêtes POST/PUT
dans Swagger via @extend_schema(request=...). La logique métier utilise request.data.
"""
from rest_framework import serializers


# --- Send ---

class SendNotificationSerializer(serializers.Serializer):
    """Body pour POST /notifications/send"""
    user_id = serializers.UUIDField(help_text="UUID de l'utilisateur destinataire")
    channels = serializers.ListField(
        child=serializers.ChoiceField(choices=["email", "sms", "push", "whatsapp", "in_app"]),
        help_text="Canaux d'envoi (ex: ['email', 'in_app'])"
    )
    template_name = serializers.CharField(help_text="Nom du template à utiliser")
    variables = serializers.DictField(required=False, default={}, help_text="Variables du template (ex: {'verification_url': '...'})")
    locale = serializers.CharField(required=False, default="fr", help_text="Langue du template")
    priority = serializers.ChoiceField(choices=["low", "normal", "high", "critical"], required=False, default="normal")
    category = serializers.ChoiceField(choices=["transactional", "marketing", "security"], required=False, default="transactional")
    idempotency_key = serializers.UUIDField(required=False, help_text="Clé d'idempotence (optionnel)")


class SendBulkNotificationSerializer(serializers.Serializer):
    """Body pour POST /notifications/send-bulk"""
    user_ids = serializers.ListField(child=serializers.UUIDField(), help_text="Liste des UUIDs destinataires (max 100)")
    channels = serializers.ListField(child=serializers.ChoiceField(choices=["email", "sms", "push", "whatsapp", "in_app"]))
    template_name = serializers.CharField()
    variables = serializers.DictField(required=False, default={})
    locale = serializers.CharField(required=False, default="fr")
    category = serializers.ChoiceField(choices=["transactional", "marketing", "security"], required=False, default="transactional")


# --- Templates ---

class TemplateCreateSerializer(serializers.Serializer):
    """Body pour POST /templates"""
    name = serializers.CharField(help_text="Nom unique du template (ex: auth_verify_email)")
    channel = serializers.ChoiceField(choices=["email", "sms", "push", "whatsapp", "in_app"])
    body = serializers.CharField(help_text="Corps du template (supporte Jinja2 : {{ variable }})")
    subject = serializers.CharField(required=False, help_text="Sujet (email uniquement)")
    category = serializers.ChoiceField(choices=["transactional", "marketing", "security"], required=False, default="transactional")
    platform_id = serializers.UUIDField(required=False, help_text="UUID plateforme (null = global)")
    locale = serializers.CharField(required=False, default="fr")


class TemplateUpdateSerializer(serializers.Serializer):
    """Body pour PUT /templates/{id}"""
    body = serializers.CharField(help_text="Nouveau corps du template")
    subject = serializers.CharField(required=False)
    locale = serializers.CharField(required=False, default="fr")


class TemplatePreviewSerializer(serializers.Serializer):
    """Body pour POST /templates/{id}/preview"""
    variables = serializers.DictField(required=False, default={}, help_text="Variables pour le rendu")
    locale = serializers.CharField(required=False, default="fr")


# --- Preferences ---

class PreferenceUpdateSerializer(serializers.Serializer):
    """Body pour PUT /users/{id}/notification-preferences"""
    channels = serializers.DictField(
        required=False,
        help_text="Canaux actifs (ex: {'email': true, 'sms': false, 'push': true, 'whatsapp': true, 'in_app': true})"
    )
    categories = serializers.DictField(
        required=False,
        help_text="Catégories actives (ex: {'transactional': true, 'marketing': false}). Security est toujours true."
    )


# --- Campaigns ---

class CampaignCreateSerializer(serializers.Serializer):
    """Body pour POST /campaigns"""
    name = serializers.CharField(help_text="Nom de la campagne")
    template_name = serializers.CharField(help_text="Nom du template")
    channel = serializers.ChoiceField(choices=["email", "sms", "push", "whatsapp", "in_app"])
    user_ids = serializers.ListField(child=serializers.UUIDField(), help_text="Liste des destinataires")
    variables = serializers.DictField(required=False, default={})
    throttle_per_second = serializers.IntegerField(required=False, default=10)


# --- Device Tokens ---

class DeviceTokenCreateSerializer(serializers.Serializer):
    """Body pour POST /users/{id}/device-tokens"""
    token = serializers.CharField(help_text="Token FCM/APNs du device")
    device_type = serializers.ChoiceField(choices=["android", "ios", "web"])
    device_name = serializers.CharField(required=False, help_text="Nom du device (ex: 'iPhone 15')")


# --- Channel Config ---

class ChannelConfigUpdateSerializer(serializers.Serializer):
    """Body pour PUT /platforms/{id}/channels-priority"""
    priority_order = serializers.ListField(
        child=serializers.ChoiceField(choices=["email", "sms", "push", "whatsapp", "in_app"]),
        required=False,
        help_text="Ordre de priorité des canaux"
    )
    fallback_enabled = serializers.BooleanField(required=False)

class ScheduledNotificationCreateSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    channels = serializers.ListField(child=serializers.CharField(), min_length=1)
    template_name = serializers.CharField()
    locale = serializers.CharField(default="fr")
    variables = serializers.DictField(required=False, default=dict)
    scheduled_at = serializers.DateTimeField()

class ScheduledNotificationUpdateSerializer(serializers.Serializer):
    scheduled_at = serializers.DateTimeField(required=False)
    variables = serializers.DictField(required=False)