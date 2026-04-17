# HANDOFF REPORT FINAL — Session du 17 avril 2026
## Service : AGT Notification Service — Mise en conformité CDC v1.2

---

## 1. CE QUI A ÉTÉ COMPLÉTÉ

### Mise en conformité CDC v1.2 — Nouvelles routes implémentées

**Section Planification (4 routes — entièrement nouvelles) :**
- ✅ `POST /notifications/schedule` — Planifier une notification future
- ✅ `GET /notifications/scheduled` — Lister avec filtre `?status=pending`
- ✅ `PUT /notifications/scheduled/{id}` — Modifier date/variables
- ✅ `DELETE /notifications/scheduled/{id}` — Annuler

Fichiers modifiés :
- `agt-notification/apps/notifications/views.py` — 3 nouvelles classes ajoutées
- `agt-notification/apps/notifications/urls.py` — 3 nouvelles routes
- `agt-notification/apps/notifications/serializers.py` — 2 nouveaux serializers

**Section Campagnes (1 route manquante) :**
- ✅ `GET /campaigns/{id}/stats` — Statistiques détaillées d'une campagne

Fichiers modifiés :
- `agt-notification/apps/campaigns/views.py` — classe `CampaignStatsView` ajoutée
- `agt-notification/apps/campaigns/urls.py` — route ajoutée

### Corrections de conformité (5 corrections)

- ✅ `POST /campaigns/{id}/cancel` — ajout de `sent_before_cancel` dans la réponse
- ✅ `GET /campaigns/{id}/progress` — ajout de `pending` dans la réponse
- ✅ `GET /users/{id}/notifications` — ajout de `unread_count` dans la réponse
- ✅ `GET /notifications/stats` — format conforme CDC (`total_sent`, `delivery_rate`)
- ✅ `GET /notifications/logs` — filtres query params (`channel`, `status`, `from`, `to`) + déclaration Swagger via `OpenApiParameter`

### Bugs corrigés (session précédente + cette session)

- ✅ **Bug #1/#2** — Emails non envoyés lors du register Auth → templates recréés sans `platform_id` + `allow_blank=True` dans Users serializer
- ✅ **Bug #3** — Swagger sans Request body sur `PUT /templates/{id}` et `POST /templates/{id}/preview` → ajout `request=` dans `@extend_schema`
- ✅ **Bug #4** — Cancel campagne acceptait les statuts `completed`/`cancelled` → vérification ajoutée
- ✅ **Bug #5** — `PUT /notifications/scheduled/{id}` sans Request body dans Swagger → ajout `request=ScheduledNotificationUpdateSerializer`

### Documentation

- ✅ `GUIDE_NOTIFICATION.md` mis à jour en **v1.2** (16 sections, 35 routes documentées)
  - Section 8 ajoutée : Notifications planifiées
  - Section 12 enrichie : stats campagne, pending, sent_before_cancel
  - Section 13 mise à jour : format stats conforme, filtres logs
  - Section 5 enrichie : explication fallback providers
  - Section 4 enrichie : note restart vs rebuild
  - Section 16 enrichie : troubleshooting RabbitMQ connection refused

---

## 2. BILAN FINAL DES ROUTES

**Total : 35 routes — toutes implémentées, testées et documentées**

| Module | Routes | Statut |
|--------|--------|--------|
| Health | 1 | ✅ |
| Templates | 7 | ✅ |
| Send | 2 | ✅ |
| Schedule | 4 | ✅ |
| Preferences | 2 | ✅ |
| In-App | 5 | ✅ |
| Devices | 3 | ✅ |
| Campaigns | 6 | ✅ |
| Stats/Logs | 2 | ✅ |
| Config | 2 | ✅ |

**Service 100% conforme au CDC v1.2.**

---

## 3. EN COURS / NON RÉSOLU

### Gateway Nginx — `agt-gateway` en Restarting sur Ubuntu
- **Cause :** `host.docker.internal` non supporté sur Linux
- **Fichier :** `gateway/nginx.conf` — tous les blocs `upstream`
- **Fix à appliquer :** remplacer `server host.docker.internal:PORT` par le nom du container Docker

Exemple :
```nginx
# Avant (ne fonctionne pas sur Linux)
upstream auth {
    server host.docker.internal:7000;
}

# Après (correct)
upstream auth {
    server agt-auth-service:7000;
}
```

Services à corriger dans `nginx.conf` :
```
auth       → agt-auth-service:7000
users      → agt-users-service:7001
notification → agt-notif-service:7002
```

- **Impact :** Non bloquant pour les tests directs sur les ports. Bloquant si on veut passer par le gateway (port 80).

