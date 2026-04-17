# GUIDE — AGT Subscription Service

## 1. Prérequis

- Docker Desktop installé et **démarré** (icône stable dans la barre des tâches)
- Dépôt `AGT-SERVICES` cloné en local
- MVP (Auth, Users, Notification) opérationnel
- Machine fraiche avec docker Desktop et Docker compose installé et ouvert mais aucun service de notre architechture lancé

---

## 2. Démarrer le MVP

Depuis la racine `AGT-SERVICES/` :

```powershell
.\reset_mvp.ps1
```

Attendre le message final :
```
DÉPLOIEMENT MVP RÉUSSI !
```

Les 3 services doivent être healthy : Auth (:7000), Users (:7001), Notification (:7002).

---

## 3. Préparer Subscription

### 3.1 Créer le fichier .env

```powershell
cd agt-subscription
copy .env.example .env
cd ..
```

### 3.2 Copier la clé publique Auth

```powershell
copy agt-auth\keys\public.pem agt-subscription\keys\auth_public.pem
```

---

## 4. Démarrer le service

```powershell
cd agt-subscription
docker compose up -d --build
```

Attendre que les 3 containers soient up :
```
✔ Container agt-sub-db        Healthy
✔ Container agt-sub-redis     Healthy
✔ Container agt-sub-service   Running
✔ Container agt-sub-worker    Running
✔ Container agt-sub-beat      Running
```

---

## 5. Migrations

```powershell
docker compose exec -e DJANGO_SETTINGS_MODULE=config.settings subscription python manage.py makemigrations plans subscriptions quotas organizations
docker compose exec subscription python manage.py migrate
```

---

## 6. Health check

```powershell
curl http://localhost:7004/api/v1/subscriptions/health
```

Réponse attendue :
```json
{"status":"healthy","database":"ok","redis":"ok","version":"1.0.0"}
```

---

## 7. Lancer les tests

```powershell
docker compose exec subscription python -m pytest -v
```

Résultat attendu : **30 passed**

---

## 8. Swagger

```
http://localhost:7004/api/v1/docs/
```

---

> ⚠️ **Note connue** : Les dossiers `migrations/` ne sont pas commités dans le repo — il faut toujours exécuter l'étape 5 au premier démarrage.

---

Lance ça de zéro et dis-moi si tu passes toutes les étapes sans accroc. On complétera ensuite le guide avec les endpoints Swagger.