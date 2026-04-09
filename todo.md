# AG TECHNOLOGIES — PLAN DE MISE EN PLACE v1.0

> **Règle** : Tous les services seront livrés en **version 1.0**.
> Chaque service = CDC v1.0 mis à jour + Code ZIP complet conforme + Template de structure unifié.

---

## PHASE 0 — FONDATIONS & STANDARDS

### 0.1 Template de structure de projet unifié

- [ ] Définir le template Django/DRF (Auth, Users, Notification, Search, Chatbot, Subscription, Payment, Wallet)
- [ ] Définir le template Node.js/NestJS (Média, Geoloc)
- [ ] Définir le template Node.js/Express (Chat)
- [ ] Valider la structure commune :
  ```
  service-name/
  ├── app/              # ou src/ (NestJS)
  ├── domain/
  ├── infrastructure/
  ├── api/
  ├── tests/
  │   ├── unit/
  │   └── integration/
  ├── docker/
  │   ├── Dockerfile
  │   └── docker-compose.yml
  ├── .env.example
  ├── requirements.txt  # ou package.json
  ├── README.md
  └── CDC_v1.0.md       # CDC embarqué dans le service
  ```
- [ ] Définir les conventions de nommage (endpoints, variables, fichiers)
- [ ] Définir le format standard des réponses d'erreur
- [ ] Définir le format standard de pagination
- [ ] Définir le health check standard (DB + Redis + version)
- [ ] Définir la convention d'identité unifiée (`user_id = users_auth.id` = `sub` JWT sauf Users qui utilise `users_profiles.id` en interne)
- [ ] Définir le `.env.example` type par stack
- [ ] Définir le `docker-compose.yml` type par stack
- [ ] Définir le README template (run local, endpoints, tests, env vars)

### 0.2 Renumérotation des CDC

- [ ] Créer le mapping de versions :
  - Auth v2.1 → **Auth v1.0**
  - Users v2.1 → **Users v1.0**
  - Notification v1.2 → **Notifs v1.0**
  - Média v1.4 → **Média v1.0**
  - Search v1.2 → **Search v1.0**
  - Chat v1.2 → **Chat v1.0**
  - Chatbot v1.2 → **Chatbot v1.0**
  - Subscription v1.2 → **Subscription v1.0**
  - Payment v1.2 → **Payment v1.0**
  - Wallet v1.1 → **Wallet v1.0**
  - Geoloc v1.2 → **Geoloc v1.0**

---

## PHASE 1 — SERVICES FONDATION

### 1.1 Service Auth v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0, historique condensé
- [ ] Intégrer la convention d'identité unifiée dans le CDC
- [ ] Intégrer le template de structure dans le CDC
- [ ] Valider les contrats inter-services (Auth → Users, Auth → Notification)

#### Code — Audit & Corrections
- [ ] Corriger le bug `cleanup_expired.py` (import `models` mal placé)
- [ ] Implémenter le rate limiting Redis (sliding window) sur les endpoints critiques
- [ ] Implémenter la protection CSRF (header `X-Requested-With` sur endpoints cookie-based)
- [ ] Vérifier le contrat `UsersServiceClient` — push `POST /api/v1/users/status-sync`
- [ ] Vérifier le contrat `UsersServiceClient` — provisioning `POST /api/v1/users`
- [ ] Vérifier le contrat `UsersServiceClient` — sync email/phone `POST /api/v1/users/sync`
- [ ] Aligner la structure du projet sur le template unifié
- [ ] Mettre à jour le health check → version `"1.0.0"`
- [ ] Vérifier et compléter les tests unitaires
- [ ] Vérifier et compléter les tests d'intégration
- [ ] Vérifier le `.env.example` (toutes les variables documentées)
- [ ] Vérifier le `docker-compose.yml`
- [ ] Mettre à jour le `README.md` selon le template
- [ ] Vérifier les migrations Django

