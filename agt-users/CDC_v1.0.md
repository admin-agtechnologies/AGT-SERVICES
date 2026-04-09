# AGT Users Service - Cahier des Charges v1.0

> Version : 1.0 | Statut : Implementation-ready | Classification : Confidentiel

## 1. Perimetre

Profils utilisateurs, RBAC dynamique, documents KYC, adresses, metadonnees, audit trail.

**Hors perimetre** : authentification (Auth), stockage fichiers (Media), envoi notifications (Notification), CRUD plateformes (Auth).

**Source de verite** : Auth = identite d'authentification. Users = profil, roles, permissions.

## 2. Convention d'identite

- `{id}` dans les endpoints = `users_profiles.id` (UUID interne Users)
- `auth_user_id` = `users_auth.id` (FK logique vers Auth)
- Les services externes utilisent `GET /api/v1/users/by-auth/{authUserId}` pour resoudre
- `platform_id` = UUID Auth directement (pas de table platforms locale)
- `email` et `phone` sont **read-only** dans Users (seul Auth modifie via sync)

## 3. Modele de donnees

### Tables principales
- `users_profiles` : profil etendu (+ hard_delete_after, purge_auth_pending, deletion_error_reason)
- `addresses` : adresses utilisateur, type libre
- `user_metadata` : cle-valeur flexible par plateforme
- `audit_logs` : tracabilite de toutes les modifications

### Tables RBAC
- `roles` : roles dynamiques par plateforme (unique: platform_id + name)
- `permissions` : permissions atomiques par plateforme
- `role_permissions` : liaison role-permission
- `user_roles` : assignation role-utilisateur (unique: user + role, sans platform redondant)

### Tables Documents
- `documents` : documents KYC avec workflow pending/validated/rejected
- `document_history` : historique des versions lors de re-soumission

## 4. Modele de suppression dual (CDC v2.1)

1. **Quitter une plateforme** : `DELETE /users/{id}/platforms/{platformId}` — retire roles, metadata, archive documents. Profil et Auth intacts.
2. **Soft delete global** : `DELETE /users/{id}` — status=deleted, hard_delete_after calcule, Auth desactive via S2S.
3. **Hard delete RGPD** : `DELETE /users/{id}/permanent` — sequence securisee : deletion_in_progress, purge Auth, puis purge Users.

## 5. Endpoints

Base URL : `/api/v1`
Documentation : `/api/v1/docs/` (Swagger) | `/api/v1/redoc/`

### Profil
- `POST /users` - Provisioning (par Auth)
- `GET /users` - Listing pagine
- `GET /users/{id}` - Consultation
- `PUT /users/{id}` - Mise a jour (email/phone NON modifiables)
- `DELETE /users/{id}` - Soft delete global
- `GET /users/by-auth/{authUserId}` - Lookup par auth_user_id
- `DELETE /users/{id}/platforms/{platformId}` - Quitter plateforme
- `DELETE /users/{id}/permanent` - Hard delete RGPD
- `PUT /users/{id}/photo` - Photo profil
- `GET /users/search` - Recherche
- `GET /users/stats` - Statistiques

### Sync (par Auth)
- `POST /users/status-sync` - Sync statut
- `POST /users/sync` - Sync email/phone

### Adresses
- `POST/GET /users/{id}/addresses` - CRUD
- `PUT/DELETE /users/{id}/addresses/{addressId}`
- `PUT /users/{id}/addresses/{addressId}/default`

### Roles
- `POST/GET /platforms/{platformId}/roles` - CRUD roles
- `POST/GET /platforms/{platformId}/permissions` - CRUD permissions
- `POST/DELETE /platforms/{platformId}/roles/{roleId}/permissions` - Liaison
- `POST/GET /users/{id}/roles` - Assignation
- `DELETE /users/{id}/roles/{roleId}`
- `GET /users/{id}/permissions/check` - Verification (cache Redis)

### Documents
- `POST/GET /users/{id}/documents` - Attacher/lister
- `PUT /users/{id}/documents/{docId}/status` - Valider/rejeter
- `GET /users/{id}/documents/{docId}/history` - Historique
- `DELETE /users/{id}/documents/{docId}`

### Metadata
- `PUT/GET /users/{id}/metadata/{platformId}` - Upsert/lecture
- `DELETE /users/{id}/metadata/{platformId}/{key}`

## 6. Contrats inter-services

### Auth vers Users
- Provisioning : `POST /api/v1/users`
- Sync status : `POST /api/v1/users/status-sync`
- Sync credentials : `POST /api/v1/users/sync`

### Users vers Auth
- Deactivation S2S : `POST /auth/admin/deactivate/{authUserId}`
- Purge RGPD : `DELETE /auth/admin/purge/{authUserId}`

### Users vers Notification
- Alertes : role_assigned, role_removed, document_validated, document_rejected

### Users vers Media
- Upload direct frontend, Users stocke media_id
- Suppression fichiers au hard delete

## 7. Port

Service : **7001**

---

*AG Technologies - Users Service CDC v1.0 - Confidentiel*
