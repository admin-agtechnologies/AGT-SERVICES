import { Injectable, Logger, ServiceUnavailableException } from '@nestjs/common';
import { RedisService } from '../../infrastructure/redis/redis.service';
import { ProviderFactory } from '../../infrastructure/providers/eta/provider.factory';

/**
 * Service ETA & Géocodage — adapter pattern (CDC §F-ETA-04, §F-GCD-04).
 * Cache Redis : TTL 60s ETA, 86400s (24h) géocodage.
 * Fallback automatique vers Haversine si le provider externe échoue.
 */
@Injectable()
export class EtaService {
  private readonly logger = new Logger(EtaService.name);

  constructor(
    private readonly providerFactory: ProviderFactory,
    private readonly redis: RedisService,
  ) {}

  async getDistance(oLat: number, oLng: number, dLat: number, dLng: number, providerName = 'haversine') {
    const cacheKey = `dist:${providerName}:${oLat.toFixed(4)},${oLng.toFixed(4)}->${dLat.toFixed(4)},${dLng.toFixed(4)}`;
    const cached = await this.redis.getCached(cacheKey);
    if (cached) return { ...JSON.parse(cached), cached: true };

    const provider = this.providerFactory.getETAProvider(providerName);
    let result: any;
    try {
      const r = await provider.getDistance(oLat, oLng, dLat, dLng);
      result = { distance_meters: r.distance_m, duration_seconds: r.duration_s, provider: providerName, cached: false };
    } catch (err) {
      this.logger.warn(`Provider ${providerName} failed (distance): ${err.message} — fallback haversine`);
      const fb = this.providerFactory.getFallbackETAProvider();
      const r = await fb.getDistance(oLat, oLng, dLat, dLng);
      result = { distance_meters: r.distance_m, duration_seconds: r.duration_s, provider: `haversine (fallback)`, cached: false };
    }

    await this.redis.setCached(cacheKey, JSON.stringify(result), 60);
    return result;
  }

  async getEta(oLat: number, oLng: number, dLat: number, dLng: number, providerName = 'haversine') {
    const cacheKey = `eta:${providerName}:${oLat.toFixed(4)},${oLng.toFixed(4)}->${dLat.toFixed(4)},${dLng.toFixed(4)}`;
    const cached = await this.redis.getCached(cacheKey);
    if (cached) return { ...JSON.parse(cached), cached: true };

    const provider = this.providerFactory.getETAProvider(providerName);
    let result: any;
    try {
      const r = await provider.getETA(oLat, oLng, dLat, dLng);
      result = { eta_seconds: r.eta_seconds, eta_datetime: r.eta_datetime, provider: providerName, cached: false };
    } catch (err) {
      this.logger.warn(`Provider ${providerName} failed (ETA): ${err.message} — fallback haversine`);
      const fb = this.providerFactory.getFallbackETAProvider();
      const r = await fb.getETA(oLat, oLng, dLat, dLng);
      result = { eta_seconds: r.eta_seconds, eta_datetime: r.eta_datetime, provider: 'haversine (fallback)', cached: false };
    }

    await this.redis.setCached(cacheKey, JSON.stringify(result), 60);
    return result;
  }

  async geocode(address: string, providerName = 'nominatim') {
    const cacheKey = `geocode:${providerName}:${address.toLowerCase().replace(/\s+/g, '_')}`;
    const cached = await this.redis.getCached(cacheKey);
    if (cached) return { ...JSON.parse(cached), cached: true };

    const provider = this.providerFactory.getGeocodingProvider(providerName);
    const r = await provider.geocode(address);
    const result = { latitude: r.lat, longitude: r.lng, formatted_address: r.formatted_address, provider: providerName, cached: false };
    await this.redis.setCached(cacheKey, JSON.stringify(result), 86400);
    return result;
  }

  async reverseGeocode(lat: number, lng: number, providerName = 'nominatim') {
    const cacheKey = `reverse:${providerName}:${lat.toFixed(5)},${lng.toFixed(5)}`;
    const cached = await this.redis.getCached(cacheKey);
    if (cached) return { ...JSON.parse(cached), cached: true };

    const provider = this.providerFactory.getGeocodingProvider(providerName);
    const r = await provider.reverseGeocode(lat, lng);
    const result = { ...r, provider: providerName, cached: false };
    await this.redis.setCached(cacheKey, JSON.stringify(result), 86400);
    return result;
  }
}
