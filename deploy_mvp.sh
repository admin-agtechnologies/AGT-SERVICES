#!/bin/bash
# =============================================================================
# AG TECHNOLOGIES — DÉPLOIEMENT MVP (Linux / macOS)
# Services : Auth (7000) + Users (7001) + Notification (7002)
# Infra    : Gateway, RabbitMQ, Mailpit, Elasticsearch
# =============================================================================

echo -e "\e[36m=========================================\e[0m"
echo -e "\e[36m DÉPLOIEMENT MVP - AG TECHNOLOGIES       \e[0m"
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
    echo -e "\e[31m -> ERREUR: $service_name n'a pas répondu après $((max_attempts * delay))s !\e[0m"
    echo -e "\e[31m   Vérifiez les logs : docker logs <container_name>\e[0m"
    return 1
}

# --- Étape 1 : Création du réseau + Infrastructure partagée ---
echo -e "\n\e[33m[1/4] Lancement de l'infrastructure partagée...\e[0m"

# Créer le réseau s'il n'existe pas
if ! docker network ls --filter name=^agt_network$ --format "{{.Name}}" | grep -q agt_network; then
    docker network create agt_network > /dev/null
    echo -e "\e[90m -> Réseau agt_network créé.\e[0m"
fi

docker compose -f docker-compose.infra.yml up -d
echo -e "\e[32m -> Infrastructure lancée (Gateway, RabbitMQ, Mailpit, Elasticsearch).\e[0m"

# --- Étape 2 : Lancement de Auth + Health Check ---
echo -e "\n\e[33m[2/4] Lancement du Service Auth...\e[0m"
cd agt-auth && bash scripts/setup.sh && cd ..

if ! wait_for_health "Auth" "http://localhost:7000/api/v1/auth/health"; then
    echo -e "\n\e[31mDÉPLOIEMENT INTERROMPU : Auth n'a pas démarré.\e[0m"
    exit 1
fi

# --- Étape 3 : Copie de la clé publique Auth ---
echo -e "\n\e[33m[3/4] Partage de la clé publique Auth...\e[0m"
AUTH_PUB_KEY="agt-auth/keys/public.pem"
if [ -f "$AUTH_PUB_KEY" ]; then
    mkdir -p agt-users/keys agt-notification/keys
    cp "$AUTH_PUB_KEY" agt-users/keys/auth_public.pem
    echo -e "\e[90m -> Clé copiée vers agt-users.\e[0m"
    cp "$AUTH_PUB_KEY" agt-notification/keys/auth_public.pem
    echo -e "\e[90m -> Clé copiée vers agt-notification.\e[0m"
    echo -e "\e[32m -> Clés distribuées avec succès.\e[0m"
else
    echo -e "\e[31m -> ERREUR: Clé publique Auth introuvable ($AUTH_PUB_KEY) !\e[0m"
    exit 1
fi

# --- Étape 4 : Lancement de Users + Notification + Health Checks ---
echo -e "\n\e[33m[4/4] Lancement des Services Users et Notification...\e[0m"
cd agt-users && bash scripts/setup.sh && cd ..
cd agt-notification && bash scripts/setup.sh && cd ..

wait_for_health "Users" "http://localhost:7001/api/v1/health"
USERS_OK=$?
wait_for_health "Notification" "http://localhost:7002/api/v1/health"
NOTIF_OK=$?

# --- Résumé final ---
echo -e "\n\e[36m=========================================\e[0m"
if [ $USERS_OK -eq 0 ] && [ $NOTIF_OK -eq 0 ]; then
    echo -e "\e[32m DÉPLOIEMENT MVP RÉUSSI !                \e[0m"
else
    echo -e "\e[33m DÉPLOIEMENT MVP PARTIEL (erreurs)       \e[0m"
fi
echo -e "\e[36m=========================================\e[0m"
echo ""
echo -e " Services :"
echo -e "\e[90m   Auth         : http://localhost:7000/api/v1/docs/\e[0m"
echo -e "\e[90m   Users        : http://localhost:7001/api/v1/docs/\e[0m"
echo -e "\e[90m   Notification : http://localhost:7002/api/v1/docs/\e[0m"
echo ""
echo -e " Outils :"
echo -e "\e[90m   Mailpit      : http://localhost:8025\e[0m"
echo -e "\e[90m   RabbitMQ     : http://localhost:15672 (agt_rabbit / agt_rabbit_password)\e[0m"
echo ""
echo -e " Commandes utiles :"
echo -e "\e[90m   docker ps                    → voir les conteneurs\e[0m"
echo -e "\e[90m   bash reset_mvp.sh            → reset soft (garde les données)\e[0m"
echo -e "\e[90m   bash reset_mvp.sh --clean    → reset complet (supprime tout)\e[0m"
echo -e "\e[36m=========================================\e[0m"