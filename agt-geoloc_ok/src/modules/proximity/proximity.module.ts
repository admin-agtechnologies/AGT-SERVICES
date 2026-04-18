import {
  Controller, Get, Query, UseGuards, BadRequestException,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Injectable } from '@nestjs/common';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { RedisService } from '../../infrastructure/redis/redis.service';
import { PlatformGeoConfig } from '../admin/entities/platform-geo-config.entity';

/**
 * Service de recherche de proximité.
 *
 * Proximité live (Redis) : GEOSEARCH → O(N+log(M)) → < 50ms pour 100K entités.
 * Retourne les entités les plus proches avec leur distance en mètres.
 */
@Injectable()
export class ProximityService {
  constructor(
    private readonly redisService: RedisService,
    @InjectRepository(PlatformGeoConfig)
    private readonly configRepo: Repository<PlatformGeoConfig>,
  ) {}

  async searchProximity(params: {
    platformId: string;
    latitude: number;
    longitude: number;
    radiusKm: number;
    limit: number;
    tags?: string[];
  }) {
    // Vérifier le rayon max autorisé pour cette plateforme
    const config = await this.configRepo.findOne({ where: { platform_id: params.platformId } });
    const maxRadius = config?.max_proximity_radius_km ?? 50;

    if (params.radiusKm > maxRadius) {
      throw new BadRequestException(`Radius exceeds max allowed: ${maxRadius} km`);
    }

    // Recherche via index GEO Redis
    const results = await this.redisService.searchProximity(
      params.platformId, params.latitude, params.longitude,
      params.radiusKm, params.limit,
    );

    // Enrichir avec les payloads détaillés et filtrer par tags
    const enriched = await Promise.all(
      results.map(async ({ entityId, distanceMeters }) => {
        const payload = await this.redisService.getEntityPayload(params.platformId, entityId);
        if (!payload) return null;

        // Filtre par tags si demandé
        if (params.tags?.length) {
          const entityTags: string[] = payload.tags || [];
          const hasAllTags = params.tags.every((t) => entityTags.includes(t));
          if (!hasAllTags) return null;
        }

        return {
          entity_id: entityId,
          latitude: payload.lat,
          longitude: payload.lng,
          distance_meters: Math.round(distanceMeters),
          tags: payload.tags || [],
          recorded_at: payload.recorded_at,
        };
      }),
    );

    const filtered = enriched.filter(Boolean);
    return { results: filtered, total: filtered.length };
  }
}

@ApiTags('proximity')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('api/v1/geo')
export class ProximityController {
  constructor(private readonly proximityService: ProximityService) {}

  /**
   * GET /api/v1/geo/proximity
   * Recherche d'entités dans un rayon donné (Redis live, < 50ms P95).
   */
  @Get('proximity')
  @ApiOperation({ summary: 'Recherche de proximité live' })
  async searchProximity(
    @Query('platform_id') platformId: string,
    @Query('latitude') latitude: string,
    @Query('longitude') longitude: string,
    @Query('radius_km') radiusKm: string,
    @Query('limit') limit: string,
    @Query('tags') tags: string,
  ) {
    return this.proximityService.searchProximity({
      platformId,
      latitude: parseFloat(latitude),
      longitude: parseFloat(longitude),
      radiusKm: parseFloat(radiusKm) || 5,
      limit: parseInt(limit) || 10,
      tags: tags ? tags.split(',') : [],
    });
  }
}

import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [TypeOrmModule.forFeature([PlatformGeoConfig])],
  controllers: [ProximityController],
  providers: [ProximityService],
})
export class ProximityModule {}
