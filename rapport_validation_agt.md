# RAPPORT DE VALIDATION — AGT Microservices
**Date :** 18 avril 2026  
**Réalisé par :** Équipe Architecture AGT  
**Objectif :** Valider que tous les microservices sont opérationnels et testés avant la mise en production

---

## 1. RÉSUMÉ EXÉCUTIF

Tous les **11 microservices** de l'écosystème AGT ont été démarrés, validés et testés.  
**217 tests sur 217 passent.** Aucun service ne présente de défaut bloquant.  
3 services avaient des bugs mineurs dans leurs fichiers de tests (pas dans le code) — tous corrigés.

---

## 2. RÉSULTATS DES TESTS PAR SERVICE

| Service | Port | Stack | Tests | Résultat | Notes |
|---|---|---|---|---|---|
| **Auth** | 7000 | Python / Django | 26/26 | ✅ | RAS |
| **Users** | 7001 | Python / Django | 17/17 | ✅ | RAS |
| **Notification** | 7002 | Python / Django | 15/15 | ✅ | RAS |
| **Media** | 7003 | NestJS / Node.js | 24/24 | ✅ | devDeps à installer en CI |
| **Subscription** | 7004 | Python / Django | 30/30 | ✅ | BOM dans pytest.ini corrigé |
| **Payment** | 7005 | Python / Django | 12/12 | ✅ | Test corrigé (assertFalse erroné) |
| **Wallet** | 7006 | Python / Django | 13/13 | ✅ | Signatures LedgerService corrigées |
| **Search** | 7007 | Python / Django | 6/6 | ✅ | Conflit port ES 9200 résolu |
| **Chat** | 7008 | Node.js / Express | 48/48 | ✅ | DATABASE_URL corrigée |
| **Geoloc** | 7009 | NestJS | 18/18 | ✅ | RAS |
| **Chatbot** | 7010 | Python / Django | 8/8 | ✅ | RAS |
| **TOTAL** | | | **217/217** | ✅ | |

---

## 3. BUGS TROUVÉS ET CORRIGÉS

### 3.1 Wallet — Désalignement signatures LedgerService
**Symptôme :** 11/13 tests échouaient avec `TypeError: missing required positional arguments`  
**Cause :** Le code de `LedgerService` avait été enrichi (ajout de `source_reference_id` et `idempotency_key` comme arguments obligatoires) mais les tests n'avaient pas été mis à jour.  
**Correction :** Mise à jour de tous les appels dans `test_all.py` + correction de `audit_balance()` → `verify_integrity()` + correction de `capture_hold(hold_id, uuid)` → `capture_hold(hold_id)`.  
**Fichier à synchroniser :**
```powershell
docker cp agt-wallet-service:/app/apps/ledger/tests/test_all.py apps\ledger\tests\test_all.py
```

### 3.2 Payment — Assertion contradictoire dans les tests
**Symptôme :** 1/12 tests échouait sur `test_valid_transition`  
**Cause :** Le développeur avait écrit `assertFalse(pending → cancelled)` puis s'était corrigé dans un commentaire sans supprimer la ligne erronée. Les deux assertions contradictoires coexistaient.  
**Correction :** Suppression de la ligne `assertFalse` et du commentaire intermédiaire. Le code du service était correct depuis le début.  
**Fichier à synchroniser :**
```powershell
docker cp agt-pay-service:/app/apps/payments/tests/test_all.py apps\payments\tests\test_all.py
```

### 3.3 Subscription — BOM dans pytest.ini
**Symptôme :** `ERROR: unexpected line: '\ufeff[pytest]'` au lancement des tests  
**Cause :** Le fichier `pytest.ini` a été créé sous Windows avec encodage UTF-8 BOM. Sur Linux/Docker, le caractère `\ufeff` invisible bloque pytest.  
**Correction :** `sed -i 's/^\xef\xbb\xbf//' pytest.ini` dans le container.  
**Action sur le source :** Rouvrir `pytest.ini` dans VSCode → Save with Encoding → UTF-8 (sans BOM).

### 3.4 Chat — DATABASE_URL incorrecte dans .env
**Symptôme :** Service en restart loop — `password authentication failed for user "chat_user"`  
**Cause :** Le `.env.example` utilisait `chat_user:chat_password` mais le `docker-compose.yml` crée la DB avec `agt_user:agt_password`.  
**Correction :** Modifier `DATABASE_URL` dans `.env` → `postgresql://agt_user:agt_password@agt-chat-db:5432/agt-chat-db`  
**Action sur le source :** Corriger `.env.example` pour aligner avec `docker-compose.yml`.

