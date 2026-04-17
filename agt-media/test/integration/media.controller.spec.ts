/**
 * Tests d'integration -- MediaController
 * Teste les endpoints principaux via supertest.
 * CDC Media v1.4 _12.2 : tests d'integration obligatoires.
 *
 * NOTE : ces tests mockent JwtAuthGuard pour se concentrer sur la logique
 * du controller et du service, sans dependance vers Auth en live.
 */
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { getRepositoryToken } from '@nestjs/typeorm';
import { getQueueToken } from '@nestjs/bullmq';
import { ConfigService } from '@nestjs/config';
import { Reflector } from '@nestjs/core';
import { MediaController } from '../../src/media/media.controller';
import { MediaService } from '../../src/media/media.service';
import { JwtAuthGuard } from '../../src/common/auth/jwt-auth.guard';
import { S2SGuard } from '../../src/common/auth/s2s.guard';
import { MediaFile } from '../../src/media/entities/media-file.entity';
import { MediaVariant } from '../../src/media/entities/media-variant.entity';
import { MediaMetadata } from '../../src/media/entities/media-metadata.entity';
import { MediaAccessLog } from '../../src/media/entities/media-access-log.entity';
import { PlatformMediaConfig } from '../../src/platform-config/entities/platform-media-config.entity';
import { LocalStorageProvider } from '../../src/common/storage/local-storage.provider';
import { MEDIA_QUEUE } from '../../src/media/media.processor';

// Mock du guard JWT -- simule un utilisateur authentifie dans tous les tests
class MockJwtAuthGuard {
  canActivate(context: any) {
    const req = context.switchToHttp().getRequest();
    req.auth = {
      id: 'test-user-uuid',
      sub: 'test-user-uuid',
      platform_id: 'test-platform-uuid',
      is_s2s: false,
    };
    return true;
  }
}

// Mock du guard S2S -- simule un token S2S
class MockS2SGuard {
  canActivate(context: any) {
    const req = context.switchToHttp().getRequest();
    return req.auth?.is_s2s === true;
  }
}

