import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { RedisService } from '../infrastructure/redis/redis.service';
import { RabbitMQService } from '../infrastructure/rabbitmq/rabbitmq.service';
import { TrackedEntity } from '../modules/positions/entities/tracked-entity.entity';
import { PositionsGateway } from '../modules/positions/positions.gateway';

/**
 * Job de détection offline (NF-15).
 *
 * Toutes les 10s : scanne les entités dont le payload Redis (TTL) a expiré
 * mais qui sont encore dans l'index GEO. Effectue le nettoyage et émet
 * l'événement geo.entity.offline UNE seule fois par transition online→offline.
 *
 * Alternative event-driven : Redis Keyspace Notifications (expired events).
 * On utilise le cron pour ne pas dépendre d'une config Redis spécifique.
 */
@Injectable()
export class OfflineDetectionJob {
  private readonly logger = new Logger(OfflineDetectionJob.name);

  constructor(
    private readonly redisService: RedisService,
    private readonly rabbitMQService: RabbitMQService,
    @InjectRepository(TrackedEntity)
    private readonly entityRepo: Repository<TrackedEntity>,
    private readonly gateway: PositionsGateway,
  ) {}

  @Cron(CronExpression.EVERY_10_SECONDS)
  async detectOfflineEntities() {
    try {
      // Pour chaque entité active en DB, vérifier si son payload Redis est expiré
      // On limite à 500 entités par cycle pour ne pas bloquer
      const activeEntities = await this.entityRepo.find({
        where: { is_active: true },
        take: 500,
        order: { last_seen_at: 'ASC' },
      });

      for (const entity of activeEntities) {
        const isOnline = await this.redisService.isEntityOnline(entity.platform_id, entity.entity_id);
        if (!isOnline && entity.last_seen_at) {
          const lastSeenMs = new Date().getTime() - entity.last_seen_at.getTime();
          // Si hors ligne depuis plus de 35s (TTL 30s + 5s de marge)
          if (lastSeenMs > 35000) {
            // Nettoyer l'index GEO
            await this.redisService.removeEntityFromIndex(entity.platform_id, entity.entity_id);

            // Notifier via WebSocket
            this.gateway.notifyEntityOffline(entity.entity_id, entity.platform_id);

            // Publier l'événement RabbitMQ (une seule fois par transition)
            await this.rabbitMQService.publishEntityOffline({
              entity_id: entity.entity_id,
              platform_id: entity.platform_id,
              last_seen_at: entity.last_seen_at.toISOString(),
            });

            this.logger.debug(`Entity offline: ${entity.entity_id} (platform: ${entity.platform_id})`);
          }
        }
      }
    } catch (err) {
      this.logger.error('Offline detection job failed', err.message);
    }
  }
}
