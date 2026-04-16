# AGT Media Service — v1.0.0

Service de gestion centralisée des fichiers pour l'écosystème AG Technologies.

**Port :** 7003 | **Stack :** NestJS / PostgreSQL / Redis / BullMQ / Sharp

## Démarrage rapide

```bash
cp .env.example .env
# Remplir S2S_CLIENT_ID, S2S_CLIENT_SECRET, SIGNED_URL_SECRET

docker compose up -d --build

# Vérifier
curl http://localhost:7003/api/v1/media/health

# Swagger
open http://localhost:7003/api/v1/docs
```

## Tests

```bash
npm install && npm test
```

## Documentation complète

→ Voir [GUIDE_MEDIA.md](./GUIDE_MEDIA.md)
