#!/bin/bash
set -e
echo "AGT Subscription Service v1.0 - Setup"
echo "======================================="
if [ ! -f .env ]; then cp .env.example .env; echo "[OK] .env cree"; fi
if [ ! -f keys/auth_public.pem ]; then
    mkdir -p keys
    [ -f ../agt-auth/keys/public.pem ] && cp ../agt-auth/keys/public.pem keys/auth_public.pem && echo "[OK] Cle Auth copiee" || echo "[WARN] Cle Auth introuvable"
fi
echo "Build et demarrage Docker..."
docker compose up -d --build
sleep 8
echo "Migrations..."
docker compose exec subscription python manage.py migrate --noinput
echo ""
curl -s http://localhost:7004/api/v1/subscriptions/health | python3 -m json.tool 2>/dev/null || echo "Service en cours de demarrage..."
echo ""
echo "[OK] Subscription Service pret sur http://localhost:7004"
echo "  Swagger : http://localhost:7004/api/v1/docs/"
echo "  Tests   : docker compose exec subscription python -m pytest -v"
