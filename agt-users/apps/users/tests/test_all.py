"""
AGT Users Service v1.0 - Tests unitaires et integration.
"""
import uuid
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import UserProfile, Address, UserMetadata, UserStatusChoice, AuditLog
from apps.roles.models import Role, Permission, RolePermission, UserRole


def make_user(**kwargs):
    defaults = {
        "auth_user_id": uuid.uuid4(),
        "first_name": "Jean",
        "last_name": "Dupont",
        "email": f"jean_{uuid.uuid4().hex[:6]}@agt.com",
    }
    defaults.update(kwargs)
    return UserProfile.objects.create(**defaults)


def make_role(platform_id=None, name="vendeur"):
    pid = platform_id or uuid.uuid4()
    return Role.objects.create(platform_id=pid, name=name, description=f"Role {name}")


def make_permission(platform_id=None, name="create_product"):
    pid = platform_id or uuid.uuid4()
    return Permission.objects.create(platform_id=pid, name=name, description=f"Perm {name}")


# --- Modeles ---

class TestUserProfileModel(TestCase):
    def test_create_user(self):
        user = make_user()
        self.assertEqual(user.status, UserStatusChoice.ACTIVE)
        self.assertIsNotNone(user.auth_user_id)

    def test_soft_delete(self):
        user = make_user()
        user.soft_delete()
        user.refresh_from_db()
        self.assertEqual(user.status, UserStatusChoice.DELETED)
        self.assertIsNotNone(user.deleted_at)
        self.assertIsNotNone(user.hard_delete_after)

    def test_hard_delete(self):
        user = make_user()
        uid = user.id
        user.hard_delete()
        self.assertFalse(UserProfile.objects.filter(id=uid).exists())

    def test_full_name(self):
        user = make_user(first_name="Marie", last_name="Curie")
        self.assertEqual(user.get_full_name(), "Marie Curie")


class TestAddressModel(TestCase):
    def test_set_default(self):
        user = make_user()
        a1 = Address.objects.create(user=user, type="home", street="Rue 1", city="Yaounde", country="Cameroun", is_default=True)
        a2 = Address.objects.create(user=user, type="work", street="Rue 2", city="Douala", country="Cameroun")
        a2.set_as_default()
        a1.refresh_from_db()
        a2.refresh_from_db()
        self.assertFalse(a1.is_default)
        self.assertTrue(a2.is_default)


class TestRBACModel(TestCase):
    def test_role_permission_link(self):
        pid = uuid.uuid4()
        role = make_role(platform_id=pid)
        perm = make_permission(platform_id=pid)
        RolePermission.objects.create(role=role, permission=perm)
        self.assertEqual(RolePermission.objects.filter(role=role).count(), 1)

    def test_user_role_unique(self):
        user = make_user()
        role = make_role()
        UserRole.objects.create(user=user, role=role)
        # Doublon doit echouer
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            UserRole.objects.create(user=user, role=role)


# --- Endpoints ---

class TestHealthEndpoint(TestCase):
    def test_health(self):
        client = APIClient()
        response = client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["version"], "1.0.0")


class TestUserCRUD(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Simuler un JWT valide en bypassant l'auth
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "auth_user_id": str(uuid.uuid4())})())

    def test_create_user_provisioning(self):
        response = self.client.post("/api/v1/users", data={
            "auth_user_id": str(uuid.uuid4()),
            "first_name": "Test",
            "last_name": "User",
            "email": "test@agt.com",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_create_duplicate(self):
        auth_id = str(uuid.uuid4())
        make_user(auth_user_id=auth_id)
        response = self.client.post("/api/v1/users", data={
            "auth_user_id": auth_id,
            "email": "other@agt.com",
        }, format="json")
        self.assertEqual(response.status_code, 409)

    def test_get_user(self):
        user = make_user()
        response = self.client.get(f"/api/v1/users/{user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["auth_user_id"], str(user.auth_user_id))

    def test_update_user(self):
        user = make_user()
        response = self.client.put(f"/api/v1/users/{user.id}", data={
            "first_name": "Updated",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["first_name"], "Updated")

    def test_by_auth_lookup(self):
        user = make_user()
        response = self.client.get(f"/api/v1/users/by-auth/{user.auth_user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], str(user.id))

    @patch("apps.users.services.AuthServiceClient.deactivate_user", return_value=True)
    def test_soft_delete(self, mock_deactivate):
        user = make_user()
        response = self.client.delete(f"/api/v1/users/{user.id}")
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.status, UserStatusChoice.DELETED)
        mock_deactivate.assert_called_once()


class TestStatusSync(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "auth_user_id": str(uuid.uuid4())})())

    def test_status_sync_inactive(self):
        user = make_user()
        response = self.client.post("/api/v1/users/status-sync", data={
            "auth_user_id": str(user.auth_user_id),
            "status": "inactive",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.status, UserStatusChoice.INACTIVE)

    def test_credentials_sync(self):
        user = make_user()
        response = self.client.post("/api/v1/users/sync", data={
            "auth_user_id": str(user.auth_user_id),
            "email": "new@agt.com",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.email, "new@agt.com")


class TestLeavePlatform(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "auth_user_id": str(uuid.uuid4())})())

    def test_leave_platform(self):
        user = make_user()
        pid = uuid.uuid4()
        role = Role.objects.create(platform_id=pid, name="vendeur")
        UserRole.objects.create(user=user, role=role)
        UserMetadata.objects.create(user=user, platform_id=pid, key="shop", value="Test")

        response = self.client.delete(f"/api/v1/users/{user.id}/platforms/{pid}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["roles_removed"], 1)
        self.assertTrue(data["metadata_cleared"])
