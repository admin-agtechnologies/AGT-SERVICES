/**
 * Tests d'intégration — Conversations API
 */
const request = require('supertest');
const app = require('../../src/app');

const PLATFORM_ID   = '550e8400-e29b-41d4-a716-446655440000';
const USER_ID       = '550e8400-e29b-41d4-a716-446655440001';
const OTHER_USER_ID = '660e8400-e29b-41d4-a716-446655440002';

// Préfixe 'mock' autorisé dans les factories jest.mock()
const mockGetFn   = jest.fn().mockResolvedValue(null);
const mockSetFn   = jest.fn().mockResolvedValue('OK');
const mockDelFn   = jest.fn().mockResolvedValue(1);
const mockIncrFn  = jest.fn().mockResolvedValue(1);
const mockExpFn   = jest.fn().mockResolvedValue(1);

jest.mock('../../src/common/cache/redis', () => ({
  getRedis: jest.fn(() => ({
    get: mockGetFn, set: mockSetFn, del: mockDelFn,
    incr: mockIncrFn, expire: mockExpFn,
    ping: jest.fn().mockResolvedValue('PONG'),
  })),
  ping: jest.fn().mockResolvedValue(true),
}));

jest.mock('../../src/common/clients/authClient', () => ({
  verifyToken: jest.fn(),
  introspectS2S: jest.fn(),
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
  getUserProfile: jest.fn().mockResolvedValue({ id: '550e8400-e29b-41d4-a716-446655440001', first_name: 'Test' }),
  checkPermission: jest.fn().mockResolvedValue(false),
  resolveProfilesId: jest.fn().mockResolvedValue(null),
}));

jest.mock('../../src/common/clients/notificationClient', () => ({
  sendNotification: jest.fn().mockResolvedValue(undefined),
}));

jest.mock('../../src/modules/capabilities/capabilities.repository');
jest.mock('../../src/modules/conversations/conversations.repository');

const { verifyToken }   = require('../../src/common/clients/authClient');
const capabilitiesRepo  = require('../../src/modules/capabilities/capabilities.repository');
const conversationsRepo = require('../../src/modules/conversations/conversations.repository');
const { getClient }     = require('../../src/common/db/pool');

const defaultCaps = {
  direct_enabled: true, channels_enabled: true, transfer_enabled: false,
  max_message_length: 4096, max_channel_members: 500, reactions_enabled: true,
  typing_enabled: true, presence_enabled: true, read_receipts_enabled: true,
  message_edit_enabled: true, message_delete_enabled: true, message_search_enabled: true,
  attachments_enabled: false, rate_limit_per_user: 30, rate_limit_per_conv: 100,
  updated_at: new Date().toISOString(),
};

beforeEach(() => {
  // Réinitialiser sans effacer les implémentations des fns mock préfixées
  mockGetFn.mockResolvedValue(null);
  mockSetFn.mockResolvedValue('OK');
  mockDelFn.mockResolvedValue(1);
  mockIncrFn.mockResolvedValue(1);
  mockExpFn.mockResolvedValue(1);
  verifyToken.mockResolvedValue({ user_id: USER_ID, platform_id: PLATFORM_ID, roles: ['user'] });
  capabilitiesRepo.findByPlatformId.mockResolvedValue(defaultCaps);
  jest.clearAllMocks();
  // Re-setter après clearAllMocks
  mockGetFn.mockResolvedValue(null);
  mockSetFn.mockResolvedValue('OK');
  mockDelFn.mockResolvedValue(1);
  mockIncrFn.mockResolvedValue(1);
  mockExpFn.mockResolvedValue(1);
  verifyToken.mockResolvedValue({ user_id: USER_ID, platform_id: PLATFORM_ID, roles: ['user'] });
  capabilitiesRepo.findByPlatformId.mockResolvedValue(defaultCaps);
});

describe('POST /api/v1/chat/conversations', () => {
  test('201 - crée une conversation directe avec JWT valide', async () => {
    conversationsRepo.findDirectBetween.mockResolvedValue(null);
    const newConv = { id: 'conv-new', type: 'direct', platform_id: PLATFORM_ID, created_at: new Date().toISOString() };
    const clientMock = {
      query: jest.fn()
        .mockResolvedValueOnce(undefined)
        .mockResolvedValueOnce({ rows: [newConv] })
        .mockResolvedValueOnce({ rows: [] })
        .mockResolvedValueOnce({ rows: [] })
        .mockResolvedValueOnce(undefined),
      release: jest.fn(),
    };
    getClient.mockResolvedValue(clientMock);

    const res = await request(app)
      .post('/api/v1/chat/conversations')
      .set('Authorization', 'Bearer valid-token')
      .send({ type: 'direct', platform_id: PLATFORM_ID, participant_ids: [OTHER_USER_ID] });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
  });

  test('400 - body invalide (type manquant)', async () => {
    const res = await request(app)
      .post('/api/v1/chat/conversations')
      .set('Authorization', 'Bearer valid-token')
      .send({ platform_id: PLATFORM_ID });

    expect(res.status).toBe(400);
    expect(res.body.error.code).toBe('VALIDATION_ERROR');
  });

  test('401 - token invalide', async () => {
    const AppError = require('../../src/common/errors/AppError');
    verifyToken.mockRejectedValueOnce(new AppError('UNAUTHORIZED', 'Token invalide', 401));

    const res = await request(app)
      .post('/api/v1/chat/conversations')
      .set('Authorization', 'Bearer bad-token')
      .send({ type: 'direct', platform_id: PLATFORM_ID, participant_ids: [OTHER_USER_ID] });

    expect(res.status).toBe(401);
  });

  test('403 - feature direct_enabled=false', async () => {
    capabilitiesRepo.findByPlatformId.mockResolvedValue({ ...defaultCaps, direct_enabled: false });
    conversationsRepo.findDirectBetween.mockResolvedValue(null);

    const res = await request(app)
      .post('/api/v1/chat/conversations')
      .set('Authorization', 'Bearer valid-token')
      .send({ type: 'direct', platform_id: PLATFORM_ID, participant_ids: [OTHER_USER_ID] });

    expect(res.status).toBe(403);
    expect(res.body.error.code).toBe('FEATURE_DISABLED');
  });
});

describe('GET /api/v1/chat/conversations', () => {
  test('200 - liste les conversations de l\'utilisateur', async () => {
    conversationsRepo.findByUser = jest.fn().mockResolvedValue([
      { id: 'conv-1', type: 'direct', updated_at: new Date().toISOString() },
    ]);

    const res = await request(app)
      .get('/api/v1/chat/conversations')
      .set('Authorization', 'Bearer valid-token');

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(Array.isArray(res.body.data)).toBe(true);
  });
});

describe('GET /api/v1/chat/health', () => {
  test('retourne le statut du service', async () => {
    const res = await request(app).get('/api/v1/chat/health');
    expect(res.body).toHaveProperty('data');
    expect(res.body.data).toHaveProperty('status');
    expect(res.body.data).toHaveProperty('database');
    expect(res.body.data).toHaveProperty('redis');
    expect(res.body.data).toHaveProperty('rabbitmq');
  });
});
