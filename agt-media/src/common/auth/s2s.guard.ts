/**
 * Guard S2S — vérifie que la requête provient d'un token S2S.
 *
 * Pourquoi : certains endpoints (hard delete, purge RGPD) sont
 * réservés aux appels inter-services uniquement.
 * CDC Media v1.4 §6.4 & §6.5 : hard delete S2S-only.
 */
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  ForbiddenException,
} from '@nestjs/common';

@Injectable()
export class S2SGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const auth = request.auth;

    if (!auth || !auth.is_s2s) {
      throw new ForbiddenException(
        'Cet endpoint est réservé aux tokens S2S (service-to-service)',
      );
    }

    return true;
  }
}
