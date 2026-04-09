# AGT Chatbot Service - CDC v1.0

> Chatbot IA multi-provider. Pipeline 4 couches. Knowledge base. Flows conversationnels.

## Pipeline
1. Keywords/Intent matching (couche 1)
2. Conversation flows (couche 2)
3. AI generative - OpenAI/Anthropic (couche 3)
4. Fallback + transfert humain (couche 4)

## Tables (15)
bots, bot_configs, bot_channels, intents, intent_keywords, conversation_flows, flow_nodes,
knowledge_categories, knowledge_base_entries, ai_provider_configs, conversation_logs,
bot_stats, transfer_logs

## Multi-provider IA
OpenAI, Anthropic, configurable par bot. Strategy pattern + circuit breaker.

## Port : 7010
