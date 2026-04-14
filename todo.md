# TODO — AGT Microservices Suite
> Dernière mise à jour : 14 avril 2026
> Méthode : 5 étapes par tâche (Analyse → Fonctionnel → Technique → Implémentation → Tests)

---

## BILAN ACTUEL — 14 avril 2026

### ✅ Ce qui est terminé et validé

| Élément | État | Notes |
|---|---|---|
| Infrastructure Docker (réseau, volumes, scripts) | ✅ | deploy_mvp, deploy_all, reset_mvp, reset_all |
| Service Auth v1.0 | ✅ | JWT RS256, sessions, OAuth, 2FA, S2S, Swagger |
| Service Users v1.0 | ✅ | Profils, rôles, permissions, RBAC, documents |
| Service Notification v1.0 | ✅ | Email, SMS, push, in-app, Celery, RabbitMQ |
| Flux MVP end-to-end | ✅ | register → provisioning Users → email Mailpit |
| Communication S2S inter-services | ✅ | Tokens JWT Bearer sur tous les appels |
| Simulateurs Media, Chat, Geoloc | ✅ | Node.js/Express, stateful en RAM |
| GETTING_STARTED.md | ✅ | Guide complet du MVP |
| README.md racine | ✅ | Vue d'ensemble du projet |
| TEAM_PROMPT.md | ✅ | Prompt pour déléguer le travail à l'équipe |
| Guides vides créés | ✅ | Tous les GUIDE_*.md existent avec titres |

### ⚠️ Points d'attention connus

| # | Problème | Impact | Priorité |
|---|---|---|---|
| 1 | Body email = template brut (variables non rendues par Jinja2) | Emails illisibles en prod | Haute |
| 2 | `run.py` — encodage UTF-16 sur certains fichiers Windows | Script de fix partiel | Basse |
| 3 | Swagger warnings sur vues APIView sans serializer_class | Non bloquant, logs verbeux | Basse |
| 4 | Tests pytest existants non encore validés en intégration | Couverture à vérifier | Haute |

### 📊 État des services

| Service | Code | Tests | Documentation | S2S configuré |
|---|---|---|---|---|
| Auth | ✅ v1.0 | ⚠️ À valider | 🔄 En cours | ✅ |
| Users | ✅ v1.0 | ⚠️ À valider | 🔄 En cours | ✅ |
| Notification | ✅ v1.0 | ⚠️ À valider | 🔄 En cours | ✅ |
| Subscription | ✅ v1.0 squelette | ⬜ | ⬜ | ⬜ |
| Payment | ✅ v1.0 squelette | ⬜ | ⬜ | ⬜ |
| Wallet | ✅ v1.0 squelette | ⬜ | ⬜ | ⬜ |
| Search | ✅ v1.0 squelette | ⬜ | ⬜ | ⬜ |
| Chatbot | ✅ v1.0 squelette | ⬜ | ⬜ | ⬜ |
| Media | 🔄 Simulateur Node.js | ⬜ | ⬜ | ⬜ |
| Chat | 🔄 Simulateur Node.js | ⬜ | ⬜ | ⬜ |
| Geoloc | 🔄 Simulateur Node.js | ⬜ | ⬜ | ⬜ |

---

## PHASE A — Infrastructure & Scripts ✅ TERMINÉE

- [x] Scripts deploy_mvp / deploy_all (PS1 + SH)
- [x] Scripts reset_mvp / reset_all avec flag --clean
- [x] docker-compose.infra.yml (Gateway, RabbitMQ, Mailpit, Elasticsearch)
- [x] Réseau agt_network avec external: true
- [x] Distribution automatique des clés RSA Auth
- [x] Health checks sur tous les services

---

## PHASE B — Documentation & Tests MVP 🔄 EN COURS

> **Peut être parallélisé sur 3 devs** — utiliser `prompt/TEAM_PROMPT.md`

### B.1 Service Auth
- [x] GETTING_STARTED.md — flux MVP complet
- [ ] Valider et corriger les tests pytest existants (`pytest` depuis agt-auth/)
- [ ] Documenter tous les endpoints dans GUIDE_AUTH.md :
  - [ ] register / login / logout / refresh / /me
  - [ ] Vérification email (token + callback)
  - [ ] Forgot password / reset password
  - [ ] Magic link
  - [ ] OTP phone
  - [ ] 2FA (TOTP)
  - [ ] OAuth Google / Facebook
  - [ ] Sessions (list, revoke)
  - [ ] Gestion des plateformes S2S
  - [ ] Tokens S2S (obtention, introspection)
