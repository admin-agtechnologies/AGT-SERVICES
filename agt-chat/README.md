# AGT Chat Service v1.2

Messagerie temps réel unifiée — AG Technologies.

**Stack :** Node.js 20 / Express / Socket.io / PostgreSQL 16 / Redis 7 / RabbitMQ  
**Port :** `7008`  
**Préfixe API :** `/api/v1/chat`

---

## Démarrage local

### Prérequis

- Docker & Docker Compose
- Le réseau Docker `agt_network` doit exister :
  ```bash
  docker network create agt_network
  ```

### Démarrage

```bash
cp .env.example .env
# Adapter les URLs de services si nécessaire
docker compose up -d --build
```

### Vérification

```bash
curl http://localhost:7008/api/v1/chat/health
# Réponse attendue : { "data": { "status": "healthy", "database": "ok", "redis": "ok", "rabbitmq": "ok" } }
```

---

## Tests

```bash
# Installer les dépendances
npm install

# Tous les tests
npm test

# Tests unitaires uniquement
npm run test:unit

# Tests d'intégration uniquement
npm run test:integration
```

---

## Variables d'environnement

| Variable | Description | Défaut |
|---|---|---|
| `PORT` | Port HTTP | `7008` |
| `DATABASE_URL` | PostgreSQL connection string | — |
| `REDIS_URL` | Redis connection string | — |
| `BROKER_URL` | RabbitMQ AMQP URL | — |
| `AUTH_SERVICE_URL` | URL du Service Auth v2.1 | — |
| `USERS_SERVICE_URL` | URL du Service Users v1.0 | — |
| `NOTIFICATION_SERVICE_URL` | URL du Service Notification v1.2 | — |
| `S2S_SECRET` | Secret partagé pour tokens S2S | — |
| `SOCKET_IO_CORS_ORIGIN` | Origines CORS WebSocket (CSV) | `http://localhost:3000` |
| `TYPING_TIMEOUT_MS` | Durée "en train d'écrire" | `3000` |
| `MESSAGE_EDIT_DELAY_MIN` | Délai d'édition en minutes | `15` |
| `TRANSFER_TIMEOUT_MIN` | Timeout transfert non clôturé | `10` |
| `USERS_CACHE_TTL_SEC` | TTL cache profils utilisateurs | `300` |
| `AUTH_CACHE_TTL_SEC` | TTL cache tokens Auth | `30` |

---

## Endpoints REST

### Health
```
GET  /api/v1/chat/health
```

### Conversations
```
POST   /api/v1/chat/conversations                       JWT
GET    /api/v1/chat/conversations                       JWT
GET    /api/v1/chat/conversations/:id                   JWT
PUT    /api/v1/chat/conversations/:id                   JWT
DELETE /api/v1/chat/conversations/:id                   JWT (owner/admin)
POST   /api/v1/chat/conversations/:id/participants      JWT
DELETE /api/v1/chat/conversations/:id/participants/:uid JWT
GET    /api/v1/chat/conversations/:id/participants      JWT
POST   /api/v1/chat/conversations/:id/leave             JWT
```

### Messages
```
POST   /api/v1/chat/conversations/:id/messages          JWT (rate limited)
GET    /api/v1/chat/conversations/:id/messages          JWT
PUT    /api/v1/chat/conversations/:id/messages/:msgId   JWT (auteur, dans délai)
DELETE /api/v1/chat/conversations/:id/messages/:msgId   JWT (auteur ou admin)
GET    /api/v1/chat/conversations/:id/messages/search   JWT
```

### Read receipts
```
POST   /api/v1/chat/conversations/:id/read              JWT
GET    /api/v1/chat/conversations/:id/read-status       JWT
```

### Réactions
```
POST   /api/v1/chat/messages/:msgId/reactions           JWT
DELETE /api/v1/chat/messages/:msgId/reactions/:emoji    JWT
GET    /api/v1/chat/messages/:msgId/reactions           JWT
```

