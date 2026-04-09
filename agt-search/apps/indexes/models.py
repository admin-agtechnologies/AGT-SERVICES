"""AGT Search Service v1.0 - Modeles PostgreSQL (metadata, configs, historique)."""
import uuid
from django.db import models


class IndexRegistry(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("rebuilding", "Rebuilding"), ("deleted", "Deleted")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    platform_id = models.UUIDField(db_index=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    document_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "indexes_registry"
        unique_together = [("name", "platform_id")]
        ordering = ["name"]


class IndexSchema(models.Model):
    FIELD_TYPES = [("text", "Text"), ("keyword", "Keyword"), ("number", "Number"), ("date", "Date"), ("boolean", "Boolean")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.ForeignKey(IndexRegistry, on_delete=models.CASCADE, related_name="schema_fields")
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    searchable = models.BooleanField(default=True)
    filterable = models.BooleanField(default=False)
    sortable = models.BooleanField(default=False)
    autocomplete = models.BooleanField(default=False)
    boost_weight = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "index_schemas"
        unique_together = [("index", "field_name")]


class SearchConfig(models.Model):
    index = models.OneToOneField(IndexRegistry, on_delete=models.CASCADE, primary_key=True, related_name="config")
    analyzer = models.CharField(max_length=50, default="french")
    fuzzy_enabled = models.BooleanField(default=True)
    fuzzy_distance = models.IntegerField(default=1)
    highlight_enabled = models.BooleanField(default=True)
    min_score = models.FloatField(null=True, blank=True)
    max_results = models.IntegerField(default=100)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "search_configs"


class Synonym(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.ForeignKey(IndexRegistry, on_delete=models.CASCADE, related_name="synonyms")
    term = models.CharField(max_length=100)
    equivalents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "synonyms"


class SearchHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    platform_id = models.UUIDField()
    index_name = models.CharField(max_length=100)
    query = models.TextField()
    filters_applied = models.JSONField(null=True, blank=True)
    result_count = models.IntegerField()
    took_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "search_history"
        ordering = ["-created_at"]


class PopularSearch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index_name = models.CharField(max_length=100)
    platform_id = models.UUIDField()
    term = models.CharField(max_length=255)
    search_count = models.BigIntegerField(default=0)
    last_searched_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "popular_searches"
        unique_together = [("index_name", "platform_id", "term")]
