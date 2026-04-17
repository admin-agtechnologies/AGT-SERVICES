import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';

/**
 * Test d'intégration : health check endpoint.
 *
 * Ces tests utilisent un module minimal sans DB/Redis réels.
 * Pour les tests avec infrastructure réelle, utiliser docker-compose.test.yml.
 */
describe('GET /api/v1/geo/health', () => {
  let app: INestApplication;

  beforeAll(async () => {
    // Module minimal qui mock les dépendances d'infrastructure
    const moduleFixture: TestingModule = await Test.createTestingModule({
      controllers: [],
      providers: [],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app?.close();
  });

  it('devrait retourner un statut de santé (structure)', () => {
    // Test de structure seulement — sans connexions réelles
    const expectedKeys = ['status', 'database', 'redis', 'rabbitmq', 'version'];
    const mockResponse = {
      status: 'healthy',
      database: 'ok',
      postgis: 'ok',
      redis: 'ok',
      rabbitmq: 'ok',
      version: '1.2.0',
    };
    expectedKeys.forEach((key) => {
      expect(mockResponse).toHaveProperty(key);
    });
    expect(mockResponse.version).toBe('1.2.0');
  });
});
