# GUIDE — Service Users

> **AG Technologies — Usage interne**
> Service Users v1.0 — Port 7001
> Dernière mise à jour : Avril 2026

---

## Table des matières

1. [Rôle du service](#1-rôle-du-service)
2. [Lancer le service localement](#2-lancer-le-service-localement)
3. [Variables d'environnement](#3-variables-denvironnement)
4. [Conventions importantes](#4-conventions-importantes)
5. [Référence rapide des endpoints](#5-référence-rapide-des-endpoints)
6. [Scénario complet — Utilisation pas à pas](#6-scénario-complet--utilisation-pas-à-pas)
7. [Flux inter-services](#7-flux-inter-services)
8. [Bugs connus et points d'attention](#8-bugs-connus-et-points-dattention)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Rôle du service

Le service Users est la **source de vérité pour tout ce qui concerne les profils utilisateurs** dans l'écosystème AGT.

Il répond à une question simple : **qui est cet utilisateur, et qu'est-ce qu'il a le droit de faire ?**

Concrètement, il gère :

- Le **profil** de chaque utilisateur (nom, email, photo, date de naissance...)
- Les **adresses** des utilisateurs
- Les **rôles et permissions** (RBAC — qui peut faire quoi sur quelle plateforme)
- Les **documents KYC** (pièces d'identité, justificatifs...)
- Les **métadonnées** (données flexibles par plateforme)
- La **suppression** des comptes (soft delete et hard delete RGPD)

> **À retenir :** Users ne gère PAS l'authentification. C'est le service Auth (port 7000) qui s'en occupe. Users stocke uniquement les informations de profil.

---

## 2. Lancer le service localement

### Prérequis

- Docker et Docker Compose installés
- Le service Auth (port 7000) doit être lancé en premier
- Fichier `keys/auth_public.pem` présent (copié automatiquement par `deploy_mvp.ps1`)

### Commandes

```bash
# Se placer dans le dossier du service
cd agt-users

# Copier le fichier d'environnement
cp .env.example .env

# Lancer le service (première fois — build obligatoire)
sudo docker compose up -d --build

# Lancer le service (fois suivantes)
sudo docker compose up -d

# Vérifier que tout tourne
sudo docker compose logs users --tail=20
```

### Appliquer les migrations (première fois uniquement)

```bash
sudo docker compose exec users python manage.py makemigrations users
sudo docker compose exec users python manage.py makemigrations roles
sudo docker compose exec users python manage.py makemigrations documents
sudo docker compose exec users python manage.py migrate
```

### Vérification

Ouvrez dans votre navigateur :

- **Swagger UI** : http://localhost:7001/api/v1/docs/
- **Health check** : http://localhost:7001/api/v1/users/health

Réponse attendue du health check :

```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```

### Arrêter le service

```bash
# Arrêter sans supprimer les données
sudo docker compose down

# Arrêter ET supprimer les données (reset complet)
sudo docker compose down -v
```

---

## 3. Variables d'environnement

| Variable                         | Exemple                                             | Description                                |
| -------------------------------- | --------------------------------------------------- | ------------------------------------------ |
| `DATABASE_URL`                   | `postgresql://user:pass@agt-users-db:5432/users_db` | Connexion à la base de données             |
| `REDIS_URL`                      | `redis://agt-users-redis:6379/0`                    | Connexion à Redis (cache permissions)      |
| `AUTH_PUBLIC_KEY_PATH`           | `keys/auth_public.pem`                              | Clé publique RSA pour valider les JWT      |
| `AUTH_SERVICE_URL`               | `http://agt-auth-service:7000/api/v1`               | URL interne du service Auth                |
| `AUTH_ADMIN_API_KEY`             | `change-me-admin-api-key-very-secret`               | Clé admin pour appeler Auth en S2S         |
| `S2S_AUTH_URL`                   | `http://agt-auth-service:7000/api/v1`               | URL Auth pour obtenir un token S2S         |
| `S2S_CLIENT_ID`                  | `<uuid>`                                            | ID de la plateforme S2S de ce service      |
| `S2S_CLIENT_SECRET`              | `<secret>`                                          | Secret de la plateforme S2S                |
| `DEFAULT_HARD_DELETE_DELAY_DAYS` | `30`                                                | Délai avant hard delete après soft delete  |
| `PERMISSION_CACHE_TTL`           | `300`                                               | Durée du cache des permissions en secondes |

> Consultez `.env.example` pour la liste complète.

---

## 4. Conventions importantes

### 4.1 Deux types d'identifiants utilisateur

C'est la convention la plus importante à comprendre. Il existe **deux identifiants différents** pour un utilisateur :

| Identifiant    | Nom dans l'API      | Origine              | Usage                                                    |
| -------------- | ------------------- | -------------------- | -------------------------------------------------------- |
| `id`           | `users_profiles.id` | Généré par Users     | Utilisé dans TOUS les endpoints de Users (`/users/{id}`) |
| `auth_user_id` | `users_auth.id`     | Vient du JWT (`sub`) | Utilisé pour faire le lien avec Auth                     |

**Règle pratique :** quand un autre service a besoin du profil Users d'un utilisateur, il utilise son `auth_user_id` (trouvé dans le JWT) et appelle `GET /users/by-auth/{authUserId}` pour récupérer le profil complet avec son `id` Users.

### 4.2 Email et téléphone sont en lecture seule

Dans Users, il est **impossible de modifier** `email` et `phone` via `PUT /users/{id}`. Ces champs ne peuvent être modifiés que par le service Auth via `POST /users/sync`. Si vous envoyez `email` ou `phone` dans un PUT, ils seront ignorés silencieusement.

### 4.3 platform_id = UUID Auth directement

Users n'a pas de table locale des plateformes. Le `platform_id` utilisé partout (rôles, permissions, metadata, documents) est directement l'UUID de la plateforme dans Auth. Pas de table intermédiaire.

### 4.4 Token Bearer obligatoire sur tous les endpoints

Tous les endpoints (sauf `/health`) nécessitent un token JWT valide dans le header :

```
Authorization: Bearer <votre_token>
```

Le token est obtenu via `POST /auth/login` sur le service Auth (port 7000).

### 4.5 Modèle de suppression en deux niveaux

Users propose deux types de suppression :

- **Soft delete** (`DELETE /users/{id}`) : le compte est marqué `deleted`, désactivé dans Auth, mais les données restent en base pendant 30 jours.
- **Hard delete RGPD** (`DELETE /users/{id}/permanent`) : suppression définitive et irréversible. Purge Auth puis purge Users.

---

## 5. Référence rapide des endpoints

> Cliquez sur le lien de chaque endpoint pour accéder au scénario de test détaillé dans la section 6.

### Health

| Méthode | URL             | Description     | Auth | Scénario                                        |
| ------- | --------------- | --------------- | ---- | ----------------------------------------------- |
| GET     | `/users/health` | État du service | Non  | [→ 6.1](#61-vérifier-que-le-service-fonctionne) |

### Profil

| Méthode | URL                                  | Description                             | Auth | Scénario                                                |
| ------- | ------------------------------------ | --------------------------------------- | ---- | ------------------------------------------------------- |
| POST    | `/users`                             | Créer un profil (provisioning par Auth) | Oui  | [→ 6.3](#63-créer-un-profil-utilisateur)                |
| GET     | `/users`                             | Lister tous les profils (paginé)        | Oui  | [→ 6.4](#64-lister-les-utilisateurs)                    |
| GET     | `/users/{id}`                        | Consulter un profil                     | Oui  | [→ 6.5](#65-consulter-un-profil)                        |
| PUT     | `/users/{id}`                        | Mettre à jour un profil                 | Oui  | [→ 6.6](#66-mettre-à-jour-un-profil)                    |
| DELETE  | `/users/{id}`                        | Soft delete                             | Oui  | [→ 6.14](#614-soft-delete--désactiver-un-compte)        |
| GET     | `/users/by-auth/{authUserId}`        | Trouver un profil par auth_user_id      | Oui  | [→ 6.7](#67-trouver-un-profil-par-auth_user_id)         |
| DELETE  | `/users/{id}/platforms/{platformId}` | Quitter une plateforme                  | Oui  | [→ 6.13](#613-quitter-une-plateforme)                   |
| DELETE  | `/users/{id}/permanent`              | Hard delete RGPD                        | Oui  | [→ 6.15](#615-hard-delete-rgpd--suppression-définitive) |
| PUT     | `/users/{id}/photo`                  | Mettre à jour la photo                  | Oui  | [→ 6.8](#68-mettre-à-jour-la-photo-de-profil)           |
| GET     | `/users/search`                      | Rechercher des utilisateurs             | Oui  | [→ 6.16](#616-rechercher-des-utilisateurs)              |
| GET     | `/users/stats`                       | Statistiques globales                   | Oui  | [→ 6.17](#617-statistiques-globales)                    |

### Sync (appelés par Auth uniquement)

| Méthode | URL                  | Description                          | Auth | Scénario                                           |
| ------- | -------------------- | ------------------------------------ | ---- | -------------------------------------------------- |
| POST    | `/users/status-sync` | Synchroniser le statut depuis Auth   | Oui  | [→ 6.18](#618-synchroniser-le-statut-depuis-auth)  |
| POST    | `/users/sync`        | Synchroniser email/phone depuis Auth | Oui  | [→ 6.19](#619-synchroniser-emailphone-depuis-auth) |

### Adresses

| Méthode | URL                                         | Description                      | Auth | Scénario                                    |
| ------- | ------------------------------------------- | -------------------------------- | ---- | ------------------------------------------- |
| POST    | `/users/{id}/addresses`                     | Ajouter une adresse              | Oui  | [→ 6.9.1](#691-ajouter-une-adresse)         |
| GET     | `/users/{id}/addresses`                     | Lister les adresses              | Oui  | [→ 6.9.2](#692-lister-les-adresses)         |
| PUT     | `/users/{id}/addresses/{addressId}`         | Modifier une adresse             | Oui  | [→ 6.9.3](#693-modifier-une-adresse)        |
| DELETE  | `/users/{id}/addresses/{addressId}`         | Supprimer une adresse            | Oui  | [→ 6.9.4](#694-supprimer-une-adresse)       |
| PUT     | `/users/{id}/addresses/{addressId}/default` | Définir comme adresse par défaut | Oui  | [→ 6.9.5](#695-définir-ladresse-par-défaut) |

### Rôles et Permissions (RBAC)

| Méthode | URL                                                           | Description                           | Auth | Scénario                                             |
| ------- | ------------------------------------------------------------- | ------------------------------------- | ---- | ---------------------------------------------------- |
| POST    | `/platforms/{platformId}/roles`                               | Créer un rôle                         | Oui  | [→ 6.10.1](#6101-créer-un-rôle)                      |
| GET     | `/platforms/{platformId}/roles`                               | Lister les rôles                      | Oui  | [→ 6.10.2](#6102-lister-les-rôles)                   |
| PUT     | `/platforms/{platformId}/roles/{roleId}`                      | Modifier un rôle                      | Oui  | [→ 6.10.3](#6103-modifier-un-rôle)                   |
| DELETE  | `/platforms/{platformId}/roles/{roleId}`                      | Supprimer un rôle                     | Oui  | [→ 6.10.4](#6104-supprimer-un-rôle)                  |
| POST    | `/platforms/{platformId}/permissions`                         | Créer une permission                  | Oui  | [→ 6.10.5](#6105-créer-une-permission)               |
| GET     | `/platforms/{platformId}/permissions`                         | Lister les permissions                | Oui  | [→ 6.10.6](#6106-lister-les-permissions)             |
| POST    | `/platforms/{platformId}/roles/{roleId}/permissions/{permId}` | Attacher une permission à un rôle     | Oui  | [→ 6.10.7](#6107-attacher-une-permission-à-un-rôle)  |
| DELETE  | `/platforms/{platformId}/roles/{roleId}/permissions/{permId}` | Détacher une permission               | Oui  | [→ 6.10.8](#6108-détacher-une-permission-dun-rôle)   |
| POST    | `/users/{id}/roles`                                           | Assigner un rôle à un utilisateur     | Oui  | [→ 6.10.9](#6109-assigner-un-rôle-à-un-utilisateur)  |
| GET     | `/users/{id}/roles`                                           | Lister les rôles d'un utilisateur     | Oui  | [→ 6.10.10](#61010-lister-les-rôles-dun-utilisateur) |
| DELETE  | `/users/{id}/roles/{roleId}`                                  | Retirer un rôle                       | Oui  | [→ 6.10.11](#61011-retirer-un-rôle-à-un-utilisateur) |
| GET     | `/users/{id}/permissions/check`                               | Vérifier une permission (cache Redis) | Oui  | [→ 6.10.12](#61012-vérifier-une-permission)          |

### Documents KYC

| Méthode | URL                                     | Description                    | Auth | Scénario                                             |
| ------- | --------------------------------------- | ------------------------------ | ---- | ---------------------------------------------------- |
| POST    | `/users/{id}/documents`                 | Attacher un document           | Oui  | [→ 6.11.1](#6111-attacher-un-document)               |
| GET     | `/users/{id}/documents`                 | Lister les documents           | Oui  | [→ 6.11.2](#6112-lister-les-documents)               |
| PUT     | `/users/{id}/documents/{docId}/status`  | Valider ou rejeter un document | Oui  | [→ 6.11.3](#6113-valider-ou-rejeter-un-document)     |
| GET     | `/users/{id}/documents/{docId}/history` | Historique des versions        | Oui  | [→ 6.11.4](#6114-consulter-lhistorique-dun-document) |
| DELETE  | `/users/{id}/documents/{docId}`         | Supprimer un document          | Oui  | [→ 6.11.5](#6115-supprimer-un-document)              |

### Métadonnées

| Méthode | URL                                       | Description                            | Auth | Scénario                                                 |
| ------- | ----------------------------------------- | -------------------------------------- | ---- | -------------------------------------------------------- |
| PUT     | `/users/{id}/metadata/{platformId}`       | Créer ou mettre à jour des métadonnées | Oui  | [→ 6.12.1](#6121-créer-ou-mettre-à-jour-des-métadonnées) |
| GET     | `/users/{id}/metadata/{platformId}`       | Lire les métadonnées                   | Oui  | [→ 6.12.2](#6122-lire-les-métadonnées)                   |
| DELETE  | `/users/{id}/metadata/{platformId}/{key}` | Supprimer une clé                      | Oui  | [→ 6.12.3](#6123-supprimer-une-clé-de-métadonnées)       |

---

## 6. Scénario complet — Utilisation pas à pas

> Ce scénario vous guide de A à Z dans l'utilisation du service Users. Suivez les étapes dans l'ordre. Chaque étape vous donne exactement quoi envoyer et ce que vous devez recevoir.
>
> **Swagger UI** : http://localhost:7001/api/v1/docs/
> **Swagger Auth** : http://localhost:7000/api/v1/docs/

---

### 6.1 Vérifier que le service fonctionne

Avant tout, vérifiez que le service est up.

**Endpoint :** `GET /api/v1/users/health`
**Auth requise :** Non

Dans Swagger, cherchez `GET /users/health`, cliquez **Try it out** puis **Execute**.

**Réponse attendue (200) :**

```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```

Si vous obtenez une erreur, vérifiez que les containers sont bien lancés :

```bash
sudo docker compose ps
```

---

### 6.2 Obtenir un token d'authentification

Tous les endpoints suivants nécessitent un token. Voici comment l'obtenir.

**Étape 1 — Aller sur le Swagger d'Auth :** http://localhost:7000/api/v1/docs/

**Étape 2 — Créer un compte** via `POST /auth/register`

> Passez cette étape si vous avez déjà un compte.

Body :

```json
{
  "email": "votre@email.com",
  "password": "VotreMotDePasse!",
  "phone": "6XXXXXXXXX",
  "method": "email"
}
```

Header requis :

```
X-Platform-Id: <votre-platform-id>
```

**Réponse attendue (201) :**

```json
{
  "id": "26d8a281-bd73-4915-b066-5e0214cf5d93",
  "email": "votre@email.com",
  "email_verified": false,
  "registration_method": "email",
  "registration_platform_id": "<votre-platform-id>",
  "message": "Verification email sent"
}
```

> Notez l'`id` retourné — c'est votre `auth_user_id`. Vous en aurez besoin si vous devez créer manuellement un profil Users (section 6.3).

**Étape 3 — Se connecter** via `POST /auth/login`

Body :

```json
{
  "email": "votre@email.com",
  "password": "VotreMotDePasse!",
  "platform_id": "<votre-platform-id>"
}
```

Header requis :

```
X-Platform-Id: <votre-platform-id>
```

**Réponse attendue (200) :**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900,
  "requires_2fa": false
}
```

**Étape 4 — Configurer le token dans Swagger Users**

1. Allez sur http://localhost:7001/api/v1/docs/
2. Cliquez sur le bouton **Authorize** 🔒 en haut à droite
3. Collez votre `access_token` dans le champ `BearerAuth`
4. Cliquez **Authorize** puis **Close**

> **Important :** le token expire après 15 minutes (900 secondes). Quand vous obtenez une erreur `invalid_token`, revenez sur Auth, refaites le login, et mettez à jour le token dans Swagger Users.

---

### 6.3 Créer un profil utilisateur

> **Note :** en conditions normales, cet endpoint est appelé **automatiquement** par Auth lors d'un `POST /auth/register`. Vous n'avez pas à l'appeler manuellement sauf pour des tests ou des cas particuliers.

**Endpoint :** `POST /api/v1/users`
**Auth requise :** Oui (token Bearer)

Body :

```json
{
  "auth_user_id": "26d8a281-bd73-4915-b066-5e0214cf5d93",
  "first_name": "Stephane",
  "last_name": "Atabong",
  "email": "stephane@example.com",
  "phone": "671949527"
}
```

> `auth_user_id` est l'`id` retourné par Auth lors du register (`POST /auth/register`).

**Réponse attendue (201) :**

```json
{
  "id": "808294af-cecd-4d15-9e4f-3575464d3668",
  "auth_user_id": "26d8a281-bd73-4915-b066-5e0214cf5d93",
  "first_name": "Stephane",
  "last_name": "Atabong",
  "full_name": "Stephane Atabong",
  "email": "stephane@example.com",
  "phone": "671949527",
  "avatar_url": null,
  "birth_date": null,
  "gender": null,
  "status": "active",
  "created_at": "2026-04-14T13:05:59.640399-05:00",
  "updated_at": "2026-04-14T13:05:59.640432-05:00"
}
```

> Notez bien l'`id` retourné (ex: `808294af-...`). C'est votre `users_profiles.id`, vous en aurez besoin pour tous les endpoints suivants.

**Erreurs possibles :**

- `409 Conflict` : un profil existe déjà pour cet `auth_user_id`

---

### 6.4 Lister les utilisateurs

**Endpoint :** `GET /api/v1/users`
**Auth requise :** Oui

Dans Swagger, cherchez `GET /users`, cliquez **Try it out** puis **Execute** (laissez les filtres vides pour commencer).

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "id": "808294af-cecd-4d15-9e4f-3575464d3668",
      "auth_user_id": "26d8a281-bd73-4915-b066-5e0214cf5d93",
      "first_name": "Stephane",
      "last_name": "Atabong",
      "email": "stephane@example.com",
      "status": "active",
      "created_at": "2026-04-14T13:05:59.640399-05:00"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1
}
```

**Filtres disponibles (query params) :**

- `status` : filtrer par statut (`active`, `inactive`, `deleted`)
- `platform_id` : filtrer par plateforme
- `role` : filtrer par nom de rôle

---

### 6.5 Consulter un profil

**Endpoint :** `GET /api/v1/users/{id}`
**Auth requise :** Oui

Dans Swagger, cherchez `GET /users/{user_id}`, cliquez **Try it out**, renseignez le `user_id` et cliquez **Execute**.

Exemple avec `user_id = 808294af-cecd-4d15-9e4f-3575464d3668` :

**Réponse attendue (200) :**

```json
{
  "id": "808294af-cecd-4d15-9e4f-3575464d3668",
  "auth_user_id": "26d8a281-bd73-4915-b066-5e0214cf5d93",
  "first_name": "Stephane",
  "last_name": "Atabong",
  "full_name": "Stephane Atabong",
  "email": "stephane@example.com",
  "phone": "671949527",
  "avatar_url": null,
  "birth_date": null,
  "gender": null,
  "status": "active",
  "created_at": "2026-04-14T13:05:59.640399-05:00",
  "updated_at": "2026-04-14T13:05:59.640432-05:00"
}
```

> **Note :** les profils consultés sont mis en cache Redis automatiquement pour accélérer les lectures.

---

### 6.6 Mettre à jour un profil

**Endpoint :** `PUT /api/v1/users/{id}`
**Auth requise :** Oui

> **Rappel important :** `email` et `phone` sont ignorés même si vous les envoyez. Seul Auth peut les modifier via `/users/sync`.

Body :

```json
{
  "first_name": "Stephane",
  "last_name": "Atabong",
  "birth_date": "1995-06-15",
  "gender": "male"
}
```

**Réponse attendue (200) :**

```json
{
  "id": "808294af-cecd-4d15-9e4f-3575464d3668",
  "first_name": "Stephane",
  "last_name": "Atabong",
  "full_name": "Stephane Atabong",
  "email": "stephane@example.com",
  "phone": "671949527",
  "birth_date": "1995-06-15",
  "gender": "male",
  "status": "active",
  "updated_at": "2026-04-15T10:00:00.000000-05:00"
}
```

> Chaque modification est enregistrée dans les `audit_logs` automatiquement.

---

### 6.7 Trouver un profil par auth_user_id

Cet endpoint est utilisé par les autres services AGT pour résoudre un profil Users à partir du JWT.

**Endpoint :** `GET /api/v1/users/by-auth/{auth_user_id}`
**Auth requise :** Oui

Exemple avec `auth_user_id = 26d8a281-bd73-4915-b066-5e0214cf5d93` :

**Réponse attendue (200) :** même format que `GET /users/{id}`

> **Cas d'usage :** un service reçoit un JWT avec `sub = 26d8a281-...`. Il appelle cet endpoint pour obtenir le profil complet et l'`id` Users (`808294af-...`) nécessaire pour les autres appels.

---

### 6.8 Mettre à jour la photo de profil

> **Prérequis :** le service Média (port 7003) doit être lancé. Uploadez d'abord votre photo sur Média, puis utilisez le `media_id` retourné ici.

**Endpoint :** `PUT /api/v1/users/{id}/photo`
**Auth requise :** Oui

Body :

```json
{
  "media_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

**Réponse attendue (200) :**

```json
{
  "id": "808294af-cecd-4d15-9e4f-3575464d3668",
  "avatar_url": "https://cdn.agt.com/media/3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "updated_at": "2026-04-15T10:00:00.000000-05:00"
}
```

---

### 6.9 Gérer les adresses

#### 6.9.1 Ajouter une adresse

**Endpoint :** `POST /api/v1/users/{id}/addresses`
**Auth requise :** Oui

Body :

```json
{
  "type": "home",
  "street": "123 Rue de la Paix",
  "city": "Yaoundé",
  "country": "Cameroun",
  "postal_code": "00237"
}
```

**Réponse attendue (201) :**

```json
{
  "id": "a7efc41a-c0a6-4250-b716-410eb9f3efa2",
  "type": "home",
  "street": "123 Rue de la Paix",
  "city": "Yaoundé",
  "country": "Cameroun",
  "postal_code": "00237",
  "is_default": false,
  "created_at": "2026-04-15T03:31:03.912720-05:00"
}
```

#### 6.9.2 Lister les adresses

**Endpoint :** `GET /api/v1/users/{id}/addresses`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "id": "a7efc41a-c0a6-4250-b716-410eb9f3efa2",
      "type": "home",
      "street": "123 Rue de la Paix",
      "city": "Yaoundé",
      "country": "Cameroun",
      "postal_code": "00237",
      "is_default": false,
      "created_at": "2026-04-15T03:31:03.912720-05:00"
    }
  ]
}
```

#### 6.9.3 Modifier une adresse

**Endpoint :** `PUT /api/v1/users/{id}/addresses/{addressId}`
**Auth requise :** Oui

Body (seuls les champs à modifier) :

```json
{
  "street": "456 Avenue Kennedy",
  "city": "Douala"
}
```

**Réponse attendue (200) :** l'adresse mise à jour.

#### 6.9.4 Supprimer une adresse

**Endpoint :** `DELETE /api/v1/users/{id}/addresses/{addressId}`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "message": "Adresse supprimee."
}
```

#### 6.9.5 Définir l'adresse par défaut

**Endpoint :** `PUT /api/v1/users/{id}/addresses/{addressId}/default`
**Auth requise :** Oui (pas de body)

**Réponse attendue (200) :**

```json
{
  "message": "Adresse definie par defaut.",
  "id": "a7efc41a-c0a6-4250-b716-410eb9f3efa2"
}
```

---

### 6.10 Gérer les rôles et permissions (RBAC)

> Le RBAC d'AGT est 100% dynamique — aucun rôle n'est codé en dur. Tout est créé via l'API.
> Le `platform_id` utilisé ici est l'UUID de la plateforme dans Auth.

#### 6.10.1 Créer un rôle

**Endpoint :** `POST /api/v1/platforms/{platformId}/roles`
**Auth requise :** Oui

Body :

```json
{
  "name": "vendeur",
  "description": "Role vendeur sur la plateforme"
}
```

**Réponse attendue (201) :**

```json
{
  "id": "91136ba8-e099-4032-a4fd-90b69cecf625",
  "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
  "name": "vendeur",
  "description": "Role vendeur sur la plateforme",
  "created_at": "2026-04-15T03:42:34.997630-05:00"
}
```

> Notez le `role_id` retourné. Il sera utile pour les étapes suivantes.

#### 6.10.2 Lister les rôles

**Endpoint :** `GET /api/v1/platforms/{platformId}/roles`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "id": "91136ba8-e099-4032-a4fd-90b69cecf625",
      "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
      "name": "vendeur",
      "description": "Role vendeur sur la plateforme",
      "created_at": "2026-04-15T03:42:34.997630-05:00"
    }
  ]
}
```

#### 6.10.3 Modifier un rôle

**Endpoint :** `PUT /api/v1/platforms/{platformId}/roles/{roleId}`
**Auth requise :** Oui

Body :

```json
{
  "name": "vendeur_senior",
  "description": "Role vendeur senior"
}
```

**Réponse attendue (200) :** le rôle mis à jour.

#### 6.10.4 Supprimer un rôle

**Endpoint :** `DELETE /api/v1/platforms/{platformId}/roles/{roleId}`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "message": "Role supprime."
}
```

#### 6.10.5 Créer une permission

**Endpoint :** `POST /api/v1/platforms/{platformId}/permissions`
**Auth requise :** Oui

Body :

```json
{
  "name": "create_product",
  "description": "Peut creer un produit"
}
```

**Réponse attendue (201) :**

```json
{
  "id": "e08ce8da-36b2-4569-a730-4af1a563a545",
  "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
  "name": "create_product",
  "description": "Peut creer un produit",
  "created_at": "2026-04-15T03:53:13.284062-05:00"
}
```

#### 6.10.6 Lister les permissions

**Endpoint :** `GET /api/v1/platforms/{platformId}/permissions`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "id": "e08ce8da-36b2-4569-a730-4af1a563a545",
      "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
      "name": "create_product",
      "description": "Peut creer un produit",
      "created_at": "2026-04-15T03:53:13.284062-05:00"
    }
  ]
}
```

#### 6.10.7 Attacher une permission à un rôle

**Endpoint :** `POST /api/v1/platforms/{platformId}/roles/{roleId}/permissions`
**Auth requise :** Oui

> La permission est passée directement dans l'URL via `permId` — aucun body requis.

Exemple d'URL complète :

```
POST /api/v1/platforms/48a8351c-.../roles/91136ba8-.../permissions/e08ce8da-...
```

**Réponse attendue (201) :**

```json
{
  "message": "Permission attachee."
}
```

#### 6.10.8 Détacher une permission d'un rôle

**Endpoint :** `DELETE /api/v1/platforms/{platformId}/roles/{roleId}/permissions/{permId}`
**Auth requise :** Oui (pas de body)

**Réponse attendue (200) :**

```json
{
  "message": "Permission detachee."
}
```

#### 6.10.9 Assigner un rôle à un utilisateur

**Endpoint :** `POST /api/v1/users/{id}/roles`
**Auth requise :** Oui

Body :

```json
{
  "role_id": "91136ba8-e099-4032-a4fd-90b69cecf625"
}
```

**Réponse attendue (201) :**

```json
{
  "user_id": "eaf6009e-0d42-42e6-97e5-5bfde4e07fd5",
  "role": {
    "id": "91136ba8-e099-4032-a4fd-90b69cecf625",
    "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
    "name": "vendeur",
    "description": "Role vendeur sur la plateforme",
    "created_at": "2026-04-15T03:42:34.997630-05:00"
  },
  "assigned": true
}
```

> Une notification est envoyée automatiquement via le service Notification quand un rôle est assigné.

#### 6.10.10 Lister les rôles d'un utilisateur

**Endpoint :** `GET /api/v1/users/{id}/roles`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "user_id": "eaf6009e-0d42-42e6-97e5-5bfde4e07fd5",
  "roles": [
    {
      "role": {
        "id": "91136ba8-e099-4032-a4fd-90b69cecf625",
        "name": "vendeur",
        "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d"
      },
      "assigned_at": "2026-04-15T09:00:16.111464+00:00",
      "assigned_by": "bb7bdaf3-2f6c-4ad7-91f8-003888e2ae99"
    }
  ]
}
```

#### 6.10.11 Retirer un rôle à un utilisateur

**Endpoint :** `DELETE /api/v1/users/{id}/roles/{roleId}`
**Auth requise :** Oui (pas de body)

**Réponse attendue (200) :**

```json
{
  "message": "Role retire."
}
```

#### 6.10.12 Vérifier une permission

C'est l'endpoint le plus utilisé par les autres services — il vérifie en temps réel si un utilisateur a une permission donnée sur une plateforme. Le résultat est mis en cache Redis.

**Endpoint :** `GET /api/v1/users/{id}/permissions/check`
**Auth requise :** Oui

Query params (obligatoires) :

- `permission` : nom de la permission à vérifier (ex: `create_product`) — visible dans le formulaire Swagger
- `platform_id` : UUID de la plateforme — visible dans le formulaire Swagger

Exemple d'URL complète :

```
GET /api/v1/users/eaf6009e-0d42-42e6-97e5-5bfde4e07fd5/permissions/check?permission=create_product&platform_id=48a8351c-8791-4845-a65e-c00e56332d2d
```

**Réponse attendue (200) :**

```json
{
  "user_id": "eaf6009e-0d42-42e6-97e5-5bfde4e07fd5",
  "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
  "permission": "create_product",
  "granted": true,
  "via_role": "vendeur"
}
```

> Si `granted` est `false`, `via_role` sera `null`.

---

### 6.11 Gérer les documents KYC

#### 6.11.1 Attacher un document

**Endpoint :** `POST /api/v1/users/{id}/documents`
**Auth requise :** Oui

> **Prérequis :** uploadez d'abord le fichier sur le service Média (port 7003) pour obtenir un `media_id`.

Body :

```json
{
  "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
  "doc_type": "identity_card",
  "media_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

**Réponse attendue (201) :**

```json
{
  "id": "fc1c01c3-811a-4301-ac5c-540f5277b95a",
  "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
  "doc_type": "identity_card",
  "media_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "status": "pending",
  "comment": null,
  "submitted_at": "2026-04-15T04:22:45.753504-05:00",
  "reviewed_at": null
}
```

> Le document est créé avec le statut `pending`. Un administrateur devra le valider ou le rejeter.
> Si un document du même type existe déjà pour cette plateforme, l'ancien est archivé automatiquement et le nouveau le remplace.

#### 6.11.2 Lister les documents

**Endpoint :** `GET /api/v1/users/{id}/documents`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "id": "fc1c01c3-811a-4301-ac5c-540f5277b95a",
      "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
      "doc_type": "identity_card",
      "media_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "status": "pending",
      "comment": null,
      "submitted_at": "2026-04-15T04:22:45.753504-05:00",
      "reviewed_at": null
    }
  ]
}
```

#### 6.11.3 Valider ou rejeter un document

**Endpoint :** `PUT /api/v1/users/{id}/documents/{docId}/status`
**Auth requise :** Oui (action réservée aux administrateurs)

Body pour valider :

```json
{
  "status": "validated",
  "comment": "Document conforme"
}
```

Body pour rejeter :

```json
{
  "status": "rejected",
  "comment": "Document illisible, veuillez resoumettre"
}
```

**Réponse attendue (200) :** le document mis à jour avec le nouveau statut et `reviewed_at` renseigné.

> Une notification est envoyée automatiquement à l'utilisateur lors d'une validation ou d'un rejet.

#### 6.11.4 Consulter l'historique d'un document

**Endpoint :** `GET /api/v1/users/{id}/documents/{docId}/history`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "id": "abc123...",
      "media_id": "ancien-media-id",
      "status": "rejected",
      "comment": "Document illisible",
      "submitted_at": "2026-04-10T10:00:00.000000-05:00",
      "reviewed_at": "2026-04-11T10:00:00.000000-05:00",
      "archived_at": "2026-04-15T04:22:45.000000-05:00"
    }
  ]
}
```

> L'historique est vide si le document n'a jamais été re-soumis. Il se remplit uniquement quand un utilisateur soumet un nouveau fichier pour remplacer un document existant.

#### 6.11.5 Supprimer un document

**Endpoint :** `DELETE /api/v1/users/{id}/documents/{docId}`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "message": "Document supprime."
}
```

---

### 6.12 Gérer les métadonnées

Les métadonnées permettent de stocker des informations flexibles (clé-valeur) par utilisateur et par plateforme. Chaque plateforme peut stocker ses propres données sans interférer avec les autres.

#### 6.12.1 Créer ou mettre à jour des métadonnées

**Endpoint :** `PUT /api/v1/users/{id}/metadata/{platformId}`
**Auth requise :** Oui

Body (objet JSON libre clé-valeur) :

```json
{
  "theme": "dark",
  "language": "fr",
  "notifications": "true"
}
```

**Réponse attendue (200) :**

```json
{
  "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
  "metadata": [
    { "key": "theme", "value": "dark" },
    { "key": "language", "value": "fr" },
    { "key": "notifications", "value": "true" }
  ]
}
```

> Cet endpoint fonctionne en "upsert" : si une clé existe déjà, elle est mise à jour. Sinon, elle est créée.

#### 6.12.2 Lire les métadonnées

**Endpoint :** `GET /api/v1/users/{id}/metadata/{platformId}`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "user_id": "eaf6009e-0d42-42e6-97e5-5bfde4e07fd5",
  "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
  "metadata": {
    "theme": "dark",
    "language": "fr",
    "notifications": "true"
  }
}
```

#### 6.12.3 Supprimer une clé de métadonnées

**Endpoint :** `DELETE /api/v1/users/{id}/metadata/{platformId}/{key}`
**Auth requise :** Oui

Exemple pour supprimer la clé `theme` :

```
DELETE /api/v1/users/eaf6009e-.../metadata/48a8351c-.../theme
```

**Réponse attendue (200) :**

```json
{
  "message": "Cle 'theme' supprimee."
}
```

---

### 6.13 Quitter une plateforme

Cet endpoint permet à un utilisateur de quitter une plateforme spécifique sans supprimer son compte global. Tout ce qui est lié à cette plateforme est nettoyé, mais le profil et le compte Auth restent intacts.

**Ce qui est supprimé :**

- Tous les rôles de l'utilisateur sur cette plateforme
- Toutes les métadonnées de l'utilisateur pour cette plateforme
- Tous les documents de l'utilisateur pour cette plateforme (passent en statut `archived`)

**Ce qui est conservé :**

- Le profil utilisateur
- Le compte Auth
- Les données des autres plateformes

**Endpoint :** `DELETE /api/v1/users/{id}/platforms/{platformId}`
**Auth requise :** Oui (pas de body)

**Réponse attendue (200) :**

```json
{
  "message": "Platform left",
  "platform_id": "48a8351c-8791-4845-a65e-c00e56332d2d",
  "roles_removed": 1,
  "metadata_cleared": true,
  "documents_archived": 0
}
```

---

### 6.14 Soft delete — Désactiver un compte

Le soft delete marque le compte comme supprimé et le désactive dans Auth. Les données restent en base pendant 30 jours (configurable via `DEFAULT_HARD_DELETE_DELAY_DAYS`).

**Endpoint :** `DELETE /api/v1/users/{id}`
**Auth requise :** Oui (pas de body)

**Réponse attendue (200) :**

```json
{
  "message": "Account deactivated",
  "status": "deleted",
  "hard_delete_scheduled": "2026-05-15T07:47:46.289414+00:00"
}
```

**Ce qui se passe sous le capot :**

1. Users passe le statut du profil à `deleted`
2. Users appelle Auth (`POST /auth/admin/deactivate/{authUserId}`) pour désactiver le compte
3. L'utilisateur ne peut plus se connecter
4. Un `hard_delete_after` est planifié à 30 jours

> **⚠️ Attention :** après un soft delete, le compte Auth est désactivé. Pour réactiver le compte, utilisez `POST /users/status-sync` avec `"status": "active"` — mais notez qu'il n'existe pas encore d'endpoint Auth pour réactiver le compte côté Auth (voir section 8).

---

### 6.15 Hard delete RGPD — Suppression définitive

**⚠️ Action irréversible.** Supprime définitivement et entièrement le profil utilisateur et son compte Auth.

**Endpoint :** `DELETE /api/v1/users/{id}/permanent`
**Auth requise :** Oui (pas de body)

**Réponse attendue (200) :**

```json
{
  "message": "Compte supprime definitivement (RGPD)."
}
```

**Ce qui se passe sous le capot :**

1. Users passe le statut à `deletion_in_progress`
2. Users appelle Auth (`DELETE /auth/admin/purge/{authUserId}`) pour purger le compte Auth
3. Si Auth répond OK (ou 404 = déjà inexistant) → Users supprime définitivement le profil et toutes ses données
4. Si Auth échoue → Users logue l'erreur dans `deletion_error_reason`, passe `purge_auth_pending = true`, et retourne une erreur 500 (un retry devra être planifié)

**Erreurs possibles :**

- `500` avec `"purge_auth_pending": true` : Auth était injoignable. Le profil est en statut `deletion_in_progress`. Un retry manuel est nécessaire.

---

### 6.16 Rechercher des utilisateurs

**Endpoint :** `GET /api/v1/users/search`
**Auth requise :** Oui

Query param requis : `q` (terme de recherche)

La recherche porte sur : `first_name`, `last_name`, `email`, `phone`.

Exemple d'URL :

```
GET /api/v1/users/search?q=Stephane
```

**Réponse attendue (200) :**

```json
{
  "data": [
    {
      "id": "eaf6009e-0d42-42e6-97e5-5bfde4e07fd5",
      "first_name": "Stephane",
      "last_name": "Atabong",
      "email": "stephane@example.com",
      "status": "active"
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 1
}
```

> Les utilisateurs en statut `deleted` sont exclus des résultats de recherche.

---

### 6.17 Statistiques globales

**Endpoint :** `GET /api/v1/users/stats`
**Auth requise :** Oui

**Réponse attendue (200) :**

```json
{
  "total_users": 2,
  "by_status": {
    "active": 1,
    "inactive": 1,
    "deleted": 0,
    "deletion_in_progress": 0
  }
}
```

---

### 6.18 Synchroniser le statut depuis Auth

> **Cet endpoint est appelé par Auth uniquement.** Vous ne devriez pas l'appeler manuellement en production.

**Endpoint :** `POST /api/v1/users/status-sync`
**Auth requise :** Oui

Body :

```json
{
  "auth_user_id": "26d8a281-bd73-4915-b066-5e0214cf5d93",
  "status": "active"
}
```

Valeurs possibles pour `status` : `active`, `inactive`, `deleted`

**Réponse attendue (200) :**

```json
{
  "message": "Statut synchronise.",
  "status": "active"
}
```

---

### 6.19 Synchroniser email/phone depuis Auth

> **Cet endpoint est appelé par Auth uniquement.** Il est déclenché quand un utilisateur change son email ou son téléphone dans Auth.

**Endpoint :** `POST /api/v1/users/sync`
**Auth requise :** Oui

Body :

```json
{
  "auth_user_id": "26d8a281-bd73-4915-b066-5e0214cf5d93",
  "email": "nouveau@email.com",
  "phone": "699111222"
}
```

**Réponse attendue (200) :**

```json
{
  "message": "Identifiants synchronises."
}
```

---

## 7. Flux inter-services

```
┌─────────────┐         ┌─────────────┐         ┌──────────────────┐
│    Auth     │         │    Users    │         │  Notification    │
│  port 7000  │         │  port 7001  │         │   port 7002      │
└──────┬──────┘         └──────┬──────┘         └────────┬─────────┘
       │                       │                          │
       │  POST /users          │                          │
       │  (provisioning)       │                          │
       │──────────────────────>│                          │
       │                       │                          │
       │  POST /users/sync     │                          │
       │  (email/phone change) │                          │
       │──────────────────────>│                          │
       │                       │                          │
       │  POST /status-sync    │                          │
       │  (account activated   │                          │
       │   or deactivated)     │                          │
       │──────────────────────>│                          │
       │                       │                          │
       │                       │  notify role_assigned    │
       │                       │─────────────────────────>│
       │                       │                          │
       │                       │  notify document_        │
       │                       │  validated/rejected      │
       │                       │─────────────────────────>│
       │                       │                          │
       │  POST /deactivate     │                          │
       │  (soft delete)        │                          │
       │<──────────────────────│                          │
       │                       │                          │
       │  DELETE /purge        │                          │
       │  (hard delete RGPD)   │                          │
       │<──────────────────────│                          │
```

### Auth → Users

| Action           | Endpoint Users            | Déclencheur                                 |
| ---------------- | ------------------------- | ------------------------------------------- |
| Créer un profil  | `POST /users`             | Lors d'un `register` dans Auth              |
| Sync email/phone | `POST /users/sync`        | Quand l'utilisateur change ses identifiants |
| Sync statut      | `POST /users/status-sync` | Quand Auth active ou désactive un compte    |

### Users → Auth

| Action               | Endpoint Auth                      | Déclencheur                 |
| -------------------- | ---------------------------------- | --------------------------- |
| Désactiver un compte | `POST /auth/admin/deactivate/{id}` | Lors d'un soft delete Users |
| Purger un compte     | `DELETE /auth/admin/purge/{id}`    | Lors d'un hard delete RGPD  |

### Users → Notification

Users envoie des notifications dans ces situations :

- Rôle assigné à un utilisateur (`role_assigned`)
- Rôle retiré à un utilisateur (`role_removed`)
- Document KYC validé (`document_validated`)
- Document KYC rejeté (`document_rejected`)

---

## 8. Bugs connus et points d'attention

### ⚠️ Pas d'endpoint Auth pour réactiver un compte désactivé

**Problème :** après un soft delete, le compte Auth est désactivé via `POST /auth/admin/deactivate`. Il n'existe pas d'endpoint dans Auth pour le réactiver. L'endpoint `POST /auth/admin/unblock` ne fonctionne que pour les comptes bloqués (brute force) — pas pour les comptes désactivés.

**Impact :** un utilisateur dont le compte a été soft-deleté ne peut plus se reconnecter même si on remet son statut Users à `active` via `/users/status-sync`.

**Contournement actuel :** aucun. À implémenter dans le service Auth.

**À signaler à :** équipe Auth — ajouter `POST /auth/admin/reactivate/{userId}`.

---

### ⚠️ Migrations non incluses dans l'image Docker

**Problème :** les fichiers de migration ne sont pas générés automatiquement au démarrage. Lors de la première installation, il faut les créer manuellement.

**Solution :** voir section [2 — Lancer le service localement](#2-lancer-le-service-localement), étape "Appliquer les migrations".

---

### ⚠️ Fix AuditLog — DjangoJSONEncoder

**Problème :** lors d'un `PUT /users/{id}` avec un champ `birth_date`, le service retournait une erreur 500 car le champ `date` Python n'est pas sérialisable en JSON nativement.

**Fix appliqué :** dans `apps/users/views.py`, méthode `put` de `UserDetailView`, les valeurs sont converties via `DjangoJSONEncoder` avant d'être passées à `AuditLog.objects.create()`.

**Statut :** corrigé ✅

---

## 9. Troubleshooting

### Le service ne démarre pas — `relation "users_profiles" does not exist`

**Cause :** les migrations n'ont pas été appliquées.

**Solution :**

```bash
sudo docker compose exec users python manage.py makemigrations users
sudo docker compose exec users python manage.py makemigrations roles
sudo docker compose exec users python manage.py makemigrations documents
sudo docker compose exec users python manage.py migrate
```

---

### Erreur `invalid_token` sur tous les endpoints

**Cause :** le token JWT a expiré (durée de vie : 15 minutes).

**Solution :** retourner sur http://localhost:7000/api/v1/docs/, refaire `POST /auth/login`, copier le nouveau `access_token`, et le mettre à jour dans le bouton **Authorize** de Swagger Users.

---

### Erreur `user_deactivated` au login

**Cause :** le compte a été désactivé (suite à un soft delete ou une désactivation manuelle).

**Solution temporaire :** appeler `POST /users/status-sync` avec `"status": "active"` pour remettre le statut Users à actif. Attention : le compte Auth reste désactivé (voir bug connu en section 8).

---

### Hard delete retourne `purge_auth_pending: true`

**Cause :** le service Auth était injoignable au moment du hard delete.

**Solution :** vérifier que Auth tourne (`curl http://localhost:7000/api/v1/auth/health`), puis relancer manuellement le hard delete sur le même utilisateur.

---

### Les modifications de code ne sont pas prises en compte

**Cause :** Docker utilise une image buildée. Modifier un fichier local ne suffit pas.

**Solution :** toujours rebuilder après une modification de code :

```bash
sudo docker compose up -d --build
```

---

### Le Swagger n'affiche pas le body sur certains endpoints

**Cause :** connue et corrigée pour la plupart des endpoints. Si un endpoint n'affiche toujours pas de body, utilisez le curl généré par Swagger en ajoutant `-H 'Content-Type: application/json'` et le body dans `-d '{...}'`.

---

_AG Technologies — Confidentiel — Usage interne_
_Guide rédigé après tests complets en conditions réelles — Avril 2026_
