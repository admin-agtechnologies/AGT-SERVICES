# HANDOFF REPORT — Session du 16 avril 2026

## 1. CE QUI A ÉTÉ COMPLÉTÉ

### Infrastructure

- Service `agt-wallet` déployé en **production (gunicorn)** sur le port 7006
- PostgreSQL (`agt-wallet-db`) et Redis (`agt-wallet-redis`) opérationnels
- Clé publique Auth copiée dans `agt-wallet/keys/auth_public.pem`
- MVP (Auth + Users + Notification) déployé et fonctionnel

### Corrections de code

- `apps/accounts/models.py` — ajout de `is_active` et `updated_at` sur `SplitRule`, ajout contrainte `unique_together`
- `config/settings.py` — ajout de `apps.cashout` dans `INSTALLED_APPS`, correction `SPECTACULAR_SETTINGS` avec `BearerAuth`

### Migrations

- Migrations générées et appliquées : `apps/accounts/migrations/0001_initial.py`
- 6 tables créées : `accounts`, `ledger_transactions`, `ledger_entries`, `holds`, `cashout_requests`, `split_rules`
- Migrations commitées dans le repo (branche `atabong-service-wallet-v1`)

### Migrations Notification (bonus)

- Migrations générées et appliquées pour `notifications`, `templates_mgr`, `campaigns`, `devices`

### Authentification

- Utilisateur de test créé : `dev2@example.com` / `Test1234!`
- Email vérifié manuellement en DB
- Login fonctionnel — token JWT obtenu
- Swagger Wallet accessible et autorisé sur http://localhost:7006/api/v1/docs/

---

## 2. EN COURS

- Tests des endpoints wallet via Swagger — **non démarrés**
- Aucun endpoint testé fonctionnellement

---

## 3. PROCHAINE ÉTAPE IMMÉDIATE

**Tester les endpoints dans l'ordre suivant via Swagger (http://localhost:7006/api/v1/docs/) :**

1. `POST /api/v1/wallet/accounts` — créer un wallet user
2. `GET /api/v1/wallet/accounts/{id}` — vérifier le solde
3. `POST /api/v1/wallet/credit` — créditer le wallet (nécessite token S2S)
4. `POST /api/v1/wallet/transfer` — virement entre deux wallets
5. `POST /api/v1/wallet/holds` — créer un hold
6. `POST /api/v1/wallet/holds/{id}/capture` — capturer un hold
7. `POST /api/v1/wallet/holds/{id}/release` — libérer un hold
8. `POST /api/v1/wallet/split` — partage commission
9. `POST /api/v1/wallet/admin/audit-ledger` — vérifier équilibre ledger

---

## 4. POINTS D'ATTENTION

### Bugs connus

- `views.py` ligne `HoldCreateView` — les paramètres passés à `LedgerService.create_hold` sont dans le mauvais ordre (à vérifier au test)
- `SplitRuleListCreateView` — utilise `r.rules` mais le champ s'appelle aussi `rules` dans le modèle corrigé (cohérent)
- `apps/cashout` et `apps/holds` sont des dossiers vides — pas de modèles ni vues propres, tout est dans `apps/accounts` et `apps/ledger`

### Décisions techniques

- Toutes les migrations sont dans `apps/accounts` — c'est là que sont tous les modèles
- Le wallet tourne en mode production (gunicorn 4 workers) — pas de hot reload
- Pour tout changement de code : `docker compose up -d --build` depuis `agt-wallet/`

### Problème machine locale

- PostgreSQL natif (`pid 1080`) et Redis natif (`pid 878`) tournent sur la machine — ils entrent en conflit avec Docker sur les ports 5432 et 6379
- **À chaque redémarrage machine** : `sudo systemctl stop postgresql redis` avant de lancer Docker

### Compte de test

- Email : `dev2@example.com`
- Password : `Test1234!`
- Platform ID : à récupérer depuis la DB Auth ou Swagger

---

## 5. COMMANDES UTILES

```bash
# Arrêter les services natifs (obligatoire après redémarrage machine)
sudo systemctl stop postgresql redis

# Lancer le MVP (Auth + Users + Notification)
cd ~/Documents/projet/AGT/AGT-SERVICES
bash deploy_mvp.sh

# Lancer le wallet
cd agt-wallet && docker compose up -d && cd ..

# Copier la clé Auth vers le wallet (si reset)
cp agt-auth/keys/public.pem agt-wallet/keys/auth_public.pem

# Rebuild wallet après changement de code
cd agt-wallet && docker compose up -d --build && cd ..

# Migrations wallet
docker exec agt-wallet-service python manage.py makemigrations accounts
docker exec agt-wallet-service python manage.py migrate

# Vérifier santé des services
curl http://localhost:7000/api/v1/auth/health
curl http://localhost:7001/api/v1/health
curl http://localhost:7002/api/v1/health
curl http://localhost:7006/api/v1/wallet/health

# Logs wallet
docker logs agt-wallet-service --tail=50

# Vérifier email utilisateur en DB Auth
docker exec agt-auth-db psql -U agt_user -d agt-auth-db -c "SELECT email, email_verified FROM users_auth WHERE email='dev2@example.com';"

# Vérifier tables wallet
docker exec agt-wallet-db psql -U wallet_user -d agt-wallet-db -c "\dt"

# Branche Git active
# atabong-service-wallet-v1
```
