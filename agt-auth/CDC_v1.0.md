# AGT Auth Service - Cahier des Charges v1.0

> Version de livraison : 1.0 | Statut : Implementation-ready | Classification : Confidentiel

## 1. Perimetre

Le service Auth couvre le cycle de vie de l'identite pure : inscription, connexion, gestion de sessions, securite (2FA, rate limiting), administration des plateformes clientes et tracabilite.

**Hors perimetre** : profils etendus (Users), roles/permissions (Users), envoi emails/SMS (Notification), logique metier des plateformes.

## 2. Stack

| Composant | Technologie |
|-----------|-------------|
| Framework | Python 3.11+ / Django 5.x / DRF |
| DB | PostgreSQL 15+ |
| Cache | Redis 7+ |
| JWT | RS256 (PyJWT) |
| Hashing | bcrypt (cost 12+) |
| 2FA | pyotp (TOTP) |
| Doc API | drf-spectacular (Swagger/OpenAPI 3.0) |

## 3. Modele de donnees

7 tables : `platforms`, `users_auth`, `sessions`, `refresh_tokens`, `oauth_providers`, `login_history`, `verification_tokens`.

Convention : `user_id` = `users_auth.id` = champ `sub` du JWT.

## 4. Endpoints (30+)

Base URL : `/api/v1`
Documentation interactive : `/api/v1/docs/` (Swagger) ou `/api/v1/redoc/`

### Health
- `GET /auth/health` - Etat du service

### Inscription
- `POST /auth/register` - Inscription email ou telephone
- `POST /auth/verify-email` - Verification email
- `POST /auth/verify-otp` - Verification OTP

### Connexion
- `POST /auth/login` - Email + mot de passe
- `POST /auth/login/phone` - OTP SMS
- `POST /auth/login/magic-link` - Magic link
- `GET /auth/magic-link/callback` - Callback magic link

### OAuth
- `GET /auth/oauth/google` et `/callback` - Google
- `GET /auth/oauth/facebook` et `/callback` - Facebook

### Securite
- `POST /auth/forgot-password` - Lien reset
- `POST /auth/reset-password` - Reset via token
- `PUT /auth/change-password` - Changement

### 2FA
- `POST /auth/2fa/enable` - Activer
- `POST /auth/2fa/confirm` - Confirmer
- `POST /auth/2fa/verify` - Challenge login
- `POST /auth/2fa/disable` - Desactiver

### Sessions
- `POST /auth/refresh` - Rotation (cookie HttpOnly)
- `POST /auth/logout` - Deconnexion
- `GET /auth/sessions` - Sessions actives
- `DELETE /auth/sessions/{id}` - Revoquer
- `GET /auth/verify-token` - Validation JWT (S2S)
- `POST /auth/token/exchange` - Cookie vers Bearer

### Profil
- `GET /auth/me` - Identite pure
- `GET /auth/login-history` - Historique
- `GET /auth/stats/{userId}` - Statistiques

### Administration
- `POST /auth/admin/block/{id}` - Bloquer
- `POST /auth/admin/unblock/{id}` - Debloquer
- `POST /auth/account/deactivate` - Self deactivate
- `POST /auth/admin/deactivate/{id}` - S2S deactivate
- `DELETE /auth/admin/purge/{id}` - Purge RGPD

### Plateformes
- `POST /auth/platforms` - Creer
- `GET /auth/platforms` - Lister
- `PUT /auth/platforms/{id}` - Modifier
- `DELETE /auth/platforms/{id}` - Desactiver

### S2S
- `POST /auth/s2s/token` - Token inter-services
- `POST /auth/s2s/introspect` - Valider token S2S

## 5. Securite

- JWT RS256 (access 15min, refresh 7j cookie HttpOnly)
- Refresh token rotation FIFO (max 5)
- Rate limiting Redis sliding window
- Brute force : blocage apres 5 tentatives (15 min)
- CSRF : SameSite=Lax + Origin + X-Requested-With
- bcrypt cost 12+

## 6. Contrats inter-services

### Auth vers Notification
- Envoi emails/SMS : verification, reset, magic link, OTP
- Transport : HTTP POST sync, timeout 5s, 3x retry

### Auth vers Users
- Provisioning : `POST /api/v1/users` apres inscription
- Sync status : `POST /api/v1/users/status-sync` (deactivation)
- Sync email/phone : `POST /api/v1/users/sync`

## 7. Variables d'environnement

Voir `.env.example` pour la liste complete.

## 8. Port

Service : **7000**

---

*AG Technologies - Auth Service CDC v1.0 - Confidentiel*
