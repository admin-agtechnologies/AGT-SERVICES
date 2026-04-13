# ROADMAP — AGT Microservices Suite

## Objectif général
Avancer sur les prochaines étapes de l’architecture AG Technologies en travaillant une tâche à la fois, avec une démarche rigoureuse, documentée et réutilisable.

## Workflow obligatoire
Pour chaque tâche ou sous-tâche technique, nous appliquerons strictement ce cycle :
- [ ] 1. Analyse de l’existant
- [ ] 2. Conception fonctionnelle
- [ ] 3. Conception technique
- [ ] 4. Mise en place / implémentation
- [ ] 5. Tests

À la fin de chaque grande tâche (ex: Tâche 1, Tâche 2...), un commit sera effectué pour sauvegarder la progression.

---

## 1. Simuler les microservices restants et le gateway
- [x] Identifier les 3 services restants (Média, Chat, Géolocalisation) et leurs contrats d'API (CDC)
- [x] Concevoir le comportement fonctionnel MVP (bouchons stateful en RAM) pour ces services
- [x] Implémenter les simulateurs en Node.js/Express pour un déploiement léger et rapide
- [x] Vérifier la configuration du Gateway (Nginx) pour s'assurer du bon routage
- [x] Tester localement le déploiement Docker et les réponses (health checks) des simulateurs
- [x] **Commit : `feat(simulators): add media, chat, geoloc simulators`**

## 2. Prise en main et Documentation de l'Écosystème (Service par Service)
*Objectif : Maîtriser chaque service individuellement avant d'analyser les flux globaux.*

#### 2.1 Service Auth
- [ ] Analyser le CDC, le code et le `README.md` du service Auth
- [ ] Configurer et lancer le service en isolation
- [ ] Tester les endpoints clés (register, login, refresh, /me) via Swagger/Postman
- [ ] Rédiger un guide d'utilisation simple `GUIDE_AUTH.md`

#### 2.2 Service Users
- [ ] Analyser le CDC, le code et le `README.md` du service Users
- [ ] Configurer et lancer le service en isolation avec sa dépendance (Auth)
- [ ] Tester les endpoints clés (profil, by-auth, rôles, permissions)
- [ ] Rédiger un guide d'utilisation simple `GUIDE_USERS.md`

#### 2.3 Service Notification
- [ ] Analyser le CDC, le code et le `README.md` du service Notification
- [ ] Configurer et lancer le service avec ses dépendances (Auth, RabbitMQ)
- [ ] Tester les endpoints clés (création de template, envoi de notification in-app)
- [ ] Rédiger un guide d'utilisation simple `GUIDE_NOTIFICATION.md`

#### 2.4 Services restants (Subscription, Payment, Wallet, Search, Chatbot)
- [ ] Appliquer la même méthode (Analyser, Configurer, Tester, Documenter) pour chaque service restant, en respectant l'ordre des dépendances.

#### 2.5 Validation des Flux Transverses
- [ ] Analyser et tester le flux complet "Inscription -> Paiement d'un abonnement -> Vérification de quota"
- [ ] Valider la gestion de l'authentification (JWT utilisateur vs Tokens S2S) sur un cas réel
- [ ] **Commit : `feat(docs): add user guides and master ecosystem usage`**

## 3. Finalisation de la Documentation
- [ ] Relire et harmoniser tous les guides (`GUIDE_*.md`) pour assurer la cohérence
- [ ] Créer un document de synthèse de l'architecture (diagramme global, flux principaux)
- [ ] Mettre à jour le `GETTING_STARTED.md` pour refléter la méthode de déploiement complète
- [ ] **Commit : `docs(global): finalize and harmonize all documentation`**

## 4. Déployer l'Infra microservices
- [ ] Analyser l'infrastructure partagée actuelle (`docker-compose.infra.yml`)
- [ ] Vérifier la configuration des réseaux, volumes et healthchecks
- [ ] Lancer et orchestrer le déploiement local de toute l'infrastructure (11 services + infra partagée)
- [ ] Valider la bonne communication de bout en bout via le Gateway
- [ ] **Commit : `chore(infra): validate full local deployment`**

## 5. Créer le Générateur de Code (Backend Template/Framework)
- [ ] Analyser les briques communes des services Django/DRF (Auth, exceptions, pagination, Docker, etc.)
- [ ] Concevoir l'architecture du générateur (CLI, templates de fichiers `*.tpl`)
- [ ] Implémenter la commande de base : `create-service <nom-du-service>`
- [ ] Implémenter la commande de scaffolding : `generate-crud <nom-table> --fields="nom:str,prix:int"`
- [ ] Implémenter la commande `create-business-backend <nom-backend>`
- [ ] Rédiger la documentation du générateur (`README.md` du template)
- [ ] Tester en générant un nouveau service de test à partir de zéro
- [ ] **Commit : `feat(template): create backend scaffolding generator`**