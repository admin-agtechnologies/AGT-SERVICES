#!/bin/bash
# =============================================================================
# AG TECHNOLOGIES — DÉPLOIEMENT MVP (Linux / macOS)
#
# Lance les 3 services socles + l'infrastructure partagée dans le bon ordre.
#
# Services  : Auth (7000) · Users (7001) · Notification (7002)
# Infra     : Gateway (80) · RabbitMQ (5672/15672) · Mailpit (8025)
#
# Ordre de démarrage (respecte les dépendances) :
#   1. Réseau agt_network
#   2. Infrastructure partagée
#   3. Auth  (service socle — tous les autres dépendent de lui)
#   4. Copie clé publique RSA Auth → Users, Notification
#      (Users et Notification valident les JWT Auth avec cette clé)
#   5. Users + Notification
#   6. Migrations Django (makemigrations + migrate)
#   7. Health checks finaux
#
# Usage : bash deploy_mvp.sh
# =============================================================================

set -e  # Arrête le script immédiatement si une commande échoue

# --- Couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
WHITE='\033[1;37m'
NC='\033[0m'

# =============================================================================
# FONCTION : attendre qu'un service réponde sur son endpoint /health
#
# Pourquoi cette fonction est nécessaire ?
# Docker démarre un container en quelques secondes, mais l'application à
# l'intérieur (Django + PostgreSQL) prend 20-40s à être prête. Sans cette
# attente, on lancerait le service suivant avant que le précédent soit opérationnel.
#
# Paramètres :
#   $1 = nom affiché (ex: "Auth")
#   $2 = URL health (ex: "http://localhost:7000/api/v1/auth/health")
#   $3 = nb max de tentatives (défaut: 40)
#   $4 = délai entre tentatives en secondes (défaut: 3)
# =============================================================================
wait_for_health() {
    local service_name=$1
    local url=$2
    local max_attempts=${3:-40}
    local delay=${4:-3}

    echo -e "${GRAY} -> Attente de $service_name (max $((max_attempts * delay))s)...${NC}"
    for i in $(seq 1 $max_attempts); do
        if curl -sf --max-time 3 "$url" > /dev/null 2>&1; then
            echo -e "${GREEN} -> $service_name est prêt ! (${i}x${delay}s)${NC}"
            return 0
        fi
        sleep $delay
    done
    echo -e "${RED} -> ERREUR : $service_name n'a pas répondu après $((max_attempts * delay))s${NC}"
    echo -e "${YELLOW}    Commande de diagnostic : docker logs <nom_du_container>${NC}"
    return 1
}

# =============================================================================
# FONCTION : exécuter les migrations Django d'un service
#
# Deux étapes obligatoires à chaque déploiement sur base vide :
#   makemigrations <apps>  → Django inspecte les modèles et génère les fichiers
#                            de migration (.py) décrivant les changements de schema
#   migrate                → Django lit ces fichiers et exécute les ALTER/CREATE
#                            TABLE correspondants en base PostgreSQL
#
# Sans makemigrations : les fichiers de migration n'existent pas dans le container
# Sans migrate         : les tables n'existent pas → erreur "relation does not exist"
#
# Paramètres :
#   $1 = nom du container (ex: "agt-auth-service")
#   $2 = apps à migrer (ex: "authentication platforms")
# =============================================================================
run_migrations() {
    local container=$1
    local apps=$2
    local service_label=$3

    echo -e "${GRAY} -> Migrations $service_label : makemigrations...${NC}"
    # shellcheck disable=SC2086
    docker exec "$container" python manage.py makemigrations $apps --noinput 2>/dev/null || true

    echo -e "${GRAY} -> Migrations $service_label : migrate...${NC}"
    docker exec "$container" python manage.py migrate --noinput

    echo -e "${GREEN} -> Migrations $service_label appliquées.${NC}"
}

# =============================================================================
# EN-TÊTE
# =============================================================================
echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN} DÉPLOIEMENT MVP - AG TECHNOLOGIES       ${NC}"
echo -e "${CYAN} Auth · Users · Notification             ${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# Vérification : on doit être à la racine du projet
if [ ! -f "docker-compose.infra.yml" ]; then
    echo -e "${RED}ERREUR : Ce script doit être lancé depuis la racine du projet AGT-SERVICES.${NC}"
    echo -e "${GRAY}         cd ~/Documents/projet/AGT/AGT-SERVICES && bash deploy_mvp.sh${NC}"
    exit 1
fi

