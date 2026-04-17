/**
 * Configuration centralisée du service Geoloc.
 * Toutes les variables d'environnement sont lues ici.
 */
export default () => ({
  port: parseInt(process.env.PORT, 10) || 7009,
  nodeEnv: process.env.NODE_ENV || 'development',

  database: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT, 10) || 5432,
    username: process.env.DB_USER || 'geoloc_user',
    password: process.env.DB_PASSWORD || 'geoloc_password',
    database: process.env.DB_NAME || 'agt_geoloc_db',
  },

  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT, 10) || 6379,
    password: process.env.REDIS_PASSWORD || undefined,
    // TTL par défaut en secondes pour les entités online
    defaultTtl: parseInt(process.env.REDIS_DEFAULT_TTL, 10) || 30,
  },

  rabbitmq: {
    url: process.env.RABBITMQ_URL || 'amqp://agt_rabbit:agt_rabbit_password@localhost:5672',
    exchange: process.env.RABBITMQ_EXCHANGE || 'agt.geoloc',
  },

  auth: {
    serviceUrl: process.env.AUTH_SERVICE_URL || 'http://localhost:7000',
    publicKeyPath: process.env.AUTH_PUBLIC_KEY_PATH || './keys/auth_public.pem',
    s2sClientId: process.env.S2S_CLIENT_ID || '',
    s2sClientSecret: process.env.S2S_CLIENT_SECRET || '',
    jwtAudience: process.env.JWT_AUDIENCE || '',
  },

  providers: {
    googleMapsApiKey: process.env.GOOGLE_MAPS_API_KEY || '',
    osrmUrl: process.env.OSRM_URL || 'http://router.project-osrm.org',
    nominatimUrl: process.env.NOMINATIM_URL || 'https://nominatim.openstreetmap.org',
  },

  geofencing: {
    // Intervalle de nettoyage du cache geofence en ms
    cacheSyncIntervalMs: parseInt(process.env.GEOFENCE_CACHE_SYNC_MS, 10) || 10000,
  },

  batch: {
    // Intervalle de flush PostGIS en secondes
    flushIntervalSeconds: parseInt(process.env.BATCH_FLUSH_SECONDS, 10) || 15,
  },
});
