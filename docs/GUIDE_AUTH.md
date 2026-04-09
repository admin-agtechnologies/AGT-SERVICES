# Service Auth v1.0 - Guide d'utilisation

> Ce guide explique comment configurer, demarrer et utiliser le service Auth de l'ecosysteme AGT.

## 1. Demarrage

### Prerequis
- Docker Desktop installe et **demarr** (icone verte dans la barre de taches)

### Lancement

**Windows :**
```powershell
cd agt-auth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

**Linux/macOS :**
```bash
cd agt-auth
bash scripts/setup.sh
```

Le script fait tout automatiquement :
1. Cree le `.env` depuis `.env.example`
2. Genere les cles RSA (via OpenSSL ou via Docker si OpenSSL absent)
3. Build et demarre PostgreSQL + Redis + le service Auth
4. Execute les migrations
5. Verifie le health check

### Verification

```
curl http://localhost:7000/api/v1/auth/health
```

Reponse attendue :
```json
{"status": "healthy", "database": "ok", "redis": "ok", "version": "1.0.0"}
```

### Documentation API interactive

- **Swagger UI** : http://localhost:7000/api/v1/docs/
- **ReDoc** : http://localhost:7000/api/v1/redoc/

---

## 2. Premiere configuration

### 2.1 Creer une plateforme

Chaque application qui utilise Auth (AGT-Market, AGT-Bot, SALMA...) doit etre enregistree comme "plateforme". C'est le premier truc a faire.

```bash
curl -X POST http://localhost:7000/api/v1/auth/platforms \
  -H "Content-Type: application/json" \
  -H "X-Admin-API-Key: change-me-admin-api-key-very-secret" \
  -d '{
    "name": "AGT Market",
    "slug": "agt-market",
    "allowed_auth_methods": ["email", "phone", "google", "magic_link"],
    "allowed_redirect_urls": ["http://localhost:3000/callback"]
  }'
```

**Important** : la reponse contient un `client_secret` qui n'est affiche qu'une seule fois. Notez-le.

La reponse inclut aussi l'`id` de la plateforme (UUID). C'est le `X-Platform-Id` que vous passerez dans toutes les requetes.

### 2.2 Inscrire un utilisateur

```bash
curl -X POST http://localhost:7000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -H "X-Platform-Id: <UUID-plateforme>" \
  -d '{
    "email": "gabriel@agt.com",
    "password": "MonMotDePasse123!",
    "method": "email"
  }'
```

Note : la verification email est envoyee au Service Notification. En dev (Notification pas encore lance), l'inscription fonctionne mais l'email n'est pas envoye. L'utilisateur peut quand meme se connecter.

### 2.3 Se connecter

```bash
curl -X POST http://localhost:7000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "gabriel@agt.com",
    "password": "MonMotDePasse123!",
    "platform_id": "<UUID-plateforme>"
  }'
```

Reponse :
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900,
  "requires_2fa": false
}
```

Le `refresh_token` est pose en cookie HttpOnly (pas visible dans la reponse JSON, mais present dans les headers Set-Cookie).

### 2.4 Utiliser le token

Tous les endpoints proteges des autres services acceptent ce token :

```bash
curl http://localhost:7001/api/v1/users \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..."
```

---

## 3. Concepts cles

### JWT RS256
Auth signe les tokens avec une **cle privee** RSA. Les autres services (Users, Notification...) valident les tokens avec la **cle publique** — sans appeler Auth. C'est pour ca que chaque service a besoin de `keys/auth_public.pem`.

### Refresh Token Rotation
Le refresh token est un cookie HttpOnly. A chaque appel `POST /auth/refresh`, l'ancien est revoque et un nouveau est emis. Maximum 5 refresh tokens actifs par utilisateur (FIFO).

### Plateformes
Une plateforme = une application cliente. Chaque plateforme a ses propres methodes d'auth autorisees, ses redirect URLs, et son client_secret pour les tokens S2S.

### Admin API Key
Le header `X-Admin-API-Key` protege les endpoints d'administration (block, unblock, purge, gestion plateformes). La cle est definie dans `.env` (`ADMIN_API_KEY`).

---

## 4. Endpoints essentiels

| Action | Methode | Endpoint | Auth |
|--------|---------|----------|------|
| Creer plateforme | POST | `/auth/platforms` | Admin Key |
| Inscrire | POST | `/auth/register` | X-Platform-Id |
| Connecter | POST | `/auth/login` | - |
| Refresh token | POST | `/auth/refresh` | Cookie |
| Deconnecter | POST | `/auth/logout` | Bearer |
| Mon profil | GET | `/auth/me` | Bearer |
| Verifier token (S2S) | GET | `/auth/verify-token` | Bearer |

Liste complete : voir Swagger http://localhost:7000/api/v1/docs/

---

## 5. Tests

```bash
docker compose exec auth python -m pytest -v
```

26 tests couvrant : modeles, JWT, sessions, register, login, refresh, admin.

---

## 6. Arret et nettoyage

```bash
# Arreter
docker compose down

# Arreter et supprimer les donnees (reset complet)
docker compose down -v
```

---

## 7. Variables d'environnement cles

| Variable | Defaut | Description |
|----------|--------|-------------|
| `ADMIN_API_KEY` | change-me... | Cle admin pour endpoints admin |
| `JWT_ACCESS_TTL` | 900 | Duree access token (secondes) |
| `JWT_REFRESH_TTL` | 604800 | Duree refresh token (7 jours) |
| `BRUTE_FORCE_MAX` | 5 | Tentatives avant blocage |
| `BRUTE_FORCE_LOCKOUT` | 900 | Duree blocage (15 min) |
| `MAX_REFRESH_TOKENS` | 5 | Max tokens actifs par user |

Liste complete : voir `.env.example`
