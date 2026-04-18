import { Injectable, Logger, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { v4 as uuidv4 } from 'uuid';

/**
 * Service RabbitMQ — publication des événements géolocalisation.
 * Utilise require() pour éviter les conflits de types amqplib.
 *
 * Exchange topic 'agt.geoloc' :
 *   geo.position.updated  → MboaMove dispatch
 *   geo.geofence.*        → AGT-Market + Notification push
 *   geo.trip.*            → plateformes
 *   geo.entity.offline    → détection de présence
 */
@Injectable()
export class RabbitMQService implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(RabbitMQService.name);
  private connection: any = null;
  private channel: any = null;
  private readonly exchange: string;
  private isConnected = false;

  constructor(private readonly configService: ConfigService) {
    this.exchange = this.configService.get<string>('rabbitmq.exchange') || 'agt.geoloc';
  }

  async onModuleInit() {
    await this.connect();
  }

  private async connect() {
    try {
      const amqp = require('amqplib');
      const url = this.configService.get<string>('rabbitmq.url');
      this.connection = await amqp.connect(url);
      this.channel = await this.connection.createChannel();
      await this.channel.assertExchange(this.exchange, 'topic', { durable: true });
      this.isConnected = true;
      this.logger.log(`RabbitMQ connected → exchange: ${this.exchange}`);

      this.connection.on('error', (err: Error) => {
        this.logger.error('RabbitMQ error', err.message);
        this.isConnected = false;
      });
      this.connection.on('close', () => {
        this.logger.warn('RabbitMQ closed — reconnect needed');
        this.isConnected = false;
      });
    } catch (err) {
      this.logger.error(`RabbitMQ connection failed: ${err.message}`);
      this.isConnected = false;
    }
  }

  async onModuleDestroy() {
    try {
      await this.channel?.close();
      await this.connection?.close();
    } catch (_) {}
  }

  /** Publie un événement avec event_id, timestamp, source (conventions AGT). */
  async publish(routingKey: string, data: Record<string, any>): Promise<void> {
    if (!this.isConnected || !this.channel) {
      this.logger.warn(`RabbitMQ not ready, dropping: ${routingKey}`);
      return;
    }
    try {
      const event = {
        event_id: uuidv4(),
        timestamp: new Date().toISOString(),
        source: 'geo-service',
        ...data,
      };
      this.channel.publish(
        this.exchange,
        routingKey,
        Buffer.from(JSON.stringify(event)),
        { persistent: true, contentType: 'application/json' },
      );
    } catch (err) {
      this.logger.error(`publish ${routingKey} failed: ${err.message}`);
    }
  }

  async publishPositionUpdated(p: { entity_id: string; platform_id: string; latitude: number; longitude: number; speed?: number; heading?: number; tags?: string[]; recorded_at: string }) {
    await this.publish('geo.position.updated', p);
  }
  async publishGeofenceEvent(type: 'enter' | 'exit', p: { entity_id: string; geofence_id: string; geofence_name: string; platform_id: string; latitude: number; longitude: number; recorded_at: string }) {
    await this.publish(`geo.geofence.${type}`, p);
  }
  async publishTripStarted(p: { trip_id: string; entity_id: string; platform_id: string; start_latitude: number; start_longitude: number }) {
    await this.publish('geo.trip.started', p);
  }
  async publishTripEnded(p: { trip_id: string; entity_id: string; platform_id: string; distance_meters: number; duration_seconds: number }) {
    await this.publish('geo.trip.ended', p);
  }
  async publishEntityOffline(p: { entity_id: string; platform_id: string; last_seen_at: string }) {
    await this.publish('geo.entity.offline', p);
  }
  async isHealthy(): Promise<boolean> {
    return this.isConnected;
  }
}
