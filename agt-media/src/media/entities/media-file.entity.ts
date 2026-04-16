/**
 * Entité media_files — table principale des fichiers uploadés.
 * CDC Media v1.4 §6.1 — modèle de données.
 */
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
  Index,
} from 'typeorm';
import { MediaVariant } from './media-variant.entity';
import { MediaMetadata } from './media-metadata.entity';
import { MediaAccessLog } from './media-access-log.entity';

@Entity('media_files')
@Index(['platform_id'])
@Index(['uploaded_by'])
@Index(['owner_user_id'])
@Index(['deleted_at'])
export class MediaFile {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ length: 255 })
  original_name: string;

  @Column({ length: 100 })
  mime_type: string;

  @Column({ type: 'bigint' })
  size_bytes: number;

  @Column({ length: 64 })
  sha256_hash: string;

  @Column({ length: 500 })
  storage_key: string;

  /** public | private */
  @Column({ length: 20, default: 'private' })
  visibility: string;

  /** FK logique → Auth platforms.id */
  @Column({ type: 'uuid' })
  platform_id: string;

  /** Auth users_auth.id — acteur qui a fait l'upload. NULL si S2S */
  @Column({ type: 'uuid', nullable: true })
  uploaded_by: string | null;

  /** Propriétaire métier du fichier. Utile quand un service uploade pour un user */
  @Column({ type: 'uuid', nullable: true })
  owner_user_id: string | null;

  /** Dimensions (images/vidéos) */
  @Column({ type: 'integer', nullable: true })
  width: number | null;

  @Column({ type: 'integer', nullable: true })
  height: number | null;

  /** Durée en ms (vidéo/audio) */
  @Column({ type: 'integer', nullable: true })
  duration_ms: number | null;

  /** Soft delete — null = actif */
  @Column({ type: 'timestamptz', nullable: true })
  deleted_at: Date | null;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamptz' })
  updated_at: Date;

  @OneToMany(() => MediaVariant, (v) => v.media_file, { cascade: true })
  variants: MediaVariant[];

  @OneToMany(() => MediaMetadata, (m) => m.media_file, { cascade: true })
  metadata: MediaMetadata[];

  @OneToMany(() => MediaAccessLog, (l) => l.media_file)
  access_logs: MediaAccessLog[];
}
