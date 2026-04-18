import { Injectable, Logger, OnModuleInit } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import * as turf from '@turf/turf';
import { Geofence } from '../modules/geofences/entities/geofence.entity';
import { RedisService } from './redis/redis.service';

/**
 * Cache mémoire des geofences avec vérification spatiale via turf.js.
 *
 * Architecture event-driven (CDC §5.3) :
 * - Au démarrage : charge toutes les zones actives en mémoire
 * - Invalidation ciblée via Redis pub/sub (pas rechargement complet)
 * - Vérification en O(Z_platform) mais très rapide en pratique
 *   car les zones sont filtrées par plateforme avant test spatial.
 *
 * Pourquoi pas de polling ? À 20 000 updates/s, vérifier toutes les zones
 * à chaque mise à jour de position via la DB serait catastrophique.
 * Le cache mémoire + pub/sub Redis donne une cohérence acceptable
 * avec une latence d'invalidation < 100ms.
 */
@Injectable()
export class GeofenceCacheService implements OnModuleInit {
  private readonly logger = new Logger(GeofenceCacheService.name);
  /** Cache principal : geofenceId → Geofence */
  private readonly fenceCache = new Map<string, Geofence>();

  constructor(
    @InjectRepository(Geofence)
    private readonly geofenceRepo: Repository<Geofence>,
    private readonly redisService: RedisService,
  ) {}

  async onModuleInit() {
    await this.loadAllActive();
    await this.subscribeToInvalidations();
  }

  /** Charge toutes les zones actives au démarrage */
  private async loadAllActive() {
    try {
      const fences = await this.geofenceRepo.find({ where: { is_active: true } });
      this.fenceCache.clear();
      fences.forEach((f) => this.fenceCache.set(f.id, f));
      this.logger.log(`Geofence cache loaded: ${fences.length} active zones`);
    } catch (err) {
      this.logger.error('Failed to load geofence cache', err.message);
    }
  }

  /** Écoute les invalidations ciblées via Redis pub/sub */
  private async subscribeToInvalidations() {
    await this.redisService.subscribeGeofenceInvalidation(async (geofenceId) => {
      try {
        const fence = await this.geofenceRepo.findOne({ where: { id: geofenceId } });
        if (fence && fence.is_active) {
          this.fenceCache.set(fence.id, fence);
        } else {
          this.fenceCache.delete(geofenceId);
        }
        this.logger.debug(`Geofence cache invalidated: ${geofenceId}`);
      } catch (err) {
        this.logger.error(`Cache invalidation failed for ${geofenceId}`, err.message);
      }
    });
  }

  addOrUpdate(fence: Geofence) {
    if (fence.is_active) {
      this.fenceCache.set(fence.id, fence);
    } else {
      this.fenceCache.delete(fence.id);
    }
  }

  remove(geofenceId: string) {
    this.fenceCache.delete(geofenceId);
  }

  /**
   * Retourne toutes les zones contenant le point donné pour une plateforme.
   * Filtre d'abord par platform_id, puis test spatial via turf.js.
   */
  getFencesContaining(platformId: string, lat: number, lng: number): Geofence[] {
    const point = turf.point([lng, lat]);
    const result: Geofence[] = [];

    for (const fence of this.fenceCache.values()) {
      if (fence.platform_id !== platformId) continue;
      try {
        if (this.pointInFence(point, fence)) result.push(fence);
      } catch (err) {
        this.logger.warn(`Geofence check error for ${fence.id}: ${err.message}`);
      }
    }
    return result;
  }

  private pointInFence(point: turf.Feature<turf.Point>, fence: Geofence): boolean {
    if (fence.fence_type === 'circle') {
      if (!fence.center_latitude || !fence.center_longitude || !fence.radius_meters) return false;
      const center = turf.point([Number(fence.center_longitude), Number(fence.center_latitude)]);
      const distM = turf.distance(point, center, { units: 'meters' });
      return distM <= fence.radius_meters;
    }
    if (fence.fence_type === 'polygon' && fence.coordinates?.length >= 4) {
      const polygon = turf.polygon([fence.coordinates]);
      return turf.booleanPointInPolygon(point, polygon);
    }
    return false;
  }

  getAll(): Geofence[] { return Array.from(this.fenceCache.values()); }
  getCount(): number { return this.fenceCache.size; }
  getByPlatform(platformId: string): Geofence[] {
    return Array.from(this.fenceCache.values()).filter((f) => f.platform_id === platformId);
  }
}
