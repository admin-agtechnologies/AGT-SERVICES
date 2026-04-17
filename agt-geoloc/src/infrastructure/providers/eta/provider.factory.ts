import { Injectable } from '@nestjs/common';
import { HaversineProvider, IETAProvider, IGeocodingProvider } from './haversine.provider';
import { OsrmProvider, GoogleMapsProvider, NominatimProvider } from './external.providers';

/**
 * Factory qui résout le bon provider selon le nom demandé.
 * Adapter pattern : ajouter un provider = ajouter un case ici.
 *
 * Fallback : si le provider demandé échoue, on tombe sur Haversine.
 */
@Injectable()
export class ProviderFactory {
  constructor(
    private readonly haversine: HaversineProvider,
    private readonly osrm: OsrmProvider,
    private readonly googleMaps: GoogleMapsProvider,
    private readonly nominatim: NominatimProvider,
  ) {}

  getETAProvider(name: string): IETAProvider {
    switch (name) {
      case 'osrm': return this.osrm;
      case 'google_maps': return this.googleMaps;
      case 'haversine':
      default: return this.haversine;
    }
  }

  getGeocodingProvider(name: string): IGeocodingProvider {
    switch (name) {
      case 'google_maps': return this.googleMaps;
      case 'nominatim':
      default: return this.nominatim;
    }
  }

  getFallbackETAProvider(): IETAProvider {
    return this.haversine;
  }
}
