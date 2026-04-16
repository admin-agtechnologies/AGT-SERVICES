/**
 * Guard d'authentification JWT.
 *
 * Pourquoi : Chaque requete vers Media doit etre accompagnee d'un JWT valide.
 * Media ne valide pas le JWT lui-meme -- il delegue a Auth via verify-token (JWT user)
 * ou s2s/introspect (token S2S).
 *
 * Pattern valide AGT : CDC Media v1.4 §8.1 & §8.2
 */
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  UnauthorizedException,
  Logger,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Reflector } from '@nestjs/core';
import axios from 'axios';

export const IS_PUBLIC_KEY = 'isPublic';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  private readonly logger = new Logger(JwtAuthGuard.name);
  private readonly authUrl: string;

  constructor(
    private config: ConfigService,
    private reflector: Reflector,
  ) {
    this.authUrl = config.get<string>('AUTH_SERVICE_URL', 'http://agt-auth-service:7000/api/v1');
  }

  async canActivate(context: ExecutionContext): Promise<boolean> {
    // Verifier si l'endpoint est marque comme public
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (isPublic) return true;

    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers['authorization'];

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      throw new UnauthorizedException('Token JWT manquant');
    }

    const token = authHeader.substring(7);

    try {
      // Tentative 1 : validation JWT utilisateur
      const payload = await this.verifyUserToken(token);
      if (payload) {
        request.auth = payload;
        return true;
      }
    } catch {
      // Tentative 2 : validation token S2S
      try {
        const s2sPayload = await this.introspectS2SToken(token);
        if (s2sPayload) {
          request.auth = { ...s2sPayload, is_s2s: true };
          return true;
        }
      } catch (s2sErr) {
        this.logger.warn(`Token invalide (user + S2S): ${s2sErr.message}`);
      }
    }

    throw new UnauthorizedException('Token invalide ou expire');
  }

  /**
   * Valide un JWT utilisateur via Auth.
   * GET /auth/verify-token
   */
  private async verifyUserToken(token: string): Promise<any> {
    const response = await axios.get(`${this.authUrl}/auth/verify-token`, {
      headers: { Authorization: `Bearer ${token}` },
      timeout: 5000,
    });
    return response.data;
  }

  /**
   * Valide un token S2S via introspection Auth.
   * POST /auth/s2s/introspect
   */
  private async introspectS2SToken(token: string): Promise<any> {
    const response = await axios.post(
      `${this.authUrl}/auth/s2s/introspect`,
      { token },
      {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 5000,
      },
    );
    return { ...response.data, is_s2s: true };
  }
}
