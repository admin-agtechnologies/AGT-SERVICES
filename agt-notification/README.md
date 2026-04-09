# AGT Notification Service - v1.0

Service de notification multi-canal de l'ecosysteme AG Technologies.
Email, SMS, push, in-app, WhatsApp avec templates dynamiques et campagnes.

## Stack

| Composant | Technologie |
|-----------|-------------|
| Framework | Django 5.x + DRF |
| Workers | Celery 5.x |
| Broker | RabbitMQ 3.13 |
| Cache | Redis 7+ |
| Templates | Jinja2 |
| Doc API | drf-spectacular (Swagger/OpenAPI 3.0) |

## Prerequisites

- Docker 24+ et Docker Compose v2
- Cle publique RSA du Service Auth

## Demarrage rapide

### Linux / macOS

```bash
bash scripts/setup.sh
```

### Windows (PowerShell)

```powershell
# 1. Ouvrir Docker Desktop et attendre qu'il soit pret (icone verte)

# 2. Autoriser l'execution des scripts (une seule fois par session)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 3. Lancer le setup
.\scripts\setup.ps1
```

> Le Service Auth doit etre demarre en premier pour generer les cles RSA.
> Le script copie automatiquement `../agt-auth/keys/public.pem`.

## Documentation API (Swagger)

| URL | Description |
|-----|-------------|
| http://localhost:7002/api/v1/docs/ | Swagger UI |
| http://localhost:7002/api/v1/redoc/ | ReDoc |
| http://localhost:15672 | RabbitMQ Management (guest/guest) |

## Services Docker

| Container | Role |
|-----------|------|
| notification | API Django (port 7002) |
| celery-worker | Worker async (envoi notifications) |
| celery-beat | Scheduler (notifications planifiees) |
| rabbitmq | Message broker |
| redis | Cache + result backend |
| db | PostgreSQL |

## Endpoints principaux

Base URL : `http://localhost:7002/api/v1`

### Envoi
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/notifications/send` | Envoi mono/multi-canal |
| POST | `/notifications/send-bulk` | Envoi masse (max 100) |

### In-App
| Methode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/users/{id}/notifications` | Lister |
| GET | `/users/{id}/notifications/unread-count` | Badge non lues |
| PUT | `/users/{id}/notifications/{nId}/read` | Marquer lue |
| PUT | `/users/{id}/notifications/read-all` | Tout lire |
| DELETE | `/users/{id}/notifications/{nId}` | Supprimer |

### Templates
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST/GET | `/templates` | CRUD |
| PUT | `/templates/{id}` | Nouvelle version |
| POST | `/templates/{id}/preview` | Preview avec variables |

### Campagnes
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST/GET | `/campaigns` | CRUD |
| GET | `/campaigns/{id}/progress` | Progression temps reel |
| POST | `/campaigns/{id}/cancel` | Annuler |

## Tests

```bash
docker compose exec notification python -m pytest -v
```

## Templates requis par Auth

Creer ces templates avant de demarrer Auth :

| Nom | Canal | Variables |
|-----|-------|-----------|
| auth_verify_email | email | verification_url, expires_in_minutes, platform_name |
| auth_otp_sms | sms | otp_code, expires_in_minutes, platform_name |
| auth_reset_password | email | reset_url, expires_in_minutes, platform_name |
| auth_magic_link | email | magic_link_url, expires_in_minutes, platform_name |

## Cahier des charges

Voir [CDC_v1.0.md](./CDC_v1.0.md)

## Dependances inter-services

| Service | Direction | Usage |
|---------|-----------|-------|
| **Auth** (7000) | Auth vers Notif | Envoi verifications, OTP, reset, magic link |
| **Users** (7001) | Notif vers Users | Resolution coordonnees (email/phone) |

---

*AG Technologies - Notification Service v1.0 - Confidentiel*
