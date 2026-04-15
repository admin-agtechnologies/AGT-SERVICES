# GUIDE AUTH SERVICE — AG Technologies
## Auth Service v1.0

> **À qui s'adresse ce guide ?**
> À tout développeur qui souhaite tester et valider le service Auth d'AGT.
> Ce guide est **autonome** — vous partez de zéro sur votre machine.
>
> **Ce guide couvre les groupes testés et validés le 15 avril 2026 :**
> Health → Platforms → S2S → Templates Notification → Register → Login
>
> **Ce qui reste à tester et documenter (suite) :**
> Sessions, Profile, Password, 2FA, Admin, OAuth

---

## Table des matières

1. [Rôle du service Auth dans l'écosystème](#1-rôle-du-service-auth-dans-lécosystème)
2. [Prérequis](#2-prérequis)
3. [Lancer le MVP](#3-lancer-le-mvp)
4. [Groupe 1 — Health](#4-groupe-1--health)
5. [Groupe 2 — Platforms](#5-groupe-2--platforms)
6. [Groupe 3 — S2S](#6-groupe-3--s2s)
7. [Prérequis Register — Créer les templates Notification](#7-prérequis-register--créer-les-templates-notification)
8. [Groupe 4 — Register](#8-groupe-4--register)
9. [Groupe 5 — Login](#9-groupe-5--login)
10. [Troubleshooting](#10-troubleshooting)
11. [Commandes utiles](#11-commandes-utiles)

---

## 1. Rôle du service Auth dans l'écosystème

Auth est le **service central de confiance** de l'écosystème AGT. Il est le **seul émetteur de tokens JWT**. Tous les autres services lui font confiance pour :

- Authentifier les utilisateurs (tokens JWT RS256)
- Authentifier les microservices entre eux (tokens S2S)
- Gérer le cycle de vie des comptes (register, verify, login, logout, 2FA, OAuth, password reset)

Auth communique avec deux services lors de l'inscription :
- **Users** → provisioning du profil utilisateur (appel synchrone S2S)
- **Notification** → envoi de l'email/SMS de vérification (asynchrone via RabbitMQ + Celery)

**Port :** 7000
**Swagger UI :** http://localhost:7000/api/v1/docs/

---

## 2. Prérequis

- Docker Desktop actif (version 24+)
- Le dépôt AGT cloné en local
- PowerShell (Windows) ou Bash (Linux/Mac)

---

## 3. Lancer le MVP

Depuis la racine du projet :

```powershell
# Windows
.\deploy_mvp.ps1

# Linux / Mac
./deploy_mvp.sh
```

Attendez le message de confirmation :

```
=========================================
 DÉPLOIEMENT MVP RÉUSSI !
=========================================
 Auth         : http://localhost:7000/api/v1/docs/
 Users        : http://localhost:7001/api/v1/docs/
 Notification : http://localhost:7002/api/v1/docs/
 Mailpit      : http://localhost:8025
 RabbitMQ     : http://localhost:15672
=========================================
```

Vérifiez l'état des containers :

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Vous devez voir au minimum ces containers avec le statut `(healthy)` :

```
agt-auth-service     Up ... (healthy)   0.0.0.0:7000->7000/tcp
agt-users-service    Up ... (healthy)   0.0.0.0:7001->7001/tcp
agt-notif-service    Up ... (healthy)   0.0.0.0:7002->7002/tcp
agt-notif-worker     Up ...
agt-rabbitmq         Up ... (healthy)
agt-mailpit          Up ... (healthy)   0.0.0.0:8025->8025/tcp
```

### Appliquer les migrations (obligatoire après un démarrage à froid)

> ⚠️ **À faire impérativement** après chaque `deploy_mvp.ps1` sur une base vide (premier lancement ou après `--clean`).
> Sans cette étape, les tables n'existent pas et toutes les requêtes API renverront une erreur 500.

```powershell
# Auth — créer et appliquer les migrations
docker exec agt-auth-service python manage.py makemigrations authentication
docker exec agt-auth-service python manage.py migrate --noinput

# Users — créer et appliquer les migrations
docker exec agt-users-service python manage.py makemigrations users roles documents
docker exec agt-users-service python manage.py migrate --noinput

# Notification — créer et appliquer les migrations
docker exec agt-notif-service python manage.py makemigrations notifications templates_mgr campaigns devices
docker exec agt-notif-service python manage.py migrate --noinput
```

Résultat attendu pour chaque service :

  ```bash
  Operations to perform:
  Apply all migrations: authentication, contenttypes, platforms, sessions, ...
  Running migrations:
  Applying authentication.0001_initial... OK
  Applying platforms.0001_initial... OK
  ```
Si vous voyez `No migrations to apply` sur tous les services, c'est que les migrations sont déjà à jour — vous pouvez continuer.

---

## 4. Groupe 1 — Health

### Rôle
Vérifier en temps réel que les 3 composants critiques sont opérationnels : l'application Django, la base PostgreSQL et le cache Redis. Utilisé par les scripts de déploiement avant de continuer.

### Test — `GET /api/v1/auth/health`

Dans Swagger : `GET /api/v1/auth/health` → `Try it out` → `Execute`

Ou en ligne de commande :
```powershell
curl http://localhost:7000/api/v1/auth/health
```

**Réponse attendue (200 OK) :**
```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```

Si vous obtenez `"status": "degraded"` → vérifiez les logs :
```powershell
docker logs agt-auth-service --tail=30
```

---

## 5. Groupe 2 — Platforms

### Rôle
Une plateforme représente un client autorisé à appeler Auth — application mobile, frontend web, ou autre microservice. Chaque plateforme reçoit un `client_id` (UUID) et un `client_secret` qui lui permettent d'obtenir des tokens S2S et d'identifier les utilisateurs qui s'inscrivent via elle.

**Sans plateforme valide → aucun register, aucun login, aucun token S2S.**

Il y a deux types de plateformes :
- **Plateformes S2S** — pour les microservices (ex : AGT Notification → appelle Users)
- **Plateformes applicatives** — pour les apps clientes (ex : app mobile, backoffice de test)

### Authentification des endpoints Platforms

Ces endpoints utilisent une **API Key admin** — pas de JWT. Dans Swagger, cliquez sur **Authorize** (en haut à droite) et saisissez :

```
X-Admin-API-Key: change-me-admin-api-key-very-secret
```

> La valeur réelle se trouve dans `agt-auth/.env` à la variable `ADMIN_API_KEY`.
> Ne jamais exposer cette clé côté client.

---

### Étape 1 — Créer la plateforme S2S de Notification

Notification doit pouvoir appeler Users pour résoudre les infos utilisateur avant d'envoyer un email. Il lui faut donc une plateforme S2S dans Auth.

**`POST /api/v1/auth/platforms`**

Body :
```json
{
  "name": "AGT Notification",
  "slug": "agt-notification",
  "allowed_auth_methods": ["email"]
}
```

**Réponse (201 Created) :**
```json
{
  "id": "<uuid_généré>",
  "name": "AGT Notification",
  "slug": "agt-notification",
  "is_active": true,
  "client_secret": "<secret_affiché_une_seule_fois>"
}
```

> ⚠️ **Le `client_secret` n'est affiché qu'une seule fois.** Notez-le immédiatement.
> En cas de perte → désactiver la plateforme et en recréer une nouvelle.

Mettez à jour `agt-notification/.env` avec les valeurs obtenues à ajouter en fin de fichier :

```env
# ─── S2S ─────────────────────────────────────────────────────────────────────
S2S_AUTH_URL=http://agt-auth-service:7000/api/v1
S2S_CLIENT_ID=<id_retourné>
S2S_CLIENT_SECRET=<client_secret_retourné>
```

Puis redémarrez Notification :

```powershell
cd agt-notification
docker compose up -d --build notification celery-worker
cd ..
```

---

### Étape 2 — Créer une plateforme applicative de test

**`POST /api/v1/auth/platforms`**

Body :
```json
{
  "name": "Plateforme Test",
  "slug": "plateforme-test",
  "allowed_auth_methods": ["email", "phone", "magic_link"],
  "allowed_redirect_urls": []
}
```

**Réponse (201 Created) :**
```json
{
  "id": "<uuid_généré>",
  "name": "Plateforme Test",
  "slug": "plateforme-test",
  "allowed_auth_methods": ["email", "phone", "magic_link"],
  "is_active": true,
  "client_secret": "<secret_affiché_une_seule_fois>"
}
```

> Notez l'`id` — c'est votre **Platform ID**. Il sera requis dans le header `X-Platform-Id` pour tous les appels Register et Login.

**Champs expliqués :**
| Champ | Rôle |
|-------|------|
| `name` | Nom lisible de la plateforme |
| `slug` | Identifiant URL-friendly — doit être unique |
| `allowed_auth_methods` | Méthodes autorisées : `email`, `phone`, `magic_link` |
| `allowed_redirect_urls` | URLs autorisées pour le callback magic link |
| `client_secret` | Secret affiché une seule fois — à stocker immédiatement |

---

### Étape 3 — Lister les plateformes

**`GET /api/v1/auth/platforms`**

Retourne toutes les plateformes y compris les inactives.

```json
{
  "data": [
    {
      "id": "<uuid>",
      "name": "AGT Notification",
      "slug": "agt-notification",
      "is_active": true
    },
    {
      "id": "<uuid>",
      "name": "Plateforme Test",
      "slug": "plateforme-test",
      "is_active": true
    }
  ]
}
```

---

### Étape 4 — Modifier une plateforme

**`PUT /api/v1/auth/platforms/{platform_id}`**

Exemple — ajouter `magic_link` aux méthodes autorisées :

```json
{
  "allowed_auth_methods": ["email", "phone", "magic_link"]
}
```

Réponse : objet plateforme mis à jour avec `updated_at` incrémenté.

---

### Étape 5 — Désactiver une plateforme

**`DELETE /api/v1/auth/platforms/{platform_id}`**

> ⚠️ **C'est un soft delete.** La plateforme n'est pas supprimée de la DB — elle passe à `is_active: false` et reste visible dans le GET. Cela permet de révoquer proprement les tokens S2S émis avant la désactivation.

Je vous conseille de créer rapidement une ``plateforme Test to delete`` comme ci haut pour faire ceci car vous allez utiliser plateform test plus bas.voici un body à utiliser:

```json
{
  "name": "Plateforme Test to delete",
  "slug": "plateforme-test-to-delete",
  "allowed_auth_methods": ["email", "phone", "magic_link"],
  "allowed_redirect_urls": []
}
````

**Réponse (200 OK) :**
```json
{
  "message": "Platform deactivated",
  "is_active": false
}
```

---

## 6. Groupe 3 — S2S (Service-to-Service)

### Rôle
Quand un microservice doit appeler un autre, il ne peut pas utiliser un token utilisateur. Il utilise un **token S2S**, généré depuis le `client_id` + `client_secret` de sa plateforme.

**Sans token S2S valide dans le header `Authorization: Bearer` → les appels inter-services sont rejetés avec 401.**

Les services mettent ce token en cache Redis et le renouvellent avant expiration (marge de 60s).

---

### Test 1 — `POST /api/v1/auth/s2s/token` — Générer un token S2S

**Headers requis :** aucun — les credentials sont dans le body.

Body (utilisez les credentials de la Plateforme Test) :
```json
{
  "client_id": "<platform_id_plateforme_test>",
  "client_secret": "<client_secret_plateforme_test>"
}
```

**Réponse (200 OK) :**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "service_name": "Plateforme Test"
}
```

> **Durée : 3600s (1h).** Notez ce token — il sera utilisé pour créer les templates dans Notification.

**Contenu du JWT (décodable sur jwt.io) :**
```json
{
  "sub": "<platform_id>",
  "type": "s2s",
  "service_name": "Plateforme Test",
  "iss": "agt-auth",
  "aud": "agt-ecosystem"
}
```

> **Note importante :** `sub` = `client_id` de la plateforme. C'est ce que les autres services lisent comme `platform_id`. Le champ `type: "s2s"` permet aux services de distinguer token utilisateur vs token service.

---

### Test 2 — `POST /api/v1/auth/s2s/introspect` — Valider un token S2S

**Headers requis :** `X-Admin-API-Key`

Permet à un service qui reçoit un token S2S de vérifier sa validité sans décoder le JWT lui-même.

Body :
```json
{
  "token": "<access_token_s2s>"
}
```

**Réponse (200 OK) :**
```json
{
  "active": true,
  "client_id": "<platform_id>",
  "service_name": "Plateforme Test",
  "exp": 1776213594
}
```

---

## 7. Prérequis Register — Créer les templates Notification

Avant tout test Register, les 4 templates suivants doivent exister dans Notification pour votre plateforme. Auth les appelle par leur nom exact lors des flux d'inscription et de récupération de mot de passe.

| Template | Canal | Déclenché par |
|----------|-------|---------------|
| `auth_verify_email` | email | Register email |
| `auth_otp_sms` | sms | Register/Login phone |
| `auth_magic_link` | email | Login magic link |
| `auth_reset_password` | email | Forgot password |

### Authentification Swagger Notification

Dans Swagger Notification (http://localhost:7002/api/v1/docs/), cliquez sur **Authorize** et entrez le token S2S généré à l'étape précédente :

```
Bearer <access_token_s2s>
```

> ⚠️ Le token S2S expire en 1h. Si vous obtenez un 401 → régénérez-en un via `POST /auth/s2s/token`.

### Champs expliqués pour la création de templates (`POST /api/v1/templates`)

| Champ | Rôle |
|-------|------|
| `name` | Identifiant métier — nom exact appelé par Auth |
| `channel` | Canal d'envoi : `email`, `sms`, `push`, `in_app` |
| `body` | Contenu du message — supporte les variables Jinja2 `{{ variable }}` |
| `subject` | Objet de l'email — supporte aussi Jinja2 |
| `platform_id` | Lie le template à une plateforme. Si absent → template global |
| `locale` | Langue (`fr` par défaut) |
| `category` | `transactional` par défaut |

---

**Template 1 — `auth_verify_email`**

Envoyé à l'inscription par email. Contient le lien d'activation du compte.

```json
{
  "name": "auth_verify_email",
  "channel": "email",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": "Vérifiez votre adresse email — {{ platform_name }}",
  "body": "Bonjour {{ first_name }},\n\nMerci de vous être inscrit sur {{ platform_name }}.\n\nCliquez sur le lien ci-dessous pour vérifier votre adresse email :\n\n{{ verification_url }}\n\nCe lien expire dans {{ expires_in_minutes }} minutes.\n\nSi vous n'avez pas créé de compte, ignorez cet email.\n\nL'équipe {{ platform_name }}",
  "locale": "fr",
  "category": "transactional"
}
```

---

**Template 2 — `auth_otp_sms`**

Envoyé lors d'un register ou login par téléphone. Contient le code OTP à usage unique.

```json
{
  "name": "auth_otp_sms",
  "channel": "sms",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": null,
  "body": "Bonjour {{ first_name }}, votre code de vérification {{ platform_name }} est : {{ otp_code }}. Valable {{ expires_in_minutes }} minutes. Ne le partagez jamais.",
  "locale": "fr",
  "category": "transactional"
}
```

---

**Template 3 — `auth_magic_link`**

Envoyé lors d'un login sans mot de passe. Contient le lien de connexion à usage unique.

```json
{
  "name": "auth_magic_link",
  "channel": "email",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": "Votre lien de connexion — {{ platform_name }}",
  "body": "Bonjour {{ first_name }},\n\nVous avez demandé un lien de connexion sans mot de passe.\n\nCliquez ici pour vous connecter :\n\n{{ magic_link_url }}\n\nCe lien expire dans {{ expires_in_minutes }} minutes. Il ne peut être utilisé qu'une seule fois.\n\nSi vous n'avez pas fait cette demande, ignorez cet email.\n\nL'équipe {{ platform_name }}",
  "locale": "fr",
  "category": "transactional"
}
```

---

**Template 4 — `auth_reset_password`**

Envoyé lors d'une demande de réinitialisation de mot de passe.

```json
{
  "name": "auth_reset_password",
  "channel": "email",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": "Réinitialisation de votre mot de passe — {{ platform_name }}",
  "body": "Bonjour {{ first_name }},\n\nVous avez demandé la réinitialisation de votre mot de passe.\n\nCliquez sur le lien ci-dessous pour choisir un nouveau mot de passe :\n\n{{ reset_url }}\n\nCe lien expire dans {{ expires_in_minutes }} minutes. Il ne peut être utilisé qu'une seule fois.\n\nSi vous n'avez pas fait cette demande, ignorez cet email — votre mot de passe reste inchangé.\n\nL'équipe {{ platform_name }}",
  "locale": "fr",
  "category": "transactional"
}
```

> ⚠️ **Bug connu :** `PUT /api/v1/templates/{id}` n'affiche pas le champ body dans Swagger.
> Pour mettre à jour un template existant, utilisez ce script PowerShell :
>
> ```powershell
> $r = Invoke-RestMethod -Uri "http://localhost:7000/api/v1/auth/s2s/token" `
>   -Method POST -ContentType "application/json" `
>   -Body '{"client_id": "<platform_id>", "client_secret": "<secret>"}'
> $token = $r.access_token
> $body = @{
>   subject = "Nouveau sujet {{ platform_name }}"
>   body    = "Nouveau corps {{ first_name }}"
>   locale  = "fr"
> } | ConvertTo-Json
> Invoke-RestMethod -Uri "http://localhost:7002/api/v1/templates/<template_id>" `
>   -Method PUT -ContentType "application/json" `
>   -Headers @{Authorization = "Bearer $token"} -Body $body
> ```

---

## 8. Groupe 4 — Register

### Rôle
Point d'entrée de tout utilisateur dans l'écosystème. Auth crée le compte, provisionne le profil dans Users, puis déclenche l'envoi de l'email de vérification via Notification.

### Flux complet Register email

```
Client → POST /auth/register (header X-Platform-Id)
             ↓
         Auth crée le compte (email_verified: false)
         Auth crée un VerificationToken (expire 1h)
             ↓
         Auth → Users : POST /users  (S2S — provisioning profil)
             ↓
         Auth → Notification : POST /notifications/send  (S2S)
             ↓
         Worker Celery → SMTP → Mailpit (dev)
             ↓
         Utilisateur reçoit l'email → copie le token du lien
             ↓
         POST /auth/verify-email  {token: "..."}
             ↓
         email_verified: true → login possible
```

---

### Test 1 — `POST /api/v1/auth/register`

**Headers requis :**
```
X-Platform-Id: <platform_id_plateforme_test>
```

**Body :**
```json
{
  "email": "jane.doe@example.com",
  "password": "Test1234!",
  "method": "email",
  "first_name": "Jane",
  "last_name": "Doe"
}
```

**Champs expliqués :**
| Champ | Obligatoire | Rôle |
|-------|-------------|------|
| `email` | ✅ si method=email | Adresse email |
| `password` | ✅ si method=email | Minimum 8 caractères |
| `method` | ✅ | `email` ou `phone` |
| `first_name` | optionnel | Prénom — utilisé dans les emails de notification |
| `last_name` | optionnel | Nom de famille |
| `phone` | ✅ si method=phone | Numéro de téléphone |

**Réponse attendue (201 Created) :**
```json
{
  "id": "2fba21ba-c47a-46e9-bf09-850ed365f039",
  "email": "jane.doe@example.com",
  "email_verified": false,
  "registration_method": "email",
  "registration_platform_id": "<platform_id>",
  "message": "Verification email sent"
}
```

Vérifiez que l'email est arrivé dans **Mailpit** : http://localhost:8025

**Erreurs possibles :**
| Code | Message | Cause |
|------|---------|-------|
| 400 | `Header X-Platform-Id requis` | Header manquant |
| 400 | `Plateforme invalide ou inactive` | UUID inconnu ou plateforme désactivée |
| 409 | `Email déjà utilisé` | Doublon |
| 400 | `Méthode 'X' non autorisée sur cette plateforme` | Méthode absente de `allowed_auth_methods` |
| 429 | `Trop de requêtes` | Rate limit — voir Troubleshooting |

---

### Test 2 — `POST /api/v1/auth/verify-email`

Après réception de l'email dans Mailpit, copiez le token depuis l'URL du lien :
```
http://localhost:7000/api/v1/auth/verify-email?token=<COPIEZ_CETTE_VALEUR>
```

**Headers requis :** aucun — endpoint public.

**Body :**
```json
{
  "token": "<token_copié_depuis_le_lien>"
}
```

**Réponse attendue (200 OK) :**
```json
{
  "message": "Email verified",
  "email_verified": true
}
```

**Erreurs possibles :**
| Code | Message | Cause |
|------|---------|-------|
| 400 | `Token invalide` | Token inexistant en DB |
| 400 | `Token expiré ou déjà utilisé` | Token consommé ou expiré (délai 1h) |

---

### Test 3 — `POST /api/v1/auth/resend-verification`

À utiliser quand l'utilisateur n'a pas reçu ou a perdu l'email de vérification. Invalide les anciens tokens et en génère un nouveau.
pour tester,créer rapidement un nouveau user sans vérifier son mail:

```json
{
  "email": "jane.doe.test@example.com",
  "password": "Test1234!",
  "method": "email",
  "first_name": "Jane test",
  "last_name": "Doe test"
}
````
Aller ensuite demander le renvoi de mail

**Headers requis :** aucun — endpoint public.

**Body :**
```json
{
  "email": "jane.doe.test@example.com",
  "platform_id": "<platform_id_plateforme_test>"
}
```

**Réponse attendue (200 OK) — toujours identique, même si l'email n'existe pas :**
```json
{
  "message": "Si cet email existe et n'est pas vérifié, un nouveau lien a été envoyé."
}
```

> **Note sécurité :** La réponse est intentionnellement générique pour éviter l'énumération d'emails.

Vérifiez qu'un nouvel email est arrivé dans Mailpit avec un nouveau lien.

---

## 9. Groupe 5 — Login

### Rôle
Authentifier un utilisateur et lui retourner un `access_token` JWT + un `refresh_token` en cookie HTTP-only. C'est le point d'entrée de toute session utilisateur.

**Règle importante :** un utilisateur dont l'email n'est pas vérifié reçoit un `403`. Il doit d'abord vérifier son email ou utiliser `resend-verification`.

### Tokens retournés

| Token | Durée | Stockage | Visible dans le body |
|-------|-------|----------|----------------------|
| `access_token` | 15 min (900s) | Mémoire côté client | ✅ oui |
| `refresh_token` | 30 jours | Cookie HTTP-only | ❌ non — inaccessible depuis JS (protection XSS) |

### Contenu du JWT access_token (décodable sur jwt.io)

```json
{
  "sub": "<user_id>",
  "iss": "agt-auth",
  "aud": "agt-ecosystem",
  "session_id": "<session_id>",
  "platform_id": "<platform_id>",
  "email": "jane.doe@example.com",
  "email_verified": true,
  "two_fa_verified": false,
  "exp": 1776214162
}
```

---

### Test 1 — Login valide

**`POST /api/v1/auth/login`**

**Headers requis :** aucun — endpoint public.

**Body :**
```json
{
  "email": "jane.doe@example.com",
  "password": "Test1234!",
  "platform_id": "<platform_id_plateforme_test>"
}
```

**Réponse attendue (200 OK) — sans 2FA :**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 900,
  "requires_2fa": false
}
```

**Réponse si 2FA activé :**
```json
{
  "requires_2fa": true,
  "temp_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 300
}
```
→ Le `temp_token` doit être utilisé sur `POST /auth/2fa/verify`.

**Ce qui se passe sous le capot :**
1. Vérifie que la plateforme est active
2. Vérifie que l'email existe
3. Vérifie que le compte n'est pas bloqué ou désactivé
4. Vérifie `email_verified` → 403 si false
5. Vérifie le mot de passe → incrémente `failed_attempts` si incorrect
6. Crée une session en DB
7. Génère `access_token` (body) + `refresh_token` (cookie HTTP-only)
8. Enregistre dans `LoginHistory`

---

### Test 2 — Login avec mauvais mot de passe

**Body :**
```json
{
  "email": "jane.doe@example.com",
  "password": "MauvaisMotDePasse!",
  "platform_id": "<platform_id_plateforme_test>"
}
```

**Réponse attendue (401 Unauthorized) :**
```json
{
  "detail": "Identifiants invalides."
}
```

---

### Test 3 — Login avec email non vérifié

Inscrivez un nouvel utilisateur **sans vérifier son email**, puis tentez de vous connecter.

**Body :**
```json
{
  "email": "jane.doe.test@example.com",
  "password": "Test1234!",
  "platform_id": "<platform_id_plateforme_test>"
}
```

**Réponse attendue (403 Forbidden) :**
```json
{
  "detail": "Email non vérifié. Consultez votre boîte mail ou renvoyez le lien de vérification."
}
```

→ Utilisez `POST /auth/resend-verification` pour renvoyer le lien, vérifiez l'email dans Mailpit, puis retestez le login.

**Erreurs possibles :**
| Code | Message | Cause |
|------|---------|-------|
| 401 | `Identifiants invalides` | Email inconnu ou mauvais mot de passe |
| 403 | `Email non vérifié...` | `email_verified: false` |
| 403 | Autre message | Compte bloqué ou désactivé |
| 400 | `Plateforme invalide` | UUID inconnu ou inactif |

---

## 10. Troubleshooting

| Symptôme | Cause probable | Solution |
|----------|---------------|----------|
| `429 Trop de requêtes` | Rate limit Redis | `docker exec agt-auth-redis redis-cli FLUSHDB` |
| `404 Template introuvable` | Template non créé dans Notification | Créer les 4 templates (section 7) |
| Email reçu mais variables vides | Nom de variable incorrect dans le template | Vérifier que les noms correspondent exactement à ceux listés en section 7 |
| Email arrivé mais `first_name` vide | `first_name` non envoyé dans le body du register | Ajouter `"first_name"` dans le body |
| `UserResolver: 404` dans les logs du worker | Race condition — Notification appelé avant Users | Vérifier que `provision_user` est avant `NotificationClient.send` dans `views_auth.py` |
| `401` sur appel Notification | Token S2S expiré | Régénérer via `POST /auth/s2s/token` |
| `badly formed hexadecimal UUID` | Placeholder `<uuid>` non remplacé | Utiliser un vrai UUID de plateforme |
| Email non reçu dans Mailpit | Worker Celery en erreur | `docker logs agt-notif-worker --tail=30` |
| `SENDGRID_API_KEY non configuré` dans les logs | Provider mal configuré | Vérifier que `SMTPProvider` est en premier dans `PROVIDER_MAP` dans `providers/providers.py` |

---

## 11. Commandes utiles

```powershell
# Lancer le MVP
.\deploy_mvp.ps1

# Reset soft (conserve les données)
.\reset_mvp.ps1

# Reset complet (supprime tout — reconfigurer depuis section 5)
.\reset_mvp.ps1 --clean

# Rebuild Auth uniquement
cd agt-auth && docker compose up -d --build auth && cd ..

# Rebuild Notification (service + worker)
cd agt-notification
docker compose up -d --build notification celery-worker
cd ..

# Vider le rate limiting Redis Auth
docker exec agt-auth-redis redis-cli FLUSHDB

# Logs Auth en temps réel
docker logs agt-auth-service --follow

# Logs worker Notification
docker logs agt-notif-worker --tail=50

# Régénérer un token S2S (PowerShell)
$r = Invoke-RestMethod -Uri "http://localhost:7000/api/v1/auth/s2s/token" `
  -Method POST -ContentType "application/json" `
  -Body '{"client_id": "<platform_id>", "client_secret": "<secret>"}'
$token = $r.access_token
Write-Host "Token S2S : $token"

# Tests pytest Auth
docker exec agt-auth-service python -m pytest -v
```

---

## Ce qui reste à tester et documenter

Ce guide s'arrête ici — les groupes suivants sont à tester, valider et documenter en suivant la même méthode :

| Groupe | Endpoints principaux |
|--------|---------------------|
| **Sessions** | `POST /refresh`, `POST /logout`, `GET /sessions`, `DELETE /sessions/{id}`, `GET /verify-token` |
| **Profile** | `GET /me`, `GET /login-history`, `GET /stats/{user_id}` |
| **Password** | `POST /forgot-password`, `POST /reset-password`, `PUT /change-password` |
| **2FA** | `POST /2fa/enable`, `POST /2fa/confirm`, `POST /2fa/verify`, `POST /2fa/disable` |
| **Admin** | `POST /admin/block/{id}`, `POST /admin/unblock/{id}`, `POST /account/deactivate`, `DELETE /admin/purge/{id}` |
| **OAuth** | `GET /oauth/google`, `GET /oauth/google/callback`, `GET /oauth/facebook`, `GET /oauth/facebook/callback` |

**Compte de test disponible après avoir suivi ce guide :**

| Email | Password | Statut |
|-------|----------|--------|
| `jane.doe@example.com` | `Test1234!` | vérifié — prêt pour les tests Sessions/Profile/Password/2FA |

---

*GUIDE_AUTH.md — AG Technologies — 15 avril 2026*
*Testé et validé sur Auth Service v1.0*

---
---
# Partie 2 du Guide

## 10. Groupe 6 — Sessions

### Rôle
Gérer le cycle de vie des sessions utilisateur : lister les sessions actives, révoquer une session spécifique (déconnexion à distance), renouveler l'access_token et se déconnecter.

### Prérequis
Être connecté avec un `access_token` valide dans Swagger (Authorize).

---

### Test 1 — `GET /api/v1/auth/verify-token`

Vérifie que le token courant est valide.

**Headers requis :** `Authorization: Bearer <token>`

**Réponse attendue (200 OK) :**
```json
{
  "valid": true,
  "user_id": "<uuid>",
  "platform_id": "<uuid>",
  "expires_at": "2026-04-15T13:48:26Z"
}
```

**Réponse si révoqué ou expiré :**
```json
{
  "detail": {
    "valid": "False",
    "reason": "session_revoked"
  }
}
```

---

### Test 2 — `GET /api/v1/auth/sessions`

Liste toutes les sessions actives. La session courante a `is_current: true`.

**Réponse attendue (200 OK) :**
```json
{
  "data": [
    {
      "id": "<session_id>",
      "platform": "plateforme-test",
      "ip_address": "172.18.0.1",
      "user_agent": "Mozilla/5.0...",
      "created_at": "2026-04-15T...",
      "is_current": true
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1
}
```

---

### Test 3 — `DELETE /api/v1/auth/sessions/{id}`

Révoque une session spécifique — simule la déconnexion depuis un autre appareil. Utiliser l'`id` d'une session non courante.

**Réponse attendue (200 OK) :**
```json
{
  "message": "Session revoked"
}
```

---

### Test 4 — `POST /api/v1/auth/refresh`

Renouvelle l'`access_token` à partir du `refresh_token` en cookie HTTP-only. Pas de body requis — le cookie est envoyé automatiquement par le navigateur.

**Réponse attendue (200 OK) :**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "Bearer",
  "expires_in": 900
}
```

---

### Test 5 — `POST /api/v1/auth/logout`

Révoque la session courante et invalide le cookie `refresh_token`.

**Réponse attendue (200 OK) :**
```json
{
  "message": "Logged out successfully"
}
```

**Vérification :** relancer `POST /refresh` après logout → doit retourner `401 Refresh token manquant`.

---

### `POST /api/v1/auth/token/exchange`

> ⏭️ **Reporté — à tester dans le contexte OAuth.** Cet endpoint échange un cookie `access_token` (posé par le callback magic-link ou OAuth) contre un token Bearer visible dans le body. Ne peut pas être testé sans frontend ou flux OAuth complet.

---

## 11. Groupe 7 — Profile

### Rôle
Accéder au profil d'authentification de l'utilisateur connecté, consulter son historique de connexions et ses statistiques.

---

### Test 1 — `GET /api/v1/auth/me`

**Réponse attendue (200 OK) :**
```json
{
  "id": "<uuid>",
  "email": "john.smith@example.com",
  "phone": null,
  "email_verified": true,
  "phone_verified": false,
  "two_fa_enabled": false,
  "registration_method": "email",
  "is_blocked": false,
  "is_deactivated": false,
  "created_at": "2026-04-15T..."
}
```

---

### Test 2 — `GET /api/v1/auth/login-history`

**Réponse attendue (200 OK) :**
```json
{
  "data": [
    {
      "id": "<uuid>",
      "method": "email",
      "platform": "plateforme-test",
      "ip_address": "172.18.0.1",
      "success": true,
      "created_at": "2026-04-15T..."
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 4
}
```

---

### Test 3 — `GET /api/v1/auth/stats/{user_id}`

Utiliser l'`id` retourné par `GET /me`.

**Réponse attendue (200 OK) :**
```json
{
  "user_id": "<uuid>",
  "total_logins": 4,
  "last_login": "2026-04-15T12:57:20+00:00",
  "active_sessions": 2
}
```

---

## 12. Groupe 8 — Password

### Rôle
Réinitialiser ou changer le mot de passe. Le forgot-password et reset-password sont publics. Le change-password nécessite d'être connecté.

---

### Test 1 — `POST /api/v1/auth/forgot-password`

**Headers requis :** aucun — endpoint public.

**Body :**
```json
{
  "email": "john.smith@example.com"
}
```

**Réponse attendue (200 OK) :**
```json
{
  "message": "Reset link sent if account exists"
}
```

Vérifiez l'email dans Mailpit — le lien contient un token à copier.

> ⚠️ Rate limit actif sur cet endpoint. Si vous obtenez `429` → `docker exec agt-auth-redis redis-cli FLUSHDB`

---

### Test 2 — `POST /api/v1/auth/reset-password`

Copier le token depuis l'URL dans Mailpit :
```
http://localhost:7000/api/v1/auth/reset-password?token=<COPIER_CE_TOKEN>
```

**Body :**
```json
{
  "token": "<token_copié>",
  "new_password": "NewPass1234!"
}
```

**Réponse attendue (200 OK) :**
```json
{
  "message": "Password reset successfully"
}
```

> Toutes les sessions actives sont révoquées après reset.

---

### Test 3 — `PUT /api/v1/auth/change-password`

**Headers requis :** `Authorization: Bearer <token>`

**Body :**
```json
{
  "current_password": "NewPass1234!",
  "new_password": "Test1234!"
}
```

**Réponse attendue (200 OK) :**
```json
{
  "message": "Password changed successfully"
}
```

---

## 13. Groupe 9 — Admin

### Rôle
Endpoints d'administration — blocage, déblocage, désactivation et purge RGPD des utilisateurs. Tous ces endpoints utilisent une **API Key admin** — pas de JWT.

**Dans Swagger, cliquez sur Authorize et saisissez :**
```
X-Admin-API-Key: change-me-admin-api-key-very-secret
```

---

### Test 1 — `POST /api/v1/auth/admin/block/{user_id}`

**Réponse attendue (200 OK) :**
```json
{
  "message": "User blocked",
  "user_id": "<uuid>",
  "is_blocked": true
}
```

Toutes les sessions de l'utilisateur sont révoquées automatiquement.

---

### Test 2 — `POST /api/v1/auth/admin/unblock/{user_id}`

**Réponse attendue (200 OK) :**
```json
{
  "message": "User unblocked",
  "user_id": "<uuid>",
  "is_blocked": false
}
```

---

### Test 3 — `POST /api/v1/auth/account/deactivate`

Désactivation par l'utilisateur lui-même. Nécessite un Bearer token valide.

**Body :**
```json
{
  "password": "<mot_de_passe_actuel>"
}
```

**Réponse attendue (200 OK) :**
```json
{
  "message": "Account deactivated",
  "is_deactivated": true
}
```

> **Soft delete** — le compte peut être réactivé par un admin.

---

### Test 4 — `DELETE /api/v1/auth/admin/purge/{user_id}`

**⚠️ Irréversible.** Supprime toutes les données de l'utilisateur : tokens, sessions, historique, profil OAuth.

**Réponse attendue (200 OK) :**
```json
{
  "message": "User purged",
  "user_id": "<uuid>",
  "purged": true
}
```

---

## 14. Groupes reportés

| Groupe | Raison | Quand |
|--------|--------|-------|
| **2FA (TOTP)** | Nécessite une app TOTP (Google Authenticator) | Prochaine session |
| **OAuth Google/Facebook** | Nécessite credentials OAuth configurés | Post-déploiement serveur |
| **OTP SMS** | Nécessite provider SMS configuré | Post-déploiement serveur |
| **token/exchange** | Nécessite flux OAuth ou magic-link complet | Post-déploiement serveur |

---

## 15. Bugs connus

| # | Bug | Fichier | Action |
|---|-----|---------|--------|
| 1 | `SENDGRID_API_KEY non configuré` dans worker quand Users retourne 404 | `agt-notification/providers/providers.py` | Vérifier ordre `PROVIDER_MAP` |
| 2 | Email non reçu quand provisioning Users échoue | `agt-notification/workers/tasks.py` | Worker tombe sur Sendgrid au lieu de SMTP |
| 3 | `resend-verification` — `first_name` toujours vide | `agt-auth/apps/authentication/views_auth.py` | Appeler `get_profile_by_auth_id` |
| 4 | Migrations absentes du repo | Tous les services | Générer et commiter les migrations |
| 5 | `deploy_mvp.ps1` lance `migrate` trop tôt | `deploy_mvp.ps1` | Intégrer `makemigrations` dans le script |
| 6 | `PUT /templates/{id}` — body non visible dans Swagger Notification | `agt-notification/apps/templates_mgr/views.py` | Ajouter `@extend_schema` |

---

## 16. Perspectives d'évolution

| # | Perspective |
|---|-------------|
| 1 | **2FA par email** — configurable par plateforme (`totp` ou `email`) |
| 2 | **OAuth** — Google + Facebook — post-déploiement |
| 3 | **Réactivation de compte** — endpoint admin dédié |
| 4 | **`makemigrations` automatique** dans `deploy_mvp.ps1` |
| 5 | **OTP SMS** — quand provider SMS configuré |

---

*GUIDE_AUTH.md — AG Technologies — 15 avril 2026*
*Testé et validé sur Auth Service v1.0*