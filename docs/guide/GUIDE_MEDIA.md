# GUIDE_MEDIA — Service Média AGT

> **Version :** 1.1.0 — rédigé après tests complets en conditions réelles — Avril 2026
> **Port :** 7003
> **Stack :** Node.js 20 / NestJS / TypeORM / PostgreSQL / Redis / BullMQ / Sharp
> **CDC de référence :** `docs/cdc/4.medias.txt` v1.4

---

## Table des matières

1. [Rôle du service](#1-rôle-du-service)
2. [Prérequis](#2-prérequis)
3. [Lancer le service localement](#3-lancer-le-service-localement)
4. [Variables d'environnement](#4-variables-denvironnement)
5. [Créer la plateforme S2S dans Auth](#5-créer-la-plateforme-s2s-dans-auth)
6. [Obtenir un token pour tester](#6-obtenir-un-token-pour-tester)
7. [Endpoints — Health](#7-endpoints--health)
8. [Endpoints — Upload](#8-endpoints--upload)
9. [Endpoints — Consultation](#9-endpoints--consultation)
10. [Endpoints — Gestion](#10-endpoints--gestion)
11. [Endpoints — RGPD](#11-endpoints--rgpd)
12. [Endpoints — Platform Config](#12-endpoints--platform-config)
13. [Endpoints — Statistiques](#13-endpoints--statistiques)
14. [Flux inter-services](#14-flux-inter-services)
15. [Troubleshooting](#15-troubleshooting)
16. [Commandes utiles](#16-commandes-utiles)

---

## 1. Rôle du service

Le service Média est la **brique de gestion centralisée des fichiers** de l'écosystème AGT. Il est **générique** : il ne connaît pas le contexte métier. C'est la plateforme consommatrice qui donne du sens aux fichiers via les métadonnées.

**Ce que Media fait :**
- Upload de fichiers (simple, batch jusqu'à 10 fichiers, depuis URL externe)
- Validation du type MIME et de la taille selon la configuration de la plateforme
- Calcul du hash SHA-256 pour garantir l'intégrité des fichiers
- Traitement asynchrone via BullMQ : compression et génération de thumbnails (Sharp)
- Contrôle d'accès : fichiers publics ou privés avec URLs signées temporaires
- Logs d'accès complets sur chaque téléchargement
- Purge RGPD : suppression totale de tous les fichiers d'un utilisateur

**Ce que Media ne fait PAS :**
- Gérer les utilisateurs → c'est le rôle du service Users
- Authentifier → c'est le rôle du service Auth
- Envoyer des notifications → c'est le rôle du service Notification
- Appliquer des règles métier des plateformes → chaque plateforme configure Media via l'API

---

## 2. Prérequis

Avant de lancer le service Media, les éléments suivants doivent être disponibles :

- Docker Desktop ou Docker Engine + Docker Compose (version 24+)
- Le service **Auth** doit tourner sur le port 7000 (Media en dépend pour valider les JWT)
- Le réseau Docker `agt_network` doit exister (créé automatiquement par `deploy_mvp.ps1`)

Vérification du réseau :
```bash
docker network ls | grep agt_network
```

Si le réseau n'existe pas :
```bash
docker network create agt_network
```

---

## 3. Lancer le service localement

### 3.1 Cloner et préparer le .env

```bash
cd AGT-SERVICES/agt-media
cp .env.example .env
```

Ouvre `.env` et remplis au minimum les champs S2S (voir section 5 pour les obtenir) :
```env
S2S_CLIENT_ID=<uuid obtenu depuis Auth>
S2S_CLIENT_SECRET=<secret obtenu depuis Auth>
SIGNED_URL_SECRET=<une chaîne secrète de ton choix, min 32 caractères>
```

### 3.2 Démarrer les containers

```bash
docker compose up -d --build
```

Cela lance 3 containers :
- `agt-media-service` → le service NestJS sur le port 7003
- `agt-media-db` → PostgreSQL dédié au service
- `agt-media-redis` → Redis dédié (cache + BullMQ)

### 3.3 Vérifier que tout tourne

```bash
docker compose ps
```

Les 3 containers doivent être en état `Up (healthy)`.

### 3.4 Migrations

Les migrations sont appliquées **automatiquement au démarrage** via TypeORM `synchronize: true` en développement. Les 5 tables suivantes sont créées automatiquement :
- `media_files`
- `media_variants`
- `media_metadata`
- `media_access_logs`
- `platform_media_configs`

> **En production**, désactiver `synchronize` et utiliser les migrations TypeORM :
> ```bash
> docker exec agt-media-service npm run migration:run
> ```

### 3.5 Vérifier le health check

```bash
curl http://localhost:7003/api/v1/media/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "service": "agt-media",
  "version": "1.0.0",
  "database": "ok",
  "timestamp": "2026-04-17T07:28:09.737Z"
}
```

### 3.6 Accéder au Swagger

```
http://localhost:7003/api/v1/docs
```

---

## 4. Variables d'environnement

| Variable | Description | Exemple |
|---|---|---|
| `NODE_ENV` | Environnement | `development` |
| `PORT` | Port d'écoute | `7003` |
| `DATABASE_URL` | URL PostgreSQL | `postgresql://media_user:media_pass@agt-media-db:5432/media_db` |
| `REDIS_URL` | URL Redis | `redis://agt-media-redis:6379` |
| `AUTH_SERVICE_URL` | URL du service Auth | `http://agt-auth-service:7000/api/v1` |
| `S2S_AUTH_URL` | URL Auth pour les tokens S2S | `http://agt-auth-service:7000/api/v1` |
| `S2S_CLIENT_ID` | UUID de la plateforme S2S Media | `f086243c-7969-40be-afe0-de89e4b6a31a` |
| `S2S_CLIENT_SECRET` | Secret de la plateforme S2S Media | `G2wJL1263X5...` |
| `STORAGE_PROVIDER` | Provider de stockage | `local` (MVP), `s3` (prod) |
| `LOCAL_STORAGE_PATH` | Dossier de stockage local | `/app/uploads` |
| `SIGNED_URL_SECRET` | Secret HMAC pour les URLs signées | `agt-media-secret-32chars` |
| `MAX_FILE_SIZE_BYTES` | Taille max d'upload (défaut 50 MB) | `52428800` |
| `THUMBNAIL_SIZES` | Tailles de thumbnails générés | `150x150,300x300` |
| `COMPRESSION_QUALITY` | Qualité de compression JPEG (1-100) | `80` |

> **Important :** `REDIS_URL` doit pointer vers `agt-media-redis` (le Redis dédié au service Media), pas vers `agt-redis` (Redis partagé). Utiliser le mauvais Redis provoque une erreur `getaddrinfo EAI_AGAIN`.

---

## 5. Créer la plateforme S2S dans Auth

Le service Media doit avoir une identité S2S dans Auth pour appeler les autres services. Cette étape est à faire **une seule fois** lors du premier déploiement.

### 5.1 Ouvrir Swagger Auth

```
http://localhost:7000/api/v1/docs
```

### 5.2 Créer la plateforme

Appelle `POST /api/v1/auth/platforms` avec le header admin :

**Header :**
```
X-Admin-API-Key: <valeur de ADMIN_API_KEY dans le .env du service Auth>
```

**Body :**
```json
{
  "name": "AGT Media",
  "slug": "agt-media",
  "allowed_auth_methods": ["email"]
}
```

**Réponse :**
```json
{
  "id": "f086243c-7969-40be-afe0-de89e4b6a31a",
  "client_secret": "G2wJL1263X5uQQw_IwTXe8ZzsxpHw2fhr2bJAkHwg_5c0enjxtB9Fpdu1xeVnTMT"
}
```

### 5.3 Reporter dans le .env

```env
S2S_CLIENT_ID=f086243c-7969-40be-afe0-de89e4b6a31a
S2S_CLIENT_SECRET=G2wJL1263X5uQQw_IwTXe8ZzsxpHw2fhr2bJAkHwg_5c0enjxtB9Fpdu1xeVnTMT
```

### 5.4 Rebuilder le service

```bash
docker compose up -d --build
```

---

## 6. Obtenir un token pour tester

Le service Media requiert un token JWT valide sur tous ses endpoints (sauf `/health` et `/:id/serve`).

### 6.1 Token utilisateur (pour les endpoints standards)

Sur Swagger Auth (`http://localhost:7000/api/v1/docs`) :

```
POST /api/v1/auth/login
Body: { "email": "ton@email.com", "password": "tonmotdepasse" }
```

Copie le champ `access_token` de la réponse.

### 6.2 Token S2S (pour les endpoints restreints)

Certains endpoints nécessitent un **token S2S** : hard delete, purge RGPD, et configuration plateforme. Un token utilisateur classique sera rejeté avec `403` sur ces endpoints.

Sur Swagger Auth :

```
POST /api/v1/auth/s2s/token
Body: {
  "client_id": "<S2S_CLIENT_ID>",
  "client_secret": "<S2S_CLIENT_SECRET>"
}
```

### 6.3 Autoriser sur Swagger Media

1. Ouvre `http://localhost:7003/api/v1/docs`
2. Clique sur **Authorize** en haut à droite
3. Entre : `Bearer <ton_token>`
4. Clique **Authorize**

> **Important :** Les tokens JWT ont une durée de vie limitée (généralement 1 heure). Si tu obtiens une erreur `500` avec `platform_id null` dans les logs, c'est que ton token a expiré. Renouvelle-le via Auth et re-autorise sur Swagger Media en cliquant d'abord sur **Logout** puis en entrant le nouveau token.

---

## 7. Endpoints — Health

### `GET /api/v1/media/health`

**Rôle :** Vérifie que le service et sa base de données sont opérationnels. Endpoint public, aucun token requis.

**Authentification :** Aucune

**Réponse (200) :**
```json
{
  "status": "healthy",
  "service": "agt-media",
  "version": "1.0.0",
  "database": "ok",
  "timestamp": "2026-04-17T07:28:09.737Z"
}
```

Si `database` vaut `error`, le container PostgreSQL `agt-media-db` est injoignable.

---

## 8. Endpoints — Upload

### `POST /api/v1/media`

**Rôle :** Upload d'un fichier unique. Le service valide le type MIME et la taille, calcule le hash SHA-256, stocke le fichier, et enqueue un job BullMQ pour le traitement asynchrone (thumbnails + compression pour les images).

**Authentification :** Token Bearer (utilisateur ou S2S)

**Content-Type :** `multipart/form-data`

**Champs du body :**

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `file` | fichier binaire | ✅ | Le fichier à uploader |
| `visibility` | `public` ou `private` | ❌ | Défaut : `public` |
| `owner_user_id` | UUID | ❌ | UUID du propriétaire métier du fichier (voir note ci-dessous) |
| `metadata` | JSON string | ❌ | Métadonnées clé-valeur libres |

> **Note sur `owner_user_id` :** Ce champ permet de distinguer *qui uploade* (`uploaded_by`, extrait automatiquement du JWT) de *pour qui est ce fichier* (`owner_user_id`, fourni explicitement). Exemple : le service Users uploade en S2S la photo de profil d'un utilisateur → `uploaded_by = null` (S2S), `owner_user_id = UUID de l'utilisateur`. Pour un upload direct par l'utilisateur, les deux peuvent être identiques. Ce champ est purement une métadonnée métier, il n'a aucun impact sur la sécurité.
>
> **Dans Swagger :** décoche "Send empty value" sur `owner_user_id` si tu ne veux pas le renseigner, sinon tu obtiendras une erreur `400 owner_user_id must be a UUID`.

**Réponse (201) :**
```json
{
  "success": true,
  "data": {
    "id": "831924c9-120b-44e9-acd9-ad37ba9a0928",
    "original_name": "photo.png",
    "mime_type": "image/png",
    "size_bytes": 182710,
    "sha256_hash": "165cfe9f...",
    "storage_key": "262528c7-26d0.../2026/04/831924c9....png",
    "visibility": "public",
    "platform_id": "262528c7-26d0-4df2-adc8-b2b01494f91d",
    "uploaded_by": "user-uuid-ou-null-si-s2s",
    "owner_user_id": null,
    "width": null,
    "height": null,
    "url": "/api/v1/media/831924c9-.../serve?...",
    "signed_url": null,
    "created_at": "2026-04-17T08:06:19.785Z",
    "updated_at": "2026-04-17T08:06:19.785Z"
  }
}
```

> **Note sur `url` :** L'URL retournée est relative (ex: `/api/v1/media/...`). Le client doit préfixer avec l'adresse du backend selon son environnement (`http://localhost:7003` en dev, `https://api.mondomaine.com` en prod). Ce comportement est intentionnel pour éviter de coder en dur l'adresse du serveur.

> **Note sur `width` / `height` :** Ces champs sont `null` immédiatement après l'upload car le traitement est asynchrone. Attends 2-3 secondes puis appelle `GET /{id}/info` pour voir les dimensions et les thumbnails générés.

---

### `POST /api/v1/media/batch`

**Rôle :** Upload de plusieurs fichiers en une seule requête (maximum 10). Chaque fichier est traité indépendamment — certains peuvent réussir et d'autres échouer dans la même requête.

**Authentification :** Token Bearer (utilisateur ou S2S)

**Content-Type :** `multipart/form-data`

**Champs du body :**

| Champ | Type | Description |
|---|---|---|
| `files` | tableau de fichiers | Les fichiers à uploader (max 10) |
| `visibility` | `public` ou `private` | Appliqué à tous les fichiers |
| `owner_user_id` | UUID | Optionnel, appliqué à tous les fichiers |

**Réponse (207 Multi-Status) :**
```json
{
  "results": [
    { "status": 201, "data": { "id": "uuid-1", ... } },
    { "status": 201, "data": { "id": "uuid-2", ... } },
    { "status": 422, "error": "Type MIME non autorise: application/exe" }
  ]
}
```

Le code `207` signifie que chaque fichier a son propre statut. Un `201` par fichier = succès, un `422` = échec pour ce fichier uniquement.

---

### `POST /api/v1/media/from-url`

**Rôle :** Importe un fichier directement depuis une URL externe. Le service télécharge lui-même le fichier, le valide et le stocke comme un upload normal. Utile pour importer des ressources depuis internet sans passer par le client.

**Authentification :** Token Bearer (utilisateur ou S2S)

**Body JSON :**
```json
{
  "url": "https://example.com/image.jpg",
  "visibility": "public",
  "owner_user_id": "uuid-optionnel",
  "metadata": { "source": "import", "campaign": "summer" }
}
```

**Sécurité SSRF intégrée :** Les URLs suivantes sont bloquées pour éviter les attaques SSRF :
- `localhost`, `127.0.0.1`, `::1`
- Plages IP privées : `10.*`, `172.16-31.*`, `192.168.*`
- IP metadata cloud : `169.254.169.254` (AWS/GCP/Azure)

Si l'URL externe retourne un `403`, c'est que le serveur cible refuse les téléchargements automatiques (ex: Wikipédia). Utilise une URL qui accepte les requêtes HTTP directes.

**Réponse (201) :** Même structure que l'upload simple.

---

## 9. Endpoints — Consultation

### `GET /api/v1/media/{id}`

**Rôle :** Télécharge le fichier binaire brut. Chaque appel est enregistré dans les logs d'accès (`media_access_logs`).

**Authentification :** Token Bearer

**Paramètre :** `id` = UUID du fichier

**Réponse :** Le fichier binaire avec les headers `Content-Type` et `Content-Disposition` appropriés.

---

### `GET /api/v1/media/{id}/info`

**Rôle :** Retourne les métadonnées complètes d'un fichier en JSON : dimensions, variants (thumbnails), métadonnées custom, dates. Ne télécharge pas le fichier binaire.

**Authentification :** Token Bearer

**Réponse (200) :**
```json
{
  "success": true,
  "data": {
    "id": "831924c9-...",
    "original_name": "photo.png",
    "mime_type": "image/png",
    "size_bytes": "182710",
    "width": 1920,
    "height": 1080,
    "visibility": "public",
    "variants": [
      {
        "id": "99ca4adc-...",
        "variant_type": "thumbnail",
        "width": 150,
        "height": 150,
        "storage_key": "..._thumb_150x150.png",
        "size_bytes": "2833",
        "created_at": "2026-04-17T08:06:20.031Z"
      },
      {
        "id": "f85030a0-...",
        "variant_type": "thumbnail",
        "width": 300,
        "height": 300,
        "storage_key": "..._thumb_300x300.png",
        "size_bytes": "8188",
        "created_at": "2026-04-17T08:06:20.181Z"
      }
    ],
    "metadata": [
      { "key": "category", "value": "profile" },
      { "key": "source", "value": "mobile" }
    ]
  }
}
```

> **Note :** Si `variants` est vide immédiatement après l'upload, c'est normal — le traitement est asynchrone. Attends 2-3 secondes et rappelle cet endpoint.

---

### `GET /api/v1/media/{id}/thumbnails`

**Rôle :** Retourne la liste JSON de tous les thumbnails générés pour un fichier, avec leurs dimensions et storage keys. Ne retourne pas le fichier binaire.

**Authentification :** Token Bearer

**Réponse (200) :**
```json
{
  "success": true,
  "data": [
    { "id": "...", "variant_type": "thumbnail", "width": 150, "height": 150, ... },
    { "id": "...", "variant_type": "thumbnail", "width": 300, "height": 300, ... }
  ]
}
```

---

### `GET /api/v1/media/{id}/thumbnail/{size}`

**Rôle :** Télécharge le fichier binaire d'un thumbnail spécifique par sa taille. Utile pour afficher des prévisualisations légères sans télécharger le fichier original.

**Authentification :** Token Bearer

**Paramètres :**
- `id` = UUID du fichier
- `size` = taille au format `WxH` (ex: `150x150`, `300x300`)

**Réponse :** Le fichier image binaire du thumbnail.

---

### `GET /api/v1/media/{id}/resize`

**Rôle :** Redimensionne une image à la volée aux dimensions exactes demandées. Contrairement aux thumbnails (tailles fixes prédéfinies), le resize accepte n'importe quelle dimension entre 1 et 4000 pixels. Le résultat est mis en cache Redis automatiquement.

**Authentification :** Token Bearer

**Query params :**
- `w` (obligatoire) : largeur cible en pixels
- `h` (obligatoire) : hauteur cible en pixels
- `crop` (optionnel, défaut `false`) : `true` = recadre exactement, `false` = conserve les proportions

**Exemple :**
```
GET /api/v1/media/831924c9-.../resize?w=500&h=300&crop=false
```

**Réponse :** L'image binaire redimensionnée avec header `Cache-Control: public, max-age=3600`.

---

### `GET /api/v1/media/{id}/signed-url`

**Rôle :** Génère une URL temporaire signée pour accéder à un fichier privé sans token Bearer. L'URL contient une signature HMAC SHA-256 et une date d'expiration. Personne ne peut fabriquer une fausse URL signée sans connaître le `SIGNED_URL_SECRET`.

**Authentification :** Token Bearer

**Query params :**
- `expires` (optionnel, défaut `3600`) : durée de validité en secondes

**Réponse (200) :**
```json
{
  "success": true,
  "data": {
    "signed_url": "/api/v1/media/831924c9-.../serve?sig=775822a1...&exp=1776417149",
    "expires_in": 3600
  }
}
```

L'URL retournée est relative — préfixe avec l'adresse du backend pour l'utiliser.

---

### `GET /api/v1/media/{id}/serve`

**Rôle :** Sert le fichier binaire via une URL signée. C'est le seul endpoint **public** du service — aucun token Bearer requis. La sécurité repose uniquement sur la signature HMAC et la date d'expiration.

**Authentification :** Aucune (public)

**Query params :**
- `sig` : la signature HMAC (obtenue depuis `GET /signed-url`)
- `exp` : le timestamp d'expiration Unix (obtenu depuis `GET /signed-url`)

**Erreurs possibles :**
- `410 Gone` → l'URL a expiré
- `403 Forbidden` → la signature est invalide ou falsifiée

**Usage :** Génère d'abord une URL signée via `GET /{id}/signed-url`, puis utilise les paramètres `sig` et `exp` retournés pour appeler cet endpoint.

---

### `GET /api/v1/media/{id}/access-logs`

**Rôle :** Retourne l'historique paginé de tous les accès à un fichier : qui a téléchargé, depuis quelle IP, à quelle heure, et quelle action a été effectuée (`download`, `signed_url`).

**Authentification :** Token Bearer

**Query params :**
- `page` (défaut `1`)
- `limit` (défaut `50`)

**Réponse (200) :**
```json
{
  "data": [
    {
      "id": 3,
      "media_id": "831924c9-...",
      "accessed_by": "user-uuid-ou-null",
      "ip_address": "192.168.1.1",
      "action": "download",
      "created_at": "2026-04-17T08:14:54.639Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 50
}
```

---

### `GET /api/v1/media`

**Rôle :** Liste paginée de tous les fichiers avec filtres optionnels. C'est l'endpoint principal pour explorer et rechercher des médias.

**Authentification :** Token Bearer

**Query params (tous optionnels) :**

| Paramètre | Description |
|---|---|
| `platform_id` | Filtrer par plateforme |
| `uploaded_by` | Filtrer par uploader (UUID) |
| `owner_user_id` | Filtrer par propriétaire (UUID) |
| `mime_type` | Filtrer par type MIME (ex: `image/png`) |
| `visibility` | `public` ou `private` |
| `from` | Date de début ISO8601 (ex: `2026-01-01T00:00:00Z`) |
| `to` | Date de fin ISO8601 |
| `page` | Numéro de page (défaut `1`) |
| `limit` | Résultats par page (défaut `20`, max `100`) |

**Réponse (200) :**
```json
{
  "data": [ { "id": "...", ... }, { "id": "...", ... } ],
  "total": 2,
  "page": 1,
  "limit": 20
}
```

> **Note :** Les fichiers supprimés (`deleted_at` non null) n'apparaissent jamais dans cette liste.

---

## 10. Endpoints — Gestion

### `PUT /api/v1/media/{id}/metadata`

**Rôle :** Met à jour les métadonnées personnalisées d'un fichier sous forme de clés-valeurs libres. Le service Media est générique — les métadonnées permettent aux plateformes consommatrices de donner du sens à leurs fichiers.

**Authentification :** Token Bearer

**Attention :** Cet endpoint **remplace entièrement** les métadonnées existantes — ce n'est pas un merge. Si tu veux conserver des clés existantes, inclus-les dans le nouveau body.

**Body :**
```json
{
  "metadata": {
    "category": "profile",
    "source": "mobile"
  }
}
```

Exemples de cas d'usage des métadonnées :
- Photo de profil : `{"type": "avatar", "user_type": "premium"}`
- Document KYC : `{"document_type": "passport", "status": "pending", "country": "CM"}`
- Fichier marketing : `{"campaign": "summer-2026", "format": "banner", "language": "fr"}`

**Réponse (200) :** Le fichier complet avec les nouvelles métadonnées.

---

### `PUT /api/v1/media/{id}/visibility`

**Rôle :** Change la visibilité d'un fichier entre `public` et `private` après son upload.

- `public` → accessible directement via URL, sans token
- `private` → accessible uniquement via URL signée temporaire ou avec un token Bearer valide

**Authentification :** Token Bearer

**Body :**
```json
{
  "visibility": "private"
}
```

**Réponse (200) :** Le fichier complet avec la nouvelle visibilité.

---

### `DELETE /api/v1/media/{id}`

**Rôle :** Suppression douce (soft delete) du fichier. Le fichier n'est pas supprimé physiquement — le champ `deleted_at` est simplement renseigné avec la date actuelle. Le fichier disparaît de tous les listings mais reste en base de données, permettant une restauration si nécessaire.

**Authentification :** Token Bearer

**Réponse :** `204 No Content` (pas de body)

> Pour vérifier que le soft delete a fonctionné : appelle `GET /api/v1/media` — le fichier ne doit plus apparaître dans la liste.

---

### `DELETE /api/v1/media/{id}/permanent`

**Rôle :** Suppression physique et **définitive** du fichier. Supprime le fichier du stockage disque ET toutes ses entrées en base de données (variants, métadonnées, logs d'accès). **Irréversible.**

**Authentification :** Token S2S uniquement — un token utilisateur sera rejeté avec `403`.

**Réponse :** `204 No Content` (pas de body)

> Pour obtenir un token S2S, voir la section [6.2](#62-token-s2s-pour-les-endpoints-restreints).

---

## 11. Endpoints — RGPD

### `DELETE /api/v1/media/by-user/{userId}`

**Rôle :** Supprime définitivement et totalement tous les fichiers appartenant à un utilisateur (`uploaded_by = userId` OU `owner_user_id = userId`), ainsi que toutes leurs variantes, métadonnées et logs d'accès. C'est l'implémentation du **droit à l'effacement RGPD**.

En pratique, c'est le service Users qui appelle cet endpoint en S2S lors de la suppression d'un compte utilisateur.

**Authentification :** Token S2S uniquement — un token utilisateur sera rejeté avec `403`.

**Paramètre :** `userId` = UUID de l'utilisateur (`users_auth.id`)

**Réponse (200) :**
```json
{
  "files_deleted": 15,
  "variants_deleted": 42,
  "storage_freed_bytes": 52428800
}
```

> **Note :** Si les compteurs retournent `0`, c'est que les fichiers ont été uploadés sans `owner_user_id` ni `uploaded_by` correspondant à cet UUID. Vérifier que les uploads ont bien été faits avec le bon `owner_user_id`.

---

## 12. Endpoints — Platform Config

### `GET /api/v1/platforms/{platformId}/media-config`

**Rôle :** Retourne la configuration Media personnalisée d'une plateforme : types autorisés, tailles max, thumbnails, compression, quota. Si aucune configuration n'a été créée, retourne `null` et le service utilise les valeurs par défaut du `.env`.

**Authentification :** Token Bearer

**Réponse (200) :**
```json
{
  "success": true,
  "data": {
    "platform_id": "262528c7-...",
    "allowed_types": ["image/jpeg", "image/png", "application/pdf"],
    "max_size_bytes": { "image": 10485760, "document": 52428800 },
    "thumbnail_sizes": ["150x150", "300x300"],
    "compression_quality": 80,
    "storage_quota_bytes": null,
    "created_at": "2026-04-17T08:48:00.001Z",
    "updated_at": "2026-04-17T08:51:45.076Z"
  }
}
```

---

### `PUT /api/v1/platforms/{platformId}/media-config`

**Rôle :** Crée ou met à jour (upsert) la configuration Media d'une plateforme. Permet de personnaliser les règles d'upload par plateforme : types autorisés, tailles max, thumbnails, compression, quota de stockage.

**Authentification :** Token S2S uniquement.

**Body :**
```json
{
  "allowed_types": ["image/jpeg", "image/png", "application/pdf"],
  "max_size_bytes": { "image": 10485760, "document": 52428800 },
  "thumbnail_sizes": ["150x150", "300x300"],
  "compression_quality": 80,
  "storage_quota_bytes": null
}
```

Description des champs :

| Champ | Description |
|---|---|
| `allowed_types` | Liste des types MIME autorisés pour cette plateforme |
| `max_size_bytes` | Taille max en octets par catégorie (`image`, `document`, etc.) |
| `thumbnail_sizes` | Tailles de thumbnails à générer au format `WxH` |
| `compression_quality` | Qualité de compression JPEG (1-100) |
| `storage_quota_bytes` | Quota total en octets (`null` = illimité) |

**Réponse (200) :** La configuration complète mise à jour.

---

## 13. Endpoints — Statistiques

### `GET /api/v1/media/stats`

**Rôle :** Retourne les statistiques globales sur tous les fichiers stockés : nombre total, espace utilisé, répartition par type MIME. Utile pour un dashboard d'administration.

**Authentification :** Token Bearer

**Réponse (200) :**
```json
{
  "total_files": 5,
  "total_size_bytes": 1204754,
  "by_mime_type": [
    { "mime_type": "image/png", "count": "4" },
    { "mime_type": "image/jpeg", "count": "1" }
  ],
  "platform_id": "all"
}
```

---

### `GET /api/v1/media/stats/{platformId}`

**Rôle :** Mêmes statistiques que ci-dessus mais filtrées pour une plateforme spécifique. Dans un contexte multi-tenant, chaque plateforme peut consulter uniquement son propre usage.

**Authentification :** Token Bearer

**Paramètre :** `platformId` = UUID de la plateforme

**Réponse (200) :** Même structure que les stats globales avec `platform_id` renseigné.

---

## 14. Flux inter-services

### Media ← Users (upload avatar / KYC)

```
Users (token S2S) ──POST /api/v1/media──▶ Media
  body: {
    file: <binaire>,
    owner_user_id: <users_auth.id>,
    visibility: "private",
    metadata: { "type": "avatar" }
  }

Media ──▶ { id: "media-uuid", ... }

Users stocke avatar_media_id = "media-uuid" dans users_profiles
```

### Media ← Users (purge RGPD)

```
Users (token S2S) ──DELETE /api/v1/media/by-user/{userId}──▶ Media
Media supprime tous les fichiers de cet utilisateur
Media ──▶ { files_deleted: N, variants_deleted: M, storage_freed_bytes: X }
```

### Media → Auth (validation JWT)

```
Client ──GET /api/v1/media/{id}/info──▶ Media
Media ──GET /auth/verify-token──▶ Auth  (pour token utilisateur)
        OU
Media ──POST /auth/s2s/introspect──▶ Auth  (pour token S2S)
Auth ──▶ payload JWT validé
```

### Flux d'upload complet

```
Client ──POST /api/v1/media (multipart)──▶ MediaController
  ↓
MediaService.uploadFile()
  1. Validation MIME + taille
  2. Calcul SHA-256
  3. Stockage fichier (LocalStorageProvider)
  4. INSERT media_files
  5. BullMQ.add('process-media', job)
  ↓ (réponse immédiate au client)
  6. MediaProcessor.process(job) — asynchrone
     a. Sharp → extraction dimensions (width, height)
     b. Sharp → génération thumbnails 150x150, 300x300
     c. Sharp → compression si gain > 10%
     d. UPDATE media_files (width, height)
     e. INSERT media_variants
```

---

## 15. Troubleshooting

### Erreur 500 avec `platform_id null` dans les logs

**Cause :** Le token Bearer a expiré. Swagger vide silencieusement le token après expiration, et `req.auth` devient `undefined`, ce qui rend `platform_id` null.

**Solution :**
1. Obtenir un nouveau token sur Auth Swagger (`POST /api/v1/auth/login`)
2. Sur Media Swagger, cliquer **Authorize** → **Logout** → entrer le nouveau token
3. Retester l'endpoint

---

### Les thumbnails apparaissent plusieurs fois dans `GET /{id}/info`

**Cause :** Le worker BullMQ rejouait les jobs sans vérifier l'idempotence — bug corrigé dans la version actuelle avec la vérification d'existence avant insertion.

**Solution :** Rebuilder le service avec le code corrigé :
```bash
docker compose up -d --build
```

---

### `GET /{id}/thumbnails` retourne un tableau vide

**Cause :** Le traitement est asynchrone — les thumbnails ne sont pas encore générés.

**Solution :** Attendre 2-5 secondes après l'upload et rappeler `GET /{id}/info`. Si toujours vide après 30 secondes :
```bash
docker compose logs agt-media-service | grep "Traitement\|Erreur"
```

---

### Erreur SSRF sur `POST /from-url`

**Cause :** L'URL fournie pointe vers un réseau privé ou le serveur cible refuse les requêtes automatiques (403).

**Solution :** Utiliser uniquement des URLs HTTP/HTTPS publiques qui acceptent les téléchargements directs. Tester d'abord avec `curl <url>` pour vérifier que l'URL est accessible.

---

### Hard delete ou purge RGPD retourne 403

**Cause :** Ces endpoints nécessitent un token S2S. Un token utilisateur classique est rejeté.

**Solution :** Obtenir un token S2S via `POST /api/v1/auth/s2s/token` avec les `client_id` et `client_secret` du service Media.

---

### `PUT /{id}/metadata` retourne 500 avec `Cannot convert undefined or null to object`

**Cause :** Le champ `metadata` est envoyé vide ou `null`. Bug corrigé dans la version actuelle avec une validation `@IsObject()` sur le DTO.

**Solution :** S'assurer d'envoyer un objet non vide dans `metadata` :
```json
{ "metadata": { "key": "value" } }
```

---

### `PUT /platforms/{platformId}/media-config` sauvegarde des champs vides

**Cause :** Le DTO `UpsertConfigDto` n'avait pas de décorateurs de validation — le `ValidationPipe` global filtrait les champs. Bug corrigé dans la version actuelle.

**Solution :** Rebuilder le service avec le code corrigé.

---

### Le container `agt-media-service` ne démarre pas avec `Cannot find module '/app/dist/main'`

**Cause :** `nest build` génère `dist/src/main.js` mais la commande Docker cherchait `dist/main.js`.

**Solution :** Vérifier que le `Dockerfile` contient bien :
```dockerfile
CMD ["node", "dist/src/main"]
```

---

### Erreur `getaddrinfo EAI_AGAIN agt-redis`

**Cause :** Le `.env` pointait vers `agt-redis` (Redis partagé) au lieu de `agt-media-redis` (Redis dédié au service Media).

**Solution :** Vérifier que dans `.env` :
```env
REDIS_URL=redis://agt-media-redis:6379
```

---

## 16. Commandes utiles

```bash
# Démarrer le service (build + run)
cd AGT-SERVICES/agt-media
docker compose up -d --build

# Démarrer sans rebuild (plus rapide si pas de changement de code)
docker compose up -d

# Arrêter le service (conserve les données)
docker compose down

# Arrêter et supprimer les volumes (repart de zéro — supprime la DB)
docker compose down -v

# Voir les logs en temps réel
docker compose logs -f agt-media-service

# Voir les 50 dernières lignes de logs
docker compose logs --tail=50 agt-media-service

# Vérifier l'état des containers
docker compose ps

# Accéder au shell du container
docker exec -it agt-media-service sh

# Lancer les tests unitaires et d'intégration
docker exec agt-media-service npx jest --config jest.config.js --no-coverage

# Accéder directement à la base de données
docker exec -it agt-media-db psql -U media_user -d media_db

# Health check rapide
curl http://localhost:7003/api/v1/media/health

# Swagger UI
open http://localhost:7003/api/v1/docs
```

---

*AG Technologies — Confidentiel — Usage interne*
*Guide rédigé après tests complets en conditions réelles — Avril 2026*