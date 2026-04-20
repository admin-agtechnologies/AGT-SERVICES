#!/bin/bash
# =============================================================================
# AG TECHNOLOGIES — RESET MVP (Linux / macOS)
#
# Arrête proprement les 3 services du MVP + l'infrastructure partagée.
# Utilise "docker compose down" qui est la seule approche fiable : Docker
# Compose sait exactement quels containers il a créés, sans dépendre des noms.
#
# Usage :
#   bash reset_mvp.sh           → reset soft  (containers supprimés, données conservées)
#   bash reset_mvp.sh --clean   → reset clean (containers + volumes supprimés = base vide)
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
echo -e "${CYAN} RESET MVP - AG TECHNOLOGIES             ${NC}"
if $CLEAN; then
    echo -e "${RED} MODE : CLEAN  (volumes supprimés)       ${NC}"
    echo -e "${RED} Les données en base seront effacées !   ${NC}"
else
    echo -e "${GREEN} MODE : SOFT   (données conservées)      ${NC}"
fi
echo -e "${CYAN}=========================================${NC}"
echo ""

# --- Confirmation si --clean (sécurité) ---
# Le mode clean supprime les bases de données. On demande confirmation.
if $CLEAN; then
    read -p "Confirmer la suppression de toutes les données MVP ? (oui/non) : " confirm
    if [ "$confirm" != "oui" ]; then
        echo ""
        echo -e "${YELLOW} -> Annulé. Aucune modification effectuée.${NC}"
        exit 0
    fi
    echo ""
    DOWN_FLAGS="down -v"   # -v = supprime les volumes Docker (données DB)
else
    DOWN_FLAGS="down"      # sans -v = containers supprimés, volumes intacts
fi

# =============================================================================
# [1/4] Arrêt des services métier MVP
# Ordre inversé du démarrage : Notification → Users → Auth
# (bonne pratique même si ça ne change rien fonctionnellement ici)
# =============================================================================
echo -e "${CYAN}[1/4] Arrêt des services métier MVP...${NC}"

for service in "agt-notification" "agt-users" "agt-auth"; do
    if [ -f "./$service/docker-compose.yml" ]; then
        echo -e "${GRAY} -> Arrêt de $service...${NC}"
        # shellcheck disable=SC2086
        docker compose -f "./$service/docker-compose.yml" $DOWN_FLAGS --remove-orphans 2>/dev/null
    else
        echo -e "${GRAY} -> $service/docker-compose.yml introuvable, ignoré.${NC}"
    fi
done

echo -e "${GREEN} -> Services MVP arrêtés.${NC}"

# =============================================================================
# [2/4] Arrêt de l'infrastructure partagée
# Gateway, RabbitMQ, Mailpit
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
#
# Pourquoi on le supprime manuellement ?
# Le réseau agt_network est déclaré "external: true" dans chaque docker-compose.yml,
# ce qui signifie que Docker Compose NE le supprime PAS avec "down".
# C'est voulu : le réseau est partagé entre plusieurs services, donc aucun
# service individuel ne doit le supprimer. On doit le faire nous-mêmes ici.
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
# [4/4] Suppression des fichiers .env MVP
#
# Les .env sont générés par setup.sh depuis .env.example.
# On les supprime pour que le prochain déploiement parte d'un état propre,
# notamment si des variables ont changé dans .env.example.
# =============================================================================
echo ""
echo -e "${CYAN}[4/4] Nettoyage des fichiers .env MVP...${NC}"

env_count=0
for service in "agt-auth" "agt-users" "agt-notification"; do
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
echo -e "${GREEN} RESET MVP TERMINÉ                       ${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# Vérification : afficher les containers AGT encore actifs (ne devrait rien montrer)
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
    echo -e "${GRAY} Données supprimées. Pour relancer depuis zéro :${NC}"
else
    echo -e "${GRAY} Données conservées. Pour relancer le MVP :${NC}"
fi
echo -e "${GRAY}   bash deploy_mvp.sh${NC}"
echo ""