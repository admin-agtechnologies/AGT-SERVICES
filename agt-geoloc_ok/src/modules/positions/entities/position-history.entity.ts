import {
  Entity, PrimaryGeneratedColumn, Column, CreateDateColumn,
  ManyToOne, JoinColumn, Index,
} from 'typeorm';
import { TrackedEntity } from './tracked-entity.entity';

/**
 * Historique des positions GPS persisté en PostGIS.
 * Partitionnée par mois sur recorded_at (géré via migration SQL).
 * Index GiST sur la colonne location pour les requêtes spatiales.
 */
@Entity('position_history')
export class PositionHistory {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'uuid' })
  entity_id: string;

  /**
   * Coordonnées WGS84 — stockées comme GEOGRAPHY(Point, 4326) en PostGIS.
   * TypeORM n'a pas de support natif GEOGRAPHY, donc on utilise une colonne
   * custom et on insère via SQL brut dans le batch writer.
   */
  @Column({ type: 'decimal', precision: 10, scale: 7 })
  latitude: number;

  @Column({ type: 'decimal', precision: 10, scale: 7 })
  longitude: number;

  @Column({ type: 'float', nullable: true })
  altitude: number;

  /** Direction 0–360° */
  @Column({ type: 'float', nullable: true })
  heading: number;

  /** Vitesse en m/s */
  @Column({ type: 'float', nullable: true })
  speed: number;

  /** Précision GPS en mètres */
  @Column({ type: 'float', nullable: true })
  accuracy: number;

  /** NULL si la position est hors d'un trajet actif */
  @Column({ type: 'uuid', nullable: true })
  trip_id: string;

  /** Horodatage de la mesure GPS (côté client) */
  @Index()
  @Column({ type: 'timestamptz' })
  recorded_at: Date;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;
}