#### Livraison
- [ ] Produire le CDC Auth v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 1.2 Service Users v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0, intégrer les changements v2.1
- [ ] Documenter la convention `{id} = users_profiles.id`
- [ ] Documenter le modèle de suppression dual (quitter plateforme vs soft delete global)
- [ ] Documenter la séquence hard delete sécurisée
- [ ] Documenter les champs `hard_delete_after`, `purge_auth_pending`, `deletion_error_reason`

#### Code — Corrections structurelles (v1.0 → v2.1)
- [ ] Supprimer la table `platforms` locale — utiliser les UUID Auth directement
- [ ] Ajouter les champs manquants à `UserProfile` :
  - [ ] `hard_delete_after` (TIMESTAMPTZ)
  - [ ] `purge_auth_pending` (BOOLEAN, default false)
  - [ ] `deletion_error_reason` (TEXT)
  - [ ] `deletion_in_progress` dans `UserStatusChoice`
- [ ] Ajouter la table `audit_logs`
- [ ] Ajouter la table `document_history`
- [ ] Ajouter l'endpoint `GET /api/v1/users/by-auth/{authUserId}`
- [ ] Ajouter l'endpoint `DELETE /api/v1/users/{id}/platforms/{platformId}` (quitter une plateforme)
- [ ] Corriger `UserRole.unique_together` : `(user, role)` au lieu de `(user, role, platform)`
- [ ] Bloquer `email` et `phone` en écriture dans `UserProfileUpdateSerializer`
- [ ] Implémenter la séquence hard delete sécurisée (Users → deletion_in_progress → purge Auth → purge Users)
- [ ] Aligner la structure sur le template unifié
- [ ] Mettre à jour le health check → version `"1.0.0"`
- [ ] Vérifier et compléter les tests unitaires
- [ ] Vérifier et compléter les tests d'intégration
- [ ] Vérifier le `.env.example`
- [ ] Vérifier le `docker-compose.yml`
- [ ] Mettre à jour le `README.md`
- [ ] Générer les migrations Django

#### Livraison
- [ ] Produire le CDC Users v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 2 — SERVICES DE SUPPORT

### 2.1 Service Notification v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0
- [ ] Clarifier la convention `user_id = users_profiles.id`
- [ ] Aligner les contrats inter-services

#### Code — Corrections
- [ ] Vérifier la résolution `user_id` (users_profiles.id vs users_auth.id)
- [ ] Vérifier l'implémentation de la table `device_tokens`
- [ ] Vérifier l'implémentation de `PlatformChannelConfig`
- [ ] Vérifier la logique de fallback inter-canal dans le worker
- [ ] Vérifier la vérification user actif avant envoi (v1.2)
- [ ] Aligner la structure sur le template unifié
- [ ] Mettre à jour le health check → version `"1.0.0"`
- [ ] Vérifier les tests
- [ ] Vérifier `.env.example` et `docker-compose.yml`
- [ ] Mettre à jour le `README.md`

#### Livraison
- [ ] Produire le CDC Notification v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 2.2 Service Média v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0
- [ ] Confirmer la convention `uploaded_by = users_auth.id`, `owner_user_id = users_auth.id`

#### Code — Corrections
- [ ] Ajouter le préfixe `/api/v1` sur tous les endpoints
- [ ] Vérifier `owner_user_id` dans le modèle `MediaFile`
- [ ] Vérifier le contrat Users ↔ Média (avatar_media_id, RGPD)
- [ ] Vérifier le hard delete S2S-only
- [ ] Aligner la structure sur le template unifié (NestJS)
- [ ] Mettre à jour le health check → version `"1.0.0"`
- [ ] Vérifier les tests
- [ ] Vérifier `.env.example` et `docker-compose.yml`
- [ ] Mettre à jour le `README.md`

#### Livraison
- [ ] Produire le CDC Média v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 3 — SERVICES MÉTIER CŒUR

### 3.1 Service Subscription v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0
- [ ] Aligner avec Auth v1.0 et Users v1.0

