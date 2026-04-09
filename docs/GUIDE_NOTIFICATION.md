# Service Notification v1.0 - Guide d'utilisation

> Ce guide explique comment configurer, demarrer et utiliser le service Notification de l'ecosysteme AGT.

## 1. Demarrage

### Prerequis
- Docker Desktop **demarre**
- **Service Auth demarre en premier** (pour la cle publique RSA)

### Lancement

**Windows :**
```powershell
cd agt-notification
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

**Linux/macOS :**
```bash
cd agt-notification
bash scripts/setup.sh
```

> Ce service demarre 6 conteneurs : API, Celery Worker, Celery Beat, RabbitMQ, Redis, PostgreSQL. Le demarrage prend ~15 secondes.

### Verification

```
curl http://localhost:7002/api/v1/health
```

Reponse attendue :
```json
{"status": "healthy", "database": "ok", "redis": "ok", "broker": "ok", "version": "1.0.0"}
```

### URLs

| URL | Description | Credentials |
|-----|-------------|-------------|
| http://localhost:7002/api/v1/docs/ | Swagger UI | - |
| http://localhost:7002/api/v1/redoc/ | ReDoc | - |
| http://localhost:15672 | RabbitMQ Management | **guest / guest** |

---

## 2. Architecture du service

```
Client -> API Django (:7002) -> RabbitMQ -> Celery Worker (envoi async)
                                         -> Celery Beat (scheduled)
```

Le flux d'envoi :
1. Un service (Auth, Users...) appelle `POST /notifications/send`
2. L'API cree la notification en base (status=pending) et la place en queue RabbitMQ
3. Le Celery Worker consomme le message et envoie via le provider (SendGrid, Twilio, FCM...)
4. En cas d'echec : retry 3x backoff > autre provider > fallback inter-canal
5. Le statut est mis a jour : sent, delivered, ou failed

---

## 3. Premiere configuration

### 3.1 Creer les templates Auth

Le Service Auth envoie des emails/SMS via Notification. Il faut creer les templates **avant** de tester les fonctionnalites Auth qui envoient des notifications (register, forgot-password, magic-link).

Connectez-vous d'abord sur Auth pour obtenir un token, puis :

```bash
TOKEN="<votre-access-token>"

# Template verification email
curl -X POST http://localhost:7002/api/v1/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth_verify_email",
    "channel": "email",
    "category": "transactional",
    "subject": "Verifiez votre email - {{ platform_name }}",
    "body": "<h1>Bienvenue</h1><p>Cliquez ici pour verifier : <a href=\"{{ verification_url }}\">Verifier</a></p><p>Expire dans {{ expires_in_minutes }} minutes.</p>"
  }'

# Template OTP SMS
curl -X POST http://localhost:7002/api/v1/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth_otp_sms",
    "channel": "sms",
    "category": "security",
    "body": "Votre code AGT : {{ otp_code }}. Expire dans {{ expires_in_minutes }} min."
  }'

# Template reset password
curl -X POST http://localhost:7002/api/v1/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth_reset_password",
    "channel": "email",
    "category": "security",
    "subject": "Reinitialisation mot de passe - {{ platform_name }}",
    "body": "<p>Cliquez pour reinitialiser : <a href=\"{{ reset_url }}\">Reset</a></p><p>Expire dans {{ expires_in_minutes }} minutes.</p>"
  }'

# Template magic link
curl -X POST http://localhost:7002/api/v1/templates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "auth_magic_link",
    "channel": "email",
    "category": "transactional",
    "subject": "Connexion {{ platform_name }}",
    "body": "<p>Cliquez pour vous connecter : <a href=\"{{ magic_link_url }}\">Connexion</a></p><p>Expire dans {{ expires_in_minutes }} minutes.</p>"
  }'
```

### 3.2 Tester un envoi

```bash
curl -X POST http://localhost:7002/api/v1/notifications/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<uuid-user>",
    "channels": ["in_app"],
    "template_name": "auth_verify_email",
    "variables": {"verification_url": "http://example.com", "expires_in_minutes": 60, "platform_name": "AGT Market"}
  }'
```

Note : le canal `in_app` fonctionne toujours (pas de provider externe). Pour `email` et `sms`, configurez les API keys des providers dans `.env`.

### 3.3 Configurer les providers (optionnel en dev)

Dans `.env` :
```
# Email (SendGrid)
SENDGRID_API_KEY=SG.xxxxx

