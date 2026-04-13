#!/bin/bash
# =============================================================================
# AG TECHNOLOGIES — RESET ALL (Linux / macOS)
# Usage : bash reset_all.sh           → reset sans perte de données
#         bash reset_all.sh --clean   → reset + suppression des volumes (données)
# =============================================================================

CLEAN=false
if [[ "$1" == "--clean" ]]; then CLEAN=true; fi

echo -e "\e[36m=========================================\e[0m"
echo -e "\e[36m RESET ALL - AG TECHNOLOGIES             \e[0m"
if $CLEAN; then
    echo -e "\e[31m MODE: CLEAN (volumes seront supprimés)  \e[0m"
else
    echo -e "\e[32m MODE: SOFT (volumes conservés)          \e[0m"
fi
echo -e "\e[36m=========================================\e[0m"

# --- Tous les conteneurs AGT (11 services + infra) ---
ALL_PATTERNS=("agt_auth_" "agt_users_" "agt_notif_" "agt_sub_" "agt_pay_" "agt_wallet_" "agt_search_" "agt_chatbot_" "agt_media_" "agt_chat_" "agt_geoloc_" "agt_gateway" "agt_rabbitmq" "agt_mailpit" "agt_elasticsearch")

# --- Étape 1 : Arrêt et suppression des conteneurs AGT ---
echo -e "\n\e[33m[1/5] Arrêt de tous les conteneurs AGT...\e[0m"
STOPPED=0
for container in $(docker ps -a --format "{{.Names}}"); do
    for pattern in "${ALL_PATTERNS[@]}"; do
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

# --- Étape 3 : Suppression des fichiers .env (tous les services) ---
echo -e "\n\e[33m[3/5] Suppression des fichiers .env...\e[0m"
SERVICES=("agt-auth" "agt-users" "agt-notification" "agt-subscription" "agt-payment" "agt-wallet" "agt-search" "agt-chatbot" "agt-media" "agt-chat" "agt-geoloc")
for service in "${SERVICES[@]}"; do
    rm -f "$service/.env"
done
echo -e "\e[32m -> Fichiers .env nettoyés.\e[0m"

# --- Étape 4 : Suppression des volumes (uniquement si --clean) ---
echo -e "\n\e[33m[4/5] Gestion des volumes...\e[0m"
if $CLEAN; then
    echo -e "\e[31m -> Mode --clean : suppression de tous les volumes AGT...\e[0m"
    VOLUME_PATTERNS=("agt-auth_" "agt-users_" "agt-notification_" "agt-subscription_" "agt-payment_" "agt-wallet_" "agt-search_" "agt-chatbot_" "agt-media_" "agt-chat_" "agt-geoloc_")
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

# --- Étape 5 : Relancement complet ---
echo -e "\n\e[33m[5/5] Relancement du déploiement complet...\e[0m"
bash deploy_all.sh