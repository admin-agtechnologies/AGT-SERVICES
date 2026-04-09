# AGT Geoloc Service - Simulateur MVP (v1.0)

> **Attention :** Ceci est un simulateur stateful en mémoire vive (RAM). Les positions sont perdues au redémarrage.

Ce simulateur permet de tester le tracking GPS (REST et WebSocket) et de répondre aux appels S2S (purge RGPD).

## Démarrage rapide

```bash
docker compose up -d --build
curl http://localhost:7009/api/v1/geoloc/health
```

## Endpoints REST simulés

Base URL : `http://localhost:7009/api/v1/geoloc` (ou `/api/v1/geo`)

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/health` | État du simulateur |
| `POST` | `/positions` | Met à jour la position d'une entité |
| `GET` | `/proximity` | Retourne de fausses entités proches |
| `DELETE`| `/by-user/{userId}` | Simule la purge RGPD |

## WebSocket (Socket.io)

Path : `/geoloc/socket.io/`

- **Écouter :** `position:updated`
- **Émettre :** `position:update` (payload: `{entity_id, latitude, longitude}`)
