"""AGT Search Service v1.0 - Views."""
import logging
from django.conf import settings
from django.db.models import Avg, F
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from common.authentication import IsS2SToken
from apps.indexes.models import IndexRegistry, IndexSchema, SearchConfig, Synonym, SearchHistory, PopularSearch
from apps.search.es_service import ESService
# APRÈS
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from drf_spectacular.types import OpenApiTypes

logger = logging.getLogger(__name__)


# --- Serializers (pour Swagger request body) ---

class IndexFieldSerializer(serializers.Serializer):
    """Définition d'un champ dans le schéma d'un index."""
    type = serializers.ChoiceField(
        choices=["text", "keyword", "integer", "float", "date", "boolean"],
        default="text",
        help_text="Type du champ : text (recherchable), keyword (exact), number, date, boolean"
    )
    searchable = serializers.BooleanField(default=True, required=False)
    filterable = serializers.BooleanField(default=False, required=False)
    sortable = serializers.BooleanField(default=False, required=False)
    autocomplete = serializers.BooleanField(default=False, required=False)
    boost_weight = serializers.IntegerField(default=1, required=False)


class IndexCreateSerializer(serializers.Serializer):
    """Body pour créer un index. platform_id est extrait du JWT, pas du body."""
    name = serializers.CharField(
        help_text="Nom de l'index ex: products, articles, users"
    )
    analyzer = serializers.ChoiceField(
        choices=["standard", "french", "english", "arabic"],
        default="standard",
        required=False,
        help_text="Analyseur linguistique pour la recherche full-text"
    )
    fields = serializers.DictField(
        child=serializers.DictField(),
        required=False,
        help_text='Champs de l\'index. Ex: {"title": {"type": "text", "searchable": true, "boost_weight": 2}}'
    )

class DocumentIndexSerializer(serializers.Serializer):
    """Body pour indexer un document dans un index."""
    doc_id = serializers.CharField(
        help_text="Identifiant unique du document. Ex: prod-123, user-456"
    )
    data = serializers.DictField(
        help_text='Contenu du document. Ex: {"title": "Nike Air Max", "price": 35000}'
    )

class DocumentUpdateSerializer(serializers.Serializer):
    """Body pour mettre à jour un document existant."""
    data = serializers.DictField(
        help_text='Nouveau contenu complet du document. Ex: {"title": "Nike Air Max", "price": 40000}'
    )

class BulkOperationSerializer(serializers.Serializer):
    """Une opération dans un bulk — index ou delete."""
    action = serializers.ChoiceField(
        choices=["index", "delete"],
        help_text="Action à effectuer : index (ajouter/modifier) ou delete (supprimer)"
    )
    doc_id = serializers.CharField(
        help_text="Identifiant unique du document. Ex: prod-001"
    )
    data = serializers.DictField(
        required=False,
        help_text="Contenu du document — obligatoire si action=index, ignoré si action=delete"
    )

class BulkIndexSerializer(serializers.Serializer):
    """Body pour l'indexation en masse."""
    operations = BulkOperationSerializer(
        many=True,
        help_text="Liste des opérations (max 500)"
    )

class SearchQuerySerializer(serializers.Serializer):
    """Body pour la recherche full-text."""
    index = serializers.CharField(
        help_text="Nom de l'index. Ex: products"
    )
    query = serializers.CharField(
        default="",
        help_text="Texte recherché. Ex: nike air max"
    )
    search_type = serializers.ChoiceField(
        choices=["fulltext", "fuzzy", "exact"],
        default="fulltext",
        required=False
    )
    filters = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        help_text='[{"field": "category", "operator": "eq", "value": "Chaussures"}]'
    )
    sort = serializers.DictField(
        required=False,
        help_text='{"field": "price", "order": "asc"}'
    )
    page = serializers.IntegerField(default=1, required=False)
    limit = serializers.IntegerField(default=20, required=False)
    include_facets = serializers.BooleanField(default=False, required=False)


