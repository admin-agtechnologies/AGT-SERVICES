# GUIDE — Service Géolocalisation AGT

> Guide complet pour lancer, utiliser et intégrer le service Géoloc dans l'écosystème AGT.

---

## Table des matières

1. [Rôle du service](#1-rôle-du-service)
2. [Lancer le service](#2-lancer-le-service)
3. [Authentification](#3-authentification)
4. [Scénarios d'utilisation](#4-scénarios-dutilisation)
5. [WebSocket — Positions temps réel](#5-websocket--positions-temps-réel)
6. [Géofencing](#6-géofencing)
7. [Trajets](#7-trajets)
8. [Distance & ETA](#8-distance--eta)
9. [Flux inter-services](#9-flux-inter-services)
10. [Config par plateforme](#10-config-par-plateforme)
11. [RGPD — Purge utilisateur](#11-rgpd--purge-utilisateur)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. Rôle du service

Le service Géoloc est la **source de vérité pour toutes les données de position** dans l'écosystème AGT.

Il répond à une question simple : **où est cette entité, et où était-elle ?**

Concrètement, il gère :
- La **position live** de n'importe quelle entité (via WebSocket haute fréquence ou REST)
- La **recherche de proximité** : trouver les N entités les plus proches d'un point
- Le **géofencing** : déclencher des alertes quand une entité entre ou sort d'une zone
- L'**historique des trajets** : enregistrer, clore et restituer un trajet complet
- Le **calcul de distance et ETA** via plusieurs providers (Haversine, OSRM, Google Maps)
- Le **géocodage** adresse ↔ coordonnées (Nominatim, Google Maps)

> **Important :** Le service ne connaît **aucun concept métier**. Il ne sait pas ce qu'est un chauffeur MboaMove ou un livreur AGT-Market. Il gère des `tracked_entities` identifiées par `(platform_id, entity_type, entity_id)`. C'est la plateforme consommatrice qui donne le sens.

---

## 2. Lancer le service

### Mode autonome (dev isolé)

```bash
cd agt-geoloc
bash scripts/setup.sh
```

### Mode intégré (avec l'écosystème AGT)

```bash
# Depuis la racine AGT-SERVICES — le MVP doit tourner
bash deploy_mvp.sh   # Lance Auth + Users + Notification

# Copier la clé publique Auth
cp agt-auth/keys/public.pem agt-geoloc/keys/auth_public.pem

# Configurer le .env
cd agt-geoloc && cp .env.example .env
# Éditer AUTH_SERVICE_URL, S2S_CLIENT_ID, S2S_CLIENT_SECRET

# Lancer
docker compose -f docker-compose.integration.yml up -d --build
```

### Vérification

```bash
curl http://localhost:7009/api/v1/geo/health
# {"status":"healthy","database":"ok","postgis":"ok","redis":"ok","rabbitmq":"ok","version":"1.2.0"}
```

---

## 3. Authentification

Tous les endpoints (sauf `/health`) requièrent un token Bearer JWT.

### Token utilisateur (JWT standard)

```bash
# Obtenir un token via Auth service
TOKEN=$(curl -s -X POST http://localhost:7000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password","platform_id":"<uuid>"}' \
  | jq -r '.access_token')

# Utiliser dans les requêtes Geoloc
curl -H "Authorization: Bearer $TOKEN" http://localhost:7009/api/v1/geo/positions/user-uuid?platform_id=<uuid>
```

### Token S2S (service-to-service)

```bash
S2S_TOKEN=$(curl -s -X POST http://localhost:7000/api/v1/auth/s2s/token \
  -H "Content-Type: application/json" \
  -d '{"client_id":"<S2S_CLIENT_ID>","client_secret":"<S2S_CLIENT_SECRET>"}' \
  | jq -r '.access_token')
```

### Mode dev sans clé JWT

Si `keys/auth_public.pem` est absent, le service tourne en mode relaxé : les tokens sont décodés sans vérification de signature. Pratique pour tester sans Auth service.

---

## 4. Scénarios d'utilisation

### 4.1 Envoyer une position (REST — usage ponctuel)

```bash
curl -X POST http://localhost:7009/api/v1/geo/positions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "550e8400-e29b-41d4-a716-446655440000",
    "entity_type": "user",
    "entity_id": "user-uuid-here",
    "latitude": 3.8480,
    "longitude": 11.5021,
    "heading": 45.0,
    "speed": 12.5,
    "accuracy": 10.0,
    "tags": ["available"],
    "recorded_at": "2026-04-16T10:00:00Z"
  }'
```

Réponse :
```json
{
  "entity_id": "user-uuid-here",
  "status": "updated",
  "geofence_events": []
}
```

Si l'entité entre dans une zone lors de cette mise à jour :
```json
{
  "entity_id": "user-uuid-here",
  "status": "updated",
  "geofence_events": [
    { "geofence_id": "zone-uuid", "name": "Zone Centre Yaoundé", "event": "enter" }
  ]
}
```

### 4.2 Lire la dernière position connue

```bash
curl "http://localhost:7009/api/v1/geo/positions/user-uuid-here?platform_id=<uuid>" \
  -H "Authorization: Bearer $TOKEN"
```

```json
{
  "entity_id": "user-uuid-here",
  "lat": 3.848,
  "lng": 11.5021,
  "heading": 45.0,
  "speed": 12.5,
  "tags": ["available"],
  "recorded_at": "2026-04-16T10:00:00Z",
  "is_online": true
}
```

→ **404** si l'entité est offline (TTL Redis expiré) ou inconnue.

### 4.3 Recherche de proximité

Trouver les 5 entités disponibles dans un rayon de 3 km :

```bash
curl "http://localhost:7009/api/v1/geo/proximity?platform_id=<uuid>&latitude=3.848&longitude=11.502&radius_km=3&limit=5&tags=available" \
  -H "Authorization: Bearer $TOKEN"
```

```json
{
  "results": [
    {
      "entity_id": "driver-uuid-1",
      "latitude": 3.849,
      "longitude": 11.503,
      "distance_meters": 142,
      "tags": ["available"],
      "recorded_at": "2026-04-16T10:00:05Z"
    }
  ],
  "total": 1
}
```

---

## 5. WebSocket — Positions temps réel

### Connexion

```javascript
import { io } from 'socket.io-client';

const socket = io('http://localhost:7009/geo', {
  auth: { token: 'Bearer eyJ...' },
  transports: ['websocket'],
});

socket.on('connect', () => console.log('Connecté au Geoloc'));
socket.on('connect_error', (err) => console.error('Erreur:', err.message));
```

### Envoyer sa position (mobile/driver)

```javascript
// Envoyer la position toutes les 5 secondes
setInterval(() => {
  socket.emit('position:update', {
    platform_id: 'platform-uuid',
    entity_type: 'user',
    entity_id: 'my-user-id',
    latitude: getCurrentLat(),
    longitude: getCurrentLng(),
    speed: 12.5,
    heading: 45,
    tags: ['available'],
    recorded_at: new Date().toISOString(),
  });
}, 5000);
```

### Suivre un autre utilisateur (passager suit son chauffeur)

```javascript
// S'abonner aux positions du chauffeur assigné
socket.emit('position:subscribe', {
  platform_id: 'platform-uuid',
  entity_ids: ['driver-uuid'],
});

// Recevoir les mises à jour en temps réel
socket.on('position:updated', (data) => {
  console.log('Chauffeur à:', data.latitude, data.longitude);
  updateMapMarker(data);
});

// Chauffeur passé offline
socket.on('position:offline', ({ entity_id }) => {
  console.log('Chauffeur hors ligne:', entity_id);
});

// Événement géofence
socket.on('geofence:trigger', (data) => {
  console.log(`Entité ${data.entity_id} ${data.event} zone ${data.name}`);
});
```

### Se désabonner

```javascript
socket.emit('position:unsubscribe', { entity_ids: ['driver-uuid'] });
```

---

## 6. Géofencing

### Créer une zone (polygone)

```bash
curl -X POST http://localhost:7009/api/v1/geo/geofences \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "platform-uuid",
    "name": "Zone Centre Yaoundé",
    "fence_type": "polygon",
    "coordinates": [
      [11.49, 3.84], [11.52, 3.84],
      [11.52, 3.87], [11.49, 3.87],
      [11.49, 3.84]
    ],
    "tags": ["delivery_zone"]
  }'
```

### Créer une zone (cercle)

```bash
curl -X POST http://localhost:7009/api/v1/geo/geofences \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "platform-uuid",
    "name": "Aéroport Nsimalen",
    "fence_type": "circle",
    "center_latitude": 3.7200,
    "center_longitude": 11.5533,
    "radius_meters": 5000,
    "tags": ["airport"]
  }'
```

### Événement RabbitMQ déclenché automatiquement

Quand une entité entre ou sort d'une zone, le service publie :

```json
{
  "event_id": "uuid",
  "timestamp": "2026-04-16T10:00:00Z",
  "source": "geo-service",
  "routing_key": "geo.geofence.enter",
  "entity_id": "user-uuid",
  "geofence_id": "zone-uuid",
  "geofence_name": "Zone Centre Yaoundé",
  "platform_id": "platform-uuid",
  "latitude": 3.850,
  "longitude": 11.505,
  "recorded_at": "2026-04-16T10:00:00Z"
}
```

---

## 7. Trajets

### Démarrer un trajet

```bash
curl -X POST http://localhost:7009/api/v1/geo/trips \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "platform-uuid",
    "entity_id": "driver-uuid",
    "start_latitude": 3.8480,
    "start_longitude": 11.5021,
    "metadata": { "ride_id": "ride-uuid-from-mboadrive" }
  }'
```

```json
{ "id": "trip-uuid", "status": "active", "started_at": "2026-04-16T10:00:00Z" }
```

> Un seul trajet `active` par entité à la fois. Retourne 409 si un trajet est déjà en cours.

### Terminer le trajet

```bash
curl -X POST http://localhost:7009/api/v1/geo/trips/trip-uuid/end \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "end_latitude": 3.8700, "end_longitude": 11.5200 }'
```

```json
{
  "trip_id": "trip-uuid",
  "status": "completed",
  "distance_meters": 4520,
  "duration_seconds": 1230,
  "start_address": null,
  "end_address": null
}
```

### Consulter l'historique

```bash
curl "http://localhost:7009/api/v1/geo/trips?entity_id=driver-uuid&platform_id=<uuid>&from_date=2026-04-01&page=1&limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 8. Distance & ETA

### Distance vol d'oiseau (Haversine, instantané)

```bash
curl "http://localhost:7009/api/v1/geo/distance?origin_lat=3.848&origin_lng=11.502&dest_lat=4.050&dest_lng=9.767&provider=haversine" \
  -H "Authorization: Bearer $TOKEN"
```

```json
{ "distance_meters": 196400, "duration_seconds": 14109, "provider": "haversine", "cached": false }
```

### Distance routière (OSRM)

```bash
curl "http://localhost:7009/api/v1/geo/distance?origin_lat=3.848&origin_lng=11.502&dest_lat=3.870&dest_lng=11.520&provider=osrm" \
  -H "Authorization: Bearer $TOKEN"
```

### ETA

```bash
curl "http://localhost:7009/api/v1/geo/eta?origin_lat=3.848&origin_lng=11.502&dest_lat=3.870&dest_lng=11.520&provider=osrm" \
  -H "Authorization: Bearer $TOKEN"
```

```json
{ "eta_seconds": 480, "eta_datetime": "2026-04-16T10:08:00Z", "provider": "osrm", "cached": false }
```

### Géocodage

```bash
# Adresse → coordonnées
curl "http://localhost:7009/api/v1/geo/geocode?address=Carrefour+Bastos+Yaounde&provider=nominatim" \
  -H "Authorization: Bearer $TOKEN"

# Coordonnées → adresse
curl "http://localhost:7009/api/v1/geo/reverse-geocode?latitude=3.8845&longitude=11.5027" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 9. Flux inter-services

### Ce service appelle

| Service | Quand | Comment |
|---|---|---|
| **Auth** | Validation JWT (chaque requête REST/WS) | Cache Redis TTL 30s |
| **Auth** | Token S2S inter-services | `POST /auth/s2s/token` |

### Ce service est appelé par

| Service | Endpoint | Quand |
|---|---|---|
| MboaMove backend | `GET /geo/proximity` | Trouver chauffeurs proches |
| MboaMove mobile | WebSocket `position:update` | Envoi position chauffeur |
| MboaMove backend | `POST /geo/trips` | Démarrage course |
| AGT-Market backend | `GET /geo/proximity` | Trouver livreurs |
| Users service | `DELETE /geo/by-user/:id` | Purge RGPD |

### Événements RabbitMQ consommés par

| Routing key | Consommateur | Usage |
|---|---|---|
| `geo.position.updated` | MboaMove dispatch | Affectation chauffeur |
| `geo.geofence.enter/exit` | Notification service | Push alert utilisateur |
| `geo.geofence.enter/exit` | AGT-Market | Livraison en zone |
| `geo.trip.ended` | MboaMove billing | Calcul tarif course |
| `geo.entity.offline` | MboaMove dispatch | Indisponibilité chauffeur |

---

## 10. Config par plateforme

Chaque plateforme peut personnaliser le comportement du service :

```bash
curl -X PUT http://localhost:7009/api/v1/geo/config/platform-uuid \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "update_interval_seconds": 5,
    "position_ttl_seconds": 30,
    "batch_flush_seconds": 15,
    "default_eta_provider": "osrm",
    "default_geocode_provider": "nominatim",
    "max_proximity_radius_km": 50
  }'
```

| Paramètre | Défaut | Description |
|---|---|---|
| `update_interval_seconds` | 5 | Fréquence envoi position mobile (1–60s) |
| `position_ttl_seconds` | 30 | Offline après X secondes sans update |
| `batch_flush_seconds` | 15 | Intervalle flush PostGIS |
| `default_eta_provider` | `haversine` | `haversine`, `osrm`, `google_maps` |
| `max_proximity_radius_km` | 50 | Rayon max recherche proximité |

---

## 11. RGPD — Purge utilisateur

```bash
# Appelé par le service Users avant la suppression du compte Auth
curl -X DELETE http://localhost:7009/api/v1/geo/by-user/user-uuid \
  -H "Authorization: Bearer $S2S_TOKEN"
```

Effet :
- La `TrackedEntity` est anonymisée (entity_id → UUID technique non lié à l'utilisateur)
- L'entité est retirée de l'index Redis live
- L'historique PostGIS est conservé pour l'analytics (données spatiales agrégées, pas nominatives)

---

## 12. Troubleshooting

### Service ne démarre pas

```bash
docker compose logs agt-geoloc
# Chercher : DB connection, Redis connection, RabbitMQ
```

### PostGIS non activé

```bash
docker compose exec agt-geoloc-db psql -U geoloc_user -d agt_geoloc_db -c "SELECT PostGIS_Version();"
# Si erreur → recréer le volume
docker compose down -v && docker compose up -d --build
```

### Redis : clés GEO vides

```bash
docker compose exec agt-geoloc-redis redis-cli
# Lister les clés GEO d'une plateforme
ZCARD geo:index:<platform_id>
# Voir payload d'une entité
GET geo:entity:<platform_id>:<entity_id>
```

### WebSocket ne se connecte pas

Vérifier que le token est valide :
```bash
# Décoder le token (sans vérification de signature)
echo $TOKEN | cut -d. -f2 | base64 -d 2>/dev/null | jq .
```

### RabbitMQ — events non reçus

```bash
# Vérifier que l'exchange existe
# Interface : http://localhost:15675 → Exchanges → agt.geoloc
```

### Tests

```bash
# Lancer tous les tests
cd agt-geoloc && npx jest --no-coverage

# Tests unitaires uniquement
npx jest --testPathPattern=unit --no-coverage

# Voir la couverture
npx jest --coverage
```

---

*AG Technologies — GUIDE_GEOLOC.md — Service Géolocalisation v1.2 — Confidentiel*
