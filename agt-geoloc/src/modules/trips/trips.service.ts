import {
  Injectable, NotFoundException, ConflictException, Logger,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Trip } from './entities/trip.entity';
import { RabbitMQService } from '../../infrastructure/rabbitmq/rabbitmq.service';
import * as turf from '@turf/turf';

/**
 * Service de gestion des trajets.
 *
 * Machine à états : active → completed | cancelled
 * Un seul trajet active par (platform_id, entity_id).
 * Les positions GPS existent hors trajet (trip_id = NULL).
 */
@Injectable()
export class TripsService {
  private readonly logger = new Logger(TripsService.name);

  constructor(
    @InjectRepository(Trip)
    private readonly tripRepo: Repository<Trip>,
    private readonly rabbitMQService: RabbitMQService,
  ) {}

  /** Démarre un nouveau trajet */
  async startTrip(params: {
    platform_id: string; entity_id: string;
    start_latitude: number; start_longitude: number;
    metadata?: Record<string, any>;
  }): Promise<Trip> {
    // Vérifie qu'il n'existe pas déjà un trajet actif
    const existing = await this.tripRepo.findOne({
      where: { entity_id: params.entity_id, platform_id: params.platform_id, status: 'active' },
    });
    if (existing) throw new ConflictException('Active trip already exists for this entity');

    const trip = this.tripRepo.create({
      entity_id: params.entity_id,
      platform_id: params.platform_id,
      status: 'active',
      start_latitude: params.start_latitude,
      start_longitude: params.start_longitude,
      metadata: params.metadata,
      started_at: new Date(),
    });
    await this.tripRepo.save(trip);

    await this.rabbitMQService.publishTripStarted({
      trip_id: trip.id,
      entity_id: trip.entity_id,
      platform_id: trip.platform_id,
      start_latitude: trip.start_latitude,
      start_longitude: trip.start_longitude,
    });

    return trip;
  }

  /** Termine un trajet actif */
  async endTrip(tripId: string, params: { end_latitude: number; end_longitude: number }): Promise<Trip> {
    const trip = await this.tripRepo.findOne({ where: { id: tripId } });
    if (!trip) throw new NotFoundException('Trip not found');
    if (trip.status !== 'active') throw new ConflictException('Trip is not active');

    const now = new Date();
    const durationSeconds = Math.round((now.getTime() - trip.started_at.getTime()) / 1000);

    // Distance vol d'oiseau entre départ et arrivée (approximation sans les points intermédiaires)
    const from = turf.point([trip.start_longitude, trip.start_latitude]);
    const to = turf.point([params.end_longitude, params.end_latitude]);
    const distanceKm = turf.distance(from, to, { units: 'kilometers' });

    trip.status = 'completed';
    trip.end_latitude = params.end_latitude;
    trip.end_longitude = params.end_longitude;
    trip.distance_meters = Math.round(distanceKm * 1000);
    trip.duration_seconds = durationSeconds;
    trip.ended_at = now;

    await this.tripRepo.save(trip);

    await this.rabbitMQService.publishTripEnded({
      trip_id: trip.id,
      entity_id: trip.entity_id,
      platform_id: trip.platform_id,
      distance_meters: trip.distance_meters,
      duration_seconds: trip.duration_seconds,
    });

    return trip;
  }

  async getTrip(tripId: string): Promise<Trip> {
    const trip = await this.tripRepo.findOne({ where: { id: tripId } });
    if (!trip) throw new NotFoundException('Trip not found');
    return trip;
  }

  async listTrips(params: {
    entity_id?: string; platform_id?: string;
    from_date?: string; to_date?: string;
    page?: number; limit?: number;
  }) {
    const qb = this.tripRepo.createQueryBuilder('trip');
    if (params.entity_id) qb.andWhere('trip.entity_id = :entity_id', { entity_id: params.entity_id });
    if (params.platform_id) qb.andWhere('trip.platform_id = :platform_id', { platform_id: params.platform_id });
    if (params.from_date) qb.andWhere('trip.started_at >= :from', { from: params.from_date });
    if (params.to_date) qb.andWhere('trip.started_at <= :to', { to: params.to_date });

    const page = params.page || 1;
    const limit = Math.min(params.limit || 20, 100);
    qb.skip((page - 1) * limit).take(limit).orderBy('trip.started_at', 'DESC');

    const [trips, total] = await qb.getManyAndCount();
    return { trips, total, page, limit };
  }
}
