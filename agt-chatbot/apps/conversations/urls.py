from django.urls import path
from apps.conversations.views import (
    HealthCheckView, BotListCreateView, BotDetailView,
    IntentListCreateView, FlowListCreateView,
    KBCategoryView, KBEntryView, AiProviderView,
    ConverseView, BotStatsView, TransferCallbackView,
)
urlpatterns = [
    path("chatbot/health", HealthCheckView.as_view()),
    path("chatbot/bots", BotListCreateView.as_view()),
    path("chatbot/bots/<uuid:bot_id>", BotDetailView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/intents", IntentListCreateView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/flows", FlowListCreateView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/knowledge/categories", KBCategoryView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/knowledge/entries", KBEntryView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/ai-providers", AiProviderView.as_view()),
    path("chatbot/bots/<uuid:bot_id>/stats", BotStatsView.as_view()),
    path("chatbot/converse", ConverseView.as_view()),
    path("chatbot/transfers/<uuid:transfer_id>/callback", TransferCallbackView.as_view()),
]
