# AGT Wallet Service - v1.0

Ledger double-entry centralise. Wallets, holds, splits, cash-in/out.

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
| http://localhost:7006/api/v1/docs/ | Swagger UI |
| http://localhost:7006/api/v1/redoc/ | ReDoc |

## Tests
```bash
docker compose exec wallet python -m pytest -v
```

## Endpoints

### Accounts
- POST /wallet/accounts (creer wallet)
- GET /wallet/accounts/{id} (detail + solde disponible)
- GET /wallet/accounts/by-owner/{ownerId}
- POST /wallet/accounts/{id}/freeze | /unfreeze

### Ledger (double-entry)
- POST /wallet/credit
- POST /wallet/debit
- POST /wallet/transfer
- POST /wallet/split (partage commission multi-beneficiaire)
- GET /wallet/accounts/{id}/transactions (historique)

### Holds
- POST /wallet/holds (reservation)
- POST /wallet/holds/{id}/capture
- POST /wallet/holds/{id}/release

### Split Rules
- POST/GET /wallet/split-rules

### Admin
- GET /wallet/admin/stats
- POST /wallet/admin/audit-ledger (verification equilibre)
- POST /wallet/admin/adjustment (correctif avec justification)

Voir [CDC_v1.0.md](./CDC_v1.0.md)

Port : **7006**
