# AG TECHNOLOGIES — STANDARDS & CONVENTIONS v1.0

> Ce document est la référence pour tout développeur de l'écosystème AGT.
> Chaque service DOIT respecter ces conventions. Aucune exception sans validation architecte.

---

## 1. Convention d'identité (CRITIQUE)

### Règle unique

| Identifiant | Signifie | Origine |
|-------------|----------|---------|
| `user_id` | `users_auth.id` | Champ `sub` du JWT |
| `platform_id` | `platforms.id` | Registre Auth, champ `platform_id` du JWT |
| `auth_user_id` | `users_auth.id` | Alias utilisé dans Users pour la FK logique |
| `users_profiles.id` | ID interne Users | Jamais exposé aux autres services |

**Règle** : tout service qui stocke ou reçoit un `user_id` utilise `users_auth.id` (= `sub` JWT).
Le Service Users est le seul à manipuler `users_profiles.id` en interne. Les autres services n'ont jamais besoin de connaître cet ID.

**Résolution** : si un service a besoin du profil Users, il appelle `GET /api/v1/users/by-auth/{authUserId}`.

---

## 2. Structure de projet

### Services Django/DRF

```
service-name/
├── apps/
│   ├── <module_1>/
│   │   ├── __init__.py
│   │   ├── models.py          # Modèles Django ORM
│   │   ├── serializers.py     # Serializers DRF
│   │   ├── views.py           # Views (ou views_*.py si volumineux)
│   │   ├── urls.py            # Routes du module
│   │   ├── services.py        # Logique métier, clients inter-services
│   │   ├── permissions.py     # Permissions custom
│   │   ├── pagination.py      # Pagination standard
│   │   └── tests/
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       └── test_services.py
│   └── <module_2>/
│       └── ...
├── config/
│   ├── __init__.py
│   ├── settings.py            # Settings Django
│   ├── urls.py                # Root URL conf
│   ├── wsgi.py
│   └── celery.py              # Si Celery requis
├── workers/                   # Si Celery requis
│   ├── __init__.py
│   └── tasks.py
├── common/                    # Code partagé intra-service
│   ├── __init__.py
│   ├── middleware.py          # Rate limiting, logging, CORS
│   ├── exceptions.py         # Handlers d'erreurs
│   └── utils.py
├── keys/                      # Clés RSA (gitignored)
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
├── pytest.ini
├── README.md
└── CDC_v1.0.md
```

### Services Node.js/NestJS

```
service-name/
├── src/
│   ├── <module_1>/
│   │   ├── <module>.module.ts
│   │   ├── <module>.controller.ts
│   │   ├── <module>.service.ts
│   │   ├── entities/
│   │   │   └── <entity>.entity.ts
│   │   └── dto/
│   │       └── <dto>.dto.ts
│   ├── common/
│   │   ├── guards/
│   │   ├── middleware/
│   │   ├── filters/
│   │   └── utils/
│   ├── app.module.ts
│   └── main.ts
├── test/
│   ├── unit/
│   └── integration/
├── keys/
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── nest-cli.json
├── README.md
└── CDC_v1.0.md
```

### Services Node.js/Express (Chat)

```
service-name/
├── src/
│   ├── modules/
│   │   ├── <module>/
│   │   │   ├── <module>.routes.js
│   │   │   ├── <module>.controller.js
│   │   │   ├── <module>.service.js
│   │   │   └── <module>.model.js
│   │   └── ...
│   ├── common/
│   │   ├── middleware/
│   │   ├── guards/
│   │   └── utils/
│   ├── socket/                # Socket.io handlers
│   │   ├── index.js
│   │   ├── presence.js
│   │   └── messaging.js
│   ├── app.js
│   └── server.js
├── test/
│   ├── unit/
│   └── integration/
├── keys/
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── package.json
├── README.md
└── CDC_v1.0.md
```

---

## 3. Format des réponses API

### Succès simple

```json
{
  "message": "Operation successful"
}
```

### Succès avec donnée

```json
{
  "id": "uuid",
  "field": "value",
  "created_at": "2026-04-06T10:00:00Z"
}
```

### Succès avec liste paginée

```json
{
  "data": [...],
  "page": 1,
  "limit": 20,
  "total": 142
}
```

