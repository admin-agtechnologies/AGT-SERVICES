#!/bin/bash
# =============================================================================
# AG TECHNOLOGIES — RESET ALL (Linux / macOS)
#
# Arrête proprement les 11 services de l'écosystème + l'infrastructure.
# Même logique que reset_mvp.sh, étendue à tous les services.
#
# Usage :
#   bash reset_all.sh           → reset soft  (containers supprimés, données conservées)
#   bash reset_all.sh --clean   → reset clean (containers + volumes supprimés = base vide)
# =============================================================================

# --- Lecture du flag --clean ---
CLEAN=false
if [[ "$1" == "--clean" ]]; then CLEAN=true; fi

# --- Couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m'

# --- En-tête ---
echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN} RESET ALL - AG TECHNOLOGIES             ${NC}"
if $CLEAN; then
    echo -e "${RED} MODE : CLEAN  (volumes supprimés)       ${NC}"
    echo -e "${RED} TOUTES les données seront effacées !    ${NC}"
else
    echo -e "${GREEN} MODE : SOFT   (données conservées)      ${NC}"
fi
echo -e "${CYAN}=========================================${NC}"
echo ""

# --- Confirmation si --clean (sécurité) ---
if $CLEAN; then
    read -p "Confirmer la suppression de TOUTES les données (11 services) ? (oui/non) : " confirm
    if [ "$confirm" != "oui" ]; then
        echo ""
        echo -e "${YELLOW} -> Annulé. Aucune modification effectuée.${NC}"
        exit 0
    fi
    echo ""
    DOWN_FLAGS="down -v"
else
    DOWN_FLAGS="down"
fi

# =============================================================================
# [1/4] Arrêt de tous les services métier
#
# Ordre inversé du démarrage (dépendances d'abord) :
# Chatbot, Search, Wallet, Payment, Subscription → puis Notification, Users, Auth
# Les simulateurs (Media, Chat, Geoloc) n'ont pas de dépendances.
# =============================================================================
echo -e "${CYAN}[1/4] Arrêt de tous les services métier...${NC}"

ALL_SERVICES=(
    "agt-chatbot"       # dépend de Auth, Users, Notification
    "agt-search"        # dépend de Auth
    "agt-wallet"        # dépend de Auth, Payment
    "agt-payment"       # dépend de Auth, Subscription
    "agt-subscription"  # dépend de Auth, Users
    "agt-notification"  # dépend de Auth
    "agt-users"         # dépend de Auth
    "agt-auth"          # service socle
    "agt-media"         # simulateur / service NestJS
    "agt-chat"          # simulateur / service NestJS
    "agt-geoloc"        # simulateur (sera remplacé par agt-geoloc_ok)
)

for service in "${ALL_SERVICES[@]}"; do
    if [ -f "./$service/docker-compose.yml" ]; then
        echo -e "${GRAY} -> Arrêt de $service...${NC}"
        # shellcheck disable=SC2086
        docker compose -f "./$service/docker-compose.yml" $DOWN_FLAGS --remove-orphans 2>/dev/null
    else
        echo -e "${GRAY} -> $service/docker-compose.yml introuvable, ignoré.${NC}"
    fi
done

echo -e "${GREEN} -> Tous les services arrêtés.${NC}"

# =============================================================================
# [2/4] Arrêt de l'infrastructure partagée
# =============================================================================
echo ""
echo -e "${CYAN}[2/4] Arrêt de l'infrastructure partagée...${NC}"

if [ -f "./docker-compose.infra.yml" ]; then
    echo -e "${GRAY} -> Arrêt de gateway, rabbitmq, mailpit...${NC}"
    # shellcheck disable=SC2086
    docker compose -f docker-compose.infra.yml $DOWN_FLAGS --remove-orphans 2>/dev/null
    echo -e "${GREEN} -> Infrastructure arrêtée.${NC}"
else
    echo -e "${GRAY} -> docker-compose.infra.yml introuvable, ignoré.${NC}"
fi

# =============================================================================
# [3/4] Suppression du réseau partagé agt_network
# (déclaré "external: true" → non géré par docker compose down)
# =============================================================================
echo ""
echo -e "${CYAN}[3/4] Suppression du réseau agt_network...${NC}"

if docker network ls --format "{{.Name}}" 2>/dev/null | grep -q "^agt_network$"; then
    docker network rm agt_network 2>/dev/null
    echo -e "${GREEN} -> Réseau agt_network supprimé.${NC}"
else
    echo -e "${GRAY} -> Réseau agt_network déjà absent.${NC}"
fi

# =============================================================================
# [4/4] Suppression des fichiers .env de tous les services
# =============================================================================
echo ""
echo -e "${CYAN}[4/4] Nettoyage des fichiers .env...${NC}"

ENV_SERVICES=(
    "agt-auth" "agt-users" "agt-notification"
    "agt-subscription" "agt-payment" "agt-wallet"
    "agt-search" "agt-chatbot" "agt-media"
    "agt-chat" "agt-geoloc"
)

env_count=0
for service in "${ENV_SERVICES[@]}"; do
    if [ -f "./$service/.env" ]; then
        rm -f "./$service/.env"
        echo -e "${GRAY} -> $service/.env supprimé.${NC}"
        ((env_count++))
    fi
done

if [ "$env_count" -eq 0 ]; then
    echo -e "${GRAY} -> Aucun fichier .env trouvé (déjà propre).${NC}"
else
    echo -e "${GREEN} -> $env_count fichier(s) .env supprimé(s).${NC}"
fi

# =============================================================================
# RÉSUMÉ FINAL
# =============================================================================
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN} RESET ALL TERMINÉ                       ${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

remaining=$(docker ps --format "{{.Names}}" 2>/dev/null | grep "^agt")
if [ -n "$remaining" ]; then
    echo -e "${YELLOW} /!\ Containers AGT encore actifs :${NC}"
    while IFS= read -r c; do
        echo -e "${YELLOW}     - $c${NC}"
    done <<< "$remaining"
else
    echo -e "${GREEN} -> Aucun container AGT actif. Tout est propre.${NC}"
fi

echo ""
if $CLEAN; then
    echo -e "${GRAY} Toutes les données supprimées. Pour relancer :${NC}"
else
    echo -e "${GRAY} Données conservées. Pour relancer :${NC}"
fi
echo -e "${GRAY}   bash deploy_mvp.sh    → MVP uniquement${NC}"
echo -e "${GRAY}   bash deploy_all.sh    → Tous les services${NC}"
echo ""