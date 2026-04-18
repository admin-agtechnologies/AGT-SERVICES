import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { TrackedEntity } from './entities/tracked-entity.entity';
import { PositionHistory } from './entities/position-history.entity';
import { RedisService } from '../../infrastructure/redis/redis.service';
import { RabbitMQService } from '../../infrastructure/rabbitmq/rabbitmq.service';
import { GeofenceCacheService } from '../../infrastructure/geofence-cache.service';
import { GeofenceEvent } from '../geofences/entities/geofence-event.entity';
import { PlatformGeoConfig } from '../admin/entities/platform-geo-config.entity';

export interface PositionUpdatePayload {
  platform_id: string;
  entity_type: string;
  entity_id: string;
  latitude: number;
  longitude: number;
  heading?: number;
  speed?: number;
  accuracy?: number;
  tags?: string[];
  recorded_at?: string;
  trip_id?: string;
}

export interface GeofenceTrigger {
  geofence_id: string;
  name: string;
  event: 'enter' | 'exit';
}

/**
 * Service principal pour la mise à jour et la lecture des positions.
 *
 * Flux d'une mise à jour de position :
 * 1. Récupérer ou créer la TrackedEntity
 * 2. Mise à jour atomique Redis (couche A GEO + couche B payload)
 * 3. Vérification geofence (O(log Z) via cache mémoire)
 * 4. Buffering pour batch write PostGIS
 * 5. Publication RabbitMQ (position.updated, geofence events)
 */
@Injectable()
export class PositionsService {
  private readonly logger = new Logger(PositionsService.name);

  /**
   * Buffer de positions en attente d'insertion PostGIS.
   * Vidé par le BatchWriterJob toutes les batch_flush_seconds.
   */
  private readonly positionBuffer: Array<{
    entity_id: string;
    latitude: number;
    longitude: number;
    heading: number;
    speed: number;
    accuracy: number;
    trip_id: string;
    recorded_at: Date;
  }> = [];

  constructor(
    @InjectRepository(TrackedEntity)
    private readonly entityRepo: Repository<TrackedEntity>,
    @InjectRepository(PositionHistory)
    private readonly positionRepo: Repository<PositionHistory>,
    @InjectRepository(GeofenceEvent)
    private readonly geofenceEventRepo: Repository<GeofenceEvent>,
    @InjectRepository(PlatformGeoConfig)
    private readonly configRepo: Repository<PlatformGeoConfig>,
    private readonly redisService: RedisService,
    private readonly rabbitMQService: RabbitMQService,
    private readonly geofenceCacheService: GeofenceCacheService,
  ) {}

  /**
   * Traite une mise à jour de position.
   * Retourne les événements geofence détectés.
   */
  async handlePositionUpdate(payload: PositionUpdatePayload): Promise<GeofenceTrigger[]> {
    const now = payload.recorded_at ? new Date(payload.recorded_at) : new Date();

    // 1. Récupérer ou créer la TrackedEntity
    const entity = await this.getOrCreateEntity(
      payload.platform_id, payload.entity_type, payload.entity_id, payload.tags,
    );

    // 2. Récupérer la config plateforme pour le TTL Redis
    const config = await this.getPlatformConfig(payload.platform_id);
    const ttl = config?.position_ttl_seconds ?? 30;

    // 3. Mise à jour atomique Redis (dual storage)
    await this.redisService.updateEntityPosition(
      payload.platform_id,
      payload.entity_id,
      payload.latitude,
      payload.longitude,
      {
        entity_type: payload.entity_type,
        heading: payload.heading,
        speed: payload.speed,
        accuracy: payload.accuracy,
        tags: payload.tags || entity.tags,
        recorded_at: now.toISOString(),
      },
      ttl,
    );

    // 4. Mettre à jour last_seen_at en DB (non bloquant)
    entity.last_seen_at = now;
    entity.tags = payload.tags || entity.tags;
    this.entityRepo.save(entity).catch((e) => this.logger.error('Entity save error', e.message));

    // 5. Buffer pour insertion PostGIS en batch
    this.positionBuffer.push({
      entity_id: entity.id,
      latitude: payload.latitude,
      longitude: payload.longitude,
      heading: payload.heading ?? null,
      speed: payload.speed ?? null,
      accuracy: payload.accuracy ?? null,
      trip_id: payload.trip_id ?? null,
      recorded_at: now,
    });

    // 6. Vérification geofencing event-driven
    const geofenceEvents = await this.checkGeofences(
      entity, payload.platform_id, payload.latitude, payload.longitude, now,
    );

    // 7. Publication RabbitMQ position.updated
    await this.rabbitMQService.publishPositionUpdated({
      entity_id: payload.entity_id,
      platform_id: payload.platform_id,
      latitude: payload.latitude,
      longitude: payload.longitude,
      speed: payload.speed,
      heading: payload.heading,
      tags: payload.tags || entity.tags,
      recorded_at: now.toISOString(),
    });

    return geofenceEvents;
  }

