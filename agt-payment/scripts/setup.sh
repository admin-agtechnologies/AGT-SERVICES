#!/bin/bash
set -e
echo "AGT Payment Service v1.2 - Setup"
echo "================================="

# --- .env ---
if [ ! -f .env ]; then
    cp .env.example .env
    echo "[OK] .env cree depuis .env.example"
fi

# --- Clé publique Auth ---
if [ ! -f keys/auth_public.pem ]; then
    mkdir -p keys
    if [ -f ../agt-auth/keys/public.pem ]; then
        cp ../agt-auth/keys/public.pem keys/auth_public.pem
        echo "[OK] Cle Auth copiee depuis agt-auth"
    else
        echo "[WARN] Cle Auth introuvable - copiez manuellement agt-auth/keys/public.pem vers keys/auth_public.pem"
    fi
fi

# --- Build et démarrage ---
docker compose up -d --build

# --- Attente que la DB soit prête ---
echo "[...] Attente demarrage base de données (15s)..."
sleep 15

# --- Health check ---
echo ""
curl -s http://localhost:7005/api/v1/payments/health | python3 -m json.tool 2>/dev/null || echo "Service en cours de demarrage..."
echo ""
echo "[OK] Payment Service pret sur http://localhost:7005"
echo "  Swagger : http://localhost:7005/api/v1/docs/"
echo "  ReDoc   : http://localhost:7005/api/v1/redoc/"
echo "  Tests   : docker compose exec payment python -m pytest -v"
echo ""
echo "[!] MIGRATIONS OBLIGATOIRES au premier lancement :"
echo "    docker exec agt-pay-service python manage.py makemigrations payments"
echo "    docker exec agt-pay-service python manage.py migrate"