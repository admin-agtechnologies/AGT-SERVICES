# AGT Chat Service - Simulateur MVP (v1.0)

> **Attention :** Ceci est un simulateur stateful en mémoire vive (RAM). Les conversations et messages sont perdus au redémarrage.

Ce simulateur permet de tester les flux de messagerie temps réel (WebSocket) et de répondre aux appels S2S du service Chatbot (transfert humain).

## Démarrage rapide

```bash
docker compose up -d --build
curl http://localhost:7008/api/v1/chat/health
```

## Endpoints REST simulés

Base URL : `http://localhost:7008/api/v1/chat`

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/health` | État du simulateur |
| `POST` | `/conversations/transfer` | Simule la réception d'un transfert depuis le Chatbot |
| `GET` | `/conversations` | Liste les conversations en mémoire |
| `POST` | `/conversations/{id}/messages` | Ajoute un message (fallback REST) |
| `GET` | `/conversations/{id}/messages` | Historique des messages |

## WebSocket (Socket.io)

Path : `/socket.io/`

- **Écouter :** `message:new`
- **Émettre :** `join_conversation` (payload: `convId`), `message:send` (payload: `{conversation_id, content, sender_id}`)
