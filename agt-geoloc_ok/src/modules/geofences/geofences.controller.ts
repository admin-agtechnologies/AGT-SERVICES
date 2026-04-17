import { Controller, Post, Get, Put, Delete, Body, Param, Query, UseGuards, HttpCode, HttpStatus } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { GeofencesService } from './geofences.service';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';

@ApiTags('geofences')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('api/v1/geo')
export class GeofencesController {
  constructor(private readonly geofencesService: GeofencesService) {}

  @Post('geofences')
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Créer une zone geofence' })
  async createGeofence(@Body() body: any) { return this.geofencesService.createGeofence(body); }

  @Get('geofences')
  @ApiOperation({ summary: 'Lister les zones' })
  async listGeofences(@Query('platform_id') platform_id: string, @Query('is_active') is_active: string, @Query('tags') tags: string) {
    return this.geofencesService.listGeofences({ platform_id, is_active: is_active === 'true' ? true : is_active === 'false' ? false : undefined, tags: tags ? tags.split(',') : [] });
  }

  @Put('geofences/:id')
  @ApiOperation({ summary: 'Modifier une zone' })
  async updateGeofence(@Param('id') id: string, @Body() body: any) { return this.geofencesService.updateGeofence(id, body); }

  @Delete('geofences/:id')
  @ApiOperation({ summary: 'Désactiver (soft delete) une zone' })
  async deleteGeofence(@Param('id') id: string) { return this.geofencesService.deleteGeofence(id); }
}
