import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    logger: ['log', 'error', 'warn', 'debug'],
  });

  app.useGlobalPipes(
    new ValidationPipe({ whitelist: true, transform: true, forbidNonWhitelisted: false }),
  );

  app.enableCors();
  app.setGlobalPrefix('api/v1');

  // ──────────────────────────────────────────────────────────────
  // SWAGGER — config complete avec bouton Authorize fonctionnel
  // Acces : http://localhost:7003/api/v1/docs
  // ──────────────────────────────────────────────────────────────
  const config = new DocumentBuilder()
    .setTitle('AGT Media Service v1.4')
    .setDescription(
      `## Service de gestion centralisee des fichiers\n\n` +
      `**Base URL :** \`http://localhost:7003/api/v1\`\n\n` +
      `### Comment s'authentifier\n` +
      `1. Obtenez un token JWT depuis **Auth Service** \`POST /api/v1/auth/s2s/token\`\n` +
      `2. Ou utilisez un token utilisateur depuis \`POST /api/v1/auth/login\`\n` +
      `3. Cliquez sur **Authorize** en haut a droite\n` +
      `4. Entrez le token au format : \`Bearer <votre_token>\`\n\n` +
      `### Tokens acceptes\n` +
      `- **Token utilisateur** : obtenu via Auth login\n` +
      `- **Token S2S** : obtenu via \`POST /auth/s2s/token\` (requis pour hard delete et purge RGPD)\n\n` +
      `### Endpoints S2S-only\n` +
      `\`DELETE /{id}/permanent\` • \`DELETE /by-user/{userId}\` • \`PUT /platforms/{id}/media-config\``,
    )
    .setVersion('1.4')
    .setContact('AGT Engineering', '', 'contact@ag-technologies.com')
    .addServer('http://localhost:7003', 'Local Development')
    // Bouton Authorize avec Bearer JWT
    .addBearerAuth(
      {
        type: 'http',
        scheme: 'bearer',
        bearerFormat: 'JWT',
        name: 'Authorization',
        description: 'Entrez : Bearer <token>',
        in: 'header',
      },
      'BearerAuth',
    )
    .addTag('Health', 'Etat du service et de ses dependances')
    .addTag('Upload', 'Upload fichiers (simple, batch, depuis URL)')
    .addTag('Consultation', 'Telechargement, metadonnees, thumbnails, resize')
    .addTag('Gestion', 'Soft delete, hard delete, visibilite, metadonnees')
    .addTag('RGPD', 'Purge totale fichiers d un utilisateur (S2S uniquement)')
    .addTag('Platform Config', 'Configuration media par plateforme (S2S)')
    .addTag('Statistiques', 'Stats globales et par plateforme')
    .build();

  const document = SwaggerModule.createDocument(app, config);

  SwaggerModule.setup('api/v1/docs', app, document, {
    swaggerOptions: {
      // Token conserve apres refresh de page
      persistAuthorization: true,
      // Afficher les requetes curl dans l'UI
      displayRequestDuration: true,
      // Tous les endpoints deployes par defaut
      docExpansion: 'list',
      // Filtre de recherche dans les endpoints
      filter: true,
      // Afficher les extensions
      showExtensions: true,
      tagsSorter: 'alpha',
      operationsSorter: 'alpha',
    },
    customSiteTitle: 'AGT Media API',
    customCss: `
      .swagger-ui .topbar { background-color: #1e5aa8; }
      .swagger-ui .topbar-wrapper .link span { color: white; font-weight: bold; }
      .swagger-ui .info h2 { color: #1e5aa8; }
      .swagger-ui .btn.authorize { background-color: #1e5aa8; border-color: #1e5aa8; color: white; }
    `,
  });

  const port = process.env.PORT || 7003;
  await app.listen(port);

  console.log(`\n╔══════════════════════════════════════════════╗`);
  console.log(`║  AGT Media Service v1.4 — Port ${port}         ║`);
  console.log(`║  Swagger : http://localhost:${port}/api/v1/docs  ║`);
  console.log(`║  Health  : http://localhost:${port}/api/v1/media/health ║`);
  console.log(`╚══════════════════════════════════════════════╝\n`);
}

bootstrap();
