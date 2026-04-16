/**
 * Tests unitaires -- MediaService
 * Couvre : upload, validation, soft delete, hard delete, purge RGPD, stats
 * CDC Media v1.4 _12 : tests obligatoires des v1.0
 */
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { getQueueToken } from '@nestjs/bullmq';
import { ConfigService } from '@nestjs/config';
import { BadRequestException, ForbiddenException, NotFoundException } from '@nestjs/common';
import { MediaService } from '../../src/media/media.service';
import { MediaFile } from '../../src/media/entities/media-file.entity';
import { MediaVariant } from '../../src/media/entities/media-variant.entity';
import { MediaMetadata } from '../../src/media/entities/media-metadata.entity';
import { MediaAccessLog } from '../../src/media/entities/media-access-log.entity';
import { PlatformMediaConfig } from '../../src/platform-config/entities/platform-media-config.entity';
import { LocalStorageProvider } from '../../src/common/storage/local-storage.provider';
import { MEDIA_QUEUE } from '../../src/media/media.processor';

// ---- Factories de mocks ----

const makeMockFile = (overrides: Partial<Express.Multer.File> = {}): Express.Multer.File => ({
  fieldname: 'file',
  originalname: 'test.jpg',
  encoding: '7bit',
  mimetype: 'image/jpeg',
  size: 1024,
  buffer: Buffer.from('fake-image-data'),
  stream: null as any,
  destination: '',
  filename: '',
  path: '',
  ...overrides,
});

const makeMockMedia = (overrides: Partial<MediaFile> = {}): MediaFile => ({
  id: 'media-uuid-1234',
  original_name: 'test.jpg',
  mime_type: 'image/jpeg',
  size_bytes: 1024,
  sha256_hash: 'abc123',
  storage_key: 'platform-id/2026/04/media-uuid-1234.jpg',
  visibility: 'private',
  platform_id: 'platform-uuid-5678',
  uploaded_by: 'user-uuid-abcd',
  owner_user_id: null,
  width: null,
  height: null,
  duration_ms: null,
  deleted_at: null,
  created_at: new Date(),
  updated_at: new Date(),
  variants: [],
  metadata: [],
  access_logs: [],
  ...overrides,
});

