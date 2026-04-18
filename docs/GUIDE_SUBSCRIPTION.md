# GUIDE SUBSCRIPTION SERVICE — AG Technologies
## Subscription Service v1.0

> **À qui s'adresse ce guide ?**
> À tout développeur qui souhaite tester et valider le service Subscription d'AGT.
> Ce guide est **autonome** — vous partez de zéro sur votre machine.
>
> **Ce guide couvre les blocs testés et validés le 17 avril 2026 :**
> Health → Plans → Abonnements → Quotas → Organizations → Config plateforme
>
> **Bugs identifiés et corrigés lors de cette session :**
> `DEFAULT_SCHEMA_CLASS` manquant · `config/__init__.py` vide · `AUTH_PUBLIC_KEY` non chargé ·
> champs `price`/`amount` et `quota_key`/`feature_key` incorrects · `trial_days` vs `default_trial_days`

---

## Table des matières

1. [Rôle du service Subscription dans l'écosystème](#1-rôle-du-service-subscription-dans-lécosystème)
2. [Prérequis](#2-prérequis)
3. [Démarrer le MVP](#3-démarrer-le-mvp)
4. [Préparer Subscription](#4-préparer-subscription)
5. [Démarrer le service](#5-démarrer-le-service)
6. [Migrations](#6-migrations)
7. [Health check](#7-health-check)
8. [Lancer les tests](#8-lancer-les-tests)
9. [Swagger](#9-swagger)
10. [Prérequis Swagger — Créer les plateformes et un utilisateur de test](#10-prérequis-swagger--créer-les-plateformes-et-un-utilisateur-de-test)
11. [Bloc 1 — Plans](#11-bloc-1--plans)
12. [Bloc 2 — Abonnements](#12-bloc-2--abonnements)
13. [Bloc 3 — Quotas](#13-bloc-3--quotas)
14. [Bloc 4 — Organizations](#14-bloc-4--organizations)
15. [Bloc 5 — Config plateforme](#15-bloc-5--config-plateforme)
16. [Flux inter-services](#16-flux-inter-services)
17. [Bugs connus](#17-bugs-connus)
18. [Troubleshooting](#18-troubleshooting)
19. [Commandes utiles](#19-commandes-utiles)

---

## 1. Rôle du service Subscription dans l'écosystème

Subscription est la **source de vérité des règles métier** de l'écosystème AGT. Il est le seul service qui définit les plans, les quotas et les limites d'utilisation par plateforme. Aucun autre service ne définit ses propres quotas — ils interrogent Subscription.

Ses responsabilités :

- Gérer les **plans** (prix par cycle, quotas associés, archivage)
- Gérer le **cycle de vie des abonnements** (création, activation, annulation, renouvellement, changement de plan avec calcul de prorata)
- Exposer les **quotas en temps réel** (check, increment, reserve/confirm/release)
- Gérer les **organisations B2B** (multi-membres, partage d'abonnement)
- Configurer les **paramètres par plateforme** (trial, grace period, devise)
- Émettre des **events RabbitMQ** vers Payment et Notification lors des transitions d'état
- Exécuter des **crons Celery Beat** pour le renouvellement automatique et les alertes quota

**Port :** 7004
**Swagger UI :** http://localhost:7004/api/v1/docs/
**Stack :** Python / Django / PostgreSQL / Redis / Celery + Beat / RabbitMQ

---

## 2. Prérequis

- Docker Desktop installé et **démarré** (icône stable dans la barre des tâches)
- Dépôt `AGT-SERVICES` cloné en local
- MVP (Auth, Users, Notification) opérationnel
- Machine fraîche avec Docker Desktop et Docker Compose installés et ouverts, mais aucun service de notre architecture lancé

---

## 3. Démarrer le MVP

Depuis la racine `AGT-SERVICES/` :

```powershell
.\reset_mvp.ps1
```

Attendre le message final :
```
=========================================
 DÉPLOIEMENT MVP RÉUSSI !
=========================================
 Auth         : http://localhost:7000/api/v1/docs/
 Users        : http://localhost:7001/api/v1/docs/
 Notification : http://localhost:7002/api/v1/docs/
 Mailpit      : http://localhost:8025
 RabbitMQ     : http://localhost:15672
=========================================
```

Les 3 services doivent être healthy : Auth (:7000), Users (:7001), Notification (:7002).

### Appliquer les migrations MVP

> ⚠️ **Obligatoire** après chaque `reset_mvp.ps1` sur une base vide (premier lancement ou après `--clean`).
> Sans cette étape, les tables n'existent pas et toutes les requêtes API renverront une erreur 500.

```powershell
# Auth
docker exec agt-auth-service python manage.py makemigrations authentication
docker exec agt-auth-service python manage.py migrate --noinput

# Users
docker exec agt-users-service python manage.py makemigrations users roles documents
docker exec agt-users-service python manage.py migrate --noinput

# Notification
docker exec agt-notif-service python manage.py makemigrations notifications templates_mgr campaigns devices
docker exec agt-notif-service python manage.py migrate --noinput
```

Résultat attendu pour chaque service :
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying authentication.0001_initial... OK
```

Si vous voyez `No migrations to apply` — les migrations sont déjà à jour, vous pouvez continuer.

---

## 4. Préparer Subscription

### 4.1 Créer le fichier .env

```powershell
cd agt-subscription
copy .env.example .env
cd ..
```

### 4.2 Copier la clé publique Auth

```powershell
copy agt-auth\keys\public.pem agt-subscription\keys\auth_public.pem
```

> ⚠️ Sans cette étape, tous les appels authentifiés retourneront `{"detail": "AUTH_PUBLIC_KEY non configure."}`.

---

## 5. Démarrer le service

```powershell
cd agt-subscription
docker compose up -d --build
```

Attendre que les 5 containers soient up :
```
✔ Container agt-sub-db        Healthy
✔ Container agt-sub-redis     Healthy
✔ Container agt-sub-service   Running
✔ Container agt-sub-worker    Running
✔ Container agt-sub-beat      Running
```

---

## 6. Migrations

```powershell
docker compose exec -e DJANGO_SETTINGS_MODULE=config.settings subscription python manage.py makemigrations plans subscriptions quotas organizations
docker compose exec subscription python manage.py migrate
```

Résultat attendu :
```
Migrations for 'plans': apps/plans/migrations/0001_initial.py
Migrations for 'subscriptions': apps/subscriptions/migrations/0001_initial.py
...
Running migrations:
  Applying plans.0001_initial... OK
  Applying subscriptions.0001_initial... OK
  Applying organizations.0001_initial... OK
```

> ⚠️ **Note connue** : Les dossiers `migrations/` ne sont pas commités dans le repo — il faut toujours exécuter cette étape au premier démarrage.

---

## 7. Health check

```powershell
curl http://localhost:7004/api/v1/subscriptions/health
```

Réponse attendue :
```json
{"status":"healthy","database":"ok","redis":"ok","version":"1.0.0"}
```

Si `"status": "degraded"` → vérifiez les logs :
```powershell
docker logs agt-sub-service --tail=30
```

---

## 8. Lancer les tests

```powershell
docker compose exec subscription python -m pytest -v
```

Résultat attendu : **30 passed**

```
tests/test_all.py::TestPlanModel::test_create_plan PASSED
tests/test_all.py::TestSubscriptionService::test_cancel PASSED
...
30 passed, 1 warning in 1.95s
```

> ℹ️ Le warning `UnorderedObjectListWarning` sur `organizations` est connu et non bloquant.

---

## 9. Swagger

```
http://localhost:7004/api/v1/docs/
```

> ⚠️ Si Swagger affiche `Failed to load API definition` → vérifier que `DEFAULT_SCHEMA_CLASS` est bien présent dans `config/settings.py` (voir section 17 — Bugs connus).

---

## 10. Prérequis Swagger — Créer les plateformes et un utilisateur de test

Avant tout test via Swagger, il faut créer les plateformes dans Auth et un utilisateur de test. Ces étapes sont à faire **une seule fois** par environnement.

### Authentification dans Auth Swagger

Dans Auth Swagger `http://localhost:7000/api/v1/docs/` → **Authorize** (en haut à droite) :

```
X-Admin-API-Key: <valeur de ADMIN_API_KEY dans agt-auth/.env>
```

> La valeur par défaut est `change-me-admin-api-key-very-secret`. La valeur réelle se trouve dans `agt-auth/.env`.

---

### Étape 1 — Créer la plateforme S2S Subscription

`POST /api/v1/auth/platforms` :
```json
{
  "name": "AGT Subscription",
  "slug": "agt-subscription",
  "allowed_auth_methods": ["email"]
}
```

**Réponse (201 Created) :**
```json
{
  "id": "<uuid_généré>",
  "name": "AGT Subscription",
  "slug": "agt-subscription",
  "is_active": true,
  "client_secret": "<secret_affiché_une_seule_fois>"
}
```

> ⚠️ Le `client_secret` n'est affiché **qu'une seule fois**. Notez-le immédiatement.
> En cas de perte → désactiver la plateforme et en recréer une nouvelle.

Mettez à jour `agt-subscription/.env` :
```env
S2S_AUTH_URL=http://agt-auth-service:7000/api/v1
S2S_CLIENT_ID=<id_retourné>
S2S_CLIENT_SECRET=<client_secret_retourné>
```

Puis rebuild Subscription :
```powershell
cd agt-subscription
docker compose up -d --build
cd ..
```

---

### Étape 2 — Créer la plateforme S2S Notification (si pas déjà fait)

`POST /api/v1/auth/platforms` :
```json
{
  "name": "AGT Notification",
  "slug": "agt-notification",
  "allowed_auth_methods": ["email"]
}
```

Mettez à jour `agt-notification/.env` avec `S2S_CLIENT_ID` et `S2S_CLIENT_SECRET`, puis rebuild Notification :
```powershell
cd agt-notification
docker compose up -d --build notification celery-worker
cd ..
```

---

### Étape 3 — Créer une plateforme applicative de test

`POST /api/v1/auth/platforms` :
```json
{
  "name": "Plateforme Test",
  "slug": "plateforme-test",
  "allowed_auth_methods": ["email", "phone", "magic_link"],
  "allowed_redirect_urls": []
}
```

**Réponse (201 Created) :**
```json
{
  "id": "<uuid_généré>",
  "name": "Plateforme Test",
  "is_active": true,
  "client_secret": "<secret_affiché_une_seule_fois>"
}
```

> Notez l'`id` — c'est votre **Platform ID**. Il sera requis dans `platform_id` et le header `X-Platform-Id` pour les appels Register/Login.

---

### Étape 4 — Créer les 4 templates Notification

Générez d'abord un token S2S — `POST /api/v1/auth/s2s/token` (sans header, credentials de la plateforme test dans le body) :
```json
{
  "client_id": "<platform_id_plateforme_test>",
  "client_secret": "<client_secret_plateforme_test>"
}
```

Copiez le `access_token`, puis dans Notification Swagger `http://localhost:7002/api/v1/docs/` → **Authorize** :
```
Bearer <access_token>
```

> ⚠️ Le token S2S expire en 1h. Si vous obtenez un 401 → régénérez via `POST /auth/s2s/token`.

Créez les 4 templates via `POST /api/v1/templates` :

**Template 1 — `auth_verify_email`**
```json
{
  "name": "auth_verify_email",
  "channel": "email",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": "Vérifiez votre adresse email — {{ platform_name }}",
  "body": "Bonjour {{ first_name }},\n\nMerci de vous être inscrit sur {{ platform_name }}.\n\nCliquez sur le lien ci-dessous pour vérifier votre adresse email :\n\n{{ verification_url }}\n\nCe lien expire dans {{ expires_in_minutes }} minutes.\n\nSi vous n'avez pas créé de compte, ignorez cet email.\n\nL'équipe {{ platform_name }}",
  "locale": "fr",
  "category": "transactional"
}
```

**Template 2 — `auth_otp_sms`**
```json
{
  "name": "auth_otp_sms",
  "channel": "sms",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": null,
  "body": "Bonjour {{ first_name }}, votre code de vérification {{ platform_name }} est : {{ otp_code }}. Valable {{ expires_in_minutes }} minutes. Ne le partagez jamais.",
  "locale": "fr",
  "category": "transactional"
}
```

**Template 3 — `auth_magic_link`**
```json
{
  "name": "auth_magic_link",
  "channel": "email",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": "Votre lien de connexion — {{ platform_name }}",
  "body": "Bonjour {{ first_name }},\n\nVous avez demandé un lien de connexion sans mot de passe.\n\nCliquez ici pour vous connecter :\n\n{{ magic_link_url }}\n\nCe lien expire dans {{ expires_in_minutes }} minutes. Il ne peut être utilisé qu'une seule fois.\n\nSi vous n'avez pas fait cette demande, ignorez cet email.\n\nL'équipe {{ platform_name }}",
  "locale": "fr",
  "category": "transactional"
}
```

**Template 4 — `auth_reset_password`**
```json
{
  "name": "auth_reset_password",
  "channel": "email",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": "Réinitialisation de votre mot de passe — {{ platform_name }}",
  "body": "Bonjour {{ first_name }},\n\nVous avez demandé la réinitialisation de votre mot de passe.\n\nCliquez sur le lien ci-dessous pour choisir un nouveau mot de passe :\n\n{{ reset_url }}\n\nCe lien expire dans {{ expires_in_minutes }} minutes. Il ne peut être utilisé qu'une seule fois.\n\nSi vous n'avez pas fait cette demande, ignorez cet email.\n\nL'équipe {{ platform_name }}",
  "locale": "fr",
  "category": "transactional"
}
```

---

### Étape 5 — Créer et vérifier un utilisateur de test

**Register** — `POST /api/v1/auth/register` avec header `X-Platform-Id: <platform_id_test>` :
```json
{
  "email": "test@agt.com",
  "password": "Test1234!",
  "method": "email",
  "first_name": "Test",
  "last_name": "AGT"
}
```

Vérifiez l'email dans Mailpit `http://localhost:8025`, copiez le token depuis le lien et appelez `POST /api/v1/auth/verify-email` :
```json
{
  "token": "<token_depuis_le_lien>"
}
```

Réponse attendue :
```json
{
  "message": "Email verified",
  "email_verified": true
}
```

**Login** — via PowerShell (`platform_id` dans le body, pas dans un header) :
```powershell
$r = Invoke-RestMethod -Uri "http://localhost:7000/api/v1/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"email": "test@agt.com", "password": "Test1234!", "method": "email", "platform_id": "<platform_id_test>"}'
$token = $r.access_token
$token | Set-Clipboard
```

> Le `sub` du JWT est le `user_id` à utiliser dans les appels Subscription comme `subscriber_id`.

**Injecter le token dans Subscription Swagger** → **Authorize** → collez le token depuis le presse-papier (sans `Bearer` devant, Swagger l'ajoute automatiquement).

> ⚠️ Le token JWT utilisateur expire après **15 minutes**. Pour en obtenir un nouveau, relancez la commande PowerShell ci-dessus — `$token` sera automatiquement mis à jour.

---

## 11. Bloc 1 — Plans

### Rôle
Les plans définissent les offres disponibles sur une plateforme : prix par cycle de facturation et quotas associés. Un plan doit exister avant de pouvoir créer un abonnement.

### Authentification
Tous les endpoints Plans requièrent un JWT utilisateur dans le header Authorization de Swagger.

---

### Test 1 — `POST /api/v1/subscriptions/plans` — Créer un plan

**Body :**
```json
{
  "platform_id": "<platform_id>",
  "name": "Pro",
  "slug": "pro",
  "description": "Plan professionnel",
  "prices": [
    {
      "billing_cycle": "monthly",
      "price": "29.99",
      "currency": "EUR"
    }
  ],
  "quotas": [
    {
      "quota_key": "api_calls",
      "limit_value": 10000,
      "overage_policy": "hard"
    }
  ]
}
```

**Champs expliqués :**

| Champ | Rôle |
|-------|------|
| `price` | Montant du prix (⚠️ pas `amount`) |
| `billing_cycle` | `monthly`, `yearly` ou `custom` |
| `quota_key` | Identifiant du quota (⚠️ pas `feature_key`) |
| `limit_value` | Limite maximale du quota (⚠️ pas `limit`) |
| `overage_policy` | `hard` = bloqué au dépassement · `soft` = autorisé |

**Réponse attendue (201 Created) :**
```json
{
  "id": "<plan_id>",
  "name": "Pro",
  "slug": "pro",
  "description": "Plan professionnel",
  "is_free": false,
  "tier_order": 0,
  "prices": [
    {
      "id": "<price_id>",
      "billing_cycle": "monthly",
      "price": 29.99,
      "currency": "EUR"
    }
  ],
  "quotas": [
    {
      "quota_key": "api_calls",
      "limit_value": 10000,
      "is_cyclical": true,
      "overage_policy": "hard",
      "overage_unit_price": 0
    }
  ]
}
```

**Erreurs possibles :**

| Code | Message | Cause |
|------|---------|-------|
| 400 | `platform_id, name et slug requis.` | Champs obligatoires manquants |
| 409 | `Slug existe deja pour cette plateforme.` | Doublon de slug |

---

### Test 2 — `GET /api/v1/subscriptions/plans` — Lister les plans

```
GET /api/v1/subscriptions/plans?platform_id=<platform_id>
```

**Réponse attendue (200 OK) :**
```json
{
  "data": [
    {
      "id": "<plan_id>",
      "name": "Pro",
      "slug": "pro",
      "is_free": false,
      "tier_order": 0,
      "platform_id": "<platform_id>"
    }
  ],
  "page": 1,
  "total": 1
}
```

---

### Test 3 — `GET /api/v1/subscriptions/plans/{id}` — Détail d'un plan

Retourne le plan complet avec ses prix et quotas.

---

### Test 4 — `PUT /api/v1/subscriptions/plans/{id}` — Modifier un plan

```json
{
  "name": "Pro Plus",
  "description": "Plan professionnel amélioré"
}
```

**Réponse attendue (200 OK) :**
```json
{
  "id": "<plan_id>",
  "name": "Pro Plus",
  "message": "Plan updated"
}
```

---

### Test 5 — `POST /api/v1/subscriptions/plans/{id}/archive` — Archiver un plan

Pas de body requis. Le plan passe à `is_active: false`.

> ⚠️ Un plan avec des abonnements actifs ne peut pas être archivé → retourne 409.

**Réponse attendue (200 OK) :**
```json
{
  "message": "Plan archived",
  "is_active": false
}
```

---

## 12. Bloc 2 — Abonnements

### Rôle
Gérer le cycle de vie complet d'un abonnement : création, activation, annulation, réactivation, changement de plan avec calcul de prorata automatique.

---

### Test 1 — `POST /api/v1/subscriptions` — Créer un abonnement

**Body :**
```json
{
  "platform_id": "<platform_id>",
  "subscriber_id": "<user_id>",
  "subscriber_type": "user",
  "plan_id": "<plan_id>",
  "billing_cycle": "monthly"
}
```

**Champs expliqués :**

| Champ | Rôle |
|-------|------|
| `subscriber_id` | UUID de l'utilisateur (⚠️ pas `user_id`) |
| `subscriber_type` | `user` ou `organization` |
| `billing_cycle` | Doit correspondre à un prix existant du plan |

> ⚠️ Un seul abonnement actif par subscriber → retourne 409 si déjà actif.

**Réponse attendue (201 Created) :**
```json
{
  "id": "<subscription_id>",
  "status": "pending_payment",
  "plan": "Pro",
  "current_period_start": "2026-04-17T19:25:42+00:00",
  "current_period_end": "2026-05-17T19:25:42+00:00",
  "trial_end": null,
  "message": "Subscription created"
}
```

---

### Test 2 — `GET /api/v1/subscriptions/list` — Lister les abonnements

```
GET /api/v1/subscriptions/list?platform_id=<platform_id>
```

Filtres disponibles : `platform_id`, `subscriber_id`, `status`.

---

### Test 3 — `GET /api/v1/subscriptions/{id}` — Détail d'un abonnement

Retourne le détail complet avec `quotas_usage` par quota.

---

### Test 4 — `POST /api/v1/subscriptions/{id}/activate` — Activer un abonnement

Pas de body. Passe le statut de `pending_payment` ou `trial` à `active`.

> ℹ️ Si le plan est gratuit (`is_free: true`), l'abonnement est activé automatiquement à la création.

**Réponse attendue (200 OK) :**
```json
{
  "id": "<subscription_id>",
  "status": "active",
  "message": "Subscription activated"
}
```

**Erreurs possibles :**

| Code | Message | Cause |
|------|---------|-------|
| 400 | `cannot_activate` | Statut actuel n'est pas `pending_payment` ou `trial` |

---

### Test 5 — `POST /api/v1/subscriptions/{id}/cancel` — Annuler un abonnement

Pas de body. Met `cancel_at_period_end: true` — l'abonnement reste actif jusqu'à la fin du cycle courant.

**Réponse attendue (200 OK) :**
```json
{
  "id": "<subscription_id>",
  "status": "active",
  "cancel_at_period_end": true,
  "message": "Subscription will cancel at period end"
}
```

---

### Test 6 — `POST /api/v1/subscriptions/{id}/reactivate` — Réactiver un abonnement

Annule une annulation en cours (`cancel_at_period_end` repasse à `false`).

**Réponse attendue (200 OK) :**
```json
{
  "id": "<subscription_id>",
  "status": "active",
  "message": "Subscription reactivated"
}
```

---

### Test 7 — `POST /api/v1/subscriptions/{id}/change-plan` — Changer de plan

**Body :**
```json
{
  "new_plan_id": "<nouveau_plan_id>",
  "billing_cycle": "monthly"
}
```

> ⚠️ Le champ s'appelle `new_plan_id` (pas `plan_id`).

Le calcul de prorata est automatique :
- `prorate_credit` = jours restants × prix journalier ancien plan
- `prorate_debit` = jours restants × prix journalier nouveau plan
- `amount_due` = max(0, debit − credit)

**Réponse attendue (200 OK) :**
```json
{
  "subscription_id": "<subscription_id>",
  "old_plan": "Pro",
  "new_plan": "Basic",
  "event_type": "downgraded",
  "prorate_credit": 28.99,
  "prorate_debit": 4.82,
  "amount_due": 0.0,
  "message": "Plan changed"
}
```

**Erreurs possibles :**

| Code | Message | Cause |
|------|---------|-------|
| 404 | `new_plan_not_found` | Plan archivé, inexistant, ou mauvais `platform_id` |
| 400 | `same_plan` | Même plan que l'abonnement actuel |
| 409 | `subscription_not_active` | Abonnement non actif |
| 400 | `new_price_not_found` | Pas de prix pour ce `billing_cycle` sur le nouveau plan |

---

## 13. Bloc 3 — Quotas

### Rôle
Exposer les quotas en temps réel. Les autres services appellent ces endpoints avant et après chaque action pour vérifier et consommer les limites définies dans le plan.

> ⚠️ **Préfixe correct :** les endpoints quotas sont sous `/api/v1/subscriptions/quotas/` (pas `/api/v1/quotas/`).

---

### Test 1 — `POST /api/v1/subscriptions/quotas/check` — Vérifier un quota

**Body :**
```json
{
  "platform_id": "<platform_id>",
  "subscriber_id": "<user_id>",
  "subscriber_type": "user",
  "quota_key": "api_calls",
  "requested": 1
}
```

**Réponse attendue (200 OK) :**
```json
{
  "allowed": true,
  "quota_key": "api_calls",
  "limit": 10000,
  "used": 0,
  "remaining": 10000,
  "overage": 0,
  "overage_policy": "hard"
}
```

> Si `allowed: false` et `overage_policy: "hard"` → l'action doit être bloquée côté appelant.

---

### Test 2 — `POST /api/v1/subscriptions/quotas/increment` — Consommer du quota

**Body :**
```json
{
  "platform_id": "<platform_id>",
  "subscriber_id": "<user_id>",
  "subscriber_type": "user",
  "quota_key": "api_calls",
  "amount": 10
}
```

**Réponse attendue (200 OK) :**
```json
{
  "quota_key": "api_calls",
  "used": 10,
  "limit": 10000,
  "overage": 0
}
```

---

### Test 3 — `GET /api/v1/subscriptions/{id}/usage` — Usage d'un abonnement

**Réponse attendue (200 OK) :**
```json
{
  "subscription_id": "<subscription_id>",
  "quotas": [
    {
      "quota_key": "api_calls",
      "used": 10,
      "limit": 10000,
      "remaining": 9990,
      "overage": 0,
      "policy": "hard"
    }
  ]
}
```

---

### Test 4 — `POST /api/v1/subscriptions/quotas/reserve` — Réserver du quota

Réservation atomique avant une opération longue. Le quota est verrouillé sans être consommé définitivement.

**Body :**
```json
{
  "platform_id": "<platform_id>",
  "subscriber_id": "<user_id>",
  "subscriber_type": "user",
  "quota_key": "api_calls",
  "amount": 5
}
```

**Réponse attendue (200 OK) :**
```json
{
  "reservation_id": "<reservation_id>",
  "amount": 5,
  "expires_at": "2026-04-17T20:09:28+00:00"
}
```

> Notez le `reservation_id` — il sera utilisé pour confirm ou release.

---

### Test 5 — `POST /api/v1/subscriptions/quotas/confirm` — Confirmer une réservation

Consomme définitivement le quota réservé.

**Body :**
```json
{
  "reservation_id": "<reservation_id>"
}
```

**Réponse attendue (200 OK) :**
```json
{
  "quota_key": "api_calls",
  "used": 15,
  "limit": 10000,
  "overage": 0
}
```

---

### Test 6 — `POST /api/v1/subscriptions/quotas/release` — Libérer une réservation

Annule la réservation sans consommer le quota.

**Body :**
```json
{
  "reservation_id": "<reservation_id>"
}
```

**Réponse attendue (200 OK) :**
```json
{
  "released": true
}
```

---

## 14. Bloc 4 — Organizations

### Rôle
Gestion des organisations B2B — permet à plusieurs utilisateurs de partager un abonnement sous une entité commune.

---

### Test 1 — `POST /api/v1/organizations` — Créer une organisation

**Body :**
```json
{
  "platform_id": "<platform_id>",
  "name": "AGT Corp",
  "owner_user_id": "<user_id>"
}
```

> ⚠️ Le champ s'appelle `owner_user_id` (pas `owner_id`).
> Le owner est automatiquement ajouté comme membre avec le rôle `owner` à la création.

**Réponse attendue (201 Created) :**
```json
{
  "id": "<org_id>",
  "platform_id": "<platform_id>",
  "name": "AGT Corp",
  "owner_user_id": "<user_id>",
  "is_active": true
}
```

---

### Test 2 — `GET /api/v1/organizations` — Lister les organisations

```
GET /api/v1/organizations?platform_id=<platform_id>
```

---

### Test 3 — `POST /api/v1/organizations/{id}/members` — Ajouter un membre

**Body :**
```json
{
  "user_id": "<user_id>",
  "role": "member"
}
```

Rôles disponibles : `owner`, `admin`, `member`.

> ℹ️ Retourne 409 `"Utilisateur déjà membre."` si l'utilisateur est déjà dans l'organisation — comportement normal, pas un bug.

**Réponse attendue (201 Created) :**
```json
{
  "id": "<member_id>",
  "user_id": "<user_id>",
  "role": "member"
}
```

---

### Test 4 — `GET /api/v1/organizations/{id}/members` — Lister les membres

**Réponse attendue (200 OK) :**
```json
{
  "organization_id": "<org_id>",
  "members": [
    {
      "id": "<member_id>",
      "user_id": "<user_id>",
      "role": "owner",
      "joined_at": "2026-04-17T20:07:29+00:00"
    }
  ]
}
```

---

### Test 5 — `DELETE /api/v1/organizations/{id}/members/{user_id}` — Retirer un membre

Retourne **204 No Content** en cas de succès — pas de body dans la réponse.

---

## 15. Bloc 5 — Config plateforme

### Rôle
Configurer les paramètres globaux d'une plateforme : durée du trial, grace period, cycles autorisés, devise par défaut.

---

### Test 1 — `GET /api/v1/subscriptions/config/{platform_id}` — Lire la config

**Réponse attendue (200 OK) :**
```json
{
  "platform_id": "<platform_id>",
  "trial_days": 0,
  "grace_period_days": 0,
  "allowed_cycles": [],
  "default_currency": "XAF"
}
```

> ℹ️ La config est créée automatiquement avec les valeurs par défaut si elle n'existe pas encore.

---

### Test 2 — `PUT /api/v1/subscriptions/config/{platform_id}` — Mettre à jour la config

**Body :**
```json
{
  "default_trial_days": 14,
  "grace_period_days": 3,
  "default_currency": "EUR"
}
```

> ⚠️ Dans le body du PUT, utiliser `default_trial_days` (pas `trial_days`).

**Réponse attendue (200 OK) :**
```json
{
  "platform_id": "<platform_id>",
  "trial_days": 14,
  "grace_period_days": 3,
  "allowed_cycles": [],
  "default_currency": "EUR",
  "message": "Config updated"
}
```

---

## 16. Flux inter-services

### Subscription → Payment
Lors de la création d'un abonnement (`pending_payment`), Subscription publie un event RabbitMQ vers Payment pour initier la transaction de paiement.

### Subscription → Notification
Lors des transitions d'état clés, Subscription publie des events vers Notification via RabbitMQ :
- Activation → email de bienvenue
- Annulation → email de confirmation
- Expiration → email d'alerte
- Quota à 80% → email d'alerte quota

### Autres services → Subscription
Les services qui ont besoin de vérifier les quotas (Chatbot, Search, Media...) appellent directement :
```
POST /api/v1/subscriptions/quotas/check    ← avant chaque action
POST /api/v1/subscriptions/quotas/increment ← après chaque action réussie
```

Tous ces appels inter-services utilisent un token S2S dans le header `Authorization: Bearer <s2s_token>`.

### Celery Beat — Tâches automatiques

| Tâche | Fréquence | Rôle |
|-------|-----------|------|
| `renew_expiring_subscriptions` | Toutes les heures (h:00) | Renouveler les abonnements expirant dans 24h |
| `process_expired_subscriptions` | Toutes les heures (h:15) | Passer les abonnements expirés en grace puis expired |
| `expire_stale_quota_reservations` | Toutes les 10 minutes | Expirer les réservations pending trop vieilles |
| `send_quota_alerts` | Toutes les heures (h:30) | Alertes quota à 80% vers Notification |

---

## 17. Bugs connus

| # | Bug | Fichier | Correction |
|---|-----|---------|------------|
| 1 | `Failed to load API definition` dans Swagger | `config/settings.py` | Ajouter `"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"` dans `REST_FRAMEWORK` |
| 2 | `AUTH_PUBLIC_KEY non configure.` (401) | `config/settings.py` | Charger le contenu du fichier PEM en mémoire après `AUTH_SERVICE_PUBLIC_KEY_PATH` |
| 3 | Celery worker absent au démarrage | `config/__init__.py` | Ajouter `from .celery import app as celery_app` + `__all__ = ("celery_app",)` |
| 4 | `KeyError: 'price'` (500) sur POST plan | `views.py` ligne ~109 | Utiliser le champ `price` dans l'objet prices (pas `amount`) |
| 5 | `null value in column "subscriber_id"` (500) | `views.py` | Utiliser `subscriber_id` dans le body (pas `user_id`) |
| 6 | `new_plan_not_found` sur change-plan | `views.py` | Utiliser `new_plan_id` dans le body (pas `plan_id`) |
| 7 | `AttributeError: trial_days` (500) sur GET/PUT config | `views.py` classe `PlatformConfigView` | Remplacer `config.trial_days` par `config.default_trial_days` partout dans la vue |
| 8 | Migrations absentes du repo | Tous les apps | Toujours exécuter `makemigrations` + `migrate` au premier démarrage |

---

## 18. Troubleshooting

| Symptôme | Cause probable | Solution |
|----------|---------------|----------|
| `Failed to load API definition` | `DEFAULT_SCHEMA_CLASS` manquant | Voir Bug #1 dans settings.py |
| `AUTH_PUBLIC_KEY non configure.` (401) | Clé PEM non chargée en mémoire | Copier la clé (section 4.2) + rebuild |
| Token expiré (401) | JWT expire après 15 minutes | Relancer la commande PowerShell de login |
| `SENDGRID_API_KEY non configuré` dans les logs | Warning informatif — non bloquant | Ignorer — `SMTPProvider` est en premier dans `PROVIDER_MAP` |
| Email non reçu dans Mailpit | S2S Notification non configuré ou worker en erreur | Vérifier `S2S_CLIENT_ID/SECRET` dans `agt-notification/.env` puis `docker logs agt-notif-worker` |
| `new_plan_not_found` (404) | Plan archivé ou champ `plan_id` au lieu de `new_plan_id` | Créer un nouveau plan actif et utiliser `new_plan_id` |
| `Utilisateur déjà membre.` (409) sur organizations | Comportement attendu | Le owner est automatiquement ajouté à la création — pas un bug |
| Worker absent (`agt-sub-worker`) | `config/__init__.py` vide | Voir Bug #3 |
| 500 sur GET/PUT config | Bug `trial_days` | Voir Bug #7 |
| `KeyError: 'price'` (500) | Mauvais nom de champ dans le body | Utiliser `price` (pas `amount`) dans l'objet prices |

---

## 19. Commandes utiles

```powershell
# Lancer le MVP
.\reset_mvp.ps1

# Health check Subscription
curl http://localhost:7004/api/v1/subscriptions/health

# Migrations Subscription
docker compose exec -e DJANGO_SETTINGS_MODULE=config.settings subscription python manage.py makemigrations plans subscriptions quotas organizations
docker compose exec subscription python manage.py migrate

# Tests automatisés (30 tests)
docker compose exec subscription python -m pytest -v

# Logs du service
docker logs agt-sub-service --tail=30

# Logs Celery worker
docker logs agt-sub-worker --tail=30 --follow

# Logs Celery beat
docker logs agt-sub-beat --tail=30

# Rebuild complet
cd agt-subscription
docker compose down
docker compose up -d --build
cd ..

# Rebuild service uniquement (après modification de code)
cd agt-subscription
docker compose up -d --build subscription
cd ..

# Obtenir et stocker un token frais (PowerShell)
$r = Invoke-RestMethod -Uri "http://localhost:7000/api/v1/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"email": "test@agt.com", "password": "Test1234!", "method": "email", "platform_id": "<platform_id>"}'
$token = $r.access_token
$token | Set-Clipboard

# Appel API Subscription avec token (PowerShell)
Invoke-RestMethod -Uri "http://localhost:7004/api/v1/subscriptions/..." `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"Authorization" = "Bearer $token"} `
  -Body '{ ... }'
```

---

## Ce qui reste à tester et documenter

Ce guide s'arrête ici. Les points suivants sont à tester, valider et documenter en suivant la même méthode :

| Groupe | Endpoints principaux |
|--------|---------------------|
| **Abonnements avec trial** | `POST /subscriptions` avec `with_trial: true` + vérification du statut `trial` |
| **Renouvellement automatique** | Vérifier les logs Celery Beat après expiration d'un cycle |
| **Flux Payment complet** | Activation via event RabbitMQ depuis Payment (au lieu d'activation manuelle) |
| **Quota hard limit** | Vérifier le blocage quand `used >= limit` avec `overage_policy: hard` |
| **Abonnements organization** | `subscriber_type: organization` + lier un abonnement à une org |
| **Admin stats** | `GET /api/v1/subscriptions/admin/stats` |

**Compte de test disponible après avoir suivi ce guide :**

| Ressource | Valeur |
|-----------|--------|
| Utilisateur de test | `test@agt.com` / `Test1234!` — vérifié |
| Platform ID | Celui créé à l'Étape 3 de la section 10 |
| Plan de référence | Plan Pro avec quota `api_calls: 10000` |

---

*GUIDE_SUBSCRIPTION.md — AG Technologies — 17 avril 2026*
*Testé et validé sur Subscription Service v1.0 — 30/30 tests*