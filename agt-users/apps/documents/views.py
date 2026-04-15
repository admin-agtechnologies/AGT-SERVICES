"""
AGT Users Service v1.0 - Views Documents.
"""
import logging
from django.utils import timezone
from rest_framework import status, serializers 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.documents.models import Document, DocumentHistory, DocumentStatus
from apps.users.models import UserProfile
from apps.users.services import NotificationClient

logger = logging.getLogger(__name__)

class DocumentCreateSerializer(serializers.Serializer):
    platform_id = serializers.UUIDField()
    doc_type = serializers.CharField(max_length=100)
    media_id = serializers.UUIDField()

class DocumentStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["validated", "rejected"])
    comment = serializers.CharField(required=False, allow_blank=True)

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "platform_id", "doc_type", "media_id", "status", "comment", "submitted_at", "reviewed_at"]


class DocumentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentHistory
        fields = ["id", "media_id", "status", "comment", "submitted_at", "reviewed_at", "archived_at"]


class DocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Documents"], summary="Attacher un document", request=DocumentCreateSerializer)
    def post(self, request, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        platform_id = request.data.get("platform_id")
        doc_type = request.data.get("doc_type")
        media_id = request.data.get("media_id")

        if not all([platform_id, doc_type, media_id]):
            return Response({"detail": "platform_id, doc_type et media_id requis."}, status=status.HTTP_400_BAD_REQUEST)

        # Re-soumission : archiver l'ancien si existe
        existing = Document.objects.filter(user=user, platform_id=platform_id, doc_type=doc_type).first()
        if existing:
            existing.archive_and_resubmit(media_id)
            return Response(DocumentSerializer(existing).data, status=status.HTTP_200_OK)

        doc = Document.objects.create(user=user, platform_id=platform_id, doc_type=doc_type, media_id=media_id)
        return Response(DocumentSerializer(doc).data, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Documents"], summary="Lister les documents d'un utilisateur")
    def get(self, request, user_id):
        try:
            UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        qs = Document.objects.filter(user_id=user_id)
        doc_type = request.GET.get("type")
        doc_status = request.GET.get("status")
        if doc_type:
            qs = qs.filter(doc_type=doc_type)
        if doc_status:
            qs = qs.filter(status=doc_status)

        return Response({"data": DocumentSerializer(qs, many=True).data})


class DocumentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Documents"], summary="Valider ou rejeter un document", request=DocumentStatusSerializer)
    def put(self, request, user_id, doc_id):
        try:
            doc = Document.objects.select_related("user").get(id=doc_id, user_id=user_id)
        except Document.DoesNotExist:
            return Response({"detail": "Document introuvable."}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        comment = request.data.get("comment", "")

        if new_status not in ["validated", "rejected"]:
            return Response({"detail": "status doit etre 'validated' ou 'rejected'."}, status=status.HTTP_400_BAD_REQUEST)

        doc.status = new_status
        doc.comment = comment
        doc.reviewed_at = timezone.now()
        doc.save(update_fields=["status", "comment", "reviewed_at"])

        NotificationClient.notify_document_status(doc.user.email, doc.doc_type, new_status, comment)

        return Response(DocumentSerializer(doc).data)


class DocumentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Documents"], summary="Historique des versions d'un document")
    def get(self, request, user_id, doc_id):
        history = DocumentHistory.objects.filter(document_id=doc_id, document__user_id=user_id)
        return Response({"data": DocumentHistorySerializer(history, many=True).data})


class DocumentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Documents"], summary="Supprimer un document")
    def delete(self, request, user_id, doc_id):
        deleted, _ = Document.objects.filter(id=doc_id, user_id=user_id).delete()
        if not deleted:
            return Response({"detail": "Document introuvable."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Document supprime."})
