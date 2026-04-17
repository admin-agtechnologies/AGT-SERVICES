/**
 * Tests d'intégration — Messages API
 */
const request = require('supertest');
const app = require('../../src/app');
const AppError = require('../../src/common/errors/AppError');

jest.mock('../../src/common/clients/authClient', () => ({
  verifyToken: jest.fn().mockResolvedValue({
    user_id: 'test-user-id',
    platform_id: 'test-platform-id',
    roles: ['user'],
  }),
  introspectS2S: jest.fn().mockResolvedValue({ valid: true, service: 'chatbot' }),
}));

jest.mock('../../src/common/cache/redis', () => ({
  getRedis: jest.fn(() => ({
    get: jest.fn().mockResolvedValue(null),
    set: jest.fn().mockResolvedValue('OK'),
    del: jest.fn().mockResolvedValue(1),
    incr: jest.fn().mockResolvedValue(1),
    expire: jest.fn().mockResolvedValue(1),
    ping: jest.fn().mockResolvedValue('PONG'),
  })),
  ping: jest.fn().mockResolvedValue(true),
}));

jest.mock('../../src/common/db/pool', () => ({
  query: jest.fn(),
  getClient: jest.fn(),
  ping: jest.fn().mockResolvedValue(true),
}));

jest.mock('../../src/common/broker/publisher', () => ({
  publish: jest.fn().mockResolvedValue(undefined),
  isConnected: jest.fn().mockReturnValue(true),
}));

jest.mock('../../src/common/clients/usersClient', () => ({
  getUserProfile: jest.fn().mockResolvedValue({ id: 'test-user-id' }),
  checkPermission: jest.fn().mockResolvedValue(false),
  resolveProfilesId: jest.fn().mockResolvedValue(null),
}));

jest.mock('../../src/common/clients/notificationClient', () => ({
  sendNotification: jest.fn().mockResolvedValue(undefined),
}));

jest.mock('../../src/modules/capabilities/capabilities.repository');
jest.mock('../../src/modules/conversations/conversations.repository');
jest.mock('../../src/modules/messages/messages.repository');

const capabilitiesRepo = require('../../src/modules/capabilities/capabilities.repository');
const conversationsRepo = require('../../src/modules/conversations/conversations.repository');
const messagesRepo = require('../../src/modules/messages/messages.repository');

const defaultCaps = {
  direct_enabled: true, channels_enabled: true, transfer_enabled: false,
  max_message_length: 4096, max_channel_members: 500, reactions_enabled: true,
  typing_enabled: true, presence_enabled: true, read_receipts_enabled: true,
  message_edit_enabled: true, message_delete_enabled: true, message_search_enabled: true,
  attachments_enabled: false, rate_limit_per_user: 30, rate_limit_per_conv: 100,
  updated_at: new Date().toISOString(),
};

describe('GET /api/v1/chat/conversations/:id/messages', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    capabilitiesRepo.findByPlatformId.mockResolvedValue(defaultCaps);
  });

  test('200 - historique paginé avec cursor', async () => {
    conversationsRepo.findParticipant.mockResolvedValue({ role: 'member' });
    messagesRepo.findByConversation.mockResolvedValue([
      { id: 'msg-1', content: 'hello', created_at: new Date().toISOString() },
      { id: 'msg-2', content: 'world', created_at: new Date().toISOString() },
    ]);

    const res = await request(app)
      .get('/api/v1/chat/conversations/conv-1/messages')
      .set('Authorization', 'Bearer valid-token');

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(Array.isArray(res.body.data)).toBe(true);
    expect(res.body).toHaveProperty('pagination');
  });

  test('403 - non participant', async () => {
    conversationsRepo.findParticipant.mockResolvedValue(null);

    const res = await request(app)
      .get('/api/v1/chat/conversations/conv-1/messages')
      .set('Authorization', 'Bearer valid-token');

    expect(res.status).toBe(403);
    expect(res.body.error.code).toBe('NOT_PARTICIPANT');
  });

  test('404 - conversation inexistante', async () => {
    // Simuler la vérification participant qui échoue car conv inexistante
    conversationsRepo.findParticipant.mockRejectedValue(
      new AppError('CONVERSATION_NOT_FOUND', 'Conversation introuvable', 404)
    );

    const res = await request(app)
      .get('/api/v1/chat/conversations/nonexistent-id/messages')
      .set('Authorization', 'Bearer valid-token');

    expect(res.status).toBe(404);
  });
});

describe('POST /api/v1/chat/conversations/:id/messages', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    capabilitiesRepo.findByPlatformId.mockResolvedValue(defaultCaps);
  });

  test('201 - envoie un message avec JWT valide', async () => {
    conversationsRepo.findById.mockResolvedValue({ id: 'conv-1', platform_id: 'test-platform-id' });
    conversationsRepo.findParticipant.mockResolvedValue({ role: 'member' });
    conversationsRepo.touch.mockResolvedValue();
    conversationsRepo.findParticipants.mockResolvedValue([]);
    messagesRepo.create.mockResolvedValue({
      id: 'msg-new', content: 'hello', created_at: new Date().toISOString(),
    });

    const res = await request(app)
      .post('/api/v1/chat/conversations/conv-1/messages')
      .set('Authorization', 'Bearer valid-token')
      .send({ content: 'hello' });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.content).toBe('hello');
  });

  test('400 - body invalide (content manquant)', async () => {
    const res = await request(app)
      .post('/api/v1/chat/conversations/conv-1/messages')
      .set('Authorization', 'Bearer valid-token')
      .send({});

    expect(res.status).toBe(400);
    expect(res.body.error.code).toBe('VALIDATION_ERROR');
  });
});
