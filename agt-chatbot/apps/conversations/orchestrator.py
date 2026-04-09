"""AGT Chatbot Service v1.0 - Conversation Orchestrator. Pipeline 4 couches."""
import logging, time, uuid, httpx
from django.core.cache import cache
from apps.bots.models import Bot, Intent, IntentKeyword, ConversationFlow, AiProviderConfig, ConversationLog

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, bot, sender_id, message, channel, conversation_id=None):
        self.bot = bot
        self.sender_id = sender_id
        self.message = message
        self.channel = channel
        self.conv_id = conversation_id or str(uuid.uuid4())
        self.context = self._load_context()
        self.start_time = time.time()

    def process(self):
        # Couche 1 : Keywords / Intent matching
        result = self._layer1_keywords()
        if result:
            return self._finalize(result, "layer_1_keywords")

        # Couche 2 : Conversation flows
        result = self._layer2_flow()
        if result:
            return self._finalize(result, "layer_2_flow")

        # Couche 3 : AI generative
        result = self._layer3_ai()
        if result:
            return self._finalize(result, "layer_3_ai")

        # Couche 4 : Fallback
        return self._layer4_fallback()

    def _layer1_keywords(self):
        intents = Intent.objects.filter(bot=self.bot, is_active=True).prefetch_related("keywords")
        msg_lower = self.message.lower()
        best_intent = None
        best_score = 0

        for intent in intents:
            score = 0
            for kw in intent.keywords.all():
                if kw.keyword.lower() in msg_lower:
                    score += float(kw.weight)
            if score > best_score:
                best_score = score
                best_intent = intent

        if best_intent and best_score >= 1.0:
            return {"response": best_intent.response, "intent": best_intent.name, "confidence": min(best_score, 1.0)}
        return None

    def _layer2_flow(self):
        # Verifier si un flow est actif en contexte
        active_flow_id = self.context.get("active_flow_id")
        if active_flow_id:
            # Continuer le flow existant (simplifie pour MVP)
            pass
        return None

    def _layer3_ai(self):
        providers = AiProviderConfig.objects.filter(
            bot=self.bot, purpose="conversation", is_active=True
        ).order_by("priority")

        for provider_cfg in providers:
            try:
                response = self._call_ai_provider(provider_cfg)
                if response:
                    return {"response": response, "provider": provider_cfg.provider, "model": provider_cfg.model}
            except Exception as e:
                logger.warning(f"AI provider {provider_cfg.provider} failed: {e}")
                continue
        return None

    def _call_ai_provider(self, cfg):
        messages = [{"role": "system", "content": self.bot.system_prompt or "Tu es un assistant utile."}]
        history = self.context.get("history", [])[-10:]
        messages.extend(history)
        messages.append({"role": "user", "content": self.message})

        if cfg.provider == "openai":
            return self._call_openai(cfg, messages)
        elif cfg.provider == "anthropic":
            return self._call_anthropic(cfg, messages)
        return None

    def _call_openai(self, cfg, messages):
        url = cfg.base_url or "https://api.openai.com/v1/chat/completions"
        try:
            resp = httpx.post(url, headers={"Authorization": f"Bearer {cfg.api_key_encrypted}",
                                             "Content-Type": "application/json"},
                               json={"model": cfg.model, "messages": messages,
                                     "temperature": float(cfg.temperature), "max_tokens": cfg.max_tokens},
                               timeout=15.0)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
        return None

    def _call_anthropic(self, cfg, messages):
        url = cfg.base_url or "https://api.anthropic.com/v1/messages"
        system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
        user_msgs = [m for m in messages if m["role"] != "system"]
        try:
            resp = httpx.post(url, headers={"x-api-key": cfg.api_key_encrypted,
                                             "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
                               json={"model": cfg.model, "system": system, "messages": user_msgs,
                                     "max_tokens": cfg.max_tokens, "temperature": float(cfg.temperature)},
                               timeout=15.0)
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
        except Exception as e:
            logger.error(f"Anthropic call failed: {e}")
        return None

    def _layer4_fallback(self):
        fallbacks = self.context.get("consecutive_fallbacks", 0) + 1
        self.context["consecutive_fallbacks"] = fallbacks
        self._save_context()

        response = self.bot.fallback_message

        # Transfert humain si seuil atteint
        if fallbacks >= self.bot.human_transfer_after:
            response += "\n\nJe vous transfere vers un agent humain."
            # TODO: S2S call to Chat Service

        result = {"response": response, "is_fallback": True, "consecutive_fallbacks": fallbacks}
        self._log("layer_4_fallback", result)
        elapsed = int((time.time() - self.start_time) * 1000)
        return {"response": response, "conversation_id": self.conv_id, "layer": "layer_4_fallback",
                "is_resolved": False, "processing_time_ms": elapsed}

    def _finalize(self, result, layer):
        self.context["consecutive_fallbacks"] = 0
        self.context.setdefault("history", []).append({"role": "user", "content": self.message})
        self.context["history"].append({"role": "assistant", "content": result["response"]})
        self._save_context()
        self._log(layer, result)

        elapsed = int((time.time() - self.start_time) * 1000)
        return {"response": result["response"], "conversation_id": self.conv_id, "layer": layer,
                "intent": result.get("intent"), "confidence": result.get("confidence"),
                "provider": result.get("provider"), "is_resolved": True, "processing_time_ms": elapsed}

    def _load_context(self):
        key = f"conv:{self.bot.id}:{self.sender_id}"
        return cache.get(key) or {"history": [], "consecutive_fallbacks": 0}

    def _save_context(self):
        key = f"conv:{self.bot.id}:{self.sender_id}"
        cache.set(key, self.context, timeout=1800)

    def _log(self, layer, result):
        try:
            ConversationLog.objects.create(
                bot=self.bot, conversation_id=self.conv_id, sender_id=self.sender_id,
                channel=self.channel, user_message=self.message, bot_response=result["response"],
                layer_used=layer, intent_detected=result.get("intent"),
                confidence=result.get("confidence"), provider_used=result.get("provider"),
                processing_time_ms=int((time.time() - self.start_time) * 1000),
                is_resolved=layer != "layer_4_fallback",
            )
        except Exception as e:
            logger.error(f"Log failed: {e}")
