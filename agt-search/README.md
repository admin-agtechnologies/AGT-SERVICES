# AGT Search Service - v1.0

Recherche full-text Elasticsearch, indexation dynamique, autocomplete, historique.

## Demarrage

### Linux
```bash
bash scripts/setup.sh
```

### Windows
```powershell
# Ouvrir Docker Desktop
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

> Elasticsearch prend ~30s au premier demarrage.

## Documentation API
| URL | Description |
|-----|-------------|
| http://localhost:7007/api/v1/docs/ | Swagger UI |
| http://localhost:7007/api/v1/redoc/ | ReDoc |
| http://localhost:9200 | Elasticsearch |

## Tests
```bash
docker compose exec search python -m pytest -v
```

## Endpoints
- CRUD /search/indexes (+ schema)
- POST/DELETE /search/indexes/{name}/documents
- POST /search/indexes/{name}/documents/bulk
- POST /search/query (full-text + filtres + facettes)
- GET /search/autocomplete?index=...&prefix=...
- GET/DELETE /search/history
- GET /search/popular?index=...
- GET/PUT /search/indexes/{name}/config
- PUT/GET /search/indexes/{name}/synonyms
- GET /search/stats

Port : **7007**
