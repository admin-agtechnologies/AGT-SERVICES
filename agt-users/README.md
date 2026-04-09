# AGT Users Service - v1.0

Service de gestion des utilisateurs de l'ecosysteme AG Technologies.
Profils, RBAC dynamique, documents KYC, metadonnees, audit trail.

## Stack

| Composant | Technologie |
|-----------|-------------|
| Langage | Python 3.11+ |
| Framework | Django 5.x + DRF |
| Base de donnees | PostgreSQL 15+ |
| Cache | Redis 7+ |
| Doc API | drf-spectacular (Swagger/OpenAPI 3.0) |

## Prerequisites

- Docker 24+ et Docker Compose v2
- Cle publique RSA du Service Auth (`public.pem`)

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

> **Prerequis** : Le Service Auth doit etre demarre en premier pour generer les cles RSA.
> Le script copie automatiquement `../agt-auth/keys/public.pem` vers `keys/auth_public.pem`.
> Si le chemin est different, copiez manuellement la cle publique.

## Documentation API (Swagger)

| URL | Description |
|-----|-------------|
| http://localhost:7001/api/v1/docs/ | Swagger UI (interactif) |
| http://localhost:7001/api/v1/redoc/ | ReDoc (lecture) |
| http://localhost:7001/api/v1/schema/ | Schema OpenAPI 3.0 (JSON) |

## Mode developpement

```bash
docker compose --profile dev up users-dev
```

## Endpoints principaux

Base URL : `http://localhost:7001/api/v1`

### Profil
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/users` | Provisioning (par Auth) |
| GET | `/users` | Listing pagine |
| GET | `/users/{id}` | Consultation profil |
| PUT | `/users/{id}` | Mise a jour (email/phone read-only) |
| DELETE | `/users/{id}` | Soft delete global |
| GET | `/users/by-auth/{authUserId}` | Lookup par auth_user_id |
| DELETE | `/users/{id}/platforms/{platformId}` | Quitter une plateforme |
| DELETE | `/users/{id}/permanent` | Hard delete RGPD |
| GET | `/users/search?q=...` | Recherche |
| GET | `/users/stats` | Statistiques |

### Sync (appeles par Auth)
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/users/status-sync` | Sync statut (inactive/active/deleted) |
| POST | `/users/sync` | Sync email/phone |

### RBAC
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST/GET | `/platforms/{pid}/roles` | CRUD roles |
| POST/GET | `/platforms/{pid}/permissions` | CRUD permissions |
| POST/DELETE | `/platforms/{pid}/roles/{rid}/permissions` | Liaison role-permission |
| POST/GET | `/users/{id}/roles` | Assignation roles |
| GET | `/users/{id}/permissions/check?platform_id=...&permission=...` | Verification permission |

### Documents
| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST/GET | `/users/{id}/documents` | Attacher/lister |
| PUT | `/users/{id}/documents/{did}/status` | Valider/rejeter |
| GET | `/users/{id}/documents/{did}/history` | Historique versions |

## Tests

```bash
docker compose exec users python -m pytest -v
```

## Cahier des charges

Voir [CDC_v1.0.md](./CDC_v1.0.md) pour le cahier des charges technique complet.

## Dependances inter-services

| Service | Direction | Usage |
|---------|-----------|-------|
| **Auth** (7000) | Users vers Auth | Deactivation S2S, purge RGPD |
| **Auth** (7000) | Auth vers Users | Provisioning, sync status, sync credentials |
| **Notification** (7002) | Users vers Notif | Alertes roles, validation documents |
| **Media** (7003) | Users vers Media | Stockage photos et documents KYC |

## Variables d'environnement

Voir `.env.example` pour la liste complete.

---

*AG Technologies - Users Service v1.0 - Confidentiel*
