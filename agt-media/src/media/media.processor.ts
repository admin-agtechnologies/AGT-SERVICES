/**
 * Processeur de traitement des medias -- Worker BullMQ.
 * Le traitement (compression, thumbnails) est execute de facon asynchrone.
 * CDC Media v1.4 : flux BullMQ obligatoire.
 */
import { Processor, WorkerHost } from '@nestjs/bullmq';
import { Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Job } from 'bullmq';
import { MediaFile } from './entities/media-file.entity';
import { MediaVariant } from './entities/media-variant.entity';
import { LocalStorageProvider } from '../common/storage/local-storage.provider';

export const MEDIA_QUEUE = 'media-processing';

export interface ProcessMediaJob {
  mediaId: string;
  storageKey: string;
  mimeType: string;
  platformId: string;
  thumbnailSizes: string[];
  compressionQuality: number;
}

@Processor(MEDIA_QUEUE)
export class MediaProcessor extends WorkerHost {
  private readonly logger = new Logger(MediaProcessor.name);

  constructor(
    @InjectRepository(MediaFile)
    private mediaRepo: Repository<MediaFile>,
    @InjectRepository(MediaVariant)
    private variantRepo: Repository<MediaVariant>,
    private storage: LocalStorageProvider,
  ) {
    super();
  }

  async process(job: Job<ProcessMediaJob>): Promise<void> {
    const { mediaId, storageKey, mimeType, thumbnailSizes, compressionQuality } = job.data;
    this.logger.log(`Traitement du media ${mediaId} (type: ${mimeType})`);

    if (!mimeType.startsWith('image/')) {
      this.logger.log(`Media ${mediaId} non-image, pas de traitement`);
      return;
    }

    try {
      // Import sharp dynamically to avoid issues if not installed
      const sharp = require('sharp');
      const buffer = await this.storage.download(storageKey);
      const image = sharp(buffer);
      const metadata = await image.metadata();

      await this.mediaRepo.update(mediaId, {
        width: metadata.width || null,
        height: metadata.height || null,
      });

      for (const sizeStr of thumbnailSizes) {
        await this.generateThumbnail(mediaId, storageKey, buffer, sizeStr, sharp);
      }

      await this.generateCompressed(mediaId, storageKey, buffer, compressionQuality, sharp);

      this.logger.log(`Media ${mediaId} traite avec succes`);
    } catch (err) {
      this.logger.error(`Erreur traitement media ${mediaId}: ${err.message}`);
      throw err;
    }
  }

  private async generateThumbnail(
    mediaId: string,
    originalKey: string,
    buffer: Buffer,
    sizeStr: string,
    sharp: any,
  ): Promise<void> {
    const [w, h] = sizeStr.split('x').map(Number);
    const thumbKey = originalKey.replace(/(\.\w+)$/, `_thumb_${w}x${h}$1`);

    const thumbBuffer = await sharp(buffer)
      .resize(w, h, { fit: 'cover', position: 'centre' })
      .jpeg({ quality: 80 })
      .toBuffer();

    await this.storage.upload(thumbBuffer, thumbKey);

    await this.variantRepo.save({
      media_id: mediaId,
      variant_type: 'thumbnail',
      width: w,
      height: h,
      storage_key: thumbKey,
      size_bytes: thumbBuffer.length,
    });
  }

  private async generateCompressed(
    mediaId: string,
    originalKey: string,
    buffer: Buffer,
    quality: number,
    sharp: any,
  ): Promise<void> {
    const compressedKey = originalKey.replace(/(\.\w+)$/, '_compressed$1');
    const compressedBuffer = await sharp(buffer).jpeg({ quality: quality || 80 }).toBuffer();

    if (compressedBuffer.length < buffer.length * 0.9) {
      await this.storage.upload(compressedBuffer, compressedKey);
      await this.variantRepo.save({
        media_id: mediaId,
        variant_type: 'compressed',
        width: null,
        height: null,
        storage_key: compressedKey,
        size_bytes: compressedBuffer.length,
      });
    }
  }
}
