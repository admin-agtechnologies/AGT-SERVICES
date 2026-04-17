import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { BullModule } from '@nestjs/bullmq';
import { MediaModule } from './media/media.module';
import { HealthModule } from './health/health.module';
import { PlatformConfigModule } from './platform-config/platform-config.module';
import { MediaFile } from './media/entities/media-file.entity';
import { MediaVariant } from './media/entities/media-variant.entity';
import { MediaMetadata } from './media/entities/media-metadata.entity';
import { MediaAccessLog } from './media/entities/media-access-log.entity';
import { PlatformMediaConfig } from './platform-config/entities/platform-media-config.entity';

@Module({
  imports: [
    // Configuration globale depuis .env
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: ['.env', '.env.example'],
    }),

    // PostgreSQL — base de données des métadonnées
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: (config: ConfigService) => ({
        type: 'postgres',
        url: config.get<string>('DATABASE_URL'),
        entities: [
          MediaFile,
          MediaVariant,
          MediaMetadata,
          MediaAccessLog,
          PlatformMediaConfig,
        ],
        synchronize: config.get('NODE_ENV') !== 'production',
        logging: config.get('NODE_ENV') === 'development',
        ssl:
          config.get('NODE_ENV') === 'production'
            ? { rejectUnauthorized: false }
            : false,
      }),
      inject: [ConfigService],
    }),

    // Redis + BullMQ — queue de traitement asynchrone
    BullModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: (config: ConfigService) => ({
        connection: {
          host: new URL(config.get<string>('REDIS_URL', 'redis://localhost:6379')).hostname,
          port: parseInt(
            new URL(config.get<string>('REDIS_URL', 'redis://localhost:6379')).port || '6379',
          ),
        },
      }),
      inject: [ConfigService],
    }),

    // Modules métier
    HealthModule,
    MediaModule,
    PlatformConfigModule,
  ],
})
export class AppModule {}
