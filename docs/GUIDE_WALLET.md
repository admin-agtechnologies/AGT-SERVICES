# GUIDE — Service Wallet

> **AG Technologies — Usage interne**
> Service Wallet v1.0 — Port 7006
> Dernière mise à jour : Avril 2026

---

## Table des matières

1. [Rôle du service](#1-rôle-du-service)
2. [Architecture interne](#2-architecture-interne)
3. [Lancer le service localement](#3-lancer-le-service-localement)
4. [Variables d'environnement](#4-variables-denvironnement)
5. [Conventions importantes](#5-conventions-importantes)
6. [Référence rapide des endpoints](#6-référence-rapide-des-endpoints)
7. [Scénario complet — Utilisation pas à pas](#7-scénario-complet--utilisation-pas-à-pas)
8. [Flux inter-services](#8-flux-inter-services)
9. [Double-entry bookkeeping — Explication](#9-double-entry-bookkeeping--explication)
10. [Bugs connus et points d'attention](#10-bugs-connus-et-points-dattention)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Rôle du service

Le service Wallet est le **ledger financier central de l'écosystème AGT**. Il est responsable de toutes les opérations monétaires qui transitent par la plateforme.

Il répond à une question fondamentale : **où est l'argent, et comment s'est-il déplacé ?**

Concrètement, il gère :

- Les **wallets** (comptes financiers) associés aux utilisateurs et aux plateformes
- Les **crédits et débits** avec une comptabilité en double entrée (double-entry bookkeeping)
- Les **virements** entre wallets
- Les **holds** (réservations de fonds) pour sécuriser des paiements avant leur capture
- Les **splits** (partages de commissions) entre plusieurs wallets en une seule transaction
- Les **règles de split** configurables par plateforme
- L'**audit du ledger** pour vérifier l'équilibre des écritures à tout moment
- Les **ajustements correctifs** administratifs

> **À retenir :** Wallet ne décide pas qui a le droit de faire quoi dans les règles métier — c'est le rôle du service Subscription. Wallet exécute les opérations financières demandées par les autres services.

> **Principe fondamental :** le ledger est **append-only**. Aucune écriture n'est jamais modifiée ni supprimée. Toute correction se fait par une nouvelle écriture dans le sens inverse.

---

## 2. Architecture interne

### 2.1 Structure des dossiers

```
agt-wallet/
├── apps/
│   ├── accounts/          # Modèles : Account, LedgerTransaction, LedgerEntry, Hold, SplitRule, CashoutRequest
│   │   └── migrations/    # Migrations Django
│   ├── ledger/            # Vues, URLs, service métier
│   │   ├── views.py       # Tous les endpoints
│   │   ├── urls.py        # Routage
│   │   └── service.py     # LedgerService — logique métier
│   ├── holds/             # App Django (vide — modèles dans accounts)
│   └── cashout/           # App Django (vide — modèles dans accounts)
├── common/
│   └── authentication.py  # JWTAuthentication + JWTPayload
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── keys/
│   └── auth_public.pem    # Clé publique RSA copiée depuis Auth
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

### 2.2 Modèles de données

#### Account — Le wallet

```
Account
├── id              UUID (PK)
├── account_type    CharField : "user" | "external" | "system"
├── owner_type      CharField : "user" | "platform" | "system"
├── owner_id        UUIDField (nullable) — auth_user_id de l'utilisateur
├── currency        CharField : "XAF" | "EUR" | "USD" ...
├── balance         DecimalField — solde total
├── hold_amount     DecimalField — montant réservé (holds actifs)
├── available_balance (propriété) = balance - hold_amount
├── status          CharField : "active" | "frozen"
├── label           CharField (nullable)
├── created_at      DateTimeField
└── updated_at      DateTimeField
```

**Types de comptes :**

- `user` : wallet appartenant à un utilisateur
- `external` : compte virtuel représentant l'extérieur (fournisseur de cash-in/out)
- `system` : compte interne à la plateforme

#### LedgerTransaction — La transaction

```
LedgerTransaction
├── id                   UUID (PK)
├── ledger_reference_id  CharField — référence lisible (ex: LTX-2026-000001)
├── idempotency_key      CharField(128) — clé unique pour éviter les doublons
├── transaction_type     CharField : "cashin" | "cashout" | "transfer" | "split"
├── platform_id          UUIDField — plateforme émettrice
├── source               CharField : "payment" | "platform" | "admin"
├── source_reference_id  CharField(128, nullable) — ID externe (ex: ID paiement)
├── description          CharField (nullable)
├── metadata             JSONField (nullable)
├── status               CharField : "completed"
└── created_at           DateTimeField
```

#### LedgerEntry — L'écriture comptable

```
LedgerEntry
├── id            UUID (PK)
├── transaction   ForeignKey → LedgerTransaction
├── account       ForeignKey → Account
├── direction     CharField : "debit" | "credit"
├── amount        DecimalField
├── balance_after DecimalField — solde du compte après l'écriture
└── created_at    DateTimeField
```

> **Règle fondamentale :** pour chaque transaction, la somme des débits = la somme des crédits.

#### Hold — La réservation

```
Hold
├── id               UUID (PK)
├── account          ForeignKey → Account
├── amount           DecimalField
├── reason           CharField
├── reference_id     CharField(128, nullable)
├── idempotency_key  CharField(128)
├── status           CharField : "pending" | "captured" | "released"
├── captured_amount  DecimalField (nullable)
├── expires_at       DateTimeField
├── resolved_at      DateTimeField (nullable)
└── created_at       DateTimeField
```

#### SplitRule — La règle de partage

```
SplitRule
├── id           UUID (PK)
├── platform_id  UUIDField
├── name         CharField
├── rules        JSONField — liste des bénéficiaires et pourcentages
├── is_active    BooleanField
├── created_at   DateTimeField
└── updated_at   DateTimeField
```

### 2.3 Schéma des relations

```
Account ←──────────── LedgerEntry ──────────→ LedgerTransaction
   │                                                    │
   │ (hold_amount)                                      │
   ↓                                                    │
 Hold                                          (source_reference_id)
                                                        │
                                                  Payment Service
```

---

## 3. Lancer le service localement

### Prérequis

- Docker et Docker Compose installés
- Le service Auth (port 7000) doit être lancé en premier (via `deploy_mvp.sh`)
- Fichier `keys/auth_public.pem` présent

### ⚠️ Important — Conflits de ports sur Ubuntu

Sur Ubuntu, PostgreSQL et Redis natifs tournent sur les mêmes ports que Docker. Avant de lancer le wallet :

```bash
sudo systemctl stop postgresql redis
```

### Commandes

```bash
# 1. Lancer le MVP d'abord (Auth + Users + Notification)
cd ~/Documents/projet/AGT/AGT-SERVICES
bash deploy_mvp.sh

# 2. Copier la clé publique Auth vers le wallet
cp agt-auth/keys/public.pem agt-wallet/keys/auth_public.pem

# 3. Lancer le wallet (première fois — build obligatoire)
cd agt-wallet && docker compose up -d --build && cd ..

# 4. Appliquer les migrations (première fois uniquement)
docker exec agt-wallet-service python manage.py migrate

# 5. Vérifier les logs
docker logs agt-wallet-service --tail=30
```

### Vérification

Ouvrez dans votre navigateur :

- **Swagger UI** : http://localhost:7006/api/v1/docs/
- **Health check** : http://localhost:7006/api/v1/wallet/health

Réponse attendue :

```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```

### Arrêter le service

```bash
# Arrêter sans supprimer les données
cd agt-wallet && docker compose down && cd ..

# Arrêter ET supprimer les données (reset complet)
cd agt-wallet && docker compose down -v && cd ..
```

### Rebuild après modification de code

```bash
cd agt-wallet && docker compose up -d --build && cd ..
```

---

## 4. Variables d'environnement

| Variable                       | Exemple                                                          | Description                       |
| ------------------------------ | ---------------------------------------------------------------- | --------------------------------- |
| `DATABASE_URL`                 | `postgresql://wallet_user:wallet_password@db:5432/agt-wallet-db` | Connexion PostgreSQL              |
| `REDIS_URL`                    | `redis://redis:6379/6`                                           | Connexion Redis (cache JWT)       |
| `AUTH_SERVICE_PUBLIC_KEY_PATH` | `keys/auth_public.pem`                                           | Chemin vers la clé publique RSA   |
| `S2S_AUTH_URL`                 | `http://agt-auth-service:7000/api/v1`                            | URL Auth pour token S2S           |
| `S2S_CLIENT_ID`                | `<uuid>`                                                         | ID de la plateforme S2S du wallet |
| `S2S_CLIENT_SECRET`            | `<secret>`                                                       | Secret de la plateforme S2S       |
| `SECRET_KEY`                   | `<django-secret>`                                                | Clé secrète Django                |
| `DEBUG`                        | `True`                                                           | Mode debug (False en production)  |
| `ALLOWED_HOSTS`                | `localhost,127.0.0.1,0.0.0.0`                                    | Hôtes autorisés                   |
| `CORS_ALLOWED_ORIGINS`         | `http://localhost:3000`                                          | Origines CORS autorisées          |

> Consultez `.env.example` pour la liste complète.

---

## 5. Conventions importantes

### 5.1 Token Bearer obligatoire sur tous les endpoints

Tous les endpoints (sauf `/wallet/health`) nécessitent un token JWT valide dans le header :

```
Authorization: Bearer <votre_token>
```

Le token est obtenu via `POST /auth/login` sur le service Auth (port 7000). Sa durée de vie est de **15 minutes**.

### 5.2 owner_id auto-rempli depuis le JWT

Lors de la création d'un wallet (`POST /wallet/accounts`), si `owner_id` n'est pas fourni dans le body, il est automatiquement rempli avec le `sub` du token JWT (l'ID Auth de l'utilisateur connecté).

### 5.3 Idempotence obligatoire sur toutes les opérations financières

Chaque opération de crédit, débit, transfer, split et hold requiert un `idempotency_key`. Si la même clé est soumise deux fois, la deuxième requête retourne `"Idempotent hit"` sans créer de doublon.

**Règle :** utiliser une clé unique par opération, par exemple `"credit-{payment_id}"` ou `"transfer-{uuid}"`.

### 5.4 Double-entry : chaque transaction génère deux écritures

Toute opération financière crée au minimum deux `LedgerEntry` :

- Une écriture **débit** sur un compte
- Une écriture **crédit** sur un autre compte

La somme totale des débits doit toujours égaler la somme totale des crédits dans tout le ledger.

### 5.5 Compte external — le compte miroir

Pour les cash-in et cash-out, le système crée automatiquement un compte `external` par devise s'il n'en existe pas encore. Ce compte représente l'argent qui entre/sort du système depuis l'extérieur.

- **Cash-in** : le compte external est débité, le wallet utilisateur est crédité
- **Cash-out** : le wallet utilisateur est débité, le compte external est crédité

### 5.6 Holds — réservation de fonds

Un hold bloque une partie du solde (`hold_amount`) sans le débiter. Le `available_balance = balance - hold_amount`.

Un hold peut être :

- **Capturé** (`capture`) : le montant est définitivement débité du solde
- **Libéré** (`release`) : la réservation est annulée, le solde disponible est restauré

### 5.7 Comptes gelés

Un wallet avec `status: "frozen"` ne peut ni être crédité, ni être débité, ni être la source d'un hold. Toute tentative retourne une erreur `account_frozen`.

---

## 6. Référence rapide des endpoints

### Health

| Méthode | URL              | Description     | Auth | Scénario                                        |
| ------- | ---------------- | --------------- | ---- | ----------------------------------------------- |
| GET     | `/wallet/health` | État du service | Non  | [→ 7.1](#71-vérifier-que-le-service-fonctionne) |

### Accounts

| Méthode | URL                                          | Description              | Auth | Scénario                                              |
| ------- | -------------------------------------------- | ------------------------ | ---- | ----------------------------------------------------- |
| POST    | `/wallet/accounts`                           | Créer un wallet          | Oui  | [→ 7.3](#73-créer-un-wallet)                          |
| GET     | `/wallet/accounts/{account_id}`              | Détail + solde           | Oui  | [→ 7.4](#74-consulter-le-solde-dun-wallet)            |
| GET     | `/wallet/accounts/by-owner/{owner_id}`       | Wallets d'un utilisateur | Oui  | [→ 7.5](#75-lister-les-wallets-dun-utilisateur)       |
| POST    | `/wallet/accounts/{account_id}/freeze`       | Geler un wallet          | Oui  | [→ 7.14](#714-geler-un-wallet)                        |
| POST    | `/wallet/accounts/{account_id}/unfreeze`     | Dégeler un wallet        | Oui  | [→ 7.15](#715-dégeler-un-wallet)                      |
| GET     | `/wallet/accounts/{account_id}/transactions` | Historique mouvements    | Oui  | [→ 7.13](#713-consulter-lhistorique-des-transactions) |

### Ledger

| Méthode | URL                | Description            | Auth | Scénario                                         |
| ------- | ------------------ | ---------------------- | ---- | ------------------------------------------------ |
| POST    | `/wallet/credit`   | Créditer un wallet     | Oui  | [→ 7.6](#76-créditer-un-wallet-cash-in)          |
| POST    | `/wallet/debit`    | Débiter un wallet      | Oui  | [→ 7.7](#77-débiter-un-wallet-cash-out)          |
| POST    | `/wallet/transfer` | Virement entre wallets | Oui  | [→ 7.8](#78-effectuer-un-virement-entre-wallets) |
| POST    | `/wallet/split`    | Partage commission     | Oui  | [→ 7.12](#712-effectuer-un-split-de-commission)  |

### Holds

| Méthode | URL                               | Description      | Auth | Scénario                                        |
| ------- | --------------------------------- | ---------------- | ---- | ----------------------------------------------- |
| POST    | `/wallet/holds/create`            | Créer un hold    | Oui  | [→ 7.9](#79-créer-un-hold-réservation-de-fonds) |
| GET     | `/wallet/holds`                   | Liste des holds  | Oui  | [→ 7.10](#710-lister-les-holds-dun-compte)      |
| GET     | `/wallet/holds/{hold_id}`         | Détail d'un hold | Oui  | [→ 7.11](#711-consulter-le-détail-dun-hold)     |
| POST    | `/wallet/holds/{hold_id}/capture` | Capturer un hold | Oui  | [→ 7.9](#79-créer-un-hold-réservation-de-fonds) |
| POST    | `/wallet/holds/{hold_id}/release` | Libérer un hold  | Oui  | [→ 7.9](#79-créer-un-hold-réservation-de-fonds) |

### Split Rules

| Méthode | URL                   | Description       | Auth | Scénario                                |
| ------- | --------------------- | ----------------- | ---- | --------------------------------------- |
| POST    | `/wallet/split-rules` | Créer une règle   | Oui  | [→ 7.16](#716-créer-une-règle-de-split) |
| GET     | `/wallet/split-rules` | Lister les règles | Oui  | [→ 7.16](#716-créer-une-règle-de-split) |

### Admin

| Méthode | URL                          | Description            | Auth | Scénario                                         |
| ------- | ---------------------------- | ---------------------- | ---- | ------------------------------------------------ |
| GET     | `/wallet/admin/stats`        | Stats globales         | Oui  | [→ 7.17](#717-consulter-les-stats-globales)      |
| POST    | `/wallet/admin/audit-ledger` | Audit équilibre ledger | Oui  | [→ 7.18](#718-auditer-léquilibre-du-ledger)      |
| POST    | `/wallet/admin/adjustment`   | Ajustement correctif   | Oui  | [→ 7.19](#719-effectuer-un-ajustement-correctif) |

---

## 7. Scénario complet — Utilisation pas à pas

> **Avant de commencer :** ouvrez http://localhost:7006/api/v1/docs/ dans votre navigateur. Tous les tests se font depuis cette interface Swagger sauf indication contraire.

---

### 7.1 Vérifier que le service fonctionne

**Objectif :** s'assurer que le wallet, sa base de données et son cache sont opérationnels.

**Swagger :** `GET /api/v1/wallet/health`

Pas de token requis. Cliquez simplement sur **Execute**.

**Réponse attendue (200) :**

```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```

Si vous obtenez `"database": "error"`, vérifiez que le container `agt-wallet-db` est bien démarré :

```bash
docker ps | grep agt-wallet
```

---

### 7.2 Obtenir un token JWT

**Objectif :** s'authentifier pour pouvoir appeler les autres endpoints.

**Swagger Auth :** http://localhost:7000/api/v1/docs/

**Endpoint :** `POST /api/v1/auth/login`

Body :

```json
{
  "email": "dev2@example.com",
  "password": "Test1234!"
}
```

**Réponse attendue (200) :**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900,
  "requires_2fa": false
}
```

Copiez la valeur de `access_token`.

**Autoriser Swagger Wallet :**

1. Retournez sur http://localhost:7006/api/v1/docs/
2. Cliquez sur le bouton **Authorize** (en haut à droite)
3. Dans le champ `BearerAuth`, entrez votre token
4. Cliquez **Authorize** puis **Close**

> ⚠️ Le token expire après 15 minutes. Si vous obtenez `invalid_token`, refaites cette étape.

---

### 7.3 Créer un wallet

**Objectif :** créer un wallet pour l'utilisateur connecté.

**Swagger :** `POST /api/v1/wallet/accounts`

Body :

```json
{
  "currency": "XAF"
}
```

> Note : `owner_id` est optionnel — s'il n'est pas fourni, il est automatiquement rempli depuis votre token JWT.

**Réponse attendue (201) :**

```json
{
  "id": "d73939d9-d063-49b6-b62f-06ce8005b921",
  "account_type": "user",
  "currency": "XAF",
  "balance": 0,
  "message": "Account created"
}
```

📌 **Notez l'`id` du wallet** — vous en aurez besoin pour tous les tests suivants. Dans ce guide, on l'appellera **WALLET_A**.

**Créer un deuxième wallet pour les tests de virement :**

Faites la même requête une deuxième fois :

Body :

```json
{
  "currency": "XAF"
}
```

📌 **Notez ce deuxième `id`** — on l'appellera **WALLET_B**.

---

### 7.4 Consulter le solde d'un wallet

**Objectif :** vérifier le solde et l'état d'un wallet.

**Swagger :** `GET /api/v1/wallet/accounts/{account_id}`

Remplacez `{account_id}` par l'ID de **WALLET_A**.

**Réponse attendue (200) :**

```json
{
  "id": "d73939d9-d063-49b6-b62f-06ce8005b921",
  "account_type": "user",
  "owner_id": "09b4d96c-87f0-42dc-b2c1-ffd8c26ea10a",
  "currency": "XAF",
  "balance": 0,
  "hold_amount": 0,
  "available_balance": 0,
  "status": "active",
  "label": null
}
```

> **À retenir :** `available_balance = balance - hold_amount`. C'est le montant réellement disponible pour une opération.

---

### 7.5 Lister les wallets d'un utilisateur

**Objectif :** retrouver tous les wallets associés à un `owner_id`.

**Swagger :** `GET /api/v1/wallet/accounts/by-owner/{owner_id}`

Remplacez `{owner_id}` par l'`owner_id` retourné lors du GET de WALLET_A (c'est le `sub` de votre JWT).

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "id": "e849c4f0-e03a-41fd-924c-917dac2de6ef",
      "account_type": "user",
      "currency": "XAF",
      "balance": 0,
      "available_balance": 0
    },
    {
      "id": "d73939d9-d063-49b6-b62f-06ce8005b921",
      "account_type": "user",
      "currency": "XAF",
      "balance": 0,
      "available_balance": 0
    }
  ]
}
```

---

### 7.6 Créditer un wallet (cash-in)

**Objectif :** ajouter des fonds sur WALLET_A comme si un paiement externe avait été reçu.

**Swagger :** `POST /api/v1/wallet/credit`

Body :

```json
{
  "account_id": "<ID_WALLET_A>",
  "amount": 10000,
  "currency": "XAF",
  "platform_id": "<VOTRE_PLATFORM_ID>",
  "source": "payment",
  "source_reference_id": "PAY-REF-001",
  "idempotency_key": "credit-PAY-REF-001",
  "description": "Paiement reçu via Orange Money"
}
```

> **`platform_id`** : c'est l'UUID de la plateforme dans Auth. Vous pouvez récupérer le vôtre depuis le JWT (`platform_id` dans le payload).
>
> **`idempotency_key`** : doit être unique par opération. Si vous soumettez deux fois la même clé, la deuxième retourne `"Idempotent hit"` sans créer de doublon.

**Réponse attendue (201) :**

```json
{
  "transaction_id": "8d58eb1b-d60d-4c77-923c-025a42a06212",
  "new_balance": 10000,
  "message": "Credit completed"
}
```

**Ce qui se passe sous le capot :**

1. Le service vérifie l'`idempotency_key` — si déjà utilisée, retourne `idempotent_hit`
2. Un compte `external` pour la devise XAF est créé s'il n'existe pas
3. Une `LedgerTransaction` de type `cashin` est créée
4. Deux `LedgerEntry` sont créées :
   - Débit sur le compte `external` : -10 000 XAF
   - Crédit sur WALLET_A : +10 000 XAF
5. Le balance de WALLET_A est mis à jour

**Vérification :**

Refaites un `GET /wallet/accounts/<ID_WALLET_A>` — le `balance` doit afficher `10000`.

---

### 7.7 Débiter un wallet (cash-out)

**Objectif :** retirer des fonds de WALLET_A.

**Swagger :** `POST /api/v1/wallet/debit`

Body :

```json
{
  "account_id": "<ID_WALLET_A>",
  "amount": 500,
  "currency": "XAF",
  "platform_id": "<VOTRE_PLATFORM_ID>",
  "source": "platform",
  "source_reference_id": "CASHOUT-001",
  "idempotency_key": "debit-CASHOUT-001",
  "description": "Retrait vers compte bancaire"
}
```

**Réponse attendue (201) :**

```json
{
  "transaction_id": "5d2c3c6d-8920-422c-ae5d-0896b475f924",
  "new_balance": 9500,
  "message": "Debit completed"
}
```

**Erreurs possibles :**

| Code | Message                | Cause             |
| ---- | ---------------------- | ----------------- |
| 403  | `insufficient_balance` | Solde insuffisant |
| 409  | `account_frozen`       | Wallet gelé       |

**Ce qui se passe sous le capot :**

1. Vérification de l'`idempotency_key`
2. Vérification que `balance >= amount`
3. Une `LedgerTransaction` de type `cashout` est créée
4. Deux `LedgerEntry` sont créées :
   - Débit sur WALLET_A : -500 XAF
   - Crédit sur le compte `external` : +500 XAF
5. Le balance de WALLET_A est mis à jour

---

### 7.8 Effectuer un virement entre wallets

**Objectif :** transférer des fonds de WALLET_A vers WALLET_B.

> **Prérequis :** WALLET_A doit avoir suffisamment de fonds. Si vous suivez ce guide dans l'ordre, il a 9 500 XAF.

**Swagger :** `POST /api/v1/wallet/transfer`

Body :

```json
{
  "from_account_id": "<ID_WALLET_A>",
  "to_account_id": "<ID_WALLET_B>",
  "amount": 2000,
  "currency": "XAF",
  "platform_id": "<VOTRE_PLATFORM_ID>",
  "idempotency_key": "transfer-001",
  "description": "Virement utilisateur"
}
```

**Réponse attendue (201) :**

```json
{
  "transaction_id": "c33422bb-1aee-4b54-9261-7a8b9cb3f4e2",
  "message": "Transfer completed"
}
```

**Vérifications après le virement :**

Faites `GET /wallet/accounts/<ID_WALLET_A>` → `balance` doit être `7500`
Faites `GET /wallet/accounts/<ID_WALLET_B>` → `balance` doit être `2000`

**Ce qui se passe sous le capot :**

1. Les deux comptes sont verrouillés (`select_for_update`) pour éviter les race conditions
2. Vérification que les deux comptes ne sont pas gelés
3. Vérification que `from_account.balance >= amount`
4. Une `LedgerTransaction` de type `transfer` est créée
5. Quatre `LedgerEntry` sont créées :
   - Débit sur WALLET_A : -2 000 XAF
   - Crédit sur WALLET_B : +2 000 XAF

**Erreurs possibles :**

| Code | Message                | Cause                          |
| ---- | ---------------------- | ------------------------------ |
| 400  | `insufficient_balance` | Solde insuffisant sur WALLET_A |
| 400  | `account_frozen`       | Un des deux wallets est gelé   |

---

### 7.9 Créer un hold (réservation de fonds)

**Objectif :** réserver 1 000 XAF sur WALLET_A pour sécuriser un paiement avant de le confirmer.

**Swagger :** `POST /api/v1/wallet/holds/create`

Body :

```json
{
  "account_id": "<ID_WALLET_A>",
  "amount": 1000,
  "reason": "Réservation commande #CMD-001",
  "idempotency_key": "hold-CMD-001",
  "ttl_seconds": 3600,
  "source_reference_id": "CMD-001"
}
```

> **`ttl_seconds`** : durée de vie du hold en secondes. Par défaut 3600 (1 heure).

**Réponse attendue (201) :**

```json
{
  "hold_id": "ac85cb4b-09a5-4020-96c1-d3dc38271afc",
  "amount": 1000,
  "expires_at": "2026-04-16T14:33:52.260744+00:00"
}
```

📌 **Notez le `hold_id`** pour les étapes suivantes.

**Vérification — le solde disponible a diminué :**

`GET /wallet/accounts/<ID_WALLET_A>`

```json
{
  "balance": 7500,
  "hold_amount": 1000,
  "available_balance": 6500
}
```

> Le `balance` n'a pas changé mais l'`available_balance` a diminué de 1 000 XAF.

---

**Capturer le hold :**

La commande est confirmée — on capture le hold pour débiter définitivement.

**Swagger :** `POST /api/v1/wallet/holds/{hold_id}/capture`

Remplacez `{hold_id}` par l'ID du hold créé ci-dessus. Body vide.

**Réponse attendue (200) :**

```json
{
  "hold_id": "ac85cb4b-09a5-4020-96c1-d3dc38271afc",
  "status": "captured"
}
```

**Vérification après capture :**

`GET /wallet/accounts/<ID_WALLET_A>`

```json
{
  "balance": 6500,
  "hold_amount": 0,
  "available_balance": 6500
}
```

> Le `balance` a diminué de 1 000 XAF et le `hold_amount` est revenu à 0.

---

**Libérer un hold (scénario annulation) :**

Créez d'abord un nouveau hold pour tester la libération :

**Swagger :** `POST /api/v1/wallet/holds/create`

Body :

```json
{
  "account_id": "<ID_WALLET_A>",
  "amount": 500,
  "reason": "Réservation commande #CMD-002",
  "idempotency_key": "hold-CMD-002",
  "ttl_seconds": 3600
}
```

Notez le nouveau `hold_id`, puis libérez-le :

**Swagger :** `POST /api/v1/wallet/holds/{hold_id}/release`

Body vide.

**Réponse attendue (200) :**

```json
{
  "hold_id": "8702af03-9852-48a0-80f9-406d66250188",
  "status": "released"
}
```

**Vérification après release :**

`GET /wallet/accounts/<ID_WALLET_A>` → `balance` inchangé, `hold_amount` revenu à 0.

---

### 7.10 Lister les holds d'un compte

**Objectif :** voir tous les holds (actifs, capturés et libérés) d'un wallet.

**Swagger :** `GET /api/v1/wallet/holds`

Dans le champ `account_id` (query parameter), entrez l'ID de WALLET_A.

Ou via curl :

```bash
curl -s "http://localhost:7006/api/v1/wallet/holds?account_id=<ID_WALLET_A>" \
  -H "Authorization: Bearer <VOTRE_TOKEN>"
```

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "hold_id": "6b21467d-f146-421f-9de3-ba29bbd5ff07",
      "amount": 300.0,
      "status": "pending",
      "reason": "Réservation commande #CMD-003",
      "expires_at": "2026-04-16T15:07:35.551885+00:00"
    },
    {
      "hold_id": "8702af03-9852-48a0-80f9-406d66250188",
      "amount": 500.0,
      "status": "released",
      "reason": "Réservation commande #CMD-002",
      "expires_at": "2026-04-16T14:37:36.488560+00:00"
    },
    {
      "hold_id": "ac85cb4b-09a5-4020-96c1-d3dc38271afc",
      "amount": 1000.0,
      "status": "captured",
      "reason": "Réservation commande #CMD-001",
      "expires_at": "2026-04-16T14:33:52.260744+00:00"
    }
  ]
}
```

---

### 7.11 Consulter le détail d'un hold

**Objectif :** voir toutes les informations d'un hold spécifique.

**Swagger :** `GET /api/v1/wallet/holds/{hold_id}`

Remplacez `{hold_id}` par un ID de hold.

**Réponse attendue (200) :**

```json
{
  "hold_id": "6b21467d-f146-421f-9de3-ba29bbd5ff07",
  "account_id": "d73939d9-d063-49b6-b62f-06ce8005b921",
  "amount": 300.0,
  "status": "pending",
  "reason": "Réservation commande #CMD-003",
  "expires_at": "2026-04-16T15:07:35.551885+00:00",
  "created_at": "2026-04-16T14:07:35.552366+00:00"
}
```

---

### 7.12 Effectuer un split de commission

**Objectif :** distribuer des fonds depuis WALLET_A vers plusieurs wallets en une seule transaction atomique.

> **Prérequis :** WALLET_A doit avoir suffisamment de fonds, et WALLET_B doit exister. Si vous suivez ce guide dans l'ordre, WALLET_A a environ 6 000 XAF et WALLET_B a 2 000 XAF.

**Swagger :** `POST /api/v1/wallet/split`

Body :

```json
{
  "source_account_id": "<ID_WALLET_A>",
  "amount": 3000,
  "currency": "XAF",
  "platform_id": "<VOTRE_PLATFORM_ID>",
  "targets": [
    {
      "account_id": "<ID_WALLET_B>",
      "amount": 2000
    },
    {
      "account_id": "<ID_WALLET_A>",
      "amount": 1000
    }
  ],
  "idempotency_key": "split-TXN-001",
  "source_reference_id": "TXN-001",
  "description": "Commission plateforme + part marchand"
}
```

> **Important :** la somme des `amount` dans `targets` doit être exactement égale à `amount`. Sinon vous obtenez l'erreur `split_unbalanced`.

**Réponse attendue (201) :**

```json
{
  "transaction_id": "8f1ca0b8-e74a-4559-8066-c7100e50baf8",
  "entries": [
    {
      "account_id": "<ID_WALLET_A>",
      "direction": "debit",
      "amount": 3000
    },
    {
      "account_id": "<ID_WALLET_B>",
      "direction": "credit",
      "amount": 2000
    },
    {
      "account_id": "<ID_WALLET_A>",
      "direction": "credit",
      "amount": 1000
    }
  ],
  "message": "Split completed"
}
```

**Erreurs possibles :**

| Code | Message                | Cause                                  |
| ---- | ---------------------- | -------------------------------------- |
| 400  | `split_unbalanced`     | La somme des targets ≠ amount total    |
| 400  | `insufficient_balance` | Solde insuffisant sur le compte source |
| 400  | `account_frozen`       | Un des comptes est gelé                |

---

### 7.13 Consulter l'historique des transactions

**Objectif :** voir tous les mouvements de fonds sur un wallet.

**Swagger :** `GET /api/v1/wallet/accounts/{account_id}/transactions`

Remplacez `{account_id}` par l'ID de WALLET_A.

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "transaction_id": "8d58eb1b-d60d-4c77-923c-025a42a06212",
      "type": "cashin",
      "direction": "credit",
      "amount": 10000,
      "balance_after": 10000,
      "description": "Paiement reçu via Orange Money",
      "created_at": "2026-04-16T13:11:18.589250+00:00"
    },
    {
      "transaction_id": "5d2c3c6d-8920-422c-ae5d-0896b475f924",
      "type": "cashout",
      "direction": "debit",
      "amount": 500,
      "balance_after": 9500,
      "description": "Retrait vers compte bancaire",
      "created_at": "2026-04-16T13:15:00.000000+00:00"
    },
    {
      "transaction_id": "c33422bb-1aee-4b54-9261-7a8b9cb3f4e2",
      "type": "transfer",
      "direction": "debit",
      "amount": 2000,
      "balance_after": 7500,
      "description": "Virement utilisateur",
      "created_at": "2026-04-16T13:30:26.041260+00:00"
    }
  ],
  "page": 1,
  "total": 3
}
```

> La pagination est gérée avec les paramètres `?page=1&limit=20`.

---

### 7.14 Geler un wallet

**Objectif :** bloquer toutes les opérations sur un wallet.

**Swagger :** `POST /api/v1/wallet/accounts/{account_id}/freeze`

Remplacez `{account_id}` par l'ID de WALLET_B. Body vide.

**Réponse attendue (200) :**

```json
{
  "message": "Account frozen"
}
```

**Vérification — tentative de crédit sur un compte gelé :**

**Swagger :** `POST /api/v1/wallet/credit`

Body :

```json
{
  "account_id": "<ID_WALLET_B>",
  "amount": 100,
  "currency": "XAF",
  "platform_id": "<VOTRE_PLATFORM_ID>",
  "source": "payment",
  "idempotency_key": "credit-frozen-test-001",
  "description": "Test crédit compte gelé"
}
```

**Réponse attendue (409) :**

```json
{
  "detail": "account_frozen"
}
```

---

### 7.15 Dégeler un wallet

**Objectif :** remettre un wallet gelé en état actif.

**Swagger :** `POST /api/v1/wallet/accounts/{account_id}/unfreeze`

Remplacez `{account_id}` par l'ID de WALLET_B. Body vide.

**Réponse attendue (200) :**

```json
{
  "message": "Account unfrozen"
}
```

---

### 7.16 Créer une règle de split

**Objectif :** configurer une règle de distribution automatique de commissions pour une plateforme.

**Swagger :** `POST /api/v1/wallet/split-rules`

Body :

```json
{
  "platform_id": "<VOTRE_PLATFORM_ID>",
  "name": "Commission standard 70/30",
  "rules": [
    {
      "account_id": "<ID_WALLET_A>",
      "percentage": 70,
      "label": "Part marchand"
    },
    {
      "account_id": "<ID_WALLET_B>",
      "percentage": 30,
      "label": "Commission plateforme"
    }
  ]
}
```

**Réponse attendue (201) :**

```json
{
  "id": "2a7efc9c-7521-469a-9633-c6c3a2286e0f",
  "name": "Commission standard 70/30"
}
```

**Lister les règles de split :**

**Swagger :** `GET /api/v1/wallet/split-rules`

Optionnellement, filtrez par plateforme avec `?platform_id=<VOTRE_PLATFORM_ID>`.

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "id": "2a7efc9c-7521-469a-9633-c6c3a2286e0f",
      "name": "Commission standard 70/30",
      "rules": [
        {
          "account_id": "<ID_WALLET_A>",
          "percentage": 70,
          "label": "Part marchand"
        },
        {
          "account_id": "<ID_WALLET_B>",
          "percentage": 30,
          "label": "Commission plateforme"
        }
      ]
    }
  ]
}
```

---

### 7.17 Consulter les stats globales

**Objectif :** avoir une vue d'ensemble du système wallet.

**Swagger :** `GET /api/v1/wallet/admin/stats`

Pas de body.

**Réponse attendue (200) :**

```json
{
  "total_accounts": 4,
  "total_user_balance": 8500
}
```

> `total_accounts` inclut tous les types de comptes (user, external, system).
> `total_user_balance` est la somme des balances des comptes de type `user` uniquement.

---

### 7.18 Auditer l'équilibre du ledger

**Objectif :** vérifier que le double-entry bookkeeping est respecté — la somme des débits doit toujours égaler la somme des crédits.

**Swagger :** `POST /api/v1/wallet/admin/audit-ledger`

Body vide.

**Réponse attendue (200) :**

```json
{
  "balanced": true,
  "total_debits": 12000,
  "total_credits": 12000
}
```

> Si `"balanced": false`, cela indique une incohérence dans le ledger — à investiguer immédiatement.

---

### 7.19 Effectuer un ajustement correctif

**Objectif :** corriger manuellement le solde d'un wallet (opération admin uniquement).

**Swagger :** `POST /api/v1/wallet/admin/adjustment`

Body (crédit correctif) :

```json
{
  "account_id": "<ID_WALLET_A>",
  "amount": 100,
  "direction": "credit",
  "reason": "Correction erreur de facturation #TICKET-123",
  "currency": "XAF",
  "idempotency_key": "adjustment-TICKET-123"
}
```

**Réponse attendue (201) :**

```json
{
  "transaction_id": "20ad772b-6e04-4fda-8abb-ea55b9c50f35",
  "message": "Adjustment credit completed"
}
```

Body (débit correctif) :

```json
{
  "account_id": "<ID_WALLET_A>",
  "amount": 50,
  "direction": "debit",
  "reason": "Remboursement frais indus #TICKET-124",
  "currency": "XAF",
  "idempotency_key": "adjustment-TICKET-124"
}
```

**Réponse attendue (201) :**

```json
{
  "transaction_id": "...",
  "message": "Adjustment debit completed"
}
```

---

## 8. Flux inter-services

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    Auth     │         │    Wallet    │         │   Payment   │
│  port 7000  │         │  port 7006  │         │  port 7005  │
└──────┬──────┘         └──────┬───────┘         └──────┬──────┘
       │                       │                         │
       │  JWT validation       │                         │
       │ (clé publique RSA)    │                         │
       │──────────────────────>│                         │
       │                       │                         │
       │                       │  POST /wallet/credit    │
       │                       │  (cash-in reçu)         │
       │                       │<────────────────────────│
       │                       │                         │
       │                       │  POST /wallet/holds/create
       │                       │  (réservation)          │
       │                       │<────────────────────────│
       │                       │                         │
       │                       │  POST /wallet/holds/{id}/capture
       │                       │  (paiement confirmé)    │
       │                       │<────────────────────────│
       │                       │                         │
       │                       │  POST /wallet/split     │
       │                       │  (distribution)         │
       │                       │<────────────────────────│
```

### Payment → Wallet

| Action        | Endpoint Wallet                   | Déclencheur                                       |
| ------------- | --------------------------------- | ------------------------------------------------- |
| Paiement reçu | `POST /wallet/credit`             | Transaction Orange Money / MTN / Stripe confirmée |
| Réservation   | `POST /wallet/holds/create`       | Avant confirmation d'un paiement                  |
| Confirmation  | `POST /wallet/holds/{id}/capture` | Paiement confirmé par le provider                 |
| Annulation    | `POST /wallet/holds/{id}/release` | Paiement annulé ou expiré                         |
| Distribution  | `POST /wallet/split`              | Distribution des commissions après paiement       |

### Subscription → Wallet

| Action                 | Endpoint Wallet       | Déclencheur                    |
| ---------------------- | --------------------- | ------------------------------ |
| Prélèvement abonnement | `POST /wallet/debit`  | Renouvellement automatique     |
| Remboursement          | `POST /wallet/credit` | Résiliation avec remboursement |

### Wallet → Auth

Wallet appelle Auth uniquement pour obtenir des tokens S2S via `POST /auth/s2s/token`. Le token est mis en cache Redis pour éviter des appels répétés.

```python
# Pattern S2S utilisé par le wallet
S2STokenService.get_token()  # Récupère depuis Redis ou renouvelle via Auth
```

---

## 9. Double-entry bookkeeping — Explication

### Principe

Chaque opération financière doit être équilibrée : **tout ce qui entre quelque part doit sortir d'ailleurs**. C'est le fondement de la comptabilité en partie double.

### Exemple : cash-in de 10 000 XAF

```
LedgerTransaction : cashin — 10 000 XAF
├── LedgerEntry : account=EXTERNAL  direction=DEBIT  amount=10 000
└── LedgerEntry : account=WALLET_A  direction=CREDIT amount=10 000

Vérification : DEBITS (10 000) = CREDITS (10 000) ✅
```

### Exemple : transfer de 2 000 XAF

```
LedgerTransaction : transfer — 2 000 XAF
├── LedgerEntry : account=WALLET_A  direction=DEBIT  amount=2 000
└── LedgerEntry : account=WALLET_B  direction=CREDIT amount=2 000

Vérification : DEBITS (2 000) = CREDITS (2 000) ✅
```

### Exemple : split 3 000 XAF (2 000 + 1 000)

```
LedgerTransaction : split — 3 000 XAF
├── LedgerEntry : account=WALLET_A  direction=DEBIT  amount=3 000
├── LedgerEntry : account=WALLET_B  direction=CREDIT amount=2 000
└── LedgerEntry : account=WALLET_A  direction=CREDIT amount=1 000

Vérification : DEBITS (3 000) = CREDITS (3 000) ✅
```

### Vérification globale

L'endpoint `POST /wallet/admin/audit-ledger` calcule :

```
total_debits  = SUM(amount) WHERE direction = 'debit'
total_credits = SUM(amount) WHERE direction = 'credit'
balanced      = (total_debits == total_credits)
```

Si `balanced: false`, une écriture a été corrompue ou une transaction est incomplète.

---

## 10. Bugs connus et points d'attention

### ⚠️ Conflits de ports PostgreSQL/Redis sur Ubuntu

**Problème :** PostgreSQL natif (port 5432) et Redis natif (port 6379) tournent par défaut sur Ubuntu et entrent en conflit avec les containers Docker du wallet.

**Solution :** avant chaque session de travail, arrêtez les services natifs :

```bash
sudo systemctl stop postgresql redis
```

---

### ⚠️ Clé publique Auth à copier manuellement

**Problème :** après chaque reset du service Auth (recréation de container), la clé publique RSA change. Le wallet garde l'ancienne clé et ne peut plus valider les tokens.

**Symptôme :** tous les endpoints retournent `AUTH_PUBLIC_KEY non configure.` ou `invalid_token`.

**Solution :**

```bash
cp agt-auth/keys/public.pem agt-wallet/keys/auth_public.pem
cd agt-wallet && docker compose up -d --build && cd ..
```

---

### ⚠️ Migrations à copier localement avant rebuild

**Problème :** les migrations générées dans le container ne persistent pas après un rebuild si elles ne sont pas copiées localement.

**Solution :** toujours copier les migrations après les avoir générées dans le container :

```bash
docker exec agt-wallet-service python manage.py makemigrations accounts
docker cp agt-wallet-service:/app/apps/accounts/migrations/XXXX.py \
  agt-wallet/apps/accounts/migrations/XXXX.py
cd agt-wallet && docker compose up -d --build && cd ..
docker exec agt-wallet-service python manage.py migrate
```

---

### ⚠️ token S2S — platform_id pour les tokens S2S

**Problème :** dans `common/authentication.py`, pour les tokens S2S, `platform_id` est lu depuis `p.get("platform_id")` alors qu'il devrait être lu depuis `p.get("sub")`.

**Impact :** les appels S2S depuis d'autres services peuvent avoir un `platform_id` null.

**Statut :** à corriger dans `common/authentication.py` :

```python
if token_type == "s2s":
    self.platform_id = payload.get("sub")  # ← à corriger
else:
    self.platform_id = payload.get("platform_id")
```

---

### ⚠️ Compte external à balance négative

**Comportement normal :** lors des cash-in, le compte `external` est débité sans limite de solde. Il est donc normal de voir ce compte avec une balance négative — il représente l'argent qui a été injecté depuis l'extérieur.

---

## 11. Troubleshooting

### Le service ne démarre pas — `AUTH_PUBLIC_KEY non configure.`

**Cause :** le fichier `keys/auth_public.pem` est absent ou vide.

**Solution :**

```bash
cp agt-auth/keys/public.pem agt-wallet/keys/auth_public.pem
cd agt-wallet && docker compose up -d --build && cd ..
```

---

### Erreur `invalid_token` sur tous les endpoints

**Cause :** le token JWT a expiré (durée de vie : 15 minutes).

**Solution :** retournez sur http://localhost:7000/api/v1/docs/, refaites `POST /auth/login`, copiez le nouveau `access_token`, et mettez-le à jour dans le bouton **Authorize** de Swagger Wallet.

---

### Erreur `decimal.ConversionSyntax` ou `InvalidOperation`

**Cause :** un champ `amount` est `None` (body non envoyé ou champ manquant).

**Solution :** vérifiez que le body est bien envoyé avec le bon `Content-Type: application/json` et que tous les champs obligatoires sont présents.

---

### Erreur `idempotent_hit` sur une requête

**Cause :** la même `idempotency_key` a déjà été utilisée pour une transaction précédente.

**Comportement attendu :** c'est voulu ! La réponse retourne la transaction originale sans créer de doublon. Si vous voulez refaire l'opération, changez la clé.

---

### `balanced: false` dans l'audit ledger

**Cause :** une transaction est incomplète ou une écriture est corrompue.

**Investigation :**

```bash
# Vérifier les transactions récentes
docker exec agt-wallet-db psql -U wallet_user -d agt-wallet-db \
  -c "SELECT id, transaction_type, created_at FROM ledger_transactions ORDER BY created_at DESC LIMIT 10;"

# Vérifier les écritures
docker exec agt-wallet-db psql -U wallet_user -d agt-wallet-db \
  -c "SELECT direction, SUM(amount) FROM ledger_entries GROUP BY direction;"
```

---

### Erreur `split_unbalanced`

**Cause :** la somme des `amount` dans `targets` ne correspond pas au `amount` total du split.

**Solution :** vérifiez que `sum(targets[i].amount) == amount`.

---

### Le Swagger n'affiche pas le body sur certains endpoints

**Cause :** endpoint sans serializer associé dans le `@extend_schema`.

**Solution temporaire :** utilisez curl :

```bash
curl -s -X POST http://localhost:7006/api/v1/wallet/<endpoint> \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"champ": "valeur"}'
```

---

### Les modifications de code ne sont pas prises en compte

**Cause :** Docker utilise une image buildée. Modifier un fichier local ne suffit pas.

**Solution :** toujours rebuilder après une modification :

```bash
cd agt-wallet && docker compose up -d --build && cd ..
```

---

### Commandes utiles

```bash
# Arrêter les services natifs (obligatoire après redémarrage machine)
sudo systemctl stop postgresql redis

# Lancer le MVP
bash deploy_mvp.sh

# Lancer le wallet
cd agt-wallet && docker compose up -d && cd ..

# Rebuild wallet
cd agt-wallet && docker compose up -d --build && cd ..

# Logs wallet (temps réel)
docker logs agt-wallet-service -f

# Logs wallet (dernières lignes)
docker logs agt-wallet-service --tail=50

# Shell Django
docker exec -it agt-wallet-service python manage.py shell

# Vérifier les tables
docker exec agt-wallet-db psql -U wallet_user -d agt-wallet-db -c "\dt"

# Vérifier les soldes
docker exec agt-wallet-db psql -U wallet_user -d agt-wallet-db \
  -c "SELECT account_type, currency, balance FROM accounts ORDER BY account_type;"

# Vérifier l'équilibre du ledger directement en SQL
docker exec agt-wallet-db psql -U wallet_user -d agt-wallet-db \
  -c "SELECT direction, SUM(amount) as total FROM ledger_entries GROUP BY direction;"

# Health checks
curl http://localhost:7000/api/v1/auth/health
curl http://localhost:7006/api/v1/wallet/health

# Swagger
# Auth    → http://localhost:7000/api/v1/docs/
# Wallet  → http://localhost:7006/api/v1/docs/
```

---

_AG Technologies — Confidentiel — Usage interne_
_Guide rédigé après tests complets en conditions réelles — Avril 2026_
