import 'reflect-metadata';
import { NestFactory } from '@nestjs/core';
import { ValidationPipe, Logger } from '@nestjs/common';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const logger = new Logger('Bootstrap');
  const app = await NestFactory.create(AppModule, { logger: ['log', 'error', 'warn', 'debug'] });

  // CORS
  app.enableCors({ origin: '*', methods: 'GET,HEAD,PUT,PATCH,POST,DELETE,OPTIONS', credentials: true });

  // Validation globale des DTOs
  app.useGlobalPipes(new ValidationPipe({ transform: true, whitelist: true, forbidNonWhitelisted: false }));

  // Swagger
  const swaggerConfig = new DocumentBuilder()
    .setTitle('AGT Geolocation Service')
    .setDescription('Service de géolocalisation centralisé — AGT-Geo v1.2\n\nCouvre : positions temps réel (REST + WebSocket), géofencing event-driven, trajets, proximité, ETA/géocodage multi-provider.')
    .setVersion('1.2.0')
    .addBearerAuth()
    .addTag('health', 'Health check')
    .addTag('positions', 'Positions GPS (REST)')
    .addTag('proximity', 'Recherche de proximité')
    .addTag('trips', 'Gestion des trajets')
    .addTag('geofences', 'Zones géographiques')
    .addTag('distance-eta', 'Distance & ETA')
    .addTag('admin', 'Administration & Config')
    .build();

  const document = SwaggerModule.createDocument(app, swaggerConfig);
  SwaggerModule.setup('api/v1/docs', app, document, {
    swaggerOptions: { persistAuthorization: true },
  });

  const port = process.env.PORT || 7009;
  await app.listen(port);
  logger.log(`🌍 Geolocation Service running on port ${port}`);
  logger.log(`📚 Swagger UI: http://localhost:${port}/api/v1/docs`);
  logger.log(`❤️  Health: http://localhost:${port}/api/v1/geo/health`);
}

bootstrap();
