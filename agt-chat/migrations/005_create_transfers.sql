-- Migration 005 : transfers
CREATE TABLE IF NOT EXISTS transfers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL UNIQUE REFERENCES conversations(id),
    user_id UUID NOT NULL,
    operator_id UUID,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'taken', 'closed', 'timeout')),
    bot_history JSONB NOT NULL DEFAULT '[]',
    context JSONB DEFAULT '{}',
    taken_at TIMESTAMPTZ,
    closed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_transfers_status ON transfers(status);
CREATE INDEX IF NOT EXISTS idx_transfers_operator ON transfers(operator_id);
