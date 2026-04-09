# Service Subscription v1.0 - Guide d'utilisation

> Ce guide explique comment configurer, demarrer et utiliser le service Subscription de l'ecosysteme AGT.

## 1. Demarrage

### Prerequis
- Docker Desktop **demarre**
- **Service Auth demarre en premier** (pour la cle publique RSA)

### Lancement

**Windows :**
```powershell
cd agt-subscription
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

**Linux/macOS :**
```bash
cd agt-subscription
bash scripts/setup.sh
```

### Verification

```
curl http://localhost:7004/api/v1/subscriptions/health
```

### URLs

| URL | Description |
|-----|-------------|
| http://localhost:7004/api/v1/docs/ | Swagger UI |
| http://localhost:7004/api/v1/redoc/ | ReDoc |

---

## 2. Concepts cles

### Plans
Un plan definit une offre : nom, prix (multi-cycle), quotas. Chaque plan est scope a une plateforme. Un plan peut etre gratuit (`is_free: true`), par defaut (`is_default: true`), ou payant.

### Quotas
Chaque plan definit N quotas avec une cle libre (ex: `max_bots`, `messages_per_month`, `storage_mb`). Deux politiques :
- **hard** : depassement interdit, acces bloque
- **overage** : depassement autorise, comptabilise pour facturation

### Subscriber
Abstrait : peut etre un `user` (B2C) ou une `organization` (B2B). Les quotas d'une organisation sont partages entre ses membres.

### Cycle de vie
```
pending_payment -> active -> [renouvellement OK] -> active
                     |
                     +-> cancelled (par l'abonne, actif jusqu'a fin cycle)
                     +-> [expiration] -> grace -> expired -> suspended

trial -> active (si paiement)
      -> [selon config] : downgrade_to_free | suspend | expire
```

### Prorata
Upgrade/downgrade en cours de cycle : credit restant ancien plan - cout restant nouveau plan = montant du.

---

## 3. Premiere configuration

### 3.1 Obtenir un token (via Auth)

```bash
curl -X POST http://localhost:7000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@agt.com", "password": "MonPass123!", "platform_id": "<UUID>"}'
```

### 3.2 Configurer la plateforme

```bash
TOKEN="<votre-access-token>"

curl -X PUT http://localhost:7004/api/v1/subscriptions/config/<platform-id> \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "default_trial_days": 14,
    "grace_period_days": 3,
    "post_trial_behavior": "suspend",
    "default_currency": "XAF",
    "allowed_cycles": ["monthly", "yearly"]
  }'
```

### 3.3 Creer un plan gratuit

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/plans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "<platform-id>",
    "name": "Free",
    "slug": "free",
    "is_free": true,
    "is_default": true,
    "tier_order": 0,
    "prices": [{"billing_cycle": "monthly", "price": 0, "currency": "XAF"}],
    "quotas": [
      {"quota_key": "max_bots", "limit_value": 1, "is_cyclical": false, "overage_policy": "hard"},
      {"quota_key": "messages_per_month", "limit_value": 100, "is_cyclical": true, "overage_policy": "hard"}
    ]
  }'
```

### 3.4 Creer un plan payant

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/plans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "<platform-id>",
    "name": "Pro",
    "slug": "pro",
    "tier_order": 2,
    "prices": [
      {"billing_cycle": "monthly", "price": 15000, "currency": "XAF"},
      {"billing_cycle": "yearly", "price": 150000, "currency": "XAF"}
    ],
    "quotas": [
      {"quota_key": "max_bots", "limit_value": 5, "is_cyclical": false, "overage_policy": "hard"},
      {"quota_key": "messages_per_month", "limit_value": 10000, "is_cyclical": true, "overage_policy": "overage", "overage_unit_price": 2}
    ]
  }'
```

### 3.5 Souscrire a un plan

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "<platform-id>",
    "subscriber_type": "user",
    "subscriber_id": "<user-auth-id>",
    "plan_id": "<plan-id>",
    "billing_cycle": "monthly",
    "with_trial": true
  }'
```

### 3.6 Activer apres paiement

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/<sub-id>/activate \
  -H "Authorization: Bearer $TOKEN"
```

---

## 4. Quotas (endpoints S2S critiques)

### Verifier (< 50ms, cache Redis)

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/quotas/check \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<pid>", "subscriber_type": "user", "subscriber_id": "<uid>", "quota_key": "messages_per_month", "requested": 1}'
```

### Consommer

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/quotas/increment \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<pid>", "subscriber_type": "user", "subscriber_id": "<uid>", "quota_key": "messages_per_month", "amount": 1}'
```

### Reserve/Confirm/Release (atomique)

```bash
# 1. Reserver
curl -X POST .../quotas/reserve -d '{"platform_id": "...", "subscriber_type": "user", "subscriber_id": "...", "quota_key": "max_bots", "amount": 1}'

# 2a. Confirmer (si operation reussie)
curl -X POST .../quotas/confirm -d '{"reservation_id": "uuid"}'

# 2b. Liberer (si operation echouee)
curl -X POST .../quotas/release -d '{"reservation_id": "uuid"}'
```

---

## 5. Upgrade / Downgrade

```bash
curl -X POST http://localhost:7004/api/v1/subscriptions/<sub-id>/change-plan \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"new_plan_id": "<premium-plan-id>", "billing_cycle": "monthly"}'
```

L'`amount_due` retourne doit etre transmis au Service Payment.

---

## 6. Organisations B2B

```bash
# Creer une organisation
curl -X POST http://localhost:7004/api/v1/organizations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<pid>", "name": "ACME Corp", "owner_user_id": "<uid>"}'

# Ajouter un membre
curl -X POST http://localhost:7004/api/v1/organizations/<org-id>/members \
  -d '{"user_id": "<member-uid>"}'

# Souscrire pour l'org (quotas partages entre membres)
curl -X POST http://localhost:7004/api/v1/subscriptions \
  -d '{"platform_id": "...", "subscriber_type": "organization", "subscriber_id": "<org-id>", "plan_id": "...", "billing_cycle": "monthly"}'
```

---

## 7. Tests

```bash
docker compose exec subscription python -m pytest -v
```

---

## 8. Ports

| Ressource | URL |
|-----------|-----|
| API | http://localhost:7004 |
| Swagger | http://localhost:7004/api/v1/docs/ |
| ReDoc | http://localhost:7004/api/v1/redoc/ |
| PostgreSQL | localhost:5435 (sub_user / sub_password) |
| Redis | localhost:6382 |
