# AGT Auth Service - v1.0

Service d'authentification centralise de l'ecosysteme AG Technologies.

## Stack

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3.11+ |
| Framework | Django 5.x + DRF |
| Base de donnees | PostgreSQL 15+ |
| Cache | Redis 7+ |
| JWT | RS256 (PyJWT) |
| Hashing | bcrypt (cost 12+) |
| 2FA | pyotp (TOTP) |
| Doc API | drf-spectacular (Swagger/OpenAPI 3.0) |

## Prerequisites

- Docker 24+ et Docker Compose v2
- OpenSSL (optionnel sur Windows, le script gere l'absence)

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

> **Note Windows** : Si OpenSSL n'est pas installe, generez les cles manuellement :
> ```powershell
> mkdir keys
> docker run --rm -v "${PWD}\keys:/keys" alpine/openssl genrsa -out /keys/private.pem 2048
> docker run --rm -v "${PWD}\keys:/keys" alpine/openssl rsa -in /keys/private.pem -pubout -out /keys/public.pem
> ```

### Demarrage manuel (tous OS)

```bash
cp .env.example .env
mkdir -p keys
openssl genrsa -out keys/private.pem 2048
openssl rsa -in keys/private.pem -pubout -out keys/public.pem
docker compose up -d --build
docker compose exec auth python manage.py migrate --noinput
curl http://localhost:7000/api/v1/auth/health
```

## Documentation API (Swagger)

Une fois le service demarre :

| URL | Description |
|-----|-------------|
| http://localhost:7000/api/v1/docs/ | Swagger UI (interactif) |
| http://localhost:7000/api/v1/redoc/ | ReDoc (lecture) |
| http://localhost:7000/api/v1/schema/ | Schema OpenAPI 3.0 (JSON) |

## Mode developpement (hot reload)

```bash
docker compose --profile dev up auth-dev
```

## Endpoints (30+)

Base URL : `http://localhost:7000/api/v1`

| Methode | Endpoint | Auth | Description |
|---------|----------|------|-------------|
| GET | `/auth/health` | - | Etat du service |
| POST | `/auth/register` | X-Platform-Id | Inscription email ou telephone |
| POST | `/auth/verify-email` | - | Verification email via token |
| POST | `/auth/verify-otp` | - | Verification OTP telephone |
| POST | `/auth/login` | - | Connexion email + mot de passe |
| POST | `/auth/login/phone` | - | Demande OTP SMS |
| POST | `/auth/login/magic-link` | - | Envoi magic link |
| GET | `/auth/magic-link/callback` | - | Callback magic link |
| GET | `/auth/oauth/google` | - | Initier OAuth Google |
| GET | `/auth/oauth/google/callback` | - | Callback Google |
| GET | `/auth/oauth/facebook` | - | Initier OAuth Facebook |
| GET | `/auth/oauth/facebook/callback` | - | Callback Facebook |
| POST | `/auth/forgot-password` | - | Envoi lien reset |
| POST | `/auth/reset-password` | - | Reset via token |
| PUT | `/auth/change-password` | Bearer | Changement mot de passe |
| POST | `/auth/2fa/enable` | Bearer | Activer 2FA |
| POST | `/auth/2fa/confirm` | Bearer | Confirmer activation 2FA |
| POST | `/auth/2fa/verify` | - | Challenge 2FA au login |
| POST | `/auth/2fa/disable` | Bearer | Desactiver 2FA |
| POST | `/auth/refresh` | Cookie | Rotation refresh token |
| POST | `/auth/logout` | Bearer | Deconnexion |
| GET | `/auth/sessions` | Bearer | Sessions actives |
| DELETE | `/auth/sessions/{id}` | Bearer | Revoquer session |
| GET | `/auth/verify-token` | Bearer | Validation JWT (inter-services) |
| POST | `/auth/token/exchange` | Cookie | Cookie vers Bearer |
| GET | `/auth/me` | Bearer | Profil identite |
| GET | `/auth/login-history` | Bearer | Historique connexions |
| GET | `/auth/stats/{userId}` | Bearer | Statistiques |
| POST | `/auth/admin/block/{userId}` | Admin Key | Bloquer utilisateur |
| POST | `/auth/admin/unblock/{userId}` | Admin Key | Debloquer |
| POST | `/auth/account/deactivate` | Bearer | Desactiver son compte |
| POST | `/auth/admin/deactivate/{id}` | Admin Key | Desactivation S2S |
| DELETE | `/auth/admin/purge/{id}` | Admin Key | Purge RGPD |
| POST | `/auth/platforms` | Admin Key | Creer plateforme |
| GET | `/auth/platforms` | Admin Key | Lister plateformes |
| PUT | `/auth/platforms/{id}` | Admin Key | Modifier plateforme |
| DELETE | `/auth/platforms/{id}` | Admin Key | Desactiver plateforme |
| POST | `/auth/s2s/token` | - | Token inter-services |
| POST | `/auth/s2s/introspect` | Bearer | Valider token S2S |

## Tests

```bash
docker compose exec auth python -m pytest -v
```

## Cahier des charges

Voir [CDC_v1.0.md](./CDC_v1.0.md) pour le cahier des charges technique complet.

## Dependances inter-services

| Service | Direction | Usage |
|---------|-----------|-------|
| **Notification** (7002) | Auth vers Notif | Envoi emails/SMS (verification, reset, magic link, OTP) |
| **Users** (7001) | Auth vers Users | Provisioning profil, sync email/phone, sync status |

## Variables d'environnement

Voir `.env.example` pour la liste complete avec descriptions.

---

*AG Technologies - Auth Service v1.0 - Confidentiel*
