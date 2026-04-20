# GUIDE — Service Chat

> **AG Technologies — Usage interne**
> Service Chat v1.2 — Port 7008
> Dernière mise à jour : Avril 2026

---

## Table des matières

1. [Rôle du service](#1-rôle-du-service)
2. [Architecture interne](#2-architecture-interne)
3. [Lancer le service localement](#3-lancer-le-service-localement)
4. [Variables d'environnement](#4-variables-denvironnement)
5. [Conventions importantes](#5-conventions-importantes)
6. [Authentification — JWT et S2S](#6-authentification--jwt-et-s2s)
7. [Capabilities — Configuration par plateforme](#7-capabilities--configuration-par-plateforme)
8. [Référence rapide des endpoints](#8-référence-rapide-des-endpoints)
9. [Scénarios complets — Utilisation pas à pas](#9-scénarios-complets--utilisation-pas-à-pas)
10. [WebSocket — Événements temps réel](#10-websocket--événements-temps-réel)
11. [Flux inter-services](#11-flux-inter-services)
12. [Bugs connus et corrections apportées](#12-bugs-connus-et-corrections-apportées)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Rôle du service

Le service Chat est le **moteur de messagerie temps réel centralisé de l'écosystème AGT**. Il est générique et multi-plateforme : une seule instance sert toutes les applications (AGT-Market, AGT-Bot, SALMA, Chatbot, etc.).

Il répond à une question fondamentale : **comment des utilisateurs communiquent-ils en temps réel, et comment un bot passe-t-il la main à un humain ?**

Concrètement, il gère :

- Les **conversations directes** (1-à-1 entre deux utilisateurs)
- Les **canaux** (groupes publics ou privés)
- Les **transferts bot→humain** (handoff Chatbot → opérateur humain)
- Les **messages** avec réponses imbriquées (threads), édition, suppression soft
- Les **réactions emoji** sur les messages
- Les **accusés de lecture** (read receipts)
- L'**indicateur de saisie** (typing indicators) via WebSocket
- La **présence en ligne** des utilisateurs (Redis TTL, pas de DB)
- La **recherche full-text** intra-conversation (index GIN PostgreSQL)
- Les **capabilities** configurables par plateforme (activer/désactiver chaque feature)

> **À retenir :** Le service Chat ne gère pas l'authentification (Service Auth v2.1), ni le stockage de fichiers (Service Média v1.4), ni la recherche transverse inter-services (Service Search v1.2). La recherche full-text reste locale au Chat (index GIN PostgreSQL — jamais indexé dans Search).

> **Architecture WebSocket :** Socket.io avec Redis Adapter permet de scaler horizontalement sur plusieurs instances. Les messages sont toujours persistés en PostgreSQL avant émission WebSocket.

---

## 2. Architecture interne

### 2.1 Stack technique

| Composant       | Technologie              | Rôle                                              |
| --------------- | ------------------------ | ------------------------------------------------- |
| Runtime         | Node.js 20               | Serveur applicatif                                |
| Framework HTTP  | Express.js               | API REST                                          |
| WebSocket       | Socket.io                | Temps réel                                        |
| Base de données | PostgreSQL 16            | Persistance                                       |
| Cache           | Redis 7                  | Présence, typing, rate limiting, cache auth/users |
| Message Broker  | RabbitMQ                 | Événements asynchrones (chat.events)              |
| WS Scaling      | Socket.io Redis Adapter  | Multi-instances                                   |
| Logging         | Pino                     | Logs structurés JSON                              |
| Doc API         | Swagger UI (OpenAPI 3.0) | Documentation interactive                         |

> **Justification Node.js :** contrairement aux autres services AGT (Python/Django), le Chat utilise Node.js/Express/Socket.io pour la gestion native des connexions WebSocket longue durée et la compatibilité Socket.io.

### 2.2 Structure des dossiers

```
agt-chat/
├── src/
│   ├── app.js                    # Application Express — routes + middlewares
│   ├── server.js                 # Démarrage serveur + migrations
│   ├── swagger.js                # Spec OpenAPI 3.0 complète (inline)
│   ├── common/
│   │   ├── cache/redis.js        # Client Redis partagé (ioredis)
│   │   ├── clients/
│   │   │   ├── authClient.js     # Vérif JWT + introspection S2S + getSelfS2SToken
│   │   │   ├── usersClient.js    # Profils + permissions (users_auth.id → users_profiles.id)
│   │   │   └── notificationClient.js # Envoi notifications hors ligne
│   │   ├── db/
│   │   │   ├── pool.js           # Pool PostgreSQL partagé
│   │   │   └── migrate.js        # Runner migrations SQL (auto au démarrage)
│   │   ├── errors/
│   │   │   ├── AppError.js       # Classe d'erreur métier
│   │   │   └── errorHandler.js   # Middleware erreurs global
│   │   ├── middleware/
│   │   │   ├── auth.middleware.js       # Validation JWT (cache Redis TTL 30s)
│   │   │   ├── s2s.middleware.js        # Validation token S2S
│   │   │   ├── capabilities.middleware.js # Chargement capabilities plateforme
│   │   │   ├── rateLimiter.middleware.js  # Rate limiting messages
│   │   │   └── requestLogger.middleware.js # Log structuré requêtes HTTP
│   │   └── utils/
│   │       ├── logger.js         # Instance Pino
│   │       └── response.js       # Helpers success/error
│   ├── modules/
│   │   ├── capabilities/         # Gestion features par plateforme
│   │   ├── conversations/        # CRUD conversations + participants
│   │   ├── messages/             # Messages, read receipts, search
│   │   ├── reactions/            # Réactions emoji
│   │   ├── transfers/            # Transferts bot→humain
│   │   └── presence/             # Présence Redis (pas de DB)
│   └── socket/
│       ├── index.js              # Initialisation Socket.io
│       ├── auth.middleware.js    # Auth WebSocket (JWT handshake)
│       ├── rooms.js              # Gestion rooms par conversation
│       └── handlers/
│           ├── messaging.handler.js  # send, edit, delete
│           ├── presence.handler.js   # online, offline, heartbeat
│           ├── typing.handler.js     # typing:start, typing:stop
│           ├── reactions.handler.js  # reaction:add, reaction:remove
│           └── read.handler.js       # message:read
├── migrations/
│   ├── 001_create_conversations.sql
│   ├── 002_create_messages.sql
│   ├── 003_create_message_reactions.sql
│   ├── 004_create_read_cursors.sql
│   ├── 005_create_transfers.sql
│   └── 006_create_platform_capabilities.sql
├── tests/
│   ├── unit/
│   │   ├── capabilities.service.test.js
│   │   ├── conversations.service.test.js
│   │   ├── messages.service.test.js
│   │   └── transfers.service.test.js
│   └── integration/
│       ├── conversations.api.test.js
│       ├── messages.api.test.js
│       └── transfers.api.test.js
├── docker/Dockerfile
├── docker-compose.yml
├── .env.example
├── package.json
└── README.md
```

### 2.3 Modèles de données

#### conversations — La conversation

```
conversations
├── id              UUID (PK)
├── type            VARCHAR(20) : "direct" | "channel" | "transfer"
├── platform_id     UUID — référence Auth (platforms.id)
├── name            VARCHAR(255) — obligatoire pour channel
├── description     TEXT
├── is_public       BOOLEAN — canaux publics rejoignables librement
├── created_by      UUID — users_auth.id du créateur
├── metadata        JSONB — données libres (ex: {source: "chatbot"})
├── deleted_at      TIMESTAMPTZ — soft delete
├── created_at      TIMESTAMPTZ
└── updated_at      TIMESTAMPTZ
```

#### conversation_participants — Les membres

```
conversation_participants
├── conversation_id UUID (PK, FK)
├── user_id         UUID (PK) — users_auth.id
├── role            VARCHAR(20) : "owner" | "admin" | "member"
├── joined_at       TIMESTAMPTZ
└── left_at         TIMESTAMPTZ — NULL = encore membre
```

#### messages — Les messages

```
messages
├── id              UUID (PK)
├── conversation_id UUID (FK)
├── sender_id       UUID — users_auth.id
├── content         TEXT — NULL si message supprimé
├── parent_id       UUID (FK self) — pour les threads/replies
├── media_ids       UUID[] — réservé pour Service Média (futur)
├── is_deleted      BOOLEAN — soft delete
├── edited_at       TIMESTAMPTZ — NULL si jamais édité
└── created_at      TIMESTAMPTZ
```

Index GIN sur `content` pour la recherche full-text en français.

#### message_reactions — Les réactions

```
message_reactions
├── message_id UUID (PK, FK)
├── user_id    UUID (PK)
├── emoji      VARCHAR(10) (PK)
└── created_at TIMESTAMPTZ
```

Clé primaire composite : un utilisateur ne peut mettre qu'une fois le même emoji sur un message.

#### read_cursors — Les accusés de lecture

```
read_cursors
├── conversation_id     UUID (PK, FK)
├── user_id             UUID (PK)
├── last_read_message_id UUID (FK → messages.id)
└── updated_at          TIMESTAMPTZ
```

#### transfers — Les transferts bot→humain

```
transfers
├── id              UUID (PK)
├── conversation_id UUID (UNIQUE, FK) — 1 transfer par conversation
├── user_id         UUID — utilisateur transféré
├── operator_id     UUID — opérateur humain assigné (NULL si pending)
├── status          VARCHAR(20) : "pending" | "taken" | "closed" | "timeout"
├── bot_history     JSONB — historique conversation bot
├── context         JSONB — variables de session
├── taken_at        TIMESTAMPTZ
├── closed_at       TIMESTAMPTZ
└── created_at      TIMESTAMPTZ
```

#### platform_capabilities — Les features par plateforme

```
platform_capabilities
├── platform_id            UUID (PK)
├── direct_enabled         BOOLEAN DEFAULT true
├── channels_enabled       BOOLEAN DEFAULT true
├── read_receipts_enabled  BOOLEAN DEFAULT true
├── typing_enabled         BOOLEAN DEFAULT true
├── presence_enabled       BOOLEAN DEFAULT true
├── reactions_enabled      BOOLEAN DEFAULT true
├── transfer_enabled       BOOLEAN DEFAULT false  ← désactivé par défaut
├── message_edit_enabled   BOOLEAN DEFAULT true
├── message_delete_enabled BOOLEAN DEFAULT true
├── message_search_enabled BOOLEAN DEFAULT true
├── attachments_enabled    BOOLEAN DEFAULT false  ← futur Service Média
├── max_message_length     INT DEFAULT 4096
├── rate_limit_per_user    INT DEFAULT 30  ← messages/minute
├── rate_limit_per_conv    INT DEFAULT 100 ← messages/minute par conv
├── max_channel_members    INT DEFAULT 500
└── updated_at             TIMESTAMPTZ
```

### 2.4 Schéma des relations

```
conversations ←──── conversation_participants
      │
      └──── messages ←──── message_reactions
      │           │
      │           └──── read_cursors
      │           │
      │           └──── messages (parent_id, self-ref)
      │
      └──── transfers

platform_capabilities (1 ligne par platform_id)
```

---

## 3. Lancer le service localement

### 3.1 Prérequis

- Docker et Docker Compose installés
- Le réseau Docker `agt_network` doit exister
- Le MVP AGT (Auth + Users + Notification + RabbitMQ) doit être lancé en premier
- Le fichier `.env` doit être configuré (voir section 4)

### 3.2 Créer le réseau Docker (si pas déjà fait)

```bash
docker network create agt_network
```

> **Important :** si le réseau n'existe pas, le service démarre mais ne peut pas communiquer avec Auth, Users ou RabbitMQ.

### 3.3 Lancer le MVP d'abord

```bash
cd ~/Documents/projet/AGT/AGT-SERVICES
bash deploy_mvp.sh
# ou sur Windows :
# .\deploy_mvp.ps1
```

Vérifier que Auth, Users, Notification et RabbitMQ sont bien démarrés :

```bash
curl http://localhost:7000/api/v1/auth/health   # Auth
curl http://localhost:7001/api/v1/health         # Users
curl http://localhost:7002/api/v1/health         # Notification
```

### 3.4 Préparer le `.env`

```bash
cd ~/Documents/projet/AGT/AGT-SERVICES/agt-chat
cp .env.example .env
# Éditer les valeurs si nécessaire
nano .env
```

> **Variables critiques à vérifier :**
>
> - `DATABASE_URL` — connexion PostgreSQL du Chat
> - `REDIS_URL` — Redis du Chat
> - `BROKER_URL` — RabbitMQ partagé (credentials `agt_rabbit` / `agt_rabbit_password`)
> - `AUTH_SERVICE_URL` — URL interne du service Auth
> - `S2S_CLIENT_ID` et `S2S_CLIENT_SECRET` — credentials S2S de la plateforme Chat dans Auth (voir section 6)

### 3.5 Créer la plateforme S2S dans Auth (première fois)

Avant de lancer le service, le Chat a besoin d'une plateforme enregistrée dans Auth pour s'authentifier lui-même lors des appels inter-services.

Ouvrir Swagger Auth (`http://localhost:7000/api/v1/docs/`) et appeler :

```
POST /api/v1/auth/platforms
```

```json
{
  "name": "AGT Chat",
  "slug": "agt-chat",
  "allowed_auth_methods": ["email"],
  "allowed_redirect_urls": []
}
```

> ⚠️ **Notez le `client_secret` immédiatement — il n'est affiché qu'une seule fois.** Vous ne pourrez plus le récupérer.

Reporter les valeurs dans `.env` :

```env
S2S_CLIENT_ID=<id_retourné>
S2S_CLIENT_SECRET=<client_secret_affiché>
```

### 3.6 Lancer le service

```bash
# Première fois — build obligatoire
docker compose up -d --build

# Vérifier les logs de démarrage
docker compose logs -f agt-chat-service
```

Logs attendus au démarrage :

```
✅ Redis connected
✅ 6/6 migrations applied
✅ RabbitMQ publisher connected (exchange: chat.events)
✅ RabbitMQ consumer connected
✅ Socket.io Redis Adapter configured
✅ AGT Chat Service started — port: 7008, env: "production"
```

> **Important :** les migrations SQL sont appliquées automatiquement au démarrage. Aucune commande manuelle n'est requise. Le runner est idempotent (utilise `IF NOT EXISTS`).

### 3.7 Vérification

```bash
# Health check (sans auth)
curl http://localhost:7008/api/v1/chat/health

# Réponse attendue :
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": "ok",
    "redis": "ok",
    "rabbitmq": "ok",
    "uptime": 12.34,
    "timestamp": "2026-04-17T00:00:00.000Z"
  }
}
```

Ouvrir Swagger UI : **http://localhost:7008/api/v1/chat/docs**

### 3.8 Arrêter le service

```bash
# Arrêter sans supprimer les données
docker compose down

# Arrêter ET supprimer les données (reset complet)
docker compose down -v

# Rebuild après modification de code
docker compose up -d --build

# Rebuild complet sans cache Docker (si le code n'est pas pris en compte)
docker compose down && docker compose build --no-cache && docker compose up -d
```

---

## 4. Variables d'environnement

### 4.1 Tableau complet

| Variable                      | Exemple                                                             | Description                                              |
| ----------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------- |
| `PORT`                        | `7008`                                                              | Port HTTP du service                                     |
| `NODE_ENV`                    | `production`                                                        | Environnement (`production` ou `development`)            |
| `DATABASE_URL`                | `postgresql://chat_user:chat_password@agt-chat-db:5432/agt-chat-db` | Connexion PostgreSQL                                     |
| `REDIS_URL`                   | `redis://agt-chat-redis:6379/0`                                     | Connexion Redis                                          |
| `BROKER_URL`                  | `amqp://agt_rabbit:agt_rabbit_password@agt-rabbitmq:5672`           | RabbitMQ (broker partagé AGT)                            |
| `AUTH_SERVICE_URL`            | `http://agt-auth-service:7000`                                      | URL interne Auth Service v2.1                            |
| `USERS_SERVICE_URL`           | `http://agt-users-service:7001`                                     | URL interne Users Service v1.0                           |
| `NOTIFICATION_SERVICE_URL`    | `http://agt-notif-service:7002`                                     | URL interne Notification Service v1.2                    |
| `S2S_SECRET`                  | `change-me-s2s-secret`                                              | Secret partagé S2S (legacy — remplacé par S2S*CLIENT*\*) |
| `S2S_CLIENT_ID`               | `<uuid>`                                                            | ID de la plateforme Chat dans Auth                       |
| `S2S_CLIENT_SECRET`           | `<secret>`                                                          | Secret de la plateforme Chat dans Auth                   |
| `SOCKET_IO_CORS_ORIGIN`       | `http://localhost:3000`                                             | Origines CORS WebSocket (CSV pour plusieurs)             |
| `TYPING_TIMEOUT_MS`           | `3000`                                                              | Durée "en train d'écrire" en millisecondes               |
| `MESSAGE_EDIT_DELAY_MIN`      | `15`                                                                | Délai maximum pour éditer un message (minutes)           |
| `TRANSFER_TIMEOUT_MIN`        | `10`                                                                | Timeout avant remise en attente d'un transfert           |
| `USERS_CACHE_TTL_SEC`         | `300`                                                               | TTL cache profils utilisateurs (Redis)                   |
| `AUTH_CACHE_TTL_SEC`          | `30`                                                                | TTL cache tokens Auth (Redis)                            |
| `RATE_LIMIT_USER_MSG_PER_MIN` | `30`                                                                | Messages max par utilisateur par minute                  |
| `RATE_LIMIT_CONV_MSG_PER_MIN` | `100`                                                               | Messages max par conversation par minute                 |
| `DB_POOL_MAX`                 | `10`                                                                | Taille max du pool de connexions PostgreSQL              |

### 4.2 `.env.example` complet

Voir le fichier `.env.example` à la racine du service — il contient toutes les variables avec leurs valeurs par défaut pour le développement local.

> **⚠️ Règle absolue :** le fichier `.env` ne doit JAMAIS être commité. Il est dans `.gitignore`. Seul `.env.example` (sans valeurs secrètes) est versionné.

---

## 5. Conventions importantes

### 5.1 Deux types d'identifiants utilisateur

C'est la convention la plus critique à comprendre dans AGT.

| Identifiant         | Nom dans le Chat    | Origine          | Usage                                                      |
| ------------------- | ------------------- | ---------------- | ---------------------------------------------------------- |
| `users_auth.id`     | `user_id` dans Chat | JWT (`sub`)      | Utilisé dans TOUTES les tables Chat                        |
| `users_profiles.id` | `profiles_id`       | Généré par Users | Utilisé pour appeler Users (`/users/{id}`) et Notification |

**Règle pratique :** Chat stocke et travaille exclusivement avec `users_auth.id`. Quand Chat appelle Users ou Notification, il résout d'abord le `users_profiles.id` via `GET /users/by-auth/{authUserId}`.

### 5.2 Migrations automatiques

Les migrations SQL sont dans le dossier `/migrations/` et sont exécutées automatiquement au démarrage du service (dans `server.js`). Le runner est idempotent : il utilise `IF NOT EXISTS` — relancer le service ne recrée jamais une table existante.

En cas d'ajout d'une nouvelle migration, il suffit de créer le fichier SQL et de redémarrer le service.

### 5.3 Présence — Redis only, pas de DB

La présence (en ligne / hors ligne) n'est **jamais persistée en base de données**. Elle est stockée exclusivement dans Redis avec un TTL de 60 secondes. Un utilisateur qui ne renouvelle pas son heartbeat (WebSocket) passe automatiquement à `offline` après 60s.

Clés Redis utilisées :

- `presence:{user_id}` → `{status, last_seen_at}` TTL 60s
- `typing:{conversation_id}:{user_id}` → `"1"` TTL TYPING_TIMEOUT_MS

### 5.4 Rate limiting

Deux compteurs Redis par envoi de message :

- Par utilisateur : `rate:user:{user_id}:{minute_bucket}` — max `RATE_LIMIT_USER_MSG_PER_MIN`
- Par conversation : `rate:conv:{conv_id}:{minute_bucket}` — max `RATE_LIMIT_CONV_MSG_PER_MIN`

Les compteurs expirent automatiquement (fenêtre glissante de 70s).

### 5.5 Capabilities — features désactivées

Si une feature est désactivée dans `platform_capabilities`, les endpoints correspondants retournent `403 FEATURE_DISABLED`. Les événements WebSocket liés à ces features ne sont également pas émis.

`transfer_enabled` est à `false` par défaut — il faut l'activer explicitement.

### 5.6 Format des réponses

**Succès :**

```json
{
  "success": true,
  "data": { ... }
}
```

**Liste paginée (cursor-based) :**

```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "cursor": "2026-04-17T00:00:00.000Z",
    "has_more": true,
    "total": null
  }
}
```

**Erreur :**

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Description lisible"
  }
}
```

**Codes d'erreur principaux :**

| Code HTTP | Code erreur           | Usage                                     |
| --------- | --------------------- | ----------------------------------------- |
| 400       | `VALIDATION_ERROR`    | Body invalide, champ manquant             |
| 401       | `UNAUTHORIZED`        | Token manquant, expiré ou invalide        |
| 403       | `FORBIDDEN`           | Permission insuffisante                   |
| 403       | `FEATURE_DISABLED`    | Feature désactivée sur la plateforme      |
| 403       | `NOT_PARTICIPANT`     | Utilisateur non membre de la conversation |
| 404       | `NOT_FOUND`           | Ressource introuvable                     |
| 409       | `CONFLICT`            | Doublon (ex: déjà membre)                 |
| 429       | `RATE_LIMIT_EXCEEDED` | Trop de messages envoyés                  |
| 500       | `INTERNAL_ERROR`      | Erreur serveur inattendue                 |

---

## 6. Authentification — JWT et S2S

### 6.1 Deux types d'authentification

Le service Chat supporte deux mécanismes d'authentification, selon qui appelle :

| Type                | Qui l'utilise                        | Header                              | Généré par             |
| ------------------- | ------------------------------------ | ----------------------------------- | ---------------------- |
| **JWT utilisateur** | Applications front-end, utilisateurs | `Authorization: Bearer <jwt>`       | `POST /auth/login`     |
| **Token S2S**       | Services internes (Chatbot, scripts) | `Authorization: Bearer <s2s_token>` | `POST /auth/s2s/token` |

Dans Swagger Chat, il y a deux champs Authorize distincts :

- **BearerAuth** → pour le token JWT utilisateur
- **S2SAuth** → pour le token S2S

### 6.2 Obtenir un token JWT utilisateur

**Prérequis :** avoir un compte enregistré et vérifié sur la plateforme Chat.

Depuis Swagger Auth (`http://localhost:7000/api/v1/docs/`) :

```
POST /api/v1/auth/login
```

```json
{
  "email": "user@example.com",
  "password": "MonMotDePasse123!",
  "platform_id": "<platform_id_de_la_plateforme_chat>"
}
```

Réponse :

```json
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 900,
  "requires_2fa": false
}
```

> **Durée : 15 minutes (900s).** Après expiration, tous les endpoints retournent `401 UNAUTHORIZED`. Il faut se reconnecter.

Coller le token dans Swagger Chat → **Authorize** → champ **BearerAuth**.

### 6.3 Obtenir un token S2S

**Prérequis :** avoir créé une plateforme dans Auth et noté le `client_id` + `client_secret`.

Depuis Swagger Auth :

```
POST /api/v1/auth/s2s/token
```

```json
{
  "client_id": "<platform_id>",
  "client_secret": "<client_secret>"
}
```

Réponse :

```json
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "service_name": "AGT Chat"
}
```

> **Durée : 1 heure (3600s).** Coller le token dans Swagger Chat → **Authorize** → champ **S2SAuth**.

> **Note :** le service Chat lui-même utilise ce mécanisme pour s'authentifier lorsqu'il appelle `/auth/s2s/introspect` et `/users/{id}/permissions/check`. Les credentials sont dans `.env` (`S2S_CLIENT_ID`, `S2S_CLIENT_SECRET`) et le token est mis en cache Redis (`chat:self_s2s_token`) avec renouvellement automatique avant expiration.

### 6.4 Enregistrer un utilisateur sur la plateforme Chat

Pour tester les endpoints JWT, les utilisateurs doivent être enregistrés sur la bonne plateforme Chat.

Depuis Swagger Auth :

```
POST /api/v1/auth/register
```

Headers requis :

```
X-Platform-Id: <platform_id_de_la_plateforme_chat>
```

Body :

```json
{
  "email": "user@example.com",
  "password": "Test1234!",
  "method": "email"
}
```

Un email de vérification est envoyé via Mailpit (`http://localhost:8025`).

> **Si l'email n'arrive pas dans Mailpit :** vérifier que le service Notification a ses credentials S2S configurés et que le template `auth_verify_email` existe pour la plateforme. Voir section 13 — Troubleshooting.

> **Contournement en développement :** forcer la vérification directement en base Auth :
>
> ```bash
> docker exec -it agt-auth-db psql -U agt_user -d agt-auth-db \
>   -c "UPDATE users_auth SET email_verified = true WHERE email = 'user@example.com';"
> ```

---

## 7. Capabilities — Configuration par plateforme

### 7.1 Principe

Chaque plateforme peut activer ou désactiver individuellement chaque feature du service Chat. Les capabilities sont stockées dans la table `platform_capabilities` (1 ligne par `platform_id`).

Si aucune ligne n'existe pour une plateforme, les valeurs par défaut s'appliquent (voir section 2.3).

### 7.2 Lire les capabilities

```
GET /api/v1/chat/capabilities/{platformId}
```

Authentification : JWT ou S2S.

Exemple de réponse :

```json
{
  "success": true,
  "data": {
    "direct_enabled": true,
    "channels_enabled": true,
    "transfer_enabled": false,
    "reactions_enabled": true,
    "attachments_enabled": false,
    ...
  }
}
```

### 7.3 Modifier les capabilities

```
PUT /api/v1/chat/capabilities/{platformId}
```

Authentification : JWT avec permission `chat:admin` sur la plateforme.

```json
{
  "transfer_enabled": true,
  "max_message_length": 2048
}
```

> **Permission requise :** l'utilisateur doit avoir la permission `chat:admin` assignée via Users Service. Voir section 9.5 pour créer et assigner cette permission.

### 7.4 Features désactivées par défaut

| Feature               | Valeur par défaut | Raison                              |
| --------------------- | ----------------- | ----------------------------------- |
| `transfer_enabled`    | `false`           | Nécessite une configuration Chatbot |
| `attachments_enabled` | `false`           | En attente Service Média v1.4       |

---

## 8. Référence rapide des endpoints

### Health

| Méthode | Endpoint              | Auth   | Description     |
| ------- | --------------------- | ------ | --------------- |
| GET     | `/api/v1/chat/health` | Aucune | État du service |

### Capabilities

| Méthode | Endpoint                                 | Auth             | Description           |
| ------- | ---------------------------------------- | ---------------- | --------------------- |
| GET     | `/api/v1/chat/capabilities/{platformId}` | JWT ou S2S       | Lire les features     |
| PUT     | `/api/v1/chat/capabilities/{platformId}` | JWT (chat:admin) | Modifier les features |

### Conversations

| Méthode | Endpoint                           | Auth              | Description               |
| ------- | ---------------------------------- | ----------------- | ------------------------- |
| POST    | `/api/v1/chat/conversations`       | JWT               | Créer une conversation    |
| GET     | `/api/v1/chat/conversations`       | JWT               | Lister mes conversations  |
| GET     | `/api/v1/chat/conversations/{id}`  | JWT               | Détail d'une conversation |
| PUT     | `/api/v1/chat/conversations/{id}`  | JWT               | Modifier une conversation |
| DELETE  | `/api/v1/chat/conversations/{id}`  | JWT (owner/admin) | Supprimer (soft delete)   |
| GET     | `/api/v1/chat/conversations/stats` | S2S               | Stats admin               |

### Participants

| Méthode | Endpoint                                             | Auth | Description             |
| ------- | ---------------------------------------------------- | ---- | ----------------------- |
| GET     | `/api/v1/chat/conversations/{id}/participants`       | JWT  | Lister les membres      |
| POST    | `/api/v1/chat/conversations/{id}/participants`       | JWT  | Ajouter un membre       |
| DELETE  | `/api/v1/chat/conversations/{id}/participants/{uid}` | JWT  | Retirer un membre       |
| POST    | `/api/v1/chat/conversations/{id}/leave`              | JWT  | Quitter la conversation |

### Messages

| Méthode | Endpoint                                           | Auth                      | Description             |
| ------- | -------------------------------------------------- | ------------------------- | ----------------------- |
| POST    | `/api/v1/chat/conversations/{id}/messages`         | JWT                       | Envoyer un message      |
| GET     | `/api/v1/chat/conversations/{id}/messages`         | JWT                       | Historique paginé       |
| PUT     | `/api/v1/chat/conversations/{id}/messages/{msgId}` | JWT (auteur, délai 15min) | Éditer un message       |
| DELETE  | `/api/v1/chat/conversations/{id}/messages/{msgId}` | JWT (auteur ou admin)     | Supprimer (soft delete) |
| GET     | `/api/v1/chat/conversations/{id}/messages/search`  | JWT                       | Recherche full-text     |

### Read Receipts

| Méthode | Endpoint                                      | Auth | Description       |
| ------- | --------------------------------------------- | ---- | ----------------- |
| POST    | `/api/v1/chat/conversations/{id}/read`        | JWT  | Marquer comme lu  |
| GET     | `/api/v1/chat/conversations/{id}/read-status` | JWT  | Statut de lecture |

### Réactions

| Méthode | Endpoint                                  | Auth | Description            |
| ------- | ----------------------------------------- | ---- | ---------------------- |
| POST    | `/api/v1/chat/messages/{msgId}/reactions` | JWT  | Ajouter une réaction   |
| DELETE  | `/api/v1/chat/messages/{msgId}/reactions` | JWT  | Supprimer une réaction |
| GET     | `/api/v1/chat/messages/{msgId}/reactions` | JWT  | Lister les réactions   |

### Canaux publics

| Méthode | Endpoint                                       | Auth | Description        |
| ------- | ---------------------------------------------- | ---- | ------------------ |
| GET     | `/api/v1/chat/platforms/{platformId}/channels` | JWT  | Canaux publics     |
| POST    | `/api/v1/chat/channels/{id}/join`              | JWT  | Rejoindre un canal |

### Présence

| Méthode | Endpoint                            | Auth | Description        |
| ------- | ----------------------------------- | ---- | ------------------ |
| GET     | `/api/v1/chat/users/{uid}/presence` | JWT  | Statut de présence |

### Transferts (S2S uniquement)

| Méthode | Endpoint                              | Auth                     | Description           |
| ------- | ------------------------------------- | ------------------------ | --------------------- |
| POST    | `/api/v1/chat/conversations/transfer` | S2S                      | Créer un transfert    |
| GET     | `/api/v1/chat/transfers/pending`      | JWT                      | Transferts en attente |
| POST    | `/api/v1/chat/transfers/{id}/take`    | JWT (chat:transfer:take) | Prendre en charge     |
| POST    | `/api/v1/chat/transfers/{id}/close`   | JWT                      | Clôturer              |
| GET     | `/api/v1/chat/transfers/stats`        | S2S                      | Stats transferts      |

---

## 9. Scénarios complets — Utilisation pas à pas

### 9.1 Scénario 1 — Première mise en service (setup complet)

Ce scénario couvre tout ce qu'il faut faire avant de commencer à utiliser le service.

**Étape 1 — Vérifier le health check**

```bash
curl http://localhost:7008/api/v1/chat/health
```

Si l'un des composants n'est pas `ok`, voir section 13 — Troubleshooting.

**Étape 2 — Créer la plateforme Chat dans Auth**

Swagger Auth → `POST /api/v1/auth/platforms` :

```json
{
  "name": "AGT Chat",
  "slug": "agt-chat",
  "allowed_auth_methods": ["email"],
  "allowed_redirect_urls": []
}
```

Notez immédiatement : `id` (= `platform_id`) et `client_secret`.

**Étape 3 — Mettre à jour le `.env`**

```env
S2S_CLIENT_ID=<id_retourné>
S2S_CLIENT_SECRET=<client_secret>
```

Redémarrer le service :

```bash
docker compose up -d
docker exec agt-chat-redis redis-cli DEL chat:self_s2s_token
```

**Étape 4 — Vérifier les capabilities par défaut**

Générer un token S2S depuis Auth, puis :

```
GET /api/v1/chat/capabilities/<platform_id>
```

**Étape 5 — Enregistrer des utilisateurs de test**

Pour chaque utilisateur, depuis Swagger Auth avec header `X-Platform-Id` :

```
POST /api/v1/auth/register
```

Vérifier les comptes (Mailpit ou directement en DB).

**Étape 6 — Obtenir un JWT et commencer les tests**

```
POST /api/v1/auth/login
```

Coller le `access_token` dans Swagger Chat → **Authorize** → **BearerAuth**.

---

### 9.2 Scénario 2 — Conversation directe

**Prérequis :** être connecté (JWT valide) avec un compte sur la plateforme.

**Étape 1 — Créer la conversation**

```
POST /api/v1/chat/conversations
```

```json
{
  "type": "direct",
  "platform_id": "<platform_id>",
  "participant_ids": ["<users_auth.id_de_l_autre_utilisateur>"]
}
```

Réponse `201` avec l'objet conversation et son `id`.

> **Obtenir l'`users_auth.id` d'un autre utilisateur :** depuis Swagger Users → `GET /api/v1/users/` → colonne `auth_user_id`.

**Étape 2 — Envoyer un message**

```
POST /api/v1/chat/conversations/{id}/messages
```

```json
{
  "content": "Bonjour !",
  "type": "text"
}
```

**Étape 3 — Répondre à un message (thread)**

```
POST /api/v1/chat/conversations/{id}/messages
```

```json
{
  "content": "Bien reçu !",
  "type": "text",
  "parent_id": "<id_du_message_parent>"
}
```

**Étape 4 — Lire l'historique**

```
GET /api/v1/chat/conversations/{id}/messages
```

Paramètres optionnels : `?limit=20&cursor=<timestamp>`

**Étape 5 — Marquer comme lu**

```
POST /api/v1/chat/conversations/{id}/read
```

```json
{
  "last_message_id": "<id_du_dernier_message_vu>"
}
```

---

### 9.3 Scénario 3 — Canal public

**Étape 1 — Créer un canal public**

```
POST /api/v1/chat/conversations
```

```json
{
  "type": "channel",
  "platform_id": "<platform_id>",
  "name": "général",
  "is_public": true,
  "participant_ids": []
}
```

**Étape 2 — Lister les canaux publics**

```
GET /api/v1/chat/platforms/<platform_id>/channels
```

**Étape 3 — Rejoindre le canal**

```
POST /api/v1/chat/channels/{id}/join
```

Aucun body requis.

**Étape 4 — Ajouter un membre manuellement**

```
POST /api/v1/chat/conversations/{id}/participants
```

```json
{
  "user_id": "<users_auth.id>"
}
```

**Étape 5 — Retirer un membre**

```
DELETE /api/v1/chat/conversations/{id}/participants/{uid}
```

---

### 9.4 Scénario 4 — Réactions et recherche

**Ajouter une réaction :**

```
POST /api/v1/chat/messages/{msgId}/reactions
```

```json
{
  "emoji": "👍"
}
```

**Lister les réactions d'un message :**

```
GET /api/v1/chat/messages/{msgId}/reactions
```

Réponse groupée par emoji :

```json
{
  "data": [
    { "emoji": "👍", "count": "3", "users": ["uuid1", "uuid2", "uuid3"] }
  ]
}
```

**Supprimer sa réaction :**

```
DELETE /api/v1/chat/messages/{msgId}/reactions
```

```json
{
  "emoji": "👍"
}
```

**Recherche dans les messages :**

```
GET /api/v1/chat/conversations/{id}/messages/search?q=bonjour
```

Réponse avec champ `rank` de pertinence (GIN index PostgreSQL, recherche full-text française).

---

### 9.5 Scénario 5 — Gestion des permissions admin

Ce scénario est nécessaire pour utiliser les endpoints `PUT /capabilities` et `POST /transfers/{id}/take`.

**Prérequis :** être connecté avec un JWT valide sur la plateforme Chat.

**Étape 1 — Créer la permission dans Users**

Depuis Swagger Users (avec un token admin) :

```
POST /api/v1/permissions
```

```json
{
  "name": "chat:admin",
  "platform_id": "<platform_id>",
  "description": "Administrateur du chat"
}
```

Notez l'`id` de la permission.

**Étape 2 — Créer le rôle**

```
POST /api/v1/roles
```

```json
{
  "name": "chat_admin",
  "platform_id": "<platform_id>",
  "description": "Administrateur du chat"
}
```

Notez l'`id` du rôle.

**Étape 3 — Assigner la permission au rôle**

```
POST /api/v1/roles/{role_id}/permissions
```

```json
{
  "permission_id": "<permission_id>"
}
```

**Étape 4 — Assigner le rôle à l'utilisateur**

Récupérer d'abord le `users_profiles.id` de l'utilisateur :

```
GET /api/v1/users/by-auth/{users_auth_id}
```

Puis assigner le rôle :

```
POST /api/v1/users/{users_profiles_id}/roles
```

```json
{
  "role_id": "<role_id>"
}
```

**Étape 5 — Vider le cache des permissions**

Les permissions sont cachées 30 secondes dans Redis. Vider le cache pour application immédiate :

```bash
docker exec agt-chat-redis redis-cli FLUSHDB
```

**Étape 6 — Se reconnecter**

Obtenir un nouveau JWT (le token précédent peut ne pas refléter les nouveaux droits).

**Étape 7 — Tester**

```
PUT /api/v1/chat/capabilities/<platform_id>
```

```json
{
  "transfer_enabled": true
}
```

---

### 9.6 Scénario 6 — Transfert bot→humain (flux complet)

Ce scénario simule le flux Chatbot → Chat → Opérateur humain.

**Prérequis :**

- `transfer_enabled: true` dans les capabilities (voir section 7.3)
- Un token S2S valide dans Swagger Chat → **S2SAuth**
- Un utilisateur avec la permission `chat:transfer:take`

**Étape 1 — Activer les transferts**

Voir scénario 9.5 pour activer `transfer_enabled: true`.

**Étape 2 — Créer le transfert (S2S — simule Chatbot)**

```
POST /api/v1/chat/conversations/transfer
```

```json
{
  "user_id": "<users_auth.id_de_l_utilisateur>",
  "platform_id": "<platform_id>",
  "bot_history": [
    { "role": "user", "content": "Je veux parler à quelqu'un" },
    { "role": "bot", "content": "Je vous mets en relation avec un conseiller" }
  ],
  "context": {
    "intent": "human_support",
    "language": "fr"
  }
}
```

Réponse `201` :

```json
{
  "data": {
    "transfer": {
      "id": "<transfer_id>",
      "status": "pending",
      ...
    },
    "conversation": {
      "id": "<conversation_id>",
      "type": "transfer",
      ...
    }
  }
}
```

**Étape 3 — Créer la permission `chat:transfer:take`**

Même procédure que section 9.5 mais avec `"name": "chat:transfer:take"`. Assigner au même rôle.

**Étape 4 — Lister les transferts en attente (JWT)**

```
GET /api/v1/chat/transfers/pending
```

**Étape 5 — Prendre en charge le transfert**

```
POST /api/v1/chat/transfers/{transfer_id}/take
```

Aucun body. `status` passe à `taken`, `operator_id` est renseigné.

**Étape 6 — Clôturer le transfert**

```
POST /api/v1/chat/transfers/{transfer_id}/close
```

`status` passe à `closed`, `closed_at` est renseigné.

**Étape 7 — Statistiques (S2S)**

```
GET /api/v1/chat/transfers/stats
```

```json
{
  "data": {
    "pending_count": "0",
    "taken_count": "0",
    "closed_count": "1",
    "total": "1",
    "avg_wait_minutes": "7.87"
  }
}
```

---

## 10. WebSocket — Événements temps réel

### 10.1 Connexion

Le client se connecte via Socket.io avec un token JWT :

```javascript
const socket = io("http://localhost:7008", {
  auth: { token: "eyJhbGci..." },
  // ou via query param :
  // query: { token: 'eyJhbGci...' }
});
```

À la connexion, le middleware auth.middleware.js :

1. Extrait le token (header, auth ou query param)
2. Valide le token via Auth Service (cache Redis TTL 30s)
3. Charge les capabilities de la plateforme
4. Inscrit l'utilisateur dans les rooms de ses conversations actives

### 10.2 Événements serveur → client

| Événement              | Payload                                                                    | Condition                  |
| ---------------------- | -------------------------------------------------------------------------- | -------------------------- |
| `message:new`          | `{message_id, conversation_id, sender_id, content, parent_id, created_at}` | Toujours                   |
| `message:updated`      | `{message_id, content, edited_at}`                                         | Toujours                   |
| `message:deleted`      | `{message_id}`                                                             | Toujours                   |
| `typing:start`         | `{user_id, conversation_id}`                                               | Si `typing_enabled`        |
| `typing:stop`          | `{user_id, conversation_id}`                                               | Si `typing_enabled`        |
| `read:update`          | `{user_id, conversation_id, last_read_message_id}`                         | Si `read_receipts_enabled` |
| `reaction:new`         | `{message_id, user_id, emoji}`                                             | Si `reactions_enabled`     |
| `reaction:removed`     | `{message_id, user_id, emoji}`                                             | Si `reactions_enabled`     |
| `participant:online`   | `{user_id, status}`                                                        | Si `presence_enabled`      |
| `participant:offline`  | `{user_id, status}`                                                        | Si `presence_enabled`      |
| `transfer:new`         | `{transfer_id, conversation_id}`                                           | Si `transfer_enabled`      |
| `conversation:updated` | `{conversation_id, ...}`                                                   | Toujours                   |

### 10.3 Événements client → serveur

| Événement         | Payload                                  |
| ----------------- | ---------------------------------------- |
| `message:send`    | `{conversation_id, content, parent_id?}` |
| `typing:start`    | `{conversation_id}`                      |
| `typing:stop`     | `{conversation_id}`                      |
| `message:read`    | `{conversation_id, message_id}`          |
| `reaction:add`    | `{message_id, emoji}`                    |
| `reaction:remove` | `{message_id, emoji}`                    |

> **Note :** WebSocket est le chemin principal pour l'envoi de messages. L'API REST est le fallback. La persistance PostgreSQL est toujours effectuée avant l'émission WebSocket.

### 10.4 Scaling multi-instances

Le Redis Adapter (Socket.io) permet de faire tourner plusieurs instances du service en parallèle. Un message envoyé sur une instance est automatiquement redistribué aux clients connectés sur les autres instances via Redis Pub/Sub.

Pour activer : `SOCKET_IO_CORS_ORIGIN` doit inclure toutes les origines front autorisées.

---

## 11. Flux inter-services

### 11.1 Chat → Auth

| Action              | Endpoint                    | Usage                                           |
| ------------------- | --------------------------- | ----------------------------------------------- |
| Validation JWT      | `GET /auth/verify-token`    | À chaque requête (cache Redis TTL 30s)          |
| Introspection S2S   | `POST /auth/s2s/introspect` | Validation token S2S entrant                    |
| Obtention token S2S | `POST /auth/s2s/token`      | Auto-authentification Chat pour appels sortants |

Le token auto-S2S est mis en cache Redis (`chat:self_s2s_token`) et renouvelé 60 secondes avant expiration.

### 11.2 Chat → Users

| Action                  | Endpoint                                                                   | Usage                                                       |
| ----------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Profil utilisateur      | `GET /users/by-auth/{authUserId}`                                          | Résoudre `users_profiles.id`, profil (cache TTL 300s)       |
| Vérification permission | `GET /users/{profilesId}/permissions/check?platform_id=...&permission=...` | Vérifier `chat:admin`, `chat:transfer:take` (cache TTL 30s) |

> **Important :** Chat appelle Users avec `users_auth.id` pour `by-auth`, mais doit résoudre le `users_profiles.id` avant d'appeler `permissions/check`. Le paramètre s'appelle `platform_id` (et non `platform`).

> **Comportement fail-closed :** en cas d'erreur Users sur la vérification de permission, Chat **refuse** l'accès (fail-closed). En cas d'erreur sur le profil, Chat retourne un profil minimal `{first_name: "Utilisateur", last_name: "inconnu"}` (fail-open).

### 11.3 Chat → Notification

| Action                  | Endpoint                   | Usage                                      |
| ----------------------- | -------------------------- | ------------------------------------------ |
| Notification hors ligne | `POST /notifications/send` | Message envoyé à un utilisateur hors ligne |

Templates Notification requis :

| Template                 | Canal | Déclenché par            |
| ------------------------ | ----- | ------------------------ |
| `chat_message_offline`   | push  | Message hors ligne       |
| `chat_transfer_new`      | push  | Nouveau transfert        |
| `chat_transfer_assigned` | push  | Transfert pris en charge |
| `chat_transfer_closed`   | push  | Transfert clôturé        |

> **Mapping identité :** Chat travaille avec `users_auth.id` mais Notification attend `users_profiles.id`. Chat résout d'abord le profil via Users avant d'appeler Notification.

### 11.4 Chatbot → Chat (S2S entrant)

Le service Chatbot appelle Chat en S2S pour créer des transferts :

```
POST /api/v1/chat/conversations/transfer
Authorization: Bearer <token_s2s_chatbot>
```

Chat valide ce token en appelant `/auth/s2s/introspect` avec son propre token S2S.

### 11.5 Événements RabbitMQ publiés

Le service Chat publie des événements sur l'exchange `chat.events` :

| Routing Key             | Déclencheur              |
| ----------------------- | ------------------------ |
| `chat.message.created`  | Nouveau message envoyé   |
| `chat.transfer.created` | Nouveau transfert créé   |
| `chat.transfer.taken`   | Transfert pris en charge |
| `chat.transfer.closed`  | Transfert clôturé        |

---

## 12. Bugs connus et corrections apportées

Cette section documente les bugs découverts lors des tests et leurs corrections. Certains sont des bugs de code (corrigés), d'autres sont des limitations connues.

### ⚠️ Bug 1 — `s2s.middleware.js` vérifiait `result.valid` au lieu de `result.active`

**Symptôme :** tous les appels S2S retournent `401 Token S2S invalide` même avec un token valide.

**Cause :** le middleware S2S vérifiait `result.valid` mais l'endpoint `/auth/s2s/introspect` retourne `active`.

**Correction apportée :**

```javascript
// Avant (incorrect)
if (!result || !result.valid) { ... }

// Après (correct)
if (!result || !result.active) { ... }
```

Fichier : `src/common/middleware/s2s.middleware.js`

---

### ⚠️ Bug 2 — `authClient.js` n'exportait pas `getSelfS2SToken`

**Symptôme :** erreur `getSelfS2SToken is not a function` lors des appels inter-services.

**Cause :** la fonction `getSelfS2SToken` était définie mais pas exportée dans `module.exports`.

**Correction apportée :**

```javascript
// Avant
module.exports = { verifyToken, introspectS2S };

// Après
module.exports = { verifyToken, introspectS2S, getSelfS2SToken };
```

Fichier : `src/common/clients/authClient.js`

---

### ⚠️ Bug 3 — `usersClient.js` utilisait `X-Service-Token` au lieu de `Authorization: Bearer`

**Symptôme :** tous les appels vers Users Service retournent `401 Unauthorized`.

**Cause :** le client Users envoyait le token dans le header `X-Service-Token` (valeur de `S2S_SECRET`) alors que Users attend `Authorization: Bearer <token_s2s>`.

**Correction apportée :**

```javascript
// Avant (incorrect)
const s2sHeaders = () => ({
  "X-Service-Token": process.env.S2S_SECRET || "",
});

// Après (correct)
const s2sHeaders = async () => {
  const token = await getSelfS2SToken();
  return { Authorization: `Bearer ${token}` };
};
```

Fichier : `src/common/clients/usersClient.js`

---

### ⚠️ Bug 4 — `usersClient.js` envoyait `users_auth.id` à `permissions/check` au lieu de `users_profiles.id`

**Symptôme :** vérification de permission retourne `400 Bad Request` depuis Users.

**Cause :** l'endpoint `/users/{id}/permissions/check` attend le `users_profiles.id` (généré par Users) mais Chat envoyait le `users_auth.id` (extrait du JWT).

**Correction apportée :**

```javascript
// Résoudre users_profiles.id depuis users_auth.id
const profile = await getUserProfile(authUserId);
const profilesId = profile?.id || authUserId;

// Puis utiliser profilesId dans l'URL
`/api/v1/users/${profilesId}/permissions/check...`;
```

Fichier : `src/common/clients/usersClient.js`

---

### ⚠️ Bug 5 — `usersClient.js` utilisait le paramètre `?platform=` au lieu de `?platform_id=`

**Symptôme :** vérification de permission retourne `400 platform_id et permission requis.` depuis Users.

**Cause :** le paramètre URL s'appelle `platform_id` dans l'API Users, mais le code envoyait `platform`.

**Correction apportée :**

```javascript
// Avant
`?platform=${platformId}&permission=${permission}`
// Après
`?platform_id=${platformId}&permission=${permission}`;
```

Fichier : `src/common/clients/usersClient.js`

---

### ⚠️ Bug 6 — `usersClient.js` vérifiait `has_permission` au lieu de `granted`

**Symptôme :** permissions toujours refusées malgré un rôle correctement assigné.

**Cause :** Users retourne `{granted: true}` mais le code vérifiait `data.has_permission`.

**Correction apportée :**

```javascript
// Avant
data.data?.has_permission === true || data.has_permission === true;

// Après
data.data?.granted === true || data.granted === true;
```

Fichier : `src/common/clients/usersClient.js`

---

### ⚠️ Limitation connue — `transfer_enabled` désactivé par défaut

**Comportement :** `transfer_enabled` est à `false` dans `platform_capabilities`. Tout appel à `POST /conversations/transfer` retourne `403 FEATURE_DISABLED`.

**Solution :** activer via `PUT /capabilities/{platformId}` avec la permission `chat:admin` (voir scénario 9.5).

---

### ⚠️ Limitation connue — Présence visible uniquement via WebSocket

**Comportement :** `GET /users/{uid}/presence` retourne `offline` si l'utilisateur n'est pas connecté via Socket.io. La présence n'est pas mise à jour par les appels REST.

**Raison :** la présence est gérée uniquement via WebSocket (heartbeat toutes les 60s) et Redis (TTL 60s). C'est un comportement voulu (CDC §5.3.2).

---

### ⚠️ Warning non bloquant — `version` obsolète dans docker-compose.yml

**Symptôme :** warning au démarrage `the attribute version is obsolete`.

**Impact :** aucun — non bloquant.

**Solution :** la ligne `version: '3.9'` a été supprimée du `docker-compose.yml`.

---

## 13. Troubleshooting

### Le service ne démarre pas — `ECONNREFUSED` vers RabbitMQ

**Cause :** RabbitMQ n'est pas démarré ou les credentials sont incorrects.

**Vérification :**

```bash
docker compose logs agt-chat-service | grep -i rabbit
```

**Solution :**

```bash
# Vérifier que RabbitMQ tourne
docker ps | grep rabbitmq

# Vérifier les credentials dans .env
grep BROKER_URL /home/atabong/Documents/projet/AGT/AGT-SERVICES/agt-chat/.env
# Attendu : amqp://agt_rabbit:agt_rabbit_password@agt-rabbitmq:5672
```

Les credentials du broker partagé AGT sont `agt_rabbit` / `agt_rabbit_password` — différents du défaut RabbitMQ `guest/guest`.

---

### Le service ne démarre pas — `Redis connection refused`

**Cause :** le container Redis du Chat n'est pas démarré.

```bash
docker compose up -d  # relance tous les containers
docker compose logs agt-chat-redis
```

---

### Erreur `401 Token invalide ou expiré` sur tous les endpoints

**Cause 1 :** le token JWT a expiré (durée de vie : 15 minutes).

**Solution :** se reconnecter via `POST /api/v1/auth/login` et mettre à jour le token dans Swagger → **Authorize** → **BearerAuth**.

**Cause 2 :** le token a été collé dans le mauvais champ (S2SAuth au lieu de BearerAuth).

**Solution :** vérifier dans Swagger que le JWT est dans **BearerAuth** et le token S2S dans **S2SAuth**.

---

### Erreur `401 Token S2S invalide` sur `/conversations/transfer`

**Cause 1 :** le token S2S a expiré (durée de vie : 1 heure).

**Solution :** régénérer un nouveau token via `POST /auth/s2s/token` et le coller dans Swagger → **S2SAuth**.

**Cause 2 :** le service Chat n'a pas ses credentials S2S configurés (`.env` incomplet).

**Vérification :**

```bash
docker exec agt-chat-service env | grep S2S_
```

Les trois variables doivent être présentes : `S2S_SECRET`, `S2S_CLIENT_ID`, `S2S_CLIENT_SECRET`.

**Cause 3 :** le cache Redis contient un ancien token S2S corrompu.

**Solution :**

```bash
docker exec agt-chat-redis redis-cli DEL chat:self_s2s_token
```

---

### Erreur `403 FEATURE_DISABLED` sur `/conversations/transfer`

**Cause :** `transfer_enabled` est à `false` dans les capabilities de la plateforme.

**Solution :** activer le transfert (voir scénario 9.5 + section 7.3).

---

### Erreur `403 Permission chat:admin requise`

**Causes possibles :**

1. L'utilisateur n'a pas le rôle avec la permission `chat:admin` assigné dans Users.
2. La permission `chat:admin` existe mais avec un `platform_id` différent.
3. Le cache Redis des permissions est périmé.

**Solution complète :**

```bash
# 1. Vider le cache permissions
docker exec agt-chat-redis redis-cli FLUSHDB

# 2. Vérifier directement via Users (remplacer les UUIDs)
curl "http://localhost:7001/api/v1/users/<users_profiles_id>/permissions/check\
?platform_id=<platform_id>&permission=chat:admin" \
  -H "Authorization: Bearer <token_s2s>"

# Réponse attendue : {"granted": true, ...}
```

Si `granted: false`, reprendre la procédure de la section 9.5 depuis le début.

---

### Erreur `500 Internal Error` sur `/conversations/transfer` (au lieu de 401)

**Cause :** les variables `S2S_CLIENT_ID` ou `S2S_CLIENT_SECRET` dans `.env` sont malformées (doublon du nom de variable dans la valeur, par exemple).

**Vérification :**

```bash
grep S2S_ /home/atabong/Documents/projet/AGT/AGT-SERVICES/agt-chat/.env
```

La valeur ne doit PAS contenir le nom de la variable. Exemple incorrect :

```
S2S_CLIENT_ID=bfd1e2cd-S2S_CLIENT_ID=bfd1e2cd-...  # ← INCORRECT
```

Exemple correct :

```
S2S_CLIENT_ID=bfd1e2cd-2e75-42b2-8def-ac9e500c9135  # ← CORRECT
```

---

### Erreur `400` depuis Users lors de la vérification de permission

**Cause :** le paramètre URL est incorrect. Users attend `?platform_id=` et non `?platform=`.

**Vérification directe :**

```bash
curl "http://localhost:7001/api/v1/users/<users_profiles_id>/permissions/check\
?platform_id=<platform_id>&permission=chat:admin" \
  -H "Authorization: Bearer <token_s2s>"
```

Si cette commande retourne `{"granted": true}` mais que le service retourne quand même `403`, vider le cache et rebuilder.

---

### Les modifications de code ne sont pas prises en compte

**Cause :** Docker utilise l'image précédente en cache. Modifier un fichier local ne suffit pas.

**Solution :**

```bash
# Rebuild standard (utilise le cache Docker si possible)
docker compose up -d --build

# Rebuild complet sans aucun cache (si le build standard ne fonctionne pas)
docker compose down && docker compose build --no-cache && docker compose up -d
```

---

### Email de vérification non reçu dans Mailpit

**Causes possibles :**

1. Le service Notification n'a pas ses credentials S2S configurés → erreur `S2S credentials manquants`.
2. Le template `auth_verify_email` n'existe pas pour la plateforme.
3. `SENDGRID_API_KEY` non configuré → Notification tente SendGrid au lieu de Mailpit.

**Vérification :**

```bash
docker logs agt-notif-worker --tail=20
```

Si `S2S credentials manquants` : ajouter `S2S_CLIENT_ID` et `S2S_CLIENT_SECRET` dans `agt-notification/.env`.

Si `SENDGRID_API_KEY non configuré` : vérifier que `EMAIL_HOST=agt-mailpit` et `EMAIL_PORT=1025` sont dans `agt-notification/.env`.

**Contournement rapide :**

```bash
docker exec -it agt-auth-db psql -U agt_user -d agt-auth-db \
  -c "UPDATE users_auth SET email_verified = true WHERE email = 'user@example.com';"
```

---

### `docker exec psql` — `role "postgres" does not exist`

Le user PostgreSQL du service Auth est `agt_user` et non `postgres`.

```bash
# Correct
docker exec -it agt-auth-db psql -U agt_user -d agt-auth-db -c "..."

# Pour Chat
docker exec -it agt-chat-db psql -U chat_user -d agt-chat-db -c "..."
```

---

### Les logs montrent des `400` vers Users mais les appels directs fonctionnent

**Cause probable :** le code dans le container n'a pas pris en compte les dernières modifications. Le cache Docker a buildé une version précédente.

```bash
docker compose down && docker compose build --no-cache && docker compose up -d
docker exec agt-chat-redis redis-cli FLUSHDB
```

---

### Commandes utiles

```bash
# Démarrer le service
cd /home/atabong/Documents/projet/AGT/AGT-SERVICES/agt-chat
docker compose up -d

# Voir les logs en temps réel
docker compose logs -f agt-chat-service

# Logs des 50 dernières lignes
docker compose logs agt-chat-service | tail -50

# Arrêter
docker compose down

# Rebuild complet (après modification de code)
docker compose up -d --build

# Rebuild sans cache
docker compose down && docker compose build --no-cache && docker compose up -d

# Health check
curl -s http://localhost:7008/api/v1/chat/health | jq

# Swagger UI
# http://localhost:7008/api/v1/chat/docs

# Vider tout le cache Redis du Chat
docker exec agt-chat-redis redis-cli FLUSHDB

# Vider uniquement le token S2S du Chat
docker exec agt-chat-redis redis-cli DEL chat:self_s2s_token

# Vérifier les variables d'environnement dans le container
docker exec agt-chat-service env | grep -E "S2S_|AUTH_|USERS_|BROKER_|DATABASE_"

# Accès base Chat (forcer vérification email)
docker exec -it agt-chat-db psql -U chat_user -d agt-chat-db -c "\dt"

# Accès base Auth (forcer vérification email)
docker exec -it agt-auth-db psql -U agt_user -d agt-auth-db \
  -c "UPDATE users_auth SET email_verified = true WHERE email = 'user@example.com';"

# Tests unitaires
npm run test:unit

# Tests d'intégration
npm run test:integration

# Tous les tests
npm test

# Health checks tous services
curl http://localhost:7000/api/v1/auth/health
curl http://localhost:7001/api/v1/health
curl http://localhost:7002/api/v1/health
curl http://localhost:7008/api/v1/chat/health
```

---

_AG Technologies — Confidentiel — Usage interne_
_Guide rédigé après tests complets en conditions réelles — Avril 2026_
_Testé et validé sur Chat Service v1.2 — Node.js 20 / Express / Socket.io_
