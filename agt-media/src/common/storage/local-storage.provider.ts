/**
 * Provider de stockage abstrait.
 *
 * Pourquoi : le CDC prévoit une migration future vers S3/GCS.
 * En abstrayant le stockage derrière une interface, on peut changer
 * de provider sans toucher au code métier.
 * CDC Media v1.4 §5.3 : interface StorageProvider.
 */
import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as fs from 'fs';
import * as path from 'path';

export interface StorageProvider {
  upload(buffer: Buffer, key: string, mimetype?: string): Promise<string>;
  download(key: string): Promise<Buffer>;
  delete(key: string): Promise<void>;
  getUrl(key: string, expiresIn?: number): Promise<string>;
  exists(key: string): Promise<boolean>;
  getAbsolutePath?(key: string): string;
}

/**
 * Stockage local — MVP uniquement.
 * Organisation : /{platformId}/{année}/{mois}/{fileUUID}/
 */
@Injectable()
export class LocalStorageProvider implements StorageProvider {
  private readonly logger = new Logger(LocalStorageProvider.name);
  private readonly basePath: string;

  constructor(private config: ConfigService) {
    this.basePath = config.get<string>('LOCAL_STORAGE_PATH', '/app/uploads');
    this.ensureBaseDir();
  }

  private ensureBaseDir(): void {
    if (!fs.existsSync(this.basePath)) {
      fs.mkdirSync(this.basePath, { recursive: true });
      this.logger.log(`Répertoire de stockage créé: ${this.basePath}`);
    }
  }

  async upload(buffer: Buffer, key: string): Promise<string> {
    const fullPath = path.join(this.basePath, key);
    const dir = path.dirname(fullPath);

    // Créer les dossiers intermédiaires si nécessaires
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    fs.writeFileSync(fullPath, buffer);
    return key;
  }

  async download(key: string): Promise<Buffer> {
    const fullPath = path.join(this.basePath, key);
    if (!fs.existsSync(fullPath)) {
      throw new Error(`Fichier introuvable: ${key}`);
    }
    return fs.readFileSync(fullPath);
  }

  async delete(key: string): Promise<void> {
    const fullPath = path.join(this.basePath, key);
    if (fs.existsSync(fullPath)) {
      fs.unlinkSync(fullPath);
    }
  }

  async getUrl(key: string): Promise<string> {
    // En local, on retourne un chemin API servant le fichier
    return `/api/v1/media/file/${encodeURIComponent(key)}`;
  }

  async exists(key: string): Promise<boolean> {
    return fs.existsSync(path.join(this.basePath, key));
  }

  getAbsolutePath(key: string): string {
    return path.join(this.basePath, key);
  }
}
