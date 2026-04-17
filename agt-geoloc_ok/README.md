# AGT — Service Géolocalisation Centralisé

> **Version** : 1.2.0 · **Stack** : NestJS / Node.js 20 / PostgreSQL + PostGIS / Redis / RabbitMQ · **Port** : 7009

Service de géolocalisation centralisé pour l'écosystème AG Technologies. Gère les positions temps réel (WebSocket + REST), le géofencing event-driven, les trajets, la recherche de proximité et le calcul d'ETA/géocodage multi-provider.

Le service est **agnostique du métier** : il ne connaît pas les chauffeurs, livreurs ou vendeurs — il gère des `tracked_entities` avec des coordonnées, des trajets et des zones. La plateforme consommatrice donne le sens métier.

---

## Démarrage rapide

### Prérequis

- Docker et Docker Compose installés
- Node.js 20+ (pour le développement local sans Docker)

### Lancement autonome (développement isolé)

```bash
# 1. Cloner / se placer dans le dossier
cd agt-geoloc

# 2. Lancer le setup complet
bash scripts/setup.sh
```

Le script crée le `.env`, démarre les conteneurs (PostgreSQL+PostGIS, Redis, RabbitMQ, service NestJS) et vérifie que le service répond.

### Intégration dans l'écosystème AGT global

```bash
# Depuis la racine AGT-SERVICES — copier la clé publique Auth
cp agt-auth/keys/public.pem agt-geoloc/keys/auth_public.pem

# Lancer avec le compose d'intégration
cd agt-geoloc
cp .env.example .env
# Éditer .env : AUTH_SERVICE_URL, S2S_CLIENT_ID, S2S_CLIENT_SECRET
docker compose -f docker-compose.integration.yml up -d --build
```

### Arrêter le service

```bash
docker compose down           # Arrêter sans supprimer les données
docker compose down -v        # Arrêter + supprimer les données (reset complet)
```

---

## Vérification

| Ressource | URL |
|---|---|
| **Swagger UI** | http://localhost:7009/api/v1/docs |
| **Health check** | http://localhost:7009/api/v1/geo/health |
| **RabbitMQ UI** | http://localhost:15675 (agt_rabbit / agt_rabbit_password) |

Réponse health attendue :
```json
{
  "status": "healthy",
  "database": "ok",
  "postgis": "ok",
  "redis": "ok",
  "rabbitmq": "ok",
  "version": "1.2.0"
}
```

---

## Architecture

### Dual storage Redis (CDC v1.1)

```
Couche A — Index GEO par plateforme
  Clé : geo:index:{platform_id}
  Commandes : GEOADD, GEOSEARCH
  Usage : EXCLUSIVEMENT pour la recherche de proximité live

Couche B — Payload détaillé par entité
  Clé : geo:entity:{platform_id}:{entity_id}
  Valeur : { lat, lng, heading, speed, tags, recorded_at, is_online }
  TTL : configurable (défaut 30s) → expiration = entité offline
  Usage : lecture position, diffusion WebSocket
```

Les deux couches sont **mises à jour atomiquement** via un pipeline Redis à chaque position update.

### Géofencing event-driven

Au lieu de polluer la DB avec des checks périodiques, chaque mise à jour de position déclenche une vérification en mémoire :

```
Position update → cache mémoire (turf.js) → O(log Z) → event enter/exit → RabbitMQ
```

Le cache est maintenu cohérent via Redis pub/sub : chaque modification de zone invalide le cache sur toutes les instances NestJS.

### Batch writes PostGIS

Les positions ne sont pas insérées une par une. Elles sont bufferisées en mémoire et flushées toutes les 15s via un INSERT batch :

```
Buffer mémoire (positions.service) → BatchWriterJob (cron 15s) → INSERT batch PostGIS
```

À 20 000 msg/s : un batch de 15s = ~300 000 lignes insérées en < 2s.

---