- [ ] Documenter les flux inter-services Auth → Users et Auth → Notification
- [ ] Commit : `docs(auth): guide complet et tests validés`

### B.2 Service Users
- [ ] Valider et corriger les tests pytest existants (`pytest` depuis agt-users/)
- [ ] Documenter tous les endpoints dans GUIDE_USERS.md :
  - [ ] Provisioning (POST /users — appelé par Auth)
  - [ ] Profil (GET/PUT /users/{id})
  - [ ] Lookup par auth_user_id (GET /users/by-auth/{id})
  - [ ] Adresses (CRUD)
  - [ ] Rôles et permissions (RBAC)
  - [ ] Métadonnées par plateforme
  - [ ] Documents
  - [ ] Sync email/phone depuis Auth
  - [ ] Soft delete / hard delete RGPD
- [ ] Documenter les flux inter-services
- [ ] Commit : `docs(users): guide complet et tests validés`

### B.3 Service Notification
- [ ] Corriger le rendu Jinja2 des templates (variables non remplacées dans le body)
- [ ] Valider et corriger les tests pytest existants
- [ ] Documenter tous les endpoints dans GUIDE_NOTIFICATION.md :
  - [ ] Création / gestion des templates
  - [ ] Envoi mono-notification (send)
  - [ ] Envoi bulk
  - [ ] Campagnes (create, start, cancel)
  - [ ] Notifications in-app (list, mark read)
  - [ ] Préférences utilisateur par canal
  - [ ] Devices (push tokens FCM)
  - [ ] Config plateforme par canal
- [ ] Documenter le flux Celery + RabbitMQ
- [ ] Documenter le pattern S2STokenService
- [ ] Commit : `docs(notification): guide complet et tests validés`

### B.4 Guides transverses
- [ ] GUIDE_SCRIPTS.md — référence complète de tous les scripts
- [ ] GUIDE_LOGS.md — comment lire les logs de chaque service
- [ ] GUIDE_NEW_SERVICE.md — démarrer un service hors MVP

---

## PHASE C — Intégration des services existants ⬜ À FAIRE

> Services avec squelette de code v1.0 — à tester, corriger et documenter

### C.1 Service Subscription (:7004)
- [ ] Lire et analyser le CDC (docs/cdc/8.subscription.txt)
- [ ] Configurer le S2S (créer plateforme dans Auth, .env)
- [ ] Lancer le service et passer les migrations
- [ ] Valider les endpoints : plans, quotas, subscriptions, organizations
- [ ] Tester le flux : créer un plan → souscrire → vérifier quota
- [ ] Corriger les bugs identifiés
- [ ] Écrire / compléter les tests pytest
- [ ] Rédiger GUIDE_SUBSCRIPTION.md
- [ ] Commit : `feat(subscription): service validé et documenté`

### C.2 Service Payment (:7005)
- [ ] Lire et analyser le CDC (docs/cdc/9.payment.txt)
- [ ] Configurer le S2S
- [ ] Lancer le service et passer les migrations
- [ ] Valider les endpoints : initiate, status, webhook, refund
- [ ] Tester l'idempotence (idempotency_key obligatoire)
- [ ] Valider les providers : Orange Money, MTN MoMo, Stripe, PayPal (mocks en dev)
- [ ] Corriger les bugs identifiés
- [ ] Écrire / compléter les tests pytest
- [ ] Rédiger GUIDE_PAYMENT.md
- [ ] Commit : `feat(payment): service validé et documenté`

### C.3 Service Wallet (:7006)
- [ ] Lire et analyser le CDC (docs/cdc/10.wallet.txt)
- [ ] Configurer le S2S
- [ ] Lancer le service et passer les migrations
- [ ] Valider le ledger double-entry (toute écriture doit être irréversible)
- [ ] Valider les endpoints : accounts, transactions, holds, cashout
- [ ] Tester l'idempotence sur toutes les opérations financières
- [ ] Corriger les bugs identifiés
- [ ] Écrire / compléter les tests pytest
- [ ] Rédiger GUIDE_WALLET.md
- [ ] Commit : `feat(wallet): service validé et documenté`

### C.4 Service Search (:7007)
- [ ] Lire et analyser le CDC (docs/cdc/5.search.txt)
- [ ] Configurer le S2S
- [ ] Lancer le service avec Elasticsearch
- [ ] Valider les endpoints : index, search, suggest, delete
- [ ] Tester l'indexation depuis un autre service (ex: Users)
- [ ] Corriger les bugs identifiés
- [ ] Écrire / compléter les tests pytest
- [ ] Rédiger GUIDE_SEARCH.md
- [ ] Commit : `feat(search): service validé et documenté`

