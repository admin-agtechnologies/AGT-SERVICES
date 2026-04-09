# Service Users v1.0 - Guide d'utilisation

> Ce guide explique comment configurer, demarrer et utiliser le service Users de l'ecosysteme AGT.

## 1. Demarrage

### Prerequis
- Docker Desktop **demarre** (icone verte)
- **Service Auth demarre en premier** (pour la cle publique RSA)

### Lancement

**Windows :**
```powershell
cd agt-users
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\setup.ps1
```

**Linux/macOS :**
```bash
cd agt-users
bash scripts/setup.sh
```

Le script copie automatiquement la cle publique depuis `../agt-auth/keys/public.pem`. Si le chemin est different, copiez manuellement :
```bash
cp <chemin-vers-auth>/keys/public.pem keys/auth_public.pem
```

### Verification

```
curl http://localhost:7001/api/v1/health
```

### Documentation API interactive

- **Swagger UI** : http://localhost:7001/api/v1/docs/
- **ReDoc** : http://localhost:7001/api/v1/redoc/

---

## 2. Comment ca marche

### Lien avec Auth
Le Service Users ne gere **pas** l'authentification. Il gere les **profils etendus** : nom, prenom, adresses, roles, permissions, documents KYC.

Le flux est :
1. L'utilisateur s'inscrit sur **Auth** (`POST /auth/register`)
2. Auth appelle automatiquement **Users** (`POST /users`) pour creer le profil
3. Le profil Users est lie a Auth par `auth_user_id`

### Convention d'identite
- `auth_user_id` = l'UUID de l'utilisateur dans Auth (= `sub` du JWT)
- `id` dans les endpoints Users = l'UUID interne du profil Users
- Pour passer de l'un a l'autre : `GET /users/by-auth/{auth_user_id}`

### Email et phone sont read-only
Les champs `email` et `phone` dans Users sont synchronises depuis Auth uniquement. L'endpoint `PUT /users/{id}` ne permet pas de les modifier. Seul Auth peut les changer via `POST /users/sync`.

---

## 3. Utilisation

### 3.1 Obtenir un token

Tout passe par Auth. Connectez-vous d'abord :
```bash
curl -X POST http://localhost:7000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "gabriel@agt.com", "password": "MonMotDePasse123!", "platform_id": "<UUID>"}'
```

Recuperez l'`access_token` de la reponse.

### 3.2 Consulter un profil

```bash
# Par ID Users
curl http://localhost:7001/api/v1/users/<user-id> \
  -H "Authorization: Bearer <token>"

# Par auth_user_id (lookup)
curl http://localhost:7001/api/v1/users/by-auth/<auth-user-id> \
  -H "Authorization: Bearer <token>"
```

### 3.3 Modifier un profil

```bash
curl -X PUT http://localhost:7001/api/v1/users/<user-id> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Gabriel", "last_name": "Doe", "gender": "male"}'
```

Note : `email` et `phone` ne sont **pas** modifiables ici (read-only, source = Auth).

### 3.4 Gerer les adresses

```bash
# Ajouter
curl -X POST http://localhost:7001/api/v1/users/<id>/addresses \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"type": "home", "street": "123 Rue Test", "city": "Yaounde", "country": "Cameroun"}'

# Lister
curl http://localhost:7001/api/v1/users/<id>/addresses \
  -H "Authorization: Bearer <token>"
```

### 3.5 RBAC : Roles et Permissions

Le RBAC est **100% dynamique** — aucun role ou permission n'est hardcode.

```bash
# 1. Creer un role pour une plateforme
curl -X POST http://localhost:7001/api/v1/platforms/<platform-id>/roles \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "vendeur", "description": "Vendeur sur la marketplace"}'

# 2. Creer une permission
curl -X POST http://localhost:7001/api/v1/platforms/<platform-id>/permissions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "create_product", "description": "Peut creer un produit"}'

# 3. Attacher la permission au role
curl -X POST http://localhost:7001/api/v1/platforms/<platform-id>/roles/<role-id>/permissions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"permission_id": "<perm-id>"}'

# 4. Assigner le role a un utilisateur
curl -X POST http://localhost:7001/api/v1/users/<user-id>/roles \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"role_id": "<role-id>"}'

# 5. Verifier une permission (cache Redis, < 200ms)
curl "http://localhost:7001/api/v1/users/<user-id>/permissions/check?platform_id=<pid>&permission=create_product" \
  -H "Authorization: Bearer <token>"
```

Reponse :
```json
{"user_id": "...", "platform_id": "...", "permission": "create_product", "granted": true, "via_role": "vendeur"}
```

### 3.6 Documents KYC

```bash
# Attacher un document
curl -X POST http://localhost:7001/api/v1/users/<id>/documents \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"platform_id": "<pid>", "doc_type": "identity_card", "media_id": "<uuid-du-fichier>"}'

# Valider un document (admin)
curl -X PUT http://localhost:7001/api/v1/users/<id>/documents/<doc-id>/status \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "validated", "comment": "Document conforme"}'
```

---

## 4. Modele de suppression

3 niveaux progressifs :

| Action | Endpoint | Effet |
|--------|----------|-------|
| Quitter une plateforme | `DELETE /users/{id}/platforms/{pid}` | Retire roles + metadata + archive docs. Profil intact. |
| Soft delete global | `DELETE /users/{id}` | Status=deleted, Auth desactive, hard_delete planifie (30j) |
| Hard delete RGPD | `DELETE /users/{id}/permanent` | Purge Auth + Users. Irreversible. |

---

## 5. Tests

```bash
docker compose exec users python -m pytest -v
```

17 tests couvrant : modeles, CRUD, sync, by-auth, leave-platform, RBAC.

---

## 6. Ports et credentials

| Ressource | URL |
|-----------|-----|
| API Users | http://localhost:7001 |
| Swagger | http://localhost:7001/api/v1/docs/ |
| PostgreSQL | localhost:5433 (users_user / users_password) |
| Redis | localhost:6380 |
