# GUIDE_PAYMENT — Service de Paiement AGT

> **AG Technologies — Usage interne — Confidentiel**
> Version 1.2 — Avril 2026
> Statut : Validé et testé

---

## Table des matières

1. [Vue d'ensemble](#1-vue-densemble)
2. [Architecture et rôle dans l'écosystème](#2-architecture-et-rôle-dans-lécosystème)
3. [Prérequis et dépendances](#3-prérequis-et-dépendances)
4. [Lancer le service](#4-lancer-le-service)
5. [Variables d'environnement](#5-variables-denvironnement)
6. [Authentification — obtenir un token](#6-authentification--obtenir-un-token)
7. [Scénario complet pas à pas](#7-scénario-complet-pas-à-pas)
8. [Référence des endpoints](#8-référence-des-endpoints)
9. [Flux inter-services](#9-flux-inter-services)
10. [Concepts clés](#10-concepts-clés)
11. [Intégration des vrais providers](#11-intégration-des-vrais-providers)
12. [Tests automatisés](#12-tests-automatisés)
13. [Troubleshooting](#13-troubleshooting)
14. [Points d'attention et écarts connus](#14-points-dattention-et-écarts-connus)

---

## 1. Vue d'ensemble

Le Service Payment est le **exécutant financier centralisé** de l'écosystème AGT. Il gère l'exécution des transactions via les providers de paiement externes (Orange Money, MTN MoMo, Stripe, PayPal).

| Attribut | Valeur |
|---|---|
| Port | **7005** |
| Base URL | `http://localhost:7005/api/v1` |
| Swagger UI | `http://localhost:7005/api/v1/docs/` |
| ReDoc | `http://localhost:7005/api/v1/redoc/` |
| Stack | Python 3.11 / Django 5 / DRF |
| Base de données | PostgreSQL (port 5436 sur hôte) |
| Cache | Redis (port 6383 sur hôte) |
| Message broker | RabbitMQ partagé (agt-rabbitmq:5672) |

### Principe fondamental

> Payment est un **exécutant pur**. Il ne décide pas quoi facturer ni combien. Il reçoit un ordre (montant, devise, provider), l'exécute et rapporte le résultat.

La séparation des responsabilités est stricte :

| Service | Responsabilité |
|---|---|
| **Subscription** | Décide quoi facturer (plans, quotas) |
| **Payment** | Exécute la transaction via le provider |
| **Wallet** | Répartit les fonds (commissions, soldes) |

### Ce que Payment fait

- Initier des paiements via Orange Money, MTN MoMo, Stripe, PayPal
- Recevoir et traiter les webhooks des providers
- Maintenir l'historique complet de chaque transaction
- Émettre des événements RabbitMQ après chaque résultat
- Gérer l'idempotence (zéro double facturation)
- Réconciliation provider ↔ base interne

### Ce que Payment ne fait PAS

- Authentification des utilisateurs (→ Auth)
- Gestion des abonnements et quotas (→ Subscription)
- Répartition des fonds et commissions (→ Wallet)
- Profils utilisateurs (→ Users)
- Remboursements (phase 2)

---

## 2. Architecture et rôle dans l'écosystème

### Diagramme de flux

```
Subscription ──[RabbitMQ: subscription.payment_required]──► Payment
                                                                │
                                          ┌─────────────────────┤
                                          │                     │
                                    Orange Money          Stripe/PayPal
                                    MTN MoMo             (redirect URL)
                                    (USSD push)               │
                                          │                     │
                                    ◄─── webhook ──────────────┘
                                          │
                                    Payment met à jour la transaction
                                          │
                    ┌─────────────────────┼────────────────────┐
                    │                     │                    │
              [payment.confirmed]  [payment.failed]  [payment.cancelled]
                    │                     │                    │
                 Wallet              Subscription          Notification
              (crédit compte)      (marquer échec)       (alerter user)
```

### Les 4 providers supportés

| Provider | Type | Marché | Comportement |
|---|---|---|---|
| `orange_money` | Mobile Money | Cameroun | Push USSD sur téléphone → user tape PIN |
| `mtn_momo` | Mobile Money | Cameroun | Push USSD sur téléphone → user tape PIN |
| `stripe` | Carte bancaire | International | Retourne URL checkout Stripe |
| `paypal` | Wallet externe | International | Retourne URL checkout PayPal |

### Machine à états d'une transaction

```
[création] ──► pending
pending    ──► processing    (provider a accusé réception)
pending    ──► succeeded     (confirmation instantanée)
pending    ──► failed        (rejet immédiat provider)
pending    ──► expired       (TTL dépassé sans réponse)
pending    ──► cancelled     (annulation avant traitement)
processing ──► succeeded     (webhook confirmation)
processing ──► failed        (webhook échec)
processing ──► expired       (TTL dépassé en cours de traitement)
```

**États terminaux** (aucune transition sortante) : `succeeded`, `failed`, `expired`, `cancelled`

### TTL par provider

| Provider | TTL | Raison |
|---|---|---|
| orange_money | 5 min | Le push USSD expire rapidement |
| mtn_momo | 5 min | Idem |
| stripe | 30 min | Session Stripe Checkout |
| paypal | 1 heure | Session PayPal |

---

## 3. Prérequis et dépendances

### Services requis

| Service | Port | Rôle |
|---|---|---|
| **Auth** | 7000 | Validation des tokens JWT et S2S |
| **RabbitMQ** | 5672 | Événements sortants (payment.confirmed, etc.) |

> ⚠️ Auth doit être lancé AVANT Payment. RabbitMQ doit être accessible sur `agt_network`.

### Fichiers requis

- `agt-payment/.env` — variables d'environnement (copié depuis `.env.example`)
- `agt-payment/keys/auth_public.pem` — clé publique RSA d'Auth pour valider les JWT

### Pourquoi `auth_public.pem` ?

Payment valide lui-même les tokens JWT reçus grâce à cette clé publique RSA. Auth signe les tokens avec sa clé privée, Payment les vérifie avec la clé publique. Cela évite un appel réseau à Auth à chaque requête.

---

## 4. Lancer le service

### Premier lancement

```bash
# 1. Aller dans le dossier du service
cd agt-payment

# 2. Lancer le service
bash scripts/setup.sh

# 3. Générer et appliquer les migrations (OBLIGATOIRE au premier lancement)
docker exec agt-pay-service python manage.py makemigrations payments
docker exec agt-pay-service python manage.py migrate
```

> ⚠️ **Les migrations ne sont pas committées dans le dépôt.** Elles doivent être générées manuellement au premier lancement ou après un `--clean`. Sans cette étape, le service démarre mais toutes les requêtes échouent avec des erreurs de table manquante.

### Lancements suivants

```bash
# Rebuild après modification de code
docker compose up -d --build

# Rebuild complet sans cache (si le code ne semble pas mis à jour)
docker compose build --no-cache
docker compose up -d
```

### Vérification du démarrage

```bash
# Vérifier les containers
docker compose ps

# Vérifier les logs
docker logs agt-pay-service --tail=30

# Health check
curl http://localhost:7005/api/v1/payments/health
```

Réponse attendue :

```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "rabbitmq": "ok",
  "version": "1.2.0"
}
```

> **Note :** `rabbitmq: "unavailable"` est normal si RabbitMQ n'est pas sur le même réseau Docker. Voir section Troubleshooting.

### Arrêter le service

```bash
# Arrêter sans supprimer les données
docker compose down

# Arrêter ET supprimer les données (reset complet)
docker compose down -v
```

---

## 5. Variables d'environnement

Fichier : `agt-payment/.env.example`

```env
# === Service Django ===
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# === Base de données PostgreSQL ===
DATABASE_URL=postgresql://pay_user:pay_password@db:5432/agt_payment_db

# === Redis (cache JWT, replay protection webhooks) ===
REDIS_URL=redis://redis:6379/5

# === Auth — clé publique RSA pour valider les tokens JWT ===
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem

# === RabbitMQ — broker pour les événements sortants ===
# Utiliser les credentials du RabbitMQ partagé AGT
BROKER_URL=amqp://agt_rabbit:agt_rabbit_password@agt-rabbitmq:5672//

# === CORS ===
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

> ⚠️ `keys/auth_public.pem` doit être copié manuellement depuis `agt-auth/keys/public.pem` si Payment est lancé sans `deploy_mvp.sh`.

---

## 6. Authentification — obtenir un token

Tous les endpoints Payment (sauf `/health` et les webhooks) nécessitent un token JWT dans le header :

```
Authorization: Bearer <access_token>
```

### Obtenir un token utilisateur

Sur Swagger Auth (`http://localhost:7000/api/v1/docs/`), appelez `POST /auth/login` :

```json
{
  "email": "votre@email.com",
  "password": "VotreMotDePasse"
}
```

Récupérez le champ `access_token` dans la réponse.

> ⚠️ Les tokens expirent en **15 minutes**. En cas d'erreur 401, reconnectez-vous.

### Utiliser le token dans Swagger Payment

1. Ouvrez `http://localhost:7005/api/v1/docs/`
2. Cliquez **Authorize** en haut à droite
3. Collez votre `access_token`
4. Cliquez **Authorize** puis **Close**

### Token S2S (inter-services)

La route `DELETE /payments/by-user/{userId}` (purge RGPD) nécessite un token S2S.

Pour obtenir un token S2S :

```bash
# Sur Swagger Auth : POST /auth/s2s/token
{
  "client_id": "<platform_id>",
  "client_secret": "<client_secret>"
}
```

---

## 7. Scénario complet pas à pas

Ce scénario couvre le flux complet depuis la configuration jusqu'à l'initiation d'un paiement.

### Étape 1 — Créer les providers

Avant tout paiement, les providers doivent être enregistrés en base. **À faire une seule fois.**

Sur Swagger, `POST /payments/providers` pour chaque provider :

**Orange Money :**
```json
{
  "provider": "orange_money",
  "display_name": "Orange Money Cameroun",
  "credentials": {
    "api_key": "votre-api-key-orange",
    "api_secret": "votre-api-secret-orange"
  },
  "api_base_url": "https://api.orange.com/orange-money-webpay/dev/v1",
  "webhook_secret": "votre-webhook-secret",
  "supported_currencies": ["XAF"]
}
```

**MTN MoMo :**
```json
{
  "provider": "mtn_momo",
  "display_name": "MTN Mobile Money Cameroun",
  "credentials": {
    "api_key": "votre-api-key-mtn",
    "api_secret": "votre-api-secret-mtn"
  },
  "api_base_url": "https://sandbox.momodeveloper.mtn.com",
  "webhook_secret": "votre-webhook-secret-mtn",
  "supported_currencies": ["XAF"]
}
```

**Stripe :**
```json
{
  "provider": "stripe",
  "display_name": "Stripe",
  "credentials": {"secret_key": "sk_test_xxx"},
  "api_base_url": "https://api.stripe.com/v1",
  "webhook_secret": "whsec_xxx",
  "supported_currencies": ["XAF", "EUR", "USD"]
}
```

**PayPal :**
```json
{
  "provider": "paypal",
  "display_name": "PayPal",
  "credentials": {
    "client_id": "votre-paypal-client-id",
    "client_secret": "votre-paypal-secret"
  },
  "api_base_url": "https://api-m.sandbox.paypal.com",
  "webhook_secret": "votre-paypal-webhook-secret",
  "supported_currencies": ["EUR", "USD"]
}
```

### Étape 2 — Configurer les providers pour votre plateforme

Récupérez votre `platform_id` depuis Auth (`GET /auth/platforms`), puis :

```json
PUT /payments/platforms/{platform_id}/providers

{
  "providers": [
    {"provider": "orange_money", "priority": 1, "is_active": true},
    {"provider": "mtn_momo", "priority": 2, "is_active": true},
    {"provider": "stripe", "priority": 3, "is_active": true}
  ],
  "default_currency": "XAF"
}
```

> La **priorité** détermine l'ordre de fallback : si Orange Money échoue, MTN MoMo est tenté automatiquement.

### Étape 3 — Initier un paiement

```json
POST /payments/initiate

{
  "platform_id": "votre-platform-uuid",
  "user_id": "uuid-de-l-utilisateur",
  "provider": "orange_money",
  "amount": 15000,
  "currency": "XAF",
  "source": "subscription",
  "source_reference_id": "uuid-de-l-abonnement",
  "idempotency_key": "uuid-unique-par-intention-de-paiement",
  "phone_number": "+237600000000",
  "metadata": {
    "plan_name": "Pro",
    "reason": "renewal"
  }
}
```

**Réponse (Mobile Money) :**
```json
{
  "transaction_id": "tx-uuid",
  "status": "pending",
  "provider": "orange_money",
  "amount": 15000,
  "currency": "XAF",
  "message": "USSD push sent, waiting for user confirmation"
}
```

**Réponse (Stripe/PayPal) :**
```json
{
  "transaction_id": "tx-uuid",
  "status": "pending",
  "provider": "stripe",
  "amount": 15000,
  "currency": "XAF",
  "payment_url": "https://checkout.stripe.com/pay/cs_xxx",
  "message": "Redirect user to payment_url"
}
```

### Étape 4 — Suivre la transaction

```
GET /payments/{transaction_id}
```

La réponse inclut `status_history` qui trace chaque transition :

```json
{
  "id": "tx-uuid",
  "status": "succeeded",
  "confirmed_at": "2026-04-17T13:22:21Z",
  "status_history": [
    {"from": null, "to": "pending", "trigger": "api_call", "at": "..."},
    {"from": "pending", "to": "succeeded", "trigger": "webhook", "at": "..."}
  ]
}
```

---

## 8. Référence des endpoints

### Health

#### `GET /payments/health`

Vérifie l'état du service. **Aucune authentification requise.**

```bash
curl http://localhost:7005/api/v1/payments/health
```

Réponse 200 :
```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "rabbitmq": "ok",
  "version": "1.2.0"
}
```

---

### Paiements

#### `POST /payments/initiate`

Initie une transaction. Auth : Bearer token ou S2S.

| Champ | Type | Requis | Description |
|---|---|---|---|
| `platform_id` | UUID | ✅ | UUID de la plateforme (registre Auth) |
| `user_id` | UUID | ❌ | UUID de l'utilisateur payeur |
| `provider` | string | ✅ | `orange_money`, `mtn_momo`, `stripe`, `paypal` |
| `amount` | decimal | ✅ | Montant (ex: 15000) |
| `currency` | string | ✅ | Devise ISO 4217 (ex: XAF) |
| `source` | string | ✅ | `subscription`, `wallet`, `platform`, `manual` |
| `source_reference_id` | UUID | ❌ | ID de la ressource source |
| `idempotency_key` | UUID | ✅ | UUID unique par intention de paiement |
| `phone_number` | string | ❌* | Obligatoire pour Mobile Money |
| `metadata` | object | ❌ | Données libres transmises telles quelles |

*`phone_number` obligatoire pour `orange_money` et `mtn_momo`

**Codes HTTP :**

| Code | Signification |
|---|---|
| 201 | Transaction créée |
| 200 | Idempotent — transaction existante retournée |
| 400 | Champs requis manquants |
| 409 | Même `idempotency_key` mais payload différent |
| 422 | Provider a rejeté la transaction |

**Règle d'idempotence :**

L'`idempotency_key` garantit qu'une même intention de paiement n'est jamais exécutée deux fois :
- Première requête → 201 Created
- Même requête (retry) → 200 OK, transaction existante
- Même clé, montant différent → 409 Conflict

---

#### `GET /payments/{transactionId}`

Détail complet d'une transaction avec historique de statuts. Auth : Bearer ou S2S.

```bash
GET /payments/44ffa81a-302a-45c5-959f-c3ac943a31b1
```

Réponse 200 :
```json
{
  "id": "44ffa81a-302a-45c5-959f-c3ac943a31b1",
  "platform_id": "uuid",
  "user_id": "uuid",
  "provider": "orange_money",
  "amount": 15000,
  "currency": "XAF",
  "status": "succeeded",
  "source": "subscription",
  "source_reference_id": "uuid",
  "provider_tx_id": "OM-44ffa81a",
  "payment_url": null,
  "failure_reason": null,
  "confirmed_at": "2026-04-17T13:22:21Z",
  "created_at": "2026-04-17T12:26:00Z",
  "status_history": [
    {"from": null, "to": "pending", "trigger": "api_call", "at": "..."},
    {"from": "pending", "to": "succeeded", "trigger": "webhook", "at": "..."}
  ]
}
```

---

#### `GET /payments`

Liste les transactions avec filtres et pagination. Auth : Bearer ou S2S.

**Query params :**

| Paramètre | Description |
|---|---|
| `platform_id` | Filtrer par plateforme |
| `user_id` | Filtrer par utilisateur |
| `status` | `pending`, `processing`, `succeeded`, `failed`, `expired`, `cancelled` |
| `provider` | `orange_money`, `mtn_momo`, `stripe`, `paypal` |
| `source` | `subscription`, `wallet`, `platform`, `manual` |
| `from_date` | Date de début (YYYY-MM-DD) |
| `to_date` | Date de fin (YYYY-MM-DD) |

Réponse 200 :
```json
{
  "data": [...],
  "page": 1,
  "total": 42
}
```

---

#### `POST /payments/{transactionId}/cancel`

Annule un paiement en état `pending` uniquement. Auth : Bearer ou S2S.

```json
{
  "reason": "Annulation à la demande de l'utilisateur"
}
```

Réponse 200 :
```json
{
  "transaction_id": "uuid",
  "status": "cancelled",
  "message": "Payment cancelled"
}
```

**Codes HTTP :**

| Code | Signification |
|---|---|
| 200 | Annulation réussie |
| 400 | Transaction non en état pending |
| 404 | Transaction introuvable |

---

### Webhooks Providers

> ⚠️ Ces endpoints **n'ont pas d'authentification JWT**. Ils sont appelés par les providers externes (Orange Money, MTN, Stripe, PayPal). La sécurité se fait par signature HMAC et IP whitelist.

> ⚠️ Ces endpoints retournent **toujours 200 OK** — même en cas d'erreur interne — pour éviter que le provider ne relance des retries inutiles.

#### `POST /payments/webhooks/orange-money`
#### `POST /payments/webhooks/mtn-momo`
#### `POST /payments/webhooks/stripe`
#### `POST /payments/webhooks/paypal`

**Comportement commun :**

1. Vérifier la signature HMAC du webhook
2. Appliquer la protection anti-replay (Redis TTL 72h)
3. Normaliser le statut provider → statut AGT
4. Mettre à jour la transaction en base
5. Émettre l'événement RabbitMQ correspondant

**Normalisation des statuts :**

| Statut AGT | Orange Money | MTN MoMo | Stripe | PayPal |
|---|---|---|---|---|
| `succeeded` | SUCCESS | SUCCESSFUL | payment_intent.succeeded | COMPLETED |
| `failed` | FAILED | FAILED | payment_intent.payment_failed | VOIDED |
| `pending` | INITIATED | PENDING | payment_intent.created | CREATED |

**Test manuel (simulation provider) :**

```json
POST /payments/webhooks/orange-money

{
  "event_id": "evt-unique-001",
  "status": "SUCCESS",
  "transaction_id": "OM-44ffa81a"
}
```

Réponse : `{"received": true}`

---

### Configuration Providers

#### `POST /payments/providers`

Crée un provider. Auth : Bearer (admin global recommandé).

```json
{
  "provider": "orange_money",
  "display_name": "Orange Money Cameroun",
  "credentials": {"api_key": "xxx", "api_secret": "yyy"},
  "api_base_url": "https://api.orange.com/orange-money-webpay/dev/v1",
  "webhook_secret": "whsec_xxx",
  "supported_currencies": ["XAF"]
}
```

Codes : 201 Created, 409 Provider existe déjà.

---

#### `PUT /payments/providers/{provider}`

Modifie la configuration d'un provider. Seuls les champs fournis sont modifiés.

```json
{
  "display_name": "Orange Money Cameroun - Production",
  "api_base_url": "https://api.orange.com/orange-money-webpay/cm/v1",
  "is_active": true
}
```

Codes : 200, 404.

---

#### `GET /payments/providers`

Liste tous les providers actifs.

```json
{
  "data": [
    {
      "id": "uuid",
      "provider": "orange_money",
      "display_name": "Orange Money Cameroun",
      "supported_currencies": ["XAF"],
      "is_active": true
    }
  ]
}
```

---

#### `PUT /payments/platforms/{platformId}/providers`

Configure les providers actifs pour une plateforme avec leur ordre de priorité.

```json
{
  "providers": [
    {"provider": "orange_money", "priority": 1, "is_active": true},
    {"provider": "mtn_momo", "priority": 2, "is_active": true},
    {"provider": "stripe", "priority": 3, "is_active": true}
  ],
  "default_currency": "XAF"
}
```

> ⚠️ Tous les providers doivent exister en base avant d'être configurés. Une validation est effectuée.

---

### Administration

#### `GET /payments/admin/stats`

Statistiques globales des transactions.

**Query params :** `platform_id`, `provider`, `from_date`, `to_date`

Réponse 200 :
```json
{
  "total_transactions": 12450,
  "total_amount": 185000000,
  "currency": "XAF",
  "success_rate": 94.2,
  "by_provider": [
    {"provider": "orange_money", "count": 8200, "success_rate": 95.1},
    {"provider": "stripe", "count": 3100, "success_rate": 93.8}
  ]
}
```

---

#### `POST /payments/admin/{transactionId}/force-status`

Force manuellement le statut d'une transaction après vérification sur le dashboard du provider. Action tracée dans `status_history` avec `trigger: "admin_manual"`.

```json
{
  "status": "succeeded",
  "reason": "Verified manually via Orange Money dashboard"
}
```

**Statuts autorisés :** `succeeded` ou `failed` uniquement. Les transactions déjà en état terminal retournent 409.

---

#### `GET /payments/admin/reconciliation`

Liste les rapports de réconciliation provider ↔ transactions internes.

**Query params :** `provider`, `from_date`, `to_date`

> En mode test, cette liste est vide. Les rapports sont générés automatiquement par le cron Celery Beat toutes les 6 heures en production.

---

#### `DELETE /payments/by-user/{userId}`

**Purge RGPD.** Auth : S2S token obligatoire.

Anonymise les données personnelles (`user_id`, `phone_number`) de toutes les transactions liées à cet utilisateur. Les transactions sont **conservées** pour obligation comptable légale — seules les données personnelles sont mises à NULL.

Réponse 200 :
```json
{
  "user_id": "uuid",
  "transactions_anonymized": 5,
  "message": "Données personnelles anonymisées avec succès."
}
```

---

## 9. Flux inter-services

### Payment reçoit de

| Source | Mécanisme | Événement / Appel |
|---|---|---|
| Subscription | RabbitMQ | `subscription.payment_required` |
| Subscription | RabbitMQ | `subscription.overage_billing` |
| Users | REST | `DELETE /payments/by-user/{userId}` (RGPD) |
| Plateformes | REST | `POST /payments/initiate` |
| Providers externes | HTTP Webhook | `POST /payments/webhooks/*` |

### Payment émet vers

| Destination | Mécanisme | Événement | Déclencheur |
|---|---|---|---|
| Wallet | RabbitMQ | `payment.confirmed` | Transaction succeeded |
| Subscription | RabbitMQ | `payment.confirmed` | Transaction succeeded |
| Subscription | RabbitMQ | `payment.failed` | Transaction failed |
| Subscription | RabbitMQ | `payment.cancelled` | Transaction cancelled |
| Notification | RabbitMQ | `payment.confirmed` | Transaction succeeded |
| Notification | RabbitMQ | `payment.failed` | Transaction failed |
| Notification | RabbitMQ | `payment.cancelled` | Transaction cancelled |
| Notification | RabbitMQ | `payment.expired` | Transaction expired |

### Format standard d'un événement RabbitMQ

```json
{
  "event_id": "uuid-v4-unique",
  "event_type": "payment.confirmed",
  "timestamp": "2026-04-17T13:22:21Z",
  "source": "payment-service",
  "idempotency_key": "uuid",
  "data": {
    "payment_reference_id": "tx-uuid",
    "platform_id": "uuid",
    "user_id": "uuid",
    "provider": "orange_money",
    "amount": 15000,
    "currency": "XAF",
    "source": "subscription",
    "source_reference_id": "sub-uuid",
    "metadata": {},
    "confirmed_at": "2026-04-17T13:22:21Z"
  }
}
```

### Matrice d'autorisation

| Endpoint | JWT | S2S | Admin |
|---|---|---|---|
| `POST /payments/initiate` | ✅ | ✅ | |
| `GET /payments/{id}` | ✅ | ✅ | ✅ |
| `GET /payments` | ✅ | ✅ | ✅ |
| `POST /payments/{id}/cancel` | ✅ | ✅ | ✅ |
| `POST /payments/webhooks/*` | signature provider | | |
| `POST /payments/providers` | ✅* | | ✅* |
| `PUT /payments/providers/{p}` | ✅* | | ✅* |
| `PUT /payments/platforms/{id}/providers` | ✅* | | ✅* |
| `GET /payments/admin/stats` | ✅* | | ✅* |
| `POST /payments/admin/{id}/force-status` | ✅* | | ✅* |
| `GET /payments/admin/reconciliation` | ✅* | | ✅* |
| `DELETE /payments/by-user/{userId}` | | ✅ | ✅ |

*Restriction admin non encore implémentée strictement — voir section 14.

---

## 10. Concepts clés

### L'idempotence

Garantit qu'une même intention de paiement n'est jamais exécutée deux fois, même en cas de retry réseau ou de double-clic.

**Règle :** le client génère un UUID v4 unique par intention de paiement et le renvoie identique en cas de retry.

```
Premier appel  : idempotency_key "abc-123" → 201 Created
Retry réseau   : idempotency_key "abc-123" → 200 OK (transaction existante)
Montant changé : idempotency_key "abc-123" → 409 Conflict
```

### Le Strategy Pattern (providers)

Chaque provider est implémenté comme un adapter derrière une interface commune :

```python
class ProviderAdapter:
    def initiate_payment(self, tx) -> dict
    def normalize_webhook(self, payload) -> dict
    def verify_webhook(self, headers, payload) -> bool
```

Ajouter un nouveau provider = écrire un nouvel adapter dans `apps/providers/adapters.py`, sans modifier le code métier.

### La réconciliation

Toutes les 6 heures, un cron compare :
- Les transactions `succeeded` dans notre base
- Les transactions confirmées chez le provider

Anomalies détectées :
- **mismatched** : présentes des deux côtés mais montants différents
- **missing_provider** : présentes en interne, absentes chez le provider — critique
- **missing_internal** : présentes chez le provider, absentes en interne — anormal

### La purge RGPD

Les transactions ne sont **jamais supprimées** (obligation comptable légale). La purge RGPD met uniquement `user_id` et `phone_number` à NULL pour anonymiser les données personnelles tout en conservant la traçabilité financière.

---

## 11. Intégration des vrais providers

Quand vous êtes prêts à passer en production, voici la procédure pour chaque provider.

### Orange Money

1. Créer un compte développeur sur `https://developer.orange.com/`
2. Obtenir `api_key`, `api_secret` et `webhook_secret`
3. Configurer l'URL webhook sur le portail Orange :
   ```
   https://votre-domaine.com/api/v1/payments/webhooks/orange-money
   ```
4. Mettre à jour le provider via `PUT /payments/providers/orange_money` avec les vrais credentials
5. Changer `api_base_url` vers la production :
   ```
   https://api.orange.com/orange-money-webpay/cm/v1
   ```

### MTN MoMo

1. Créer un compte sur `https://momodeveloper.mtn.com/`
2. Suivre le même processus que Orange Money
3. URL webhook : `https://votre-domaine.com/api/v1/payments/webhooks/mtn-momo`

### Stripe

1. Créer un compte sur `https://stripe.com/`
2. Récupérer la clé secrète `sk_live_xxx` (production) ou `sk_test_xxx` (test)
3. Configurer le webhook sur le dashboard Stripe :
   ```
   https://votre-domaine.com/api/v1/payments/webhooks/stripe
   ```
4. Récupérer le `Signing Secret` (whsec_xxx) pour la vérification HMAC

### PayPal

1. Créer une application sur `https://developer.paypal.com/`
2. Obtenir `client_id` et `client_secret`
3. Configurer l'URL webhook dans le dashboard PayPal :
   ```
   https://votre-domaine.com/api/v1/payments/webhooks/paypal
   ```

> ⚠️ **Important :** implémenter la méthode `normalize_webhook()` dans l'adapter correspondant (`apps/providers/adapters.py`) pour que les statuts providers soient traduits correctement vers les statuts AGT internes.

---

## 12. Tests automatisés

```bash
# Lancer les tests
docker compose exec payment python -m pytest -v

# Avec couverture
docker compose exec payment python -m pytest --cov=apps -v
```

### Structure des tests

```
apps/payments/tests/
└── test_all.py    ← tests unitaires et d'intégration
```

### Ce que les tests couvrent

- Création et transitions de statut d'une transaction
- Idempotence sur `idempotency_key`
- Machine à états (transitions autorisées et interdites)
- Détection des états terminaux
- Expiration des transactions pending

---

## 13. Troubleshooting

### `rabbitmq: "unavailable"` dans le health check

**Cause 1 :** Le container Payment n'est pas sur le réseau `agt_network`.

Vérifier :
```bash
docker inspect agt-pay-service --format '{{json .NetworkSettings.Networks}}' | python3 -m json.tool
```

Le réseau `agt_network` doit apparaître. Si non, vérifier que `docker-compose.yml` contient :
```yaml
networks:
  - default
  - agt_network
```

**Cause 2 :** Mauvais credentials RabbitMQ dans `.env`.

Vérifier les credentials réels :
```bash
docker exec agt-rabbitmq env | grep RABBITMQ
```

Puis mettre à jour `.env` :
```env
BROKER_URL=amqp://agt_rabbit:agt_rabbit_password@agt-rabbitmq:5672//
```

**Note :** `rabbitmq: "unavailable"` n'affecte pas le statut global `"healthy"` — seuls DB et Redis sont critiques pour le fonctionnement de base.

---

### `No migrations to apply` alors que les tables manquent

Le dossier `migrations/` n'existe pas localement.

```bash
docker exec agt-pay-service python manage.py makemigrations payments
docker exec agt-pay-service python manage.py migrate
```

---

### `relation "transactions" does not exist`

Les migrations n'ont pas été appliquées. Exécutez la procédure de migrations ci-dessus.

---

### `401 Unauthorized` sur tous les endpoints

Le token JWT a expiré (durée de vie : 15 minutes).

Reconnectez-vous sur Auth Swagger, récupérez un nouveau token et re-autorisez sur Payment Swagger (Authorize → Logout → nouveau token).

---

### `409 Conflict` sur `POST /payments/initiate`

Vous avez envoyé la même `idempotency_key` avec un montant ou un provider différent. C'est une protection intentionnelle — changez l'`idempotency_key` si c'est une nouvelle intention de paiement.

---

### `400 Bad Request` sur `PUT /payments/platforms/{id}/providers`

Un provider dans la liste n'existe pas en base ou est inactif. Créez d'abord tous les providers via `POST /payments/providers` avant de les configurer pour une plateforme.

---

### Le code modifié n'est pas pris en compte après rebuild

Le service tourne en mode production (gunicorn) — les fichiers dans le container sont copiés au moment du build. Après toute modification de code :

```bash
docker compose build --no-cache
docker compose up -d
```

---

### `status_history` vide sur une transaction

Ce bug existait dans la version initiale. Il est corrigé dans la version actuelle — la création d'une transaction enregistre automatiquement l'entrée initiale `null → pending` dans `status_history`. Si vous voyez encore ce comportement, vérifiez que vous utilisez le code mis à jour et faites un rebuild.

---

## 14. Points d'attention et écarts connus

| # | Point | Statut |
|---|---|---|
| 1 | **Restriction admin non stricte** — les routes admin (`POST /providers`, `force-status`, etc.) acceptent n'importe quel token JWT valide, pas seulement les admins globaux. À implémenter sur tous les services en même temps. | ⚠️ Connu |
| 2 | **Credentials providers non chiffrés AES-256** — le CDC exige un chiffrement AES-256 des credentials avant stockage. Actuellement stockés en clair en JSON. | ⚠️ Phase 2 |
| 3 | **Adapters providers = mocks** — les adapters Orange Money, MTN, Stripe et PayPal sont des mocks de développement. Ils simulent des réponses sans contacter les vrais APIs. À implémenter lors de l'intégration production. | ℹ️ Attendu |
| 4 | **Cron Celery Beat non configuré** — la réconciliation automatique et l'expiration des transactions pending (cron) ne tournent pas. À ajouter avec Celery + Celery Beat. | ⚠️ Phase 2 |
| 5 | **Migrations non committées** — les fichiers de migration doivent être générés manuellement au premier lancement. | ℹ️ Convention AGT |
| 6 | **RabbitMQ non inclus dans docker-compose.yml** — Payment utilise le RabbitMQ partagé sur `agt_network`. Il ne démarre pas son propre RabbitMQ. | ℹ️ Attendu |

---

*AG Technologies — Service Payment v1.2 — Guide rédigé le 17 avril 2026*
*Confidentiel — Usage interne exclusivement*