### C.5 Service Chatbot (:7010)
- [ ] Lire et analyser le CDC (docs/cdc/7.chatbot.txt)
- [ ] Configurer le S2S + clé API LLM
- [ ] Lancer le service et passer les migrations
- [ ] Valider les endpoints : bots, conversations, knowledge base
- [ ] Tester le flux RAG (Retrieval Augmented Generation)
- [ ] Corriger les bugs identifiés
- [ ] Écrire / compléter les tests pytest
- [ ] Rédiger GUIDE_CHATBOT.md
- [ ] Commit : `feat(chatbot): service validé et documenté`

### C.6 Flux transverses (intégration complète)
- [ ] Flux : inscription → abonnement → paiement → quota vérifié
- [ ] Flux : événement métier → indexation Search → résultat retrouvable
- [ ] Flux : paiement réussi → notification email → wallet crédité
- [ ] Commit : `test(integration): flux transverses validés`

---

## PHASE D — Services simulés → Vrais services ⬜ À FAIRE

> Remplacer les simulateurs Node.js par de vraies implémentations

### D.1 Service Media (:7003)
- [ ] Lire et analyser le CDC (docs/cdc/4.medias.txt)
- [ ] Choisir le stack final : Node.js/NestJS ou Django
- [ ] Implémenter upload (multipart), traitement (resize, compress), stockage (local / S3)
- [ ] Endpoints : upload, get, delete, thumbnail, CDN URL
- [ ] Intégration avec Users (avatar) et autres services
- [ ] Tests et documentation
- [ ] Commit : `feat(media): implémentation complète`

### D.2 Service Chat (:7008)
- [ ] Lire et analyser le CDC (docs/cdc/6.chat.txt)
- [ ] Implémenter Socket.io, rooms, présence, messages, fichiers
- [ ] Endpoints REST + événements WebSocket
- [ ] Intégration Auth (JWT sur handshake Socket.io)
- [ ] Tests et documentation
- [ ] Commit : `feat(chat): implémentation complète`

### D.3 Service Geoloc (:7009)
- [ ] Lire et analyser le CDC (docs/cdc/11.geoloc.txt)
- [ ] Implémenter tracking GPS, geofencing, zones
- [ ] Endpoints : position, zones, alertes
- [ ] Intégration avec Notification (alertes géofencing)
- [ ] Tests et documentation
- [ ] Commit : `feat(geoloc): implémentation complète`

---

## PHASE E — Backend Template (Générateur de service) ⬜ À FAIRE

> Objectif : permettre de scaffolder un nouveau microservice AGT en une commande

### E.1 Analyse et conception
- [ ] Identifier les briques communes à tous les services Django (auth, exceptions, pagination, Docker, settings pattern, Swagger config)
- [ ] Concevoir la CLI : `agt create-service <nom>`
- [ ] Définir les templates de fichiers (.tpl) pour chaque brique

### E.2 Implémentation du générateur
- [ ] CLI de base : `agt create-service <nom>` — génère la structure complète
- [ ] Générateur CRUD : `agt generate-crud <table> --fields="nom:str,prix:int"` — génère model + serializer + view + url + test
- [ ] Générateur backend complet : `agt create-backend <nom>` — service métier prêt à déployer
- [ ] Templates inclus : authentication.py, settings.py, Dockerfile, docker-compose.yml, pytest.ini, .env.example

### E.3 Validation
- [ ] Générer un service test à partir de zéro avec le générateur
- [ ] Vérifier que le service généré démarre, passe les migrations et les tests
- [ ] Documenter le générateur dans un README dédié
- [ ] Commit : `feat(template): backend scaffolding generator`

---

## PHASE F — Frontend Next.js Template ⬜ À FAIRE

> Objectif : un template Next.js prêt à consommer les APIs AGT

### F.1 Template frontend générique
- [ ] Initialiser un projet Next.js avec TypeScript, Tailwind CSS, shadcn/ui
- [ ] Intégration Auth AGT :
  - [ ] Login / Register / Logout
  - [ ] Gestion des tokens JWT (access + refresh)
  - [ ] Intercepteur axios/fetch avec refresh automatique
  - [ ] Protection des routes (middleware Next.js)
