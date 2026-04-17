/**
 * PlatformConfigService — configuration par plateforme.
 * Upsert : créer ou mettre à jour la config d'une plateforme.
 * CDC Media v1.4 §7.4 — module configuration plateforme.
 */
import { Injectable, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { PlatformMediaConfig } from './entities/platform-media-config.entity';

@Injectable()
export class PlatformConfigService {
  private readonly logger = new Logger(PlatformConfigService.name);

  constructor(
    @InjectRepository(PlatformMediaConfig)
    private configRepo: Repository<PlatformMediaConfig>,
  ) {}

  async getConfig(platformId: string): Promise<PlatformMediaConfig | null> {
    return this.configRepo.findOne({ where: { platform_id: platformId } });
  }

  /** Upsert — crée ou met à jour la configuration */
  async upsertConfig(
    platformId: string,
    dto: Partial<PlatformMediaConfig>,
  ): Promise<PlatformMediaConfig | null> {
    const existing = await this.configRepo.findOne({ where: { platform_id: platformId } });

    if (existing) {
      await this.configRepo.update({ platform_id: platformId }, dto);
      this.logger.log(`Config mise à jour pour platform ${platformId}`);
    } else {
      await this.configRepo.save({ platform_id: platformId, ...dto });
      this.logger.log(`Config créée pour platform ${platformId}`);
    }

    return this.configRepo.findOne({ where: { platform_id: platformId } });
  }
}
