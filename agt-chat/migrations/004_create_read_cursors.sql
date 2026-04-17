-- Migration 004 : read_cursors
CREATE TABLE IF NOT EXISTS read_cursors (
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    last_read_message_id UUID REFERENCES messages(id),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (conversation_id, user_id)
);
CREATE INDEX IF NOT EXISTS idx_read_cursors_user ON read_cursors(user_id);
