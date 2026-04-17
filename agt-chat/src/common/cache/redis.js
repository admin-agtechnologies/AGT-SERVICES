/**
 * Client Redis partagé (ioredis).
 * Utilisé pour : présence, typing, rate limiting, cache auth/users, idempotence events.
 * NE PAS créer d'autres instances Redis ailleurs — toujours importer ce module.
 */
const Redis = require('ioredis');
const logger = require('../utils/logger');

let redisClient = null;

const getRedis = () => {
  if (!redisClient) {
    redisClient = new Redis(process.env.REDIS_URL || 'redis://localhost:6379/0', {
      // Reconnexion automatique avec backoff exponentiel
      retryStrategy: (times) => Math.min(times * 100, 3000),
      maxRetriesPerRequest: 3,
      lazyConnect: false,
    });

    redisClient.on('connect', () => logger.info('Redis connected'));
    redisClient.on('error', (err) => logger.error({ err }, 'Redis error'));
    redisClient.on('reconnecting', () => logger.warn('Redis reconnecting'));
  }
  return redisClient;
};

/**
 * Vérifie la connexion Redis (utilisé par le health check).
 * @returns {Promise<boolean>}
 */
const ping = async () => {
  const result = await getRedis().ping();
  return result === 'PONG';
};

module.exports = { getRedis, ping };
