/**
 * Entité media_metadata — clé-valeur libres par plateforme.
 * CDC Media v1.4 §6.3
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

@Entity('media_metadata')
@Index(['media_id'])
export class MediaMetadata {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'uuid' })
  media_id: string;

  @Column({ length: 100 })
  key: string;

  @Column({ type: 'text' })
  value: string;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;

  @ManyToOne(() => MediaFile, (f) => f.metadata, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'media_id' })
  media_file: MediaFile;
}
