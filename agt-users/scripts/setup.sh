#!/bin/bash
set -e
echo "AGT Users Service v1.0 - Setup"
echo "==============================="

if [ ! -f .env ]; then
    cp .env.example .env
    echo "[OK] .env cree"
fi

if [ ! -f keys/auth_public.pem ]; then
    mkdir -p keys
    if [ -f ../agt-auth/keys/public.pem ]; then
        cp ../agt-auth/keys/public.pem keys/auth_public.pem
        echo "[OK] Cle publique Auth copiee depuis ../agt-auth/"
    else
        echo "[WARN] Cle publique Auth introuvable dans ../agt-auth/keys/public.pem"
        echo "       Copiez-la manuellement : cp <chemin>/public.pem keys/auth_public.pem"
    fi
fi

echo ""
echo "Build et demarrage Docker..."
docker compose up -d --build

echo "Attente demarrage services..."
sleep 8

echo "Migrations..."
docker compose exec users python manage.py migrate --noinput

echo ""
echo "Health check..."
curl -s http://localhost:7001/api/v1/health | python3 -m json.tool 2>/dev/null || echo "Service en cours de demarrage..."

echo ""
echo "[OK] Users Service pret sur http://localhost:7001"
echo ""
echo "Documentation API :"
echo "  Swagger UI : http://localhost:7001/api/v1/docs/"
echo "  ReDoc      : http://localhost:7001/api/v1/redoc/"
echo ""
echo "Tests : docker compose exec users python -m pytest -v"
