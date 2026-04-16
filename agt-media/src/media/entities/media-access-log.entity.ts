/**
 * Entité media_access_logs — log de chaque accès/téléchargement.
 * CDC Media v1.4 §6.5 : chaque download et URL signée sont loggés.
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

@Entity('media_access_logs')
@Index(['media_id'])
@Index(['accessed_by'])
export class MediaAccessLog {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'uuid' })
  media_id: string;

  @Column({ type: 'uuid', nullable: true })
  accessed_by: string | null;

  @Column({ type: 'varchar', length: 45, nullable: true })
  ip_address: string | null;

  /** download | signed_url | view */
  @Column({ length: 50 })
  action: string;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;

  @ManyToOne(() => MediaFile, (f) => f.access_logs, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'media_id' })
  media_file: MediaFile;
}
