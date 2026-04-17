import { PositionsService } from '../../src/modules/positions/positions.service';

/**
 * Tests d'intégration du service Positions.
 * Mock complet des dépendances — valide la logique sans infrastructure réelle.
 */
describe('PositionsService — intégration', () => {
  let service: PositionsService;

  const mockEntityRepo = {
    findOne: jest.fn(),
    create: jest.fn(),
    save: jest.fn(),
  };
  const mockPositionRepo = { save: jest.fn() };
  const mockGeofenceEventRepo = { create: jest.fn(), save: jest.fn() };
  const mockConfigRepo = { findOne: jest.fn().mockResolvedValue(null) };
  const mockRedis = {
    updateEntityPosition: jest.fn().mockResolvedValue(undefined),
    getEntityFences: jest.fn().mockResolvedValue([]),
    setEntityFences: jest.fn().mockResolvedValue(undefined),
    isEntityOnline: jest.fn().mockResolvedValue(true),
    getEntityPayload: jest.fn(),
    removeEntityFromIndex: jest.fn().mockResolvedValue(undefined),
  };
  const mockRabbitMQ = {
    publishPositionUpdated: jest.fn().mockResolvedValue(undefined),
    publishGeofenceEvent: jest.fn().mockResolvedValue(undefined),
  };
  const mockGeofenceCache = {
    getFencesContaining: jest.fn().mockReturnValue([]),
    getAll: jest.fn().mockReturnValue([]),
  };

  beforeEach(() => {
    jest.clearAllMocks();
    service = new PositionsService(
      mockEntityRepo as any,
      mockPositionRepo as any,
      mockGeofenceEventRepo as any,
      mockConfigRepo as any,
      mockRedis as any,
      mockRabbitMQ as any,
      mockGeofenceCache as any,
    );
  });

  describe('handlePositionUpdate()', () => {
    const payload = {
      platform_id: 'plat-1',
      entity_type: 'user',
      entity_id: 'user-1',
      latitude: 3.848,
      longitude: 11.502,
      speed: 12.5,
      heading: 45.0,
      tags: ['available'],
    };

    it('crée une TrackedEntity si elle n\'existe pas', async () => {
      mockEntityRepo.findOne.mockResolvedValue(null);
      const newEntity = { id: 'te-1', entity_id: 'user-1', platform_id: 'plat-1', entity_type: 'user', tags: [], last_seen_at: null };
      mockEntityRepo.create.mockReturnValue(newEntity);
      mockEntityRepo.save.mockResolvedValue(newEntity);

      await service.handlePositionUpdate(payload);

      expect(mockEntityRepo.create).toHaveBeenCalledTimes(1);
      expect(mockRedis.updateEntityPosition).toHaveBeenCalledWith(
        'plat-1', 'user-1', 3.848, 11.502,
        expect.objectContaining({ tags: ['available'] }),
        30, // TTL par défaut
      );
    });

    it('utilise une TrackedEntity existante', async () => {
      const existing = { id: 'te-1', entity_id: 'user-1', platform_id: 'plat-1', entity_type: 'user', tags: ['vip'], last_seen_at: new Date(), save: jest.fn() };
      mockEntityRepo.findOne.mockResolvedValue(existing);
      mockEntityRepo.save.mockResolvedValue(existing);

      await service.handlePositionUpdate(payload);

      expect(mockEntityRepo.create).not.toHaveBeenCalled();
    });

    it('publie un événement RabbitMQ position.updated', async () => {
      const existing = { id: 'te-1', entity_id: 'user-1', platform_id: 'plat-1', entity_type: 'user', tags: [], last_seen_at: new Date() };
      mockEntityRepo.findOne.mockResolvedValue(existing);
      mockEntityRepo.save.mockResolvedValue(existing);

      await service.handlePositionUpdate(payload);

      expect(mockRabbitMQ.publishPositionUpdated).toHaveBeenCalledWith(
        expect.objectContaining({ entity_id: 'user-1', platform_id: 'plat-1' }),
      );
    });

    it('retourne un tableau vide de geofence events si aucune zone', async () => {
      const existing = { id: 'te-1', entity_id: 'user-1', platform_id: 'plat-1', entity_type: 'user', tags: [], last_seen_at: new Date() };
      mockEntityRepo.findOne.mockResolvedValue(existing);
      mockEntityRepo.save.mockResolvedValue(existing);
      mockGeofenceCache.getFencesContaining.mockReturnValue([]);

      const result = await service.handlePositionUpdate(payload);

      expect(result).toEqual([]);
    });

    it('détecte une entrée en zone geofence', async () => {
      const existing = { id: 'te-1', entity_id: 'user-1', platform_id: 'plat-1', entity_type: 'user', tags: [], last_seen_at: new Date() };
      mockEntityRepo.findOne.mockResolvedValue(existing);
      mockEntityRepo.save.mockResolvedValue(existing);

      // Pas dans la zone avant, dans la zone maintenant
      mockRedis.getEntityFences.mockResolvedValue([]); // était dans 0 zones
      mockGeofenceCache.getFencesContaining.mockReturnValue([
        { id: 'fence-1', name: 'Zone Test', platform_id: 'plat-1' },
      ]);
      mockGeofenceEventRepo.create.mockReturnValue({});
      mockGeofenceEventRepo.save.mockResolvedValue({});

      const result = await service.handlePositionUpdate(payload);

      expect(result).toHaveLength(1);
      expect(result[0].event).toBe('enter');
      expect(result[0].geofence_id).toBe('fence-1');
      expect(mockRabbitMQ.publishGeofenceEvent).toHaveBeenCalledWith('enter', expect.any(Object));
    });
  });

  describe('flushBuffer()', () => {
    it('retourne et vide le buffer de positions', async () => {
      const existing = { id: 'te-1', entity_id: 'user-1', platform_id: 'plat-1', entity_type: 'user', tags: [], last_seen_at: new Date() };
      mockEntityRepo.findOne.mockResolvedValue(existing);
      mockEntityRepo.save.mockResolvedValue(existing);

      await service.handlePositionUpdate({ platform_id: 'plat-1', entity_type: 'user', entity_id: 'user-1', latitude: 3.848, longitude: 11.502 });

      const batch = service.flushBuffer();
      expect(batch.length).toBe(1);
      // Buffer doit être vide après flush
      expect(service.flushBuffer().length).toBe(0);
    });
  });
});
