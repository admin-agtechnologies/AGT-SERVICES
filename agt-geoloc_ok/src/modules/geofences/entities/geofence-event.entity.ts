import {
  Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, Index,
} from 'typeorm';

/** Enregistrement d'un événement d'entrée ou sortie de geofence. */
@Entity('geofence_events')
export class GeofenceEvent {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'uuid' })
  @Index()
  geofence_id: string;

  @Column({ type: 'uuid' })
  @Index()
  entity_id: string;

  /** enter | exit */
  @Column({ type: 'varchar', length: 10 })
  event_type: 'enter' | 'exit';

  @Column({ type: 'decimal', precision: 10, scale: 7 })
  latitude: number;

  @Column({ type: 'decimal', precision: 10, scale: 7 })
  longitude: number;

  @Column({ type: 'timestamptz' })
  recorded_at: Date;
}
