/**
 * Entité platform_media_configs — configuration par plateforme.
 * CDC Media v1.4 §6.4 : types autorisés, tailles max, thumbnails, quota.
 * Upsert uniquement (pas de create/delete séparés).
 */
import {
  Entity,
  PrimaryColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('platform_media_configs')
export class PlatformMediaConfig {
  /** FK logique → Auth platforms.id */
  @PrimaryColumn({ type: 'uuid' })
  platform_id: string;

  /** Types MIME autorisés. Ex: ["image/jpeg","image/png","application/pdf"] */
  @Column({ type: 'jsonb', default: [] })
  allowed_types: string[];

  /** Taille max en octets par catégorie. Ex: {"image":10485760,"document":52428800} */
  @Column({ type: 'jsonb', default: {} })
  max_size_bytes: Record<string, number>;

  /** Tailles de thumbnails. Ex: ["150x150","300x300"] */
  @Column({ type: 'jsonb', default: ['150x150', '300x300'] })
  thumbnail_sizes: string[];

  /** Qualité compression 1-100. NULL = valeur par défaut du service */
  @Column({ type: 'integer', nullable: true })
  compression_quality: number | null;

  /** Quota total de stockage en octets. NULL = illimité */
  @Column({ type: 'bigint', nullable: true })
  storage_quota_bytes: number | null;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamptz' })
  updated_at: Date;
}
