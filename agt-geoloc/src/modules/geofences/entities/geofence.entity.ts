import {
  Entity, PrimaryGeneratedColumn, Column, CreateDateColumn,
  UpdateDateColumn, Unique,
} from 'typeorm';

/**
 * Zone géographique (geofence).
 * Peut être un polygone ou un cercle.
 * La vérification d'entrée/sortie est event-driven (à chaque update de position),
 * pas en polling.
 */
@Entity('geofences')
@Unique(['platform_id', 'name'])
export class Geofence {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'uuid' })
  platform_id: string;

  @Column({ type: 'varchar', length: 100 })
  name: string;

  /** polygon | circle */
  @Column({ type: 'varchar', length: 10 })
  fence_type: 'polygon' | 'circle';

  /**
   * Pour les polygones : tableau de [lng, lat] fermé.
   * Stocké en JSONB pour simplifier la compatibilité TypeORM/PostGIS.
   * La vérification spatiale en mémoire utilise turf.js (R-tree via rbush).
   */
  @Column({ type: 'jsonb', nullable: true })
  coordinates: number[][];

  /** Centre pour les cercles */
  @Column({ type: 'decimal', precision: 10, scale: 7, nullable: true })
  center_latitude: number;

  @Column({ type: 'decimal', precision: 10, scale: 7, nullable: true })
  center_longitude: number;

  /** Rayon en mètres (pour les cercles) */
  @Column({ type: 'float', nullable: true })
  radius_meters: number;

  @Column({ type: 'jsonb', default: [] })
  tags: string[];

  @Column({ type: 'jsonb', nullable: true })
  metadata: Record<string, any>;

  @Column({ type: 'boolean', default: true })
  is_active: boolean;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamptz' })
  updated_at: Date;
}
