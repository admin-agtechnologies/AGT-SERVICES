#!/bin/bash
# =============================================================================
# AG TECHNOLOGIES — DÉPLOIEMENT COMPLET (Linux / macOS)
#
# Lance les 11 services de l'écosystème dans l'ordre des dépendances.
#
# Ordre de démarrage :
#   1. Réseau + Infrastructure partagée (Gateway, RabbitMQ, Mailpit)
#   2. Auth  (socle — tous les autres dépendent de lui)
#   3. Distribution clé RSA Auth → tous les services
#   4. Users + Notification  (MVP)
#   5. Services métier Python  (Subscription, Payment, Wallet, Search, Chatbot)
#      → Search démarre son propre Elasticsearch (seul service qui en a besoin)
#   6. Services NestJS  (Media, Chat)
#   7. Geoloc
#   8. Migrations Django pour tous les services Python
#   9. Health checks finaux
#
# Usage : bash deploy_all.sh
# =============================================================================

set -e

# --- Couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
WHITE='\033[1;37m'
NC='\033[0m'

# Répertoire racine — mémorisé une fois pour ne jamais le perdre
ROOT_DIR="$(pwd)"

# =============================================================================
# FONCTION : attendre qu'un service réponde sur son endpoint /health
# =============================================================================
wait_for_health() {
    local service_name=$1
    local url=$2
    local max_attempts=${3:-20}
    local delay=${4:-3}

    echo -e "${GRAY} -> Vérification de $service_name...${NC}"
    for i in $(seq 1 $max_attempts); do
        if curl -sf --max-time 3 "$url" > /dev/null 2>&1; then
            echo -e "${GREEN} -> $service_name prêt ! (${i}x${delay}s)${NC}"
            return 0
        fi
        sleep $delay
    done
    echo -e "${YELLOW} -> AVERTISSEMENT : $service_name n'a pas répondu après $((max_attempts * delay))s${NC}"
    return 1
}

# =============================================================================
# FONCTION : migrations Django
# Vérifie d'abord que le container tourne avant d'essayer.
# =============================================================================
run_migrations() {
    local container=$1
    local apps=$2
    local label=$3
    local extra_env=${4:-""}

    echo -e "${GRAY} -> Migrations $label...${NC}"

    if ! docker ps --format "{{.Names}}" | grep -q "^${container}$"; then
        echo -e "${YELLOW}    Container $container absent, migrations ignorées.${NC}"
        return 0
    fi

    if [ -n "$extra_env" ]; then
        # shellcheck disable=SC2086
        docker exec -e $extra_env "$container" python manage.py makemigrations $apps --noinput 2>/dev/null || true
        docker exec -e $extra_env "$container" python manage.py migrate --noinput
    else
        # shellcheck disable=SC2086
        docker exec "$container" python manage.py makemigrations $apps --noinput 2>/dev/null || true
        docker exec "$container" python manage.py migrate --noinput
    fi
    echo -e "${GREEN} -> Migrations $label appliquées.${NC}"
}

# =============================================================================
# FONCTION : lancer un service Python avec setup.sh
# Revient toujours à ROOT_DIR après le lancement.
# =============================================================================
start_python_service() {
    local service_dir=$1
    local label=$2

    if [ ! -f "$ROOT_DIR/$service_dir/scripts/setup.sh" ]; then
        echo -e "${GRAY} -> $label : setup.sh introuvable, ignoré.${NC}"
        return 0
    fi

    echo -e "${GRAY} -> Démarrage de $label...${NC}"
    cd "$ROOT_DIR/$service_dir" && bash scripts/setup.sh
    cd "$ROOT_DIR"
    echo -e "${GREEN} -> $label lancé.${NC}"
}

# =============================================================================
# FONCTION : lancer un service NestJS (pas de setup.sh)
# Revient toujours à ROOT_DIR après le lancement.
# =============================================================================
start_nestjs_service() {
    local service_dir=$1
    local label=$2

    if [ ! -d "$ROOT_DIR/$service_dir" ]; then
        echo -e "${GRAY} -> $label : dossier introuvable, ignoré.${NC}"
        return 0
    fi

    echo -e "${GRAY} -> Démarrage de $label...${NC}"

    if [ ! -f "$ROOT_DIR/$service_dir/.env" ] && [ -f "$ROOT_DIR/$service_dir/.env.example" ]; then
        cp "$ROOT_DIR/$service_dir/.env.example" "$ROOT_DIR/$service_dir/.env"
        echo -e "${GRAY}    -> .env créé depuis .env.example${NC}"
    fi

    cd "$ROOT_DIR/$service_dir" && docker compose up -d --build
    cd "$ROOT_DIR"
    echo -e "${GREEN} -> $label lancé.${NC}"
}

