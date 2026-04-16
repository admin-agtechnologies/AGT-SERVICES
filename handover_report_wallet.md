# HANDOFF REPORT — Session du 16 avril 2026 (Wallet — Finale)

## 1. CE QUI A ÉTÉ COMPLÉTÉ

### Infrastructure

- Service `agt-wallet` déployé en production (gunicorn) sur le port 7006
- PostgreSQL (`agt-wallet-db`) et Redis (`agt-wallet-redis`) opérationnels
- Clé publique Auth copiée dans `agt-wallet/keys/auth_public.pem`
- MVP (Auth + Users + Notification) déployé et fonctionnel

### Corrections de bugs (models)

- `apps/accounts/models.py` — `idempotency_key` : `UUIDField` → `CharField(128)` sur `LedgerTransaction`, `Hold`, `CashoutRequest`
- `apps/accounts/models.py` — `source_reference_id` : `UUIDField` → `CharField(128)` sur `LedgerTransaction`
- `apps/accounts/models.py` — `reference_id` : `UUIDField` → `CharField(128)` sur `Hold`
- `apps/accounts/models.py` — `payment_tx_id` : `UUIDField` → `CharField(128)` sur `CashoutRequest`

### Corrections de bugs (views)

- `CreditView` — suppression de `metadata` en arg superflu
- `HoldCreateView` — correction de l'ordre des arguments
- `HoldCaptureView` — suppression de `platform_id` en arg incorrect
- `AccountCreateView` — `owner_id` auto depuis JWT si absent du body
- `AdminAuditView` — `audit_balance()` → `verify_integrity()`
- `AdminAdjustmentView` — ajout validation `account_id` et `amount`

### Serializers ajoutés (views)

- `CreditSerializer`
- `DebitSerializer`
- `TransferSerializer`
- `HoldSerializer`
- `SplitSerializer`
- `SplitRuleSerializer`
- `AdjustmentSerializer`
- `OpenApiParameter` sur `HoldListView` pour affichage Swagger

### Nouveaux endpoints ajoutés

- `GET /wallet/holds` — liste des holds d'un compte (query param `account_id`)
- `GET /wallet/holds/{hold_id}` — détail d'un hold
- `POST /wallet/holds/create` — création d'un hold (séparé du GET liste)

### Migrations

- `0001_initial` — tables initiales
- `0002_alter_cashoutrequest_idempotency_key_and_more` — idempotency_key CharField
- `0003_alter_cashoutrequest_payment_tx_id_and_more` — source_reference_id, reference_id, payment_tx_id CharField

### Documentation

- `docs/GUIDE_WALLET.md` — guide complet généré (11 sections, 20 endpoints, 19 scénarios détaillés)

### Git

- Branche `atabong-service-wallet-v1` pushée et à jour
- `main` mergé avec tous les changements wallet
- Pas de conflits

---

## 2. EN COURS

Rien — tous les endpoints sont fonctionnels et testés.

---

## 3. PROCHAINE ÉTAPE IMMÉDIATE

