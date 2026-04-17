import { Injectable, NotFoundException, ConflictException, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Geofence } from './entities/geofence.entity';
import { GeofenceCacheService } from '../../infrastructure/geofence-cache.service';
import { RedisService } from '../../infrastructure/redis/redis.service';

/**
 * Service de gestion des geofences.
 * Toute modification déclenche une invalidation ciblée via Redis pub/sub
 * pour que toutes les instances NestJS rechargent uniquement la zone concernée.
 */
@Injectable()
export class GeofencesService {
  private readonly logger = new Logger(GeofencesService.name);

  constructor(
    @InjectRepository(Geofence)
    private readonly geofenceRepo: Repository<Geofence>,
    private readonly geofenceCacheService: GeofenceCacheService,
    private readonly redisService: RedisService,
  ) {}

  async createGeofence(params: {
    platform_id: string; name: string; fence_type: 'polygon' | 'circle';
    coordinates?: number[][]; center_latitude?: number; center_longitude?: number;
    radius_meters?: number; tags?: string[]; metadata?: Record<string, any>;
  }): Promise<Geofence> {
    const existing = await this.geofenceRepo.findOne({
      where: { platform_id: params.platform_id, name: params.name },
    });
    if (existing) throw new ConflictException(`Geofence with name "${params.name}" already exists`);

    const fence = this.geofenceRepo.create({ ...params, is_active: true });
    await this.geofenceRepo.save(fence);

    // Mise à jour immédiate du cache mémoire local + invalidation des autres instances
    this.geofenceCacheService.addOrUpdate(fence);
    await this.redisService.publishGeofenceInvalidation(fence.id);

    return fence;
  }

  async listGeofences(params: { platform_id?: string; is_active?: boolean; tags?: string[] }): Promise<Geofence[]> {
    const qb = this.geofenceRepo.createQueryBuilder('fence');
    if (params.platform_id) qb.andWhere('fence.platform_id = :pid', { pid: params.platform_id });
    if (params.is_active !== undefined) qb.andWhere('fence.is_active = :active', { active: params.is_active });
    if (params.tags?.length) {
      // JSONB contains query
      qb.andWhere('fence.tags @> :tags', { tags: JSON.stringify(params.tags) });
    }
    return qb.getMany();
  }

  async updateGeofence(id: string, params: Partial<Geofence>): Promise<Geofence> {
    const fence = await this.geofenceRepo.findOne({ where: { id } });
    if (!fence) throw new NotFoundException('Geofence not found');

    Object.assign(fence, params);
    await this.geofenceRepo.save(fence);

    // Invalidation ciblée — toutes les instances rechargent cette zone
    this.geofenceCacheService.addOrUpdate(fence);
    await this.redisService.publishGeofenceInvalidation(fence.id);

    return fence;
  }

  /**
   * Soft delete : is_active = false (les données historiques sont conservées).
   * Déclenche l'invalidation du cache sur toutes les instances.
   */
  async deleteGeofence(id: string): Promise<{ success: boolean }> {
    const fence = await this.geofenceRepo.findOne({ where: { id } });
    if (!fence) throw new NotFoundException('Geofence not found');

    fence.is_active = false;
    await this.geofenceRepo.save(fence);

    this.geofenceCacheService.remove(id);
    await this.redisService.publishGeofenceInvalidation(id);

    return { success: true };
  }

  async getGeofence(id: string): Promise<Geofence> {
    const fence = await this.geofenceRepo.findOne({ where: { id } });
    if (!fence) throw new NotFoundException('Geofence not found');
    return fence;
  }
}