### Erreur

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Description lisible"
  }
}
```

### Codes d'erreur standard

| Code HTTP | Code erreur | Usage |
|-----------|-------------|-------|
| 400 | `VALIDATION_ERROR` | Données invalides |
| 401 | `UNAUTHORIZED` | Token manquant ou invalide |
| 403 | `FORBIDDEN` | Droits insuffisants |
| 404 | `NOT_FOUND` | Ressource introuvable |
| 409 | `CONFLICT` | Doublon, idempotence violée |
| 429 | `RATE_LIMITED` | Trop de requêtes |
| 500 | `INTERNAL_ERROR` | Erreur serveur |

---

## 4. Health Check

Chaque service expose `GET /api/v1/health` (ou `GET /api/v1/<service>/health` pour Auth).

Format obligatoire :

```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```

Si un composant est en erreur : `"status": "degraded"` + HTTP 503.

Champs optionnels selon le service : `"broker"`, `"elasticsearch"`, `"storage"`.

---

## 5. Authentification inter-services

### JWT utilisateur

- Signé RS256 par Auth
- Tous les services valident avec la clé publique Auth
- Payload standard :

```json
{
  "sub": "users_auth.id",
  "iss": "agt-auth",
  "aud": "agt-ecosystem",
  "iat": 1710840000,
  "exp": 1710840900,
  "jti": "unique-token-id",
  "session_id": "session-uuid",
  "platform_id": "platform-uuid",
  "email": "user@example.com",
  "email_verified": true,
  "two_fa_verified": false
}
```

### Token S2S (service-to-service)

- Obtenu via `POST /api/v1/auth/s2s/token`
- Validé via `POST /api/v1/auth/s2s/introspect`
- Utilisé pour les appels inter-services sans contexte utilisateur

### Admin API Key

- Header `X-Admin-API-Key`
- Pour les opérations d'administration (block, purge, plateformes)
- Variable d'environnement `ADMIN_API_KEY`

---

## 6. Événements RabbitMQ

### Format standard d'événement

```json
{
  "event_id": "uuid-v4",
  "event_type": "payment.confirmed",
  "timestamp": "2026-04-06T10:00:00Z",
  "source": "payment-service",
  "data": { ... },
  "idempotency_key": "uuid-unique"
}
```

### Règles

- Chaque événement DOIT contenir `event_id`, `timestamp`, `source`
- Les consommateurs DOIVENT être idempotents (déduplication sur `event_id`)
- Retry automatique avec backoff exponentiel (1s, 2s, 4s)
- Dead letter queue pour les messages en échec après 3 retries

### Événements définis

| Source | Événement | Consommateurs |
|--------|-----------|---------------|
| Subscription | `subscription.billing_requested` | Payment |
| Payment | `payment.confirmed` | Wallet, Notification |
| Payment | `payment.failed` | Subscription, Notification |
| Payment | `payment.cancelled` | Subscription, Notification |
| Wallet | `wallet.credited` | Notification |
| Wallet | `wallet.debited` | Notification |
| Geoloc | `geofence.entered` | Plateformes, Notification |
| Geoloc | `geofence.exited` | Plateformes, Notification |
| Plateformes | `index.upsert` | Search |
| Plateformes | `index.delete` | Search |

---

## 7. Ports par service

| Service | Port app | Port DB (host) | Port Redis (host) |
|---------|----------|----------------|-------------------|
| Auth | 7000 | 5432 | 6379 |
| Users | 7001 | 5433 | 6380 |
| Notification | 7002 | 5434 | 6381 |
| Média | 7003 | 5435 | 6382 |
| Subscription | 7004 | 5436 | 6383 |
| Payment | 7005 | 5437 | 6384 |
| Wallet | 7006 | 5438 | 6385 |
| Search | 7007 | 5439 | 6386 |
| Chat | 7008 | 5440 | 6387 |
| Geoloc | 7009 | 5441 | 6388 |
| Chatbot | 7010 | 5442 | 6389 |
| **Infra partagée** | | | |
| RabbitMQ | 5672 / 15672 | — | — |
| Elasticsearch | 9200 | — | — |
| API Gateway | 80 / 443 | — | — |

---

## 8. Variables d'environnement communes

Chaque `.env.example` DOIT contenir au minimum :

```env
# === Service ===
SERVICE_NAME=agt-auth
SERVICE_PORT=7000
DEBUG=False
SECRET_KEY=change-me-in-production

# === Database ===
DATABASE_URL=postgresql://user:password@db:5432/dbname

# === Redis ===
REDIS_URL=redis://redis:6379/0

# === Auth (tous sauf Auth lui-même) ===
AUTH_SERVICE_URL=http://localhost:7000
AUTH_PUBLIC_KEY_PATH=./keys/auth_public.pem

# === Inter-services (selon besoins) ===
USERS_SERVICE_URL=http://localhost:7001
NOTIFICATION_SERVICE_URL=http://localhost:7002
MEDIA_SERVICE_URL=http://localhost:7003

# === RabbitMQ (si event-driven) ===
BROKER_URL=amqp://guest:guest@rabbitmq:5672//
```

---

## 9. Docker

### Dockerfile Django (template)

```dockerfile
# ── Builder ──
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Production ──
FROM python:3.11-slim AS production
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN python manage.py collectstatic --noinput 2>/dev/null || true
EXPOSE ${SERVICE_PORT:-7000}
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7000", "--workers", "4"]
```

### Dockerfile NestJS (template)

```dockerfile
# ── Builder ──
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ── Production ──
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json .
EXPOSE ${SERVICE_PORT:-7003}
CMD ["node", "dist/main"]
```

---

## 10. Tests

### Structure obligatoire

```
tests/
├── unit/          # Logique métier, modèles, services
└── integration/   # Endpoints, DB, inter-services
```

### Exécution

```bash
# Django
pytest

# NestJS
npm test

# Express
npm test
```

### Règle de validation

> Un service sans tests n'est pas considéré comme terminé.

---

## 11. README template

Chaque service DOIT avoir un README contenant :

1. **Nom et description** (1-2 lignes)
2. **Prérequis** (Docker, clés RSA...)
3. **Installation et démarrage** (3-5 commandes max)
4. **Variables d'environnement** (tableau)
5. **Endpoints principaux** (tableau)
6. **Lancer les tests** (1 commande)
7. **Dépendances inter-services** (qui j'appelle, qui m'appelle)

---

## 12. Git & Versionnement

- Branche principale : `main`
- Convention de commit : `[service] action: description`
  - Ex : `[auth] fix: corriger bug cleanup_expired`
  - Ex : `[users] feat: ajouter endpoint by-auth`
- Un service = un dossier à la racine du monorepo
- Tags de release : `auth-v1.0.0`, `users-v1.0.0`, etc.

---

*AG Technologies — Standards v1.0 — Avril 2026*