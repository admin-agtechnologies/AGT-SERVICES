import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Geofence } from './entities/geofence.entity';
import { GeofenceEvent } from './entities/geofence-event.entity';
import { GeofencesController } from './geofences.controller';
import { GeofencesService } from './geofences.service';
import { GeofenceCacheService } from '../../infrastructure/geofence-cache.service';

@Module({
  imports: [TypeOrmModule.forFeature([Geofence, GeofenceEvent])],
  controllers: [GeofencesController],
  providers: [GeofencesService, GeofenceCacheService],
  exports: [GeofencesService],
})
export class GeofencesModule {}
