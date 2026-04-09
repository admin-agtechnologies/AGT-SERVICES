"""AGT Search Service v1.0 - Views."""
import logging, time
from django.db.models import Count, Avg, Sum, F
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from apps.indexes.models import IndexRegistry, IndexSchema, SearchConfig, Synonym, SearchHistory, PopularSearch
from apps.search.es_service import ESService

logger = logging.getLogger(__name__)

class Paginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    def get_paginated_response(self, data):
        return Response({"data": data, "page": self.page.number, "total": self.page.paginator.count})


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    @extend_schema(tags=["Health"], summary="Health check")
    def get(self, request):
        db_ok = redis_ok = es_ok = True
        try:
            from django.db import connection; connection.ensure_connection()
        except Exception: db_ok = False
        try:
            from django.core.cache import cache; cache.set("h", "ok", 5); redis_ok = cache.get("h") == "ok"
        except Exception: redis_ok = False
        try:
            from apps.search.es_service import _get_es
            es = _get_es()
            es_ok = es.ping() if es else False
        except Exception: es_ok = False
        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({"status": "healthy" if db_ok and redis_ok and es_ok else "degraded",
                         "database": "ok" if db_ok else "error", "redis": "ok" if redis_ok else "error",
                         "elasticsearch": "ok" if es_ok else "error", "version": "1.0.0"}, status=code)


# --- Indexes CRUD ---

class IndexListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Indexes"], summary="Creer un index")
    def post(self, request):
        d = request.data
        name, pid = d.get("name"), d.get("platform_id")
        if not name or not pid:
            return Response({"detail": "name et platform_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        if IndexRegistry.objects.filter(name=name, platform_id=pid).exists():
            return Response({"detail": "Index existe deja."}, status=status.HTTP_409_CONFLICT)
        idx = IndexRegistry.objects.create(name=name, platform_id=pid, description=d.get("description"))
        schema = d.get("schema", [])
        for f in schema:
            IndexSchema.objects.create(index=idx, field_name=f["field_name"], field_type=f.get("field_type", "text"),
                                        searchable=f.get("searchable", True), filterable=f.get("filterable", False),
                                        sortable=f.get("sortable", False), autocomplete=f.get("autocomplete", False),
                                        boost_weight=f.get("boost_weight", 1))
        SearchConfig.objects.create(index=idx)
        es_name = f"{pid}_{name}"
        ESService.create_index(es_name, schema)
        return Response({"id": str(idx.id), "name": name, "es_index": es_name, "message": "Index created"}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Indexes"], summary="Lister les index")
    def get(self, request):
        qs = IndexRegistry.objects.filter(status="active")
        pid = request.GET.get("platform_id")
        if pid:
            qs = qs.filter(platform_id=pid)
        data = [{"id": str(i.id), "name": i.name, "platform_id": str(i.platform_id),
                 "document_count": i.document_count, "status": i.status} for i in qs]
        return Response({"data": data})


class IndexDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Indexes"], summary="Detail index avec schema")
    def get(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        fields = [{"field_name": f.field_name, "field_type": f.field_type, "searchable": f.searchable,
                    "filterable": f.filterable, "autocomplete": f.autocomplete} for f in idx.schema_fields.all()]
        return Response({"id": str(idx.id), "name": idx.name, "platform_id": str(idx.platform_id),
                         "document_count": idx.document_count, "schema": fields})

    @extend_schema(tags=["Indexes"], summary="Supprimer un index")
    def delete(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        ESService.delete_index(f"{idx.platform_id}_{index_name}")
        idx.status = "deleted"
        idx.save(update_fields=["status", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Documents ---

class DocumentIndexView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Documents"], summary="Indexer un document")
    def post(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        doc_id = request.data.get("doc_id")
        data = request.data.get("data", {})
        if not doc_id:
            return Response({"detail": "doc_id requis."}, status=status.HTTP_400_BAD_REQUEST)
        es_name = f"{idx.platform_id}_{index_name}"
        ESService.index_document(es_name, doc_id, data)
        idx.document_count = F("document_count") + 1
        idx.save(update_fields=["document_count", "updated_at"])
        return Response({"doc_id": doc_id, "index": index_name, "message": "Document indexed"}, status=status.HTTP_201_CREATED)


class DocumentDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Documents"], summary="Supprimer un document")
    def delete(self, request, index_name, doc_id):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        ESService.delete_document(f"{idx.platform_id}_{index_name}", doc_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentBulkView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Documents"], summary="Indexation en masse")
    def post(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        ops = request.data.get("operations", [])
        if len(ops) > 500:
            return Response({"detail": "Max 500 operations."}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        result = ESService.bulk_operations(f"{idx.platform_id}_{index_name}", ops)
        return Response(result, status=status.HTTP_207_MULTI_STATUS)


# --- Search ---

class SearchQueryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Search"], summary="Recherche full-text")
    def post(self, request):
        d = request.data
        index_name = d.get("index")
        query = d.get("query", "")
        if not index_name:
            return Response({"detail": "index requis."}, status=status.HTTP_400_BAD_REQUEST)
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)

        es_name = f"{idx.platform_id}_{index_name}"
        cfg = SearchConfig.objects.filter(index=idx).first()
        result = ESService.search(es_name, query, d.get("filters"), d.get("sort"),
                                   d.get("page", 1), min(d.get("limit", 20), cfg.max_results if cfg else 100),
                                   fuzzy=cfg.fuzzy_enabled if cfg else True,
                                   highlight=cfg.highlight_enabled if cfg else True)

        # Log historique
        uid = getattr(request.user, "auth_user_id", None)
        pid = str(getattr(request.user, "platform_id", idx.platform_id))
        SearchHistory.objects.create(user_id=uid, platform_id=pid, index_name=index_name,
                                      query=query, filters_applied=d.get("filters"),
                                      result_count=result["total"], took_ms=result["took_ms"])

        # Popular search update
        if query.strip():
            ps, _ = PopularSearch.objects.get_or_create(index_name=index_name, platform_id=pid, term=query.strip().lower(),
                                                          defaults={"search_count": 0})
            ps.search_count += 1
            ps.save(update_fields=["search_count", "last_searched_at", "updated_at"])

        return Response(result)


class AutocompleteView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Search"], summary="Auto-completion (< 50ms)")
    def get(self, request):
        index_name = request.GET.get("index")
        prefix = request.GET.get("prefix", "")
        if not index_name or not prefix:
            return Response({"detail": "index et prefix requis."}, status=status.HTTP_400_BAD_REQUEST)
        idx = IndexRegistry.objects.filter(name=index_name, status="active").first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        limit = min(int(request.GET.get("limit", 8)), 20)
        suggestions = ESService.autocomplete(f"{idx.platform_id}_{index_name}", prefix, limit)
        return Response({"suggestions": suggestions})


# --- History ---

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["History"], summary="Historique recherches")
    def get(self, request):
        uid = getattr(request.user, "auth_user_id", None)
        qs = SearchHistory.objects.filter(user_id=uid)
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{"query": h.query, "index": h.index_name, "result_count": h.result_count,
                 "took_ms": h.took_ms, "created_at": h.created_at.isoformat()} for h in page]
        return paginator.get_paginated_response(data)

    @extend_schema(tags=["History"], summary="Supprimer historique (RGPD)")
    def delete(self, request):
        uid = getattr(request.user, "auth_user_id", None)
        deleted, _ = SearchHistory.objects.filter(user_id=uid).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoryPurgeView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["History"], summary="Purge RGPD par userId (S2S)")
    def delete(self, request, user_id):
        deleted, _ = SearchHistory.objects.filter(user_id=user_id).delete()
        return Response({"message": "Search history purged", "user_id": str(user_id), "entries_deleted": deleted})


class PopularView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["History"], summary="Recherches populaires")
    def get(self, request):
        index_name = request.GET.get("index")
        if not index_name:
            return Response({"detail": "index requis."}, status=status.HTTP_400_BAD_REQUEST)
        limit = int(request.GET.get("limit", 10))
        popular = PopularSearch.objects.filter(index_name=index_name).order_by("-search_count")[:limit]
        return Response({"data": [{"term": p.term, "count": p.search_count} for p in popular]})


# --- Config ---

class ConfigView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Config"], summary="Lire/modifier config index")
    def get(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name).first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        cfg = SearchConfig.objects.filter(index=idx).first()
        if not cfg:
            return Response({"detail": "Config introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"analyzer": cfg.analyzer, "fuzzy_enabled": cfg.fuzzy_enabled,
                         "fuzzy_distance": cfg.fuzzy_distance, "highlight_enabled": cfg.highlight_enabled,
                         "min_score": cfg.min_score, "max_results": cfg.max_results})

    def put(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name).first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        cfg, _ = SearchConfig.objects.get_or_create(index=idx)
        d = request.data
        for f in ["analyzer", "fuzzy_enabled", "fuzzy_distance", "highlight_enabled", "min_score", "max_results"]:
            if f in d:
                setattr(cfg, f, d[f])
        cfg.save()
        return Response({"message": "Config updated"})


class SynonymsView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Config"], summary="Gerer synonymes")
    def put(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name).first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        Synonym.objects.filter(index=idx).delete()
        for s in request.data.get("synonyms", []):
            Synonym.objects.create(index=idx, term=s["term"], equivalents=",".join(s.get("equivalents", [])))
        return Response({"message": "Synonyms updated"})

    def get(self, request, index_name):
        idx = IndexRegistry.objects.filter(name=index_name).first()
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        syns = Synonym.objects.filter(index=idx)
        return Response({"data": [{"term": s.term, "equivalents": s.equivalents.split(",")} for s in syns]})


# --- Stats ---

class StatsView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Stats"], summary="Statistiques globales")
    def get(self, request):
        total = SearchHistory.objects.count()
        avg_ms = SearchHistory.objects.aggregate(avg=Avg("took_ms"))["avg"] or 0
        return Response({"total_searches": total, "avg_response_ms": round(avg_ms, 1)})
