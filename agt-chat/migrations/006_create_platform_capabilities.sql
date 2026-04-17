-- Migration 006 : platform_capabilities
CREATE TABLE IF NOT EXISTS platform_capabilities (
    platform_id UUID PRIMARY KEY,
    direct_enabled BOOLEAN DEFAULT true,
    channels_enabled BOOLEAN DEFAULT true,
    read_receipts_enabled BOOLEAN DEFAULT true,
    typing_enabled BOOLEAN DEFAULT true,
    presence_enabled BOOLEAN DEFAULT true,
    reactions_enabled BOOLEAN DEFAULT true,
    transfer_enabled BOOLEAN DEFAULT false,
    message_edit_enabled BOOLEAN DEFAULT true,
    message_delete_enabled BOOLEAN DEFAULT true,
    message_search_enabled BOOLEAN DEFAULT true,
    attachments_enabled BOOLEAN DEFAULT false,
    max_message_length INT DEFAULT 4096,
    rate_limit_per_user INT DEFAULT 30,
    rate_limit_per_conv INT DEFAULT 100,
    max_channel_members INT DEFAULT 500,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
