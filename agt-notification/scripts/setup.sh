#!/bin/bash
set -e
echo "AGT Notification Service v1.0 - Setup"
echo "======================================="

if [ ! -f .env ]; then
    cp .env.example .env
    echo "[OK] .env cree"
fi

if [ ! -f keys/auth_public.pem ]; then
    mkdir -p keys
    if [ -f ../agt-auth/keys/public.pem ]; then
        cp ../agt-auth/keys/public.pem keys/auth_public.pem
        echo "[OK] Cle publique Auth copiee"
    else
        echo "[WARN] Cle publique Auth introuvable dans ../agt-auth/keys/public.pem"
        echo "       Copiez-la : cp <chemin>/public.pem keys/auth_public.pem"
    fi
fi

echo ""
echo "Build et demarrage Docker (API + Worker + Beat + RabbitMQ)..."
docker compose up -d --build

echo "Attente demarrage services..."
sleep 12

echo "Migrations..."
docker compose exec notification python manage.py migrate --noinput

echo ""
echo "Health check..."
curl -s http://localhost:7002/api/v1/health | python3 -m json.tool 2>/dev/null || echo "Service en cours de demarrage..."

echo ""
echo "[OK] Notification Service pret sur http://localhost:7002"
echo ""
echo "Documentation API :"
echo "  Swagger UI : http://localhost:7002/api/v1/docs/"
echo "  RabbitMQ   : http://localhost:15672 (guest/guest)"
echo ""
echo "Tests : docker compose exec notification python -m pytest -v"
