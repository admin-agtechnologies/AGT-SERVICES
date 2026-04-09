from django.urls import path
from apps.templates_mgr.views import TemplateListCreateView, TemplateDetailView, TemplatePreviewView, TemplateVersionsView

urlpatterns = [
    path("templates", TemplateListCreateView.as_view(), name="templates-list"),
    path("templates/<uuid:template_id>", TemplateDetailView.as_view(), name="templates-detail"),
    path("templates/<uuid:template_id>/preview", TemplatePreviewView.as_view(), name="templates-preview"),
    path("templates/<uuid:template_id>/versions", TemplateVersionsView.as_view(), name="templates-versions"),
]
