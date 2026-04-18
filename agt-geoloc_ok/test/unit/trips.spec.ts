import { ConflictException, NotFoundException } from '@nestjs/common';
import { TripsService } from '../../src/modules/trips/trips.service';
import { Trip } from '../../src/modules/trips/entities/trip.entity';

/**
 * Tests unitaires du service Trips.
 * Machine à états : active → completed | cancelled.
 */
describe('TripsService', () => {
  let service: TripsService;

  const mockTripRepo = {
    findOne: jest.fn(),
    find: jest.fn(),
    create: jest.fn(),
    save: jest.fn(),
    createQueryBuilder: jest.fn(),
  };
  const mockRabbitMQ = {
    publishTripStarted: jest.fn().mockResolvedValue(undefined),
    publishTripEnded: jest.fn().mockResolvedValue(undefined),
  };

  beforeEach(() => {
    jest.clearAllMocks();
    service = new TripsService(mockTripRepo as any, mockRabbitMQ as any);
  });

  describe('startTrip()', () => {
    it('crée un trajet si aucun trajet actif', async () => {
      mockTripRepo.findOne.mockResolvedValue(null); // pas de trajet actif
      const newTrip: Partial<Trip> = {
        id: 'trip-1',
        entity_id: 'entity-1',
        platform_id: 'plat-1',
        status: 'active',
        start_latitude: 3.848,
        start_longitude: 11.502,
        started_at: new Date(),
        distance_meters: 0,
        duration_seconds: 0,
      };
      mockTripRepo.create.mockReturnValue(newTrip);
      mockTripRepo.save.mockResolvedValue(newTrip);

      const result = await service.startTrip({
        platform_id: 'plat-1',
        entity_id: 'entity-1',
        start_latitude: 3.848,
        start_longitude: 11.502,
      });

      expect(result.status).toBe('active');
      expect(mockRabbitMQ.publishTripStarted).toHaveBeenCalledTimes(1);
    });

    it('lève ConflictException si un trajet actif existe déjà', async () => {
      mockTripRepo.findOne.mockResolvedValue({ id: 'existing', status: 'active' });

      await expect(service.startTrip({
        platform_id: 'plat-1',
        entity_id: 'entity-1',
        start_latitude: 3.848,
        start_longitude: 11.502,
      })).rejects.toThrow(ConflictException);
    });
  });

  describe('endTrip()', () => {
    it('termine un trajet actif et calcule la distance', async () => {
      const activeTrip: Partial<Trip> = {
        id: 'trip-1',
        entity_id: 'entity-1',
        platform_id: 'plat-1',
        status: 'active',
        start_latitude: 3.848,
        start_longitude: 11.502,
        started_at: new Date(Date.now() - 600_000), // 10 min ago
        distance_meters: 0,
        duration_seconds: 0,
      };
      mockTripRepo.findOne.mockResolvedValue(activeTrip);
      mockTripRepo.save.mockImplementation((t) => Promise.resolve(t));

      const result = await service.endTrip('trip-1', {
        end_latitude: 3.870,
        end_longitude: 11.520,
      });

      expect(result.status).toBe('completed');
      expect(result.distance_meters).toBeGreaterThan(0);
      expect(result.duration_seconds).toBeGreaterThan(0);
      expect(mockRabbitMQ.publishTripEnded).toHaveBeenCalledTimes(1);
    });

    it('lève NotFoundException pour un trajet inexistant', async () => {
      mockTripRepo.findOne.mockResolvedValue(null);
      await expect(service.endTrip('bad-id', { end_latitude: 0, end_longitude: 0 }))
        .rejects.toThrow(NotFoundException);
    });

    it('lève ConflictException si le trajet est déjà terminé', async () => {
      mockTripRepo.findOne.mockResolvedValue({ id: 'trip-1', status: 'completed' });
      await expect(service.endTrip('trip-1', { end_latitude: 0, end_longitude: 0 }))
        .rejects.toThrow(ConflictException);
    });
  });
});
