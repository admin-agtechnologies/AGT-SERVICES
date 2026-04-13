# HANDOFF REPORT — Session du 13 avril 2026

> **Projet** : AG Technologies — Architecture Microservices
> **Pair-programmer** : Claude (Anthropic)
> **Méthode** : 5 étapes (Analyse → Fonctionnel → Technique → Implémentation → Tests)

---

## 1. CE QUI A ÉTÉ COMPLÉTÉ AVEC SUCCÈS

### 1.1 Scripts de déploiement (Phase A — TERMINÉ ✅)

Créé/corrigé **8 scripts** : `deploy_mvp.ps1/.sh`, `deploy_all.ps1/.sh`, `reset_mvp.ps1/.sh`, `reset_all.ps1/.sh`. Flag `--clean` pour purger les volumes. Filtrage par pattern AGT. Health check avec retry. Renommé fichier infra. Retiré Média du MVP. Résolu le conflit labels réseau `agt_network` via `external: true`.

### 1.2 Corrections Swagger (TERMINÉ ✅)

Ajouté `COMPONENT_SPLIT_REQUEST`, `APPEND_COMPONENTS`, `SECURITY`, `SWAGGER_UI_SETTINGS` dans Users et Notification. Créé serializers Notification. Corrigé S2S Auth avec `S2STokenRequestSerializer`.

**⚠️ Vérifier** : `fix_swagger_notif.py` a été généré, confirmer que les POST Notification ont bien un body après rebuild.

### 1.3 Migrations (TERMINÉ ✅ — à relancer après reset --clean)

```bash
# Auth (depuis agt-auth/)
docker compose exec auth python manage.py makemigrations authentication platforms
docker compose exec auth python manage.py migrate
# Users (depuis agt-users/)
docker compose exec users python manage.py makemigrations users roles documents
docker compose exec users python manage.py migrate
# Notification (depuis agt-notification/)
docker compose exec notification python manage.py makemigrations notifications templates_mgr campaigns devices
docker compose exec notification python manage.py migrate
```

### 1.4 Configuration flux MVP (FAIT — à refaire après reset --clean)

**Plateforme** : `POST /auth/platforms` avec `X-Admin-API-Key: change-me-admin-api-key-very-secret`
```json
{"name": "AGT Market", "slug": "agt-market", "allowed_auth_methods": ["email"]}
```

**Token S2S** : `POST /auth/s2s/token` avec `client_id` (platform UUID) + `client_secret`

**4 templates** créés via `POST /templates` (Notification Swagger, Bearer S2S) :

| Template | Canal | Variables clés |
|---|---|---|
| `auth_verify_email` | email | `verification_url`, `expires_in_minutes`, `platform_name` |
| `auth_reset_password` | email | `reset_url`, `expires_in_minutes`, `platform_name` |
| `auth_magic_link` | email | `magic_link_url`, `expires_in_minutes`, `platform_name` |
| `auth_otp_sms` | sms | `otp_code`, `expires_in_minutes`, `platform_name` |

### 1.5 Script renommage container_name (GÉNÉRÉ ✅ — À EXÉCUTER)

**Problème** : `container_name` avec underscores (`agt_users_service`) → Django 4.2+ rejette car RFC 1034/1035 interdit les underscores dans les hostnames HTTP. Tous les appels inter-services (Auth → Users, Auth → Notification) échouent avec `DisallowedHost` / `400 Bad Request`.

**Script** : `fix_container_names.py` — search-and-replace `agt_xxx_yyy` → `agt-xxx-yyy` dans ~15 fichiers. Le réseau `agt_network` n'est PAS touché.

---

## 2. PROCHAINE ACTION IMMÉDIATE

```powershell
# 1. Exécuter le renommage
python fix_container_names.py

# 2. Tout arrêter et rebuild
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
.\reset_mvp.ps1 --clean

# 3. Migrations (depuis chaque dossier service)
cd agt-auth && docker compose exec auth python manage.py makemigrations authentication platforms && docker compose exec auth python manage.py migrate && cd ..
cd agt-users && docker compose exec users python manage.py makemigrations users roles documents && docker compose exec users python manage.py migrate && cd ..
cd agt-notification && docker compose exec notification python manage.py makemigrations notifications templates_mgr campaigns devices && docker compose exec notification python manage.py migrate && cd ..

# 4. Recréer plateforme (Swagger Auth → POST /auth/platforms)
# 5. Obtenir token S2S (POST /auth/s2s/token)
# 6. Recréer 4 templates (Swagger Notification → POST /templates × 4)
# 7. Tester inscription (POST /auth/register)
# 8. Vérifier Mailpit (http://localhost:8025) + profil Users
```

---

## 3. PLAN GLOBAL RESTANT

| Phase | Description | Statut |
|---|---|---|
| **B** | GETTING_STARTED.md (progressif, ensemble) | 🔄 En cours |
| **C** | Guides par service (Auth, Users, Notification) | ⬜ |
| **D** | Intégration Subscription → Payment → Wallet → Search → Chatbot | ⬜ |
| **E** | Génération vrais services (Média, Chat, Geoloc) | ⬜ |
| **F** | Backend template | ⬜ |

---

## 4. DIFFICULTÉS ET RÉSOLUTIONS

| # | Problème | Résolution | Statut |
|---|---|---|---|
| 1 | Scripts reset tuaient tout Docker | Filtrage par pattern AGT | ✅ |
| 2 | Conflit labels réseau | `external: true` + création idempotente | ✅ |
| 3 | Swagger sans Authorize/body | `APPEND_COMPONENTS` + serializers | ✅ |
| 4 | S2S Swagger : additionalProp | Serializers dédiés | ✅ |
| 5 | Tables inexistantes | makemigrations + migrate | ✅ |
| 6 | RFC 1034 underscores hostnames | `fix_container_names.py` | ✅ Généré |
| 7 | Docker Desktop ne s'ouvre plus | Non bloquant, CLI fonctionne | ⚠️ Connu |

---

## 5. CONVENTIONS

- **Méthode 5 étapes** : Analyse → Fonctionnel → Technique → Implémentation → Tests
- **CDC > Code**
- **GETTING_STARTED.md construit ensemble**, pas généré en bloc
- **Solutions propres pour la prod**, pas de quick fixes
- **Scripts séparés** : deploy_mvp, deploy_all, reset_mvp, reset_all

---

## 6. PORTS

| Service | Port | Swagger |
|---|---|---|
| Auth | 7000 | http://localhost:7000/api/v1/docs/ |
| Users | 7001 | http://localhost:7001/api/v1/docs/ |
| Notification | 7002 | http://localhost:7002/api/v1/docs/ |
| Mailpit | 8025 | http://localhost:8025 |
| RabbitMQ | 15672 | http://localhost:15672 (agt_rabbit / agt_rabbit_password) |

---

*AG Technologies — Handoff Report — 13 avril 2026*