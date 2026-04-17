import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { PositionsController } from './positions.controller';
import { PositionsService } from './positions.service';
import { PositionsGateway } from './positions.gateway';
import { TrackedEntity } from './entities/tracked-entity.entity';
import { PositionHistory } from './entities/position-history.entity';
import { GeofenceEvent } from '../geofences/entities/geofence-event.entity';
import { PlatformGeoConfig } from '../admin/entities/platform-geo-config.entity';
import { GeofenceCacheService } from '../../infrastructure/geofence-cache.service';
import { Geofence } from '../geofences/entities/geofence.entity';

@Module({
  imports: [
    TypeOrmModule.forFeature([
      TrackedEntity, PositionHistory, GeofenceEvent, PlatformGeoConfig, Geofence,
    ]),
  ],
  controllers: [PositionsController],
  providers: [PositionsService, PositionsGateway, GeofenceCacheService],
  exports: [PositionsService, GeofenceCacheService],
})
export class PositionsModule {}
