# AGT Search Service - CDC v1.0

> Recherche full-text Elasticsearch, indexation dynamique, autocomplete, historique.

## Tables (6)
indexes_registry, index_schemas, search_configs, synonyms, search_history, popular_searches

## Elasticsearch
Index par plateforme ({platform_id}_{index_name}). Full-text, fuzzy, facettes, boost, autocomplete.

## Endpoints principaux
- CRUD indexes avec schema dynamique
- Indexation documents (unitaire + bulk 500 max)
- POST /search/query (full-text + filtres + facettes)
- GET /search/autocomplete (< 50ms)
- GET/DELETE /search/history (RGPD)
- GET /search/popular
- GET/PUT config + synonymes par index

## Port : 7007 | Elasticsearch : 9200