# =============================================================================
# [1/6] RÉSEAU + INFRASTRUCTURE PARTAGÉE
#
# Le réseau agt_network est déclaré "external: true" dans tous les services.
# Il doit exister AVANT de démarrer quoi que ce soit, sinon Docker Compose
# refuse de créer les containers qui en dépendent.
# =============================================================================
echo -e "${YELLOW}[1/6] Réseau et infrastructure partagée...${NC}"

# Créer le réseau s'il n'existe pas (idempotent : pas d'erreur s'il existe déjà)
if ! docker network ls --format "{{.Name}}" | grep -q "^agt_network$"; then
    docker network create agt_network > /dev/null
    echo -e "${GRAY} -> Réseau agt_network créé.${NC}"
else
    echo -e "${GRAY} -> Réseau agt_network déjà présent.${NC}"
fi

docker compose -f docker-compose.infra.yml up -d --remove-orphans
echo -e "${GREEN} -> Infrastructure lancée (Gateway, RabbitMQ, Mailpit).${NC}"

# =============================================================================
# [2/6] SERVICE AUTH
#
# Auth est le service socle. Tous les autres services :
#   - valident leurs JWT avec la clé publique RSA d'Auth
#   - appellent Auth en S2S pour des opérations d'identité
# Il DOIT être opérationnel avant de lancer quoi que ce soit d'autre.
#
# setup.sh fait : copie .env.example → .env si absent + docker compose up --build
# =============================================================================
echo ""
echo -e "${YELLOW}[2/6] Service Auth...${NC}"

if [ ! -f "agt-auth/scripts/setup.sh" ]; then
    echo -e "${RED}ERREUR : agt-auth/scripts/setup.sh introuvable.${NC}"
    exit 1
fi

cd agt-auth && bash scripts/setup.sh && cd ..

# Fail-fast : si Auth ne démarre pas, inutile de continuer
if ! wait_for_health "Auth" "http://localhost:7000/api/v1/auth/health"; then
    echo ""
    echo -e "${RED}DÉPLOIEMENT INTERROMPU : Auth n'a pas démarré.${NC}"
    echo -e "${YELLOW}Diagnostic : docker logs agt-auth-service${NC}"
    exit 1
fi

# =============================================================================
# [3/6] DISTRIBUTION DE LA CLÉ PUBLIQUE RSA AUTH
#
# Auth utilise un chiffrement asymétrique RS256 pour ses JWT :
#   - clé PRIVÉE (agt-auth/keys/private.pem) : Auth signe les tokens → secret absolu
#   - clé PUBLIQUE (agt-auth/keys/public.pem) : les autres services vérifient les tokens
#
# Sans cette clé, Users et Notification ne peuvent pas valider les JWT entrants
# et rejetteront toutes les requêtes avec une erreur 401.
#
# On copie UNIQUEMENT la clé publique (jamais la privée).
# =============================================================================
echo ""
echo -e "${YELLOW}[3/6] Distribution de la clé publique RSA Auth...${NC}"

AUTH_PUB_KEY="agt-auth/keys/public.pem"

if [ ! -f "$AUTH_PUB_KEY" ]; then
    echo -e "${RED}ERREUR : Clé publique Auth introuvable ($AUTH_PUB_KEY).${NC}"
    echo -e "${YELLOW}Auth a peut-être échoué à générer ses clés. Vérifiez : docker logs agt-auth-service${NC}"
    exit 1
fi

for service in "agt-users" "agt-notification"; do
    mkdir -p "$service/keys"
    cp "$AUTH_PUB_KEY" "$service/keys/auth_public.pem"
    echo -e "${GRAY} -> Clé copiée vers $service/keys/auth_public.pem${NC}"
done

echo -e "${GREEN} -> Clé publique distribuée.${NC}"

# =============================================================================
# [4/6] SERVICES USERS ET NOTIFICATION
#
# Users dépend uniquement de Auth (pour valider les JWT).
# Notification dépend de Auth + RabbitMQ (pour consommer les events async).
# Les deux peuvent démarrer en parallèle — on les lance l'un après l'autre
# mais sans attendre entre les deux (setup.sh est non-bloquant).
# =============================================================================
echo ""
echo -e "${YELLOW}[4/6] Services Users et Notification...${NC}"

for service in "agt-users" "agt-notification"; do
    if [ ! -f "$service/scripts/setup.sh" ]; then
        echo -e "${RED}ERREUR : $service/scripts/setup.sh introuvable.${NC}"
        exit 1
    fi
    echo -e "${GRAY} -> Démarrage de $service...${NC}"
    cd "$service" && bash scripts/setup.sh && cd ..
