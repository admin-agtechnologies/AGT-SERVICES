# GUIDE COMPLET — Service Chatbot AGT
> **AG Technologies** — `agt-chatbot` — Port `7010` — Version `1.0`  
> Ce guide vous accompagne de zéro à un bot IA fonctionnel, étape par étape.  
> Accessible à un débutant, complet pour un développeur confirmé.

---

## Table des matières

1. [Qu'est-ce que le Service Chatbot ?](#1-quest-ce-que-le-service-chatbot)
2. [Pré-requis et Démarrage](#2-pré-requis-et-démarrage)
3. [Vérifier que le Service est Opérationnel](#3-vérifier-que-le-service-est-opérationnel)
4. [Obtenir un Token JWT pour Tester](#4-obtenir-un-token-jwt-pour-tester)
5. [Toutes les Routes du Service](#5-toutes-les-routes-du-service)
6. [Tests des Routes Critiques (Résultats Réels)](#6-tests-des-routes-critiques-résultats-réels)
7. [Configurer l'IA Générative (Couche 3)](#7-configurer-lia-générative-couche-3)
8. [Tests Automatisés (pytest)](#8-tests-automatisés-pytest)
9. [Résolution des Problèmes Courants](#9-résolution-des-problèmes-courants)
10. [Commandes Utiles de Référence](#10-commandes-utiles-de-référence)

---

## 1. Qu'est-ce que le Service Chatbot ?

### 1.1 Rôle dans l'architecture AGT

Le service Chatbot est l'**orchestrateur IA** de l'écosystème AGT. Il permet à n'importe quelle application de disposer d'un assistant intelligent, configurable et multicanal, sans avoir à gérer la complexité de l'intelligence artificielle.

### 1.2 Le Pipeline 4 Couches — Le cœur du service

Chaque message envoyé au bot traverse un pipeline de 4 couches dans l'ordre. **Le bot s'arrête à la première couche qui trouve une réponse.**

| Couche | Nom | Comment ça fonctionne | Vitesse |
|--------|-----|-----------------------|---------|
| **1** | Keywords / Intents | Détecte des mots-clés dans le message. Si "bonjour" est présent et qu'une intention "greeting" existe → réponse immédiate. | ⚡ ~20ms |
| **2** | Conversation Flows | Scénarios guidés (questions/réponses enchaînées). Ex : un formulaire de commande en plusieurs étapes. | ⚡ ~50ms |
| **3** | IA Générative | Appel à OpenAI ou Anthropic si les couches 1 et 2 échouent. Réponse intelligente et contextuelle. | 🐢 ~1-3s |
| **4** | Fallback | Message par défaut si aucune couche ne répond. Après 3 fallbacks consécutifs → transfert vers un agent humain. | ⚡ Immédiat |

> **Note :** La couche 2 (Flows) est présente dans l'architecture mais non implémentée dans la v1.0 (retourne toujours `null`). C'est un TODO assumé pour la v1.1.

---

## 2. Pré-requis et Démarrage

### 2.1 Ce dont vous avez besoin

> ✅ **Requis avant de commencer**
> - Docker Desktop installé et démarré
> - Le service Auth (`agt-auth`) doit tourner sur le port `7000`
> - Le fichier `keys/auth_public.pem` doit être présent dans `agt-chatbot/keys/`

### 2.2 Étape 1 — Préparer le fichier .env

Le fichier `.env` contient toutes les variables de configuration. Sans lui, le service ne peut pas démarrer.

**Windows (PowerShell) :**
```powershell
cd agt-chatbot
copy .env.example .env
```

**Linux / Mac :**
```bash
cd agt-chatbot
cp .env.example .env
```

Le fichier `.env` doit contenir :
```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgresql://chatbot_user:chatbot_password@db:5432/agt-chatbot-db
REDIS_URL=redis://redis:6379/8
AUTH_SERVICE_PUBLIC_KEY_PATH=/app/keys/auth_public.pem
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 2.3 Étape 2 — Copier la clé publique Auth

Le service Chatbot doit pouvoir vérifier les tokens JWT émis par Auth. Il a besoin de la clé publique RSA d'Auth.

**Windows :**
```powershell
# Depuis la racine AGT-SERVICES
mkdir agt-chatbot\keys -Force
copy agt-auth\keys\public.pem agt-chatbot\keys\auth_public.pem
```

**Linux / Mac :**
```bash
mkdir -p agt-chatbot/keys
cp agt-auth/keys/public.pem agt-chatbot/keys/auth_public.pem
```

### 2.4 Étape 3 — Lancer le service

On lance en mode **développement** (profil `dev`), ce qui exécute automatiquement les migrations.

```powershell
cd agt-chatbot
docker compose down
docker compose --profile dev up --build
```

> ⏱ Le premier lancement prend 1 à 3 minutes (téléchargement des images Docker et installation des dépendances Python). Les lancements suivants sont beaucoup plus rapides.

### 2.5 Étape 4 — Générer les migrations (premier lancement uniquement)

Après le premier démarrage, il faut générer et appliquer les migrations de base de données :

```powershell
docker exec agt-chatbot-dev python manage.py makemigrations bots
docker exec agt-chatbot-dev python manage.py makemigrations conversations
docker exec agt-chatbot-dev python manage.py migrate
```

**Résultat attendu :**
```
Operations to perform:
  Apply all migrations: bots, contenttypes
Running migrations:
  Applying bots.0001_initial... OK
```

---

## 3. Vérifier que le Service est Opérationnel

### 3.1 Health Check

Le health check vérifie la connexion à la base de données et au cache Redis.

```powershell
curl http://localhost:7010/api/v1/chatbot/health -UseBasicParsing
```

**Résultat attendu :**
```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "version": "1.0.0"
}
```

> ✅ Si vous voyez `status: healthy` avec `database: ok` et `redis: ok`, le service est pleinement fonctionnel.

### 3.2 Swagger UI — Documentation interactive

Le service expose une documentation interactive permettant de tester toutes les routes directement depuis votre navigateur.

> 🌐 Ouvrez : **http://localhost:7010/api/v1/docs/**

---

## 4. Obtenir un Token JWT pour Tester

Toutes les routes du Chatbot (sauf `/health`) nécessitent un token JWT valide émis par le service Auth.

### 4.1 Étape 1 — Créer une plateforme dans Auth

Une plateforme représente votre application cliente.

```powershell
$body = '{"name": "Test Platform", "slug": "test-platform", "allowed_auth_methods": ["email"]}'
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7000/api/v1/auth/platforms" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"X-Admin-Api-Key" = "change-me-admin-api-key-very-secret"} `
  -Body $body -UseBasicParsing
$resp.Content
```

**Résultat obtenu lors de nos tests :**
```json
{
  "id": "fc877f7a-8d44-413d-9a7d-6b7791379fae",
  "name": "Test Platform",
  "slug": "test-platform",
  "allowed_auth_methods": ["email"],
  "is_active": true,
  "client_secret": "f-DID173QsLNv8lcv..."
}
```

> 📌 **Notez le `platform_id` :** `fc877f7a-8d44-413d-9a7d-6b7791379fae` — vous en aurez besoin pour les étapes suivantes.

> ⚠️ Les valeurs valides pour `allowed_auth_methods` sont : `email`, `phone`, `google`, `facebook`, `magic_link`.

### 4.2 Étape 2 — Créer un compte utilisateur

```powershell
$body = '{"email": "test@agt.com", "password": "Test1234!", "first_name": "Test", "last_name": "AGT", "method": "email", "platform_id": "fc877f7a-8d44-413d-9a7d-6b7791379fae"}'
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7000/api/v1/auth/register" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"X-Platform-Id" = "fc877f7a-8d44-413d-9a7d-6b7791379fae"} `
  -Body $body -UseBasicParsing
$resp.Content
```

**Résultat obtenu :**
```json
{
  "id": "d534866d-5128-4bb1-a9d2-9fdc005c463f",
  "email": "test@agt.com",
  "email_verified": false,
  "message": "Verification email sent"
}
```

### 4.3 Étape 3 — Se connecter et récupérer le token

```powershell
$body = '{"email": "test@agt.com", "password": "Test1234!", "method": "email", "platform_id": "fc877f7a-8d44-413d-9a7d-6b7791379fae"}'
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7000/api/v1/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"X-Platform-Id" = "fc877f7a-8d44-413d-9a7d-6b7791379fae"} `
  -Body $body -UseBasicParsing
$resp.Content
```

**Résultat obtenu :**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 900,
  "requires_2fa": false
}
```

**Sauvegardez le token dans une variable PowerShell :**
```powershell
$token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."   # collez votre token ici
```

> ⏱ Le token expire après **15 minutes** (`expires_in: 900`). En cas d'erreur 401, reconnectez-vous.

---

## 5. Toutes les Routes du Service

| Méthode | URL | Description |
|---------|-----|-------------|
| `GET` | `/api/v1/chatbot/health` | Health check (DB + Redis) |
| `POST` | `/api/v1/chatbot/bots` | Créer un bot |
| `GET` | `/api/v1/chatbot/bots` | Lister tous les bots |
| `GET` | `/api/v1/chatbot/bots/{id}` | Détail d'un bot |
| `PUT` | `/api/v1/chatbot/bots/{id}` | Modifier un bot |
| `DELETE` | `/api/v1/chatbot/bots/{id}` | Désactiver un bot |
| `POST` | `/api/v1/chatbot/bots/{id}/intents` | Ajouter une intention |
| `GET` | `/api/v1/chatbot/bots/{id}/intents` | Lister les intentions |
| `POST` | `/api/v1/chatbot/bots/{id}/flows` | Créer un flow conversationnel |
| `GET` | `/api/v1/chatbot/bots/{id}/flows` | Lister les flows |
| `POST` | `/api/v1/chatbot/bots/{id}/knowledge/categories` | Créer une catégorie KB |
| `GET` | `/api/v1/chatbot/bots/{id}/knowledge/categories` | Lister les catégories KB |
| `POST` | `/api/v1/chatbot/bots/{id}/knowledge/entries` | Ajouter une entrée KB |
| `GET` | `/api/v1/chatbot/bots/{id}/knowledge/entries` | Lister les entrées KB |
| `POST` | `/api/v1/chatbot/bots/{id}/ai-providers` | Configurer un provider IA |
| `GET` | `/api/v1/chatbot/bots/{id}/ai-providers` | Lister les providers IA |
| `POST` | `/api/v1/chatbot/converse` | ⭐ Envoyer un message au bot |
| `GET` | `/api/v1/chatbot/bots/{id}/stats` | Statistiques du bot |
| `POST` | `/api/v1/chatbot/transfers/{id}/callback` | Callback transfert humain |

---

## 6. Tests des Routes Critiques (Résultats Réels)

> Toutes les commandes et réponses ci-dessous sont les résultats **réels obtenus** lors de la session de test du 15 Avril 2026.

### 6.1 Créer un Bot — `POST /chatbot/bots`

Un bot définit son comportement, son message de secours, et le seuil de transfert humain.

```powershell
$body = '{"name": "Bot Test",
          "platform_id": "fc877f7a-8d44-413d-9a7d-6b7791379fae",
          "system_prompt": "Tu es un assistant de test AGT.",
          "fallback_message": "Je ne comprends pas. Pouvez-vous reformuler ?",
          "human_transfer_after": 3,
          "channels": ["web"]}'
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7010/api/v1/chatbot/bots" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"Authorization" = "Bearer $token"} `
  -Body $body -UseBasicParsing
$resp.Content

# Sauvegarder le bot_id
$bot_id = ($resp.Content | ConvertFrom-Json).id
```

**Résultat obtenu ✅**
```json
{
  "id": "7cb6d749-caca-4491-910c-1090a5d78bba",
  "name": "Bot Test",
  "message": "Bot created"
}
```

> 📌 **Sauvegardez le `bot_id` :** `7cb6d749-caca-4491-910c-1090a5d78bba`

---

### 6.2 Voir le Détail d'un Bot — `GET /chatbot/bots/{id}`

```powershell
$bot_id = "7cb6d749-caca-4491-910c-1090a5d78bba"
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7010/api/v1/chatbot/bots/$bot_id" `
  -Method GET `
  -Headers @{"Authorization" = "Bearer $token"} `
  -UseBasicParsing
$resp.Content
```

**Résultat obtenu ✅**
```json
{
  "id": "7cb6d749-caca-4491-910c-1090a5d78bba",
  "name": "Bot Test",
  "description": null,
  "system_prompt": "Tu es un assistant de test AGT.",
  "fallback_message": "Je ne comprends pas. Pouvez-vous reformuler ?",
  "human_transfer_after": 3,
  "channels": [{"channel": "web", "is_active": true}]
}
```

---

### 6.3 Ajouter une Intention — `POST /chatbot/bots/{id}/intents`

Une intention associe des mots-clés à une réponse prédéfinie. C'est la **couche 1** du pipeline.

```powershell
$body = '{"name": "greeting",
          "response": "Bonjour ! Je suis votre assistant AGT. Comment puis-je vous aider ?",
          "keywords": [
            {"keyword": "bonjour", "weight": 1.0},
            {"keyword": "salut",   "weight": 1.0},
            {"keyword": "hello",   "weight": 1.0}
          ]}'
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7010/api/v1/chatbot/bots/$bot_id/intents" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"Authorization" = "Bearer $token"} `
  -Body $body -UseBasicParsing
$resp.Content
```

**Résultat obtenu ✅**
```json
{
  "id": "cc7f5e18-35e1-4e60-87a6-cb3470474321",
  "name": "greeting"
}
```

---

### 6.4 Envoyer un Message au Bot — `POST /chatbot/converse`

C'est la **route principale**. On envoie un message contenant le mot-clé "bonjour" pour déclencher la couche 1.

```powershell
$body = "{`"bot_id`": `"$bot_id`", `"message`": `"Bonjour, j'ai besoin d'aide`", `"channel`": `"web`"}"
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7010/api/v1/chatbot/converse" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"Authorization" = "Bearer $token"} `
  -Body $body -UseBasicParsing
$resp.Content
```

**Résultat obtenu ✅ — Couche 1 activée**
```json
{
  "response": "Bonjour ! Je suis votre assistant AGT. Comment puis-je vous aider ?",
  "conversation_id": "8309f085-056d-4258-a7a3-3bf212805fa9",
  "layer": "layer_1_keywords",
  "intent": "greeting",
  "confidence": 1.0,
  "provider": null,
  "is_resolved": true,
  "processing_time_ms": 20
}
```

> ✅ `layer_1_keywords` confirme que le mot-clé a été détecté. `is_resolved: true` — réponse satisfaisante. `processing_time_ms: 20` — très rapide.

---

### 6.5 Tester le Fallback — Message incompréhensible

On envoie un message sans aucun mot-clé connu pour déclencher le **fallback (couche 4)**.

```powershell
$body = "{`"bot_id`": `"$bot_id`", `"message`": `"xyzqwerty blabla incomprehensible`", `"channel`": `"web`"}"
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7010/api/v1/chatbot/converse" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"Authorization" = "Bearer $token"} `
  -Body $body -UseBasicParsing
$resp.Content
```

**Résultat obtenu ✅ — Couche 4 activée**
```json
{
  "response": "Je ne comprends pas. Pouvez-vous reformuler ?",
  "conversation_id": "8f0b7af1-fcbd-4847-a780-6d4a1cf93adc",
  "layer": "layer_4_fallback",
  "is_resolved": false,
  "processing_time_ms": 33
}
```

---

### 6.6 Transfert Humain — 3 Fallbacks Consécutifs

Redis maintient un compteur de fallbacks par conversation. Après 3 fallbacks avec le **même `conversation_id`**, le bot déclenche automatiquement un transfert humain.

```powershell
$conv_id = "8f0b7af1-fcbd-4847-a780-6d4a1cf93adc"   # même conversation_id

# Fallback 2
$body = "{`"bot_id`": `"$bot_id`", `"message`": `"azerty incomprehensible`", `"channel`": `"web`", `"conversation_id`": `"$conv_id`"}"
$resp = Invoke-WebRequest -Uri "http://localhost:7010/api/v1/chatbot/converse" `
  -Method POST -ContentType "application/json" `
  -Headers @{"Authorization" = "Bearer $token"} -Body $body -UseBasicParsing
$resp.Content

# Fallback 3 — déclenche le transfert humain
$body = "{`"bot_id`": `"$bot_id`", `"message`": `"toujours incomprehensible`", `"channel`": `"web`", `"conversation_id`": `"$conv_id`"}"
$resp = Invoke-WebRequest -Uri "http://localhost:7010/api/v1/chatbot/converse" `
  -Method POST -ContentType "application/json" `
  -Headers @{"Authorization" = "Bearer $token"} -Body $body -UseBasicParsing
$resp.Content
```

**Résultat obtenu au 3ème fallback ✅**
```json
{
  "response": "Je ne comprends pas. Pouvez-vous reformuler ?\n\nJe vous transfere vers un agent humain.",
  "conversation_id": "8f0b7af1-fcbd-4847-a780-6d4a1cf93adc",
  "layer": "layer_4_fallback",
  "is_resolved": false,
  "processing_time_ms": 8
}
```

> ✅ Le message "Je vous transfere vers un agent humain." apparaît bien au 3ème fallback consécutif. Le compteur Redis fonctionne correctement.

---

### 6.7 Statistiques du Bot — `GET /chatbot/bots/{id}/stats`

```powershell
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7010/api/v1/chatbot/bots/$bot_id/stats" `
  -Method GET `
  -Headers @{"Authorization" = "Bearer $token"} `
  -UseBasicParsing
$resp.Content
```

**Résultat obtenu ✅ (après nos 4 échanges de test)**
```json
{
  "total_messages": 4,
  "resolved": 1,
  "resolution_rate": 25.0,
  "avg_processing_ms": 13.2,
  "by_layer": {
    "layer_1_keywords": 1,
    "layer_4_fallback": 3
  }
}
```

> ✅ Les stats sont cohérentes : 4 messages total, 1 résolu (le greeting), 3 fallbacks.

---

## 7. Configurer l'IA Générative (Couche 3)

Pour activer la couche 3, vous devez configurer un provider IA sur votre bot. Sans cette configuration, les messages sans keyword tombent directement en fallback.

### 7.1 Configurer OpenAI

```powershell
$body = '{"provider": "openai",
          "model": "gpt-4o-mini",
          "api_key": "sk-votre-cle-openai",
          "temperature": 0.7,
          "max_tokens": 500,
          "purpose": "conversation",
          "priority": 0}'
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7010/api/v1/chatbot/bots/$bot_id/ai-providers" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"Authorization" = "Bearer $token"} `
  -Body $body -UseBasicParsing
$resp.Content
```

### 7.2 Configurer Anthropic (Claude)

```powershell
$body = '{"provider": "anthropic",
          "model": "claude-haiku-4-5-20251001",
          "api_key": "sk-ant-votre-cle-anthropic",
          "temperature": 0.7,
          "max_tokens": 500,
          "purpose": "conversation",
          "priority": 1}'
$resp = Invoke-WebRequest `
  -Uri "http://localhost:7010/api/v1/chatbot/bots/$bot_id/ai-providers" `
  -Method POST `
  -ContentType "application/json" `
  -Headers @{"Authorization" = "Bearer $token"} `
  -Body $body -UseBasicParsing
$resp.Content
```

> 💡 **Priorité des providers :** `priority: 0` est essayé en premier. Si OpenAI échoue, Anthropic (`priority: 1`) est essayé automatiquement. C'est le **circuit breaker** intégré.

---

## 8. Tests Automatisés (pytest)

Le service inclut une suite de tests automatisés qui valide le comportement du pipeline.

### 8.1 Lancer les tests

```powershell
docker exec agt-chatbot-dev python -m pytest -v
```

### 8.2 Ce que couvrent les tests

| Classe de test | Ce qui est testé |
|----------------|-----------------|
| `TestBotModel` | Création d'un bot avec les valeurs par défaut |
| `TestLayer1Keywords` | Détection de mots-clés et fallback si aucun match |
| `TestFallbackCounter` | Compteur de fallbacks consécutifs via Redis |
| `TestConversationLog` | Enregistrement des logs de conversation en base |
| `TestHealthEndpoint` | Endpoint `/health` retourne 200 avec version `1.0.0` |
| `TestBotEndpoints` | Création de bot via API et bot introuvable (404) |

---

## 9. Résolution des Problèmes Courants

### 🔴 Port 7010 déjà utilisé

**Erreur :**
```
Bind for 0.0.0.0:7010 failed: port is already allocated
```

**Solution :**
```powershell
docker ps | findstr 7010      # identifier le container
docker compose down           # arrêter tous les containers du service
docker compose --profile dev up --build
```

---

### 🔴 Tables manquantes

**Erreur :**
```
django.db.utils.ProgrammingError: relation "bots" does not exist
```

**Solution :** Les migrations n'ont pas été appliquées.
```powershell
docker exec agt-chatbot-dev python manage.py makemigrations bots
docker exec agt-chatbot-dev python manage.py migrate
```

---

### 🔴 Token expiré (401 Unauthorized)

**Erreur :**
```json
{"valid": false, "reason": "token_expired"}
```

**Solution :** Les tokens expirent après 15 minutes. Reconnectez-vous :
```powershell
$body = '{"email": "test@agt.com", "password": "Test1234!", "method": "email", "platform_id": "fc877f7a-8d44-413d-9a7d-6b7791379fae"}'
$resp = Invoke-WebRequest -Uri "http://localhost:7000/api/v1/auth/login" `
  -Method POST -ContentType "application/json" `
  -Headers @{"X-Platform-Id" = "fc877f7a-8d44-413d-9a7d-6b7791379fae"} `
  -Body $body -UseBasicParsing
$token = ($resp.Content | ConvertFrom-Json).access_token
```

---

### 🔴 AUTH_PUBLIC_KEY non configurée

**Erreur :**
```
AuthenticationFailed: AUTH_PUBLIC_KEY non configure.
```

**Solution :** Le fichier `keys/auth_public.pem` est manquant.
```powershell
copy ..\agt-auth\keys\public.pem .\keys\auth_public.pem
docker compose restart chatbot
```

---

### 🔴 Slug déjà utilisé lors de la création de plateforme

**Erreur :**
```json
{"slug": ["Ce slug est déjà utilisé."]}
```

**Solution :** Choisissez un slug différent dans le body de la requête. Ex : `"slug": "test-platform-2"`.

---

## 10. Commandes Utiles de Référence

### Gestion du service

```powershell
# Démarrer en mode dev
docker compose --profile dev up --build

# Arrêter
docker compose down

# Voir les logs en direct
docker logs agt-chatbot-dev -f

# Ouvrir un shell dans le container
docker exec -it agt-chatbot-dev bash

# Redémarrer uniquement le service Django (sans reconstruire)
docker compose restart chatbot
```

### Base de données

```powershell
# Appliquer les migrations
docker exec agt-chatbot-dev python manage.py migrate

# Créer de nouvelles migrations
docker exec agt-chatbot-dev python manage.py makemigrations bots

# Shell Django interactif
docker exec -it agt-chatbot-dev python manage.py shell
```

### Tests

```powershell
# Lancer tous les tests
docker exec agt-chatbot-dev python -m pytest -v

# Lancer avec couverture de code
docker exec agt-chatbot-dev python -m pytest -v --cov=apps

# Lancer un test spécifique
docker exec agt-chatbot-dev python -m pytest apps/conversations/tests/test_all.py::TestLayer1Keywords -v
```

### URLs utiles

| URL | Description |
|-----|-------------|
| `http://localhost:7010/api/v1/chatbot/health` | Health check |
| `http://localhost:7010/api/v1/docs/` | Swagger UI |
| `http://localhost:7010/api/v1/redoc/` | ReDoc |

---

*AG Technologies — Guide Service Chatbot v1.0 — Usage interne — Confidentiel*  
*Testé et validé le 15 Avril 2026*