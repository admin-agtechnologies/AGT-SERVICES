-- Migration 002 : messages
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id UUID NOT NULL,
    content TEXT,
    parent_id UUID REFERENCES messages(id),
    media_ids UUID[] DEFAULT '{}',
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    edited_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_messages_conv_created ON messages(conversation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_content_gin ON messages USING GIN (to_tsvector('french', COALESCE(content, '')));
CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_id);
