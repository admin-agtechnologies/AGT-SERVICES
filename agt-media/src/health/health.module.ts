/**
 * Health Check -- CDC Media v1.4 §3.10 (NF-10)
 * GET /api/v1/media/health -- endpoint public, pas de JWT requis.
 */
import { Controller, Get, Module } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';
import { Public } from '../common/auth/public.decorator';

@ApiTags('Health')
@Controller('media')
export class HealthController {
  constructor(@InjectDataSource() private dataSource: DataSource) {}

  @Public()
  @Get('health')
  @ApiOperation({ summary: 'Health check du service Media' })
  async health() {
    let dbStatus = 'ok';
    try {
      await this.dataSource.query('SELECT 1');
    } catch {
      dbStatus = 'error';
    }

    const status = dbStatus === 'ok' ? 'healthy' : 'degraded';

    return {
      status,
      service: 'agt-media',
      version: '1.0.0',
      database: dbStatus,
      timestamp: new Date().toISOString(),
    };
  }
}

@Module({
  controllers: [HealthController],
})
export class HealthModule {}