  /**
   * Vérification geofencing event-driven.
   * Compare l'état précédent (Redis) avec l'état actuel (cache mémoire).
   * Émet un événement seulement sur changement d'état (enter/exit).
   */
  private async checkGeofences(
    entity: TrackedEntity,
    platformId: string,
    lat: number,
    lng: number,
    recordedAt: Date,
  ): Promise<GeofenceTrigger[]> {
    const triggers: GeofenceTrigger[] = [];

    // Zones contenant le point actuel (O(log Z) via R-tree mémoire)
    const currentFences = this.geofenceCacheService.getFencesContaining(platformId, lat, lng);
    const currentFenceIds = new Set(currentFences.map((f) => f.id));

    // Zones précédentes depuis Redis
    const previousFenceIds = new Set(await this.redisService.getEntityFences(entity.id));

    // Entrées (nouvelles zones)
    for (const fence of currentFences) {
      if (!previousFenceIds.has(fence.id)) {
        triggers.push({ geofence_id: fence.id, name: fence.name, event: 'enter' });
        await this.persistGeofenceEvent(fence.id, entity.id, 'enter', lat, lng, recordedAt);
        await this.rabbitMQService.publishGeofenceEvent('enter', {
          entity_id: entity.entity_id,
          geofence_id: fence.id,
          geofence_name: fence.name,
          platform_id: platformId,
          latitude: lat,
          longitude: lng,
          recorded_at: recordedAt.toISOString(),
        });
      }
    }

    // Sorties (zones quittées)
    for (const fenceId of previousFenceIds) {
      if (!currentFenceIds.has(fenceId)) {
        const fence = this.geofenceCacheService.getAll().find((f) => f.id === fenceId);
        const fenceName = fence?.name ?? fenceId;
        triggers.push({ geofence_id: fenceId, name: fenceName, event: 'exit' });
        await this.persistGeofenceEvent(fenceId, entity.id, 'exit', lat, lng, recordedAt);
        await this.rabbitMQService.publishGeofenceEvent('exit', {
          entity_id: entity.entity_id,
          geofence_id: fenceId,
          geofence_name: fenceName,
          platform_id: platformId,
          latitude: lat,
          longitude: lng,
          recorded_at: recordedAt.toISOString(),
        });
      }
    }

    // Persister le nouvel état geofence dans Redis
    await this.redisService.setEntityFences(entity.id, Array.from(currentFenceIds));

    return triggers;
  }

  private async persistGeofenceEvent(
    geofenceId: string, entityId: string, eventType: 'enter' | 'exit',
    lat: number, lng: number, recordedAt: Date,
  ) {
    const ev = this.geofenceEventRepo.create({
      geofence_id: geofenceId, entity_id: entityId,
      event_type: eventType, latitude: lat, longitude: lng, recorded_at: recordedAt,
    });
    await this.geofenceEventRepo.save(ev).catch((e) => this.logger.error('GeofenceEvent save error', e.message));
  }

  /** Récupère ou crée une TrackedEntity */
  async getOrCreateEntity(
    platformId: string, entityType: string, entityId: string, tags?: string[],
  ): Promise<TrackedEntity> {
    let entity = await this.entityRepo.findOne({
      where: { platform_id: platformId, entity_type: entityType, entity_id: entityId },
    });
    if (!entity) {
      entity = this.entityRepo.create({
        platform_id: platformId, entity_type: entityType,
        entity_id: entityId, tags: tags || [], is_active: true,
      });
      await this.entityRepo.save(entity);
      this.logger.debug(`TrackedEntity created: ${entityId}`);
    }
    return entity;
  }

  /** Dernière position connue depuis Redis */
  async getLastPosition(platformId: string, entityId: string): Promise<any> {
    const payload = await this.redisService.getEntityPayload(platformId, entityId);
    if (!payload) throw new NotFoundException('Entity not found or offline');
    return { entity_id: entityId, ...payload };
  }

  /** Retourne et vide le buffer de positions pour le batch write */
  flushBuffer(): typeof this.positionBuffer {
    return this.positionBuffer.splice(0, this.positionBuffer.length);
  }

  getBufferSize(): number {
    return this.positionBuffer.length;
  }

  private async getPlatformConfig(platformId: string): Promise<PlatformGeoConfig | null> {
    return this.configRepo.findOne({ where: { platform_id: platformId } });
  }
}
