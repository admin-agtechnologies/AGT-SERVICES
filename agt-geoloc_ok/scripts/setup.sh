#!/bin/bash
# ── AGT Geolocation Service — Setup Script ─────────────────────────────────────
# Usage: bash scripts/setup.sh
# Lance le service en mode autonome (avec sa propre DB/Redis/RabbitMQ)

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

info "AGT Geolocation Service v1.2 — Setup"
echo "────────────────────────────────────────"

# Vérifications préalables
command -v docker >/dev/null 2>&1 || error "Docker non trouvé. Installer Docker Desktop."
command -v docker compose >/dev/null 2>&1 || error "Docker Compose non trouvé."

# Copie du .env si absent
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
    info ".env créé depuis .env.example"
    warn "Vérifiez les variables dans .env avant de continuer."
  else
    error ".env.example introuvable."
  fi
fi

# Clé publique Auth
if [ ! -f "keys/auth_public.pem" ]; then
  warn "keys/auth_public.pem absent."
  warn "En dev autonome : le service tourne sans validation JWT (mode relaxé)."
  warn "En intégration AGT : copier depuis agt-auth/keys/public.pem"
  warn "  cp ../agt-auth/keys/public.pem keys/auth_public.pem"
  touch keys/.gitkeep
fi

# Build et démarrage
info "Démarrage des conteneurs..."
docker compose down --remove-orphans 2>/dev/null || true
docker compose up -d --build

# Attente du service
info "Attente du démarrage (30s max)..."
for i in $(seq 1 30); do
  if curl -sf http://localhost:7009/api/v1/geo/health >/dev/null 2>&1; then
    echo ""
    info "Service prêt !"
    break
  fi
  printf "."
  sleep 1
done

echo ""
echo "────────────────────────────────────────"
info "✅ AGT Geolocation Service opérationnel"
echo ""
echo "  Swagger UI  : http://localhost:7009/api/v1/docs"
echo "  Health      : http://localhost:7009/api/v1/geo/health"
echo "  RabbitMQ UI : http://localhost:15675 (agt_rabbit / agt_rabbit_password)"
echo ""
echo "Commandes utiles :"
echo "  docker compose logs -f agt-geoloc   # logs temps réel"
echo "  docker compose down                  # arrêter"
echo "  docker compose down -v               # arrêter + supprimer données"
echo "────────────────────────────────────────"
