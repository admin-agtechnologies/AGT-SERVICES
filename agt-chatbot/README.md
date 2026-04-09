# AGT Chatbot Service - v1.0

Chatbot IA multi-provider avec pipeline 4 couches.

## Demarrage

### Linux
```bash
bash scripts/setup.sh
```

### Windows
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Documentation API
| URL | Description |
|-----|-------------|
| http://localhost:7010/api/v1/docs/ | Swagger UI |
| http://localhost:7010/api/v1/redoc/ | ReDoc |

## Tests
```bash
docker compose exec chatbot python -m pytest -v
```

## Endpoints
- CRUD /chatbot/bots
- POST/GET /chatbot/bots/{id}/intents (+ keywords)
- POST/GET /chatbot/bots/{id}/flows (+ nodes)
- POST/GET /chatbot/bots/{id}/knowledge/categories
- POST/GET /chatbot/bots/{id}/knowledge/entries
- POST/GET /chatbot/bots/{id}/ai-providers
- **POST /chatbot/converse** (endpoint principal - pipeline 4 couches)
- GET /chatbot/bots/{id}/stats
- POST /chatbot/transfers/{id}/callback

Port : **7010**
