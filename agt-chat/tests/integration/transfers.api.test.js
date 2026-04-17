/**
 * Tests d'intégration — Transfers API
 */
const request = require('supertest');
const app = require('../../src/app');

jest.mock('../../src/common/clients/authClient', () => ({
  verifyToken: jest.fn().mockResolvedValue({
    user_id: '550e8400-e29b-41d4-a716-446655440010',
    platform_id: '550e8400-e29b-41d4-a716-446655440000',
    roles: ['operator'],
  }),
  introspectS2S: jest.fn().mockResolvedValue({ active: true, service: "chatbot" }),
}));

jest.mock('../../src/common/cache/redis', () => ({
  getRedis: jest.fn(() => ({
    get: jest.fn().mockResolvedValue(null),
    set: jest.fn().mockResolvedValue('OK'),
    del: jest.fn().mockResolvedValue(1),
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
  getUserProfile: jest.fn().mockResolvedValue({ id: '550e8400-e29b-41d4-a716-446655440010' }),
  checkPermission: jest.fn().mockResolvedValue(true),
  resolveProfilesId: jest.fn().mockResolvedValue(null),
}));

jest.mock('../../src/common/clients/notificationClient', () => ({
  sendNotification: jest.fn().mockResolvedValue(undefined),
}));

jest.mock('../../src/modules/capabilities/capabilities.repository');
jest.mock('../../src/modules/conversations/conversations.repository');
jest.mock('../../src/modules/transfers/transfers.repository');

const capabilitiesRepo = require('../../src/modules/capabilities/capabilities.repository');
const conversationsRepo = require('../../src/modules/conversations/conversations.repository');
const transfersRepo = require('../../src/modules/transfers/transfers.repository');
const { getClient } = require('../../src/common/db/pool');

const PLATFORM_ID = '550e8400-e29b-41d4-a716-446655440000';
const USER_ID = '550e8400-e29b-41d4-a716-446655440020';
const OPERATOR_ID = '550e8400-e29b-41d4-a716-446655440010';

const defaultCaps = {
  direct_enabled: true, channels_enabled: true, transfer_enabled: true,
  max_message_length: 4096, max_channel_members: 500, reactions_enabled: true,
  typing_enabled: true, presence_enabled: true, read_receipts_enabled: true,
  message_edit_enabled: true, message_delete_enabled: true, message_search_enabled: true,
  attachments_enabled: false, rate_limit_per_user: 30, rate_limit_per_conv: 100,
  updated_at: new Date().toISOString(),
};

describe('POST /api/v1/chat/conversations/transfer', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    capabilitiesRepo.findByPlatformId.mockResolvedValue(defaultCaps);
  });

  test('201 - S2S token valide crée le transfert', async () => {
    const newConv = { id: '660e8400-e29b-41d4-a716-446655440030', type: 'transfer', platform_id: PLATFORM_ID };
    const clientMock = {
      query: jest.fn()
        .mockResolvedValueOnce(undefined)
        .mockResolvedValueOnce({ rows: [newConv] })
        .mockResolvedValueOnce({ rows: [] })
        .mockResolvedValueOnce(undefined),
      release: jest.fn(),
    };
    conversationsRepo.createWithParticipants.mockResolvedValue(newConv);
    getClient.mockResolvedValue(clientMock);
    conversationsRepo.findParticipants.mockResolvedValue([]);
    transfersRepo.create.mockResolvedValue({
      id: '770e8400-e29b-41d4-a716-446655440040', status: 'pending', conversation_id: newConv.id,
    });

    const res = await request(app)
      .post('/api/v1/chat/conversations/transfer')
      .set('Authorization', 'Bearer s2s-token')
      .send({ user_id: USER_ID, platform_id: PLATFORM_ID, bot_history: [], context: {} });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
  });

  test('401 - introspect S2S échoue', async () => {
    const { introspectS2S } = require('../../src/common/clients/authClient');
    const AppError = require('../../src/common/errors/AppError');
    introspectS2S.mockRejectedValueOnce(new AppError('UNAUTHORIZED', 'Token S2S invalide', 401));

    const res = await request(app)
      .post('/api/v1/chat/conversations/transfer')
      .set('Authorization', 'Bearer invalid-token')
      .send({ user_id: USER_ID, platform_id: PLATFORM_ID });

    expect(res.status).toBe(401);
  });

  test('400 - body invalide (user_id manquant)', async () => {
    const res = await request(app)
      .post('/api/v1/chat/conversations/transfer')
      .set('Authorization', 'Bearer s2s-token')
      .send({ platform_id: PLATFORM_ID });

    expect(res.status).toBe(400);
    expect(res.body.error.code).toBe('VALIDATION_ERROR');
  });
});

describe('POST /api/v1/chat/transfers/:id/take', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    capabilitiesRepo.findByPlatformId.mockResolvedValue(defaultCaps);
  });

  test('409 - verrou optimiste si transfert déjà pris', async () => {
    transfersRepo.takeOptimistic.mockResolvedValue(null);

    const res = await request(app)
      .post('/api/v1/chat/transfers/770e8400-e29b-41d4-a716-446655440040/take')
      .set('Authorization', 'Bearer valid-token');

    expect(res.status).toBe(409);
    expect(res.body.error.code).toBe('TRANSFER_ALREADY_TAKEN');
  });

  test('200 - prise en charge réussie', async () => {
    const taken = {
      id: '770e8400-e29b-41d4-a716-446655440040',
      status: 'taken',
      operator_id: OPERATOR_ID,
      conversation_id: '660e8400-e29b-41d4-a716-446655440030',
    };
    transfersRepo.takeOptimistic.mockResolvedValue(taken);
    conversationsRepo.addParticipant.mockResolvedValue({});

    const res = await request(app)
      .post('/api/v1/chat/transfers/770e8400-e29b-41d4-a716-446655440040/take')
      .set('Authorization', 'Bearer valid-token');

    expect(res.status).toBe(200);
    expect(res.body.data.status).toBe('taken');
  });
});
