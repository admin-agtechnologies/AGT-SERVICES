/**
 * Consumer RabbitMQ pour les événements entrants vers le service Chat.
 * Vérifie l'idempotence via event_id stocké en Redis avant traitement.
 */
const amqp = require('amqplib');
const logger = require('../utils/logger');
const { getRedis } = require('../cache/redis');

const IDEMPOTENCY_TTL = 86400; // 24h en secondes

let connection = null;
let channel = null;

/**
 * Vérifie si un événement a déjà été traité (idempotence).
 * @param {string} eventId - UUID de l'événement
 * @returns {Promise<boolean>} true si déjà traité
 */
const isAlreadyProcessed = async (eventId) => {
  const redis = getRedis();
  const key = `processed_event:${eventId}`;
  const result = await redis.set(key, '1', 'EX', IDEMPOTENCY_TTL, 'NX');
  // NX retourne null si la clé existe déjà (événement déjà traité)
  return result === null;
};

/**
 * Initialise la connexion et enregistre les handlers de messages entrants.
 * @param {object} handlers - Map { queueName: handlerFn }
 */
const connect = async (handlers = {}) => {
  try {
    connection = await amqp.connect(process.env.BROKER_URL || 'amqp://localhost:5672');
    channel = await connection.createChannel();
    channel.prefetch(10);

    for (const [queue, handler] of Object.entries(handlers)) {
      await channel.assertQueue(queue, { durable: true });
      channel.consume(queue, async (msg) => {
        if (!msg) return;
        try {
          const event = JSON.parse(msg.content.toString());

          // Vérification idempotence avant traitement
          if (event.event_id && await isAlreadyProcessed(event.event_id)) {
            logger.info({ event_id: event.event_id, queue }, 'Duplicate event skipped');
            channel.ack(msg);
            return;
          }

          await handler(event);
          channel.ack(msg);
        } catch (err) {
          logger.error({ err, queue }, 'Event processing failed — nacking');
          channel.nack(msg, false, true); // requeue
        }
      });
      logger.info({ queue }, 'Consumer registered');
    }

    logger.info('RabbitMQ consumer connected');
  } catch (err) {
    logger.error({ err }, 'RabbitMQ consumer connection failed');
  }
};

module.exports = { connect };
