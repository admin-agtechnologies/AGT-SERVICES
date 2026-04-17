import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { OfflineDetectionJob } from './offline-detection.job';
import { BatchWriterJob } from './batch-writer.job';
import { TrackedEntity } from '../modules/positions/entities/tracked-entity.entity';
import { PositionsModule } from '../modules/positions/positions.module';

@Module({
  imports: [
    TypeOrmModule.forFeature([TrackedEntity]),
    PositionsModule,
  ],
  providers: [OfflineDetectionJob, BatchWriterJob],
})
export class JobsModule {}
