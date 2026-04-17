import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ScheduleModule } from '@nestjs/schedule';

import configuration from './config/configuration';
import { RedisModule } from './infrastructure/redis/redis.module';
import { RabbitMQModule } from './infrastructure/rabbitmq/rabbitmq.module';

import { PositionsModule } from './modules/positions/positions.module';
import { ProximityModule } from './modules/proximity/proximity.module';
import { TripsModule } from './modules/trips/trips.module';
import { GeofencesModule } from './modules/geofences/geofences.module';
import { EtaModule } from './modules/eta/eta.module';
import { AdminModule } from './modules/admin/admin.module';
import { HealthModule } from './modules/health/health.module';
import { JobsModule } from './jobs/jobs.module';

// Entités
import { TrackedEntity } from './modules/positions/entities/tracked-entity.entity';
import { PositionHistory } from './modules/positions/entities/position-history.entity';
import { Trip } from './modules/trips/entities/trip.entity';
import { Geofence } from './modules/geofences/entities/geofence.entity';
import { GeofenceEvent } from './modules/geofences/entities/geofence-event.entity';
import { PlatformGeoConfig } from './modules/admin/entities/platform-geo-config.entity';

@Module({
  imports: [
    // Config globale
    ConfigModule.forRoot({
      isGlobal: true,
      load: [configuration],
    }),

    // Tâches planifiées (offline detection, batch flush)
    ScheduleModule.forRoot(),

    // Base de données PostgreSQL + PostGIS
    TypeOrmModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (cfg: ConfigService) => ({
        type: 'postgres',
        host: cfg.get('database.host'),
        port: cfg.get('database.port'),
        username: cfg.get('database.username'),
        password: cfg.get('database.password'),
        database: cfg.get('database.database'),
        entities: [
          TrackedEntity, PositionHistory, Trip,
          Geofence, GeofenceEvent, PlatformGeoConfig,
        ],
        synchronize: cfg.get('nodeEnv') !== 'production',
        logging: cfg.get('nodeEnv') === 'development',
        ssl: cfg.get('nodeEnv') === 'production' ? { rejectUnauthorized: false } : false,
      }),
    }),

    // Infrastructure partagée (global)
    RedisModule,
    RabbitMQModule,

    // Modules métier
    PositionsModule,
    ProximityModule,
    TripsModule,
    GeofencesModule,
    EtaModule,
    AdminModule,
    HealthModule,
    JobsModule,
  ],
})
export class AppModule {}