### Transferts (bot→humain)
```
POST   /api/v1/chat/conversations/transfer              S2S uniquement
GET    /api/v1/chat/transfers/pending                   JWT (opérateurs)
POST   /api/v1/chat/transfers/:id/take                  JWT (permission chat:transfer:take)
POST   /api/v1/chat/transfers/:id/close                 JWT (opérateur assigné)
GET    /api/v1/chat/transfers/stats                     JWT admin / S2S
```

### Canaux & présence
```
GET    /api/v1/chat/platforms/:platformId/channels      JWT
POST   /api/v1/chat/channels/:id/join                   JWT
GET    /api/v1/chat/users/:uid/presence                 JWT
```

### Capabilities
```
GET    /api/v1/chat/capabilities/:platformId            JWT ou S2S
PUT    /api/v1/chat/capabilities/:platformId            JWT admin (permission chat:admin)
```

---

## WebSocket (Socket.io)

**Connexion :** `ws://localhost:7008?token=<JWT>`

### Événements client → serveur

| Événement | Payload |
|---|---|
| `join_conversation` | `{ conversation_id }` |
| `leave_conversation` | `{ conversation_id }` |
| `message:send` | `{ conversation_id, content, parent_id? }` |
| `message:edit` | `{ message_id, conversation_id, content }` |
| `message:delete` | `{ message_id, conversation_id }` |
| `reaction:add` | `{ message_id, emoji }` |
| `reaction:remove` | `{ message_id, emoji }` |
| `typing:start` | `{ conversation_id }` |
| `typing:stop` | `{ conversation_id }` |
| `read:mark` | `{ conversation_id, last_message_id }` |
| `presence:heartbeat` | `{}` |

### Événements serveur → client

| Événement | Payload |
|---|---|
| `message:new` | `{ message_id, conversation_id, sender_id, content, parent_id, created_at }` |
| `message:updated` | `{ message_id, content, edited_at }` |
| `message:deleted` | `{ message_id }` |
| `reaction:updated` | `{ message_id, reactions }` |
| `typing:update` | `{ user_id, conversation_id, is_typing }` |
| `read:updated` | `{ conversation_id, user_id, last_read_message_id }` |
| `presence:update` | `{ user_id, status, last_seen_at }` |
| `transfer:new` | `{ transfer_id, conversation_id, user_id }` |
| `transfer:taken` | `{ transfer_id, operator_id }` |
| `transfer:closed` | `{ transfer_id }` |
| `error` | `{ code, message }` |

---

## Architecture

```
src/
├── modules/          ← Logique métier par domaine
│   ├── capabilities/ ← Feature flags par plateforme (source de vérité)
│   ├── conversations/
│   ├── messages/
│   ├── reactions/
│   ├── presence/     ← Redis-only
│   └── transfers/    ← bot→humain
├── socket/           ← Socket.io handlers
├── common/
│   ├── middleware/   ← auth, s2s, rateLimit, capabilities
│   ├── errors/       ← AppError + errorHandler
│   ├── clients/      ← authClient, usersClient, notificationClient
│   ├── db/           ← pool pg + migrate runner
│   ├── cache/        ← ioredis client
│   └── broker/       ← RabbitMQ publisher + consumer
migrations/           ← SQL idempotents (IF NOT EXISTS)
tests/
├── unit/             ← Services mockés
└── integration/      ← API supertest
```

---

## Règles d'identité (CDC §1.3)

- `user_id` = **`users_auth.id`** (= `sub` du JWT) — partout dans ce service
- Notification attend `users_profiles.id` → résolution via `usersClient.resolveProfilesId()` avant tout appel Notification
- `platform_id` = UUID du registre Auth (`platforms.id`)

---

## Événements RabbitMQ émis

| Routing key | Déclencheur |
|---|---|
| `chat.message.created` | Nouveau message |
| `chat.transfer.created` | Nouveau transfert |
| `chat.transfer.taken` | Transfert pris en charge |
| `chat.transfer.closed` | Transfert clôturé |

Exchange : `chat.events` (topic, durable)
