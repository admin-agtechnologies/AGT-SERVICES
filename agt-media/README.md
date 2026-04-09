# AGT Media Service - Simulateur MVP (v1.0)

> **Attention :** Ceci est un simulateur (bouchon stateful) conçu pour le développement local. Il stocke les métadonnées en mémoire vive (RAM) et les fichiers sur le disque local. Les données sont perdues au redémarrage du conteneur.

Ce simulateur permet aux autres services (comme `Users` ou `Chat`) de fonctionner sans erreur 502 en simulant un véritable service d'upload de fichiers.

## Prérequis
- Docker et Docker Compose
- Le réseau Docker `agt_network` doit exister (`docker network create agt_network`)

## Démarrage rapide

```bash
# Démarrer le simulateur en arrière-plan
docker compose up -d --build

# Vérifier que le service tourne
curl http://localhost:7003/api/v1/media/health
```

## Endpoints simulés

Base URL : `http://localhost:7003/api/v1/media`

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/health` | Vérifie l'état du simulateur |
| `POST` | `/` | Upload un fichier (multipart/form-data, champ `file`) |
| `GET` | `/{id}/info` | Récupère les métadonnées mockées du fichier |
| `GET` | `/{filename}` | Télécharge ou affiche le fichier brut |
| `DELETE`| `/by-user/{userId}` | Simule la purge RGPD (Contrat S2S avec Users) |

## Exemples d'utilisation

### 1. Uploader un fichier
```bash
curl -X POST http://localhost:7003/api/v1/media \
  -F "file=@chemin/vers/ton/image.jpg"
```
*Réponse attendue :*
```json
{
  "id": "uuid-genere",
  "original_name": "image.jpg",
  "mime_type": "image/jpeg",
  "size_bytes": 12345,
  "url": "/api/v1/media/uuid-genere.jpg",
  "created_at": "2026-04-09T12:00:00.000Z"
}
```

### 2. Voir les infos du fichier
```bash
curl http://localhost:7003/api/v1/media/<id-du-fichier>/info
```

### 3. Afficher l'image dans le navigateur
Ouvre simplement l'URL retournée lors de l'upload dans ton navigateur :
`http://localhost:7003/api/v1/media/<uuid-genere.jpg>`
```
