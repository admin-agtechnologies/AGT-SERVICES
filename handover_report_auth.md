# HANDOFF REPORT — Session du 15 avril 2026

> **Projet** : AG Technologies — Auth Service v1.0
> **Méthode** : Test manuel via Swagger + corrections de bugs + documentation

---

## 1. CE QUI A ÉTÉ COMPLÉTÉ

### MVP validé
- `deploy_mvp.ps1` exécuté et validé — 15 containers UP, tous healthy
- Flux end-to-end Register → Email → Verify → Login fonctionnel et testé

### Bugs corrigés dans Auth

| Fichier | Correction |
|---------|------------|
| `agt-auth/apps/authentication/views_auth.py` | Ordre inversé : `provision_user` (Users) appelé AVANT `NotificationClient.send` |
| `agt-auth/apps/authentication/views_auth.py` | `first_name`/`last_name` ajoutés au register, resend-verification et login bloqué si email non vérifié |
| `agt-auth/apps/authentication/views_auth.py` | Nouveau endpoint `ResendVerificationView` créé |
| `agt-auth/apps/authentication/serializers.py` | `first_name`/`last_name` ajoutés dans `RegisterSerializer` + `ResendVerificationSerializer` créé |
| `agt-auth/apps/authentication/services.py` | `"data"` → `"variables"` dans le payload envoyé à Notification + `first_name`/`last_name` dans payload Users |
| `agt-auth/apps/authentication/urls.py` | Route `auth/resend-verification` ajoutée + import `ResendVerificationView` |

### Nouveau endpoint créé
- `POST /api/v1/auth/resend-verification` — renvoi email de vérification avec invalidation des anciens tokens

### Templates Notification créés
| Template | Canal | Platform ID |
|----------|-------|-------------|
| `auth_verify_email` | email | à recréer sur votre machine |
| `auth_otp_sms` | sms | à recréer sur votre machine |
| `auth_magic_link` | email | à recréer sur votre machine |
| `auth_reset_password` | email | à recréer sur votre machine |

### Documentation produite
- `GUIDE_AUTH.md` — guide complet autonome couvrant Health, Platforms, S2S, Register, Login
- `HANDOFF_REPORT_15_AVRIL_2026.md` — ce fichier

### Groupes testés et validés
| Groupe | Statut |
|--------|--------|
| Health | ✅ |
| Platforms (POST, GET, PUT, DELETE) | ✅ |
| S2S (token + introspect) | ✅ |
| Register (register + verify-email + resend-verification) | ✅ |
| Login (valide + mauvais password + email non vérifié) | ✅ |

---

## 2. EN COURS

Tests manuels Auth via Swagger — groupes non encore testés :

| Groupe | Endpoints à tester |
|--------|-------------------|
| Sessions | `POST /refresh`, `POST /logout`, `GET /sessions`, `DELETE /sessions/{id}`, `GET /verify-token`, `POST /token/exchange` |
| Profile | `GET /me`, `GET /login-history`, `GET /stats/{user_id}` |
| Password | `POST /forgot-password`, `POST /reset-password`, `PUT /change-password` |
| 2FA | `POST /2fa/enable`, `POST /2fa/confirm`, `POST /2fa/verify`, `POST /2fa/disable` |
| Admin | `POST /admin/block/{id}`, `POST /admin/unblock/{id}`, `POST /account/deactivate`, `DELETE /admin/purge/{id}` |
| OAuth | `GET /oauth/google`, `GET /oauth/google/callback`, `GET /oauth/facebook`, `GET /oauth/facebook/callback` |

---

## 3. PROCHAINE ÉTAPE IMMÉDIATE

**Reprendre le guide au groupe Sessions.**

Méthode à suivre pour chaque groupe :
1. Demander à l'IA d'expliquer le rôle de chaque endpoint du groupe
2. Tester chaque endpoint dans Swagger avec les bons JSON (voir section 5)
3. Si un bug est trouvé → diagnostiquer avec les logs avant de coder
4. Documenter le résultat dans `GUIDE_AUTH.md` à la suite de ce qui existe

**Compte de test disponible :**
- Email : `jane.doe@example.com` / Password : `Test1234!` — vérifié, prêt pour tous les tests
- Obtenir un `access_token` frais via `POST /auth/login` avant de tester les endpoints protégés

**JSON de login pour récupérer un token frais :**
```json
POST /api/v1/auth/login
{
  "email": "jane.doe@example.com",
  "password": "Test1234!",
  "platform_id": "<votre_platform_id>"
}
```
→ Copier le `access_token` et cliquer **Authorize** dans Swagger.

---

## 4. POINTS D'ATTENTION

| # | Point | Action requise |
|---|-------|----------------|
| 1 | `PUT /templates/{id}` n'affiche pas le body dans Swagger Notification | Bug Swagger à corriger — ajouter `@extend_schema(request=TemplateUpdateSerializer)` dans `apps/templates_mgr/views.py` |
| 2 | `resend-verification` apparaît dans le groupe `auth` au lieu de `Register` dans Swagger | Vérifier le tag dans `@extend_schema` de `ResendVerificationView` |
| 3 | Apostrophes perdues dans les templates (`L equipe`, `n avez`) | Corriger les templates via PUT quand le bug Swagger sera fixé |
| 4 | `first_name` toujours vide dans `resend-verification` | Auth ne stocke pas le prénom — amélioration future : le récupérer depuis Users |
| 5 | Après `reset --clean` : recréer plateformes + templates + credentials S2S Notification | Refaire les sections 5, 6, 7 du GUIDE_AUTH.md depuis le début |
| 6 | Tests pytest Auth non encore lancés | À faire après les tests manuels complets |

---

## 5. COMMANDES UTILES

```powershell
# Lancer le MVP
.\deploy_mvp.ps1

# Reset complet (reconfigurer depuis section 5 du GUIDE_AUTH.md)
.\reset_mvp.ps1 --clean

# Rebuild Auth uniquement
cd agt-auth && docker compose up -d --build auth && cd ..

# Rebuild Notification (service + worker)
cd agt-notification
docker compose up -d --build notification celery-worker
cd ..

# Vider le rate limiting Redis Auth
docker exec agt-auth-redis redis-cli FLUSHDB

# Logs Auth en temps réel
docker logs agt-auth-service --follow

# Logs worker Notification
docker logs agt-notif-worker --tail=50

# Régénérer un token S2S (remplacer les valeurs)
$r = Invoke-RestMethod -Uri "http://localhost:7000/api/v1/auth/s2s/token" `
  -Method POST -ContentType "application/json" `
  -Body '{"client_id": "<platform_id>", "client_secret": "<secret>"}'
$token = $r.access_token

# Tests pytest Auth
docker exec agt-auth-service python -m pytest -v
```

---

## 6. PORTS DE RÉFÉRENCE

| Service | Port | Swagger |
|---------|------|---------|
| Auth | 7000 | http://localhost:7000/api/v1/docs/ |
| Users | 7001 | http://localhost:7001/api/v1/docs/ |
| Notification | 7002 | http://localhost:7002/api/v1/docs/ |
| Mailpit | 8025 | http://localhost:8025 |
| RabbitMQ | 15672 | http://localhost:15672 (agt_rabbit / agt_rabbit_password) |

---

*AG Technologies — Handoff Report — 15 avril 2026*