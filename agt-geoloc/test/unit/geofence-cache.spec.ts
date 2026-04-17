import { GeofenceCacheService } from '../../src/infrastructure/geofence-cache.service';
import { Geofence } from '../../src/modules/geofences/entities/geofence.entity';

/**
 * Tests unitaires du cache geofence en mémoire.
 * On mock le repository et Redis — on teste uniquement la logique spatiale.
 */
describe('GeofenceCacheService — logique spatiale', () => {
  let service: GeofenceCacheService;

  const mockRepo = {
    find: jest.fn().mockResolvedValue([]),
    findOne: jest.fn(),
  };
  const mockRedis = {
    subscribeGeofenceInvalidation: jest.fn().mockResolvedValue(undefined),
  };

  beforeEach(async () => {
    // Instancier manuellement pour éviter le DI NestJS dans les tests unitaires
    service = new GeofenceCacheService(mockRepo as any, mockRedis as any);
    // Bypass onModuleInit (évite DB + Redis)
  });

  const makePolygonFence = (platformId: string): Geofence => ({
    id: 'fence-1',
    platform_id: platformId,
    name: 'Zone Test',
    fence_type: 'polygon',
    // Carré autour de Yaoundé centre
    coordinates: [
      [11.49, 3.84], [11.52, 3.84],
      [11.52, 3.87], [11.49, 3.87],
      [11.49, 3.84],
    ],
    center_latitude: null,
    center_longitude: null,
    radius_meters: null,
    tags: ['test'],
    metadata: null,
    is_active: true,
    created_at: new Date(),
    updated_at: new Date(),
  });

  const makeCircleFence = (platformId: string): Geofence => ({
    id: 'fence-2',
    platform_id: platformId,
    name: 'Zone Cercle',
    fence_type: 'circle',
    coordinates: null,
    center_latitude: 3.855,
    center_longitude: 11.505,
    radius_meters: 1000, // 1 km
    tags: [],
    metadata: null,
    is_active: true,
    created_at: new Date(),
    updated_at: new Date(),
  });

  describe('addOrUpdate() + getFencesContaining()', () => {
    it('détecte un point DANS un polygone', () => {
      const fence = makePolygonFence('platform-1');
      service.addOrUpdate(fence);

      // Point au centre du carré : 3.855°N 11.505°E
      const result = service.getFencesContaining('platform-1', 3.855, 11.505);
      expect(result).toHaveLength(1);
      expect(result[0].id).toBe('fence-1');
    });

    it('ne détecte pas un point HORS du polygone', () => {
      const fence = makePolygonFence('platform-1');
      service.addOrUpdate(fence);

      // Point loin du carré
      const result = service.getFencesContaining('platform-1', 4.05, 9.77);
      expect(result).toHaveLength(0);
    });

    it('détecte un point DANS un cercle', () => {
      const fence = makeCircleFence('platform-1');
      service.addOrUpdate(fence);

      // Point à 100m du centre
      const result = service.getFencesContaining('platform-1', 3.856, 11.505);
      expect(result).toHaveLength(1);
    });

    it('ne détecte pas un point HORS du cercle', () => {
      const fence = makeCircleFence('platform-1');
      service.addOrUpdate(fence);

      // Point à 10 km du centre
      const result = service.getFencesContaining('platform-1', 3.950, 11.600);
      expect(result).toHaveLength(0);
    });

    it('filtre correctement par platform_id', () => {
      const fence = makePolygonFence('platform-A');
      service.addOrUpdate(fence);

      // Mauvaise plateforme → 0 résultats
      const result = service.getFencesContaining('platform-B', 3.855, 11.505);
      expect(result).toHaveLength(0);
    });
  });

  describe('remove()', () => {
    it('retire la zone du cache', () => {
      const fence = makePolygonFence('platform-1');
      service.addOrUpdate(fence);
      expect(service.getCount()).toBe(1);

      service.remove('fence-1');
      expect(service.getCount()).toBe(0);
    });
  });

  describe('addOrUpdate() avec is_active = false', () => {
    it('retire une zone désactivée du cache', () => {
      const fence = makePolygonFence('platform-1');
      service.addOrUpdate(fence);
      expect(service.getCount()).toBe(1);

      fence.is_active = false;
      service.addOrUpdate(fence);
      expect(service.getCount()).toBe(0);
    });
  });
});
