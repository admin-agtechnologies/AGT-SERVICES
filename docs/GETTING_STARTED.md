# AGT Microservices - Getting Started (Guide de Démarrage)

Bienvenue dans l'écosystème microservices d'AG Technologies. Ce guide vous accompagne pas à pas pour lancer, configurer et comprendre l'environnement de développement local (MVP).

---

## 1. Architecture du MVP (Minimum Viable Product)

Pour développer et tester les flux de base (Inscription, Profil, Fichiers), nous déployons un sous-ensemble de l'architecture complète. Le **MVP** se compose de :

### Services Métier
*   **Auth (7000) :** Gère l'identité, les tokens JWT, la sécurité (2FA) et le registre des plateformes.
*   **Users (7001) :** Gère les profils étendus, les rôles (RBAC) et les documents KYC.
*   **Notification (7002) :** Orchestre l'envoi des emails, SMS et push via des files d'attente.
*   **Média (7003) :** Gère l'upload, le traitement et le stockage des fichiers. *(Note : Le service final en NestJS n'étant pas encore terminé, nous utilisons un simulateur léger pour le MVP afin de ne pas bloquer les autres services).*

### Infrastructure Partagée
*   **API Gateway (Nginx) :** Point d'entrée unique de l'écosystème sur le port `80`.
*   **RabbitMQ :** Bus de messages pour la communication asynchrone entre les services.
*   **Mailpit :** Serveur SMTP local de développement. Il intercepte tous les emails envoyés par le service Notification pour éviter de spammer de vraies adresses. Accessible sur `http://localhost:8025`.
*   **PostgreSQL & Redis :** Chaque service métier possède sa propre base de données et son propre cache, isolés des autres.

---

## 2. Configuration Initiale

Avant de lancer les services, configurez la clé d'administration globale :

