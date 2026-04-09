"""AGT Search Service v1.0 - Tests (sans ES)."""
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from apps.indexes.models import IndexRegistry, IndexSchema, SearchConfig, SearchHistory, PopularSearch

class TestModels(TestCase):
    def test_create_index(self):
        idx = IndexRegistry.objects.create(name="products", platform_id=uuid.uuid4())
        self.assertEqual(idx.status, "active")
        self.assertEqual(idx.document_count, 0)

    def test_schema(self):
        idx = IndexRegistry.objects.create(name="test", platform_id=uuid.uuid4())
        IndexSchema.objects.create(index=idx, field_name="title", field_type="text", searchable=True)
        self.assertEqual(idx.schema_fields.count(), 1)

    def test_search_history(self):
        SearchHistory.objects.create(user_id=uuid.uuid4(), platform_id=uuid.uuid4(),
                                      index_name="products", query="test", result_count=10, took_ms=50)
        self.assertEqual(SearchHistory.objects.count(), 1)

    def test_popular_search(self):
        ps = PopularSearch.objects.create(index_name="products", platform_id=uuid.uuid4(), term="nike", search_count=42)
        self.assertEqual(ps.search_count, 42)

class TestHealth(TestCase):
    def test_health(self):
        resp = APIClient().get("/api/v1/search/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")

class TestIndexEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())
    def test_list_indexes(self):
        resp = self.client.get("/api/v1/search/indexes")
        self.assertEqual(resp.status_code, 200)
