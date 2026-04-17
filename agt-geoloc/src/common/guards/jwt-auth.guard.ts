import {
  CanActivate, ExecutionContext, Injectable, Logger, UnauthorizedException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as jwt from 'jsonwebtoken';
import * as fs from 'fs';

/**
 * Guard JWT RS256 — vérifie le token Bearer contre la clé publique du service Auth.
 * Compatible user tokens et S2S tokens.
 */
@Injectable()
export class JwtAuthGuard implements CanActivate {
  private readonly logger = new Logger(JwtAuthGuard.name);
  private publicKey: string;

  constructor(private readonly configService: ConfigService) {
    const keyPath = this.configService.get<string>('auth.publicKeyPath');
    try {
      this.publicKey = fs.readFileSync(keyPath, 'utf8');
      this.logger.log(`JWT public key loaded from ${keyPath}`);
    } catch (err) {
      this.logger.warn(`JWT public key not found at ${keyPath} — JWT validation disabled in dev`);
      this.publicKey = null;
    }
  }

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const token = this.extractToken(request);
    if (!token) throw new UnauthorizedException('Missing Authorization token');

    if (!this.publicKey) {
      // Mode dev sans clé publique : on décode sans vérification
      const decoded = jwt.decode(token) as any;
      if (!decoded) throw new UnauthorizedException('Invalid token');
      request.user = decoded;
      return true;
    }

    try {
      const decoded = jwt.verify(token, this.publicKey, { algorithms: ['RS256'] }) as any;
      request.user = decoded;
      return true;
    } catch (err) {
      throw new UnauthorizedException(`Invalid token: ${err.message}`);
    }
  }

  private extractToken(request: any): string | null {
    const auth = request.headers?.authorization;
    if (auth?.startsWith('Bearer ')) return auth.slice(7);
    return null;
  }
}
