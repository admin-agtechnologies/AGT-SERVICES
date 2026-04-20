# AGT — Guide Complet du Service Notification v1.2

> Ce guide vous accompagne pas à pas pour configurer, démarrer, comprendre et tester toutes les routes du service Notification de l'écosystème AGT. Il est conçu pour être accessible à un débutant tout en étant complet pour un développeur confirmé.

---

## Table des matières

1. [Rôle du service dans l'architecture AGT](#1-rôle-du-service)
2. [Prérequis](#2-prérequis)
3. [Lancement du service](#3-lancement-du-service)
4. [Configuration initiale obligatoire](#4-configuration-initiale-obligatoire)
5. [Comprendre l'authentification](#5-comprendre-lauthentification)
6. [Templates — Créer et gérer les modèles de messages](#6-templates)
7. [Envoi de notifications](#7-envoi-de-notifications)
8. [Notifications planifiées](#8-notifications-planifiées)
9. [Notifications In-App](#9-notifications-in-app)
10. [Préférences utilisateur](#10-préférences-utilisateur)
11. [Device Tokens — Notifications Push](#11-device-tokens)
12. [Campagnes — Envoi en masse](#12-campagnes)
13. [Statistiques et Logs](#13-statistiques-et-logs)
14. [Configuration des canaux par plateforme](#14-configuration-des-canaux)
15. [Intégration dans un frontend](#15-intégration-dans-un-frontend)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. Rôle du service

Le service Notification est le **hub de communication** de l'écosystème AGT. Il est responsable de l'envoi de tous les messages vers les utilisateurs, quel que soit le canal.

### Ce qu'il fait

- Envoie des **emails** (via SMTP local Mailpit en dev, SendGrid en prod)
- Envoie des **SMS** (via Twilio en prod, Console en dev)
- Envoie des **notifications push** (via FCM pour Android/Web)
- Gère les **notifications in-app** (messages dans l'interface de l'application)
- Gère des **campagnes** d'envoi en masse
- Gère les **notifications planifiées** (envoi différé à une date future)
- Gère les **préférences** de notification des utilisateurs
- Gère les **templates** dynamiques avec variables (moteur Jinja2)

### Sa place dans l'architecture

```
Auth Service ──────────────────────────────┐
                                           ↓
Autres services ──────────────→  Notification Service (7002)
                                           ↓
                              ┌────────────┴────────────┐
                              ↓                         ↓
                         RabbitMQ                    Redis
                              ↓
                         Celery Worker
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
               Mailpit (dev)       SendGrid (prod)
```

### Ce qu'il ne fait PAS

- Il ne stocke pas les données métier des utilisateurs (c'est le rôle de Users Service)
- Il ne génère pas les tokens d'authentification (c'est le rôle de Auth Service)
- Il ne contient pas de logique métier profonde

---

## 2. Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Docker Desktop** installé et démarré
- **Le MVP AGT lancé** (Auth, Users, Notification, infrastructure)
- **Une plateforme S2S** créée dans Auth Service
- **Un token S2S valide** pour vous authentifier sur les routes

> ℹ️ Si ce n'est pas encore fait, suivez le [GETTING_STARTED.md](./GETTING_STARTED.md) pour lancer le MVP complet.

---

## 3. Lancement du service

### Option A — Via le script MVP (recommandé)

À la racine du projet AGT :

```bash
# Linux / macOS
bash deploy_mvp.sh

# Windows (PowerShell en administrateur)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\deploy_mvp.ps1
```

### Option B — Service seul (pour le développement)

```bash
cd agt-notification
bash scripts/setup.sh       # Linux/macOS
.\scripts\setup.ps1         # Windows
```

### Vérification

```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep notif
```

Vous devez voir 3 containers `Up` :

| Container | Rôle |
|-----------|------|
| `agt-notif-service` | API REST (port 7002) |
| `agt-notif-worker` | Worker Celery (envoi asynchrone) |
| `agt-notif-beat` | Scheduler Celery (notifications planifiées) |

### Health Check

```bash
curl http://localhost:7002/api/v1/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "broker": "ok",
  "version": "1.0.0"
}
```

### Swagger UI

```
http://localhost:7002/api/v1/docs/
```

---

## 4. Configuration initiale obligatoire

### Étape préalable — Migrations (premier lancement uniquement)

Lors du premier lancement ou après un reset complet de la base de données, les bases sont vides. Vous devez générer et appliquer les schémas avant toute utilisation.

**Auth :**
```bash
docker exec -it agt-auth-service python manage.py makemigrations authentication platforms
docker exec -it agt-auth-service python manage.py migrate
```

**Users :**
```bash
docker exec -it agt-users-service python manage.py makemigrations users roles documents
docker exec -it agt-users-service python manage.py migrate
```

**Notification :**
```bash
docker exec -it agt-notif-service python manage.py makemigrations notifications templates_mgr campaigns devices
docker exec -it agt-notif-service python manage.py migrate
```

> ⚠️ Ces commandes sont à exécuter **une seule fois** lors du premier lancement ou après un reset complet. Si les tables existent déjà, Django ignorera les migrations déjà appliquées.

---

### Étape 1 — Créer une plateforme S2S dans Auth

Dans Swagger Auth (`http://localhost:7000/api/v1/docs/`), appelez `POST /api/v1/auth/platforms` :

**Header requis :**
```
X-Admin-API-Key: votre-cle-admin
```

**Body :**
```json
{
  "name": "Mon Application",
  "slug": "mon-application",
  "allowed_auth_methods": ["email"],
  "allowed_redirect_urls": ["http://localhost:3000/callback"]
}
```

**Réponse :**
```json
{
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "client_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "client_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

> ⚠️ **Conservez précieusement** le `client_id` et le `client_secret` — le `client_secret` ne sera plus affiché après.

---

### Étape 2 — Obtenir un token S2S

Dans Swagger Auth, appelez `POST /api/v1/auth/s2s/token` :

```json
{
  "client_id": "votre-client-id",
  "client_secret": "votre-client-secret"
}
```

**Réponse :**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

> ℹ️ Ce token expire après 1 heure. Renouvelez-le en rappelant ce endpoint.

---

### Étape 3 — S'authentifier dans Swagger Notification

1. Ouvrez `http://localhost:7002/api/v1/docs/`
2. Cliquez sur **Authorize** (icône cadenas)
3. Entrez votre token S2S dans le champ **BearerAuth**
4. Cliquez **Authorize** puis **Close**

---

### Étape 4 — Configurer le .env du service Notification

Dans `agt-notification/.env` :

```env
S2S_AUTH_URL=http://agt-auth-service:7000/api/v1
S2S_CLIENT_ID=votre-client-id-du-service-notification
S2S_CLIENT_SECRET=votre-client-secret-du-service-notification
```

Après modification, redémarrez le worker :

```bash
docker restart agt-notif-worker
```

> ⚠️ **Restart vs Rebuild :** En développement, le code est monté en volume (`- .:/app`). Un simple `docker restart` suffit après modification du code ou du `.env`. Le rebuild (`--build`) n'est nécessaire que si vous modifiez le `Dockerfile` ou `requirements.txt`.

---

### Étape 5 — Créer les templates système (obligatoire pour Auth)

Les templates système sont des templates **sans `platform_id`** (globaux). Créez ces 4 templates via `POST /api/v1/templates` :

**Template 1 — Vérification email :**
```json
{
  "name": "auth_verify_email",
  "channel": "email",
  "subject": "Vérifiez votre adresse email",
  "body": "Bonjour,\n\nCliquez sur ce lien pour vérifier votre email : {{verification_url}}\n\nCe lien expire dans {{expires_in_minutes}} minutes.\n\n{{platform_name}}",
  "category": "transactional"
}
```

**Template 2 — Réinitialisation mot de passe :**
```json
{
  "name": "auth_reset_password",
  "channel": "email",
  "subject": "Réinitialisation de votre mot de passe",
  "body": "Bonjour,\n\nCliquez sur ce lien pour réinitialiser votre mot de passe : {{reset_url}}\n\nCe lien expire dans {{expires_in_minutes}} minutes.\n\n{{platform_name}}",
  "category": "transactional"
}
```

**Template 3 — Magic Link :**
```json
{
  "name": "auth_magic_link",
  "channel": "email",
  "subject": "Votre lien de connexion",
  "body": "Bonjour,\n\nCliquez sur ce lien pour vous connecter : {{magic_link_url}}\n\nCe lien expire dans {{expires_in_minutes}} minutes.\n\n{{platform_name}}",
  "category": "transactional"
}
```

**Template 4 — OTP SMS :**
```json
{
  "name": "auth_otp_sms",
  "channel": "sms",
  "body": "Votre code de vérification AGT : {{otp_code}}. Expire dans {{expires_in_minutes}} minutes.",
  "category": "transactional"
}
```

> ⚠️ Ne pas inclure le champ `platform_id` — ces templates doivent être globaux.

---

## 5. Comprendre l'authentification

### Deux types d'appelants

| Type | Qui | Comment |
|------|-----|---------|
| **Plateforme applicative** | App mobile, site web, dashboard | Token S2S avec `platform_id` = UUID de la plateforme |
| **Service AGT** | Auth, Users, Payment... | Token S2S avec `platform_id` = UUID du service |

### Comment le service résout les templates

Notification extrait le `platform_id` du token JWT et cherche dans cet ordre :

1. Template avec ce `platform_id` exact → priorité maximale
2. Template global (`platform_id = null`) → fallback universel

### Mécanisme de fallback entre providers

```
Tentative 1 : smtp_local (Mailpit en dev)
      ↓ échec
Tentative 2 : sendgrid
      ↓ échec
Notification marquée "failed"
```

Les logs tracent chaque tentative (`attempt: 1`, `attempt: 2`). Voir deux tentatives est **normal** en dev si SENDGRID_API_KEY n'est pas configuré.

---

## 6. Templates

Un template est un **modèle de message réutilisable** avec des variables dynamiques (moteur Jinja2, syntaxe `{{nom_variable}}`).

### GET /api/v1/templates — Lister

Supporte : `?channel=email&platform_id=uuid&page=1&limit=20`

**Réponse :**
```json
{
  "data": [
    {
      "id": "b18b48c3-a02f-477d-8ae0-e461e8a247d9",
      "name": "auth_verify_email",
      "channel": "email",
      "platform_id": null,
      "category": "transactional"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 4
}
```

---

### POST /api/v1/templates — Créer

**Body :**
```json
{
  "name": "bienvenue_client",
  "channel": "email",
  "subject": "Bienvenue {{prenom}} !",
  "body": "Bonjour {{prenom}},\n\nBienvenue sur {{platform_name}} !",
  "category": "transactional",
  "platform_id": "votre-platform-id",
  "locale": "fr"
}
```

| Champ | Requis | Description |
|-------|--------|-------------|
| `name` | ✅ | Identifiant unique (par plateforme) |
| `channel` | ✅ | `email`, `sms`, `push`, `whatsapp`, `in_app` |
| `body` | ✅ | Corps du message avec `{{variable}}` |
| `subject` | ❌ | Sujet (email uniquement) |
| `category` | ❌ | `transactional` (défaut) ou `marketing` |
| `platform_id` | ❌ | Vide = template global |
| `locale` | ❌ | `fr` par défaut |

**Réponse 201 :** `{"id": "uuid", "name": "bienvenue_client", "channel": "email"}`

**Codes :** 201 Created, 400 Validation error, 409 Name already exists for this platform.

---

### GET /api/v1/templates/{template_id} — Détail

**Réponse :**
```json
{
  "id": "uuid",
  "name": "auth_verify_email",
  "channel": "email",
  "subject": "Vérifiez votre adresse email",
  "body": "Bonjour,\n\nCliquez sur ce lien : {{verification_url}}..."
}
```

---

### PUT /api/v1/templates/{template_id} — Modifier

Crée automatiquement une nouvelle version en conservant l'historique.

**Body :** `{"subject": "Nouveau sujet", "body": "Nouveau corps {{variable}}", "locale": "fr"}`

**Réponse :** `{"message": "Template mis a jour.", "version": 2}`

---

### POST /api/v1/templates/{template_id}/preview — Prévisualiser

> ⚠️ Swagger ne montre pas le champ body pour cette route. Utilisez curl ou Postman.

```bash
curl -s -X POST http://localhost:7002/api/v1/templates/{template_id}/preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer VOTRE_TOKEN" \
  -d '{
    "variables": {
      "verification_url": "https://app.agt.com/verify?token=test123",
      "expires_in_minutes": "60",
      "platform_name": "Mon Application"
    },
    "locale": "fr"
  }'
```

**Réponse :**
```json
{
  "subject": "Vérifiez votre adresse email",
  "body": "Bonjour,\n\nCliquez sur ce lien : https://app.agt.com/verify?token=test123\n\nExpire dans 60 minutes.\n\nMon Application"
}
```

---

### GET /api/v1/templates/{template_id}/versions — Historique

**Réponse :**
```json
{
  "data": [
    {"version": 2, "locale": "fr", "is_current": true, "created_at": "..."},
    {"version": 1, "locale": "fr", "is_current": false, "created_at": "..."}
  ]
}
```

---

### DELETE /api/v1/templates/{template_id} — Désactiver

Suppression logique (`is_active = false`). Le template n'est plus utilisable mais reste en base.

**Réponse :** `{"message": "Template desactive."}`

---

## 7. Envoi de notifications

### POST /api/v1/notifications/send — Envoi unitaire

**Body :**
```json
{
  "user_id": "uuid-de-l-utilisateur",
  "channels": ["email"],
  "template_name": "auth_verify_email",
  "locale": "fr",
  "variables": {
    "verification_url": "https://app.agt.com/verify?token=abc123",
    "expires_in_minutes": "60",
    "platform_name": "Mon Application"
  },
  "category": "transactional",
  "priority": "high",
  "idempotency_key": "unique-key-pour-eviter-doublons"
}
```

| Champ | Requis | Description |
|-------|--------|-------------|
| `user_id` | ✅ | ID Auth de l'utilisateur |
| `channels` | ✅ | `email`, `sms`, `push`, `whatsapp`, `in_app` |
| `template_name` | ✅ | Nom du template |
| `locale` | ❌ | `fr` par défaut |
| `variables` | ❌ | Variables à injecter |
| `category` | ❌ | `transactional`, `marketing` ou `security` |
| `priority` | ❌ | `low`, `normal`, `high`, `critical` |
| `idempotency_key` | ❌ | Évite les doublons |

**Réponse 202 :**
```json
{
  "notifications": [{"id": "uuid", "channel": "email", "status": "pending"}],
  "message": "Notifications queued"
}
```

**Codes :** 202 Accepted, 400, 401, 404 Template not found, 409 Idempotency conflict.

**Ce qui se passe sous le capot :**
```
POST /notifications/send → Validation → Résolution template → Rendu Jinja2
→ Création en base (pending) → RabbitMQ → Worker Celery
→ Appel Users Service (email/téléphone) → Provider (SMTP/SendGrid...) → sent/failed
```

---

### POST /api/v1/notifications/send-bulk — Envoi en masse (max 100)

**Body :**
```json
{
  "user_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "channels": ["email"],
  "template_name": "auth_verify_email",
  "locale": "fr",
  "variables": {"verification_url": "...", "expires_in_minutes": "60", "platform_name": "..."},
  "category": "transactional"
}
```

**Réponse 202 :** `{"message": "3 notifications queued", "total": 3}`

**Codes :** 202 Accepted, 400 (dont user_ids > 100), 401.

---

## 8. Notifications planifiées

Les notifications planifiées permettent de programmer l'envoi d'un message à une **date et heure future**. Le worker Celery Beat les consomme automatiquement à l'heure prévue.

### POST /api/v1/notifications/schedule — Planifier

**Body :**
```json
{
  "user_id": "uuid-de-l-utilisateur",
  "channels": ["email"],
  "template_name": "auth_verify_email",
  "locale": "fr",
  "variables": {
    "verification_url": "https://app.agt.com/verify?token=sched123",
    "expires_in_minutes": "60",
    "platform_name": "Mon Application"
  },
  "scheduled_at": "2026-04-20T10:00:00Z"
}
```

| Champ | Requis | Description |
|-------|--------|-------------|
| `user_id` | ✅ | ID Auth de l'utilisateur |
| `channels` | ✅ | Canaux souhaités (le premier est utilisé) |
| `template_name` | ✅ | Nom du template |
| `scheduled_at` | ✅ | Date/heure UTC future |
| `variables` | ❌ | Variables du template |
| `locale` | ❌ | `fr` par défaut |

**Réponse 201 :**
```json
{
  "id": "78b9a014-b31a-485c-94e1-0a95ed5fc206",
  "status": "pending",
  "scheduled_at": "2026-04-20T10:00:00+00:00",
  "message": "Notification scheduled"
}
```

> ℹ️ Un seul canal est planifié par entrée. Pour plusieurs canaux, faites plusieurs appels.

---

### GET /api/v1/notifications/scheduled — Lister

Supporte : `?status=pending&page=1`

**Réponse :**
```json
{
  "data": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "channel": "email",
      "template": "auth_verify_email",
      "scheduled_at": "2026-04-20T10:00:00+00:00",
      "status": "pending",
      "created_at": "..."
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1
}
```

**Statuts possibles :** `pending`, `sent`, `cancelled`, `failed`

---

### PUT /api/v1/notifications/scheduled/{scheduled_id} — Modifier

> ⚠️ Impossible de modifier une notification avec le statut `sent` ou `cancelled`.

**Body :**
```json
{
  "scheduled_at": "2026-04-21T08:00:00Z",
  "variables": {
    "verification_url": "https://app.agt.com/verify?token=updated",
    "expires_in_minutes": "30",
    "platform_name": "Mon Application"
  }
}
```

**Réponse :**
```json
{
  "id": "uuid",
  "scheduled_at": "2026-04-21T08:00:00+00:00",
  "status": "pending",
  "message": "Notification planifiée mise à jour."
}
```

---

### DELETE /api/v1/notifications/scheduled/{scheduled_id} — Annuler

> ⚠️ Impossible d'annuler une notification déjà envoyée (`sent`).

**Réponse :** `{"message": "Scheduled notification cancelled"}`

---

## 9. Notifications In-App

Les notifications in-app sont des messages affichés directement dans l'interface de l'application. Elles sont stockées en base et consultables à tout moment.

### GET /api/v1/users/{user_id}/notifications — Lister

Supporte : `?status=unread&page=1&limit=20`

**Réponse :**
```json
{
  "data": [
    {
      "id": "uuid",
      "subject": "Vérifiez votre adresse email",
      "body": "Bonjour,\n\nCliquez sur ce lien...",
      "is_read": false,
      "created_at": "2026-04-15T08:44:22.294005+00:00"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 3,
  "unread_count": 3
}
```

> ℹ️ Le champ `unread_count` est inclus directement dans la réponse pour éviter un appel supplémentaire.

---

### GET /api/v1/users/{user_id}/notifications/unread-count — Badge

**Réponse :** `{"user_id": "uuid", "unread_count": 3}`

---

### PUT /api/v1/users/{user_id}/notifications/{notification_id}/read — Marquer lue

**Réponse :** `{"message": "Notification lue."}`

---

### PUT /api/v1/users/{user_id}/notifications/read-all — Tout marquer comme lu

**Réponse :** `{"message": "3 notifications marquees lues."}`

---

### DELETE /api/v1/users/{user_id}/notifications/{notification_id} — Supprimer

Suppression logique — n'apparaît plus dans les listes.

**Réponse :** `{"message": "Notification supprimee."}`

---

## 10. Préférences utilisateur

### GET /api/v1/users/{user_id}/notification-preferences

Supporte : `?platform_id=uuid`

**Réponse :**
```json
{
  "channels": {"email": true, "sms": true, "push": true, "whatsapp": true, "in_app": true},
  "categories": {"transactional": true, "marketing": false, "security": true}
}
```

> ℹ️ `security` est toujours `true` et ne peut pas être désactivé.

---

### PUT /api/v1/users/{user_id}/notification-preferences — Modifier

**Body :**
```json
{
  "channels": {"email": true, "sms": false, "push": true, "whatsapp": false, "in_app": true},
  "categories": {"transactional": true, "marketing": false}
}
```

**Réponse :** `{"message": "Preferences mises a jour."}`

---

## 11. Device Tokens

Un **device token** est un identifiant unique généré par Android ou iOS pour envoyer des notifications push.

### Flux d'enregistrement

```
App mobile démarre → Android/iOS génère un token unique
→ L'app envoie ce token à votre backend
→ POST /users/{user_id}/device-tokens
→ AGT stocke token + user_id
→ AGT peut envoyer des push à cet appareil
```

### POST /api/v1/users/{user_id}/device-tokens — Enregistrer

**Body :**
```json
{
  "token": "fcm_token_genere_par_android_ou_ios",
  "device_type": "android",
  "device_name": "Pixel 7",
  "platform_id": "votre-platform-id"
}
```

**Réponse 201 :** `{"id": "uuid", "device_type": "android", "created": true}`

---

### GET /api/v1/users/{user_id}/device-tokens — Lister

**Réponse :**
```json
{
  "data": [{"id": "uuid", "device_type": "android", "device_name": "Pixel 7", "created_at": "..."}]
}
```

---

### DELETE /api/v1/users/{user_id}/device-tokens/{token_id} — Supprimer

**Réponse :** `{"message": "Device token supprime."}`

---

## 12. Campagnes

Une campagne est un envoi en masse vers une liste d'utilisateurs avec un même template.

### Différence avec send-bulk

| | send-bulk | Campagne |
|---|---|---|
| Limite | 100 max | Illimité |
| Envoi | Immédiat | Throttlé |
| Annulable | Non | Oui |
| Suivi progression | Non | Oui |
| Stats détaillées | Non | Oui |

### POST /api/v1/campaigns — Créer

**Body :**
```json
{
  "name": "Newsletter Avril 2026",
  "template_name": "newsletter_avril",
  "channel": "email",
  "locale": "fr",
  "user_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "variables": {"promo_code": "AVRIL20", "platform_name": "Mon Application"},
  "throttle_per_second": 10,
  "scheduled_at": "2026-06-01T09:00:00Z"
}
```

**Réponse 201 :**
```json
{"id": "uuid", "name": "Newsletter Avril 2026", "status": "draft", "total_recipients": 3}
```

---

### GET /api/v1/campaigns — Lister

Supporte : `?status=running&page=1&limit=20`

---

### GET /api/v1/campaigns/{campaign_id} — Détail

**Réponse :**
```json
{
  "id": "uuid", "name": "Newsletter Avril 2026", "status": "completed",
  "total_recipients": 3, "sent_count": 3, "failed_count": 0, "progress": 100
}
```

---

### GET /api/v1/campaigns/{campaign_id}/progress — Progression en temps réel

**Réponse :**
```json
{
  "progress": 64.3, "sent": 3200, "failed": 15,
  "pending": 1785, "total": 5000, "status": "running"
}
```

---

### GET /api/v1/campaigns/{campaign_id}/stats — Statistiques détaillées

**Réponse :**
```json
{
  "total_recipients": 5000, "sent": 4985,
  "failed": 15, "pending": 0, "delivery_rate": 99.7
}
```

---

### POST /api/v1/campaigns/{campaign_id}/cancel — Annuler

> ⚠️ Impossible d'annuler une campagne `completed` ou `cancelled`.

**Réponse :**
```json
{"message": "Campaign cancelled", "status": "cancelled", "sent_before_cancel": 3200}
```

**Cycle de vie :**
```
draft → running → completed
              ↘ cancelled
```

---

## 13. Statistiques et Logs

### GET /api/v1/notifications/stats — Statistiques globales

Supporte : `?platform_id=uuid&period=last_30d`

**Réponse :**
```json
{
  "total_sent": 125000,
  "by_channel": {"email": 80000, "push": 30000, "sms": 5000, "in_app": 8000, "whatsapp": 2000},
  "by_status": {"sent": 120000, "failed": 3000, "pending": 2000},
  "delivery_rate": 96.0
}
```

---

### GET /api/v1/notifications/logs — Logs d'envoi

Supporte : `?channel=email&status=failed&from=2026-04-01&to=2026-04-30&page=1`

| Param | Description |
|-------|-------------|
| `channel` | Filtrer par canal |
| `status` | Filtrer par statut (`sent`, `failed`...) |
| `from` | Date début |
| `to` | Date fin |

**Réponse :**
```json
{
  "data": [
    {
      "id": "uuid", "notification_id": "uuid", "channel": "email",
      "provider": "smtp_local", "status": "sent", "attempt": 1, "created_at": "..."
    }
  ],
  "page": 1, "limit": 20, "total": 14
}
```

> ℹ️ Voir `attempt: 1 → failed` puis `attempt: 2 → failed` est **normal** — c'est le fallback entre providers.

---

## 14. Configuration des canaux

La config canaux définit l'ordre de priorité des canaux et le fallback automatique par plateforme.

### GET /api/v1/platforms/{platform_id}/channels-priority

**Réponse :**
```json
{
  "platform_id": "uuid",
  "priority_order": ["email", "push", "in_app", "whatsapp", "sms"],
  "fallback_enabled": true
}
```

---

### PUT /api/v1/platforms/{platform_id}/channels-priority — Modifier

**Body :** `{"priority_order": ["email", "in_app", "sms", "push", "whatsapp"], "fallback_enabled": true}`

**Réponse :** `{"message": "Config mise a jour."}`

---

## 15. Intégration dans un frontend

### React — Notifications In-App

```javascript
const NOTIF_API = 'http://localhost:7002/api/v1';

export async function getNotifications(userId, token) {
  const res = await fetch(`${NOTIF_API}/users/${userId}/notifications`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return res.json(); // inclut unread_count directement
}

export async function getUnreadCount(userId, token) {
  const res = await fetch(`${NOTIF_API}/users/${userId}/notifications/unread-count`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return (await res.json()).unread_count;
}

export async function markAsRead(userId, notificationId, token) {
  await fetch(`${NOTIF_API}/users/${userId}/notifications/${notificationId}/read`, {
    method: 'PUT', headers: { 'Authorization': `Bearer ${token}` }
  });
}

export async function markAllAsRead(userId, token) {
  await fetch(`${NOTIF_API}/users/${userId}/notifications/read-all`, {
    method: 'PUT', headers: { 'Authorization': `Bearer ${token}` }
  });
}

export async function registerDeviceToken(userId, fcmToken, deviceType, token) {
  const res = await fetch(`${NOTIF_API}/users/${userId}/device-tokens`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: fcmToken, device_type: deviceType, device_name: navigator.userAgent })
  });
  return res.json();
}

export async function scheduleNotification(userId, templateName, variables, scheduledAt, token) {
  const res = await fetch(`${NOTIF_API}/notifications/schedule`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId, channels: ['email'],
      template_name: templateName, variables, scheduled_at: scheduledAt
    })
  });
  return res.json();
}

// Polling badge toutes les 30 secondes
function startNotificationPolling(userId, token, onUpdate) {
  const interval = setInterval(async () => {
    const count = await getUnreadCount(userId, token);
    onUpdate(count);
  }, 30000);
  return () => clearInterval(interval);
}
```

### Node.js — Envoi depuis votre backend

```javascript
async function sendNotification(userId, templateName, variables, s2sToken) {
  const res = await fetch('http://agt-notif-service:7002/api/v1/notifications/send', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${s2sToken}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId, channels: ['email', 'in_app'],
      template_name: templateName, variables,
      category: 'transactional', priority: 'normal'
    })
  });
  return res.json();
}
```

---

## 16. Troubleshooting

### Le service ne démarre pas

```bash
docker logs agt-notif-service --tail 50
```

Causes fréquentes : DB non disponible, variables `.env` manquantes, migrations non appliquées.

---

### Les emails n'arrivent pas dans Mailpit

```bash
docker logs agt-notif-worker --tail 30
```

Vérifier dans `.env` : `EMAIL_HOST=agt-mailpit` et `EMAIL_PORT=1025`

Vérifier que le profil Users existe pour le destinataire :
```bash
docker exec -it agt-auth-service python manage.py shell -c "
from apps.authentication.services import UsersServiceClient
UsersServiceClient.provision_user(auth_user_id='uuid-du-user', email='email@test.com')
"
```

---

### Erreur "Connection refused" vers RabbitMQ

Après un rebuild, le worker peut perdre la connexion. Solution :

```bash
docker restart agt-notif-service agt-notif-worker
```

---

### Erreur "Template introuvable" (404)

Causes : template inexistant, `platform_id` ne correspond pas, template désactivé.

Solution : créez les templates sans `platform_id` pour qu'ils soient globaux.

---

### Erreur "S2S credentials manquants"

Configurez dans `agt-notification/.env` :
```env
S2S_AUTH_URL=http://agt-auth-service:7000/api/v1
S2S_CLIENT_ID=votre-client-id
S2S_CLIENT_SECRET=votre-client-secret
```
Puis : `docker restart agt-notif-worker`

---

### Erreur 429 Too Many Requests

```bash
docker exec -it agt-auth-redis redis-cli FLUSHDB
```

---

### Les variables ne sont pas substituées

Vérifiez que le champ s'appelle `"variables"` (pas `"data"`) et que c'est un objet JSON.

Test rapide :
```bash
docker exec -it agt-notif-service python manage.py shell -c "
from apps.templates_mgr.models import Template
t = Template.objects.get(name='auth_verify_email')
print(t.render({'verification_url': 'https://test.com', 'expires_in_minutes': '60', 'platform_name': 'Test'}))
"
```

---

### Commandes utiles

```bash
# Logs en direct
docker logs -f agt-notif-service
docker logs -f agt-notif-worker

# Restart (après modif code ou .env)
docker restart agt-notif-service agt-notif-worker

# Rebuild complet (Dockerfile ou requirements.txt modifiés)
docker compose -f agt-notification/docker-compose.yml up -d --build
docker compose -f agt-auth/docker-compose.yml up -d --build
docker compose -f agt-users/docker-compose.yml up -d --build

# Shell Django
docker exec -it agt-notif-service python manage.py shell

# Tests
docker exec -it agt-notif-service python -m pytest -v

# Interfaces
# RabbitMQ : http://localhost:15672 (agt_rabbit / agt_rabbit_password)
# Mailpit   : http://localhost:8025
```

---

*AG Technologies — Notification Service Guide v1.2 — Confidentiel*