# SMS (Twilio)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_FROM_NUMBER=+1234567890

# Push (Firebase)
FCM_SERVER_KEY=xxxxx
```

Sans ces cles, les envois email/SMS echoueront (mais la notification sera cree en base avec status=failed, et un fallback in-app sera tente).

---

## 4. Utilisation courante

### Envoyer une notification

```bash
curl -X POST http://localhost:7002/api/v1/notifications/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<uuid>",
    "channels": ["email", "in_app"],
    "template_name": "order_confirmed",
    "variables": {"order_id": "ORD-123", "total": "15000 FCFA"},
    "category": "transactional",
    "priority": "high",
    "idempotency_key": "order-confirm-ORD-123"
  }'
```

### Notifications in-app

```bash
# Lister
curl http://localhost:7002/api/v1/users/<uid>/notifications \
  -H "Authorization: Bearer $TOKEN"

# Badge (non lues)
curl http://localhost:7002/api/v1/users/<uid>/notifications/unread-count \
  -H "Authorization: Bearer $TOKEN"

# Marquer comme lue
curl -X PUT http://localhost:7002/api/v1/users/<uid>/notifications/<nid>/read \
  -H "Authorization: Bearer $TOKEN"

# Tout marquer lu
curl -X PUT http://localhost:7002/api/v1/users/<uid>/notifications/read-all \
  -H "Authorization: Bearer $TOKEN"
```

### Campagnes (envoi en masse)

```bash
curl -X POST http://localhost:7002/api/v1/campaigns \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Promo Noel 2026",
    "template_name": "promo_noel",
    "channel": "email",
    "user_ids": ["<uid1>", "<uid2>", "<uid3>"],
    "variables": {"discount": "20%"},
    "throttle_per_second": 5
  }'

# Suivre la progression
curl http://localhost:7002/api/v1/campaigns/<campaign-id>/progress \
  -H "Authorization: Bearer $TOKEN"
```

### Preferences utilisateur

```bash
# Lire
curl http://localhost:7002/api/v1/users/<uid>/notification-preferences \
  -H "Authorization: Bearer $TOKEN"

# Modifier
curl -X PUT http://localhost:7002/api/v1/users/<uid>/notification-preferences \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channels": {"email": true, "sms": false, "push": true},
    "categories": {"marketing": false}
  }'
```

Note : `security` est toujours force a `true` (non modifiable).

---

## 5. RabbitMQ Management

Accessible sur http://localhost:15672

- **Username** : guest
- **Password** : guest

Vous y verrez les queues Celery, le nombre de messages en attente, et le debit d'envoi.

---

## 6. Templates : concepts

### Resolution
Quand vous envoyez avec `template_name: "order_confirmed"` :
1. Cherche un template avec ce nom **pour la plateforme du JWT**
2. Si pas trouve, cherche un template **global** (platform_id = null)
3. Si pas trouve, erreur 404

### Variables Jinja2
Les templates utilisent Jinja2. Toute syntaxe Jinja2 est supportee :
```
Bonjour {{ name }},
{% if discount %}Vous avez {{ discount }} de reduction !{% endif %}
```

### Versioning
Quand vous faites `PUT /templates/{id}`, l'ancienne version est archivee et une nouvelle est creee. On peut voir l'historique via `GET /templates/{id}/versions`.

### Preview
Avant d'envoyer, testez le rendu :
```bash
curl -X POST http://localhost:7002/api/v1/templates/<id>/preview \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"variables": {"name": "Gabriel", "discount": "20%"}}'
```

---

## 7. Tests

```bash
docker compose exec notification python -m pytest -v
```

15 tests couvrant : modeles, templates, envoi, idempotency, in-app.

---

## 8. Ports et credentials

| Ressource | URL | Credentials |
|-----------|-----|-------------|
| API Notification | http://localhost:7002 | JWT Bearer |
| Swagger | http://localhost:7002/api/v1/docs/ | - |
| RabbitMQ Management | http://localhost:15672 | guest / guest |
| PostgreSQL | localhost:5434 | notif_user / notif_password |
| Redis | localhost:6381 | - |

---

## 9. Logs et debug

```bash
# Logs API
docker compose logs -f notification

# Logs Worker (envois)
docker compose logs -f celery-worker

# Logs Scheduler
docker compose logs -f celery-beat
```
