from django.urls import path
from apps.documents.views import (
    DocumentListCreateView, DocumentStatusUpdateView,
    DocumentHistoryView, DocumentDeleteView,
)

urlpatterns = [
    path("users/<uuid:user_id>/documents", DocumentListCreateView.as_view(), name="documents-list-create"),
    path("users/<uuid:user_id>/documents/<uuid:doc_id>/status", DocumentStatusUpdateView.as_view(), name="document-status"),
    path("users/<uuid:user_id>/documents/<uuid:doc_id>/history", DocumentHistoryView.as_view(), name="document-history"),
    path("users/<uuid:user_id>/documents/<uuid:doc_id>", DocumentDeleteView.as_view(), name="document-delete"),
]
