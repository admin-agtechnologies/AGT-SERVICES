# Getting Started — AG Technologies Microservices

> **À qui s'adresse ce guide ?**
> À tout développeur qui rejoint le projet AGT et souhaite comprendre, lancer et utiliser l'écosystème microservices pour la première fois.
>
> **Ce guide couvre le MVP** : les trois services socles (Auth, Users, Notification) suffisants pour valider le flux d'inscription complet.

---

## Table des matières

1. [Vue d'ensemble de l'architecture](#1-vue-densemble-de-larchitecture)
2. [Prérequis](#2-prérequis)
3. [Les scripts de déploiement](#3-les-scripts-de-déploiement)
4. [Lancer le MVP](#4-lancer-le-mvp)
5. [Vérifier l'état des services](#5-vérifier-létat-des-services)
6. [Configurer l'environnement](#6-configurer-lenvironnement)
7. [Créer les plateformes S2S des microservices](#7-créer-les-plateformes-s2s-des-microservices)
8. [Créer une plateforme applicative de test](#8-créer-une-plateforme-applicative-de-test)
9. [Créer les templates de notification](#9-créer-les-templates-de-notification)
10. [Inscrire un premier utilisateur](#10-inscrire-un-premier-utilisateur)
11. [Vérifier l'email dans Mailpit](#11-vérifier-lemail-dans-mailpit)
12. [Ce qui se passe sous le capot](#12-ce-qui-se-passe-sous-le-capot)
13. [Redémarrer un service](#13-redémarrer-un-service)
14. [Consulter les logs](#14-consulter-les-logs)
15. [Aller plus loin — les autres flux](#15-aller-plus-loin--les-autres-flux)

---

## 1. Vue d'ensemble de l'architecture

AGT est une architecture **microservices découplée**. Chaque service est autonome, responsable d'un seul périmètre métier, et dispose de sa propre base de données. Les services communiquent entre eux de deux façons :

- **REST (synchrone)** : pour les lectures rapides, validations et actions critiques.
- **RabbitMQ (asynchrone)** : pour les opérations comme l'envoi de notifications, les paiements ou les mises à jour de wallet.

Voici les services de l'écosystème complet :

| Service | Port | Rôle |
|---|---|---|
| **Auth** | 7000 | Identité, JWT, sessions, OAuth 2.0, 2FA, tokens S2S |
| **Users** | 7001 | Profils utilisateurs, rôles, permissions, documents |
| **Notification** | 7002 | Envoi multi-canal : email, SMS, push, in-app, WhatsApp |
| **Media** | 7003 | Upload, traitement, stockage, thumbnails |
| **Subscription** | 7004 | Plans, quotas, cycles de facturation |
| **Payment** | 7005 | Transactions via Orange Money, MTN MoMo, Stripe, PayPal |
| **Wallet** | 7006 | Ledger double-entry, virements, cash-in/out |
| **Search** | 7007 | Indexation et recherche full-text (Elasticsearch) |
| **Chat** | 7008 | Messagerie temps réel, présence |
| **Geoloc** | 7009 | Tracking GPS, geofencing |
| **Chatbot** | 7010 | Orchestrateur IA, flows, knowledge base, RAG |

**Le MVP** regroupe les trois premiers services (Auth + Users + Notification) et l'infrastructure partagée (RabbitMQ, Mailpit, Elasticsearch, Gateway Nginx).

---

## 2. Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Docker Desktop** (ou Docker Engine + Docker Compose) — version 24+
- **Git**
- **PowerShell** (Windows) ou **Bash** (Linux/Mac)

Vérifiez que Docker est actif :

```powershell
docker --version
docker compose version
```

Clonez le dépôt si ce n'est pas encore fait :

```bash
git clone <URL_DU_REPO>
cd AGT-SERVICES
```

---

## 3. Les scripts de déploiement

À la racine du projet, vous trouverez plusieurs scripts. Voici leur rôle :

| Script | Rôle |
|---|---|
| `deploy_mvp.ps1` / `deploy_mvp.sh` | Lance uniquement le MVP (Auth + Users + Notification + infra) |
| `deploy_all.ps1` / `deploy_all.sh` | Lance tous les services de l'écosystème |
| `reset_mvp.ps1` / `reset_mvp.sh` | Arrête et nettoie les containers du MVP (garde les données) |
| `reset_mvp.ps1 --clean` | Arrête, nettoie **et supprime les volumes** (repart de zéro) |
| `reset_all.ps1` / `reset_all.sh` | Idem pour tous les services |

> **Règle importante :** utilisez toujours `--clean` si vous souhaitez repartir d'une base vide (ex : après avoir modifié les migrations ou corrompu une DB).

---

## 4. Lancer le MVP

Lancez le MVP avec la commande suivante depuis la racine du projet :

```powershell
# Windows
.\deploy_mvp.ps1

# Linux / Mac
./deploy_mvp.sh
```

Le script effectue automatiquement dans l'ordre :

1. Création du réseau Docker `agt_network` s'il n'existe pas
2. Démarrage de l'infrastructure partagée (Gateway, RabbitMQ, Mailpit, Elasticsearch)
3. Copie du `.env.example` vers `.env` pour chaque service si absent
4. Build et démarrage du service Auth
5. Distribution de la clé publique RSA d'Auth vers Users et Notification
6. Build et démarrage de Users et Notification
7. Exécution des migrations de base de données
8. Health checks pour confirmer que tout est up

En fin de script, vous devriez voir :

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

---

## 5. Vérifier l'état des services

### Via Docker

```powershell
docker ps
```

Vous devriez voir tous les containers avec le statut `(healthy)` :

```
agt-auth-service     Up ... (healthy)   0.0.0.0:7000->7000/tcp
agt-users-service    Up ... (healthy)   0.0.0.0:7001->7001/tcp
agt-notif-service    Up ... (healthy)   0.0.0.0:7002->7002/tcp
agt-notif-worker     Up ...             7002/tcp
agt-notif-beat       Up ...             7002/tcp
agt-rabbitmq         Up ... (healthy)   0.0.0.0:5672->5672/tcp
agt-mailpit          Up ... (healthy)   0.0.0.0:8025->8025/tcp
```

### Via les endpoints de santé

Chaque service expose un endpoint `/health` :

```powershell
# Auth
curl http://localhost:7000/api/v1/health

# Users
curl http://localhost:7001/api/v1/health

# Notification
curl http://localhost:7002/api/v1/health
```

Réponse attendue :

```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```

### Via Swagger (interface graphique)

Chaque service dispose d'une documentation API interactive :

- Auth : http://localhost:7000/api/v1/docs/
- Users : http://localhost:7001/api/v1/docs/
- Notification : http://localhost:7002/api/v1/docs/

---

## 6. Configurer l'environnement

Les fichiers `.env` sont générés automatiquement par les scripts de déploiement à partir des `.env.example`. Vous n'avez normalement rien à faire manuellement pour le MVP en local.

Si vous devez le faire manuellement :

```powershell
# Auth
Copy-Item agt-auth\.env.example agt-auth\.env

# Users
Copy-Item agt-users\.env.example agt-users\.env

# Notification
Copy-Item agt-notification\.env.example agt-notification\.env
```

> **Note :** les `.env` ne sont jamais commités en Git. Seuls les `.env.example` le sont. Ne mettez jamais de secrets dans un `.env.example`.

### Migrations

Les migrations sont exécutées automatiquement au démarrage. Si vous devez les relancer manuellement :

```powershell
# Auth
docker exec agt-auth-service python manage.py makemigrations authentication platforms
docker exec agt-auth-service python manage.py migrate

# Users
docker exec agt-users-service python manage.py makemigrations users roles documents
docker exec agt-users-service python manage.py migrate

# Notification
docker exec agt-notif-service python manage.py makemigrations notifications templates_mgr campaigns devices
docker exec agt-notif-service python manage.py migrate
```

---

## 7. Créer les plateformes S2S des microservices

> **Pourquoi cette étape ?**
>
> Dans AGT, Auth est le seul émetteur de tokens JWT. Tout service qui doit appeler un autre service doit posséder une **plateforme S2S** dans Auth. Cette plateforme lui permet d'obtenir un token JWT pour s'authentifier lors de ses appels inter-services.
>
> **Règle fondamentale :** les plateformes S2S des microservices doivent être créées **avant** les plateformes applicatives.

### 7.1 Créer la plateforme S2S de Notification

Dans Swagger Auth (http://localhost:7000/api/v1/docs/), appelez `POST /api/v1/auth/platforms` avec le header :

```
X-Admin-API-Key: change-me-admin-api-key-very-secret
```

Body :

```json
{
  "name": "AGT Notification",
  "slug": "agt-notification",
  "allowed_auth_methods": ["email"]
}
```

Notez le `id` (qui sera votre `client_id`) et le `client_secret` retournés.

### 7.2 Configurer le `.env` de Notification

Ajoutez ces variables dans `agt-notification/.env` :

```env
S2S_AUTH_URL=http://agt-auth-service:7000/api/v1
S2S_CLIENT_ID=<id_retourné>
S2S_CLIENT_SECRET=<client_secret_retourné>
```

### 7.3 Redémarrer Notification

```powershell
cd agt-notification
docker compose up -d --build notification celery-worker
cd ..
```

> **Répétez cette procédure** pour chaque nouveau microservice qui a besoin d'appeler d'autres services (Subscription, Payment, Wallet, etc.).

---

## 8. Créer une plateforme applicative de test

Une plateforme applicative représente une application cliente qui utilise l'écosystème AGT (ex : une app mobile, un site web, un backoffice). Pour ce guide, nous créons une plateforme générique de test.

Dans Swagger Auth, appelez `POST /api/v1/auth/platforms` :

```
X-Admin-API-Key: change-me-admin-api-key-very-secret
```

```json
{
  "name": "Plateforme Test",
  "slug": "plateforme-test",
  "allowed_auth_methods": ["email"]
}
```

Notez l'`id` retourné — c'est votre **Platform ID**, vous en aurez besoin pour toutes les requêtes suivantes.

---

## 9. Créer les templates de notification

Notification utilise des templates pour formater les emails envoyés. Avant d'inscrire un utilisateur, il faut créer les templates nécessaires au flux d'authentification.

### 9.1 Obtenir un token S2S

Dans Swagger Auth, appelez `POST /api/v1/auth/s2s/token` :

```json
{
  "client_id": "<id_de_la_plateforme_test>",
  "client_secret": "<client_secret_de_la_plateforme_test>"
}
```

Notez le `access_token` retourné. Dans Swagger Notification (http://localhost:7002/api/v1/docs/), cliquez sur **Authorize** et entrez :

```
Bearer <access_token>
```

### 9.2 Créer les 4 templates

Appelez `POST /api/v1/templates/` pour chacun des templates suivants :

**Template 1 — Vérification email**
```json
{
  "name": "auth_verify_email",
  "channel": "email",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": "Vérifiez votre adresse email",
  "body": "Bonjour,\n\nCliquez sur ce lien pour vérifier votre email : {{verification_url}}\n\nCe lien expire dans {{expires_in_minutes}} minutes.\n\n{{platform_name}}",
  "variables": ["verification_url", "expires_in_minutes", "platform_name"]
}
```

**Template 2 — Réinitialisation de mot de passe**
```json
{
  "name": "auth_reset_password",
  "channel": "email",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": "Réinitialisation de votre mot de passe",
  "body": "Bonjour,\n\nCliquez sur ce lien pour réinitialiser votre mot de passe : {{reset_url}}\n\nCe lien expire dans {{expires_in_minutes}} minutes.\n\n{{platform_name}}",
  "variables": ["reset_url", "expires_in_minutes", "platform_name"]
}
```

**Template 3 — Magic link**
```json
{
  "name": "auth_magic_link",
  "channel": "email",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": "Votre lien de connexion",
  "body": "Bonjour,\n\nCliquez sur ce lien pour vous connecter : {{magic_link_url}}\n\nCe lien expire dans {{expires_in_minutes}} minutes.\n\n{{platform_name}}",
  "variables": ["magic_link_url", "expires_in_minutes", "platform_name"]
}
```

**Template 4 — OTP SMS**
```json
{
  "name": "auth_otp_sms",
  "channel": "sms",
  "platform_id": "<platform_id_plateforme_test>",
  "subject": null,
  "body": "{{platform_name}} - Votre code de vérification : {{otp_code}}\nExpire dans {{expires_in_minutes}} minutes.",
  "variables": ["otp_code", "expires_in_minutes", "platform_name"]
}
```

---

## 10. Inscrire un premier utilisateur

Tout est en place. Inscrivez un utilisateur via Swagger Auth (`POST /api/v1/auth/register`).

Ajoutez le header suivant :

```
X-Platform-ID: <platform_id_plateforme_test>
```

Body :

```json
{
  "email": "dev@example.com",
  "password": "Test1234!",
  "method": "email"
}
```

Réponse attendue (HTTP 201) :

```json
{
  "id": "...",
  "email": "dev@example.com",
  "email_verified": false,
  "registration_method": "email",
  "registration_platform_id": "...",
  "message": "Verification email sent"
}
```

---

## 11. Vérifier l'email dans Mailpit

Ouvrez Mailpit dans votre navigateur : http://localhost:8025

Vous devriez voir un email **"Vérifiez votre adresse email"** destiné à `dev@example.com`.

> **Qu'est-ce que Mailpit ?**
> Mailpit est un serveur SMTP de développement. Il intercepte tous les emails envoyés par l'application et les affiche dans une interface web, sans jamais les envoyer réellement. C'est l'équivalent de Mailtrap ou MailHog.

---

## 12. Ce qui se passe sous le capot

Lorsque vous avez appelé `POST /auth/register`, voici précisément ce qui s'est passé dans l'écosystème :

### Chorégraphie inter-services

```
Client
  │
  │  POST /auth/register
  ▼
┌─────────────┐
│    Auth     │  1. Valide les données, hache le mot de passe
│   :7000     │  2. Crée l'utilisateur dans sa propre base PostgreSQL
└──────┬──────┘
       │
       │  POST /api/v1/users  (appel S2S avec JWT)
       ▼
┌─────────────┐
│    Users    │  3. Reçoit le auth_user_id et l'email
│   :7001     │  4. Crée le profil dans sa propre base PostgreSQL
└─────────────┘
       │
       │  POST /api/v1/notifications/send  (appel S2S avec JWT)
       ▼
┌─────────────────┐
│  Notification   │  5. Enregistre la demande en base
│     :7002       │  6. Place la tâche dans RabbitMQ
└────────┬────────┘
         │
         │  Celery Worker consomme la tâche
         ▼
┌─────────────────┐
│  Celery Worker  │  7. Récupère le profil utilisateur depuis Users (S2S)
│                 │  8. Rend le template email avec les variables
│                 │  9. Envoie l'email via SMTP → Mailpit
└─────────────────┘
```

### Points clés à retenir

**Auth est le seul émetteur de tokens JWT.** Tous les appels inter-services utilisent des tokens S2S signés par Auth avec sa clé privée RSA. Chaque service valide ces tokens grâce à la clé publique RSA d'Auth (copiée dans son répertoire `keys/`).

**Chaque service a sa propre base de données.** Auth ne connaît que l'email et le mot de passe haché. Users détient le profil complet. Notification ne stocke que les événements de notification. Aucun service n'accède directement à la base d'un autre.

**La notification est asynchrone.** Auth ne "attend" pas que l'email soit envoyé. Il dépose une demande dans RabbitMQ et répond immédiatement au client avec un 201. C'est le worker Celery qui traite l'envoi en arrière-plan, ce qui garantit la résilience.

---

## 13. Redémarrer un service

Si vous modifiez le code d'un service, vous devez le rebuilder :

```powershell
# Rebuilder Auth
cd agt-auth
docker compose up -d --build auth
cd ..

# Rebuilder Users
cd agt-users
docker compose up -d --build users
cd ..

# Rebuilder Notification (service + worker)
cd agt-notification
docker compose up -d --build notification celery-worker
cd ..
```

Pour un simple redémarrage sans rebuild (ex : après modification d'un `.env`) :

```powershell
docker restart agt-auth-service
docker restart agt-users-service
docker restart agt-notif-service agt-notif-worker agt-notif-beat
```

Pour réinitialiser complètement le MVP et repartir de zéro :

```powershell
.\reset_mvp.ps1 --clean
.\deploy_mvp.ps1
```

> **Attention :** `--clean` supprime tous les volumes Docker, donc toutes les données en base. Vous devrez reconfigurer les plateformes et templates.

---

## 14. Consulter les logs

### Logs d'un service

```powershell
# Dernières 50 lignes
docker logs agt-auth-service --tail=50

# Suivre en temps réel
docker logs agt-auth-service --follow

# Logs du worker Celery (pour déboguer les notifications)
docker logs agt-notif-worker --tail=50 --follow
```

### Ce qu'il faut surveiller

Dans les logs d'Auth, les appels inter-services apparaissent ainsi :

```
HTTP Request: POST http://agt-notif-service:7002/api/v1/notifications/send "HTTP/1.1 202 Accepted"
HTTP Request: POST http://agt-users-service:7001/api/v1/users "HTTP/1.1 201 Created"
```

Dans les logs du worker Celery, une tâche réussie ressemble à :

```
Task notifications.send_notification[...] received
HTTP Request: GET http://agt-users-service:7001/api/v1/users/by-auth/... "HTTP/1.1 200 OK"
Task notifications.send_notification[...] succeeded in 0.76s: None
```

Pour une documentation complète sur les logs, consultez → [GUIDE_LOGS.md](./GUIDE_LOGS.md)

---

## 15. Aller plus loin — les autres flux

Félicitations, le flux d'inscription fonctionne. Voici les prochaines étapes naturelles pour approfondir votre connaissance de l'écosystème :

### Flux d'authentification

Le flux suivant logique est la connexion d'un utilisateur déjà inscrit (login, refresh token, logout, /me). Ce flux est entièrement documenté dans :

→ **[GUIDE_AUTH.md](./GUIDE_AUTH.md)** — Authentification, sessions, JWT, 2FA, OAuth

### Gestion des profils utilisateurs

Après l'inscription, Users est le service qui gère les profils, les rôles et les permissions. Pour comprendre comment mettre à jour un profil, assigner des rôles ou gérer les adresses :

→ **[GUIDE_USERS.md](./GUIDE_USERS.md)** — Profils, rôles, permissions, RBAC

### Notifications avancées

Pour aller au-delà des emails transactionnels : campagnes, notifications in-app, SMS, templates avancés :

→ **[GUIDE_NOTIFICATION.md](./GUIDE_NOTIFICATION.md)** — Templates, campagnes, préférences, canaux

### Abonnements et quotas

Pour comprendre comment les plans d'abonnement définissent les quotas d'utilisation de chaque service :

→ **[GUIDE_SUBSCRIPTION.md](./GUIDE_SUBSCRIPTION.md)** — Plans, cycles, quotas

### Paiements

Pour intégrer un flux de paiement (Orange Money, MTN MoMo, Stripe) :

→ **[GUIDE_PAYMENT.md](./GUIDE_PAYMENT.md)** — Providers, webhooks, idempotence

### Wallet

Pour gérer les portefeuilles électroniques, les virements et le ledger double-entry :

→ **[GUIDE_WALLET.md](./GUIDE_WALLET.md)** — Ledger, virements, cash-in/out

### Autres services

| Guide | Sujet |
|---|---|
| [GUIDE_SEARCH.md](./GUIDE_SEARCH.md) | Indexation et recherche full-text |
| [GUIDE_CHAT.md](./GUIDE_CHAT.md) | Messagerie temps réel |
| [GUIDE_CHATBOT.md](./GUIDE_CHATBOT.md) | Orchestrateur IA et RAG |
| [GUIDE_MEDIA.md](./GUIDE_MEDIA.md) | Upload et gestion de fichiers |
| [GUIDE_GEOLOC.md](./GUIDE_GEOLOC.md) | Géolocalisation et geofencing |

### Guides transverses

| Guide | Sujet |
|---|---|
| [GUIDE_SCRIPTS.md](./GUIDE_SCRIPTS.md) | Référence complète des scripts de déploiement |
| [GUIDE_LOGS.md](./GUIDE_LOGS.md) | Lire et interpréter les logs de chaque service |
| [GUIDE_NEW_SERVICE.md](./GUIDE_NEW_SERVICE.md) | Démarrer un service qui n'est pas dans le MVP |

---

*AG Technologies — Usage interne — Tous droits réservés*