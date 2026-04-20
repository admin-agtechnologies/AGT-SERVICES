# GUIDE_SEARCH — AGT Search Service v1.0

> **À qui s'adresse ce guide ?**
> À tout développeur qui rejoint le projet AGT et souhaite comprendre, lancer, tester et intégrer le service Search dans l'écosystème AGT.

---

## Table des matières

1. [Rôle du service](#1-rôle-du-service)
2. [Architecture et conception](#2-architecture-et-conception)
3. [Prérequis — Services à lancer avant Search](#3-prérequis--services-à-lancer-avant-search)
4. [Lancer le service Search](#4-lancer-le-service-search)
5. [Variables d'environnement](#5-variables-denvironnement)
6. [Migrations — étape obligatoire](#6-migrations--étape-obligatoire)
7. [Authentification — obtenir un token](#7-authentification--obtenir-un-token)
8. [Endpoints — référence complète](#8-endpoints--référence-complète)
9. [Flux inter-services](#9-flux-inter-services)
10. [Tests](#10-tests)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Rôle du service

Le **Service Search** est le moteur de recherche unifié et générique de toutes les plateformes AG Technologies. Il encapsule Elasticsearch et n'expose qu'une API REST simple.

**Ce service ne connaît aucun concept métier.** Il gère des index abstraits contenant des documents avec des champs définis dynamiquement par les plateformes consommatrices.

### Ce que fait Search

- Gestion d'index dynamiques (création, suppression, mise à jour du schéma)
- Indexation de documents (unitaire, mise à jour, suppression, bulk)
- Recherche full-text avec scoring, highlighting, fuzzy matching et filtres
- Auto-complétion optimisée (< 50ms)
- Historique de recherche par utilisateur (RGPD)
- Statistiques d'usage (termes populaires, recherches sans résultats)
- Configuration par index (analyzer, fuzzy, highlight)
- Gestion des synonymes par index

### Ce que Search ne fait pas

- Il ne stocke pas les données source (chaque plateforme conserve sa propre base)
- Il ne gère pas l'authentification (déléguée au service Auth)
- Il ne gère pas les rôles et permissions (délégués au service Users)
- Il n'expose jamais Elasticsearch directement aux plateformes

### Port

**Search : 7007**

---

## 2. Architecture et conception

### Schéma général

```
Plateforme A (AGT-Market)          Plateforme B (AGT-Bot)
        |                                   |
        +------------- Search Service ------+
                              |
                      Elasticsearch
                    (moteur de recherche)
                              |
                       PostgreSQL
                    (métadonnées des index)
                              |
                           Redis
                    (cache tokens JWT)
```

### Les 3 couches internes

**PostgreSQL** — La mémoire administrative. Stocke les métadonnées : qui a créé quoi, combien de documents, quelle config, l'historique des recherches. Tables : `index_registry`, `index_schema`, `search_config`, `synonym`, `search_history`, `popular_search`.

**Elasticsearch** — Le vrai moteur de recherche. Stocke les documents et fait la recherche full-text. Chaque index ES est nommé `{platform_id}_{index_name}` pour garantir l'isolation multi-tenant.

**Redis** — Cache les tokens JWT décodés pour éviter de les re-décoder à chaque requête (TTL 30 secondes).

### Isolation multi-tenant

Chaque plateforme est **totalement isolée** des autres. Le `platform_id` est extrait automatiquement du token JWT — jamais du body de la requête. Une plateforme ne peut jamais voir ni toucher les index d'une autre plateforme.

---

## 3. Prérequis — Services à lancer avant Search

Avant de lancer et utiliser le service Search, vous devez avoir les services suivants opérationnels.

### 3.1 Service Auth (:7000) — Obligatoire

Le service Auth est **indispensable**. Il émet les tokens JWT que Search utilise pour authentifier toutes les requêtes. Sans Auth, aucun endpoint de Search n'est utilisable.

> Pour tous les détails sur le lancement et l'utilisation du service Auth, référez-vous au **GUIDE_AUTH.md**.

**Étapes minimales à effectuer sur Auth avant d'utiliser Search :**

**Étape 1 — Lancer Auth**
```bash
cd agt-auth
bash scripts/setup.sh
```
Auth sera disponible sur `http://localhost:7000`.

**Étape 2 — Créer une plateforme de test**

Search s'utilise toujours dans le contexte d'une plateforme. Le `platform_id` de la plateforme sera associé à tous vos index Search.

```
POST http://localhost:7000/api/v1/auth/platforms
Content-Type: application/json

{
  "name": "Ma Plateforme Test",
  "type": "web"
}
```

Notez le `platform_id` retourné dans la réponse.

**Étape 3 — Créer un utilisateur**

```
POST http://localhost:7000/api/v1/auth/register
Content-Type: application/json
X-Platform-Id: <platform_id>

{
  "email": "test@exemple.com",
  "password": "MotDePasse123!",
  "method": "email"
}
```

**Étape 4 — Vérifier l'email** si la vérification est activée, puis passer à la section 7 pour obtenir l'access token.

---

### 3.2 Service Users (:7001) — Recommandé

Le service Users gère les profils utilisateurs. Il n'est pas strictement obligatoire pour utiliser Search seul, mais il est nécessaire dans l'écosystème AGT complet.

> Pour tous les détails, référez-vous au **GUIDE_USERS.md**.

---

### 3.3 Service Notification (:7002) — pas requis pour search

Le service Notification n'est pas forcement requis direcment pour Search . Il intervient dans d'autres flux de l'écosystème AGT.

> Pour tous les détails, référez-vous au **GUIDE_NOTIFICATION.md**.

---

## 4. Lancer le service Search

Une fois Auth opérationnel et un utilisateur créé, lancez Search :

```bash
cd agt-search
bash scripts/setup.sh
```

Ce script effectue automatiquement :
1. Création du fichier `.env` depuis `.env.example`
2. Build de l'image Docker
3. Démarrage des containers (Elasticsearch + Redis + PostgreSQL + Search)
4. Application des migrations
5. Health check de tous les composants

### Vérification du démarrage

Le service est prêt quand vous voyez :

```json
{
    "status": "healthy",
    "database": "ok",
    "redis": "ok",
    "elasticsearch": "ok",
    "version": "1.0.0"
}

[OK] Search Service prêt sur http://localhost:7007
```

> ⚠️ **Elasticsearch prend environ 30 secondes au premier démarrage.** C'est normal — le script attend automatiquement que ES soit `healthy` avant de démarrer Search.

### URLs disponibles

| URL | Description |
|---|---|
| `http://localhost:7007/api/v1/docs/` | Swagger UI |
| `http://localhost:7007/api/v1/redoc/` | ReDoc |
| `http://localhost:9200` | Elasticsearch direct |

### Rebuild après modification de code

```bash
docker compose down
docker compose up --build -d
```

> ⚠️ **Ne jamais utiliser `docker compose restart`** après modification de fichiers Python. Le restart ne reconstruit pas l'image Docker — les modifications de code ne seront pas prises en compte. Toujours utiliser `--build`.

### Arrêt du service

```bash
docker compose down
```

---

## 5. Variables d'environnement

Fichier : `agt-search/.env.example`

```bash
# Django
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Base de données PostgreSQL
DATABASE_URL=postgresql://search_user:search_password@db:5432/agt-search-db

# Redis (cache JWT et données temporaires)
REDIS_URL=redis://redis:6379/7

# Elasticsearch
ELASTICSEARCH_URL=http://elasticsearch:9200

# Auth — chemin vers la clé publique RSA pour valider les tokens JWT
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Quota maximum d'index actifs par plateforme (défaut : 20)
MAX_INDEXES_PER_PLATFORM=20

# S2S — communication inter-services
# Créer la plateforme dans Auth via POST /auth/platforms
# puis renseigner les credentials obtenus ici
S2S_AUTH_URL=http://agt-auth-service:7000/api/v1
S2S_CLIENT_ID=
S2S_CLIENT_SECRET=
```

> ⚠️ Le fichier `keys/auth_public.pem` doit contenir la clé publique RSA du service Auth. Ce fichier est copié automatiquement par `deploy_mvp.sh` en déploiement intégré. En développement isolé, copiez-le manuellement depuis `agt-auth/keys/public.pem`.

---

## 6. Migrations — étape obligatoire

> ⚠️ **IMPORTANT** : Les fichiers de migration ne sont pas inclus dans le dépôt initial. Ils doivent être générés manuellement au premier lancement. Sans cette étape, le service démarre mais toutes les requêtes échouent avec `relation "indexes_registry" does not exist`.

### Générer et appliquer les migrations

```bash
docker compose exec search python manage.py makemigrations indexes
docker compose exec search python manage.py makemigrations search
docker compose exec search python manage.py migrate
```

Résultat attendu :

```
Migrations for 'indexes':
  apps/indexes/migrations/0001_initial.py
    - Create model IndexRegistry
    - Create model SearchHistory
    - Create model SearchConfig
    - Create model PopularSearch
    - Create model Synonym
    - Create model IndexSchema

Running migrations:
  Applying indexes.0001_initial... OK
```

### Committer les migrations générées

Une fois les migrations générées, les committer dans le dépôt pour que les autres développeurs n'aient pas à les régénérer :

```bash
git add apps/indexes/migrations/
git commit -m "fix(search): add missing initial migrations for indexes app"
```

---

## 7. Authentification — obtenir un token

Tous les endpoints de Search (sauf `/health`) nécessitent un token JWT dans le header :

```
Authorization: Bearer <access_token>
```

### Obtenir un access token via Auth

```
POST http://localhost:7000/api/v1/auth/login
Content-Type: application/json

{
  "email": "test@exemple.com",
  "password": "MotDePasse123!"
}
```

Récupérez le champ `access_token` dans la réponse.

> ⚠️ Les tokens ont une durée de vie de **15 minutes**. Après expiration, reconnectez-vous pour en obtenir un nouveau. Vous verrez l'erreur `{"valid": false, "reason": "token_expired"}`.

### Utiliser le token dans Swagger

1. Ouvrez `http://localhost:7007/api/v1/docs/`
2. Cliquez **Authorize** en haut à droite
3. Collez votre `access_token` dans le champ
4. Cliquez **Authorize** puis **Close**

Swagger injectera automatiquement le token dans toutes vos requêtes de test.

### Tokens S2S (inter-services)

Certains endpoints sont réservés aux tokens S2S (`/history/by-user/{id}` et `/no-results`). Pour créer une plateforme S2S et obtenir un token S2S, référez-vous au **GUIDE_AUTH.md**.

---

## 8. Endpoints — référence complète

### Récapitulatif

| Endpoint | Méthode | Auth | Description |
|---|---|---|---|
| `/search/health` | GET | Public | Health check |
| `/search/indexes` | POST | JWT | Créer un index |
| `/search/indexes` | GET | JWT | Lister les index |
| `/search/indexes/{n}` | GET | JWT | Détail d'un index |
| `/search/indexes/{n}/schema` | PUT | JWT | Ajouter des champs au schéma |
| `/search/indexes/{n}` | DELETE | JWT | Supprimer un index |
| `/search/indexes/{n}/reindex` | POST | JWT | Reconstruire l'index ES |
| `/search/indexes/{n}/documents` | POST | JWT | Indexer un document |
| `/search/indexes/{n}/documents/{d}` | PUT | JWT | Mettre à jour un document |
| `/search/indexes/{n}/documents/{d}` | DELETE | JWT | Supprimer un document |
| `/search/indexes/{n}/documents/bulk` | POST | JWT | Indexation en masse |
| `/search/query` | POST | JWT | Recherche full-text |
| `/search/autocomplete` | GET | JWT | Auto-complétion |
| `/search/history` | GET | JWT | Historique utilisateur |
| `/search/history` | DELETE | JWT | Supprimer son historique (RGPD) |
| `/search/history/by-user/{id}` | DELETE | S2S | Purge RGPD par userId |
| `/search/popular` | GET | JWT | Recherches populaires |
| `/search/no-results` | GET | S2S | Recherches sans résultats |
| `/search/indexes/{n}/config` | GET | JWT | Lire la config d'un index |
| `/search/indexes/{n}/config` | PUT | JWT | Modifier la config d'un index |
| `/search/indexes/{n}/synonyms` | PUT | JWT | Définir les synonymes |
| `/search/indexes/{n}/synonyms` | GET | JWT | Lire les synonymes |
| `/search/stats` | GET | JWT | Statistiques globales |
| `/search/stats/terms` | GET | JWT | Termes les plus recherchés |

---

### 8.1 Health Check

**`GET /api/v1/search/health`** — Aucune authentification requise.

Vérifie l'état de toutes les dépendances du service : base de données, Redis et Elasticsearch.

**Réponse 200 :**
```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "elasticsearch": "ok",
  "version": "1.0.0"
}
```

**Réponse 503** si une dépendance est indisponible — `status` passe à `"degraded"` et le composant défaillant affiche `"error"`.

**Codes :** 200 OK, 503 Service Unavailable.

---

### 8.2 Gestion des index

#### `POST /api/v1/search/indexes` — Créer un index

Crée un nouvel index. Le `platform_id` est extrait **automatiquement du token JWT** — ne jamais le passer dans le body.

Sous le capot, Search crée simultanément :
- Un enregistrement `IndexRegistry` dans PostgreSQL
- Les champs `IndexSchema` associés dans PostgreSQL
- Une `SearchConfig` avec les valeurs par défaut
- Un index physique dans Elasticsearch nommé `{platform_id}_{name}`

**Body :**
```json
{
  "name": "products",
  "analyzer": "french",
  "fields": {
    "title": {
      "type": "text",
      "searchable": true,
      "autocomplete": true,
      "boost_weight": 3
    },
    "price": {
      "type": "float",
      "filterable": true,
      "sortable": true
    },
    "category": {
      "type": "keyword",
      "filterable": true
    }
  }
}
```

**Types de champs disponibles :**

| Type | Usage |
|---|---|
| `text` | Texte analysé, recherche full-text (title, description) |
| `keyword` | Valeur exacte non analysée (category, status, email) |
| `float` / `integer` | Numérique, filtrable et triable (price, stock) |
| `date` | Date, filtrable par plage (created_at) |
| `boolean` | Vrai/Faux (is_active, in_stock) |

**Analyzers disponibles :** `standard`, `french`, `english`, `arabic`

**Propriétés de champ :**

| Propriété | Défaut | Description |
|---|---|---|
| `type` | `text` | Type de la donnée |
| `searchable` | `true` | Ce champ est recherchable en full-text |
| `filterable` | `false` | Ce champ peut être utilisé comme filtre |
| `sortable` | `false` | Ce champ peut être utilisé pour le tri |
| `autocomplete` | `false` | Ce champ alimente l'auto-complétion |
| `boost_weight` | `1` | Importance dans le score de pertinence |

**Quota :** Maximum 20 index actifs par plateforme. Au-delà → 429 Too Many Requests.

**Réponse 201 :**
```json
{
  "id": "uuid-de-l-index",
  "name": "products",
  "es_index": "{platform_id}_products",
  "message": "Index created"
}
```

**Codes :** 201 Created, 400 Validation error, 401 Unauthorized, 409 Index already exists, 429 Quota dépassé.

---

#### `GET /api/v1/search/indexes` — Lister les index

Retourne uniquement les index actifs de la plateforme authentifiée. L'isolation est automatique — une plateforme ne voit jamais les index d'une autre plateforme.

**Réponse 200 :**
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "products",
      "platform_id": "uuid-de-la-plateforme",
      "document_count": 42,
      "status": "active"
    }
  ]
}
```

**Codes :** 200, 401.

---

#### `GET /api/v1/search/indexes/{indexName}` — Détail d'un index

Retourne les métadonnées complètes d'un index ainsi que son schéma (liste de tous les champs définis).

**Paramètre path :** `indexName` — nom de l'index. Ex: `products`

**Réponse 200 :**
```json
{
  "id": "uuid",
  "name": "products",
  "platform_id": "uuid",
  "document_count": 42,
  "schema": [
    {
      "field_name": "title",
      "field_type": "text",
      "searchable": true,
      "filterable": false,
      "autocomplete": true
    },
    {
      "field_name": "price",
      "field_type": "float",
      "searchable": false,
      "filterable": true,
      "autocomplete": false
    },
    {
      "field_name": "category",
      "field_type": "keyword",
      "searchable": false,
      "filterable": true,
      "autocomplete": false
    }
  ]
}
```

**Codes :** 200, 401, 403 (index appartenant à une autre plateforme), 404.

---

#### `PUT /api/v1/search/indexes/{indexName}/schema` — Ajouter des champs au schéma

Ajoute de nouveaux champs au schéma d'un index existant **sans perdre les documents déjà indexés**.

> ⚠️ **Seul l'ajout de champs est supporté.** Modifier le type d'un champ existant nécessite un reindex complet via `POST /reindex`. Les champs déjà existants passés dans le body sont ignorés (`skipped`) sans erreur.

**Body :**
```json
{
  "fields": {
    "stock": {
      "type": "integer",
      "filterable": true,
      "sortable": true
    },
    "brand": {
      "type": "keyword",
      "filterable": true,
      "searchable": true
    }
  }
}
```

**Réponse 200 :**
```json
{
  "message": "Schema updated",
  "added": ["stock", "brand"],
  "skipped": ["title"]
}
```

**Codes :** 200, 400, 401, 403, 404.

---

#### `DELETE /api/v1/search/indexes/{indexName}` — Supprimer un index

> ⚠️ **Action irréversible.** Supprime l'index physique dans Elasticsearch et marque le statut `deleted` dans PostgreSQL. Tous les documents indexés sont perdus. Aucune récupération possible.

**Réponse :** 204 No Content (pas de body).

**Codes :** 204, 401, 403, 404.

---

#### `POST /api/v1/search/indexes/{indexName}/reindex` — Reconstruire l'index

Reconstruit complètement l'index Elasticsearch à partir du schéma actuel enregistré dans PostgreSQL. À utiliser après l'ajout de champs via `/schema` pour que le nouveau mapping soit pris en compte sur tous les documents existants.

> ⚠️ Les documents existants dans ES sont perdus après cette opération — il faudra les réindexer via `/documents` ou `/documents/bulk`.

**Pas de body requis.**

**Réponse 202 :**
```json
{
  "message": "Reindex started",
  "index": "products",
  "status": "rebuilding"
}
```

**Codes :** 202 Accepted, 401, 403, 404.

---

### 8.3 Indexation des documents

#### `POST /api/v1/search/indexes/{indexName}/documents` — Indexer un document

Ajoute un document dans l'index Elasticsearch. Si un document avec le même `doc_id` existe déjà, il est remplacé intégralement.

**Body :**
```json
{
  "doc_id": "prod-123",
  "data": {
    "title": "Nike Air Max 270",
    "price": 35000,
    "category": "Chaussures",
    "is_boosted": false,
    "created_at": "2026-01-10T08:00:00Z"
  }
}
```

Le `doc_id` est l'identifiant de votre choix — typiquement l'ID de l'objet dans votre base de données métier. Le champ `data` contient les valeurs des champs définis dans votre schéma.

**Réponse 201 :**
```json
{
  "doc_id": "prod-123",
  "index": "products",
  "message": "Document indexed"
}
```

**Codes :** 201 Created, 400 (doc_id manquant), 401, 403, 404 (index introuvable).

---

#### `PUT /api/v1/search/indexes/{indexName}/documents/{docId}` — Mettre à jour un document

Met à jour **complètement** un document existant. Le contenu du document est entièrement remplacé par le nouveau contenu fourni.

**Paramètre path :** `docId` — identifiant du document. Ex: `prod-123`

**Body :**
```json
{
  "data": {
    "title": "Nike Air Max 270 - Edition Limitée",
    "price": 40000,
    "category": "Chaussures",
    "stock": 5,
    "brand": "Nike"
  }
}
```

**Réponse 200 :**
```json
{
  "doc_id": "prod-123",
  "index": "products",
  "message": "Document updated"
}
```

**Codes :** 200, 400 (data manquant), 401, 403, 404.

---

#### `DELETE /api/v1/search/indexes/{indexName}/documents/{docId}` — Supprimer un document

Supprime un document spécifique de l'index Elasticsearch. À appeler quand un objet est supprimé de votre base de données métier.

**Réponse :** 204 No Content.

**Codes :** 204, 401, 403, 404.

---

#### `POST /api/v1/search/indexes/{indexName}/documents/bulk` — Indexation en masse

Indexe ou supprime plusieurs documents en une seule requête. Utilisé pour les imports en lot ou les synchronisations. Maximum **500 opérations** par requête — au-delà, retourne 413.

**Body :**
```json
{
  "operations": [
    {
      "action": "index",
      "doc_id": "prod-001",
      "data": {"title": "Produit A", "price": 5000}
    },
    {
      "action": "index",
      "doc_id": "prod-002",
      "data": {"title": "Produit B", "price": 8000}
    },
    {
      "action": "delete",
      "doc_id": "prod-999"
    }
  ]
}
```

`action` accepte deux valeurs : `index` (ajouter ou mettre à jour) ou `delete` (supprimer). Pour `action: delete`, le champ `data` est ignoré.

**Réponse 207 Multi-Status :**
```json
{
  "total": 3,
  "succeeded": 2,
  "failed": 1,
  "errors": [
    {
      "doc_id": "prod-999",
      "error": "Document not found"
    }
  ]
}
```

Le code 207 signifie que certaines opérations ont réussi et d'autres non — consultez toujours le champ `errors` pour identifier les échecs.

**Codes :** 207 Multi-Status, 400, 401, 403, 404, 413 (> 500 opérations).

---

### 8.4 Recherche

#### `POST /api/v1/search/query` — Recherche full-text

C'est l'endpoint principal du service. Recherche dans un index et retourne les résultats triés par score de pertinence Elasticsearch. Chaque appel est automatiquement loggé dans `search_history` et comptabilisé dans `popular_searches`.

**Body :**
```json
{
  "index": "products",
  "query": "chaussures nike",
  "search_type": "fulltext",
  "filters": [
    {
      "field": "price",
      "operator": "range",
      "min": 5000,
      "max": 50000
    },
    {
      "field": "category",
      "operator": "eq",
      "value": "Chaussures"
    }
  ],
  "sort": {"field": "price", "order": "asc"},
  "page": 1,
  "limit": 20,
  "include_facets": true
}
```

| Champ | Obligatoire | Description |
|---|---|---|
| `index` | ✅ | Nom de l'index dans lequel chercher |
| `query` | ✅ | Texte recherché |
| `search_type` | ❌ | `fulltext` (défaut), `fuzzy`, `exact` |
| `filters` | ❌ | Filtres sur les champs déclarés `filterable: true` |
| `sort` | ❌ | Tri : `{"field": "price", "order": "asc"}` ou `"desc"` |
| `page` | ❌ | Numéro de page (défaut: 1) |
| `limit` | ❌ | Résultats par page (défaut: 20, max: 100) |
| `include_facets` | ❌ | Inclure les agrégats par champ dans la réponse |

**Réponse 200 :**
```json
{
  "results": [
    {
      "doc_id": "prod-123",
      "score": 4.82,
      "data": {
        "title": "Nike Air Max 270",
        "price": 35000
      },
      "highlights": {
        "title": ["<em>Nike</em> Air Max 270"]
      }
    }
  ],
  "total": 48,
  "page": 1,
  "limit": 20,
  "took_ms": 34
}
```

Le champ `highlights` contient les termes recherchés surlignés avec des balises `<em>` — à utiliser pour afficher les résultats en gras dans votre interface.

**Codes :** 200, 400 (index manquant), 401, 403, 408 Timeout (query ES > 5s), 429 Rate limited.

---

#### `GET /api/v1/search/autocomplete` — Auto-complétion

Retourne des suggestions en temps réel basées sur un préfixe tapé par l'utilisateur. Optimisé pour répondre en **moins de 50ms**. Seuls les champs déclarés `"autocomplete": true` dans le schéma alimentent cet endpoint.

**Query params :**

| Paramètre | Obligatoire | Description |
|---|---|---|
| `index` | ✅ | Nom de l'index |
| `prefix` | ✅ | Préfixe à compléter. Ex: `sam` → Samsung |
| `limit` | ❌ | Nombre de suggestions retournées (défaut: 8, max: 20) |

**Exemple :** `GET /api/v1/search/autocomplete?index=products&prefix=sam&limit=5`

**Réponse 200 :**
```json
{
  "suggestions": [
    {
      "text": "Samsung Galaxy S24",
      "doc_id": "prod-002"
    }
  ]
}
```

**Codes :** 200, 400 (index ou prefix manquant), 401, 403, 429.

---

### 8.5 Historique de recherche

#### `GET /api/v1/search/history` — Historique de l'utilisateur

Retourne l'historique de recherche de l'utilisateur authentifié. Les entrées sont paginées, les plus récentes en premier.

**Query params :** `page` (défaut: 1), `limit` (défaut: 20)

**Réponse 200 :**
```json
{
  "data": [
    {
      "query": "samsung",
      "index": "products",
      "result_count": 1,
      "took_ms": 335,
      "created_at": "2026-04-16T14:01:49.021917+00:00"
    }
  ],
  "page": 1,
  "total": 1
}
```

**Codes :** 200, 401.

---

#### `DELETE /api/v1/search/history` — Supprimer son historique (RGPD)

Supprime tout l'historique de recherche de l'utilisateur authentifié. Seul l'utilisateur lui-même peut supprimer son propre historique via cet endpoint.

**Réponse :** 204 No Content (pas de body).

**Codes :** 204, 401.

---

#### `DELETE /api/v1/search/history/by-user/{userId}` — Purge RGPD par userId (S2S uniquement)

Purge l'intégralité de l'historique de recherche d'un utilisateur spécifique identifié par son UUID. **Token S2S uniquement** — un token utilisateur classique retourne 403 Forbidden.

Cet endpoint est destiné à être appelé par le service Users lors de la suppression complète d'un compte utilisateur, pour respecter la conformité RGPD.

**Paramètre path :** `userId` — UUID de l'utilisateur (`users_auth.id`)

**Réponse 200 :**
```json
{
  "message": "Search history purged",
  "user_id": "uuid",
  "entries_deleted": 342
}
```

**Codes :** 200, 401, 403 (token non S2S), 404, 500.

---

#### `GET /api/v1/search/popular` — Recherches populaires

Retourne les termes les plus recherchés sur un index donné, triés par fréquence décroissante. Utile pour afficher une section "Tendances" ou "Recherches populaires" dans une interface.

**Query params :**

| Paramètre | Obligatoire | Description |
|---|---|---|
| `index` | ✅ | Nom de l'index |
| `limit` | ❌ | Nombre de résultats (défaut: 10) |

**Exemple :** `GET /api/v1/search/popular?index=products&limit=10`

**Réponse 200 :**
```json
{
  "data": [
    {"term": "samsung", "count": 42},
    {"term": "iphone", "count": 28},
    {"term": "nike", "count": 15}
  ]
}
```

**Codes :** 200, 400 (index manquant), 401.

---

#### `GET /api/v1/search/no-results` — Recherches sans résultats (Admin/S2S)

Retourne les recherches qui n'ont retourné aucun résultat (`result_count = 0`). **Token S2S uniquement.** Utile pour identifier les lacunes dans le contenu indexé — si beaucoup d'utilisateurs cherchent un terme sans résultat, c'est un signal pour enrichir le catalogue.

**Query params :**

| Paramètre | Obligatoire | Description |
|---|---|---|
| `index` | ❌ | Filtrer par nom d'index |
| `from` | ❌ | Date de début. Ex: `2026-01-01` |
| `to` | ❌ | Date de fin. Ex: `2026-12-31` |

**Exemple :** `GET /api/v1/search/no-results?index=products&from=2026-04-01&to=2026-04-30`

**Réponse 200 :**
```json
{
  "data": [
    {
      "query": "écouteurs bluetooth",
      "index": "products",
      "created_at": "2026-04-16T14:01:49+00:00"
    }
  ],
  "total": 1
}
```

**Codes :** 200, 400, 401, 403 (token non S2S).

---

### 8.6 Configuration

#### `GET /api/v1/search/indexes/{indexName}/config` — Lire la configuration

Retourne la configuration actuelle de recherche d'un index. La config est créée automatiquement avec des valeurs par défaut à la création de l'index.

**Réponse 200 :**
```json
{
  "analyzer": "french",
  "fuzzy_enabled": true,
  "fuzzy_distance": 1,
  "highlight_enabled": true,
  "min_score": null,
  "max_results": 100
}
```

**Codes :** 200, 401, 403, 404.

---

#### `PUT /api/v1/search/indexes/{indexName}/config` — Modifier la configuration

Modifie le comportement de la recherche pour un index. Seuls les champs présents dans le body sont mis à jour — les champs absents conservent leur valeur actuelle.

**Body :**
```json
{
  "analyzer": "french",
  "fuzzy_enabled": true,
  "fuzzy_distance": 2,
  "highlight_enabled": true,
  "min_score": 0.5,
  "max_results": 50
}
```

| Paramètre | Description |
|---|---|
| `analyzer` | Langue d'analyse : `standard`, `french`, `english`, `arabic` |
| `fuzzy_enabled` | Active la tolérance aux fautes de frappe |
| `fuzzy_distance` | Nombre de caractères différents tolérés : `1` ou `2` |
| `highlight_enabled` | Active le surlignage des termes dans les résultats avec `<em>` |
| `min_score` | Score minimum pour inclure un résultat (0.0 à 1.0). `null` = pas de filtre |
| `max_results` | Nombre maximum de résultats retournables (max 100) |

**Réponse 200 :**
```json
{"message": "Config updated"}
```

**Codes :** 200, 400, 401, 403, 404.

---

#### `PUT /api/v1/search/indexes/{indexName}/synonyms` — Définir les synonymes

Définit les synonymes pour un index. Quand un synonyme est configuré, chercher le terme principal retrouvera aussi les documents contenant ses équivalents. L'opération est un **remplacement complet** — les anciens synonymes sont supprimés et remplacés par les nouveaux.

**Body :**
```json
{
  "synonyms": [
    {
      "term": "telephone",
      "equivalents": ["smartphone", "mobile", "cellulaire"]
    },
    {
      "term": "chaussure",
      "equivalents": ["basket", "sneaker", "shoe"]
    }
  ]
}
```

**Réponse 200 :**
```json
{"message": "Synonyms updated"}
```

**Codes :** 200, 400, 401, 403, 404.

---

#### `GET /api/v1/search/indexes/{indexName}/synonyms` — Lire les synonymes

Retourne la liste des synonymes actuellement configurés sur un index.

**Réponse 200 :**
```json
{
  "data": [
    {
      "term": "telephone",
      "equivalents": ["smartphone", "mobile", "cellulaire"]
    },
    {
      "term": "chaussure",
      "equivalents": ["basket", "sneaker", "shoe"]
    }
  ]
}
```

**Codes :** 200, 401, 403, 404.

---

### 8.7 Statistiques

#### `GET /api/v1/search/stats` — Statistiques globales

Retourne des statistiques globales sur l'utilisation du service Search — nombre total de recherches effectuées et temps de réponse moyen.

**Réponse 200 :**
```json
{
  "total_searches": 125430,
  "avg_response_ms": 87
}
```

**Codes :** 200, 401.

---

#### `GET /api/v1/search/stats/terms` — Termes les plus recherchés

Retourne les termes les plus recherchés sur un index spécifique, avec filtre optionnel par période. Utile pour l'analyse du comportement des utilisateurs.

**Query params :**

| Paramètre | Obligatoire | Description |
|---|---|---|
| `index` | ✅ | Nom de l'index |
| `limit` | ❌ | Nombre de termes retournés (défaut: 10) |
| `from` | ❌ | Date de début. Ex: `2026-01-01` |
| `to` | ❌ | Date de fin. Ex: `2026-12-31` |

**Exemple :** `GET /api/v1/search/stats/terms?index=products&limit=10&from=2026-04-01&to=2026-04-30`

**Réponse 200 :**
```json
{
  "data": [
    {"term": "samsung", "count": 42},
    {"term": "iphone", "count": 28},
    {"term": "nike", "count": 15}
  ]
}
```

**Codes :** 200, 400 (index manquant), 401.

---

## 9. Flux inter-services

### Search reçoit des appels de

Toutes les plateformes qui ont besoin de capacités de recherche : AGT-Market, AGT-Bot, SALMA, Service Chatbot, et toute future plateforme AGT.

### Search est appelé par

Le service **Users** via token S2S pour purger l'historique lors de la suppression d'un compte (RGPD) :
```
DELETE /api/v1/search/history/by-user/{userId}
Authorization: Bearer <token_S2S>
```

### Configurer un appel S2S vers Search

Pour qu'un service appelle Search avec un token S2S :

1. Créer une plateforme S2S dans Auth : `POST /api/v1/auth/platforms`
2. Stocker `client_id` et `client_secret` dans le `.env` du service appelant
3. Obtenir un token S2S : `POST /api/v1/auth/s2s/token`
4. Injecter ce token dans le header `Authorization: Bearer <token_S2S>`

> Pour tous les détails sur la configuration S2S et le pattern `S2STokenService`, référez-vous au **GUIDE_AUTH.md** et au code de `agt-notification` comme référence d'implémentation.

---

## 10. Tests

### Lancer les tests

```bash
docker compose exec search python -m pytest -v
```

### Structure des tests

```
apps/search/tests/
├── test_all.py    ← tests unitaires (sans Elasticsearch réel)
```

---

## 11. Troubleshooting

### `relation "indexes_registry" does not exist`

Les migrations n'ont pas été générées ou appliquées. Exécutez :
```bash
docker compose exec search python manage.py makemigrations indexes
docker compose exec search python manage.py migrate
```

### `Authentication credentials were not provided`

Le token JWT est absent ou mal formaté dans la requête. Vérifiez que :
- Le header est exactement `Authorization: Bearer <token>` sans espace ni saut de ligne dans le token
- Le token n'a pas expiré (durée de vie : 15 minutes)
- Dans Swagger, le bouton **Authorize** a bien été utilisé avec le token

### Token expiré — `{"valid": false, "reason": "token_expired"}`

Reconnectez-vous via Auth pour obtenir un nouveau token :
```
POST http://localhost:7000/api/v1/auth/login
```

### `405 Method Not Allowed` sur `/documents/bulk`

L'ordre des routes dans `urls.py` est incorrect — la route `/documents/bulk` doit être déclarée **avant** `/documents/<str:doc_id>`. Sans cela, Django capture le mot `bulk` comme un `doc_id` et route vers la mauvaise vue.

### Elasticsearch lent au premier démarrage

Normal — ES peut prendre 30 à 60 secondes au premier démarrage. Le script `setup.sh` attend automatiquement que le healthcheck ES soit `healthy` avant de démarrer le service Search. Ne pas interrompre le script.

### `403 Forbidden` sur `/search/history/by-user/{id}` ou `/search/no-results`

Ces deux endpoints nécessitent un **token S2S**, pas un token utilisateur classique. La réponse sera :
```json
{"detail": "Cet endpoint est réservé aux appels inter-services (S2S)."}
```
Voir section 9 pour configurer un appel S2S.

### Le bouton Authorize de Swagger ne fonctionne pas

Vérifiez que `SPECTACULAR_SETTINGS` dans `config/settings.py` contient bien les clés `SECURITY` et `APPEND_COMPONENTS` avec le schéma `BearerAuth`. Sans ces clés, le bouton Authorize est présent visuellement mais n'injecte pas le token dans les requêtes.

---

*AG Technologies — Usage interne — Confidentiel*
*Guide rédigé le 16 avril 2026 — Session d'audit et de tests complète*