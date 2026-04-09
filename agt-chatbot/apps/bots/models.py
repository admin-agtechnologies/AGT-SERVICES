"""AGT Chatbot Service v1.0 - Modeles complets."""
import uuid
from django.db import models


class Bot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform_id = models.UUIDField(db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    system_prompt = models.TextField(null=True, blank=True)
    fallback_message = models.TextField(default="Je n'ai pas compris. Pouvez-vous reformuler ?")
    human_transfer_after = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_by = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bots"
        ordering = ["-created_at"]


class BotConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="configs")
    config_key = models.CharField(max_length=100)
    config_value = models.TextField()

    class Meta:
        db_table = "bot_configs"
        unique_together = [("bot", "config_key")]


class BotChannel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="channels")
    channel = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "bot_channels"
        unique_together = [("bot", "channel")]


class Intent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="intents")
    name = models.CharField(max_length=100)
    response = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "intents"
        unique_together = [("bot", "name")]


class IntentKeyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name="keywords")
    keyword = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)

    class Meta:
        db_table = "intent_keywords"


class ConversationFlow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="flows")
    name = models.CharField(max_length=100)
    trigger_intent = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversation_flows"


class FlowNode(models.Model):
    NODE_TYPES = [("message", "Message"), ("question", "Question"), ("condition", "Condition"), ("action", "Action")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow = models.ForeignKey(ConversationFlow, on_delete=models.CASCADE, related_name="nodes")
    type = models.CharField(max_length=20, choices=NODE_TYPES)
    content = models.JSONField()
    next_node = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    branches = models.JSONField(null=True, blank=True)
    position = models.IntegerField(default=0)

    class Meta:
        db_table = "flow_nodes"
        ordering = ["position"]


class KnowledgeCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="kb_categories")
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "knowledge_categories"
        unique_together = [("bot", "name")]


class KnowledgeBaseEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="kb_entries")
    category = models.ForeignKey(KnowledgeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    embedding = models.JSONField(null=True, blank=True)  # pgvector en prod
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "knowledge_base_entries"


class AiProviderConfig(models.Model):
    PURPOSE_CHOICES = [("conversation", "Conversation"), ("rag", "RAG"), ("translation", "Translation"), ("fallback", "Fallback")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="ai_providers")
    provider = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    api_key_encrypted = models.TextField(null=True, blank=True)
    base_url = models.CharField(max_length=500, null=True, blank=True)
    temperature = models.DecimalField(max_digits=3, decimal_places=2, default=0.7)
    max_tokens = models.IntegerField(default=1000)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    circuit_breaker_threshold = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_provider_configs"
        unique_together = [("bot", "provider", "purpose")]


class ConversationLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="conversation_logs")
    conversation_id = models.UUIDField(db_index=True)
    sender_id = models.UUIDField()
    channel = models.CharField(max_length=30)
    user_message = models.TextField()
    bot_response = models.TextField()
    layer_used = models.CharField(max_length=30)
    intent_detected = models.CharField(max_length=100, null=True, blank=True)
    confidence = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    provider_used = models.CharField(max_length=30, null=True, blank=True)
    tokens_used = models.IntegerField(null=True, blank=True)
    processing_time_ms = models.IntegerField()
    is_resolved = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversation_logs"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["bot", "created_at"]), models.Index(fields=["bot", "is_resolved"])]


class BotStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="stats")
    date = models.DateField()
    total_messages = models.IntegerField(default=0)
    resolved_count = models.IntegerField(default=0)
    fallback_count = models.IntegerField(default=0)
    human_transfer_count = models.IntegerField(default=0)
    layer1_count = models.IntegerField(default=0)
    layer2_count = models.IntegerField(default=0)
    layer3_count = models.IntegerField(default=0)
    top_intents = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "bot_stats"
        unique_together = [("bot", "date")]


class TransferLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="transfer_logs")
    conversation_id = models.UUIDField()
    chat_transfer_id = models.UUIDField(null=True, blank=True)
    user_id = models.UUIDField()
    reason = models.CharField(max_length=50, null=True, blank=True)
    bot_history = models.JSONField(null=True, blank=True)
    context = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=20, default="sent")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transfer_logs"
        ordering = ["-created_at"]