describe('MediaController - Tests Integration', () => {
  let app: INestApplication;

  const mockMedia: Partial<MediaFile> = {
    id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    original_name: 'test.jpg',
    mime_type: 'image/jpeg',
    size_bytes: 2048,
    sha256_hash: 'abc123hash',
    storage_key: 'platform/2026/04/test-media-uuid.jpg',
    visibility: 'public',
    platform_id: 'test-platform-uuid',
    uploaded_by: 'test-user-uuid',
    owner_user_id: null,
    deleted_at: null,
    created_at: new Date('2026-04-14T10:00:00Z'),
    updated_at: new Date('2026-04-14T10:00:00Z'),
    variants: [],
    metadata: [],
  };

  const mockMediaService = {
    uploadFile: jest.fn().mockResolvedValue(mockMedia),
    uploadFromUrl: jest.fn().mockResolvedValue(mockMedia),
    getMediaInfo: jest.fn().mockResolvedValue(mockMedia),
    downloadFile: jest.fn().mockResolvedValue({
      buffer: Buffer.from('fake-image'),
      mimeType: 'image/jpeg',
      filename: 'test.jpg',
    }),
    listMedia: jest.fn().mockResolvedValue({
      data: [mockMedia],
      total: 1,
      page: 1,
      limit: 20,
    }),
    getVariants: jest.fn().mockResolvedValue([]),
    generateSignedUrl: jest.fn().mockResolvedValue('/api/v1/media/test-uuid/serve?sig=abc&exp=9999999999'),
    getAccessLogs: jest.fn().mockResolvedValue({ data: [], total: 0, page: 1, limit: 50 }),
    updateMetadata: jest.fn().mockResolvedValue(mockMedia),
    updateVisibility: jest.fn().mockResolvedValue(mockMedia),
    softDelete: jest.fn().mockResolvedValue(undefined),
    hardDelete: jest.fn().mockResolvedValue(undefined),
    purgeByUser: jest.fn().mockResolvedValue({ deleted_count: 3 }),
    getStats: jest.fn().mockResolvedValue({ total_files: 42, total_size_bytes: 1048576 }),
  };

  const mockConfig = {
    get: jest.fn((key: string, def?: any) => {
      const vals: Record<string, any> = { SIGNED_URL_SECRET: 'test-secret' };
      return vals[key] ?? def;
    }),
  };

  beforeAll(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [MediaController],
      providers: [
        { provide: MediaService, useValue: mockMediaService },
        { provide: ConfigService, useValue: mockConfig },
        Reflector,
      ],
    })
      .overrideGuard(JwtAuthGuard)
      .useClass(MockJwtAuthGuard)
      .overrideGuard(S2SGuard)
      .useClass(MockS2SGuard)
      .compile();

    app = module.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
    app.setGlobalPrefix('api/v1');
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  beforeEach(() => {
    jest.clearAllMocks();
  });

  // ---- Health (via controller) ----

  describe('GET /api/v1/media (liste)', () => {
    it('doit retourner la liste paginee des medias', async () => {
      mockMediaService.listMedia.mockResolvedValue({
        data: [mockMedia],
        total: 1,
        page: 1,
        limit: 20,
      });

      const res = await request(app.getHttpServer())
        .get('/api/v1/media')
        .set('Authorization', 'Bearer test-token')
        .expect(200);

      expect(res.body.data).toHaveLength(1);
      expect(res.body.total).toBe(1);
    });
  });

  describe('GET /api/v1/media/:id/info', () => {
    it('doit retourner les metadonnees completes', async () => {
      mockMediaService.getMediaInfo.mockResolvedValue(mockMedia);

      const res = await request(app.getHttpServer())
        .get('/api/v1/media/a1b2c3d4-e5f6-7890-abcd-ef1234567890/info')
        .set('Authorization', 'Bearer test-token')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.id).toBe('a1b2c3d4-e5f6-7890-abcd-ef1234567890');
    });
  });

  describe('GET /api/v1/media/:id/thumbnails', () => {
    it('doit retourner la liste des thumbnails', async () => {
      mockMediaService.getVariants.mockResolvedValue([
        { id: 'v1', variant_type: 'thumbnail', width: 150, height: 150 },
        { id: 'v2', variant_type: 'thumbnail', width: 300, height: 300 },
        { id: 'v3', variant_type: 'compressed', width: null, height: null },
      ]);

      const res = await request(app.getHttpServer())
        .get('/api/v1/media/a1b2c3d4-e5f6-7890-abcd-ef1234567890/thumbnails')
        .set('Authorization', 'Bearer test-token')
        .expect(200);

      // Seuls les thumbnails doivent etre retournes (pas les compressed)
      expect(res.body.data).toHaveLength(2);
      expect(res.body.data[0].variant_type).toBe('thumbnail');
    });
  });

  describe('GET /api/v1/media/:id/signed-url', () => {
    it('doit retourner une URL signee', async () => {
      const res = await request(app.getHttpServer())
        .get('/api/v1/media/a1b2c3d4-e5f6-7890-abcd-ef1234567890/signed-url')
        .set('Authorization', 'Bearer test-token')
        .expect(200);

      expect(res.body.success).toBe(true);
      expect(res.body.data.signed_url).toContain('/serve');
    });
  });

  describe('PUT /api/v1/media/:id/visibility', () => {
    it('doit mettre a jour la visibilite', async () => {
      mockMediaService.updateVisibility.mockResolvedValue({ ...mockMedia, visibility: 'public' });

      const res = await request(app.getHttpServer())
        .put('/api/v1/media/a1b2c3d4-e5f6-7890-abcd-ef1234567890/visibility')
        .set('Authorization', 'Bearer test-token')
        .send({ visibility: 'public' })
        .expect(200);

      expect(res.body.success).toBe(true);
    });

    it('doit rejeter une visibilite invalide', async () => {
      await request(app.getHttpServer())
        .put('/api/v1/media/a1b2c3d4-e5f6-7890-abcd-ef1234567890/visibility')
        .set('Authorization', 'Bearer test-token')
        .send({ visibility: 'invalid-value' })
        .expect(400);
    });
  });

  describe('DELETE /api/v1/media/:id', () => {
    it('doit soft-supprimer un fichier (204)', async () => {
      await request(app.getHttpServer())
        .delete('/api/v1/media/a1b2c3d4-e5f6-7890-abcd-ef1234567890')
        .set('Authorization', 'Bearer test-token')
        .expect(204);

      expect(mockMediaService.softDelete).toHaveBeenCalledWith('a1b2c3d4-e5f6-7890-abcd-ef1234567890', expect.any(Object));
    });
  });

  describe('GET /api/v1/media/stats', () => {
    it('doit retourner les statistiques', async () => {
      const res = await request(app.getHttpServer())
        .get('/api/v1/media/stats')
        .set('Authorization', 'Bearer test-token')
        .expect(200);

      expect(res.body.total_files).toBe(42);
    });
  });

  describe('POST /api/v1/media/from-url', () => {
    it('doit importer un fichier depuis une URL valide', async () => {
      mockMediaService.uploadFromUrl.mockResolvedValue(mockMedia);

      const res = await request(app.getHttpServer())
        .post('/api/v1/media/from-url')
        .set('Authorization', 'Bearer test-token')
        .send({ url: 'https://example.com/image.jpg', visibility: 'public' })
        .expect(201);

      expect(res.body.success).toBe(true);
    });
  });
});
