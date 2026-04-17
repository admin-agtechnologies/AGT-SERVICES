import { Injectable, Logger, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import Redis from 'ioredis';

/**
 * Service Redis centralisé pour le Geoloc Service.
 *
 * Architecture dual-storage (CDC v1.1) :
 *
 * Couche A — Index GEO par plateforme (GEOADD/GEOSEARCH) :
 *   Clé : geo:index:{platform_id}
 *   Usage : EXCLUSIVEMENT pour la recherche de proximité live
 *
 * Couche B — Payload détaillé par entité :
 *   Clé : geo:entity:{platform_id}:{entity_id}
 *   Usage : lecture de la dernière position, diffusion WebSocket
 *   TTL : configurable (défaut 30s) → expiration = entité offline
 *
 * Règle : la mise à jour des deux couches est ATOMIQUE via pipeline Redis.
 */
@Injectable()
export class RedisService implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(RedisService.name);
  private client: Redis;
  private subscriberClient: Redis;

  constructor(private readonly configService: ConfigService) {}

  async onModuleInit() {
    const config = this.configService.get('redis');
    const options = {
      host: config.host,
      port: config.port,
      password: config.password || undefined,
      lazyConnect: false,
      retryStrategy: (times: number) => Math.min(times * 100, 3000),
    };
    this.client = new Redis(options);
    this.subscriberClient = new Redis(options);
    this.client.on('error', (err) => this.logger.error('Redis client error', err.message));
    this.logger.log(`Redis connected → ${config.host}:${config.port}`);
  }

  async onModuleDestroy() {
    await this.client?.quit();
    await this.subscriberClient?.quit();
  }

  getClient(): Redis {
    return this.client;
  }

  getSubscriberClient(): Redis {
    return this.subscriberClient;
  }

  // ── Couche A : Index GEO par plateforme ─────────────────────────────

  /**
   * Mise à jour atomique des deux couches Redis (pipeline).
   * Couche A : GEOADD geo:index:{platform_id}
   * Couche B : SET geo:entity:{platform_id}:{entity_id} avec TTL
   */
  async updateEntityPosition(
    platformId: string,
    entityId: string,
    lat: number,
    lng: number,
    payload: Record<string, any>,
    ttlSeconds: number,
  ): Promise<void> {
    const geoKey = `geo:index:${platformId}`;
    const entityKey = `geo:entity:${platformId}:${entityId}`;
    const payloadStr = JSON.stringify({ ...payload, lat, lng, is_online: true });

    // Pipeline atomique : les deux couches sont mises à jour ensemble
    const pipeline = this.client.pipeline();
    pipeline.geoadd(geoKey, lng, lat, entityId);
    pipeline.set(entityKey, payloadStr, 'EX', ttlSeconds);
    await pipeline.exec();
  }

  /**
   * Supprime une entité de l'index GEO et de son payload.
   * Utilisé lors de la transition online → offline.
   */
  async removeEntityFromIndex(platformId: string, entityId: string): Promise<void> {
    const geoKey = `geo:index:${platformId}`;
    const entityKey = `geo:entity:${platformId}:${entityId}`;
    const pipeline = this.client.pipeline();
    pipeline.zrem(geoKey, entityId);
    pipeline.del(entityKey);
    await pipeline.exec();
  }

  /**
   * Recherche de proximité via GEOSEARCH (Redis 6.2+).
   * Retourne les entity_ids dans le rayon donné, triés par distance.
   */
  async searchProximity(
    platformId: string,
    lat: number,
    lng: number,
    radiusKm: number,
    limit: number,
  ): Promise<Array<{ entityId: string; distanceMeters: number }>> {
    const geoKey = `geo:index:${platformId}`;
    try {
      // GEOSEARCH avec BYRADIUS, ASC, WITHCOORD WITHDIST COUNT
      const results = await this.client.call(
        'GEOSEARCH',
        geoKey, 'FROMLONLAT', lng, lat,
        'BYRADIUS', radiusKm, 'km',
        'ASC', 'COUNT', limit, 'WITHDIST',
      ) as any[];
      return results.map((r: any) => ({
        entityId: r[0],
        distanceMeters: parseFloat(r[1]) * 1000, // WITHDIST retourne en km
      }));
    } catch (err) {
      this.logger.warn(`GEOSEARCH failed, trying GEORADIUSBYMEMBER fallback: ${err.message}`);
      return [];
    }
  }

  // ── Couche B : Payload entité ────────────────────────────────────────

  async getEntityPayload(platformId: string, entityId: string): Promise<Record<string, any> | null> {
    const key = `geo:entity:${platformId}:${entityId}`;
    const val = await this.client.get(key);
    return val ? JSON.parse(val) : null;
  }

  async isEntityOnline(platformId: string, entityId: string): Promise<boolean> {
    const key = `geo:entity:${platformId}:${entityId}`;
    return (await this.client.exists(key)) === 1;
  }

  // ── Cache geofences (état précédent des entités) ──────────────────────

  /** Stocke les zones dans lesquelles se trouve actuellement une entité */
  async setEntityFences(entityId: string, fenceIds: string[]): Promise<void> {
    const key = `geo:fences:${entityId}`;
    await this.client.set(key, JSON.stringify(fenceIds), 'EX', 300);
  }

  async getEntityFences(entityId: string): Promise<string[]> {
    const key = `geo:fences:${entityId}`;
    const val = await this.client.get(key);
    return val ? JSON.parse(val) : [];
  }

  // ── Cache ETA / Géocodage ─────────────────────────────────────────────

  async getCached(key: string): Promise<string | null> {
    return this.client.get(`cache:${key}`);
  }

  async setCached(key: string, value: string, ttlSeconds: number): Promise<void> {
    await this.client.set(`cache:${key}`, value, 'EX', ttlSeconds);
  }

  // ── Cache autorisation WebSocket ──────────────────────────────────────

  async getWsAuthCache(userId: string, platformId: string): Promise<string[] | null> {
    const key = `geo:auth:${userId}:${platformId}`;
    const val = await this.client.get(key);
    return val ? JSON.parse(val) : null;
  }

  async setWsAuthCache(userId: string, platformId: string, allowedEntityIds: string[]): Promise<void> {
    const key = `geo:auth:${userId}:${platformId}`;
    await this.client.set(key, JSON.stringify(allowedEntityIds), 'EX', 300);
  }

  // ── Pub/Sub pour invalidation cache geofence ──────────────────────────

  async publishGeofenceInvalidation(geofenceId: string): Promise<void> {
    await this.client.publish('geo:geofence:invalidate', geofenceId);
  }

  async subscribeGeofenceInvalidation(handler: (geofenceId: string) => void): Promise<void> {
    await this.subscriberClient.subscribe('geo:geofence:invalidate');
    this.subscriberClient.on('message', (_channel: string, message: string) => {
      handler(message);
    });
  }

  // ── Utilitaires ────────────────────────────────────────────────────────

  async ping(): Promise<string> {
    return this.client.ping();
  }

  /** Récupère le nombre de membres dans l'index GEO d'une plateforme */
  async getActiveEntityCount(platformId: string): Promise<number> {
    return this.client.zcard(`geo:index:${platformId}`);
  }
}