done

# Attendre que les deux services soient prêts
if ! wait_for_health "Users" "http://localhost:7001/api/v1/health"; then
    echo -e "${RED}DÉPLOIEMENT INTERROMPU : Users n'a pas démarré.${NC}"
    echo -e "${YELLOW}Diagnostic : docker logs agt-users-service${NC}"
    exit 1
fi

if ! wait_for_health "Notification" "http://localhost:7002/api/v1/health"; then
    echo -e "${RED}DÉPLOIEMENT INTERROMPU : Notification n'a pas démarré.${NC}"
    echo -e "${YELLOW}Diagnostic : docker logs agt-notif-service${NC}"
    exit 1
fi

# =============================================================================
# [5/6] MIGRATIONS DJANGO
#
# Cette étape est OBLIGATOIRE sur toute base vide (premier lancement ou --clean).
# Elle est idempotente : si les migrations sont déjà appliquées, Django détecte
# qu'il n'y a rien à faire et passe sans erreur.
#
# Ordre important : Auth en premier car Users et Notification référencent
# potentiellement des données Auth (ex: auth_user_id).
# =============================================================================
echo ""
echo -e "${YELLOW}[5/6] Migrations des bases de données...${NC}"

# Auth — apps : authentication (JWT, sessions, users) + platforms (S2S)
run_migrations "agt-auth-service" "authentication platforms" "Auth"

# Users — apps : users (profils) + roles (RBAC) + documents (pièces jointes)
run_migrations "agt-users-service" "users roles documents" "Users"

# Notification — apps : notifications + templates_mgr + campaigns + devices
run_migrations "agt-notif-service" "notifications templates_mgr campaigns devices" "Notification"

# =============================================================================
# [6/6] HEALTH CHECKS FINAUX
#
# On revérifie les 3 services après les migrations pour s'assurer que
# les migrations n'ont pas causé de redémarrage ou d'erreur inattendue.
# =============================================================================
echo ""
echo -e "${YELLOW}[6/6] Vérification finale de santé...${NC}"

AUTH_OK=0
USERS_OK=0
NOTIF_OK=0

wait_for_health "Auth"         "http://localhost:7000/api/v1/auth/health" 10 2 && AUTH_OK=1 || true
wait_for_health "Users"        "http://localhost:7001/api/v1/health"      10 2 && USERS_OK=1 || true
wait_for_health "Notification" "http://localhost:7002/api/v1/health"      10 2 && NOTIF_OK=1 || true

# =============================================================================
# RÉSUMÉ FINAL
# =============================================================================
echo ""
echo -e "${CYAN}=========================================${NC}"

if [ $AUTH_OK -eq 1 ] && [ $USERS_OK -eq 1 ] && [ $NOTIF_OK -eq 1 ]; then
    echo -e "${GREEN} DÉPLOIEMENT MVP RÉUSSI !                ${NC}"
else
    echo -e "${YELLOW} DÉPLOIEMENT MVP PARTIEL                 ${NC}"
    [ $AUTH_OK -eq 0 ]  && echo -e "${RED}   ✗ Auth         KO${NC}"
    [ $USERS_OK -eq 0 ] && echo -e "${RED}   ✗ Users        KO${NC}"
    [ $NOTIF_OK -eq 0 ] && echo -e "${RED}   ✗ Notification KO${NC}"
fi

echo -e "${CYAN}=========================================${NC}"
echo ""
echo -e "${WHITE} Services :${NC}"
echo -e "${GRAY}   Auth         : http://localhost:7000/api/v1/docs/${NC}"
echo -e "${GRAY}   Users        : http://localhost:7001/api/v1/docs/${NC}"
echo -e "${GRAY}   Notification : http://localhost:7002/api/v1/docs/${NC}"
echo ""
echo -e "${WHITE} Outils :${NC}"
echo -e "${GRAY}   Mailpit   : http://localhost:8025${NC}"
echo -e "${GRAY}   RabbitMQ  : http://localhost:15672  (agt_rabbit / agt_rabbit_password)${NC}"
echo ""
echo -e "${WHITE} Commandes utiles :${NC}"
echo -e "${GRAY}   docker ps                      → état des containers${NC}"
echo -e "${GRAY}   docker logs agt-auth-service   → logs d'un service${NC}"
echo -e "${GRAY}   bash reset_mvp.sh              → reset soft (données conservées)${NC}"
echo -e "${GRAY}   bash reset_mvp.sh --clean      → reset complet (base vide)${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""


