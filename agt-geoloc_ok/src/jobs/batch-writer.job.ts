import { Injectable, Logger } from '@nestjs/common';
import { Cron } from '@nestjs/schedule';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';
import { PositionsService } from '../modules/positions/positions.service';

/**
 * Batch writer PostGIS (NF-14, F-POS-07).
 *
 * Toutes les 15s : vide le buffer de positions accumulées et les insère
 * en un seul INSERT batch dans PostGIS.
 *
 * Pourquoi le batch ? À 20 000 msg/s, un INSERT par position saturerait la DB.
 * Un batch de 15s = ~300 000 lignes insérées en < 2s avec PostgreSQL.
 *
 * On utilise SQL brut car TypeORM ne supporte pas nativement GEOGRAPHY(Point, 4326).
 * ST_MakePoint(lng, lat) — longitude en premier, latitude en second (convention GeoJSON).
 */
@Injectable()
export class BatchWriterJob {
  private readonly logger = new Logger(BatchWriterJob.name);

  constructor(
    private readonly positionsService: PositionsService,
    @InjectDataSource() private readonly dataSource: DataSource,
  ) {}

  @Cron('*/15 * * * * *')
  async flushPositionBuffer() {
    const batch = this.positionsService.flushBuffer();
    if (!batch.length) return;

    try {
      // Construire le INSERT batch
      // Paramètres par ligne : entity_id, lng, lat, heading, speed, accuracy, trip_id, recorded_at
      const placeholders = batch.map((_, i) => {
        const b = i * 8;
        return `($${b+1}, ST_SetSRID(ST_MakePoint($${b+2}, $${b+3}), 4326)::geography, $${b+4}, $${b+5}, $${b+6}, $${b+7}, $${b+8})`;
      }).join(', ');

      const params: any[] = [];
      for (const p of batch) {
        params.push(
          p.entity_id,
          p.longitude,    // ST_MakePoint(lng, lat)
          p.latitude,
          p.heading ?? null,
          p.speed ?? null,
          p.accuracy ?? null,
          p.trip_id ?? null,
          p.recorded_at,
        );
      }

      await this.dataSource.query(
        `INSERT INTO position_history
           (entity_id, location, heading, speed, accuracy, trip_id, recorded_at)
         VALUES ${placeholders}
         ON CONFLICT DO NOTHING`,
        params,
      );

      this.logger.debug(`Batch flush: ${batch.length} positions → PostGIS`);
    } catch (err) {
      this.logger.error(`Batch flush failed: ${err.message}`);
    }
  }
}