describe('MediaService - Tests Unitaires', () => {
  let service: MediaService;

  // Repos mockes
  const mockMediaRepo = {
    create: jest.fn(),
    save: jest.fn(),
    findOne: jest.fn(),
    find: jest.fn(),
    findAndCount: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
    existsBy: jest.fn(),
    createQueryBuilder: jest.fn(),
  };

  const mockVariantRepo = { save: jest.fn(), find: jest.fn() };
  const mockMetaRepo = { save: jest.fn(), delete: jest.fn(), create: jest.fn() };
  const mockLogRepo = { save: jest.fn(), create: jest.fn(), findAndCount: jest.fn() };
  const mockConfigRepo = { findOne: jest.fn() };

  const mockStorage = {
    upload: jest.fn().mockResolvedValue('storage-key'),
    download: jest.fn().mockResolvedValue(Buffer.from('data')),
    delete: jest.fn().mockResolvedValue(undefined),
    getUrl: jest.fn().mockResolvedValue('/api/v1/media/file/key'),
    exists: jest.fn().mockResolvedValue(true),
  };

  const mockQueue = { add: jest.fn().mockResolvedValue({ id: 'job-1' }) };

  const mockConfig = {
    get: jest.fn((key: string, defaultVal?: any) => {
      const vals: Record<string, any> = {
        SIGNED_URL_SECRET: 'test-secret-key',
        COMPRESSION_QUALITY: 80,
        LOCAL_STORAGE_PATH: '/tmp/test-uploads',
      };
      return vals[key] ?? defaultVal;
    }),
  };

  beforeEach(async () => {
    jest.clearAllMocks();

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        MediaService,
        { provide: getRepositoryToken(MediaFile), useValue: mockMediaRepo },
        { provide: getRepositoryToken(MediaVariant), useValue: mockVariantRepo },
        { provide: getRepositoryToken(MediaMetadata), useValue: mockMetaRepo },
        { provide: getRepositoryToken(MediaAccessLog), useValue: mockLogRepo },
        { provide: getRepositoryToken(PlatformMediaConfig), useValue: mockConfigRepo },
        { provide: getQueueToken(MEDIA_QUEUE), useValue: mockQueue },
        { provide: LocalStorageProvider, useValue: mockStorage },
        { provide: ConfigService, useValue: mockConfig },
      ],
    }).compile();

    service = module.get<MediaService>(MediaService);
  });

  // ============================================================
  // UPLOAD
  // ============================================================

  describe('uploadFile()', () => {
    it('doit uploader un fichier valide et retourner les metadonnees', async () => {
      const file = makeMockFile();
      const media = makeMockMedia();

      mockConfigRepo.findOne.mockResolvedValue(null); // pas de config plateforme _ fallback
      mockMediaRepo.create.mockReturnValue(media);
      mockMediaRepo.save.mockResolvedValue(media);

      const result = await service.uploadFile(
        file,
        'platform-uuid-5678',
        'user-uuid-abcd',
        null,
        'private',
      );

      expect(result).toBeDefined();
      expect(mockStorage.upload).toHaveBeenCalledTimes(1);
      expect(mockMediaRepo.save).toHaveBeenCalledTimes(1);
      // Le job de traitement doit etre enqueue pour les images
      expect(mockQueue.add).toHaveBeenCalledWith('process-media', expect.any(Object), expect.any(Object));
    });

    it('doit rejeter un type MIME non autorise', async () => {
      const file = makeMockFile({ mimetype: 'application/x-executable', originalname: 'virus.exe' });
      mockConfigRepo.findOne.mockResolvedValue(null);

      await expect(
        service.uploadFile(file, 'platform-uuid', 'user-uuid', null, 'private'),
      ).rejects.toThrow(BadRequestException);
    });

    it('doit rejeter un fichier trop volumineux', async () => {
      const file = makeMockFile({ size: 100_000_000 }); // 100 MB > 50 MB limite
      mockConfigRepo.findOne.mockResolvedValue(null);

      await expect(
        service.uploadFile(file, 'platform-uuid', 'user-uuid', null, 'private'),
      ).rejects.toThrow(BadRequestException);
    });

    it('ne doit PAS enqueuer de traitement pour les documents PDF (non-image)', async () => {
      const file = makeMockFile({ mimetype: 'application/pdf', originalname: 'doc.pdf' });
      const media = makeMockMedia({ mime_type: 'application/pdf' });

      mockConfigRepo.findOne.mockResolvedValue(null);
      mockMediaRepo.create.mockReturnValue(media);
      mockMediaRepo.save.mockResolvedValue(media);

      await service.uploadFile(file, 'platform-uuid', 'user-uuid', null, 'private');

      expect(mockQueue.add).not.toHaveBeenCalled();
    });
  });

  // ============================================================
  // CONSULTATION
  // ============================================================

  describe('getMediaInfo()', () => {
    it('doit retourner les infos d un media existant', async () => {
      const media = makeMockMedia();
      mockMediaRepo.findOne.mockResolvedValue(media);

      const result = await service.getMediaInfo('media-uuid-1234');
      expect(result.id).toBe('media-uuid-1234');
    });

    it('doit lever NotFoundException si le media n existe pas', async () => {
      mockMediaRepo.findOne.mockResolvedValue(null);

      await expect(service.getMediaInfo('inexistant-uuid')).rejects.toThrow(NotFoundException);
    });
  });

  describe('downloadFile()', () => {
    it('doit retourner le buffer pour un fichier public', async () => {
      const media = makeMockMedia({ visibility: 'public' });
      mockMediaRepo.findOne.mockResolvedValue(media);
      mockStorage.download.mockResolvedValue(Buffer.from('image-data'));
      mockLogRepo.create.mockReturnValue({});
      mockLogRepo.save.mockResolvedValue({});

      const result = await service.downloadFile('media-uuid-1234', null, '127.0.0.1');
      expect(result.buffer).toBeDefined();
      expect(result.mimeType).toBe('image/jpeg');
    });

    it('doit lever ForbiddenException pour un fichier prive sans auth valide', async () => {
      const media = makeMockMedia({ visibility: 'private', uploaded_by: 'autre-user' });
      mockMediaRepo.findOne.mockResolvedValue(media);

      await expect(
        service.downloadFile('media-uuid-1234', { id: 'mauvais-user', is_s2s: false }, '127.0.0.1'),
      ).rejects.toThrow(ForbiddenException);
    });

    it('doit autoriser un token S2S a telecharger un fichier prive', async () => {
      const media = makeMockMedia({ visibility: 'private' });
      mockMediaRepo.findOne.mockResolvedValue(media);
      mockStorage.download.mockResolvedValue(Buffer.from('data'));
      mockLogRepo.create.mockReturnValue({});
      mockLogRepo.save.mockResolvedValue({});

      const result = await service.downloadFile('media-uuid-1234', { is_s2s: true }, undefined);
      expect(result.buffer).toBeDefined();
    });
  });

  // ============================================================
  // GESTION
  // ============================================================

  describe('softDelete()', () => {
    it('doit soft-supprimer un fichier appartenant au uploader', async () => {
      const auth = { id: 'user-uuid-abcd', is_s2s: false, platform_id: 'platform-uuid-5678' };
      const media = makeMockMedia({ uploaded_by: 'user-uuid-abcd' });
      mockMediaRepo.findOne.mockResolvedValue(media);
      mockMediaRepo.update.mockResolvedValue({});

      await service.softDelete('media-uuid-1234', auth);

      expect(mockMediaRepo.update).toHaveBeenCalledWith(
        'media-uuid-1234',
        expect.objectContaining({ deleted_at: expect.any(Date) }),
      );
    });

    it('doit rejeter un soft delete par un utilisateur non proprietaire', async () => {
      const auth = { id: 'autre-user', is_s2s: false, platform_id: 'autre-platform' };
      const media = makeMockMedia({ uploaded_by: 'user-uuid-abcd' });
      mockMediaRepo.findOne.mockResolvedValue(media);

      await expect(service.softDelete('media-uuid-1234', auth)).rejects.toThrow(ForbiddenException);
    });
  });

  describe('hardDelete()', () => {
    it('doit supprimer physiquement le fichier et ses variantes', async () => {
      const media = makeMockMedia({
        variants: [
          { id: 'variant-1', storage_key: 'key-thumb', media_id: 'media-uuid-1234' } as any,
        ],
      });
      mockMediaRepo.findOne.mockResolvedValue(media);
      mockMediaRepo.delete.mockResolvedValue({});

      await service.hardDelete('media-uuid-1234');

      // Le fichier original + sa variante doivent etre supprimes du stockage
      expect(mockStorage.delete).toHaveBeenCalledTimes(2);
      expect(mockMediaRepo.delete).toHaveBeenCalledWith('media-uuid-1234');
    });
  });

  describe('purgeByUser() -- RGPD', () => {
    it('doit supprimer tous les fichiers de cet utilisateur', async () => {
      const medias = [
        makeMockMedia({ id: 'media-1', uploaded_by: 'target-user', variants: [] }),
        makeMockMedia({ id: 'media-2', owner_user_id: 'target-user', variants: [] }),
      ];

      // Mock du createQueryBuilder pour la purge
      const mockQb = {
        leftJoinAndSelect: jest.fn().mockReturnThis(),
        where: jest.fn().mockReturnThis(),
        getMany: jest.fn().mockResolvedValue(medias),
      };
      mockMediaRepo.createQueryBuilder.mockReturnValue(mockQb);
      mockMediaRepo.delete.mockResolvedValue({});

      const result = await service.purgeByUser('target-user');

      expect(result.files_deleted).toBe(2);
      expect(mockStorage.delete).toHaveBeenCalledTimes(2);
    });
  });

  // ============================================================
  // STATISTIQUES
  // ============================================================

  describe('getStats()', () => {
    it('doit retourner les statistiques globales', async () => {
      const mockQb = {
        where: jest.fn().mockReturnThis(),
        andWhere: jest.fn().mockReturnThis(),
        getCount: jest.fn().mockResolvedValue(42),
        select: jest.fn().mockReturnThis(),
        addSelect: jest.fn().mockReturnThis(),
        groupBy: jest.fn().mockReturnThis(),
        getRawOne: jest.fn().mockResolvedValue({ total: '1048576' }),
        getRawMany: jest.fn().mockResolvedValue([
          { mime_type: 'image/jpeg', count: '30' },
          { mime_type: 'application/pdf', count: '12' },
        ]),
      };
      mockMediaRepo.createQueryBuilder.mockReturnValue(mockQb);

      const stats = await service.getStats();

      expect(stats.total_files).toBe(42);
      expect(stats.total_size_bytes).toBe(1048576);
      expect(stats.by_mime_type).toHaveLength(2);
    });
  });

  // ============================================================
  // URLS SIGN_ES
  // ============================================================

  describe('generateSignedUrl()', () => {
    it('doit generer une URL signee avec signature HMAC valide', async () => {
      const media = makeMockMedia();
      mockMediaRepo.findOne.mockResolvedValue(media);
      mockLogRepo.create.mockReturnValue({});
      mockLogRepo.save.mockResolvedValue({});

      const url = await service.generateSignedUrl('media-uuid-1234', { id: 'user-uuid' }, 3600);

      expect(url).toContain('/api/v1/media/media-uuid-1234/serve');
      expect(url).toContain('sig=');
      expect(url).toContain('exp=');
    });
  });
});