#### Code — Implémentation from scratch
- [ ] Implémenter les modèles (Plan, PlanVersion, Subscriber, SubscriptionCycle, QuotaDefinition, QuotaUsage, QuotaReservation)
- [ ] Implémenter les endpoints REST
- [ ] Implémenter la vérification de quotas (reserve/confirm/release)
- [ ] Implémenter les événements RabbitMQ (→ Payment, → Notification)
- [ ] Implémenter les workers Celery (renewal, expiration, trial)
- [ ] Implémenter la stratégie de résilience (4 niveaux)
- [ ] Implémenter le rate limiting
- [ ] Écrire les tests unitaires et d'intégration
- [ ] Créer `.env.example`, `docker-compose.yml`, `README.md`
- [ ] Respecter le template de structure

#### Livraison
- [ ] Produire le CDC Subscription v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 3.2 Service Payment v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0
- [ ] Aligner avec Auth v1.0, Subscription v1.0

#### Code — Implémentation from scratch
- [ ] Implémenter les modèles (PaymentIntent, Transaction, WebhookEvent, ProviderConfig, PaymentMethod)
- [ ] Implémenter les endpoints REST (initiate, status, cancel, webhooks)
- [ ] Implémenter les providers (Orange Money, MTN MoMo, Stripe, PayPal)
- [ ] Implémenter les webhooks normalisés
- [ ] Implémenter l'idempotence (`idempotency_key`)
- [ ] Implémenter les événements RabbitMQ sortants (payment.confirmed/failed/cancelled)
- [ ] Implémenter la réconciliation
- [ ] Écrire les tests unitaires et d'intégration
- [ ] Créer `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Payment v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 3.3 Service Wallet v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0
- [ ] Aligner avec Auth v1.0, Payment v1.0

#### Code — Implémentation from scratch
- [ ] Implémenter les modèles (Account, LedgerTransaction, Hold, CashoutRequest, AutoSplit)
- [ ] Implémenter le ledger double-entry (OBLIGATOIRE — aucune modification/suppression d'écriture)
- [ ] Implémenter les endpoints REST (balance, transactions, transfer, cash-in, cash-out, holds)
- [ ] Implémenter la consommation des événements RabbitMQ (payment.confirmed → crédit wallet)
- [ ] Implémenter les émissions d'événements (wallet.credited, wallet.debited)
- [ ] Implémenter l'idempotence
- [ ] Écrire les tests unitaires et d'intégration
- [ ] Créer `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Wallet v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 4 — SERVICES APPLICATIFS

### 4.1 Service Search v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0

#### Code — Implémentation from scratch
- [ ] Implémenter les modèles (SearchIndex, IndexConfig, PopularSearch)
- [ ] Implémenter les endpoints REST (search, index CRUD, suggestions, boost)
- [ ] Implémenter l'intégration Elasticsearch
- [ ] Implémenter la consommation des événements RabbitMQ (indexation async via Celery)
- [ ] Implémenter la gouvernance des index (nommage, quotas)
- [ ] Écrire les tests unitaires et d'intégration
- [ ] Créer `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Search v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 4.2 Service Chat v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0

#### Code — Implémentation from scratch (Node.js/Express/Socket.io)
- [ ] Implémenter les modèles (Conversation, Participant, Message, Attachment, Reaction, ReadReceipt)
- [ ] Implémenter les endpoints REST (conversations, messages, attachments)
- [ ] Implémenter les WebSockets (Socket.io) : présence, typing, messages temps réel
- [ ] Implémenter le Redis Adapter (multi-instance)
- [ ] Implémenter l'intégration Média (fichiers)
- [ ] Implémenter le transfert opérateur
- [ ] Écrire les tests
- [ ] Créer `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Chat v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

### 4.3 Service Geoloc v1.0

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0

