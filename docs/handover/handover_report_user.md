# HANDOFF REPORT — Session du 15 avril 2026

## 1. CE QUI A ÉTÉ COMPLÉTÉ

### Corrections structurelles

- **Migrations générées et appliquées** — `users`, `roles`, `documents` (tables créées : `users_profiles`, `audit_logs`, `addresses`, `user_metadata`, `roles`, `permissions`, `role_permissions`, `user_roles`, `documents`, `document_history`)
- **Bug AuditLog corrigé** — `TypeError: Object of type date is not JSON serializable` dans `apps/users/views.py` méthode `put` → fix via `DjangoJSONEncoder`
- **Bug UserStatsView corrigé** — suppression de l'import inutile `UserRole`, ajout du statut `deletion_in_progress` dans `by_status`
- **Fix AuthServiceClient.purge_user** — un 404 Auth est maintenant traité comme un succès (utilisateur déjà inexistant = purge OK)

### Swagger — body manquants corrigés

- `POST /platforms/{platformId}/roles` — serializer `RoleCreateSerializer` ajouté
- `POST /platforms/{platformId}/permissions` — serializer `PermissionCreateSerializer` ajouté
- `POST /users/{userId}/roles` — serializer `UserRoleAssignSerializer` ajouté
- `PUT /users/{userId}/metadata/{platformId}` — schéma JSON libre ajouté via `@extend_schema`
- `POST /users/{userId}/documents` — serializer `DocumentCreateSerializer` ajouté
- `PUT /users/{userId}/documents/{docId}/status` — serializer `DocumentStatusSerializer` ajouté
- `PUT /platforms/{platformId}/roles/{roleId}` — serializer `RoleUpdateSerializer` ajouté

### Swagger — paramètres query manquants corrigés

- `GET /users` — paramètres `status`, `platform_id`, `role` ajoutés via `OpenApiParameter`
- `GET /users/search` — paramètre `q` ajouté via `OpenApiParameter`
- `GET /users/{userId}/permissions/check` — paramètres `permission` et `platform_id` ajoutés

### Routes dupliquées corrigées

- Suppression de la route `platforms/{platformId}/roles/{roleId}/permissions` (sans `perm_id`)
- Seule la route avec `perm_id` dans l'URL est conservée pour attacher ET détacher une permission
- Méthode `post` de `RolePermissionView` mise à jour — `perm_id` vient de l'URL, plus de body

### Fonctionnalités implémentées et testées

- **Hard delete RGPD** (`DELETE /users/{id}/permanent`) — séquence complète : `deletion_in_progress` → purge Auth → purge Users. Testé avec un vrai compte Auth ✅
- **Quitter une plateforme** (`DELETE /users/{id}/platforms/{platformId}`) — retire rôles, metadata, archive documents. Profil et Auth intacts ✅

### Tests manuels validés (tous les endpoints)

| Groupe        | Endpoints testés | Statut |
| ------------- | ---------------- | ------ |
| Health        | 1                | ✅     |
| Profil        | 10               | ✅     |
| Sync          | 2                | ✅     |
| Adresses      | 5                | ✅     |
| RBAC          | 12               | ✅     |
| Documents KYC | 5                | ✅     |
| Metadata      | 3                | ✅     |

### Documentation produite

- **`docs/GUIDE_USERS.md`** — guide complet 9 sections, scénario détaillé pas à pas (section 6 avec 19 sous-sections), référence rapide avec liens cliquables, troubleshooting, bugs connus

---

## 2. EN COURS

Rien en cours — toutes les tâches de la session sont terminées.

---

## 3. PROCHAINE ÉTAPE IMMÉDIATE

**Tâche AV-7 — [Payment] Lancer & démarrer les tests**

Étape 1 — Analyse de l'existant :

- Lire le CDC du service Payment (`docs/cdc/payment.txt` ou `agt-payment/CDC_v1.0.md`)
- Vérifier l'état du code existant dans `agt-payment/`
- Identifier les dépendances (Auth, Users, Wallet, RabbitMQ)

---

## 4. POINTS D'ATTENTION

| #   | Point                                                                                                                                                                                                                       | Statut        |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| 1   | **Bug Auth — pas d'endpoint pour réactiver un compte désactivé** — `POST /auth/admin/unblock` ne fonctionne que pour les comptes bloqués (brute force), pas pour les comptes désactivés. À implémenter dans Auth.           | ⚠️ Ouvert     |
| 2   | **Photo profil non testable en isolation** — `PUT /users/{id}/photo` dépend du service Média (port 7003). Tester quand Média sera lancé.                                                                                    | ⚠️ En attente |
| 3   | **Fix DjangoJSONEncoder — attention au rebuild** — toute modification de `apps/users/views.py` nécessite un `sudo docker compose up -d --build` pour être prise en compte.                                                  | ℹ️ Convention |
| 4   | **Migrations non incluses dans le repo** — à la première installation, il faut générer les migrations manuellement (voir GUIDE_USERS.md section 2).                                                                         | ⚠️ À corriger |
| 5   | **Compte Auth désactivé après soft delete** — après un `DELETE /users/{id}`, le compte Auth est désactivé. Remettre le statut Users à `active` via `/users/status-sync` ne réactive pas le compte Auth. Bug lié au point 1. | ⚠️ Ouvert     |

---

## 5. COMMANDES UTILES

```bash
# Lancer le service
cd agt-users
sudo docker compose up -d

# Lancer avec rebuild (obligatoire après modification de code)
sudo docker compose up -d --build

# Appliquer les migrations (première installation uniquement)
sudo docker compose exec users python manage.py makemigrations users
sudo docker compose exec users python manage.py makemigrations roles
sudo docker compose exec users python manage.py makemigrations documents
sudo docker compose exec users python manage.py migrate

# Lancer les tests
sudo docker compose exec users python -m pytest -v

# Consulter les logs
sudo docker compose logs users --tail=30

# Arrêter le service
sudo docker compose down

# Arrêter et supprimer les données
sudo docker compose down -v
```

**URLs utiles :**
| Service | URL |
|---------|-----|
| Swagger Users | http://localhost:7001/api/v1/docs/ |
| Swagger Auth | http://localhost:7000/api/v1/docs/ |
| Health Users | http://localhost:7001/api/v1/users/health |

**Données de test disponibles en base :**
| Donnée | Valeur |
|--------|--------|
| Platform ID | `48a8351c-8791-4845-a65e-c00e56332d2d` |
| Users profile ID (actif) | `eaf6009e-0d42-42e6-97e5-5bfde4e07fd5` |
| Auth user ID (actif) | `bb7bdaf3-2f6c-4ad7-91f8-003888e2ae99` |
| Role ID (vendeur) | `91136ba8-e099-4032-a4fd-90b69cecf625` |
| Permission ID (create_product) | `e08ce8da-36b2-4569-a730-4af1a563a545` |

---

_AG Technologies — Handoff Report — 15 avril 2026_