1. Allez dans le dossier `agt-auth/`.
2. Copiez `.env.example` vers `.env` (si ce n'est pas déjà fait).
3. Ouvrez `agt-auth/.env` et modifiez la variable `ADMIN_API_KEY` :
   ```env
   ADMIN_API_KEY=votre-cle-secrete-admin-123
   ```
   *Cette clé sera utilisée pour les opérations sensibles (création de plateforme, blocage d'utilisateur).*

---

## 3. Lancement du MVP

Des scripts automatisés à la racine du projet orchestrent le démarrage (respect des dépendances et partage des clés RSA).

**Sur Windows (PowerShell en administrateur) :**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\deploy_mvp.ps1
```

**Sur Linux / macOS :**
```bash
bash deploy_mvp.sh
```

Vérifiez que tout fonctionne avec `docker ps`. Tous les conteneurs doivent avoir le statut `Up` et `(healthy)`.

---

## 4. Génération et Application des Migrations

Lors du premier lancement, les bases de données sont vides. Il faut générer et appliquer les schémas de base de données.

Exécutez ces commandes dans votre terminal :

**Pour Auth :**
```bash
docker exec -it agt_auth_service python manage.py makemigrations authentication platforms
docker exec -it agt_auth_service python manage.py migrate
```

**Pour Users :**
```bash
docker exec -it agt_users_service python manage.py makemigrations users roles documents
docker exec -it agt_users_service python manage.py migrate
```

**Pour Notification :**
```bash
docker exec -it agt_notif_service python manage.py makemigrations notifications templates_mgr campaigns devices
docker exec -it agt_notif_service python manage.py migrate
```

---

## 5. Premier Flux Complet : Comprendre les Microservices

Nous allons créer une plateforme, inscrire un utilisateur, et valider son email. Tout se fait via le **Swagger UI**.

### Étape A : Créer la plateforme
1. Ouvrez le Swagger Auth : `http://localhost:7000/api/v1/docs/`
2. Allez sur `POST /api/v1/auth/platforms` et cliquez sur **Try it out**.
3. Header `X-Admin-API-Key` : mettez la clé définie à l'étape 2.
4. Body :
   ```json
   {
     "name": "AGT Market",
     "slug": "agt-market",
     "allowed_auth_methods": ["email", "phone", "magic_link"],
     "allowed_redirect_urls": ["http://localhost:3000/callback"]
   }
   ```
5. **Execute**. Copiez l'UUID du champ `"id"` dans la réponse. C'est votre `platform_id`.

> **Que se passe-t-il sous le capot ?**
> Le service Auth valide votre clé Admin, génère un `client_secret` chiffré, et enregistre la plateforme dans sa base de données `agt_auth_db`. Cette plateforme est désormais reconnue par tout l'écosystème.

### Étape B : Inscrire un utilisateur
1. Sur le Swagger Auth, allez sur `POST /api/v1/auth/register` et cliquez sur **Try it out**.
2. Header `X-Platform-Id` : collez l'UUID copié à l'étape A.
3. Body :
   ```json
   {
     "email": "test@agt.com",
     "password": "Password123!",
     "method": "email"
   }
   ```
4. **Execute**. Vous obtenez un `201 Created`.

> **Que se passe-t-il sous le capot ? (Chorégraphie inter-services)**
> 1. **Auth** hache le mot de passe et crée l'utilisateur dans sa base.
> 2. **Auth** fait un appel HTTP (S2S) au service **Users** (`POST /api/v1/users`) pour lui dire : *"Un nouvel utilisateur s'est inscrit, provisionne son profil"*. Users crée le profil dans sa propre base.
> 3. **Auth** génère un token de vérification, puis fait un appel HTTP au service **Notification** pour demander l'envoi de l'email de bienvenue.
> 4. **Notification** enregistre la demande en base, la place dans **RabbitMQ**, et un **Worker Celery** la consomme pour envoyer l'email vers **Mailpit**.

### Étape C : Vérifier l'email via Mailpit
1. Ouvrez Mailpit : `http://localhost:8025`
2. Ouvrez l'email "Vérifiez votre email - AGT Market".
3. Copiez le `token` présent dans le lien.

### Étape D : Valider l'email
1. Sur le Swagger Auth, allez sur `POST /api/v1/auth/verify-email`.
2. Body : `{"token": "le-token-copie"}`
3. **Execute**. Réponse `200 OK`.

> **Que se passe-t-il sous le capot ?**
> Auth vérifie le hash du token dans sa base. S'il est valide et non expiré, il passe le champ `email_verified` à `true` et marque le token comme utilisé.

---

## 6. Commandes Utiles (Debug & Reset)

**Voir les logs en direct (très utile pour le debug) :**
```bash
docker logs --tail 50 -f agt_gateway          # Logs du routeur Nginx
docker logs --tail 50 -f agt_auth_service     # Logs de l'API Auth
docker logs --tail 50 -f agt_users_service    # Logs de l'API Users
docker logs --tail 50 -f agt_notif_service    # Logs de l'API Notification
docker logs --tail 50 -f agt_notif_worker     # Logs des envois d'emails/SMS (Celery)
docker logs --tail 50 -f agt_media_simulator  # Logs des uploads de fichiers
```

**Arrêter l'environnement :**
```bash
docker stop $(docker ps -aq)
```

**Réinitialiser complètement (Attention : supprime bases de données et réseaux) :**
```bash
docker rm -f $(docker ps -aq)
docker volume rm $(docker volume ls -q)
docker network prune -f
```

---

## 7. Prochaines Étapes

Maintenant que l'infrastructure de base est comprise, vous pouvez approfondir chaque domaine :

*   **Approfondir l'Authentification :** Testez le login, le refresh token via les cookies, et la sécurité 2FA. $\rightarrow$ [Voir le Guide Auth](./GUIDE_AUTH.md)
*   **Gestion du Profil et RBAC :** Connectez-vous, récupérez votre JWT, et utilisez le Swagger Users (`http://localhost:7001/api/v1/docs/`) pour modifier votre profil ou créer des rôles dynamiques. $\rightarrow$[Voir le Guide Users](./GUIDE_USERS.md)
*   **Gestion des Notifications :** Créez des templates dynamiques avec variables et testez les notifications In-App. $\rightarrow$ [Voir le Guide Notification](./GUIDE_NOTIFICATION.md)
*   **Gestion des Abonnements :** Découvrez comment créer des plans, des quotas et gérer le cycle de vie B2B/B2C. $\rightarrow$ [Voir le Guide Subscription](./GUIDE_SUBSCRIPTION.md)
*   **Gestion des Médias :** Testez l'upload d'une photo de profil via le simulateur Média sur le port `7003`.
