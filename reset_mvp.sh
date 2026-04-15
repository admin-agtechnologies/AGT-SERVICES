#!/bin/bash
# =============================================================================
# AG TECHNOLOGIES — RESET MVP (Linux / macOS)
# Usage : bash reset_mvp.sh           → reset sans perte de données
#         bash reset_mvp.sh --clean   → reset + suppression des volumes (données)
# =============================================================================

CLEAN=false
if [[ "$1" == "--clean" ]]; then CLEAN=true; fi

echo -e "\e[36m=========================================\e[0m"
echo -e "\e[36m RESET MVP - AG TECHNOLOGIES             \e[0m"
if $CLEAN; then
    echo -e "\e[31m MODE: CLEAN (volumes seront supprimés)  \e[0m"
else
    echo -e "\e[32m MODE: SOFT (volumes conservés)          \e[0m""""
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
    fallback_enabled = serializers.BooleanField(required=False)"""
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
fi
echo -e "\e[36m=========================================\e[0m"

# --- Patterns des conteneurs MVP ---
MVP_PATTERNS=("agt_auth_" "agt_users_" "agt_notif_" "agt-gateway" "agt-rabbitmq" "agt-mailpit" "agt-elasticsearch")

# --- Étape 1 : Arrêt et suppression des conteneurs AGT MVP ---
echo -e "\n\e[33m[1/5] Arrêt des conteneurs AGT MVP...\e[0m"
STOPPED=0
for container in $(docker ps -a --format "{{.Names}}"); do
    for pattern in "${MVP_PATTERNS[@]}"; do
        if [[ "$container" == ${pattern}* ]]; then
            echo -e "\e[90m -> Arrêt de $container...\e[0m"
            docker stop "$container" > /dev/null 2>&1
            docker rm "$container" > /dev/null 2>&1
            STOPPED=$((STOPPED + 1))
            break
        fi
    done
done
echo -e "\e[32m -> $STOPPED conteneur(s) supprimé(s).\e[0m"

# --- Étape 2 : Suppression du réseau AGT ---
echo -e "\n\e[33m[2/5] Suppression du réseau agt_network...\e[0m"
if docker network ls --filter name=^agt_network$ --format "{{.Name}}" | grep -q agt_network; then
    docker network rm agt_network > /dev/null 2>&1
    echo -e "\e[32m -> Réseau supprimé.\e[0m"
else
    echo -e "\e[90m -> Réseau inexistant, rien à faire.\e[0m"
fi

# --- Étape 3 : Suppression des fichiers .env MVP ---
echo -e "\n\e[33m[3/5] Suppression des fichiers .env MVP...\e[0m"
rm -f agt-auth/.env agt-users/.env agt-notification/.env
echo -e "\e[32m -> Fichiers .env nettoyés.\e[0m"

# --- Étape 4 : Suppression des volumes (uniquement si --clean) ---
echo -e "\n\e[33m[4/5] Gestion des volumes...\e[0m"
if $CLEAN; then
    echo -e "\e[31m -> Mode --clean : suppression des volumes AGT MVP...\e[0m"
    VOLUME_PATTERNS=("agt-auth_" "agt-users_" "agt-notification_")
    DELETED=0
    for vol in $(docker volume ls --format "{{.Name}}"); do
        for pattern in "${VOLUME_PATTERNS[@]}"; do
            if [[ "$vol" == ${pattern}* ]]; then
                docker volume rm "$vol" > /dev/null 2>&1
                echo -e "\e[90m    -> Volume $vol supprimé.\e[0m"
                DELETED=$((DELETED + 1))
                break
            fi
        done
        # Volumes infra
        if [[ "$vol" == *"rabbitmq_data"* ]] || [[ "$vol" == *"es_data"* ]]; then
            docker volume rm "$vol" > /dev/null 2>&1
            echo -e "\e[90m    -> Volume $vol supprimé.\e[0m"
            DELETED=$((DELETED + 1))
        fi
    done
    echo -e "\e[32m -> $DELETED volume(s) supprimé(s).\e[0m"
else
    echo -e "\e[32m -> Mode soft : volumes conservés (données intactes).\e[0m"
fi

# --- Étape 5 : Relancement du MVP ---
echo -e "\n\e[33m[5/5] Relancement du déploiement MVP...\e[0m"
bash deploy_mvp.sh