---

## 4. POINTS D'ATTENTION

### Templates système Auth — à recréer après chaque reset DB

Les 4 templates suivants doivent être créés **sans `platform_id`** après chaque reset complet :

| Nom | Canal | Variables |
|-----|-------|-----------|
| `auth_verify_email` | email | `verification_url`, `expires_in_minutes`, `platform_name` |
| `auth_reset_password` | email | `reset_url`, `expires_in_minutes`, `platform_name` |
| `auth_magic_link` | email | `magic_link_url`, `expires_in_minutes`, `platform_name` |
| `auth_otp_sms` | sms | `otp_code`, `expires_in_minutes`, `platform_name` |

> ⚠️ Si ces templates sont créés avec un `platform_id`, Auth ne pourra pas les résoudre et les emails ne seront pas envoyés lors du register.

### Profil Users — requis pour l'envoi de notifications

Le worker Notification appelle Users Service pour récupérer l'email du destinataire. Si le profil n'existe pas → 404 → pas d'envoi.

Après un reset DB, provisionner manuellement si nécessaire :
```bash
docker exec -it agt-auth-service python manage.py shell -c "
from apps.authentication.services import UsersServiceClient
UsersServiceClient.provision_user(auth_user_id='uuid', email='email@test.com')
"
```

### Restart vs Rebuild

En développement, le code est monté en volume (`- .:/app`) dans le service Notification :
- **Modification de code ou `.env`** → `docker restart agt-notif-service agt-notif-worker` suffit
- **Modification de `Dockerfile` ou `requirements.txt`** → rebuild obligatoire : `docker compose -f agt-notification/docker-compose.yml up -d --build`

### allow_blank dans Users serializer

`allow_blank=True` a été ajouté sur `first_name` et `last_name` dans `agt-users/apps/users/serializers.py`. Ce changement est nécessaire car Auth envoie `""` pour ces champs lors du provisioning. Ne pas le retirer.

### SENDGRID_API_KEY non configuré en dev

Normal — en développement, `SMTPProvider` (Mailpit) est le provider principal. Les logs montreront parfois `sendgrid → failed` en attempt 2 — c'est le fallback normal, pas un bug.

---

## 5. PROCHAINE ÉTAPE IMMÉDIATE

**Tester et documenter le service Auth** (`GUIDE_AUTH.md`) en suivant la même méthode :

1. **Analyse** — lire le CDC Auth v1.x et scanner le code existant
2. **Conformité** — faire le diff CDC vs code, identifier les routes manquantes
3. **Tests** — tester route par route via Swagger (register, verify-email, login, refresh, logout, 2FA, magic link, sessions, admin, S2S)
4. **Corrections** — corriger les bugs et routes manquantes
5. **Documentation** — rédiger `GUIDE_AUTH.md` sur le modèle de `GUIDE_NOTIFICATION.md`

> ℹ️ Auth est le service de référence de l'architecture AGT. Son guide doit être particulièrement complet car tous les autres services dépendent de lui.

---

## 6. COMMANDES UTILES

```bash
# Lancer le MVP complet
bash deploy_mvp.sh

# Vérifier l'état des containers
docker ps --format "table {{.Names}}\t{{.Status}}"

# Logs en direct
docker logs -f agt-notif-service
docker logs -f agt-notif-worker
docker logs -f agt-auth-service

# Vider le cache Redis Auth (rate limiting)
docker exec -it agt-auth-redis redis-cli FLUSHDB

# Restart services Notification (après modif code ou .env)
docker restart agt-notif-service agt-notif-worker

# Rebuild complet Notification (Dockerfile ou requirements.txt)
docker compose -f agt-notification/docker-compose.yml up -d --build

# Rebuild Auth et Users
docker compose -f agt-auth/docker-compose.yml up -d --build
docker compose -f agt-users/docker-compose.yml up -d --build

# Tests Notification
docker exec -it agt-notif-service python -m pytest -v

# Migrations (après reset DB)
docker exec -it agt-auth-service python manage.py migrate
docker exec -it agt-users-service python manage.py migrate
docker exec -it agt-notif-service python manage.py migrate

# Swagger UIs
# Auth         : http://localhost:7000/api/v1/docs/
# Users        : http://localhost:7001/api/v1/docs/
# Notification : http://localhost:7002/api/v1/docs/
# Mailpit      : http://localhost:8025
# RabbitMQ     : http://localhost:15672 (agt_rabbit / agt_rabbit_password)
```

---

*AG Technologies — Handoff Report Final — Notification Service v1.2 — 17 avril 2026*