# =============================================================================
# EN-TÊTE
# =============================================================================
echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN} DÉPLOIEMENT COMPLET - AG TECHNOLOGIES   ${NC}"
echo -e "${CYAN} 11 services + infrastructure            ${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# Vérification répertoire
if [ ! -f "docker-compose.infra.yml" ]; then
    echo -e "${RED}ERREUR : Lancez ce script depuis la racine du projet AGT-SERVICES.${NC}"
    exit 1
fi

# =============================================================================
# [1/9] RÉSEAU + INFRASTRUCTURE PARTAGÉE
# Gateway, RabbitMQ, Mailpit
# (Elasticsearch n'est PAS ici — Search gère son propre ES)
# =============================================================================
echo -e "${YELLOW}[1/9] Réseau et infrastructure partagée...${NC}"

if ! docker network ls --format "{{.Name}}" | grep -q "^agt_network$"; then
    docker network create agt_network > /dev/null
    echo -e "${GRAY} -> Réseau agt_network créé.${NC}"
else
    echo -e "${GRAY} -> Réseau agt_network déjà présent.${NC}"
fi

docker compose -f docker-compose.infra.yml up -d --remove-orphans
echo -e "${GREEN} -> Infrastructure lancée (Gateway, RabbitMQ, Mailpit).${NC}"

# =============================================================================
# [2/9] AUTH (socle obligatoire)
# =============================================================================
echo ""
echo -e "${YELLOW}[2/9] Service Auth (socle)...${NC}"

start_python_service "agt-auth" "Auth"

if ! wait_for_health "Auth" "http://localhost:7000/api/v1/auth/health" 40 3; then
    echo -e "${RED}DÉPLOIEMENT INTERROMPU : Auth n'a pas démarré.${NC}"
    echo -e "${YELLOW}Diagnostic : docker logs agt-auth-service${NC}"
    exit 1
fi

# =============================================================================
# [3/9] DISTRIBUTION CLÉ RSA AUTH
# Tous les services valident les JWT avec la clé publique d'Auth.
# =============================================================================
echo ""
echo -e "${YELLOW}[3/9] Distribution de la clé publique RSA Auth...${NC}"

AUTH_PUB_KEY="$ROOT_DIR/agt-auth/keys/public.pem"

if [ ! -f "$AUTH_PUB_KEY" ]; then
    echo -e "${RED}ERREUR : Clé publique Auth introuvable.${NC}"
    exit 1
fi

for service in agt-users agt-notification agt-subscription agt-payment \
               agt-wallet agt-search agt-chatbot agt-media agt-chat agt-geoloc; do
    if [ -d "$ROOT_DIR/$service" ]; then
        mkdir -p "$ROOT_DIR/$service/keys"
        cp "$AUTH_PUB_KEY" "$ROOT_DIR/$service/keys/auth_public.pem"
        echo -e "${GRAY} -> Clé → $service${NC}"
    fi
done

echo -e "${GREEN} -> Clé publique distribuée.${NC}"

# =============================================================================
# [4/9] MVP — USERS + NOTIFICATION
# =============================================================================
echo ""
echo -e "${YELLOW}[4/9] Services MVP (Users + Notification)...${NC}"

start_python_service "agt-users" "Users"
start_python_service "agt-notification" "Notification"

if ! wait_for_health "Users" "http://localhost:7001/api/v1/health" 40 3; then
    echo -e "${RED}DÉPLOIEMENT INTERROMPU : Users n'a pas démarré.${NC}"
    exit 1
fi
if ! wait_for_health "Notification" "http://localhost:7002/api/v1/health" 40 3; then
    echo -e "${RED}DÉPLOIEMENT INTERROMPU : Notification n'a pas démarré.${NC}"
    exit 1
fi

# =============================================================================
# [5/9] SERVICES MÉTIER PYTHON
#
# Chaque setup.sh fait son propre health check interne et attend que
# le service soit prêt avant de rendre la main — pas de wait_for_health
# redondant ici.
#
# Search démarre son propre Elasticsearch (port 9200).
# C'est voulu : seul Search en a besoin dans l'écosystème.
# =============================================================================
echo ""
echo -e "${YELLOW}[5/9] Services métier Python...${NC}"

start_python_service "agt-subscription" "Subscription"
start_python_service "agt-payment"      "Payment"
start_python_service "agt-wallet"       "Wallet"
start_python_service "agt-search"       "Search"
start_python_service "agt-chatbot"      "Chatbot"

# =============================================================================
# [6/9] SERVICES NESTJS (Media, Chat)
# =============================================================================
echo ""
echo -e "${YELLOW}[6/9] Services NestJS (Media, Chat)...${NC}"

start_nestjs_service "agt-media" "Media"
start_nestjs_service "agt-chat"  "Chat"

# =============================================================================
# [7/9] GEOLOC
# =============================================================================
echo ""
echo -e "${YELLOW}[7/9] Service Geoloc...${NC}"

start_nestjs_service "agt-geoloc" "Geoloc"

