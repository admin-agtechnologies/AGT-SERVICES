import {
  Injectable, CanActivate, ExecutionContext,
  UnauthorizedException, Logger,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import axios from 'axios';
import { RedisService } from '../../infrastructure/redis/redis.service';

/**
 * Guard JWT pour les endpoints REST.
 * Valide le token Bearer via le service Auth.
 * Cache la validation Redis TTL 30s pour éviter les appels répétés.
 */
@Injectable()
export class JwtAuthGuard implements CanActivate {
  private readonly logger = new Logger(JwtAuthGuard.name);
  private readonly authUrl: string;

  constructor(
    private readonly configService: ConfigService,
    private readonly redisService: RedisService,
  ) {
    this.authUrl = this.configService.get('auth.serviceUrl');
  }

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractToken(request);

    if (!token) throw new UnauthorizedException('Missing Bearer token');

    // Vérifie le cache Redis avant d'appeler Auth
    const cacheKey = `jwt:${token.substring(0, 32)}`;
    const cached = await this.redisService.getCached(cacheKey);
    if (cached) {
      request.user = JSON.parse(cached);
      return true;
    }

    try {
      const { data } = await axios.get(`${this.authUrl}/api/v1/auth/verify-token`, {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 3000,
      });
      const userInfo = { sub: data.sub || data.user_id, platform_id: data.platform_id, token };
      await this.redisService.setCached(cacheKey, JSON.stringify(userInfo), 30);
      request.user = userInfo;
      return true;
    } catch (err) {
      // En mode développement sans Auth service, on accepte les tokens mock
      if (process.env.NODE_ENV === 'development' && process.env.AUTH_BYPASS === 'true') {
        this.logger.warn('AUTH_BYPASS enabled — skipping token validation');
        request.user = { sub: 'dev-user', platform_id: 'dev-platform', token };
        return true;
      }
      throw new UnauthorizedException('Invalid or expired token');
    }
  }

  private extractToken(request: any): string | null {
    const auth = request.headers?.authorization;
    if (!auth?.startsWith('Bearer ')) return null;
    return auth.substring(7);
  }
}

/**
 * Guard S2S (Service-to-Service).
 * Vérifie que le token est un token S2S émis par Auth.
 */
@Injectable()
export class S2SAuthGuard implements CanActivate {
  private readonly authUrl: string;

  constructor(
    private readonly configService: ConfigService,
    private readonly redisService: RedisService,
  ) {
    this.authUrl = this.configService.get('auth.serviceUrl');
  }

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractToken(request);
    if (!token) throw new UnauthorizedException('Missing S2S Bearer token');

    const cacheKey = `s2s:${token.substring(0, 32)}`;
    const cached = await this.redisService.getCached(cacheKey);
    if (cached) {
      request.s2s = JSON.parse(cached);
      return true;
    }

    try {
      const { data } = await axios.post(
        `${this.authUrl}/api/v1/auth/s2s/introspect`,
        {},
        { headers: { Authorization: `Bearer ${token}` }, timeout: 3000 },
      );
      const s2sInfo = { client_id: data.client_id, platform_id: data.platform_id };
      await this.redisService.setCached(cacheKey, JSON.stringify(s2sInfo), 30);
      request.s2s = s2sInfo;
      return true;
    } catch {
      if (process.env.NODE_ENV === 'development' && process.env.AUTH_BYPASS === 'true') {
        request.s2s = { client_id: 'dev-s2s', platform_id: 'dev-platform' };
        return true;
      }
      throw new UnauthorizedException('Invalid S2S token');
    }
  }

  private extractToken(request: any): string | null {
    const auth = request.headers?.authorization;
    if (!auth?.startsWith('Bearer ')) return null;
    return auth.substring(7);
  }
}

/**
 * Guard flexible : accepte JWT ou S2S.
 * Utilisé pour les endpoints accessibles aux deux types de clients.
 */
@Injectable()
export class AnyAuthGuard implements CanActivate {
  constructor(
    private readonly jwtGuard: JwtAuthGuard,
    private readonly s2sGuard: S2SAuthGuard,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    try {
      return await this.jwtGuard.canActivate(context);
    } catch {
      try {
        return await this.s2sGuard.canActivate(context);
      } catch {
        throw new UnauthorizedException('Valid JWT or S2S token required');
      }
    }
  }
}
