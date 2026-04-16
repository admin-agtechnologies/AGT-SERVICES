from django.urls import path
from apps.search.views import (
    HealthCheckView, IndexListCreateView, IndexDetailView,
    IndexSchemaUpdateView, IndexReindexView,
    DocumentIndexView, DocumentDetailView, DocumentBulkView,
    SearchQueryView, AutocompleteView,
    HistoryView, HistoryPurgeView, PopularView,
    ConfigView, SynonymsView,
    StatsView, StatsTermsView, NoResultsView,
)

urlpatterns = [
    path("search/health", HealthCheckView.as_view()),
    path("search/indexes", IndexListCreateView.as_view()),
    path("search/indexes/<str:index_name>", IndexDetailView.as_view()),
    path("search/indexes/<str:index_name>/schema", IndexSchemaUpdateView.as_view()),
    path("search/indexes/<str:index_name>/reindex", IndexReindexView.as_view()),
    path("search/indexes/<str:index_name>/documents/bulk", DocumentBulkView.as_view()),
    path("search/indexes/<str:index_name>/documents", DocumentIndexView.as_view()),
   path("search/indexes/<str:index_name>/documents/<str:doc_id>", DocumentDetailView.as_view()),
    path("search/indexes/<str:index_name>/config", ConfigView.as_view()),
    path("search/indexes/<str:index_name>/synonyms", SynonymsView.as_view()),
    path("search/query", SearchQueryView.as_view()),
    path("search/autocomplete", AutocompleteView.as_view()),
    path("search/history", HistoryView.as_view()),
    path("search/history/by-user/<uuid:user_id>", HistoryPurgeView.as_view()),
    path("search/popular", PopularView.as_view()),
    path("search/no-results", NoResultsView.as_view()),
    path("search/stats", StatsView.as_view()),
    path("search/stats/terms", StatsTermsView.as_view()),
]