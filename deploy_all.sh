#!/bin/bash
# =============================================================================
# AG TECHNOLOGIES — DÉPLOIEMENT COMPLET (Linux / macOS)
# Tous les 11 services + infrastructure partagée
# =============================================================================

echo -e "\e[36m=========================================\e[0m"
echo -e "\e[36m DÉPLOIEMENT COMPLET - AG TECHNOLOGIES   \e[0m"
echo -e "\e[36m=========================================\e[0m"

# --- Fonction utilitaire : attendre qu'un service soit healthy ---
wait_for_health() {
    local service_name=$1
    local url=$2
    local max_attempts=${3:-30}
    local delay=${4:-2}

    echo -e "\e[90m -> Attente de $service_name...\e[0m"
    for i in $(seq 1 $max_attempts); do
        if curl -sf --max-time 3 "$url" > /dev/null 2>&1; then
            echo -e "\e[32m -> $service_name est prêt ! ($i tentative(s))\e[0m"
            return 0
        fi
        sleep $delay
    done
    echo -e "\e[33m -> ATTENTION: $service_name n'a pas répondu après $((max_attempts * delay))s\e[0m"
    return 1
}

# --- Étape 1 : Création du réseau + Infrastructure partagée ---
echo -e "\n\e[33m[1/6] Lancement de l'infrastructure partagée...\e[0m"

if ! docker network ls --filter name=^agt_network$ --format "{{.Name}}" | grep -q agt_network; then
    docker network create agt_network > /dev/null
    echo -e "\e[90m -> Réseau agt_network créé.\e[0m"
fi

docker compose -f docker-compose.infra.yml up -d
echo -e "\e[32m -> Infrastructure lancée.\e[0m"

# --- Étape 2 : Simulateurs (Média, Chat, Geoloc) ---
echo -e "\n\e[33m[2/6] Lancement des simulateurs...\e[0m"
for sim in agt-media agt-chat agt-geoloc; do
    if [ -d "$sim" ]; then
        echo -e "\e[90m -> Démarrage de $sim...\e[0m"
        cd "$sim" && docker compose up -d --build && cd ..
    else
        echo -e "\e[33m -> $sim non trouvé, ignoré.\e[0m"
    fi
done

# --- Étape 3 : Auth + Health Check ---
echo -e "\n\e[33m[3/6] Lancement du Service Auth...\e[0m"
cd agt-auth && bash scripts/setup.sh && cd ..

if ! wait_for_health "Auth" "http://localhost:7000/api/v1/auth/health"; then
    echo -e "\n\e[31mDÉPLOIEMENT INTERROMPU : Auth n'a pas démarré.\e[0m"
    exit 1
fi

# --- Étape 4 : Distribution de la clé publique Auth ---
echo -e "\n\e[33m[4/6] Partage de la clé publique Auth vers tous les services...\e[0m"
AUTH_PUB_KEY="agt-auth/keys/public.pem"
TARGET_SERVICES=("agt-users" "agt-notification" "agt-subscription" "agt-payment" "agt-wallet" "agt-search" "agt-chatbot")

if [ -f "$AUTH_PUB_KEY" ]; then
    for service in "${TARGET_SERVICES[@]}"; do
        if [ -d "$service" ]; then
            mkdir -p "$service/keys"
            cp "$AUTH_PUB_KEY" "$service/keys/auth_public.pem"
            echo -e "\e[90m -> Clé copiée vers $service.\e[0m"
        fi
    done
    echo -e "\e[32m -> Toutes les clés distribuées.\e[0m"
else
    echo -e "\e[31m -> ERREUR: Clé publique Auth introuvable !\e[0m"
    exit 1
fi

# --- Étape 5 : Lancement des services métier (dans l'ordre des dépendances) ---
echo -e "\n\e[33m[5/6] Lancement des services métier...\e[0m"
for service in "${TARGET_SERVICES[@]}"; do
    if [ -f "$service/scripts/setup.sh" ]; then
        echo -e "\e[90m -> Démarrage de $service...\e[0m"
        cd "$service" && bash scripts/setup.sh && cd ..
    else
        echo -e "\e[33m -> $service : script setup non trouvé, ignoré.\e[0m"
    fi
done

# --- Étape 6 : Health Checks finaux ---
echo -e "\n\e[33m[6/6] Vérification de santé de tous les services...\e[0m"

ALL_OK=true
wait_for_health "Auth"         "http://localhost:7000/api/v1/auth/health"          15 2 || ALL_OK=false
wait_for_health "Users"        "http://localhost:7001/api/v1/health"               15 2 || ALL_OK=false
wait_for_health "Notification" "http://localhost:7002/api/v1/health"               15 2 || ALL_OK=false
wait_for_health "Subscription" "http://localhost:7004/api/v1/subscriptions/health" 15 2 || ALL_OK=false
wait_for_health "Payment"      "http://localhost:7005/api/v1/payments/health"      15 2 || ALL_OK=false
wait_for_health "Wallet"       "http://localhost:7006/api/v1/wallet/health"        15 2 || ALL_OK=false
wait_for_health "Search"       "http://localhost:7007/api/v1/search/health"        15 2 || ALL_OK=false
wait_for_health "Chatbot"      "http://localhost:7010/api/v1/chatbot/health"       15 2 || ALL_OK=false

# --- Résumé final ---
echo -e "\n\e[36m=========================================\e[0m"
if $ALL_OK; then
    echo -e "\e[32m DÉPLOIEMENT COMPLET RÉUSSI !            \e[0m"
else
    echo -e "\e[33m DÉPLOIEMENT PARTIEL (certains services KO)\e[0m"
fi
echo -e "\e[36m=========================================\e[0m"
echo ""
echo -e "\e[90m Vérifiez l'état : docker ps\e[0m"
echo -e "\e[90m Reset soft       : bash reset_all.sh\e[0m"
echo -e "\e[90m Reset complet    : bash reset_all.sh --clean\e[0m"
echo -e "\e[36m=========================================\e[0m"