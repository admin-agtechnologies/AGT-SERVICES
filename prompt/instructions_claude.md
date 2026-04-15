# AG TECHNOLOGIES

## RÈGLES D’IMPLÉMENTATION MICRO-SERVICES

**Version 1.1 — Référence interne**

---

# 1. PRINCIPES GLOBAUX

## 1.1 Source de vérité

* Les **CDC validés (Implementation-ready)** sont la référence absolue.
* Le code existant **n’est pas une référence fiable** s’il diverge du CDC.
* En cas de conflit : **CDC > Code existant**.

## 1.2 Philosophie d’architecture

* Architecture **microservices découplée**
* Communication :

  * REST → synchrone
  * RabbitMQ → asynchrone
* Chaque service est :

  * autonome
  * déployable indépendamment
  * responsable de ses données

---

# 2. RÈGLES DE DÉVELOPPEMENT

## 2.1 Un service = un périmètre métier

* Aucun service ne doit empiéter sur un autre
* Pas de logique métier dupliquée

## 2.2 Base de données

* **1 service = 1 base de données**
* Interdiction d’accès direct à la DB d’un autre service
* Communication uniquement via API ou événements

## 2.3 API REST

* JSON uniquement
* Versionnement recommandé (`/v1/`)
* Endpoints cohérents et explicites

Exemple :

```text
POST   /v1/subscriptions
GET    /v1/users/{id}
POST   /v1/payments/initiate
```

## 2.4 Authentification

* Basée sur **Auth Service**
* JWT obligatoire
* Support :

  * user tokens
  * service-to-service tokens (S2S)

---

# 3. COMMUNICATION INTER-SERVICES

## 3.1 REST (synchrone)

Utilisé pour :

* lecture rapide
* validation
* actions critiques

## 3.2 Event-driven (RabbitMQ)

Obligatoire pour :

* Paiement
* Wallet
* Notification
* Abonnement

Règles :

* events **idempotents**
* chaque event contient :

  * `event_id`
  * `timestamp`
  * `source`
* retry automatique

---

# 4. GESTION DES ERREURS

## 4.1 Standard

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Description"
  }
}
```

## 4.2 Idempotence

* Obligatoire pour :

  * paiements
  * wallet
  * actions critiques
* via `idempotency_key`

---

# 5. RÈGLES SPÉCIFIQUES MÉTIER

## 5.1 Abonnement

* Source des règles métier (plans, quotas)
* Aucun service ne définit ses propres quotas

## 5.2 Paiement

* Exécute uniquement les transactions externes
* Ne contient pas de logique métier

## 5.3 Wallet

* Ledger obligatoire
* **Double-entry bookkeeping requis**
* Aucune modification/suppression d’écriture

## 5.4 Search

* Index uniquement
* Ne remplace pas les DB métier

## 5.5 Chatbot

* Orchestrateur IA
* Ne contient pas de logique métier profonde

---

# 6. CONVENTIONS TECHNIQUES

## 6.1 Stack (référence actuelle)

* Backend : Python / Django / FastAPI
* DB : PostgreSQL
* Cache : Redis
* Queue : RabbitMQ
* Conteneurisation : Docker

## 6.2 Structure d’un service

```text
service-name/
├── app/
├── domain/
├── infrastructure/
├── api/
├── tests/
├── docker/
├── .env.example
├── requirements.txt
├── README.md
```

---

# 7. RÈGLES DE LIVRAISON

Chaque service doit être livré avec :

* code complet
* `.env.example`
* README (run local)
* migrations
* commandes de lancement
* endpoints testables
* dépendances documentées

---

# 8. TEST LOCAL (OBLIGATOIRE)

Avant validation :

* le service démarre sans erreur
* les endpoints principaux fonctionnent
* connexion DB OK
* variables d’environnement documentées

---

# 9. COMPATIBILITÉ USERS 2.1

* Tous les services doivent être compatibles avec **Users v2.1**
* Toute référence à Users v1.0 est interdite
* Vérifier :

  * modèles
  * rôles
  * permissions
  * endpoints

---

# 10. RÈGLES D’ÉVOLUTION

* Aucun changement breaking sans justification
* Toute modification d’API doit être explicitée
* Toujours préserver la compatibilité inter-services

---

# 11. POSTURE D’IMPLÉMENTATION

* Privilégier :

  * simplicité
  * robustesse
  * cohérence
* Éviter :

  * sur-engineering
  * duplication
  * dépendances implicites

---

# 12. TESTS (OBLIGATOIRE)

Chaque microservice doit inclure :

## 12.1 Tests unitaires

* couvrent la logique métier critique
* obligatoires dès la v1.0
* exemples :

  * Abonnement → quotas
  * Paiement → idempotence
  * Wallet → écritures ledger

## 12.2 Tests d’intégration

* testent les endpoints principaux
* vérifient DB + logique applicative

## 12.3 Structure obligatoire

```text
tests/
├── unit/
├── integration/
```

## 12.4 Exécution

* les tests doivent être exécutables avec :

```bash
pytest
```

## 12.5 Règle de validation

> ❗ Un service sans tests n’est pas considéré comme terminé

---

# 13. RÈGLE FINALE

> Un service n’est considéré terminé que s’il est :
>
> * conforme au CDC
> * testable localement
> * compatible avec les autres services
> * couvert par des tests
> * prêt à être déployé

---
# 11.1 QUALITÉ DU CODE (OBLIGATOIRE)

## 11.1.1 Lisibilité et commentaires

* Le code doit être **lisible et compréhensible sans effort**
* Les fonctions critiques doivent être **commentées**
* Les logiques complexes doivent inclure :

  * une explication du **pourquoi**
  * pas seulement du **comment**
* Pas de commentaires inutiles ou redondants

## 11.1.2 Modularité

* Le code doit être **découpé en modules clairs**
* Respect de la séparation :

  * domain (logique métier)
  * api (exposition)
  * infrastructure (DB, cache, externes)
* Les fonctions doivent être :

  * petites
  * testables
  * réutilisables

## 11.1.3 Scalabilité

* Le code doit être conçu pour :

  * supporter la montée en charge
  * éviter les dépendances fortes
* Pas de logique bloquante inutile
* Favoriser :

  * async si nécessaire
  * découplage via events
* Anticiper :

  * multi-instance
  * horizontal scaling

## 11.1.4 Maintenabilité

* Nommage explicite (pas de noms ambigus)
* Pas de duplication de code
* Respect des conventions du projet
* Toute logique métier doit être centralisée dans le bon service

## 11.1.5 Règle stricte

> ❗ Un code non lisible, non modulaire ou non maintenable est considéré comme non conforme
