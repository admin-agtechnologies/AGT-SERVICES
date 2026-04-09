"""AGT Chatbot Service v1.0 - Tests."""
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from apps.bots.models import Bot, Intent, IntentKeyword, ConversationLog, KnowledgeBaseEntry
from apps.conversations.orchestrator import Orchestrator

def make_bot(**kw):
    defaults = {"platform_id": uuid.uuid4(), "name": "Test Bot", "system_prompt": "Tu es un assistant.",
                "fallback_message": "Je ne comprends pas.", "human_transfer_after": 3}
    defaults.update(kw)
    return Bot.objects.create(**defaults)

def add_intent(bot, name, response, keywords):
    intent = Intent.objects.create(bot=bot, name=name, response=response)
    for kw in keywords:
        IntentKeyword.objects.create(intent=intent, keyword=kw, weight=1.0)
    return intent

class TestBotModel(TestCase):
    def test_create_bot(self):
        bot = make_bot()
        self.assertTrue(bot.is_active)
        self.assertEqual(bot.human_transfer_after, 3)

class TestLayer1Keywords(TestCase):
    def test_intent_matching(self):
        bot = make_bot()
        add_intent(bot, "greeting", "Bonjour ! Comment puis-je aider ?", ["bonjour", "salut", "hello"])
        orch = Orchestrator(bot, uuid.uuid4(), "Bonjour tout le monde", "web")
        result = orch.process()
        self.assertTrue(result["is_resolved"])
        self.assertEqual(result["layer"], "layer_1_keywords")
        self.assertIn("Bonjour", result["response"])

    def test_no_match_fallback(self):
        bot = make_bot()
        orch = Orchestrator(bot, uuid.uuid4(), "xyz random text", "web")
        result = orch.process()
        self.assertFalse(result["is_resolved"])
        self.assertEqual(result["layer"], "layer_4_fallback")

class TestFallbackCounter(TestCase):
    def test_consecutive_fallbacks(self):
        bot = make_bot(human_transfer_after=2)
        sid = uuid.uuid4()
        r1 = Orchestrator(bot, sid, "incomprehensible", "web").process()
        self.assertEqual(r1["layer"], "layer_4_fallback")
        r2 = Orchestrator(bot, sid, "still incomprehensible", "web").process()
        self.assertIn("agent humain", r2["response"])

class TestConversationLog(TestCase):
    def test_log_created(self):
        bot = make_bot()
        add_intent(bot, "help", "Comment puis-je aider ?", ["aide", "help"])
        Orchestrator(bot, uuid.uuid4(), "aide moi", "web").process()
        self.assertEqual(ConversationLog.objects.count(), 1)
        log = ConversationLog.objects.first()
        self.assertTrue(log.is_resolved)

class TestHealthEndpoint(TestCase):
    def test_health(self):
        resp = APIClient().get("/api/v1/chatbot/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["version"], "1.0.0")

class TestBotEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=type("U", (), {"is_authenticated": True, "platform_id": str(uuid.uuid4()), "auth_user_id": str(uuid.uuid4())})())

    def test_create_bot(self):
        resp = self.client.post("/api/v1/chatbot/bots", data={
            "platform_id": str(uuid.uuid4()), "name": "Sales Bot",
            "system_prompt": "Tu vends des produits.", "channels": ["web", "whatsapp"],
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_converse_bot_not_found(self):
        resp = self.client.post("/api/v1/chatbot/converse", data={
            "bot_id": str(uuid.uuid4()), "message": "hello",
        }, format="json")
        self.assertEqual(resp.status_code, 404)
