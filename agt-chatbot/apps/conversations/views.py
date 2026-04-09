"""AGT Chatbot Service v1.0 - Views."""
import uuid, logging
from django.db.models import Count, Sum, Avg
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from apps.bots.models import (
    Bot, BotConfig, BotChannel, Intent, IntentKeyword, ConversationFlow, FlowNode,
    KnowledgeCategory, KnowledgeBaseEntry, AiProviderConfig, ConversationLog, BotStats, TransferLog,
)
from apps.conversations.orchestrator import Orchestrator

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
        db_ok = redis_ok = True
        try:
            from django.db import connection; connection.ensure_connection()
        except Exception: db_ok = False
        try:
            from django.core.cache import cache; cache.set("h", "ok", 5); redis_ok = cache.get("h") == "ok"
        except Exception: redis_ok = False
        ok = db_ok and redis_ok
        return Response({"status": "healthy" if ok else "degraded", "database": "ok" if db_ok else "error",
                         "redis": "ok" if redis_ok else "error", "version": "1.0.0"},
                        status=status.HTTP_200_OK if ok else status.HTTP_503_SERVICE_UNAVAILABLE)


# --- Bots CRUD ---

class BotListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Bots"], summary="Creer un bot")
    def post(self, request):
        d = request.data
        bot = Bot.objects.create(platform_id=d.get("platform_id"), name=d["name"],
                                  description=d.get("description"), system_prompt=d.get("system_prompt"),
                                  fallback_message=d.get("fallback_message", "Je n'ai pas compris."),
                                  human_transfer_after=d.get("human_transfer_after", 3),
                                  created_by=getattr(request.user, "auth_user_id", None))
        for ch in d.get("channels", []):
            BotChannel.objects.create(bot=bot, channel=ch)
        return Response({"id": str(bot.id), "name": bot.name, "message": "Bot created"}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["Bots"], summary="Lister les bots")
    def get(self, request):
        qs = Bot.objects.filter(is_active=True)
        pid = request.GET.get("platform_id")
        if pid: qs = qs.filter(platform_id=pid)
        data = [{"id": str(b.id), "name": b.name, "platform_id": str(b.platform_id), "is_active": b.is_active} for b in qs]
        return Response({"data": data})


class BotDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Bots"], summary="Detail bot")
    def get(self, request, bot_id):
        try: bot = Bot.objects.get(id=bot_id)
        except Bot.DoesNotExist: return Response({"detail": "Bot introuvable."}, status=status.HTTP_404_NOT_FOUND)
        channels = [{"channel": c.channel, "is_active": c.is_active} for c in bot.channels.all()]
        return Response({"id": str(bot.id), "name": bot.name, "description": bot.description,
                         "system_prompt": bot.system_prompt, "fallback_message": bot.fallback_message,
                         "human_transfer_after": bot.human_transfer_after, "channels": channels})

    @extend_schema(tags=["Bots"], summary="Modifier bot")
    def put(self, request, bot_id):
        try: bot = Bot.objects.get(id=bot_id)
        except Bot.DoesNotExist: return Response({"detail": "Bot introuvable."}, status=status.HTTP_404_NOT_FOUND)
        d = request.data
        for f in ["name", "description", "system_prompt", "fallback_message", "human_transfer_after", "is_active"]:
            if f in d: setattr(bot, f, d[f])
        bot.save()
        return Response({"message": "Bot updated"})

    @extend_schema(tags=["Bots"], summary="Supprimer bot")
    def delete(self, request, bot_id):
        try: bot = Bot.objects.get(id=bot_id)
        except Bot.DoesNotExist: return Response({"detail": "Bot introuvable."}, status=status.HTTP_404_NOT_FOUND)
        bot.is_active = False
        bot.save(update_fields=["is_active", "updated_at"])
        return Response({"message": "Bot deactivated"})


# --- Intents ---

class IntentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Intents"], summary="CRUD intentions")
    def post(self, request, bot_id):
        d = request.data
        intent = Intent.objects.create(bot_id=bot_id, name=d["name"], response=d.get("response"))
        for kw in d.get("keywords", []):
            IntentKeyword.objects.create(intent=intent, keyword=kw.get("keyword", kw) if isinstance(kw, dict) else kw,
                                          weight=kw.get("weight", 1.0) if isinstance(kw, dict) else 1.0)
        return Response({"id": str(intent.id), "name": intent.name}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        intents = Intent.objects.filter(bot_id=bot_id, is_active=True)
        data = [{"id": str(i.id), "name": i.name, "keywords": list(i.keywords.values_list("keyword", flat=True))} for i in intents]
        return Response({"data": data})


# --- Flows ---

class FlowListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Flows"], summary="CRUD conversation flows")
    def post(self, request, bot_id):
        d = request.data
        flow = ConversationFlow.objects.create(bot_id=bot_id, name=d["name"], trigger_intent=d.get("trigger_intent"))
        for n in d.get("nodes", []):
            FlowNode.objects.create(flow=flow, type=n["type"], content=n.get("content", {}),
                                     branches=n.get("branches"), position=n.get("position", 0))
        return Response({"id": str(flow.id), "name": flow.name}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        flows = ConversationFlow.objects.filter(bot_id=bot_id, is_active=True)
        data = [{"id": str(f.id), "name": f.name, "trigger_intent": f.trigger_intent, "nodes_count": f.nodes.count()} for f in flows]
        return Response({"data": data})


# --- Knowledge Base ---

class KBCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Knowledge"], summary="Categories knowledge base")
    def post(self, request, bot_id):
        cat = KnowledgeCategory.objects.create(bot_id=bot_id, name=request.data["name"])
        return Response({"id": str(cat.id), "name": cat.name}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        cats = KnowledgeCategory.objects.filter(bot_id=bot_id)
        return Response({"data": [{"id": str(c.id), "name": c.name} for c in cats]})


class KBEntryView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Knowledge"], summary="CRUD entries knowledge base")
    def post(self, request, bot_id):
        d = request.data
        entry = KnowledgeBaseEntry.objects.create(bot_id=bot_id, category_id=d.get("category_id"),
                                                    question=d["question"], answer=d["answer"])
        return Response({"id": str(entry.id), "message": "Entry created"}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        qs = KnowledgeBaseEntry.objects.filter(bot_id=bot_id, is_active=True)
        cat_id = request.GET.get("category_id")
        if cat_id: qs = qs.filter(category_id=cat_id)
        paginator = Paginator()
        page = paginator.paginate_queryset(qs, request)
        data = [{"id": str(e.id), "question": e.question, "answer": e.answer[:200]} for e in page]
        return paginator.get_paginated_response(data)


# --- AI Providers ---

class AiProviderView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["AI Providers"], summary="Config providers IA par bot")
    def post(self, request, bot_id):
        d = request.data
        cfg = AiProviderConfig.objects.create(
            bot_id=bot_id, provider=d["provider"], model=d["model"],
            api_key_encrypted=d.get("api_key"), base_url=d.get("base_url"),
            temperature=d.get("temperature", 0.7), max_tokens=d.get("max_tokens", 1000),
            purpose=d.get("purpose", "conversation"), priority=d.get("priority", 0))
        return Response({"id": str(cfg.id), "provider": cfg.provider, "model": cfg.model}, status=status.HTTP_201_CREATED)

    def get(self, request, bot_id):
        cfgs = AiProviderConfig.objects.filter(bot_id=bot_id, is_active=True)
        data = [{"id": str(c.id), "provider": c.provider, "model": c.model, "purpose": c.purpose, "priority": c.priority} for c in cfgs]
        return Response({"data": data})


# --- Converse (endpoint principal) ---

class ConverseView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Converse"], summary="Envoyer un message au bot (pipeline 4 couches)")
    def post(self, request):
        d = request.data
        bot_id = d.get("bot_id")
        try: bot = Bot.objects.get(id=bot_id, is_active=True)
        except Bot.DoesNotExist: return Response({"detail": "Bot introuvable ou inactif."}, status=status.HTTP_404_NOT_FOUND)
        message = d.get("message", "")
        if not message: return Response({"detail": "message requis."}, status=status.HTTP_400_BAD_REQUEST)
        sender_id = d.get("sender_id") or getattr(request.user, "auth_user_id", str(uuid.uuid4()))
        channel = d.get("channel", "web")
        conv_id = d.get("conversation_id")
        orchestrator = Orchestrator(bot, sender_id, message, channel, conv_id)
        result = orchestrator.process()
        return Response(result)


# --- Stats ---

class BotStatsView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Stats"], summary="Statistiques bot")
    def get(self, request, bot_id):
        total = ConversationLog.objects.filter(bot_id=bot_id).count()
        resolved = ConversationLog.objects.filter(bot_id=bot_id, is_resolved=True).count()
        avg_ms = ConversationLog.objects.filter(bot_id=bot_id).aggregate(a=Avg("processing_time_ms"))["a"] or 0
        by_layer = dict(ConversationLog.objects.filter(bot_id=bot_id).values_list("layer_used").annotate(c=Count("id")))
        return Response({"total_messages": total, "resolved": resolved,
                         "resolution_rate": round(resolved / total * 100, 1) if total else 0,
                         "avg_processing_ms": round(avg_ms, 1), "by_layer": by_layer})


# --- Transfer callback ---

class TransferCallbackView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["Transfers"], summary="Callback transfert humain (depuis Chat Service)")
    def post(self, request, transfer_id):
        try:
            tl = TransferLog.objects.get(id=transfer_id)
        except TransferLog.DoesNotExist:
            return Response({"detail": "Transfer introuvable."}, status=status.HTTP_404_NOT_FOUND)
        tl.status = request.data.get("status", "closed")
        tl.save(update_fields=["status", "updated_at"])
        return Response({"message": "Transfer updated", "status": tl.status})
