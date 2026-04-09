# AGT Payment Service - v1.0

Execution de transactions multi-provider: Orange Money, MTN MoMo, Stripe, PayPal.

## Demarrage

### Linux
```bash
bash scripts/setup.sh
```

### Windows
```powershell
# Ouvrir Docker Desktop
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Documentation API

| URL | Description |
|-----|-------------|
| http://localhost:7005/api/v1/docs/ | Swagger UI |
| http://localhost:7005/api/v1/redoc/ | ReDoc |

## Tests
```bash
docker compose exec payment python -m pytest -v
```

## Endpoints

### Payments
- POST /payments/initiate (idempotency_key obligatoire)
- GET /payments (listing avec filtres)
- GET /payments/{id} (detail + historique statuts)
- POST /payments/{id}/cancel (pending uniquement)

### Webhooks (sans auth)
- POST /payments/webhooks/orange-money
- POST /payments/webhooks/mtn-momo
- POST /payments/webhooks/stripe
- POST /payments/webhooks/paypal

### Providers
- POST/GET /payments/providers (config globale)
- GET/PUT /payments/platforms/{id}/providers (config plateforme)

### Admin
- GET /payments/admin/stats
- POST /payments/admin/{id}/force-status

Voir [CDC_v1.0.md](./CDC_v1.0.md)

Port : **7005**
