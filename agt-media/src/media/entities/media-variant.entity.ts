/**
 * Entité media_variants — thumbnails, versions compressées, resizées.
 * CDC Media v1.4 §6.2
 */
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  ManyToOne,
  JoinColumn,
  Index,
} from 'typeorm';
import { MediaFile } from './media-file.entity';

@Entity('media_variants')
@Index(['media_id'])
export class MediaVariant {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'uuid' })
  media_id: string;

  /** thumbnail | compressed | resized */
  @Column({ length: 20 })
  variant_type: string;

  @Column({ type: 'integer', nullable: true })
  width: number | null;

  @Column({ type: 'integer', nullable: true })
  height: number | null;

  @Column({ length: 500 })
  storage_key: string;

  @Column({ type: 'bigint' })
  size_bytes: number;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;

  @ManyToOne(() => MediaFile, (f) => f.variants, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'media_id' })
  media_file: MediaFile;
}
