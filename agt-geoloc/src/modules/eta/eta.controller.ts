import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth, ApiQuery } from '@nestjs/swagger';
import { EtaService } from './eta.service';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';

@ApiTags('distance-eta')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('api/v1/geo')
export class EtaController {
  constructor(private readonly etaService: EtaService) {}

  @Get('distance')
  @ApiOperation({ summary: 'Distance entre deux points (vol d\'oiseau ou routière)' })
  async getDistance(
    @Query('origin_lat') oLat: string,
    @Query('origin_lng') oLng: string,
    @Query('dest_lat') dLat: string,
    @Query('dest_lng') dLng: string,
    @Query('provider') provider: string,
  ) {
    return this.etaService.getDistance(+oLat, +oLng, +dLat, +dLng, provider || 'haversine');
  }

  @Get('eta')
  @ApiOperation({ summary: 'Temps estimé d\'arrivée entre deux points' })
  async getEta(
    @Query('origin_lat') oLat: string,
    @Query('origin_lng') oLng: string,
    @Query('dest_lat') dLat: string,
    @Query('dest_lng') dLng: string,
    @Query('provider') provider: string,
  ) {
    return this.etaService.getEta(+oLat, +oLng, +dLat, +dLng, provider || 'haversine');
  }

  @Get('geocode')
  @ApiOperation({ summary: 'Géocodage : adresse → coordonnées' })
  async geocode(
    @Query('address') address: string,
    @Query('provider') provider: string,
  ) {
    return this.etaService.geocode(address, provider || 'nominatim');
  }

  @Get('reverse-geocode')
  @ApiOperation({ summary: 'Géocodage inverse : coordonnées → adresse' })
  async reverseGeocode(
    @Query('latitude') lat: string,
    @Query('longitude') lng: string,
    @Query('provider') provider: string,
  ) {
    return this.etaService.reverseGeocode(+lat, +lng, provider || 'nominatim');
  }
}