## Endpoints principaux

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/geo/health` | Health check |
| `POST` | `/api/v1/geo/positions` | Envoi position (REST) |
| `GET` | `/api/v1/geo/positions/:entityId` | Dernière position (Redis live) |
| `GET` | `/api/v1/geo/proximity` | Recherche de proximité |
| `POST` | `/api/v1/geo/trips` | Démarrer un trajet |
| `POST` | `/api/v1/geo/trips/:id/end` | Terminer un trajet |
| `GET` | `/api/v1/geo/trips` | Historique des trajets |
| `POST` | `/api/v1/geo/geofences` | Créer une zone |
| `GET` | `/api/v1/geo/geofences` | Lister les zones |
| `GET` | `/api/v1/geo/distance` | Calculer une distance |
| `GET` | `/api/v1/geo/eta` | Calculer un ETA |
| `GET` | `/api/v1/geo/geocode` | Géocodage adresse → coords |
| `GET` | `/api/v1/geo/reverse-geocode` | Géocodage inverse |
| `PUT` | `/api/v1/geo/config/:platformId` | Config plateforme |
| `GET` | `/api/v1/geo/admin/stats` | Statistiques |
| `DELETE` | `/api/v1/geo/by-user/:userId` | Purge RGPD |

### WebSocket

Connexion : `ws://localhost:7009/geo?token=<JWT>`

| Événement client → serveur | Description |
|---|---|
| `position:update` | Envoi de position haute fréquence |
| `position:subscribe` | Abonnement aux positions d'autres entités |
| `position:unsubscribe` | Désabonnement |

| Événement serveur → client | Description |
|---|---|
| `position:updated` | Position d'une entité suivie |
| `position:offline` | Entité passée offline (TTL expiré) |
| `geofence:trigger` | Événement d'entrée/sortie de zone |

---

## Événements RabbitMQ publiés

Exchange : `agt.geoloc` (type `topic`)

| Routing key | Consommateurs |
|---|---|
| `geo.position.updated` | MboaMove (dispatch), AGT-Market |
| `geo.geofence.enter` | AGT-Market, Notification |
| `geo.geofence.exit` | AGT-Market, Notification |
| `geo.trip.started` | Plateformes |
| `geo.trip.ended` | Plateformes |
| `geo.entity.offline` | Présence, dispatch |

---

## Tests

```bash
# Tests unitaires
npx jest --testPathPattern=unit

# Tests d'intégration
npx jest --testPathPattern=integration

# Tous les tests avec couverture
npx jest --coverage
```

**18 tests unitaires** couvrent :
- Calcul Haversine (distances réelles Yaoundé/Douala)
- Cache géofence (détection polygone, cercle, filtrage par plateforme)
- Machine à états des trajets (active → completed/cancelled)
- Service Positions (création entité, géofencing, buffer)

---

## Variables d'environnement clés

| Variable | Défaut | Description |
|---|---|---|
| `PORT` | `7009` | Port d'écoute |
| `DB_HOST` | `localhost` | Host PostgreSQL+PostGIS |
| `REDIS_HOST` | `localhost` | Host Redis |
| `RABBITMQ_URL` | `amqp://...` | URL RabbitMQ |
| `AUTH_SERVICE_URL` | `http://localhost:7000` | URL du service Auth |
| `AUTH_PUBLIC_KEY_PATH` | `./keys/auth_public.pem` | Clé publique JWT |
| `BATCH_FLUSH_SECONDS` | `15` | Intervalle flush PostGIS |
| `OSRM_URL` | `http://router.project-osrm.org` | Provider routage |
| `GOOGLE_MAPS_API_KEY` | _(vide)_ | Clé Google Maps (optionnel) |

Voir `.env.example` pour la liste complète.

---

## Troubleshooting

**Le service démarre mais PostGIS n'est pas disponible**
```bash
docker compose exec agt-geoloc-db psql -U geoloc_user -d agt_geoloc_db -c "SELECT PostGIS_Version();"
# Si erreur : recréer le volume
docker compose down -v && docker compose up -d --build
```

**JWT invalide en dev (sans Auth service)**
Le service tourne en mode relaxé si `keys/auth_public.pem` est absent. Les tokens sont décodés sans vérification de signature — pratique pour les tests locaux.

**RabbitMQ non connecté**
Les événements sont loggés en warning et ignorés. Le service continue de fonctionner sans RabbitMQ (dégradé).

**Rebuild après modification de code**
```bash
docker compose up -d --build
```

---

*AG Technologies — Service Géolocalisation v1.2 — Confidentiel*
