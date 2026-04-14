# HANDOFF REPORT — Session du 14 avril 2026

> **Projet** : AG Technologies — Architecture Microservices
> **Méthode** : 5 étapes (Analyse → Fonctionnel → Technique → Implémentation → Tests)

---

## 1. CE QUI A ÉTÉ COMPLÉTÉ AVEC SUCCÈS

### Flux MVP complet — TERMINÉ ✅

Le flux `register → email de vérification dans Mailpit` fonctionne end-to-end.

**Fixes appliqués :**

1. `agt-auth/apps/authentication/services.py` — Ajout header `Authorization Bearer` S2S sur tous les appels inter-services (`NotificationClient`, `UsersServiceClient`). Auto-génération du token S2S interne avec le bon `platform_id`.
2. `agt-auth/apps/authentication/views_auth.py` — Ajout `user_id` et `platform_id` dans `recipient` sur tous les appels `NotificationClient.send`.
3. `agt-notification/apps/notifications/authentication.py` — Fix `platform_id` pour tokens S2S (lecture depuis `sub`) + ajout `is_authenticated = True`.
4. `agt-notification/apps/notifications/services.py` — Ajout `S2STokenService` (obtention et cache Redis du token S2S via `POST /auth/s2s/token`) + `UserResolverService` mis à jour pour utiliser ce token.
5. `agt-notification/config/settings.py` — Déclaration des variables `S2S_AUTH_URL`, `S2S_CLIENT_ID`, `S2S_CLIENT_SECRET`.
6. `agt-notification/.env` — Ajout credentials S2S de la plateforme `agt-notification` (créée dans Auth).
7. `agt-notification/providers/providers.py` — SMTP (Mailpit) en premier dans `PROVIDER_MAP`, suppression du double `PROVIDER_MAP` qui écrasait le bon.
8. `agt-notification/config/celery.py` — Ajout `app.conf.imports = ["workers.tasks"]` pour découvrir la tâche `notifications.send_notification`.
9. `agt-auth/apps/authentication/services.py` — Suppression de `first_name` et `last_name` vides dans le payload `provision_user` (causait 400 sur Users).

### Plateformes S2S créées dans Auth

| Service | client_id | Statut |
|---|---|---|
| AGT Market | c87d50a1-e954-4249-ad3e-04e3f07271c7 | ✅ |
| AGT Notification | d3aa237c-726e-4cae-b250-30db70357623 | ✅ |

### Règle architecture établie
> Tout microservice qui appelle d'autres services doit avoir sa propre plateforme S2S dans Auth. Les plateformes S2S des microservices doivent être créées **avant** les plateformes applicatives au premier démarrage.

---

## 2. ÉTAT ACTUEL

Tous les containers MVP sont up et healthy :
- Auth : http://localhost:7000
- Users : http://localhost:7001
- Notification : http://localhost:7002
- Mailpit : http://localhost:8025
- RabbitMQ : http://localhost:15672

---

## 3. PROCHAINE ÉTAPE IMMÉDIATE

**Phase B — Finaliser `GETTING_STARTED.md`**

Le guide doit documenter le flux de démarrage complet incluant :
1. Lancer `deploy_mvp.ps1`
2. Créer les plateformes S2S des microservices (agt-notification, etc.)
3. Créer les plateformes applicatives (AGT Market, etc.)
4. Créer les templates de notification
5. Tester le flux register → email

---

## 4. POINTS D'ATTENTION

| # | Point | Statut |
|---|---|---|
| 1 | Token S2S Notification expire après 1h → renouvelé automatiquement via Redis | ✅ Géré |
| 2 | `first_name`/`last_name` non envoyés au provisioning Users | ✅ Corrigé |
| 3 | `PROVIDER_MAP` dupliqué dans providers.py | ✅ Corrigé |
| 4 | Variables S2S manquantes dans settings.py Notification | ✅ Corrigé |
| 5 | Body de l'email = template brut sans rendu Jinja2 | ⚠️ À améliorer |
| 6 | `run.py` (fix container_names) — encodage UTF-16 sur certains fichiers | ⚠️ Connu |

---

## 5. PORTS

| Service | Port | Swagger |
|---|---|---|
| Auth | 7000 | http://localhost:7000/api/v1/docs/ |
| Users | 7001 | http://localhost:7001/api/v1/docs/ |
| Notification | 7002 | http://localhost:7002/api/v1/docs/ |
| Mailpit | 8025 | http://localhost:8025 |
| RabbitMQ | 15672 | http://localhost:15672 |

---

*AG Technologies — Handoff Report — 14 avril 2026*