# =============================================================================
# [8/9] MIGRATIONS DJANGO — TOUS LES SERVICES PYTHON
# Idempotent : si déjà migrés, Django détecte "No changes" et passe.
# =============================================================================
echo ""
echo -e "${YELLOW}[8/9] Migrations des bases de données...${NC}"

run_migrations "agt-auth-service"    "authentication platforms"                      "Auth"
run_migrations "agt-users-service"   "users roles documents"                         "Users"
run_migrations "agt-notif-service"   "notifications templates_mgr campaigns devices" "Notification"
run_migrations "agt-pay-service"     "payments"                                      "Payment"
run_migrations "agt-wallet-service"  "accounts"                                      "Wallet"
run_migrations "agt-search-service"  "indexes"                                       "Search"
run_migrations "agt-chatbot-service" "bots"                                          "Chatbot"

# Subscription : nécessite DJANGO_SETTINGS_MODULE explicite
run_migrations "agt-sub-service" \
    "plans subscriptions quotas organizations" \
    "Subscription" \
    "DJANGO_SETTINGS_MODULE=config.settings"

# =============================================================================
# [9/9] HEALTH CHECKS FINAUX
# =============================================================================
echo ""
echo -e "${YELLOW}[9/9] Vérification finale de santé...${NC}"

declare -A STATUS

check() {
    local label=$1
    local url=$2
    if curl -sf --max-time 3 "$url" > /dev/null 2>&1; then
        STATUS[$label]="✓"
    else
        STATUS[$label]="✗"
    fi
}

check "Auth"         "http://localhost:7000/api/v1/auth/health"
check "Users"        "http://localhost:7001/api/v1/health"
check "Notification" "http://localhost:7002/api/v1/health"
check "Media"        "http://localhost:7003/api/v1/media/health"
check "Subscription" "http://localhost:7004/api/v1/subscriptions/health"
check "Payment"      "http://localhost:7005/api/v1/payments/health"
check "Wallet"       "http://localhost:7006/api/v1/wallet/health"
check "Search"       "http://localhost:7007/api/v1/search/health"
check "Chat"         "http://localhost:7008/api/v1/chat/health"
check "Geoloc"       "http://localhost:7009/api/v1/geo/health"
check "Chatbot"      "http://localhost:7010/api/v1/chatbot/health"

# =============================================================================
# RÉSUMÉ FINAL
# =============================================================================
echo ""
echo -e "${CYAN}=========================================${NC}"

ALL_OK=true
for label in Auth Users Notification Media Subscription Payment Wallet Search Chat Geoloc Chatbot; do
    [ "${STATUS[$label]:-✗}" = "✗" ] && ALL_OK=false && break
done

$ALL_OK \
    && echo -e "${GREEN} DÉPLOIEMENT COMPLET RÉUSSI !           ${NC}" \
    || echo -e "${YELLOW} DÉPLOIEMENT PARTIEL                    ${NC}"

echo -e "${CYAN}=========================================${NC}"
echo ""
echo -e "${WHITE} État des services :${NC}"
for label in Auth Users Notification Media Subscription Payment Wallet Search Chat Geoloc Chatbot; do
    s="${STATUS[$label]:-✗}"
    [ "$s" = "✓" ] \
        && echo -e "${GREEN}   ✓ $label${NC}" \
        || echo -e "${RED}   ✗ $label${NC}"
done

echo ""
echo -e "${WHITE} Interfaces :${NC}"
echo -e "${GRAY}   Auth         : http://localhost:7000/api/v1/docs/${NC}"
echo -e "${GRAY}   Users        : http://localhost:7001/api/v1/docs/${NC}"
echo -e "${GRAY}   Notification : http://localhost:7002/api/v1/docs/${NC}"
echo -e "${GRAY}   Subscription : http://localhost:7004/api/v1/docs/${NC}"
echo -e "${GRAY}   Payment      : http://localhost:7005/api/v1/docs/${NC}"
echo -e "${GRAY}   Wallet       : http://localhost:7006/api/v1/docs/${NC}"
echo -e "${GRAY}   Search       : http://localhost:7007/api/v1/docs/${NC}"
echo -e "${GRAY}   Chatbot      : http://localhost:7010/api/v1/docs/${NC}"
echo ""
echo -e "${WHITE} Outils :${NC}"
echo -e "${GRAY}   Mailpit   : http://localhost:8025${NC}"
echo -e "${GRAY}   RabbitMQ  : http://localhost:15672  (agt_rabbit / agt_rabbit_password)${NC}"
echo ""
echo -e "${WHITE} Commandes utiles :${NC}"
echo -e "${GRAY}   docker ps                  → état des containers${NC}"
echo -e "${GRAY}   bash reset_all.sh          → reset soft${NC}"
echo -e "${GRAY}   bash reset_all.sh --clean  → reset complet${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""