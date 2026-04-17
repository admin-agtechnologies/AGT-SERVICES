import {
  Entity, PrimaryGeneratedColumn, Column, CreateDateColumn,
  UpdateDateColumn, OneToMany, Index, Unique,
} from 'typeorm';

/**
 * Entité trackée par le service de géolocalisation.
 * NE contient aucun concept métier : c'est la plateforme consommatrice
 * qui donne le sens (chauffeur, livreur, vendeur...).
 */
@Entity('tracked_entities')
@Unique(['platform_id', 'entity_type', 'entity_id'])
export class TrackedEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'uuid' })
  platform_id: string;

  /** Type d'entité : user, vehicle, asset */
  @Column({ type: 'varchar', length: 20 })
  entity_type: string;

  /** Référence externe — correspond à users_auth.id dans la plupart des cas */
  @Column({ type: 'uuid' })
  entity_id: string;

  /** Tags métier libres ex: ["available", "vip"] */
  @Column({ type: 'jsonb', default: [] })
  tags: string[];

  @Column({ type: 'boolean', default: true })
  is_active: boolean;

  @Column({ type: 'timestamptz', nullable: true })
  last_seen_at: Date;

  @CreateDateColumn({ type: 'timestamptz' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamptz' })
  updated_at: Date;
}
