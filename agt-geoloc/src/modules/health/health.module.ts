import { Controller, Get, Injectable, Module } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';
import { RedisService } from '../../infrastructure/redis/redis.service';
import { RabbitMQService } from '../../infrastructure/rabbitmq/rabbitmq.service';

@Injectable()
export class HealthService {
  constructor(
    @InjectDataSource() private readonly dataSource: DataSource,
    private readonly redisService: RedisService,
    private readonly rabbitMQService: RabbitMQService,
  ) {}

  async check() {
    let database = 'ok', postgis = 'ok', redis = 'ok', rabbitmq = 'ok';

    try {
      await this.dataSource.query('SELECT 1');
    } catch { database = 'error'; }

    try {
      await this.dataSource.query("SELECT PostGIS_Version()");
    } catch { postgis = 'unavailable'; }

    try {
      await this.redisService.ping();
    } catch { redis = 'error'; }

    rabbitmq = (await this.rabbitMQService.isHealthy()) ? 'ok' : 'error';

    const allOk = database === 'ok' && redis === 'ok';
    return { status: allOk ? 'healthy' : 'degraded', database, postgis, redis, rabbitmq, version: '1.2.0' };
  }
}

@ApiTags('health')
@Controller('api/v1/geo')
export class HealthController {
  constructor(private readonly healthService: HealthService) {}

  @Get('health')
  @ApiOperation({ summary: 'Health check du service' })
  async health() {
    return this.healthService.check();
  }
}

@Module({
  controllers: [HealthController],
  providers: [HealthService],
})
export class HealthModule {}