Écrire les tests pytest selon la règle AGT (un service sans tests n'est pas terminé) :

```
agt-wallet/tests/
├── unit/
│   ├── test_ledger_service.py   # credit, debit, transfer, split, holds, verify_integrity
│   └── test_models.py           # available_balance, is_frozen, can_debit
└── integration/
    ├── test_accounts.py         # create, detail, freeze, unfreeze, by-owner
    ├── test_credit_debit.py     # credit, debit, idempotence
    ├── test_transfer.py         # transfer, insufficient_balance, frozen
    ├── test_holds.py            # create, capture, release, list, detail
    ├── test_split.py            # split, split_unbalanced
    └── test_admin.py            # stats, audit, adjustment
```

Lancer avec :

```bash
docker exec agt-wallet-service python -m pytest -v
```

---

## 4. POINTS D'ATTENTION

### Bug connu — token S2S platform_id

`common/authentication.py` : pour les tokens S2S, `platform_id` est lu depuis `p.get("platform_id")` alors qu'il devrait être `p.get("sub")`.

Fix à appliquer :

```python
if token_type == "s2s":
    self.platform_id = payload.get("sub")
else:
    self.platform_id = payload.get("platform_id")
```

### Conflits de ports sur Ubuntu

PostgreSQL natif (5432) et Redis natif (6379) entrent en conflit avec Docker.
**À chaque redémarrage machine :**

```bash
sudo systemctl stop postgresql redis
```

### Clé publique Auth

Après tout reset du service Auth, recopier la clé :

```bash
cp agt-auth/keys/public.pem agt-wallet/keys/auth_public.pem
cd agt-wallet && docker compose up -d --build && cd ..
```

### Migrations à copier localement

Toujours copier les migrations avant rebuild :

```bash
docker exec agt-wallet-service python manage.py makemigrations accounts
docker cp agt-wallet-service:/app/apps/accounts/migrations/XXXX.py \
  agt-wallet/apps/accounts/migrations/XXXX.py
cd agt-wallet && docker compose up -d --build && cd ..
docker exec agt-wallet-service python manage.py migrate
```

### Compte de test

- Email : `dev2@example.com`
- Password : `Test1234!`
- Platform ID : `5c2f1299-7447-4a70-80e9-597421f43371`

---

## 5. ENDPOINTS VALIDÉS (20/20)

| Endpoint                                 | Statut |
| ---------------------------------------- | ------ |
| GET /wallet/health                       | ✅     |
| POST /wallet/accounts                    | ✅     |
| GET /wallet/accounts/{id}                | ✅     |
| GET /wallet/accounts/by-owner/{owner_id} | ✅     |
| POST /wallet/accounts/{id}/freeze        | ✅     |
| POST /wallet/accounts/{id}/unfreeze      | ✅     |
| GET /wallet/accounts/{id}/transactions   | ✅     |
| POST /wallet/credit                      | ✅     |
| POST /wallet/debit                       | ✅     |
| POST /wallet/transfer                    | ✅     |
| POST /wallet/split                       | ✅     |
| POST /wallet/holds/create                | ✅     |
| GET /wallet/holds                        | ✅     |
| GET /wallet/holds/{id}                   | ✅     |
| POST /wallet/holds/{id}/capture          | ✅     |
| POST /wallet/holds/{id}/release          | ✅     |
| GET /wallet/split-rules                  | ✅     |
| POST /wallet/split-rules                 | ✅     |
| GET /wallet/admin/stats                  | ✅     |
| POST /wallet/admin/audit-ledger          | ✅     |
| POST /wallet/admin/adjustment            | ✅     |

---

## 6. COMMANDES UTILES

```bash
# Arrêter les services natifs (obligatoire après redémarrage machine)
sudo systemctl stop postgresql redis

# Lancer le MVP (Auth + Users + Notification)
cd ~/Documents/projet/AGT/AGT-SERVICES
bash deploy_mvp.sh

# Copier la clé Auth vers le wallet
cp agt-auth/keys/public.pem agt-wallet/keys/auth_public.pem

# Lancer le wallet
cd agt-wallet && docker compose up -d && cd ..

# Rebuild wallet après changement de code
cd agt-wallet && docker compose up -d --build && cd ..

# Migrations
docker exec agt-wallet-service python manage.py makemigrations accounts
docker exec agt-wallet-service python manage.py migrate

# Logs wallet
docker logs agt-wallet-service --tail=50
docker logs agt-wallet-service -f

# Tests
docker exec agt-wallet-service python -m pytest -v

# Vérifier santé des services
curl http://localhost:7000/api/v1/auth/health
curl http://localhost:7006/api/v1/wallet/health

# Vérifier tables wallet
docker exec agt-wallet-db psql -U wallet_user -d agt-wallet-db -c "\dt"

# Vérifier équilibre ledger en SQL
docker exec agt-wallet-db psql -U wallet_user -d agt-wallet-db \
  -c "SELECT direction, SUM(amount) FROM ledger_entries GROUP BY direction;"

# Swagger
# Auth   → http://localhost:7000/api/v1/docs/
# Wallet → http://localhost:7006/api/v1/docs/

# Branche Git active
# atabong-service-wallet-v1
```
