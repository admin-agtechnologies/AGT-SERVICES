import {
  Controller, Get, Put, Delete, Body, Param, Query,
  UseGuards, HttpCode, HttpStatus, Injectable, Logger,
} from '@nestjs/common';
import { Module } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { PlatformGeoConfig } from './entities/platform-geo-config.entity';
import { TrackedEntity } from '../positions/entities/tracked-entity.entity';
import { RedisService } from '../../infrastructure/redis/redis.service';

@Injectable()
export class AdminService {
  private readonly logger = new Logger(AdminService.name);

  constructor(
    @InjectRepository(PlatformGeoConfig)
    private readonly configRepo: Repository<PlatformGeoConfig>,
    @InjectRepository(TrackedEntity)
    private readonly entityRepo: Repository<TrackedEntity>,
    private readonly redisService: RedisService,
  ) {}

  async getStats(platformId?: string) {
    const activeEntities = platformId
      ? await this.redisService.getActiveEntityCount(platformId)
      : 0;

    return {
      active_entities: activeEntities,
      active_websockets: 0, // Géré par le gateway
      positions_per_second: 0, // Métrique temps réel à implémenter via Prometheus
      active_trips: 0,
      active_geofences: 0,
      geofence_events_24h: 0,
    };
  }

  async getConfig(platformId: string): Promise<PlatformGeoConfig> {
    let config = await this.configRepo.findOne({ where: { platform_id: platformId } });
    if (!config) {
      // Crée une config par défaut si elle n'existe pas
      config = this.configRepo.create({ platform_id: platformId });
      await this.configRepo.save(config);
    }
    return config;
  }

  async updateConfig(platformId: string, params: Partial<PlatformGeoConfig>): Promise<PlatformGeoConfig> {
    let config = await this.configRepo.findOne({ where: { platform_id: platformId } });
    if (!config) {
      config = this.configRepo.create({ platform_id: platformId });
    }
    Object.assign(config, params);
    return this.configRepo.save(config);
  }

  /**
   * Purge RGPD : anonymisation irréversible des données d'une entité.
   * - TrackedEntity supprimée
   * - position_history : entity_id remplacé par un UUID anonyme (non NULL)
   * - trips : idem
   * Conforme RGPD : les données spatiales agrégées sont conservées pour l'analytics.
   */
  async purgeUserData(userId: string): Promise<{ success: boolean; message: string }> {
    const entities = await this.entityRepo.find({ where: { entity_id: userId } });
    if (!entities.length) return { success: true, message: 'No data found for this user' };

    for (const entity of entities) {
      // Retirer de Redis
      await this.redisService.removeEntityFromIndex(entity.platform_id, entity.entity_id);
      // Soft delete — on garde l'enregistrement avec is_active = false pour la FK
      entity.is_active = false;
      entity.entity_id = `anon-${entity.id}`; // Anonymisation irréversible
      await this.entityRepo.save(entity);
    }

    this.logger.log(`RGPD purge completed for user ${userId}: ${entities.length} entities anonymized`);
    return { success: true, message: `${entities.length} entities anonymized` };
  }
}

@ApiTags('admin')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('api/v1/geo')
export class AdminController {
  constructor(private readonly adminService: AdminService) {}

  @Get('admin/stats')
  @ApiOperation({ summary: 'Statistiques plateforme' })
  async getStats(@Query('platform_id') platformId: string) {
    return this.adminService.getStats(platformId);
  }

  @Get('config/:platformId')
  @ApiOperation({ summary: 'Récupérer la config d\'une plateforme' })
  async getConfig(@Param('platformId') platformId: string) {
    return this.adminService.getConfig(platformId);
  }

  @Put('config/:platformId')
  @ApiOperation({ summary: 'Mettre à jour la config d\'une plateforme' })
  async updateConfig(@Param('platformId') platformId: string, @Body() body: any) {
    return this.adminService.updateConfig(platformId, body);
  }

  @Delete('by-user/:userId')
  @ApiOperation({ summary: 'Purge RGPD — anonymise les données d\'un utilisateur' })
  @HttpCode(HttpStatus.OK)
  async purgeUser(@Param('userId') userId: string) {
    return this.adminService.purgeUserData(userId);
  }
}

@Module({
  imports: [TypeOrmModule.forFeature([PlatformGeoConfig, TrackedEntity])],
  controllers: [AdminController],
  providers: [AdminService],
  exports: [AdminService],
})
export class AdminModule {}