class ConfigUpdateSerializer(serializers.Serializer):
    """Body pour modifier la configuration d'un index."""
    analyzer = serializers.ChoiceField(
        choices=["standard", "french", "english", "arabic"],
        required=False,
        help_text="Analyseur linguistique"
    )
    fuzzy_enabled = serializers.BooleanField(
        required=False,
        help_text="Activer la recherche floue"
    )
    fuzzy_distance = serializers.IntegerField(
        required=False,
        help_text="Distance Levenshtein (1 ou 2)"
    )
    highlight_enabled = serializers.BooleanField(
        required=False,
        help_text="Activer le surlignage des termes"
    )
    min_score = serializers.FloatField(
        required=False,
        help_text="Score minimum (0.0 à 1.0)"
    )
    max_results = serializers.IntegerField(
        required=False,
        help_text="Nombre maximum de résultats (max 100)"
    )


class SynonymItemSerializer(serializers.Serializer):
    """Un synonyme avec ses équivalents."""
    term = serializers.CharField(
        help_text="Terme principal. Ex: telephone"
    )
    equivalents = serializers.ListField(
        child=serializers.CharField(),
        help_text='["smartphone", "mobile", "cellulaire"]'
    )


class SynonymsUpdateSerializer(serializers.Serializer):
    """Body pour mettre à jour les synonymes d'un index."""
    synonyms = SynonymItemSerializer(
        many=True,
        help_text="Liste des synonymes"
    )

class SchemaUpdateSerializer(serializers.Serializer):
    """Body pour ajouter des champs à un index existant."""
    fields = serializers.DictField(
        child=serializers.DictField(),
        help_text='Nouveaux champs à ajouter. Ex: {"stock": {"type": "integer", "filterable": true}}'
    )
# --- Helper privé ---

def _get_owned_index(index_name, platform_id):
    """
    Récupère un index actif en vérifiant qu'il appartient bien à la plateforme.
    Garantit l'isolation multi-tenant : une plateforme ne peut pas accéder
    aux index d'une autre plateforme.
    """
    return IndexRegistry.objects.filter(
        name=index_name,
        platform_id=platform_id,
        status="active"
    ).first()


# --- Pagination ---

class Paginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"

    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "page": self.page.number,
            "total": self.page.paginator.count
        })

class SearchQuerySerializer(serializers.Serializer):
    """Body pour la recherche full-text."""
    index = serializers.CharField(
        help_text="Nom de l'index dans lequel chercher. Ex: products"
    )
    query = serializers.CharField(
        default="",
        help_text="Texte recherché. Ex: nike air max"
    )
    search_type = serializers.ChoiceField(
        choices=["fulltext", "fuzzy", "exact"],
        default="fulltext",
        required=False,
        help_text="Type de recherche : fulltext, fuzzy, exact"
    )
    filters = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        help_text='Filtres. Ex: [{"field": "category", "operator": "eq", "value": "Chaussures"}]'
    )
    sort = serializers.DictField(
        required=False,
        help_text='Tri. Ex: {"field": "price", "order": "asc"}'
    )
    page = serializers.IntegerField(default=1, required=False)
    limit = serializers.IntegerField(default=20, required=False)
    include_facets = serializers.BooleanField(default=False, required=False)


class ConfigUpdateSerializer(serializers.Serializer):
    """Body pour modifier la configuration d'un index."""
    analyzer = serializers.ChoiceField(
        choices=["standard", "french", "english", "arabic"],
        required=False,
        help_text="Analyseur linguistique"
    )
    fuzzy_enabled = serializers.BooleanField(
        required=False,
        help_text="Activer la recherche floue (tolérance aux fautes)"
    )
    fuzzy_distance = serializers.IntegerField(
        required=False,
        help_text="Distance de Levenshtein pour le fuzzy (1 ou 2)"
    )
    highlight_enabled = serializers.BooleanField(
        required=False,
        help_text="Activer le surlignage des termes dans les résultats"
    )
    min_score = serializers.FloatField(
        required=False,
        help_text="Score minimum pour inclure un résultat (0.0 à 1.0)"
    )
    max_results = serializers.IntegerField(
        required=False,
        help_text="Nombre maximum de résultats retournés (max 100)"
    )


