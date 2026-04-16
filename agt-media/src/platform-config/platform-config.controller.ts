import { Controller, Get, Put, Param, Body, UseGuards, ParseUUIDPipe } from '@nestjs/common';
import { ApiTags, ApiBearerAuth, ApiOperation } from '@nestjs/swagger';
import { PlatformConfigService } from './platform-config.service';
import { JwtAuthGuard } from '../common/auth/jwt-auth.guard';
import { S2SGuard } from '../common/auth/s2s.guard';

class UpsertConfigDto {
  allowed_types?: string[];
  max_size_bytes?: Record<string, number>;
  thumbnail_sizes?: string[];
  compression_quality?: number;
  storage_quota_bytes?: number;
}

@ApiTags('Platform Config')
@ApiBearerAuth('BearerAuth')
@UseGuards(JwtAuthGuard)
@Controller('platforms')
export class PlatformConfigController {
  constructor(private readonly service: PlatformConfigService) {}

  /**
   * GET /api/v1/platforms/:platformId/media-config
   * Retourne la configuration media d'une plateforme.
   */
  @Get(':platformId/media-config')
  @ApiOperation({ summary: 'Configuration media d une plateforme' })
  async getConfig(@Param('platformId', ParseUUIDPipe) platformId: string) {
    const config = await this.service.getConfig(platformId);
    return { success: true, data: config };
  }

  /**
   * PUT /api/v1/platforms/:platformId/media-config
   * Upsert -- S2S ou admin requis.
   */
  @Put(':platformId/media-config')
  @UseGuards(S2SGuard)
  @ApiOperation({ summary: 'Upsert configuration media d une plateforme S2S' })
  async upsertConfig(
    @Param('platformId', ParseUUIDPipe) platformId: string,
    @Body() dto: UpsertConfigDto,
  ) {
    const config = await this.service.upsertConfig(platformId, dto);
    return { success: true, data: config };
  }
}
