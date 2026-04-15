#!/bin/bash

# =========================================
#  STOP & CLEAN - AG TECHNOLOGIES
#  Arrete et supprime TOUT sans redéployer
#  Usage : ./stop_clean.sh
# =========================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo ""
echo -e "${RED}=========================================${NC}"
echo -e "${RED} STOP & CLEAN - AG TECHNOLOGIES          ${NC}"
echo -e "${RED} TOUS les services seront arretes et     ${NC}"
echo -e "${RED} supprimes (containers, volumes, reseau) ${NC}"
echo -e "${RED}=========================================${NC}"
echo ""

# --- Confirmation interactive ---
read -p "Es-tu sur de vouloir tout supprimer ? (oui/non) : " confirm
if [ "$confirm" != "oui" ]; then
    echo ""
    echo -e "${YELLOW} -> Annule. Aucune modification effectuee.${NC}"
    exit 0
fi

echo ""

# =========================================
# LISTE DE TOUS LES SERVICES AGT
# =========================================

SERVICES=(
    "agt-auth"
    "agt-users"
    "agt-notification"
    "agt-subscription"
    "agt-payment"
    "agt-wallet"
    "agt-search"
    "agt-chatbot"
    "agt-chat"
    "agt-media"
    "agt-geoloc"
)

# =========================================
# [1/5] ARRET ET SUPPRESSION DES SERVICES
# =========================================

echo -e "${CYAN}[1/5] Arret des services AGT...${NC}"

for svc in "${SERVICES[@]}"; do
    compose_path="./$svc/docker-compose.yml"
    if [ -f "$compose_path" ]; then
        echo -e "${GRAY} -> Arret de $svc...${NC}"
        docker compose -f "$compose_path" down --remove-orphans 2>/dev/null
    fi
done

# =========================================
# [2/5] ARRET DE L'INFRASTRUCTURE PARTAGEE
# =========================================

echo ""
echo -e "${CYAN}[2/5] Arret de l'infrastructure partagee...${NC}"

if [ -f "./docker-compose.infra.yml" ]; then
    echo -e "${GRAY} -> Arret de gateway, rabbitmq, elasticsearch, mailpit...${NC}"
    docker compose -f docker-compose.infra.yml down --remove-orphans 2>/dev/null
fi

# =========================================
# [3/5] SUPPRESSION DES VOLUMES AGT
# =========================================

echo ""
echo -e "${CYAN}[3/5] Suppression des volumes AGT...${NC}"

volumes=$(docker volume ls --format "{{.Name}}" 2>/dev/null | grep "^agt")

if [ -n "$volumes" ]; then
    count=0
    while IFS= read -r vol; do
        echo -e "${GRAY} -> Suppression volume : $vol${NC}"
        docker volume rm "$vol" 2>/dev/null
        ((count++))
    done <<< "$volumes"
    echo -e "${GREEN} -> $count volume(s) supprime(s).${NC}"
else
    echo -e "${GRAY} -> Aucun volume AGT trouve.${NC}"
fi

# =========================================
# [4/5] SUPPRESSION DU RESEAU AGT
# =========================================

echo ""
echo -e "${CYAN}[4/5] Suppression du reseau agt_network...${NC}"

if docker network ls --format "{{.Name}}" 2>/dev/null | grep -q "^agt_network$"; then
    docker network rm agt_network 2>/dev/null
    echo -e "${GREEN} -> Reseau agt_network supprime.${NC}"
else
    echo -e "${GRAY} -> Reseau agt_network introuvable (deja supprime).${NC}"
fi

# =========================================
# [5/5] SUPPRESSION DES FICHIERS .env
# =========================================

echo ""
echo -e "${CYAN}[5/5] Suppression des fichiers .env...${NC}"

env_count=0
for svc in "${SERVICES[@]}"; do
    env_path="./$svc/.env"
    if [ -f "$env_path" ]; then
        rm -f "$env_path"
        echo -e "${GRAY} -> $svc/.env supprime.${NC}"
        ((env_count++))
    fi
done

if [ "$env_count" -eq 0 ]; then
    echo -e "${GRAY} -> Aucun fichier .env trouve.${NC}"
else
    echo -e "${GREEN} -> $env_count fichier(s) .env supprime(s).${NC}"
fi

# =========================================
# VERIFICATION FINALE
# =========================================

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN} NETTOYAGE TERMINE                       ${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${WHITE} Verification - containers actifs :${NC}"
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
docker ps
echo ""
echo -e "${CYAN} Pour relancer le MVP :${NC}"
echo -e "${WHITE}   ./deploy_mvp.sh${NC}"
echo ""
echo -e "${CYAN} Pour relancer tous les services :${NC}"
echo -e "${WHITE}   ./deploy_all.sh${NC}"
echo ""