# GUIDE_MEDIA — Service Média AGT

> **Version :** 1.0.0  
> **Port :** 7003  
> **Stack :** Node.js 20 / NestJS / TypeORM / PostgreSQL / Redis / BullMQ / Sharp  
> **CDC de référence :** `docs/cdc/4.medias.txt` v1.4  

---

## Table des matières

1. [Rôle du service](#1-rôle-du-service)
2. [Lancer le service localement](#2-lancer-le-service-localement)
3. [Variables d'environnement](#3-variables-denvironnement)
4. [Créer la plateforme S2S](#4-créer-la-plateforme-s2s)
5. [Endpoints principaux](#5-endpoints-principaux)
6. [Flux inter-services](#6-flux-inter-services)
7. [Tests](#7-tests)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Rôle du service

Le service Média est la **brique de gestion centralisée des fichiers** de l'écosystème AGT. Il est **générique** : il ne connaît pas le contexte métier. C'est la plateforme consommatrice qui donne du sens aux fichiers via les métadonnées.

**Ce que Media fait :**
- Upload (simple, batch, depuis URL externe)
- Validation type MIME + taille selon config par plateforme
- Calcul hash SHA-256 pour intégrité
- Traitement asynchrone via BullMQ : compression + thumbnails (Sharp)
- Accès public/privé + URLs signées temporaires
- Logs d'accès complets
- Purge RGPD (suppression totale par utilisateur)

**Ce que Media ne fait PAS :**
- Gérer les utilisateurs → Users Service
- Authentifier → Auth Service
- Envoyer des notifications → Notification Service
- Appliquer des règles métier des plateformes

---

## 2. Lancer le service localement

### Prérequis

- Docker + Docker Compose
- Le réseau `agt_network` doit exister : `docker network create agt_network`
- Auth Service (:7000) doit être opérationnel pour la validation JWT

### Démarrage

```bash
cd agt-media

# 1. Copier le fichier de configuration
cp .env.example .env
# Éditer .env avec vos valeurs (S2S_CLIENT_ID, S2S_CLIENT_SECRET, etc.)

# 2. Lancer le service + sa base PostgreSQL
docker compose up -d --build

# 3. Vérifier que le service est sain
curl http://localhost:7003/api/v1/media/health
```

**Réponse attendue :**
```json
{
  "status": "healthy",
  "service": "agt-media",
  "version": "1.0.0",
  "database": "ok",
  "timestamp": "2026-04-16T10:00:00.000Z"
}
```

### Swagger UI (documentation interactive)

```
http://localhost:7003/api/v1/docs
```

Cliquer sur **Authorize** et entrer :
```
Bearer <votre_token_jwt>
```

---

## 3. Variables d'environnement

| Variable | Obligatoire | Description | Défaut |
|---|---|---|---|
| `PORT` | Non | Port d'écoute | `7003` |
| `DATABASE_URL` | **Oui** | URL PostgreSQL | — |
| `REDIS_URL` | **Oui** | URL Redis | — |
| `AUTH_SERVICE_URL` | **Oui** | URL du service Auth | `http://agt-auth-service:7000/api/v1` |
| `S2S_AUTH_URL` | **Oui** | URL Auth pour S2S | `http://agt-auth-service:7000/api/v1` |
| `S2S_CLIENT_ID` | **Oui** | ID plateforme S2S dans Auth | — |
| `S2S_CLIENT_SECRET` | **Oui** | Secret plateforme S2S | — |
| `STORAGE_PROVIDER` | Non | `local` / `s3` / `gcs` | `local` |
| `LOCAL_STORAGE_PATH` | Non | Chemin stockage local | `/app/uploads` |
| `SIGNED_URL_SECRET` | **Oui** | Clé HMAC pour URLs signées | — |
| `MAX_FILE_SIZE_BYTES` | Non | Taille max upload | `52428800` (50 MB) |
| `COMPRESSION_QUALITY` | Non | Qualité JPEG Sharp (1-100) | `80` |
| `THUMBNAIL_SIZES` | Non | Tailles thumbnails | `150x150,300x300` |

---

## 4. Créer la plateforme S2S

Avant de lancer Media en production, créer sa plateforme S2S dans Auth.

### 4.1 Créer la plateforme

Dans Swagger Auth (`http://localhost:7000/api/v1/docs`), appeler `POST /api/v1/auth/platforms` :

**Header :**
```
X-Admin-API-Key: change-me-admin-api-key-very-secret
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
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "client_secret": "xxxxxxxxxxxxxxxxxxxxx"
}
```

### 4.2 Configurer le .env

```env
S2S_CLIENT_ID=<id retourné>
S2S_CLIENT_SECRET=<client_secret retourné>
```

### 4.3 Redémarrer le service

```bash
docker compose up -d --build agt-media-service
```

---

## 5. Endpoints principaux

### 5.1 Health Check

```bash
GET /api/v1/media/health
```
**Aucune authentification requise.**

---

### 5.2 Upload simple

```bash
POST /api/v1/media
Authorization: Bearer <token>
Content-Type: multipart/form-data

file=@/chemin/vers/image.jpg
visibility=public          # optionnel, défaut: private
owner_user_id=<uuid>       # optionnel (si upload pour le compte d'un user)
```

**Réponse (201) :**
```json
{
  "success": true,
  "data": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "original_name": "image.jpg",
    "mime_type": "image/jpeg",
    "size_bytes": 102400,
    "sha256_hash": "a3f5...",
    "storage_key": "platform-uuid/2026/04/3fa85f64.jpg",
    "visibility": "public",
    "platform_id": "platform-uuid",
    "uploaded_by": "user-uuid",
    "created_at": "2026-04-16T10:00:00.000Z"
  }
}
```

> **Note :** le traitement (thumbnails, compression) est asynchrone. Les variantes apparaîtront dans `GET /:id/info` quelques secondes après l'upload.

---

### 5.3 Upload multiple (batch)

```bash
POST /api/v1/media/batch
Authorization: Bearer <token>
Content-Type: multipart/form-data

files=@image1.jpg
files=@image2.png
```

**Réponse (207 Multi-Status) :**
```json
{
  "results": [
    { "status": 201, "data": { "id": "...", ... } },
    { "status": 201, "data": { "id": "...", ... } }
  ]
}
```

---

### 5.4 Import depuis URL

```bash
POST /api/v1/media/from-url
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://example.com/photo.jpg",
  "visibility": "public"
}
```

> **Sécurité SSRF :** les URLs vers `localhost`, `127.0.0.1`, `192.168.*`, `10.*`, `172.*` sont bloquées.

---

### 5.5 Métadonnées d'un fichier

```bash
GET /api/v1/media/{id}/info
Authorization: Bearer <token>
```

**Réponse :**
```json
{
  "success": true,
  "data": {
    "id": "3fa85f64...",
    "original_name": "image.jpg",
    "mime_type": "image/jpeg",
    "size_bytes": 102400,
    "visibility": "public",
    "width": 1920,
    "height": 1080,
    "variants": [
      { "variant_type": "thumbnail", "width": 150, "height": 150, "storage_key": "..." },
      { "variant_type": "thumbnail", "width": 300, "height": 300, "storage_key": "..." },
      { "variant_type": "compressed", "size_bytes": 80000 }
    ],
    "metadata": []
  }
}
```

---

### 5.6 Téléchargement fichier brut

```bash
GET /api/v1/media/{id}
Authorization: Bearer <token>
```

Retourne le fichier binaire avec les headers `Content-Type` et `Content-Disposition` corrects.

---

### 5.7 URL signée temporaire (fichiers privés)

```bash
GET /api/v1/media/{id}/signed-url?expires_in=3600
Authorization: Bearer <token>
```

**Réponse :**
```json
{
  "success": true,
  "data": {
    "signed_url": "/api/v1/media/{id}/serve?sig=abc123&exp=1745000000",
    "expires_in": 3600
  }
}
```

L'URL `/serve` est **publique** (pas de Bearer requis), valide pendant `expires_in` secondes.

---

### 5.8 Changer la visibilité

```bash
PUT /api/v1/media/{id}/visibility
Authorization: Bearer <token>
Content-Type: application/json

{ "visibility": "public" }
```

---

### 5.9 Soft delete

```bash
DELETE /api/v1/media/{id}
Authorization: Bearer <token>
```

Répond **204 No Content**. Le fichier reste physiquement sur le disque, seul `deleted_at` est renseigné.

---

### 5.10 Hard delete — S2S uniquement

```bash
DELETE /api/v1/media/{id}/permanent
Authorization: Bearer <token_s2s>
```

Supprime physiquement le fichier du stockage ET de la base de données. Réservé aux tokens S2S.

---

### 5.11 Purge RGPD — S2S uniquement

```bash
DELETE /api/v1/media/by-user/{userId}
Authorization: Bearer <token_s2s>
```

Supprime **tous** les fichiers d'un utilisateur (où `uploaded_by = userId` OU `owner_user_id = userId`), ainsi que toutes leurs variantes, métadonnées et logs d'accès.

**Réponse :**
```json
{ "deleted_count": 15 }
```

---

### 5.12 Configuration plateforme (S2S)

```bash
# Lire la config
GET /api/v1/platforms/{platformId}/media-config
Authorization: Bearer <token>

# Créer/mettre à jour (upsert)
PUT /api/v1/platforms/{platformId}/media-config
Authorization: Bearer <token_s2s>
Content-Type: application/json

{
  "allowed_types": ["image/jpeg", "image/png", "application/pdf"],
  "max_size_bytes": { "image": 10485760, "document": 52428800 },
  "thumbnail_sizes": ["150x150", "300x300", "600x600"],
  "compression_quality": 85,
  "storage_quota_bytes": 10737418240
}
```

---

### 5.13 Statistiques

```bash
# Stats globales
GET /api/v1/media/stats
Authorization: Bearer <token>

# Stats par plateforme
GET /api/v1/media/stats/{platformId}
Authorization: Bearer <token>
```

---

## 6. Flux inter-services

### Contrat Users → Media (photo de profil / KYC)

```
Users (S2S) ──POST /api/v1/media──▶ Media
   body: { file, owner_user_id: auth_user_id }
   
Media ──▶ retourne { id: "media-uuid" }

Users stocke avatar_media_id = "media-uuid"
L'URL publique est résolue à la lecture via GET /api/v1/media/{id}/info
```

### Contrat Users → Media (purge RGPD)

```
Users (S2S) ──DELETE /api/v1/media/by-user/{userId}──▶ Media
Media supprime tous les fichiers de cet utilisateur
Media ──▶ { deleted_count: N }
```

### Contrat Media → Auth (validation JWT)

```
Client ──GET /api/v1/media/{id}/info──▶ Media
Media ──GET /auth/verify-token──▶ Auth  (JWT user)
        OU
Media ──POST /auth/s2s/introspect──▶ Auth  (token S2S)
Auth ──▶ payload JWT validé
```

---

## 7. Tests

### Lancer les tests

```bash
# Dans le conteneur
docker exec agt-media-service npm test

# En local (si Node.js installé)
npm install
npm test

# Avec coverage
npm run test:cov
```

### Structure des tests

```
test/
├── unit/
│   └── media.service.spec.ts     # Logique métier : upload, validation, RGPD, stats
└── integration/
    └── media.controller.spec.ts  # Endpoints REST : HTTP responses, validations
```

### Ce que les tests couvrent

| Cas testé | Type |
|---|---|
| Upload fichier valide → 201 | Unitaire + Intégration |
| Rejet type MIME non autorisé → 400 | Unitaire |
| Rejet fichier trop volumineux → 400 | Unitaire |
| Pas de traitement pour non-images | Unitaire |
| Accès fichier public sans owner | Unitaire |
| Refus accès privé mauvais user | Unitaire |
| Accès S2S sur fichier privé | Unitaire |
| Soft delete par propriétaire | Unitaire |
| Rejet soft delete non propriétaire | Unitaire |
| Hard delete + suppression stockage | Unitaire |
| Purge RGPD multi-fichiers | Unitaire |
| Stats globales | Unitaire |
| URL signée HMAC valide | Unitaire |
| Liste paginée | Intégration |
| Infos médias | Intégration |
| Thumbnails filtrés | Intégration |
| Visibilité invalide → 400 | Intégration |
| Soft delete → 204 | Intégration |

---

## 8. Troubleshooting

### Le service ne démarre pas

```bash
docker compose logs agt-media-service
```

**Erreur fréquente :** `ECONNREFUSED agt-media-db:5432`  
→ La DB n'est pas encore prête. Attendre quelques secondes, relancer :
```bash
docker compose restart agt-media-service
```

---

### Upload échoue avec 401

Vérifier que :
1. Le token JWT est valide (`Authorization: Bearer <token>`)
2. Auth Service (:7000) est opérationnel
3. `AUTH_SERVICE_URL` pointe correctement vers Auth

---

### Les thumbnails n'apparaissent pas après upload

Le traitement est **asynchrone**. Attendre 2-5 secondes puis rappeler `GET /api/v1/media/{id}/info`.

Si toujours vide :
```bash
# Vérifier les logs du worker BullMQ
docker compose logs agt-media-service | grep "Traitement\|Erreur"
```

---

### Erreur SSRF sur upload from-url

L'endpoint `POST /from-url` bloque les URLs pointant vers des réseaux privés.
Utiliser uniquement des URLs HTTP/HTTPS publiques.

---

### Purge RGPD échoue avec 403

Cet endpoint requiert un **token S2S** (service-to-service).
Un token utilisateur classique sera rejeté même avec les bons rôles.

---

### Commandes utiles

```bash
# Démarrer le service + DB
docker compose up -d --build

# Voir les logs en temps réel
docker compose logs -f agt-media-service

# Accéder au shell du conteneur
docker exec -it agt-media-service sh

# Vérifier la DB directement
docker exec -it agt-media-db psql -U media_user -d media_db

# Arrêter (sans supprimer les données)
docker compose down

# Arrêter ET supprimer les volumes (repart de zéro)
docker compose down -v
```
