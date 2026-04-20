# HANDOFF REPORT — Session du 15 avril 2026

## 1. CE QUI A ÉTÉ COMPLÉTÉ

### Scripts

- `stop_clean.ps1` et `stop_clean.sh` créés et validés — arrêt + nettoyage complet sans redéploiement

### Bugs corrigés dans Auth

| Fichier                                          | Correction                                                                                                                                             |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `agt-auth/apps/authentication/authentication.py` | `JWTPayload` ajouté + `authenticate` retourne `JWTPayload` au lieu de `UserAuth`                                                                       |
| `agt-auth/apps/authentication/views_sessions.py` | Toutes les vues migrées de `user=request.user` vers `user_id=request.user.auth_user_id` + `UsersServiceClient` importé                                 |
| `agt-auth/apps/authentication/views_sessions.py` | `ForgotPasswordView` — `user_id` ajouté dans `recipient` + `first_name` récupéré depuis Users                                                          |
| `agt-auth/apps/authentication/views_auth.py`     | `MagicLinkRequestView` — `first_name` récupéré depuis Users via `get_profile_by_auth_id` + correction `data.get("first_name")` → variable `first_name` |
| `agt-auth/apps/authentication/services.py`       | `UsersServiceClient.get_profile_by_auth_id()` ajouté                                                                                                   |
| `agt-auth/apps/authentication/views_admin.py`    | `AccountDeactivateView` — `user = request.user` → `UserAuth.objects.get(id=request.user.auth_user_id)`                                                 |

15 avril 2026 — Rapport quotidien — Atabong Stéphane
GROSSE TACHE

Projet : AGT-SERVICES / AV-3
Tâche : [Users] Tests & documentation complète
Statut : Terminé
Fait : Tests manuels complets de tous les endpoints du service Users via Swagger, correction des bugs identifiés (AuditLog DjangoJSONEncoder, UserStatsView, Swagger body manquants, routes dupliquées permissions), implémentation du hard delete RGPD et du quitter plateforme, rédaction complète du GUIDE_USERS.md
Difficultés : Migrations non appliquées au démarrage, fix DjangoJSONEncoder non pris en compte car modifications faites hors container
Mesures prises : Génération manuelle des migrations, rebuild systématique après chaque modification, fix appliqué directement dans le container puis reporté en local
Remarque : Bug Auth identifié — pas d'endpoint pour réactiver un compte désactivé. À remonter à l'équipe Auth

PETITE TACHE

Projet : AGT-SERVICES / AV-7
Tâche : [Payment] Lancer & démarrer les tests
Statut : En pause
Fait : aucun
Difficultés : aucune
Mesures prises : reporté au lendemain — grosse tâche AV-3 a pris toute la journée
Remarque : aucune

DIVERS

Interruptions / imprévus : aucun
Besoin pour demain : démarrer AV-7 Payment en priorité

### Migrations

- Découverte et correction du bug critique : migrations non générées au déploiement
- Fix documenté dans le guide : `makemigrations authentication` + `makemigrations users roles documents` + `makemigrations notifications templates_mgr campaigns devices`

### Groupes testés et validés

| Groupe                                                  | Statut |
| ------------------------------------------------------- | ------ |
| Health                                                  | ✅     |
| Platforms (POST, GET, PUT, DELETE)                      | ✅     |
| S2S (token + introspect)                                | ✅     |
| Templates Notification (4 templates)                    | ✅     |
| Register (register + verify + resend)                   | ✅     |
| Login (valide + mauvais mdp + non vérifié + magic-link) | ✅     |
| Sessions (list + revoke + refresh + logout)             | ✅     |
| Profile (me + login-history + stats)                    | ✅     |
| Password (forgot + reset + change)                      | ✅     |
| Admin (block + unblock)                                 | ✅     |

---

## 2. EN COURS

Tests Admin — non encore testés :

| Endpoint                   | Notes                                             |
| -------------------------- | ------------------------------------------------- |
| `POST /account/deactivate` | Erreur `invalid_signature` — à investiguer        |
| `DELETE /admin/purge/{id}` | Non testé — à faire en début de prochaine session |

---

