# AGT — Guide Complet du Service Notification v1.0

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
8. [Notifications In-App](#8-notifications-in-app)
9. [Préférences utilisateur](#9-préférences-utilisateur)
10. [Device Tokens — Notifications Push](#10-device-tokens)
11. [Campagnes — Envoi en masse](#11-campagnes)
12. [Statistiques et Logs](#12-statistiques-et-logs)
13. [Configuration des canaux par plateforme](#13-configuration-des-canaux)
14. [Intégration dans un frontend](#14-intégration-dans-un-frontend)
15. [Troubleshooting](#15-troubleshooting)

---

## 1. Rôle du service

Le service Notification est le **hub de communication** de l'écosystème AGT. Il est responsable de l'envoi de tous les messages vers les utilisateurs, quel que soit le canal.

### Ce qu'il fait

- Envoie des **emails** (via SMTP local Mailpit en dev, SendGrid en prod)
- Envoie des **SMS** (via Twilio en prod, Console en dev)
- Envoie des **notifications push** (via FCM pour Android/Web)
- Gère les **notifications in-app** (messages dans l'interface de l'application)
- Gère des **campagnes** d'envoi en masse
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

Ouvrez dans votre navigateur :
```
http://localhost:7002/api/v1/docs/
```

---

## 4. Configuration initiale obligatoire

Avant de pouvoir utiliser le service, vous devez effectuer ces étapes dans l'ordre.

### Étape préalable — Migrations (premier lancement uniquement)

Lors du premier lancement, les bases de données sont vides.
Vous devez générer et appliquer les schémas avant toute utilisation.

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

> ⚠️ Ces commandes sont à exécuter **une seule fois** lors du premier
> lancement ou après un reset complet de la base de données.
> Si les tables existent déjà, Django ignorera les migrations déjà appliquées.
### Étape 1 — Créer une plateforme S2S dans Auth

> ℹ️ Une plateforme S2S est l'identité machine de votre service ou application dans l'écosystème AGT. Elle lui permet de s'authentifier de service à service.

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

### Étape 3 — S'authentifier dans Swagger Notification

1. Ouvrez `http://localhost:7002/api/v1/docs/`
2. Cliquez sur le bouton **Authorize** (icône cadenas en haut à droite)
3. Dans le champ **BearerAuth**, entrez votre token S2S :
   ```
   eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
4. Cliquez **Authorize** puis **Close**

> ✅ Toutes les routes protégées sont maintenant accessibles.

### Étape 4 — Configurer le .env du service Notification (pour les services AGT)

> ℹ️ Cette étape concerne uniquement les développeurs qui intègrent Notification comme service appelant d'autres services AGT.

Dans `agt-notification/.env`, ajoutez les credentials S2S du service Notification :

```env
S2S_AUTH_URL=http://agt-auth-service:7000/api/v1
S2S_CLIENT_ID=votre-client-id-du-service-notification
S2S_CLIENT_SECRET=votre-client-secret-du-service-notification
```

> ℹ️ Ces credentials permettent au service Notification d'appeler Users Service pour récupérer l'email/téléphone d'un utilisateur avant d'envoyer une notification.

### Étape 5 — Créer les templates système (obligatoire pour Auth)

> ℹ️ Les templates système sont des templates **sans `platform_id`** (globaux). Ils sont utilisés par Auth Service pour envoyer les emails de vérification, réinitialisation de mot de passe, etc.

Dans Swagger Notification, créez ces 4 templates via `POST /api/v1/templates` :

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

> ⚠️ **Important :** Ne pas inclure le champ `platform_id` dans ces templates — ils doivent être globaux (valables pour toutes les plateformes).

---

## 5. Comprendre l'authentification

### Deux types d'appelants

| Type | Qui | Comment |
|------|-----|---------|
| **Plateforme applicative** | Une app mobile, un site web, un dashboard | Token S2S avec `platform_id` = UUID de la plateforme |
| **Service AGT** | Auth, Users, Payment... | Token S2S avec `platform_id` = UUID du service |

### Comment le service résout les templates

Quand une notification est envoyée, Notification extrait le `platform_id` du token JWT et cherche le template dans cet ordre :

1. Template avec ce `platform_id` exact → priorité maximale
2. Template global (`platform_id = null`) → fallback universel

> ℹ️ C'est pourquoi les templates système d'Auth sont créés sans `platform_id` — ils doivent fonctionner quelle que soit la plateforme qui appelle.

---

## 6. Templates

Un template est un **modèle de message réutilisable** avec des variables dynamiques. Il utilise le moteur **Jinja2** avec la syntaxe `{{nom_variable}}`.

### GET /api/v1/templates — Lister les templates

**Header :** `Authorization: Bearer <token>`

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

### POST /api/v1/templates — Créer un template

**Header :** `Authorization: Bearer <token>`

**Body :**
```json
{
  "name": "bienvenue_client",
  "channel": "email",
  "subject": "Bienvenue {{prenom}} !",
  "body": "Bonjour {{prenom}},\n\nBienvenue sur {{platform_name}} !\n\nVotre compte est actif.",
  "category": "transactional",
  "platform_id": "votre-platform-id",
  "locale": "fr"
}
```

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `name` | string | ✅ | Identifiant unique du template (par plateforme) |
| `channel` | string | ✅ | `email`, `sms`, `push`, `whatsapp`, `in_app` |
| `body` | string | ✅ | Corps du message avec variables `{{variable}}` |
| `subject` | string | ❌ | Sujet (email uniquement) |
| `category` | string | ❌ | `transactional` (défaut) ou `marketing` |
| `platform_id` | UUID | ❌ | Laisser vide pour un template global |
| `locale` | string | ❌ | Langue (`fr` par défaut) |

**Réponse :**
```json
{
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "name": "bienvenue_client",
  "channel": "email"
}
```

---

### GET /api/v1/templates/{template_id} — Détail d'un template

**Réponse :**
```json
{
  "id": "b18b48c3-a02f-477d-8ae0-e461e8a247d9",
  "name": "auth_verify_email",
  "channel": "email",
  "subject": "Vérifiez votre adresse email",
  "body": "Bonjour,\n\nCliquez sur ce lien : {{verification_url}}\n\nExpire dans {{expires_in_minutes}} minutes."
}
```

---

### PUT /api/v1/templates/{template_id} — Modifier un template

Chaque modification crée une **nouvelle version** tout en conservant l'historique.

**Body :**
```json
{
  "subject": "Nouveau sujet",
  "body": "Nouveau corps avec {{variable}}",
  "locale": "fr"
}
```

**Réponse :**
```json
{
  "message": "Template mis a jour.",
  "version": 2
}
```

> ℹ️ Le système de versioning permet de revenir à une version précédente et de suivre l'évolution des templates.

---

### POST /api/v1/templates/{template_id}/preview — Prévisualiser un template

Permet de tester le rendu d'un template avec des variables de test, sans envoyer de notification réelle.

> ⚠️ **Note Swagger :** Cette route ne montre pas de champ body dans Swagger UI. Utilisez curl ou Postman.

**Curl :**
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
  "body": "Bonjour,\n\nCliquez sur ce lien pour vérifier votre email : https://app.agt.com/verify?token=test123\n\nCe lien expire dans 60 minutes.\n\nMon Application"
}
```

---

### GET /api/v1/templates/{template_id}/versions — Historique des versions

**Réponse :**
```json
{
  "data": [
    {
      "version": 2,
      "locale": "fr",
      "is_current": true,
      "created_at": "2026-04-15T08:25:07.397890+00:00"
    },
    {
      "version": 1,
      "locale": "fr",
      "is_current": false,
      "created_at": "2026-04-14T17:55:20.598281+00:00"
    }
  ]
}
```

---

### DELETE /api/v1/templates/{template_id} — Désactiver un template

> ℹ️ La suppression est **logique** — le template est marqué `is_active = false` mais reste en base pour conserver l'historique. Il ne sera plus utilisable pour les nouveaux envois.

**Réponse :**
```json
{
  "message": "Template desactive."
}
```

---

## 7. Envoi de notifications

### POST /api/v1/notifications/send — Envoi unitaire

Envoie une notification à **un seul utilisateur** sur un ou plusieurs canaux.

**Header :** `Authorization: Bearer <token>`

**Body :**
```json
{
  "user_id": "uuid-de-l-utilisateur",
  "channels": ["email"],
  "template_name": "auth_verify_email",
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

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `user_id` | UUID | ✅ | ID Auth de l'utilisateur destinataire |
| `channels` | array | ✅ | Liste des canaux : `email`, `sms`, `push`, `whatsapp`, `in_app` |
| `template_name` | string | ✅ | Nom du template à utiliser |
| `variables` | object | ❌ | Variables à injecter dans le template |
| `category` | string | ❌ | `transactional` (défaut) ou `marketing` ou `security` |
| `priority` | string | ❌ | `low`, `normal` (défaut), `high`, `critical` |
| `idempotency_key` | string | ❌ | Clé unique pour éviter les doublons |

**Réponse :**
```json
{
  "notifications": [
    {
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "channel": "email",
      "status": "pending"
    }
  ],
  "message": "Notifications queued"
}
```

> ℹ️ Le statut `pending` indique que la notification est en file d'attente. Le worker Celery la traitera de manière asynchrone.

**Ce qui se passe sous le capot :**
```
POST /notifications/send
        ↓
  Validation du body
        ↓
  Résolution du template (par nom + platform_id)
        ↓
  Rendu Jinja2 (injection des variables)
        ↓
  Création en base (status: pending)
        ↓
  Envoi dans RabbitMQ
        ↓
  Worker Celery consomme la tâche
        ↓
  Appel Users Service pour récupérer email/téléphone
        ↓
  Envoi via le provider (SMTP/SendGrid/Twilio...)
        ↓
  Mise à jour status (sent/failed)
```

---

### POST /api/v1/notifications/send-bulk — Envoi en masse (max 100)

Envoie le même message à **plusieurs utilisateurs** en une seule requête.

> ℹ️ Pour plus de 100 utilisateurs, utilisez les **Campagnes** (voir section 11).

**Body :**
```json
{
  "user_ids": [
    "uuid-user-1",
    "uuid-user-2",
    "uuid-user-3"
  ],
  "channels": ["email"],
  "template_name": "auth_verify_email",
  "variables": {
    "verification_url": "https://app.agt.com/verify?token=bulk123",
    "expires_in_minutes": "60",
    "platform_name": "Mon Application"
  },
  "category": "transactional"
}
```

**Réponse :**
```json
{
  "message": "3 notifications queued",
  "total": 3
}
```

---

## 8. Notifications In-App

Les notifications in-app sont des messages affichés **directement dans l'interface** de l'application (comme les notifications d'une app mobile ou d'un dashboard web). Elles sont stockées en base et consultables à tout moment.

### GET /api/v1/users/{user_id}/notifications — Lister les notifications

**Réponse :**
```json
{
  "data": [
    {
      "id": "9a8143ad-5d40-44b3-a814-05f2f34f54cf",
      "subject": "Vérifiez votre adresse email",
      "body": "Bonjour,\n\nCliquez sur ce lien...",
      "is_read": false,
      "created_at": "2026-04-15T08:44:22.294005+00:00"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1
}
```

---

### GET /api/v1/users/{user_id}/notifications/unread-count — Compteur non lues

Utilisé pour afficher le **badge** de notifications non lues dans votre interface.

**Réponse :**
```json
{
  "user_id": "uuid-user",
  "unread_count": 3
}
```

---

### PUT /api/v1/users/{user_id}/notifications/{notification_id}/read — Marquer comme lue

Appelé quand l'utilisateur clique sur une notification.

**Réponse :**
```json
{
  "message": "Notification lue."
}
```

---

### PUT /api/v1/users/{user_id}/notifications/read-all — Tout marquer comme lu

Appelé quand l'utilisateur clique sur "Tout marquer comme lu".

**Réponse :**
```json
{
  "message": "3 notifications marquees lues."
}
```

---

### DELETE /api/v1/users/{user_id}/notifications/{notification_id} — Supprimer

**Réponse :**
```json
{
  "message": "Notification supprimee."
}
```

---

## 9. Préférences utilisateur

Les préférences permettent à chaque utilisateur de choisir **quels canaux** et **quelles catégories** de notifications il souhaite recevoir.

> ℹ️ Si aucune préférence n'est définie pour un utilisateur, le système utilise les valeurs par défaut (tout activé sauf marketing).

### GET /api/v1/users/{user_id}/notification-preferences

**Réponse :**
```json
{
  "channels": {
    "email": true,
    "sms": true,
    "push": true,
    "whatsapp": true,
    "in_app": true
  },
  "categories": {
    "transactional": true,
    "marketing": false,
    "security": true
  }
}
```

> ℹ️ La catégorie `security` est toujours `true` et ne peut pas être désactivée — les notifications de sécurité (2FA, alertes de connexion) sont toujours envoyées.

---

### PUT /api/v1/users/{user_id}/notification-preferences — Modifier

**Body :**
```json
{
  "channels": {
    "email": true,
    "sms": false,
    "push": true,
    "whatsapp": false,
    "in_app": true
  },
  "categories": {
    "transactional": true,
    "marketing": false
  }
}
```

**Réponse :**
```json
{
  "message": "Preferences mises a jour."
}
```

---

## 10. Device Tokens

Un **device token** est un identifiant unique généré automatiquement par Android ou iOS pour chaque appareil. Il est nécessaire pour envoyer des **notifications push** sur les téléphones des utilisateurs.

### Flux d'enregistrement

```
App mobile démarre
      ↓
Android/iOS génère un token unique
      ↓
L'app envoie ce token à votre backend
      ↓
Votre backend appelle POST /users/{user_id}/device-tokens
      ↓
AGT stocke token + user_id
      ↓
AGT peut maintenant envoyer des push à cet appareil
```

### POST /api/v1/users/{user_id}/device-tokens — Enregistrer

**Body :**
```json
{
  "token": "fcm_token_genere_par_android_ou_ios",
  "device_type": "android",
  "device_name": "Pixel 7"
}
```

| Champ | Valeurs | Description |
|-------|---------|-------------|
| `device_type` | `android`, `ios`, `web` | Type d'appareil |
| `device_name` | string | Nom lisible de l'appareil (optionnel) |

**Réponse :**
```json
{
  "id": "5b03b5e2-5682-42a3-9f88-22298fb1fa3e",
  "device_type": "android",
  "created": true
}
```

---

### GET /api/v1/users/{user_id}/device-tokens — Lister

**Réponse :**
```json
{
  "data": [
    {
      "id": "5b03b5e2-5682-42a3-9f88-22298fb1fa3e",
      "device_type": "android",
      "device_name": "Pixel 7",
      "created_at": "2026-04-15T08:55:14.779587+00:00"
    }
  ]
}
```

---

### DELETE /api/v1/users/{user_id}/device-tokens/{token_id} — Supprimer

Appelé quand l'utilisateur se déconnecte ou désinstalle l'app.

**Réponse :**
```json
{
  "message": "Device token supprime."
}
```

---

## 11. Campagnes

Une campagne est un **envoi en masse programmé** vers une liste d'utilisateurs avec un même template. Elle est conçue pour les newsletters, promotions, et annonces produit.

### Différence avec send-bulk

| | send-bulk | Campagne |
|---|---|---|
| Limite utilisateurs | 100 max | Illimité |
| Envoi | Immédiat | Throttlé (ex: 10/sec) |
| Annulable | Non | Oui |
| Suivi progression | Non | Oui |
| Usage | Notifications système | Marketing, newsletters |

### POST /api/v1/campaigns — Créer une campagne

**Body :**
```json
{
  "name": "Newsletter Avril 2026",
  "template_name": "newsletter_avril",
  "channel": "email",
  "user_ids": [
    "uuid-user-1",
    "uuid-user-2",
    "uuid-user-3"
  ],
  "variables": {
    "promo_code": "AVRIL20",
    "platform_name": "Mon Application"
  },
  "throttle_per_second": 10
}
```

| Champ | Description |
|-------|-------------|
| `throttle_per_second` | Nombre d'envois par seconde (évite la surcharge) |
| `variables` | Variables communes à tous les destinataires |

**Réponse :**
```json
{
  "id": "b74a1016-9ae0-4a9c-a5eb-ed9f71e669a8",
  "name": "Newsletter Avril 2026",
  "status": "draft",
  "total_recipients": 3
}
```

> ℹ️ La campagne démarre automatiquement en arrière-plan après création.

---

### GET /api/v1/campaigns — Lister les campagnes

Supporte le filtre par statut : `?status=completed`

**Réponse :**
```json
{
  "data": [
    {
      "id": "b74a1016-9ae0-4a9c-a5eb-ed9f71e669a8",
      "name": "Newsletter Avril 2026",
      "status": "completed",
      "sent_count": 3,
      "total_recipients": 3
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1
}
```

---

### GET /api/v1/campaigns/{campaign_id} — Détail

**Réponse :**
```json
{
  "id": "b74a1016-9ae0-4a9c-a5eb-ed9f71e669a8",
  "name": "Newsletter Avril 2026",
  "status": "completed",
  "total_recipients": 3,
  "sent_count": 3,
  "failed_count": 0,
  "progress": 100
}
```

---

### GET /api/v1/campaigns/{campaign_id}/progress — Progression en temps réel

Idéal pour afficher une barre de progression dans votre interface pendant l'envoi.

**Réponse :**
```json
{
  "progress": 75,
  "sent": 75,
  "failed": 2,
  "total": 100,
  "status": "running"
}
```

---

### POST /api/v1/campaigns/{campaign_id}/cancel — Annuler

> ⚠️ Impossible d'annuler une campagne avec le statut `completed` ou `cancelled`.

**Réponse :**
```json
{
  "message": "Campagne annulee.",
  "status": "cancelled"
}
```

**Cycle de vie d'une campagne :**
```
draft → running → completed
              ↘ cancelled
```

---

## 12. Statistiques et Logs

### GET /api/v1/notifications/stats — Statistiques globales

**Réponse :**
```json
{
  "by_status": {
    "sent": 9,
    "read": 2,
    "failed": 4
  },
  "by_channel": {
    "email": 10,
    "in_app": 5
  }
}
```

---

### GET /api/v1/notifications/logs — Logs d'envoi détaillés

Chaque tentative d'envoi génère un log avec le provider utilisé, le statut et le numéro de tentative.

**Réponse :**
```json
{
  "data": [
    {
      "id": "uuid",
      "notification_id": "uuid",
      "channel": "email",
      "provider": "smtp_local",
      "status": "sent",
      "attempt": 1,
      "created_at": "2026-04-15T08:22:04.395380+00:00"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 14
}
```

> ℹ️ Si `attempt: 2` avec le provider `sendgrid` après un `attempt: 1` échoué avec `smtp_local`, cela indique que le mécanisme de **fallback** entre providers a fonctionné.

---

## 13. Configuration des canaux

La config canaux définit pour chaque plateforme **l'ordre de priorité** des canaux et si le **fallback automatique** est activé.

### Qu'est-ce que le fallback ?

Si un canal échoue (ex: email bounce), le système essaie automatiquement le canal suivant dans l'ordre de priorité.

**Exemple :**
```
Ordre: email → in_app → sms → push → whatsapp
```
Si l'email échoue → essaie in_app. Si in_app échoue → essaie sms, etc.

### GET /api/v1/platforms/{platform_id}/channels-priority

**Réponse :**
```json
{
  "platform_id": "uuid",
  "priority_order": ["email", "in_app", "sms", "push", "whatsapp"],
  "fallback_enabled": true
}
```

---

### PUT /api/v1/platforms/{platform_id}/channels-priority — Modifier

**Body :**
```json
{
  "priority_order": ["email", "push", "in_app", "sms", "whatsapp"],
  "fallback_enabled": true
}
```

**Réponse :**
```json
{
  "message": "Config mise a jour."
}
```

---

## 14. Intégration dans un frontend

### Exemple d'intégration React — Notifications In-App

```javascript
// notificationService.js
const NOTIF_API = 'http://localhost:7002/api/v1';

// Récupérer les notifications d'un utilisateur
export async function getNotifications(userId, token) {
  const response = await fetch(`${NOTIF_API}/users/${userId}/notifications`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
}

// Récupérer le compteur de notifications non lues (pour le badge)
export async function getUnreadCount(userId, token) {
  const response = await fetch(`${NOTIF_API}/users/${userId}/notifications/unread-count`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const data = await response.json();
  return data.unread_count;
}

// Marquer une notification comme lue
export async function markAsRead(userId, notificationId, token) {
  await fetch(`${NOTIF_API}/users/${userId}/notifications/${notificationId}/read`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${token}` }
  });
}

// Tout marquer comme lu
export async function markAllAsRead(userId, token) {
  await fetch(`${NOTIF_API}/users/${userId}/notifications/read-all`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${token}` }
  });
}

// Enregistrer un device token pour les push notifications
export async function registerDeviceToken(userId, fcmToken, deviceType, token) {
  const response = await fetch(`${NOTIF_API}/users/${userId}/device-tokens`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      token: fcmToken,
      device_type: deviceType,
      device_name: navigator.userAgent
    })
  });
  return response.json();
}
```

### Exemple d'envoi depuis votre backend (Node.js)

```javascript
// Envoyer une notification depuis votre backend
async function sendNotification(userId, templateName, variables, s2sToken) {
  const response = await fetch('http://agt-notif-service:7002/api/v1/notifications/send', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${s2sToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      channels: ['email', 'in_app'],
      template_name: templateName,
      variables: variables,
      category: 'transactional',
      priority: 'normal'
    })
  });
  return response.json();
}
```

### Polling du compteur de notifications non lues

```javascript
// Actualiser le badge toutes les 30 secondes
function startNotificationPolling(userId, token, onUpdate) {
  const interval = setInterval(async () => {
    const count = await getUnreadCount(userId, token);
    onUpdate(count);
  }, 30000);
  return () => clearInterval(interval); // Cleanup
}
```

---

## 15. Troubleshooting

### Le service ne démarre pas

```bash
docker logs agt-notif-service --tail 50
```

**Causes fréquentes :**
- Base de données non disponible → vérifier `agt-notif-db`
- Variables d'environnement manquantes → vérifier `.env`

---

### Les emails n'arrivent pas dans Mailpit

**Étape 1 — Vérifier les logs du worker :**
```bash
docker logs agt-notif-worker --tail 30
```

**Étape 2 — Vérifier la config SMTP dans `.env` :**
```env
EMAIL_HOST=agt-mailpit
EMAIL_PORT=1025
```

**Étape 3 — Vérifier que Mailpit est accessible :**
```
http://localhost:8025
```

---

### Erreur "Template introuvable" (404)

**Causes possibles :**
1. Le template n'existe pas avec ce nom
2. Le `platform_id` dans votre token ne correspond pas au `platform_id` du template
3. Le template a été désactivé (`DELETE`)

**Solution :** Créez les templates sans `platform_id` (globaux) pour qu'ils soient accessibles depuis n'importe quelle plateforme.

---

### Erreur "S2S credentials manquants"

Le service Notification ne peut pas appeler Users Service pour récupérer l'email/téléphone du destinataire.

**Solution :** Configurez les credentials S2S dans `agt-notification/.env` :
```env
S2S_AUTH_URL=http://agt-auth-service:7000/api/v1
S2S_CLIENT_ID=votre-client-id
S2S_CLIENT_SECRET=votre-client-secret
```

Puis redémarrez :
```bash
docker restart agt-notif-worker
```

---

### Erreur 429 Too Many Requests

Le rate limiting Redis est déclenché. En développement :

```bash
docker exec -it agt-auth-redis redis-cli FLUSHDB
```

---

### Les variables ne sont pas substituées dans le message

**Vérifiez que :**
1. Les noms des variables dans votre body correspondent exactement à ceux du template
2. Le champ dans votre requête s'appelle bien `"variables"` (et non `"data"`)
3. Les variables sont un objet JSON (et non une chaîne de caractères)

**Test rapide en shell :**
```bash
docker exec -it agt-notif-service python manage.py shell -c "
from apps.templates_mgr.models import Template
t = Template.objects.get(name='auth_verify_email')
result = t.render({'verification_url': 'https://test.com', 'expires_in_minutes': '60', 'platform_name': 'Test'})
print(result)
"
```

---

### Commandes utiles

```bash
# Voir les logs en direct
docker logs -f agt-notif-service
docker logs -f agt-notif-worker

# Redémarrer le service
docker restart agt-notif-service
docker restart agt-notif-worker

#rebuild les services
docker compose -f agt-auth/docker-compose.yml up -d --build
docker compose -f agt-notification/docker-compose.yml up -d --build
docker compose -f agt-users/docker-compose.yml up -d --build

# Accéder au shell Django
docker exec -it agt-notif-service python manage.py shell

# Lancer les tests
docker exec -it agt-notif-service python -m pytest -v

# Vérifier RabbitMQ
http://localhost:15672 (agt_rabbit / agt_rabbit_password)

# Vérifier Mailpit
http://localhost:8025
```

---

*AG Technologies — Notification Service Guide v1.0 — Confidentiel*