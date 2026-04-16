import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { BullModule } from '@nestjs/bullmq';
import { ConfigModule } from '@nestjs/config';
import { MediaController } from './media.controller';
import { MediaService } from './media.service';
import { MediaProcessor, MEDIA_QUEUE } from './media.processor';
import { MediaFile } from './entities/media-file.entity';
import { MediaVariant } from './entities/media-variant.entity';
import { MediaMetadata } from './entities/media-metadata.entity';
import { MediaAccessLog } from './entities/media-access-log.entity';
import { PlatformMediaConfig } from '../platform-config/entities/platform-media-config.entity';
import { LocalStorageProvider } from '../common/storage/local-storage.provider';
import { JwtAuthGuard } from '../common/auth/jwt-auth.guard';
import { S2SGuard } from '../common/auth/s2s.guard';
import { Reflector } from '@nestjs/core';

@Module({
  imports: [
    ConfigModule,
    TypeOrmModule.forFeature([
      MediaFile,
      MediaVariant,
      MediaMetadata,
      MediaAccessLog,
      PlatformMediaConfig,
    ]),
    BullModule.registerQueue({ name: MEDIA_QUEUE }),
  ],
  controllers: [MediaController],
  providers: [
    MediaService,
    MediaProcessor,
    LocalStorageProvider,
    JwtAuthGuard,
    S2SGuard,
    Reflector,
  ],
  exports: [MediaService],
})
export class MediaModule {}