## 3. PROCHAINE ÉTAPE IMMÉDIATE

1. **Valider le guide de façon autonome** — refaire les parties 1 et 2 depuis zéro avec `stop_clean.ps1`
2. **Terminer Admin** — tester `account/deactivate` + `admin/purge`
3. **Corriger les bugs connus** listés en section 4
4. **Documenter les perspectives** dans le guide

---

## 4. POINTS D'ATTENTION ET BUGS CONNUS

| #   | Bug                                                                            | Fichier                                        | Action                                                                    |
| --- | ------------------------------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------------------- |
| 1   | `SENDGRID_API_KEY non configuré` dans les logs worker quand Users retourne 404 | `agt-notification/providers/providers.py`      | Vérifier ordre `PROVIDER_MAP` — SMTP doit être en premier                 |
| 2   | Email non reçu quand provisioning Users échoue (404)                           | `agt-notification/workers/tasks.py`            | Le worker tombe sur Sendgrid au lieu de SMTP                              |
| 3   | `resend-verification` — `first_name` toujours vide                             | `agt-auth/apps/authentication/views_auth.py`   | Appeler `get_profile_by_auth_id` comme dans magic-link et forgot-password |
| 4   | Migrations absentes du repo                                                    | Tous les services                              | Générer et commiter les migrations                                        |
| 5   | `deploy_mvp.ps1` lance `migrate` trop tôt                                      | `deploy_mvp.ps1`                               | Ajouter `makemigrations` avant `migrate` dans le script                   |
| 6   | `account/deactivate` — `invalid_signature` à investiguer                       | `views_admin.py`                               | Tester avec token frais copié proprement                                  |
| 7   | `PUT /templates/{id}` — body non visible dans Swagger Notification             | `agt-notification/apps/templates_mgr/views.py` | Ajouter `@extend_schema(request=TemplateUpdateSerializer)`                |

---

## 5. PERSPECTIVES À DOCUMENTER

| #   | Perspective                                                     |
| --- | --------------------------------------------------------------- |
| 1   | 2FA par email — configurable par plateforme (TOTP vs email)     |
| 2   | OAuth Google + Facebook — à tester post-déploiement serveur     |
| 3   | `token/exchange` — à tester dans le contexte OAuth              |
| 4   | OTP SMS — à tester quand provider SMS configuré                 |
| 5   | Réactivation de compte désactivé — endpoint admin à implémenter |
| 6   | `deploy_mvp.ps1` — intégrer `makemigrations` automatiquement    |

---

## 6. COMMANDES UTILES

```powershell
# Nettoyage complet
.\stop_clean.ps1

# Déploiement MVP
.\deploy_mvp.ps1

# Migrations (obligatoire après deploy sur base vide)
docker exec agt-auth-service python manage.py makemigrations authentication
docker exec agt-auth-service python manage.py migrate --noinput
docker exec agt-users-service python manage.py makemigrations users roles documents
docker exec agt-users-service python manage.py migrate --noinput
docker exec agt-notif-service python manage.py makemigrations notifications templates_mgr campaigns devices
docker exec agt-notif-service python manage.py migrate --noinput

# Vider le rate limiting Redis
docker exec agt-auth-redis redis-cli FLUSHDB

# Rebuild Auth
cd agt-auth && docker compose up -d --build auth && cd ..

# Logs
docker logs agt-auth-service --tail=30
docker logs agt-notif-worker --tail=30

# Tests pytest
docker exec agt-auth-service python -m pytest -v
```

---

## 7. PORTS DE RÉFÉRENCE

| Service      | Port  | Swagger                                                   |
| ------------ | ----- | --------------------------------------------------------- |
| Auth         | 7000  | http://localhost:7000/api/v1/docs/                        |
| Users        | 7001  | http://localhost:7001/api/v1/docs/                        |
| Notification | 7002  | http://localhost:7002/api/v1/docs/                        |
| Mailpit      | 8025  | http://localhost:8025                                     |
| RabbitMQ     | 15672 | http://localhost:15672 (agt_rabbit / agt_rabbit_password) |

---

_AG Technologies — Handoff Report — 15 avril 2026_
