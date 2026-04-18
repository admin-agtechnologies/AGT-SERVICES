import {
  Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, Index,
} from 'typeorm';

/**
 * Trajet d'une entité trackée.
 *
 * Machine à états : active → completed | cancelled
 * États terminaux : completed, cancelled (aucune transition sortante)
 *
 * Un seul trajet active par (platform_id, entity_id) à tout moment.
 */
@Entity('trips')
export class Trip {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'uuid' })
  @Index()
  entity_id: string;

  @Column({ type: 'uuid' })
  platform_id: string;

  /** active | completed | cancelled */
  @Column({ type: 'varchar', length: 20, default: 'active' })
  status: 'active' | 'completed' | 'cancelled';

  @Column({ type: 'decimal', precision: 10, scale: 7 })
  start_latitude: number;

  @Column({ type: 'decimal', precision: 10, scale: 7 })
  start_longitude: number;

  @Column({ type: 'decimal', precision: 10, scale: 7, nullable: true })
  end_latitude: number;

  @Column({ type: 'decimal', precision: 10, scale: 7, nullable: true })
  end_longitude: number;

  @Column({ type: 'varchar', length: 255, nullable: true })
  start_address: string;

  @Column({ type: 'varchar', length: 255, nullable: true })
  end_address: string;

  @Column({ type: 'float', default: 0 })
  distance_meters: number;

  @Column({ type: 'int', default: 0 })
  duration_seconds: number;

  /** Données métier opaques — le service Geoloc ne les interprète pas */
  @Column({ type: 'jsonb', nullable: true })
  metadata: Record<string, any>;

  @Column({ type: 'timestamptz' })
  started_at: Date;

  @Column({ type: 'timestamptz', nullable: true })
  ended_at: Date;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;
}
