# AGT Notification Service - Cahier des Charges v1.0

> Version : 1.0 | Statut : Implementation-ready | Classification : Confidentiel

## 1. Perimetre

Envoi multi-canal (email, SMS, push, in-app, WhatsApp), templates dynamiques Jinja2, campagnes, preferences utilisateur, notifications planifiees, device tokens.

## 2. Stack

| Composant | Technologie |
|-----------|-------------|
| Framework | Django 5.x + DRF |
| Workers | Celery 5.x |
| Broker | RabbitMQ 3.13 |
| Cache | Redis 7+ |
| Templates | Jinja2 |
| Doc API | drf-spectacular |

## 3. Modele de donnees

11 tables : notifications, notification_logs, user_preferences, scheduled_notifications, platform_channel_config, templates, template_versions, template_variables, campaigns, campaign_recipients, device_tokens.

## 4. Providers

| Canal | Provider 1 | Provider 2 |
|-------|-----------|-----------|
| Email | SendGrid | Mailgun |
| SMS | Twilio | Vonage |
| Push | FCM | - |
| WhatsApp | Meta Cloud API | - |

Strategie fallback : retry meme provider (3x backoff) > autre provider meme canal > fallback inter-canal (sauf security).

## 5. Endpoints

### Envoi
- `POST /notifications/send` - Envoi mono/multi-canal
- `POST /notifications/send-bulk` - Envoi masse (max 100)

### In-App
- `GET /users/{id}/notifications` - Lister
- `GET /users/{id}/notifications/unread-count` - Badge
- `PUT /users/{id}/notifications/{nId}/read` - Marquer lue
- `PUT /users/{id}/notifications/read-all` - Tout lire
- `DELETE /users/{id}/notifications/{nId}` - Supprimer

### Templates
- `POST/GET /templates` - CRUD
- `GET /templates/{id}` - Detail
- `PUT /templates/{id}` - Nouvelle version
- `POST /templates/{id}/preview` - Preview
- `GET /templates/{id}/versions` - Historique

### Campagnes
- `POST/GET /campaigns` - CRUD
- `GET /campaigns/{id}` - Detail
- `GET /campaigns/{id}/progress` - Progression
- `POST /campaigns/{id}/cancel` - Annuler

### Preferences
- `GET/PUT /users/{id}/notification-preferences`

### Device Tokens
- `POST/GET /users/{id}/device-tokens`
- `DELETE /users/{id}/device-tokens/{tId}`

### Config
- `GET/PUT /platforms/{id}/channels-priority`

## 6. Templates requis par Auth

| Nom | Canal | Variables |
|-----|-------|-----------|
| auth_verify_email | email | verification_url, expires_in_minutes, platform_name |
| auth_otp_sms | sms | otp_code, expires_in_minutes, platform_name |
| auth_reset_password | email | reset_url, expires_in_minutes, platform_name |
| auth_magic_link | email | magic_link_url, expires_in_minutes, platform_name |

## 7. Port

Service : **7002** | RabbitMQ Management : **15672**

---

*AG Technologies - Notification Service CDC v1.0 - Confidentiel*
