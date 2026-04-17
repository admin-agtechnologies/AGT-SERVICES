import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import axios from 'axios';
import {
  IETAProvider, IGeocodingProvider,
  DistanceResult, ETAResult, GeocodeResult, ReverseGeocodeResult,
} from './haversine.provider';

/**
 * Provider OSRM (Open Source Routing Machine).
 * Self-hosted, gratuit. Distance et ETA routière.
 */
@Injectable()
export class OsrmProvider implements IETAProvider {
  private readonly logger = new Logger(OsrmProvider.name);
  private readonly baseUrl: string;

  constructor(private readonly configService: ConfigService) {
    this.baseUrl = this.configService.get('providers.osrmUrl');
  }

  async getDistance(originLat: number, originLng: number, destLat: number, destLng: number): Promise<DistanceResult> {
    const url = `${this.baseUrl}/route/v1/driving/${originLng},${originLat};${destLng},${destLat}?overview=false`;
    const { data } = await axios.get(url, { timeout: 5000 });
    const route = data.routes?.[0];
    if (!route) throw new Error('OSRM: no route found');
    return { distance_m: route.distance, duration_s: Math.round(route.duration) };
  }

  async getETA(originLat: number, originLng: number, destLat: number, destLng: number): Promise<ETAResult> {
    const { duration_s } = await this.getDistance(originLat, originLng, destLat, destLng);
    return {
      eta_seconds: duration_s,
      eta_datetime: new Date(Date.now() + duration_s * 1000).toISOString(),
    };
  }
}

/**
 * Provider Google Maps.
 * Payant, distance routière précise, trafic temps réel.
 */
@Injectable()
export class GoogleMapsProvider implements IETAProvider, IGeocodingProvider {
  private readonly logger = new Logger(GoogleMapsProvider.name);
  private readonly apiKey: string;

  constructor(private readonly configService: ConfigService) {
    this.apiKey = this.configService.get('providers.googleMapsApiKey');
  }

  async getDistance(originLat: number, originLng: number, destLat: number, destLng: number): Promise<DistanceResult> {
    const url = `https://maps.googleapis.com/maps/api/distancematrix/json`;
    const { data } = await axios.get(url, {
      params: {
        origins: `${originLat},${originLng}`,
        destinations: `${destLat},${destLng}`,
        key: this.apiKey,
      },
      timeout: 8000,
    });
    const element = data.rows?.[0]?.elements?.[0];
    if (element?.status !== 'OK') throw new Error(`Google Maps: ${element?.status}`);
    return {
      distance_m: element.distance.value,
      duration_s: element.duration.value,
    };
  }

  async getETA(originLat: number, originLng: number, destLat: number, destLng: number): Promise<ETAResult> {
    const { duration_s } = await this.getDistance(originLat, originLng, destLat, destLng);
    return {
      eta_seconds: duration_s,
      eta_datetime: new Date(Date.now() + duration_s * 1000).toISOString(),
    };
  }

  async geocode(address: string): Promise<GeocodeResult> {
    const url = `https://maps.googleapis.com/maps/api/geocode/json`;
    const { data } = await axios.get(url, {
      params: { address, key: this.apiKey },
      timeout: 8000,
    });
    const result = data.results?.[0];
    if (!result) throw new Error('Google Maps geocoding: no result');
    return {
      lat: result.geometry.location.lat,
      lng: result.geometry.location.lng,
      formatted_address: result.formatted_address,
    };
  }

  async reverseGeocode(lat: number, lng: number): Promise<ReverseGeocodeResult> {
    const url = `https://maps.googleapis.com/maps/api/geocode/json`;
    const { data } = await axios.get(url, {
      params: { latlng: `${lat},${lng}`, key: this.apiKey },
      timeout: 8000,
    });
    const result = data.results?.[0];
    if (!result) throw new Error('Google Maps reverse geocoding: no result');
    const components = result.address_components;
    const city = components.find((c: any) => c.types.includes('locality'))?.long_name || '';
    const country = components.find((c: any) => c.types.includes('country'))?.long_name || '';
    return { address: result.formatted_address, city, country };
  }
}

/**
 * Provider Nominatim (OpenStreetMap, gratuit).
 * Géocodage direct et inverse. Respecter la politique d'usage (max 1 req/s).
 */
@Injectable()
export class NominatimProvider implements IGeocodingProvider {
  private readonly logger = new Logger(NominatimProvider.name);
  private readonly baseUrl: string;

  constructor(private readonly configService: ConfigService) {
    this.baseUrl = this.configService.get('providers.nominatimUrl');
  }

  async geocode(address: string): Promise<GeocodeResult> {
    const { data } = await axios.get(`${this.baseUrl}/search`, {
      params: { q: address, format: 'json', limit: 1 },
      headers: { 'User-Agent': 'AGT-Geoloc-Service/1.2' },
      timeout: 8000,
    });
    if (!data?.length) throw new Error('Nominatim: address not found');
    return {
      lat: parseFloat(data[0].lat),
      lng: parseFloat(data[0].lon),
      formatted_address: data[0].display_name,
    };
  }

  async reverseGeocode(lat: number, lng: number): Promise<ReverseGeocodeResult> {
    const { data } = await axios.get(`${this.baseUrl}/reverse`, {
      params: { lat, lon: lng, format: 'json' },
      headers: { 'User-Agent': 'AGT-Geoloc-Service/1.2' },
      timeout: 8000,
    });
    if (!data?.display_name) throw new Error('Nominatim: coordinates not found');
    return {
      address: data.display_name,
      city: data.address?.city || data.address?.town || data.address?.village || '',
      country: data.address?.country || '',
    };
  }
}
