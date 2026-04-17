import {
  Entity, PrimaryGeneratedColumn, Column, CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

/**
 * Configuration de géolocalisation par plateforme.
 * Chaque plateforme peut définir son intervalle de mise à jour,
 * son TTL Redis, ses providers ETA/géocodage, etc.
 */
@Entity('platform_geo_configs')
export class PlatformGeoConfig {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'uuid', unique: true })
  platform_id: string;

  /** Fréquence de mise à jour en secondes (1–60) */
  @Column({ type: 'int', default: 5 })
  update_interval_seconds: number;

  /** TTL Redis : l'entité est offline après X secondes sans update */
  @Column({ type: 'int', default: 30 })
  position_ttl_seconds: number;

  /** Intervalle de flush batch vers PostGIS */
  @Column({ type: 'int', default: 15 })
  batch_flush_seconds: number;

  /** Provider ETA prioritaire : haversine | osrm | google_maps */
  @Column({ type: 'varchar', length: 30, default: 'haversine' })
  default_eta_provider: string;

  /** Provider géocodage : nominatim | google_maps */
  @Column({ type: 'varchar', length: 30, default: 'nominatim' })
  default_geocode_provider: string;

  /** Rayon max autorisé pour les requêtes de proximité */
  @Column({ type: 'float', default: 50 })
  max_proximity_radius_km: number;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamptz' })
  updated_at: Date;
}
