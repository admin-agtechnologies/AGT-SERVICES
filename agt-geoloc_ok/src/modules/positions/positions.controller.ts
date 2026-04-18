import {
  Controller, Post, Get, Body, Param, Query,
  UseGuards, HttpCode, HttpStatus,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth, ApiResponse } from '@nestjs/swagger';
import { PositionsService } from './positions.service';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { IsLatitude, IsLongitude, IsString, IsOptional, IsArray, IsNumber, IsDateString } from 'class-validator';
import { Type } from 'class-transformer';

class UpdatePositionDto {
  @IsString() platform_id: string;
  @IsString() entity_type: string;
  @IsString() entity_id: string;
  @IsNumber() @Type(() => Number) latitude: number;
  @IsNumber() @Type(() => Number) longitude: number;
  @IsOptional() @IsNumber() @Type(() => Number) heading?: number;
  @IsOptional() @IsNumber() @Type(() => Number) speed?: number;
  @IsOptional() @IsNumber() @Type(() => Number) accuracy?: number;
  @IsOptional() @IsArray() tags?: string[];
  @IsOptional() @IsDateString() recorded_at?: string;
}

@ApiTags('positions')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('api/v1/geo')
export class PositionsController {
  constructor(private readonly positionsService: PositionsService) {}

  /**
   * POST /api/v1/geo/positions
   * Envoi d'une position via REST (usage ponctuel ou batch mobile).
   */
  @Post('positions')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Envoyer une position (REST)' })
  @ApiResponse({ status: 200, description: 'Position mise à jour, geofence events éventuels retournés' })
  async updatePosition(@Body() dto: UpdatePositionDto) {
    const geofenceEvents = await this.positionsService.handlePositionUpdate(dto);
    return {
      entity_id: dto.entity_id,
      status: 'updated',
      geofence_events: geofenceEvents,
    };
  }

  /**
   * GET /api/v1/geo/positions/:entityId
   * Dernière position connue depuis Redis (temps réel).
   */
  @Get('positions/:entityId')
  @ApiOperation({ summary: 'Dernière position connue' })
  @ApiResponse({ status: 200, description: 'Position live depuis Redis' })
  @ApiResponse({ status: 404, description: 'Entité hors ligne ou inconnue' })
  async getPosition(
    @Param('entityId') entityId: string,
    @Query('platform_id') platformId: string,
  ) {
    return this.positionsService.getLastPosition(platformId, entityId);
  }
}
