import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigModule } from '@nestjs/config';
import { PlatformConfigController } from './platform-config.controller';
import { PlatformConfigService } from './platform-config.service';
import { PlatformMediaConfig } from './entities/platform-media-config.entity';
import { JwtAuthGuard } from '../common/auth/jwt-auth.guard';
import { S2SGuard } from '../common/auth/s2s.guard';
import { Reflector } from '@nestjs/core';

@Module({
  imports: [ConfigModule, TypeOrmModule.forFeature([PlatformMediaConfig])],
  controllers: [PlatformConfigController],
  providers: [PlatformConfigService, JwtAuthGuard, S2SGuard, Reflector],
  exports: [PlatformConfigService],
})
export class PlatformConfigModule {}
