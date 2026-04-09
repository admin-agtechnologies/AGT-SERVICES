# AGT Subscription Service - v1.0

Plans, abonnements, quotas temps reel, prorata, trial, organisations B2B.

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

## Swagger
http://localhost:7004/api/v1/docs/

## Tests
```bash
docker compose exec subscription python -m pytest -v
```

## Endpoints principaux

### Plans
- POST/GET /subscriptions/plans
- GET/PUT /subscriptions/plans/{id}
- POST /subscriptions/plans/{id}/archive

### Subscriptions
- POST /subscriptions (create)
- GET /subscriptions/list
- GET /subscriptions/{id}
- POST /subscriptions/{id}/cancel
- POST /subscriptions/{id}/change-plan (prorata)
- POST /subscriptions/{id}/activate
- POST /subscriptions/{id}/reactivate
- GET /subscriptions/{id}/usage

### Quotas (S2S)
- POST /subscriptions/quotas/check (< 50ms)
- POST /subscriptions/quotas/increment
- POST /subscriptions/quotas/reserve
- POST /subscriptions/quotas/confirm
- POST /subscriptions/quotas/release

### Organizations B2B
- POST/GET /organizations
- POST/GET/DELETE /organizations/{id}/members

### Config
- GET/PUT /subscriptions/config/{platformId}

Voir [CDC_v1.0.md](./CDC_v1.0.md)

Port : **7004**
