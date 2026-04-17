/**
 * Tests unitaires — CapabilitiesService
 * Mocks : repository, Redis
 */
const capabilitiesService = require('../../src/modules/capabilities/capabilities.service');
const capabilitiesRepo = require('../../src/modules/capabilities/capabilities.repository');
const { getRedis } = require('../../src/common/cache/redis');
const AppError = require('../../src/common/errors/AppError');

jest.mock('../../src/modules/capabilities/capabilities.repository');
jest.mock('../../src/common/cache/redis', () => ({
  getRedis: jest.fn(() => ({
    get: jest.fn().mockResolvedValue(null),
    set: jest.fn().mockResolvedValue('OK'),
    del: jest.fn().mockResolvedValue(1),
  })),
}));

describe('CapabilitiesService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset Redis mock to return null (cache miss) by default
    getRedis.mockReturnValue({
      get: jest.fn().mockResolvedValue(null),
      set: jest.fn().mockResolvedValue('OK'),
      del: jest.fn().mockResolvedValue(1),
    });
  });

  describe('getCapabilities', () => {
    test('retourne les valeurs par défaut si plateforme inconnue', async () => {
      capabilitiesRepo.findByPlatformId.mockResolvedValue(null);
      const caps = await capabilitiesService.getCapabilities('unknown-platform-id');
      expect(caps.direct_enabled).toBe(true);
      expect(caps.transfer_enabled).toBe(false);
      expect(caps.max_message_length).toBe(4096);
    });

    test('retourne les capabilities DB si plateforme connue', async () => {
      capabilitiesRepo.findByPlatformId.mockResolvedValue({
        platform_id: 'plat-1',
        direct_enabled: false,
        transfer_enabled: true,
        max_message_length: 2048,
      });
      const caps = await capabilitiesService.getCapabilities('plat-1');
      expect(caps.direct_enabled).toBe(false);
      expect(caps.transfer_enabled).toBe(true);
      expect(caps.max_message_length).toBe(2048);
    });

    test('retourne depuis le cache Redis si disponible', async () => {
      const cached = { ...capabilitiesService.getDefaults(), direct_enabled: false };
      getRedis.mockReturnValue({
        get: jest.fn().mockResolvedValue(JSON.stringify(cached)),
        set: jest.fn(),
        del: jest.fn(),
      });
      const caps = await capabilitiesService.getCapabilities('cached-plat');
      expect(caps.direct_enabled).toBe(false);
      expect(capabilitiesRepo.findByPlatformId).not.toHaveBeenCalled();
    });
  });

  describe('updateCapabilities', () => {
    test('admin peut mettre à jour les capabilities', async () => {
      capabilitiesRepo.upsert.mockResolvedValue({ platform_id: 'plat-1', transfer_enabled: true });
      const result = await capabilitiesService.updateCapabilities('plat-1', { transfer_enabled: true });
      expect(capabilitiesRepo.upsert).toHaveBeenCalledWith('plat-1', { transfer_enabled: true });
      expect(result.transfer_enabled).toBe(true);
    });

    test('rejette les champs inconnus', async () => {
      await expect(
        capabilitiesService.updateCapabilities('plat-1', { unknown_field: true })
      ).rejects.toThrow(AppError);
    });
  });

  describe('requireFeature', () => {
    test('retourne 403 si feature désactivée', () => {
      const caps = { reactions_enabled: false };
      expect(() => capabilitiesService.requireFeature(caps, 'reactions_enabled'))
        .toThrow(AppError);
    });

    test('ne lance pas d\'erreur si feature activée', () => {
      const caps = { reactions_enabled: true };
      expect(() => capabilitiesService.requireFeature(caps, 'reactions_enabled')).not.toThrow();
    });
  });
});
