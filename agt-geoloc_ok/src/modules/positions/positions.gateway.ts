import {
  WebSocketGateway, WebSocketServer, SubscribeMessage,
  OnGatewayConnection, OnGatewayDisconnect, MessageBody,
  ConnectedSocket,
} from '@nestjs/websockets';
import { Logger } from '@nestjs/common';
import { Server, Socket } from 'socket.io';
import * as jwt from 'jsonwebtoken';
import * as fs from 'fs';
import { ConfigService } from '@nestjs/config';
import { PositionsService } from './positions.service';
import { RedisService } from '../../infrastructure/redis/redis.service';
import { RabbitMQService } from '../../infrastructure/rabbitmq/rabbitmq.service';

/**
 * Gateway WebSocket pour le streaming de positions en temps réel.
 *
 * Règles d'autorisation (CDC v1.1) :
 * - Cas 1 : Un client peut toujours écouter sa propre position
 * - Cas 2 : Suivi d'autres entités → vérifié via cache Redis geo:auth:{userId}:{platformId}
 * - Cas 3 : Abonnement massif → réservé aux tokens S2S ou admin plateforme
 *
 * Événements client → serveur :
 *   position:update     → mise à jour de position
 *   position:subscribe  → s'abonner aux positions d'autres entités
 *   position:unsubscribe
 *
 * Événements serveur → client :
 *   position:updated    → position d'une entité suivie
 *   position:offline    → entité passée offline
 *   geofence:trigger    → événement geofence
 */
@WebSocketGateway({ namespace: '/geo', cors: { origin: '*' } })
export class PositionsGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer() server: Server;
  private readonly logger = new Logger(PositionsGateway.name);
  private publicKey: string;

  /** Map userId → socketId pour le routage des mises à jour */
  private readonly clientMap = new Map<string, string>();

  constructor(
    private readonly positionsService: PositionsService,
    private readonly redisService: RedisService,
    private readonly rabbitMQService: RabbitMQService,
    private readonly configService: ConfigService,
  ) {
    const keyPath = this.configService.get<string>('auth.publicKeyPath');
    try {
      this.publicKey = fs.readFileSync(keyPath, 'utf8');
    } catch {
      this.logger.warn('JWT public key not found — WS token validation relaxed in dev');
      this.publicKey = null;
    }
  }

  /** Authentification lors de la connexion WebSocket */
  async handleConnection(client: Socket) {
    try {
      const token = this.extractToken(client);
      if (!token) { client.disconnect(); return; }

      const decoded = this.verifyToken(token);
      if (!decoded) { client.disconnect(); return; }

      // Stocke les infos utilisateur dans les données du socket
      (client as any).user = decoded;
      this.clientMap.set(decoded.sub, client.id);
      this.logger.debug(`WS connected: ${decoded.sub} → socket ${client.id}`);
    } catch (err) {
      this.logger.warn(`WS connection rejected: ${err.message}`);
      client.disconnect();
    }
  }

  handleDisconnect(client: Socket) {
    const user = (client as any).user;
    if (user?.sub) this.clientMap.delete(user.sub);
    this.logger.debug(`WS disconnected: socket ${client.id}`);
  }

  /** Mise à jour de position via WebSocket (haute fréquence) */
  @SubscribeMessage('position:update')
  async handlePositionUpdate(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: any,
  ) {
    const user = (client as any).user;
    if (!user) return;

    try {
      const geofenceEvents = await this.positionsService.handlePositionUpdate({
        platform_id: data.platform_id,
        entity_type: data.entity_type || 'user',
        entity_id: data.entity_id || user.sub,
        latitude: data.latitude,
        longitude: data.longitude,
        heading: data.heading,
        speed: data.speed,
        accuracy: data.accuracy,
        tags: data.tags,
        recorded_at: data.recorded_at,
      });

      // Diffuse la position aux abonnés (dans la room de l'entité)
      const room = `entity:${data.entity_id || user.sub}`;
      this.server.to(room).emit('position:updated', {
        entity_id: data.entity_id || user.sub,
        latitude: data.latitude,
        longitude: data.longitude,
        heading: data.heading,
        speed: data.speed,
        recorded_at: data.recorded_at || new Date().toISOString(),
      });

      // Émet les événements geofence aux abonnés
      for (const ev of geofenceEvents) {
        this.server.to(room).emit('geofence:trigger', {
          entity_id: data.entity_id || user.sub,
          geofence_id: ev.geofence_id,
          name: ev.name,
          event: ev.event,
          location: { latitude: data.latitude, longitude: data.longitude },
        });
      }
    } catch (err) {
      this.logger.error(`position:update error: ${err.message}`);
      client.emit('error', { message: 'Position update failed' });
    }
  }

  /**
   * Abonnement aux positions d'autres entités.
   * Vérifie les autorisations selon les règles CDC v1.1.
   */
  @SubscribeMessage('position:subscribe')
  async handleSubscribe(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { platform_id: string; entity_ids: string[] },
  ) {
    const user = (client as any).user;
    if (!user) return;

    const allowedEntityIds = await this.getAuthorizedEntityIds(
      user.sub, data.platform_id, data.entity_ids, user,
    );

    for (const entityId of allowedEntityIds) {
      await client.join(`entity:${entityId}`);
    }

    this.logger.debug(`WS subscribe: user=${user.sub} → entities=${allowedEntityIds.join(',')}`);
    client.emit('position:subscribed', { entity_ids: allowedEntityIds });
  }

  @SubscribeMessage('position:unsubscribe')
  async handleUnsubscribe(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { entity_ids: string[] },
  ) {
    for (const entityId of data.entity_ids || []) {
      await client.leave(`entity:${entityId}`);
    }
  }

  /**
   * Vérifie les autorisations d'abonnement WebSocket.
   * - L'utilisateur peut toujours s'abonner à lui-même
   * - Pour les autres entités : vérification via cache Redis
   * - Token S2S ou admin plateforme : accès illimité
   */
  private async getAuthorizedEntityIds(
    userId: string,
    platformId: string,
    requestedIds: string[],
    user: any,
  ): Promise<string[]> {
    // S2S ou admin → accès illimité
    if (user.type === 's2s' || user.role === 'platform_admin' || user.role === 'global_admin') {
      return requestedIds;
    }

    // Cache d'autorisations (défini par le backend produit)
    const cachedAllowed = await this.redisService.getWsAuthCache(userId, platformId);
    const allowedSet = new Set(cachedAllowed || []);

    return requestedIds.filter((id) => id === userId || allowedSet.has(id));
  }

  /** Notifie les abonnés qu'une entité est passée offline */
  notifyEntityOffline(entityId: string, platformId: string) {
    this.server.to(`entity:${entityId}`).emit('position:offline', { entity_id: entityId });
  }

  private extractToken(client: Socket): string | null {
    const auth = client.handshake.auth?.token || client.handshake.query?.token;
    if (typeof auth === 'string') return auth.replace('Bearer ', '');
    return null;
  }

  private verifyToken(token: string): any {
    if (!this.publicKey) return jwt.decode(token);
    return jwt.verify(token, this.publicKey, { algorithms: ['RS256'] });
  }
}
