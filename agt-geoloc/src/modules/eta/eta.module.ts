import { Module } from '@nestjs/common';
import { EtaController } from './eta.controller';
import { EtaService } from './eta.service';
import { HaversineProvider } from '../../infrastructure/providers/eta/haversine.provider';
import { OsrmProvider, GoogleMapsProvider, NominatimProvider } from '../../infrastructure/providers/eta/external.providers';
import { ProviderFactory } from '../../infrastructure/providers/eta/provider.factory';

@Module({
  controllers: [EtaController],
  providers: [
    EtaService,
    HaversineProvider,
    OsrmProvider,
    GoogleMapsProvider,
    NominatimProvider,
    ProviderFactory,
  ],
  exports: [EtaService],
})
export class EtaModule {}