#### Code — Implémentation from scratch (Node.js/NestJS/Socket.io/PostGIS)
- [ ] Implémenter les modèles (TrackedEntity, GeoZone, GeoEvent, PositionHistory)
- [ ] Implémenter les endpoints REST (zones CRUD, position history, nearby)
- [ ] Implémenter les WebSockets (Socket.io) : position updates, geofence events
- [ ] Implémenter le geofencing (R-tree/quadtree in-memory)
- [ ] Implémenter les événements RabbitMQ (geofence triggers)
- [ ] Implémenter PostGIS pour le stockage spatial
- [ ] Écrire les tests
- [ ] Créer `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Geoloc v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 5 — ORCHESTRATEUR IA (DERNIER)

### 5.1 Service Chatbot v1.0

> ⚠️ Ne commence qu'après stabilisation de : Auth, Users, Chat, Notification, Média

#### CDC
- [ ] Mettre à jour le CDC : version → 1.0
- [ ] Aligner avec Chat v1.0, Search v1.0, Média v1.0

#### Code — Implémentation from scratch
- [ ] Implémenter les modèles (Bot, BotConfig, BotChannel, Flow, FlowNode, FlowAction, Intent, KnowledgeCategory, KnowledgeBaseEntry, AiProviderConfig, ConversationSession, ConversationLog, BotAction, BotStats, IngestionJob, TransferLog)
- [ ] Implémenter le Conversation Orchestrator
- [ ] Implémenter l'Action System standardisé
- [ ] Implémenter les 3 couches de réponse (rules → KB → IA)
- [ ] Implémenter les endpoints REST (bots CRUD, flows, intents, knowledge, stats)
- [ ] Implémenter le endpoint `POST /chatbot/converse`
- [ ] Implémenter le multi-provider IA (OpenAI, Anthropic) avec circuit breaker
- [ ] Implémenter le RAG (knowledge base + embeddings)
- [ ] Implémenter les workers Celery (ingestion docs, stats, health check providers)
- [ ] Écrire les tests
- [ ] Créer `.env.example`, `docker-compose.yml`, `README.md`

#### Livraison
- [ ] Produire le CDC Chatbot v1.0 final (markdown)
- [ ] Produire le ZIP du service complet
- [ ] Checklist de validation avant zip

---

## PHASE 6 — VALIDATION GLOBALE

### 6.1 Tests inter-services
- [ ] Vérifier la compatibilité Auth ↔ Users (provisioning, sync, purge)
- [ ] Vérifier la compatibilité Auth ↔ Notification
- [ ] Vérifier la compatibilité Subscription ↔ Payment (RabbitMQ)
- [ ] Vérifier la compatibilité Payment ↔ Wallet (RabbitMQ)
- [ ] Vérifier la compatibilité Chat ↔ Chatbot (transfert)
- [ ] Vérifier tous les contrats S2S

### 6.2 Documentation finale
- [ ] Vérifier que chaque ZIP contient son CDC v1.0
- [ ] Vérifier que chaque service démarre sans erreur
- [ ] Vérifier que chaque `.env.example` est complet
- [ ] Vérifier que chaque `README.md` est exploitable
- [ ] Produire le document de synthèse inter-services (contrats, ports, dépendances)

---

## RÉSUMÉ DES LIVRABLES PAR SERVICE

| # | Service | Stack | CDC v1.0 | ZIP Code | Statut |
|---|---------|-------|----------|----------|--------|
| 1 | Auth | Django/DRF | ⬜ | ⬜ | Correction |
| 2 | Users | Django/DRF | ⬜ | ⬜ | Refonte partielle |
| 3 | Notification | Django/DRF + Celery | ⬜ | ⬜ | Correction |
| 4 | Média | NestJS | ⬜ | ⬜ | Correction |
| 5 | Subscription | Django/DRF + Celery/RabbitMQ | ⬜ | ⬜ | From scratch |
| 6 | Payment | Django/DRF + RabbitMQ | ⬜ | ⬜ | From scratch |
| 7 | Wallet | Django/DRF + RabbitMQ | ⬜ | ⬜ | From scratch |
| 8 | Search | Django/DRF + Elasticsearch + Celery | ⬜ | ⬜ | From scratch |
| 9 | Chat | Express/Socket.io | ⬜ | ⬜ | From scratch |
| 10 | Geoloc | NestJS/Socket.io/PostGIS | ⬜ | ⬜ | From scratch |
| 11 | Chatbot | Django/DRF + Celery | ⬜ | ⬜ | From scratch |

---

*AG Technologies — Plan de mise en place v1.0 — Avril 2026*