class SynonymItemSerializer(serializers.Serializer):
    """Un synonyme avec ses équivalents."""
    term = serializers.CharField(
        help_text="Terme principal. Ex: telephone"
    )
    equivalents = serializers.ListField(
        child=serializers.CharField(),
        help_text='Liste des équivalents. Ex: ["smartphone", "mobile", "cellulaire"]'
    )


class SynonymsUpdateSerializer(serializers.Serializer):
    """Body pour mettre à jour les synonymes d'un index."""
    synonyms = SynonymItemSerializer(
        many=True,
        help_text="Liste des synonymes à définir"
    )


# --- Health ---

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Health"], summary="Health check")
    def get(self, request):
        db_ok = redis_ok = es_ok = True
        try:
            from django.db import connection
            connection.ensure_connection()
        except Exception:
            db_ok = False
        try:
            from django.core.cache import cache
            cache.set("h", "ok", 5)
            redis_ok = cache.get("h") == "ok"
        except Exception:
            redis_ok = False
        try:
            from apps.search.es_service import _get_es
            es = _get_es()
            es_ok = es.ping() if es else False
        except Exception:
            es_ok = False
        code = status.HTTP_200_OK if db_ok and redis_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response({
            "status": "healthy" if db_ok and redis_ok and es_ok else "degraded",
            "database": "ok" if db_ok else "error",
            "redis": "ok" if redis_ok else "error",
            "elasticsearch": "ok" if es_ok else "error",
            "version": "1.0.0"
        }, status=code)


# --- Indexes CRUD ---

class IndexListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Indexes"],
        summary="Creer un index",
        request=IndexCreateSerializer
    )
    def post(self, request):
        d = request.data
        name = d.get("name")

        # Sécurité : platform_id vient du token JWT, jamais du body
        pid = str(request.user.platform_id)

        if not name:
            return Response({"detail": "name requis."}, status=status.HTTP_400_BAD_REQUEST)
        if not pid or pid == "None":
            return Response({"detail": "platform_id absent du token."}, status=status.HTTP_403_FORBIDDEN)
        if IndexRegistry.objects.filter(name=name, platform_id=pid).exists():
            return Response({"detail": "Index existe deja."}, status=status.HTTP_409_CONFLICT)

        # Quota : maximum 20 index actifs par plateforme (CDC v1.0)
        MAX_INDEXES = int(getattr(settings, "MAX_INDEXES_PER_PLATFORM", 20))
        current_count = IndexRegistry.objects.filter(platform_id=pid, status="active").count()
        if current_count >= MAX_INDEXES:
            return Response({
                "detail": f"Quota atteint : maximum {MAX_INDEXES} index actifs par plateforme.",
                "current": current_count,
                "max": MAX_INDEXES
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Création en PostgreSQL
        analyzer = d.get("analyzer", "standard")
        idx = IndexRegistry.objects.create(
            name=name,
            platform_id=pid,
            description=d.get("description", "")
        )

        # Champs au format CDC : {"title": {"type": "text", "searchable": true, ...}}
        fields = d.get("fields", {})
        schema_list = []
        for field_name, field_props in fields.items():
            IndexSchema.objects.create(
                index=idx,
                field_name=field_name,
                field_type=field_props.get("type", "text"),
                searchable=field_props.get("searchable", True),
                filterable=field_props.get("filterable", False),
                sortable=field_props.get("sortable", False),
                autocomplete=field_props.get("autocomplete", False),
                boost_weight=field_props.get("boost_weight", 1)
            )
            schema_list.append({"field_name": field_name, **field_props})

        # Config par défaut avec l'analyzer choisi
        SearchConfig.objects.create(index=idx, analyzer=analyzer)

        # Création dans Elasticsearch avec le nom préfixé par platform_id
        es_name = f"{pid}_{name}"
        ESService.create_index(es_name, schema_list)

        return Response({
            "id": str(idx.id),
            "name": name,
            "es_index": es_name,
            "message": "Index created"
        }, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Indexes"], summary="Lister les index")
    def get(self, request):
        # Isolation automatique : uniquement les index de la plateforme du token
        pid = str(request.user.platform_id)
        qs = IndexRegistry.objects.filter(status="active", platform_id=pid)
        data = [{
            "id": str(i.id),
            "name": i.name,
            "platform_id": str(i.platform_id),
            "document_count": i.document_count,
            "status": i.status
        } for i in qs]
        return Response({"data": data})


class IndexDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Indexes"], summary="Detail index avec schema")
    def get(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        fields = [{
            "field_name": f.field_name,
            "field_type": f.field_type,
            "searchable": f.searchable,
            "filterable": f.filterable,
            "autocomplete": f.autocomplete
        } for f in idx.schema_fields.all()]
        return Response({
            "id": str(idx.id),
            "name": idx.name,
            "platform_id": str(idx.platform_id),
            "document_count": idx.document_count,
            "schema": fields
        })

    @extend_schema(tags=["Indexes"], summary="Supprimer un index")
    def delete(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        ESService.delete_index(f"{idx.platform_id}_{index_name}")
        idx.status = "deleted"
        idx.save(update_fields=["status", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class IndexSchemaUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Indexes"],
        summary="Ajouter des champs au schema",
        request=SchemaUpdateSerializer
    )
    def put(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)

        fields = request.data.get("fields", {})
        if not fields:
            return Response({"detail": "fields requis."}, status=status.HTTP_400_BAD_REQUEST)

        added = []
        skipped = []

        for field_name, field_props in fields.items():
            # Vérifie que le champ n'existe pas déjà — ajout uniquement
            if IndexSchema.objects.filter(index=idx, field_name=field_name).exists():
                skipped.append(field_name)
                continue
            IndexSchema.objects.create(
                index=idx,
                field_name=field_name,
                field_type=field_props.get("type", "text"),
                searchable=field_props.get("searchable", True),
                filterable=field_props.get("filterable", False),
                sortable=field_props.get("sortable", False),
                autocomplete=field_props.get("autocomplete", False),
                boost_weight=field_props.get("boost_weight", 1)
            )
            added.append(field_name)

        return Response({
            "message": "Schema updated",
            "added": added,
            "skipped": skipped
        }, status=status.HTTP_200_OK)


class IndexReindexView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Indexes"],
        summary="Reconstruire l index (reindex)"
    )
    def post(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)

        # Récupère le schéma actuel
        schema_list = [{
            "field_name": f.field_name,
            "field_type": f.field_type,
            "searchable": f.searchable,
            "filterable": f.filterable,
            "sortable": f.sortable,
            "autocomplete": f.autocomplete,
            "boost_weight": f.boost_weight,
        } for f in idx.schema_fields.all()]

        es_name = f"{pid}_{index_name}"

        # Supprime et recrée l'index ES avec le schéma actuel
        ESService.delete_index(es_name)
        ESService.create_index(es_name, schema_list)

        return Response({
            "message": "Reindex started",
            "index": index_name,
            "status": "rebuilding"
        }, status=status.HTTP_202_ACCEPTED)
    
# --- Documents ---

class DocumentIndexView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
    tags=["Documents"],
    summary="Indexer un document",
    request=DocumentIndexSerializer
    )
    def post(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
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
        return Response({
            "doc_id": doc_id,
            "index": index_name,
            "message": "Document indexed"
        }, status=status.HTTP_201_CREATED)


class DocumentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Documents"],
        summary="Mettre a jour un document",
        request=DocumentUpdateSerializer
    )
    def put(self, request, index_name, doc_id):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.get("data", {})
        if not data:
            return Response({"detail": "data requis."}, status=status.HTTP_400_BAD_REQUEST)
        es_name = f"{idx.platform_id}_{index_name}"
        ESService.index_document(es_name, doc_id, data)
        return Response({
            "doc_id": doc_id,
            "index": index_name,
            "message": "Document updated"
        }, status=status.HTTP_200_OK)

    @extend_schema(tags=["Documents"], summary="Supprimer un document")
    def delete(self, request, index_name, doc_id):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        ESService.delete_document(f"{idx.platform_id}_{index_name}", doc_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DocumentBulkView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
    tags=["Documents"],
    summary="Indexation en masse",
    request=BulkIndexSerializer
    )

    def post(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
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

    @extend_schema(
    tags=["Search"],
    summary="Recherche full-text",
    request=SearchQuerySerializer
    )
    def post(self, request):
        d = request.data
        index_name = d.get("index")
        query = d.get("query", "")
        if not index_name:
            return Response({"detail": "index requis."}, status=status.HTTP_400_BAD_REQUEST)
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        es_name = f"{idx.platform_id}_{index_name}"
        cfg = SearchConfig.objects.filter(index=idx).first()
        result = ESService.search(
            es_name, query, d.get("filters"), d.get("sort"),
            d.get("page", 1),
            min(d.get("limit", 20), cfg.max_results if cfg else 100),
            fuzzy=cfg.fuzzy_enabled if cfg else True,
            highlight=cfg.highlight_enabled if cfg else True
        )
        # Log historique de recherche
        uid = getattr(request.user, "auth_user_id", None)
        SearchHistory.objects.create(
            user_id=uid, platform_id=pid, index_name=index_name,
            query=query, filters_applied=d.get("filters"),
            result_count=result["total"], took_ms=result["took_ms"]
        )
        # Mise à jour des recherches populaires
        if query.strip():
            ps, _ = PopularSearch.objects.get_or_create(
                index_name=index_name, platform_id=pid,
                term=query.strip().lower(), defaults={"search_count": 0}
            )
            ps.search_count += 1
            ps.save(update_fields=["search_count", "last_searched_at", "updated_at"])
        return Response(result)


class AutocompleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
    tags=["Search"],
    summary="Auto-completion (< 50ms)",
    parameters=[
        OpenApiParameter(
            name="index",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Nom de l'index dans lequel chercher. Ex: products"
        ),
        OpenApiParameter(
            name="prefix",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Préfixe à compléter. Ex: sam → Samsung..."
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Nombre de suggestions (défaut: 8, max: 20)"
        ),
    ]
    )
    def get(self, request):
        index_name = request.GET.get("index")
        prefix = request.GET.get("prefix", "")
        if not index_name or not prefix:
            return Response({"detail": "index et prefix requis."}, status=status.HTTP_400_BAD_REQUEST)
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        limit = min(int(request.GET.get("limit", 8)), 20)
        suggestions = ESService.autocomplete(f"{idx.platform_id}_{index_name}", prefix, limit)
        return Response({"suggestions": suggestions})


# --- History ---

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
    tags=["History"],
    summary="Historique recherches",
    parameters=[
        OpenApiParameter(
            name="page",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Numéro de page (défaut: 1)"
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Nombre de résultats par page (défaut: 20)"
        ),
    ]
    )
    def get(self, request):
        uid = getattr(request.user, "auth_user_id", None)
        qs = SearchHistory.objects.filter(user_id=uid)
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{
            "query": h.query,
            "index": h.index_name,
            "result_count": h.result_count,
            "took_ms": h.took_ms,
            "created_at": h.created_at.isoformat()
        } for h in page]
        return paginator.get_paginated_response(data)

    @extend_schema(tags=["History"], summary="Supprimer historique (RGPD)")
    def delete(self, request):
        uid = getattr(request.user, "auth_user_id", None)
        SearchHistory.objects.filter(user_id=uid).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoryPurgeView(APIView):
    permission_classes = [IsAuthenticated, IsS2SToken]

    @extend_schema(tags=["History"], summary="Purge RGPD par userId (S2S uniquement)")
    def delete(self, request, user_id):
        deleted, _ = SearchHistory.objects.filter(user_id=user_id).delete()
        return Response({
            "message": "Search history purged",
            "user_id": str(user_id),
            "entries_deleted": deleted
        })


class PopularView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
    tags=["History"],
    summary="Recherches populaires",
    parameters=[
        OpenApiParameter(
            name="index",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Nom de l'index. Ex: products"
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Nombre de résultats (défaut: 10)"
        ),
    ]
    )
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

    @extend_schema(
        tags=["Config"],
        summary="Lire config index"
    )
    def get(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        cfg = SearchConfig.objects.filter(index=idx).first()
        if not cfg:
            return Response({"detail": "Config introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "analyzer": cfg.analyzer,
            "fuzzy_enabled": cfg.fuzzy_enabled,
            "fuzzy_distance": cfg.fuzzy_distance,
            "highlight_enabled": cfg.highlight_enabled,
            "min_score": cfg.min_score,
            "max_results": cfg.max_results
        })

    @extend_schema(
        tags=["Config"],
        summary="Modifier config index",
        request=ConfigUpdateSerializer
    )
    def put(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        cfg, _ = SearchConfig.objects.get_or_create(index=idx)
        for f in ["analyzer", "fuzzy_enabled", "fuzzy_distance", "highlight_enabled", "min_score", "max_results"]:
            if f in request.data:
                setattr(cfg, f, request.data[f])
        cfg.save()
        return Response({"message": "Config updated"})

class SynonymsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Config"],
        summary="Modifier synonymes",
        request=SynonymsUpdateSerializer
    )
    def put(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        Synonym.objects.filter(index=idx).delete()
        for s in request.data.get("synonyms", []):
            Synonym.objects.create(
                index=idx,
                term=s["term"],
                equivalents=",".join(s.get("equivalents", []))
            )
        return Response({"message": "Synonyms updated"})

    @extend_schema(
        tags=["Config"],
        summary="Lire synonymes"
    )
    def get(self, request, index_name):
        pid = str(request.user.platform_id)
        idx = _get_owned_index(index_name, pid)
        if not idx:
            return Response({"detail": "Index introuvable."}, status=status.HTTP_404_NOT_FOUND)
        syns = Synonym.objects.filter(index=idx)
        return Response({"data": [{
            "term": s.term,
            "equivalents": s.equivalents.split(",")
        } for s in syns]})

# --- Stats ---

class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Stats"], summary="Statistiques globales")
    def get(self, request):
        total = SearchHistory.objects.count()
        avg_ms = SearchHistory.objects.aggregate(avg=Avg("took_ms"))["avg"] or 0
        return Response({
            "total_searches": total,
            "avg_response_ms": round(avg_ms, 1)
        })

class StatsTermsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Stats"],
        summary="Termes les plus recherches",
        parameters=[
            OpenApiParameter(
                name="index",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Nom de l'index. Ex: products"
            ),
            OpenApiParameter(
                name="limit",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Nombre de termes (défaut: 10)"
            ),
            OpenApiParameter(
                name="from",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Date de début. Ex: 2026-01-01"
            ),
            OpenApiParameter(
                name="to",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Date de fin. Ex: 2026-12-31"
            ),
        ]
    )
    def get(self, request):
        index_name = request.GET.get("index")
        if not index_name:
            return Response({"detail": "index requis."}, status=status.HTTP_400_BAD_REQUEST)
        limit = int(request.GET.get("limit", 10))
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")

        # Filtre par index et plateforme
        pid = str(request.user.platform_id)
        qs = SearchHistory.objects.filter(index_name=index_name, platform_id=pid)

        # Filtre optionnel par date
        if from_date:
            qs = qs.filter(created_at__date__gte=from_date)
        if to_date:
            qs = qs.filter(created_at__date__lte=to_date)

        # Agrégation par terme
        from django.db.models import Count
        terms = (
            qs.values("query")
            .annotate(count=Count("query"))
            .order_by("-count")[:limit]
        )
        return Response({
            "data": [{"term": t["query"], "count": t["count"]} for t in terms]
        })

class NoResultsView(APIView):
    permission_classes = [IsAuthenticated, IsS2SToken]

    @extend_schema(
        tags=["Stats"],
        summary="Recherches sans resultats (Admin/S2S)",
        parameters=[
            OpenApiParameter(
                name="index",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtrer par index. Ex: products"
            ),
            OpenApiParameter(
                name="from",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Date de début. Ex: 2026-01-01"
            ),
            OpenApiParameter(
                name="to",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Date de fin. Ex: 2026-12-31"
            ),
        ]
    )
    def get(self, request):
        qs = SearchHistory.objects.filter(result_count=0)
        index_name = request.GET.get("index")
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")

        if index_name:
            qs = qs.filter(index_name=index_name)
        if from_date:
            qs = qs.filter(created_at__date__gte=from_date)
        if to_date:
            qs = qs.filter(created_at__date__lte=to_date)

        data = [{
            "query": h.query,
            "index": h.index_name,
            "created_at": h.created_at.isoformat()
        } for h in qs[:100]]

        return Response({"data": data, "total": qs.count()})