/**
 * S2STokenService — Gestion des tokens inter-services.
 * Pattern valide AGT : obtient et cache un token S2S depuis Auth.
 */
import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import axios from 'axios';

@Injectable()
export class S2STokenService {
  private readonly logger = new Logger(S2STokenService.name);
  private readonly CACHE_KEY = 'media_s2s_token';
  private readonly MARGIN_SECONDS = 60;
  private cachedToken: string = '';
  private tokenExpiry: number = 0;

  constructor(private config: ConfigService) {}

  async getToken(): Promise<string> {
    const now = Math.floor(Date.now() / 1000);
    if (this.cachedToken && now < this.tokenExpiry - this.MARGIN_SECONDS) {
      return this.cachedToken;
    }
    return this.fetchNewToken();
  }

  private async fetchNewToken(): Promise<string> {
    const authUrl = this.config.get<string>('S2S_AUTH_URL', '');
    const clientId = this.config.get<string>('S2S_CLIENT_ID', '');
    const clientSecret = this.config.get<string>('S2S_CLIENT_SECRET', '');

    if (!authUrl || !clientId || !clientSecret) {
      this.logger.warn('Variables S2S manquantes');
      return '';
    }

    try {
      const resp = await axios.post(
        `${authUrl}/auth/s2s/token`,
        { client_id: clientId, client_secret: clientSecret },
        { timeout: 5000 },
      );
      const token: string = resp.data?.access_token || '';
      const expiresIn: number = resp.data?.expires_in || 3600;
      this.cachedToken = token;
      this.tokenExpiry = Math.floor(Date.now() / 1000) + expiresIn;
      return token;
    } catch (err) {
      this.logger.error(`Echec token S2S: ${err.message}`);
      return '';
    }
  }
}