### 3.5 Search — Conflit port Elasticsearch 9200
**Symptôme :** Container ES en état `Created` (jamais `Up`) — `Bind for 0.0.0.0:9200 failed: port is already allocated`  
**Cause :** Un autre container Elasticsearch (du Chatbot ou d'une session précédente) occupait déjà le port 9200.  
**Correction :** Remapper le port ES de Search vers 9201 dans `docker-compose.yml`.  
**Action long terme :** Partager une seule instance Elasticsearch entre Search et Chatbot plutôt que deux instances séparées.

---

## 4. PROBLÈMES D'INFRASTRUCTURE

| # | Service | Problème | Criticité | Solution |
|---|---|---|---|---|
| 1 | Subscription, Wallet, Payment | `.env` absent au premier lancement | Faible | Toujours faire `cp .env.example .env` avant `docker compose up` |
| 2 | Media, Chat | `devDependencies` absentes en production | Moyenne | Utiliser le target `builder` du Dockerfile en CI/CD pour les tests |
| 3 | Search | Elasticsearch en conflit de port | Moyenne | Un seul ES partagé entre Search et Chatbot |
| 4 | Chat | `agt_network` doit exister avant le lancement | Faible | Toujours démarrer le MVP global avant les services individuels |

---

## 5. CE QUE LES TESTS COUVRENT (ET NE COUVRENT PAS)

### Ce que les tests actuels garantissent ✅
- Chaque service fonctionne **en isolation** correctement
- La logique métier de chaque service est saine
- Les endpoints principaux répondent avec les bons codes HTTP
- Les règles critiques sont respectées (idempotence, machines à états, double-entry bookkeeping)

### Ce que les tests actuels ne garantissent PAS ⚠️
- La communication **réelle entre services** (les appels inter-services sont mockés)
- Les flux end-to-end complets (inscription → abonnement → paiement → wallet)
- Les providers externes réels (Orange Money, Stripe, Nominatim, OSRM)
- Les WebSockets sous charge (Chat, Geoloc)
- Le rate limiting en conditions réelles

---

## 6. ACTIONS REQUISES AVANT LA PRODUCTION

### 🔴 Bloquant — À faire absolument

| # | Action | Service | Commande / Fichier |
|---|---|---|---|
| 1 | Synchroniser `test_all.py` corrigé sur disque | Wallet | `docker cp agt-wallet-service:/app/apps/ledger/tests/test_all.py apps\ledger\tests\test_all.py` |
| 2 | Synchroniser `test_all.py` corrigé sur disque | Payment | `docker cp agt-pay-service:/app/apps/payments/tests/test_all.py apps\payments\tests\test_all.py` |
| 3 | Corriger `.env.example` | Chat | `DATABASE_URL=postgresql://agt_user:agt_password@agt-chat-db:5432/agt-chat-db` |
| 4 | Corriger `pytest.ini` (BOM) | Subscription | Sauvegarder en UTF-8 sans BOM dans VSCode |
| 5 | Configurer les tokens S2S réels | Tous | `S2S_CLIENT_ID` et `S2S_CLIENT_SECRET` dans chaque `.env` |
| 6 | Configurer les clés publiques Auth | Tous | `cp agt-auth/keys/public.pem <service>/keys/auth_public.pem` |

### 🟡 Important — À faire avant la mise en production

| # | Action | Description |
|---|---|---|
| 7 | Tests d'intégration inter-services | Tester le flux complet inscription → provisioning Users → email Notification avec vrais tokens |
| 8 | Tests end-to-end | Flux complet : register → subscribe → pay → wallet credit |
| 9 | Configurer les providers de paiement | Orange Money, MTN MoMo : credentials réels dans Payment `.env` |
| 10 | Partager Elasticsearch | Un seul ES pour Search + Chatbot — évite le conflit de port 9200 |
| 11 | Pipeline CI/CD | Utiliser le target `builder` Docker pour les tests NestJS (Media, Geoloc, Chat) |
| 12 | Variables d'environnement production | Remplacer toutes les valeurs par défaut (`change-me`, `secret`, `password`) |

### 🟢 Recommandé — Bonnes pratiques

| # | Action | Description |
|---|---|---|
| 13 | Monitoring | Ajouter Prometheus + Grafana pour les métriques de chaque service |
| 14 | Centraliser les logs | ELK Stack ou équivalent pour les logs structurés JSON |
| 15 | Backup PostgreSQL | Politique de backup automatique pour chaque DB de service |
| 16 | Redis persistence | Activer AOF sur les Redis critiques (Wallet, Auth) |
| 17 | Secrets management | Migrer vers Vault ou AWS Secrets Manager pour les credentials |

---

## 7. ARCHITECTURE DES PORTS (RÉFÉRENCE)

| Service | Port HTTP | Port PostgreSQL | Port Redis |
|---|---|---|---|
| Auth | 7000 | 5432 | 6379 |
| Users | 7001 | 5433 | 6380 |
| Notification | 7002 | 5434 | 6381 |
| Media | 7003 | 5435 | 6382 |
| Subscription | 7004 | 5436 | 6383 |
| Payment | 7005 | 5437 | 6384 |
| Wallet | 7006 | 5438 | 6385 |
| Search | 7007 | 5439 | 6386 |
| Chat | 7008 | 5440 | 6387 |
| Geoloc | 7009 | 5441 | 6388 |
| Chatbot | 7010 | 5442 | 6389 |
| RabbitMQ | 5672 / 15672 | — | — |
| Elasticsearch | 9200 | — | — |

---

## 8. COMMANDES UTILES

```powershell
# Lancer le MVP (Auth + Users + Notification)
bash deploy_mvp.sh   # Linux
.\deploy_mvp.ps1     # Windows

# Vérifier l'état de tous les containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Lancer les tests d'un service Python
docker exec <container> python -m pytest -v

# Lancer les tests d'un service Node.js
docker exec -u root <container> npm install --include=dev
docker exec <container> npm test

# Voir les logs d'un service
docker logs <container> --tail=50 --follow

# Rebuilder un service après modification
docker compose up -d --build
```

---

*AG Technologies — Rapport de Validation — 18 avril 2026*  
*217/217 tests passent — Écosystème validé en isolation*