- [ ] SDK client AGT :
  - [ ] Client Auth (login, register, me, refresh)
  - [ ] Client Users (profil, adresses, rôles)
  - [ ] Client Notification (préférences, in-app)
  - [ ] Client générique extensible pour les autres services
- [ ] Pages de base : login, register, dashboard, profil
- [ ] Gestion d'erreurs globale (401 → redirect login, 403 → page accès refusé)
- [ ] Commit : `feat(frontend): Next.js template AGT`

### F.2 Frontends par microservice
- [ ] Interface Admin Auth (gestion plateformes, utilisateurs, sessions)
- [ ] Interface Users (annuaire, profils, rôles)
- [ ] Interface Notification (templates, campagnes, historique)
- [ ] Interface Subscription (plans, quotas, facturation)
- [ ] Interface Payment (transactions, webhooks, remboursements)
- [ ] Interface Wallet (ledger, virements, solde)
- [ ] Interface Search (requêtes, index, suggestions)
- [ ] Interface Chat (messagerie, rooms, présence)
- [ ] Interface Chatbot (bots, conversations, knowledge base)

---

## PHASE G — Dashboard de supervision ⬜ À FAIRE

> Objectif : un tableau de bord pour monitorer l'architecture en temps réel

### G.1 Dashboard technique
- [ ] Vue d'ensemble : état de santé de tous les services (health check agrégé)
- [ ] Métriques RabbitMQ (queues, messages pending, consumers)
- [ ] Métriques Elasticsearch (indices, documents, latence)
- [ ] Logs agrégés (streaming depuis tous les services)
- [ ] Alertes : service down, queue saturée, erreur rate élevé

### G.2 Dashboard métier
- [ ] Métriques Auth : inscriptions, connexions actives, taux d'erreur
- [ ] Métriques Users : utilisateurs actifs, nouveaux, supprimés
- [ ] Métriques Notification : emails envoyés, taux d'ouverture, échecs
- [ ] Métriques Payment : transactions, montants, taux de succès
- [ ] Métriques Wallet : soldes, flux financiers
- [ ] Métriques Subscription : abonnements actifs, churns, revenus

### G.3 Stack recommandée
- [ ] Frontend : Next.js + Recharts / Tremor
- [ ] Collecte métriques : Prometheus + Grafana (optionnel)
- [ ] Logs : ELK Stack ou Loki + Grafana
- [ ] Alerting : intégration Notification AGT pour les alertes critiques

---

## PHASE H — Déploiement Production ⬜ À FAIRE

> Cette phase démarre après validation complète des Phases B, C et D en local

### H.1 Préparation
- [ ] Audit de sécurité : secrets, variables d'environnement, CORS, HTTPS
- [ ] Remplacer tous les `change-me-in-production` dans les .env
- [ ] Configurer les vraies clés RSA (régénérer pour la prod)
- [ ] Configurer les providers de production (SendGrid, Twilio, Stripe, etc.)
- [ ] Audit des `DEBUG=True` → passer à `False` en prod

### H.2 Infrastructure cloud
- [ ] Choisir le provider (AWS / GCP / Azure / VPS)
- [ ] Configurer les bases de données managées (RDS PostgreSQL)
- [ ] Configurer Redis managé (ElastiCache ou Redis Cloud)
- [ ] Configurer RabbitMQ managé (CloudAMQP ou Amazon MQ)
- [ ] Configurer Elasticsearch managé (Elastic Cloud ou OpenSearch)
- [ ] Configurer le stockage objet (S3 ou compatible) pour Media

### H.3 CI/CD
- [ ] Pipeline GitHub Actions : test → build → deploy
- [ ] Docker registry (ECR, GCR ou Docker Hub)
- [ ] Déploiement Kubernetes ou Docker Swarm
- [ ] Health checks et rollback automatique

### H.4 Monitoring production
- [ ] Logs centralisés
- [ ] Alertes sur erreurs critiques
- [ ] Dashboard de supervision (Phase G)

---

## ORDRE DE PRIORITÉ RECOMMANDÉ

```
B (Documentation MVP)     ← Paralléliser sur 3 devs maintenant
    ↓
C (Intégration services)  ← Subscription → Payment → Wallet → Search → Chatbot
    ↓
E (Backend Template)      ← Pour accélérer Phase D
    ↓
D (Vrais services)        ← Media, Chat, Geoloc
    ↓
F (Frontend Template)     ← Next.js + SDK AGT
    ↓
G (Dashboard)             ← Supervision de l'archi
    ↓
H (Production)            ← Déploiement final
```

---

*AG Technologies — Usage interne — Mis à jour le 14 avril 2026*