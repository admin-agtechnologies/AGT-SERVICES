#!/bin/bash
set -e
echo "AGT Auth Service v1.0 - Setup"
echo "=============================="

# 1. .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "[OK] .env cree depuis .env.example"
fi

# 2. Cles RSA
if [ ! -f keys/private.pem ]; then
    mkdir -p keys
    if command -v openssl &> /dev/null; then
        openssl genrsa -out keys/private.pem 2048
        openssl rsa -in keys/private.pem -pubout -out keys/public.pem
    else
        echo "[INFO] OpenSSL absent, generation via Docker..."
        docker run --rm -v "$(pwd)/keys:/keys" alpine/openssl genrsa -out /keys/private.pem 2048
        docker run --rm -v "$(pwd)/keys:/keys" alpine/openssl rsa -in /keys/private.pem -pubout -out /keys/public.pem
    fi
    chmod 600 keys/private.pem
    echo "[OK] Cles RSA generees"
fi

# 3. Build & Start
echo ""
echo "Build et demarrage Docker..."
docker compose up -d --build

# 4. Attente
echo "Attente demarrage services..."
sleep 8

# 5. Migrations
echo "Migrations..."
docker compose exec auth python manage.py migrate --noinput

# 6. Health check
echo ""
echo "Health check..."
curl -s http://localhost:7000/api/v1/auth/health | python3 -m json.tool 2>/dev/null || echo "Service en cours de demarrage..."

echo ""
echo "[OK] Auth Service pret sur http://localhost:7000"
echo ""
echo "Documentation API :"
echo "  Swagger UI : http://localhost:7000/api/v1/docs/"
echo "  ReDoc      : http://localhost:7000/api/v1/redoc/"
echo ""
echo "Tests : docker compose exec auth python -m pytest -v"
