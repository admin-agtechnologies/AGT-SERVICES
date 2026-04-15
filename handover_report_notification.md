# HANDOFF REPORT — Session du 15 avril 2026

## 1. CE QUI A ÉTÉ COMPLÉTÉ

### Infrastructure
- ✅ MVP AGT lancé sur Ubuntu (Auth :7000, Users :7001, Notification :7002)
- ✅ Bug gateway Nginx corrigé (identifié : `host.docker.internal` non supporté sur Linux — à corriger plus tard)

### Tests — Service Notification (29/29 routes testées)
- ✅ `GET /health`
- ✅ `GET/POST /templates` + `GET/PUT/DELETE /templates/{id}` + `POST /templates/{id}/preview` + `GET /templates/{id}/versions`
- ✅ `POST /notifications/send` + `POST /notifications/send-bulk`
- ✅ `GET/PUT /users/{id}/notification-preferences`
- ✅ `GET /users/{id}/notifications` + unread-count + read + read-all + DELETE
- ✅ `GET/POST /users/{id}/device-tokens` + DELETE
- ✅ `GET /notifications/stats` + `GET /notifications/logs`
- ✅ `GET/PUT /platforms/{id}/channels-priority`
- ✅ `GET/POST /campaigns` + detail + progress + cancel

### Bugs corrigés
- ✅ **Bug #3** — Swagger ne montrait pas le Request body sur `PUT /templates/{id}` et `POST /templates/{id}/preview` → corrigé en ajoutant `request=TemplateUpdateSerializer` et `request=TemplatePreviewSerializer` dans les `@extend_schema`
- ✅ **Bug #4** — `POST /campaigns/{id}/cancel` acceptait les campagnes déjà `completed` ou `cancelled` → corrigé en ajoutant une vérification de statut dans `CampaignCancelView`
- ✅ **Bug #1 & #2** — Emails de vérification non envoyés par Auth → deux causes corrigées :
  - Templates recréés sans `platform_id` (globaux) pour être accessibles depuis toutes les plateformes
  - `allow_blank=True` ajouté dans `UserProfileCreateSerializer` côté Users Service pour accepter `first_name=""` et `last_name=""`

### Documentation
- ✅ `GUIDE_NOTIFICATION.md` rédigé — guide complet 15 sections, 29 routes documentées, exemples d'intégration frontend, troubleshooting

---

## 2. EN COURS

- 🔄 **Gateway Nginx** — container `agt-gateway` en `Restarting` sur Ubuntu car `host.docker.internal` n'existe pas sur Linux
  - Fichier : `gateway/nginx.conf`
  - Tous les upstreams utilisent `host.docker.internal:PORT` → à remplacer par les vrais noms de containers Docker
  - Non bloquant pour les tests (chaque service accessible directement sur son port)

---

## 3. PROCHAINE ÉTAPE IMMÉDIATE

**Tester le `GUIDE_NOTIFICATION.md`** étape par étape pour valider qu'un débutant peut le suivre sans aide.

Ensuite, selon la roadmap :
- Corriger le gateway Nginx pour Ubuntu (remplacer `host.docker.internal` par les noms de containers)
- Documenter le service **Auth** (`GUIDE_AUTH.md`) en suivant la même méthode
- Documenter le service **Users** (`GUIDE_USERS.md`)

---

## 4. POINTS D'ATTENTION

### Templates système — obligatoire avant tout test Auth
Les 4 templates suivants doivent exister **sans `platform_id`** dans Notification avant de tester Auth :
- `auth_verify_email`
- `auth_reset_password`
- `auth_magic_link`
- `auth_otp_sms`

IDs actuels en base :
| Nom | ID |
|-----|----|
| `auth_magic_link` | `e9669e75-2471-482f-9e3a-c8206939ef22` |
| `auth_otp_sms` | `3c7ea199-98b0-46d5-a526-bebae8a55239` |
| `auth_reset_password` | `c585d88f-595d-4458-8b3e-2434ee5bed53` |
| `auth_verify_email` | `b18b48c3-a02f-477d-8ae0-e461e8a247d9` |

### Plateformes S2S configurées
| Service | platform_id | Usage |
|---------|-------------|-------|
| Plateforme Test | `e92253f7-a220-4fad-9811-cff90c200877` | Tests manuels Swagger |
| Notification S2S | `eeb544bc-cc38-46b9-b2dd-7b286e5a7aef` | Identité machine du service Notification |

### Rate limiting
En développement, le rate limiting Redis peut bloquer les tests répétitifs. Vider avec :
```bash
docker exec -it agt-auth-redis redis-cli FLUSHDB
```

### SENDGRID_API_KEY vide
Normal en dev — le fallback SMTP (Mailpit) fonctionne. Ne pas configurer SendGrid en dev.

### Gateway Nginx non fonctionnel sur Ubuntu
Non bloquant — accéder directement aux services via leurs ports :
- Auth → `http://localhost:7000/api/v1/docs/`
- Users → `http://localhost:7001/api/v1/docs/`
- Notification → `http://localhost:7002/api/v1/docs/`

---

## 5. COMMANDES UTILES

```bash
# Démarrer le MVP
bash deploy_mvp.sh

# Vérifier l'état des containers
docker ps --format "table {{.Names}}\t{{.Status}}"

# Logs en direct
docker logs -f agt-notif-service
docker logs -f agt-notif-worker
docker logs -f agt-auth-service

# Vider le cache Redis Auth (rate limiting)
docker exec -it agt-auth-redis redis-cli FLUSHDB

# Rebuild un service après modification de code
docker compose -f agt-notification/docker-compose.yml up -d --build
docker compose -f agt-auth/docker-compose.yml up -d --build
docker compose -f agt-users/docker-compose.yml up -d --build

# Lancer les tests Notification
docker exec -it agt-notif-service python -m pytest -v

# Shell Django Notification
docker exec -it agt-notif-service python manage.py shell

# Mailpit (emails de dev)
http://localhost:8025

# RabbitMQ Management
http://localhost:15672 (agt_rabbit / agt_rabbit_password)

# Swagger des services
http://localhost:7000/api/v1/docs/  → Auth
http://localhost:7001/api/v1/docs/  → Users
http://localhost:7002/api/v1/docs/  → Notification
```