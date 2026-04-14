# HANDOFF REPORT — Session du 14 avril 2026

> **Projet** : AG Technologies — Architecture Microservices
> **Pair-programmer** : Claude (Anthropic)
> **Méthode** : 5 étapes (Analyse → Fonctionnel → Technique → Implémentation → Tests)

---

## 1. CE QUI A ÉTÉ COMPLÉTÉ AVEC SUCCÈS

### Flux MVP end-to-end — VALIDÉ ✅

Le flux complet `register → provisioning Users → email de vérification dans Mailpit` fonctionne.

### Corrections techniques appliquées

| Fichier | Correction |
|---|---|
| `agt-auth/apps/authentication/services.py` | Ajout header `Authorization Bearer` S2S sur tous les appels inter-services. Auto-génération du token S2S avec le bon `platform_id` dans le JWT. Suppression de `first_name`/`last_name` vides dans `provision_user`. |
| `agt-auth/apps/authentication/views_auth.py` | Ajout `user_id` et `platform_id` dans `recipient` sur tous les appels `NotificationClient.send`. |
| `agt-notification/apps/notifications/authentication.py` | Fix `platform_id` pour tokens S2S (lecture depuis `sub` au lieu de `platform_id`) + ajout `is_authenticated = True`. |
| `agt-notification/apps/notifications/services.py` | Ajout `S2STokenService` (obtention et cache Redis via `POST /auth/s2s/token`) + `UserResolverService` mis à jour. |
| `agt-notification/config/settings.py` | Déclaration des variables `S2S_AUTH_URL`, `S2S_CLIENT_ID`, `S2S_CLIENT_SECRET`. |
| `agt-notification/config/celery.py` | Ajout `app.conf.imports = ["workers.tasks"]` — sans ça, Celery ne découvrait pas la tâche `notifications.send_notification`. |
| `agt-notification/providers/providers.py` | SMTP (Mailpit) en premier dans `PROVIDER_MAP`. Suppression du double `PROVIDER_MAP` qui écrasait le bon. |
| `agt-notification/.env` | Ajout credentials S2S de la plateforme `agt-notification`. |

### Plateformes créées dans Auth (à NE PAS recréer sauf après `--clean`)

| Plateforme | client_id | Usage |
|---|---|---|
| Plateforme Test | `c87d50a1-e954-4249-ad3e-04e3f07271c7` | Tests d'inscription et flux utilisateur |
| AGT Notification | `d3aa237c-726e-4cae-b250-30db70357623` | Token S2S de Notification → Users |

### Documentation produite

- `docs/GETTING_STARTED.md` — guide complet du MVP avec chorégraphie inter-services
- `README.md` racine — vue d'ensemble du projet, structure, scripts, outils
- `prompt/TEAM_PROMPT.md` — prompt générique pour déléguer le travail à l'équipe
- `todo.md` — roadmap complète phases A→H avec bilan et priorités
- Guides vides créés : GUIDE_PAYMENT, GUIDE_WALLET, GUIDE_SEARCH, GUIDE_CHAT, GUIDE_CHATBOT, GUIDE_MEDIA, GUIDE_GEOLOC, GUIDE_SCRIPTS, GUIDE_LOGS, GUIDE_NEW_SERVICE

---

## 2. RÈGLES ET PATTERNS CRITIQUES À RESPECTER

Ces points ont causé des bugs en session — toute l'équipe doit les connaître.

### Communication inter-services (S2S)
Tout appel HTTP entre services **doit** porter un header `Authorization: Bearer <token>`. Le token est obtenu via `POST /auth/s2s/token` et mis en cache Redis. Voir `S2STokenService` dans `agt-notification/apps/notifications/services.py` — copier ce pattern dans chaque nouveau service.

### JWTPayload dans chaque service
Toujours inclure `is_authenticated = True`. Pour les tokens S2S, `platform_id` est dans le champ `sub` du JWT (pas dans `platform_id`). Voir `agt-notification/apps/notifications/authentication.py`.

### Celery : découverte des tâches
`app.autodiscover_tasks()` ne découvre que `apps/*/tasks.py`. Pour des tâches dans `workers/tasks.py`, ajouter explicitement dans `config/celery.py` :
```python
app.conf.imports = ["workers.tasks"]
```

### Container names Docker
Utiliser des **tirets**, jamais des underscores. Django 4.2+ rejette les underscores comme hostnames (RFC 1034).

### Variables .env dans settings.py
Toute variable lue depuis l'environnement doit être déclarée dans `settings.py` avec `config("MA_VAR", default="")`. Sans déclaration, Django ne la voit pas même si elle est dans le `.env`.

### Swagger — bouton Authorize
Nécessite dans `settings.py` :
```python
SPECTACULAR_SETTINGS = {
    "SECURITY": [{"BearerAuth": []}],
    "APPEND_COMPONENTS": {"securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer"}}}
}
```

---

## 3. PROCHAINE ÉTAPE IMMÉDIATE

**Phase B — Documentation & Tests MVP en parallèle**

Utiliser `prompt/TEAM_PROMPT.md` pour déléguer :

```
Dev 1  →  GUIDE_AUTH.md + pytest agt-auth/
Dev 2  →  GUIDE_USERS.md + pytest agt-users/
Dev 3  →  GUIDE_NOTIFICATION.md + pytest agt-notification/ + fix rendu Jinja2
Lead   →  Phase C — Subscription ou Payment
```

---

## 4. POINTS D'ATTENTION EN SUSPENS

| # | Point | Action requise |
|---|---|---|
| 1 | Body des emails = template brut, variables Jinja2 non rendues | Corriger dans `agt-notification` — le template est stocké en base mais non rendu avant envoi |
| 2 | Tests pytest non validés en intégration réelle | Les lancer sur chaque service, corriger les échecs |
| 3 | `.env.example` de Notification ne contient pas encore `S2S_CLIENT_ID/SECRET` | Mettre à jour `.env.example` avec les clés S2S (valeurs vides, commentées) |
| 4 | Après tout `reset --clean` : recréer plateformes + token S2S + templates | Documenter dans GUIDE_SCRIPTS.md ou automatiser dans un script `setup_platforms.ps1` |

---

## 5. COMMANDES UTILES

```powershell
# Lancer le MVP
.\deploy_mvp.ps1

# Reset complet (repart de zéro)
.\reset_mvp.ps1 --clean

# Rebuild Auth
cd agt-auth && docker compose up -d --build auth && cd ..

# Rebuild Notification (service + worker)
cd agt-notification
docker compose up -d --build notification celery-worker
cd ..

# Logs en temps réel
docker logs agt-auth-service --follow
docker logs agt-notif-worker --follow

# Vider le cache Redis Auth (rate limiting)
docker exec agt-auth-redis redis-cli FLUSHDB

# Lancer les tests
docker exec agt-auth-service python -m pytest -v
docker exec agt-users-service python -m pytest -v
docker exec agt-notif-service python -m pytest -v
```

---

## 6. PORTS DE RÉFÉRENCE

| Service | Port | Swagger |
|---|---|---|
| Auth | 7000 | http://localhost:7000/api/v1/docs/ |
| Users | 7001 | http://localhost:7001/api/v1/docs/ |
| Notification | 7002 | http://localhost:7002/api/v1/docs/ |
| Mailpit | 8025 | http://localhost:8025 |
| RabbitMQ | 15672 | http://localhost:15672 (agt_rabbit / agt_rabbit_password) |

---

*AG Technologies — Handoff Report — 14 avril 2026*