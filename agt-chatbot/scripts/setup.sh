#!/bin/bash
set -e
echo "AGT Chatbot Service v1.0 - Setup"
echo "================================="
if [ ! -f .env ]; then cp .env.example .env; echo "[OK] .env cree"; fi
if [ ! -f keys/auth_public.pem ]; then
    mkdir -p keys
    [ -f ../agt-auth/keys/public.pem ] && cp ../agt-auth/keys/public.pem keys/auth_public.pem && echo "[OK] Cle Auth copiee" || echo "[WARN] Cle Auth introuvable"
fi
docker compose up -d --build
sleep 8
docker compose exec chatbot python manage.py migrate --noinput
echo ""
curl -s http://localhost:7010/api/v1/chatbot/health | python3 -m json.tool 2>/dev/null || echo "En cours..."
echo ""
echo "[OK] Chatbot Service pret sur http://localhost:7010"
echo "  Swagger : http://localhost:7010/api/v1/docs/"
echo "  ReDoc   : http://localhost:7010/api/v1/redoc/"
echo "  Tests   : docker compose exec chatbot python -m pytest -v"
