# AGT Microservices - Getting Started

> Guide de demarrage rapide pour l'ecosysteme AGT. Ordre de lancement, premiers pas, et FAQ.

## Ordre de demarrage

Les services ont des dependances. Respectez cet ordre :

```
1. Auth      (port 7000) - en premier, genere les cles RSA
2. Users     (port 7001) - depend de la cle publique Auth
3. Notification (port 7002) - depend de la cle publique Auth
4. Subscription (port 7004) - depend de la cle publique Auth
5. Payment   (port 7005) - depend de la cle publique Auth
```

Les services 4+ (Payment, Wallet...) viendront ensuite.

## Demarrage complet (Windows)

```powershell
# 0. Ouvrir Docker Desktop et attendre qu'il soit pret

# 1. Auth
cd agt-auth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1

# 2. Users (nouveau terminal PowerShell)
cd agt-users
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1

# 3. Notification (nouveau terminal PowerShell)
cd agt-notification
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1

# 4. Subscription (nouveau terminal PowerShell)
cd agt-subscription
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Demarrage complet (Linux/macOS)

```bash
cd agt-auth && bash scripts/setup.sh && cd ..
cd agt-users && bash scripts/setup.sh && cd ..
cd agt-notification && bash scripts/setup.sh && cd ..
cd agt-subscription && bash scripts/setup.sh && cd ..
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1

# 3. Notification (nouveau terminal PowerShell)
cd agt-notification
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

## Demarrage complet (Linux/macOS)

```bash
cd agt-auth && bash scripts/setup.sh && cd ..
cd agt-users && bash scripts/setup.sh && cd ..
cd agt-notification && bash scripts/setup.sh && cd ..
```

## Verification

```bash
curl http://localhost:7000/api/v1/auth/health
curl http://localhost:7001/api/v1/health
curl http://localhost:7002/api/v1/health
```

Les 3 doivent repondre `{"status": "healthy", ...}`.

## Premier flux complet

### 1. Creer une plateforme (sur Auth)

```bash
curl -X POST http://localhost:7000/api/v1/auth/platforms \
  -H "Content-Type: application/json" \
  -H "X-Admin-API-Key: change-me-admin-api-key-very-secret" \
  -d '{"name": "AGT Market", "slug": "agt-market", "allowed_auth_methods": ["email"]}'
```

Notez le `id` (UUID) et le `client_secret` retournes.

### 2. Inscrire un utilisateur

```bash
curl -X POST http://localhost:7000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -H "X-Platform-Id: <UUID-plateforme>" \
  -d '{"email": "test@agt.com", "password": "Test1234!", "method": "email"}'
```

Auth cree le compte ET provisionne automatiquement le profil dans Users.

### 3. Se connecter

```bash
curl -X POST http://localhost:7000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@agt.com", "password": "Test1234!", "platform_id": "<UUID>"}'
```

Copiez l'`access_token` de la reponse.

### 4. Consulter le profil (sur Users)

```bash
curl http://localhost:7001/api/v1/users/by-auth/<auth-user-id> \
  -H "Authorization: Bearer <token>"
```

### 5. Envoyer une notification (sur Notification)

```bash
curl -X POST http://localhost:7002/api/v1/notifications/send \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<user-id>", "channels": ["in_app"], "template_name": "auth_verify_email", "variables": {"verification_url": "http://test.com", "expires_in_minutes": 60, "platform_name": "AGT Market"}}'
```

Note : creez d'abord le template (voir GUIDE_NOTIFICATION.md section 3.1).

### 6. Souscrire a un plan (sur Subscription)

```bash
# D'abord creer un plan (voir GUIDE_SUBSCRIPTION.md section 3.3)
# Puis souscrire
curl -X POST http://localhost:7004/api/v1/subscriptions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<UUID>", "subscriber_type": "user", "subscriber_id": "<auth-user-id>", "plan_id": "<plan-id>", "billing_cycle": "monthly"}'
```

## Ports

| Service | Port API | PostgreSQL | Redis | Autre |
|---------|----------|-----------|-------|-------|
| Auth | 7000 | 5432 | 6379 | - |
| Users | 7001 | 5433 | 6380 | - |
| Notification | 7002 | 5434 | 6381 | RabbitMQ 5672/15672 |
| Subscription | 7004 | 5435 | 6382 | - |
| Payment | 7005 | 5436 | 6383 | - |

## Documentation API (Swagger)

| Service | Swagger UI |
|---------|-----------|
| Auth | http://localhost:7000/api/v1/docs/ |
| Users | http://localhost:7001/api/v1/docs/ |
| Notification | http://localhost:7002/api/v1/docs/ |
| Subscription | http://localhost:7004/api/v1/docs/ |
| Subscription | http://localhost:7004/api/v1/docs/ |
| Payment | http://localhost:7005/api/v1/docs/ |

## FAQ

**Q: Docker dit "pipe not found" ou "unable to get image"**
A: Docker Desktop n'est pas demarre. Ouvrez-le et attendez l'icone verte.

**Q: "openssl n'est pas reconnu"**
A: Normal sur Windows. Le script genere les cles via Docker a la place.

**Q: Le service Users dit "AUTH_PUBLIC_KEY non configure"**
A: Copiez la cle publique : `copy ..\agt-auth\keys\public.pem keys\auth_public.pem`

**Q: L'inscription ne cree pas le profil Users**
A: Normal si Users n'est pas demarre. Auth log un warning mais l'inscription reussit. Demarrez Users et le provisioning fonctionnera pour les prochaines inscriptions.

**Q: Les emails/SMS ne s'envoient pas**
A: Normal en dev. Les providers (SendGrid, Twilio) ne sont pas configures. Les notifications sont creees en base avec status=failed. Utilisez le canal `in_app` pour tester.

**Q: Comment voir les logs ?**
A: `docker compose logs -f <service-name>` (auth, users, notification, celery-worker, etc.)

**Q: Comment tout arreter ?**
A: `docker compose down` dans chaque dossier service. Ajoutez `-v` pour supprimer les donnees.

## Guides detailles

- [GUIDE_AUTH.md](./GUIDE_AUTH.md) - Configuration et utilisation Auth
- [GUIDE_USERS.md](./GUIDE_USERS.md) - Configuration et utilisation Users
- [GUIDE_NOTIFICATION.md](./GUIDE_NOTIFICATION.md) - Configuration et utilisation Notification
- [GUIDE_SUBSCRIPTION.md](./GUIDE_SUBSCRIPTION.md) - Configuration et utilisation Subscription
- [GUIDE_SUBSCRIPTION.md](./GUIDE_SUBSCRIPTION.md) - Configuration et utilisation Subscription
- [GUIDE_PAYMENT.md](./GUIDE_PAYMENT.md) - Configuration et utilisation Payment (a venir)
