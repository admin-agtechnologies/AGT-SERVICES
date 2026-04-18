import { Injectable } from '@nestjs/common';

// ── Interfaces (adapter pattern CDC §F-ETA-04) ────────────────────────────────

export interface DistanceResult {
  distance_m: number;
  duration_s: number;
}

export interface ETAResult {
  eta_seconds: number;
  eta_datetime: string;
}

export interface GeocodeResult {
  lat: number;
  lng: number;
  formatted_address: string;
}

export interface ReverseGeocodeResult {
  address: string;
  city: string;
  country: string;
}

export interface IETAProvider {
  getDistance(originLat: number, originLng: number, destLat: number, destLng: number): Promise<DistanceResult>;
  getETA(originLat: number, originLng: number, destLat: number, destLng: number): Promise<ETAResult>;
}

export interface IGeocodingProvider {
  geocode(address: string): Promise<GeocodeResult>;
  reverseGeocode(lat: number, lng: number): Promise<ReverseGeocodeResult>;
}

/**
 * Provider Haversine (interne, gratuit).
 * Calcul vol d'oiseau — utilisé comme fallback et pour les distances rapides.
 * Formule Haversine : précision < 0.5% pour distances < 1000 km.
 */
@Injectable()
export class HaversineProvider implements IETAProvider {
  readonly name = 'haversine';

  async getDistance(oLat: number, oLng: number, dLat: number, dLng: number): Promise<DistanceResult> {
    const R = 6371000;
    const toRad = (d: number) => (d * Math.PI) / 180;
    const dLat2 = toRad(dLat - oLat);
    const dLng2 = toRad(dLng - oLng);
    const a = Math.sin(dLat2/2)**2 + Math.cos(toRad(oLat)) * Math.cos(toRad(dLat)) * Math.sin(dLng2/2)**2;
    const dist = R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    // Estimation ETA à 50 km/h (fallback grossier — préférer OSRM/Google pour la précision)
    const duration_s = Math.round((dist / 1000) / 50 * 3600);
    return { distance_m: Math.round(dist), duration_s };
  }

  async getETA(oLat: number, oLng: number, dLat: number, dLng: number): Promise<ETAResult> {
    const { duration_s } = await this.getDistance(oLat, oLng, dLat, dLng);
    return { eta_seconds: duration_s, eta_datetime: new Date(Date.now() + duration_s * 1000).toISOString() };
  }
}
