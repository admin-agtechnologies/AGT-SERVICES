import { Controller, Post, Get, Body, Param, Query, UseGuards, HttpCode, HttpStatus } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { TripsService } from './trips.service';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';

@ApiTags('trips')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('api/v1/geo')
export class TripsController {
  constructor(private readonly tripsService: TripsService) {}

  @Post('trips')
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Démarrer un trajet' })
  async startTrip(@Body() body: any) {
    return this.tripsService.startTrip(body);
  }

  @Post('trips/:tripId/end')
  @ApiOperation({ summary: 'Terminer un trajet' })
  async endTrip(@Param('tripId') tripId: string, @Body() body: any) {
    return this.tripsService.endTrip(tripId, body);
  }

  @Get('trips/:tripId')
  @ApiOperation({ summary: 'Détail d\'un trajet' })
  async getTrip(@Param('tripId') tripId: string) {
    return this.tripsService.getTrip(tripId);
  }

  @Get('trips')
  @ApiOperation({ summary: 'Historique des trajets' })
  async listTrips(
    @Query('entity_id') entity_id: string,
    @Query('platform_id') platform_id: string,
    @Query('from_date') from_date: string,
    @Query('to_date') to_date: string,
    @Query('page') page: string,
    @Query('limit') limit: string,
  ) {
    return this.tripsService.listTrips({ entity_id, platform_id, from_date, to_date, page: +page, limit: +limit });
  }
}
