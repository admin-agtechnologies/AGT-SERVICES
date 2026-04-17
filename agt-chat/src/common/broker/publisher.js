/**
 * Publisher RabbitMQ pour les événements émis par le service Chat.
 * Exchange : chat.events (topic)
 * Chaque event contient : event_id, timestamp, source: 'chat' (CDC §3.2)
 */
const amqp = require('amqplib');
const { v4: uuidv4 } = require('uuid');
const logger = require('../utils/logger');

const EXCHANGE = 'chat.events';
let channel = null;
let connection = null;

/**
 * Initialise la connexion RabbitMQ et déclare l'exchange.
 * Appelé au démarrage du service.
 */
const connect = async () => {
  try {
    connection = await amqp.connect(process.env.BROKER_URL || 'amqp://localhost:5672');
    channel = await connection.createChannel();
    await channel.assertExchange(EXCHANGE, 'topic', { durable: true });
    logger.info({ exchange: EXCHANGE }, 'RabbitMQ publisher connected');

    connection.on('error', (err) => logger.error({ err }, 'RabbitMQ connection error'));
    connection.on('close', () => logger.warn('RabbitMQ connection closed'));
  } catch (err) {
    // Ne pas planter le service si RabbitMQ est indisponible au démarrage
    logger.error({ err }, 'RabbitMQ publisher connection failed — events will be lost');
  }
};

/**
 * Publie un événement sur l'exchange chat.events.
 * @param {string} routingKey - Ex: chat.message.created
 * @param {object} payload - Données métier de l'événement
 */
const publish = async (routingKey, payload) => {
  if (!channel) {
    logger.warn({ routingKey }, 'RabbitMQ channel not available, skipping event');
    return;
  }
  try {
    const event = {
      event_id: uuidv4(),
      timestamp: new Date().toISOString(),
      source: 'chat',
      ...payload,
    };
    channel.publish(EXCHANGE, routingKey, Buffer.from(JSON.stringify(event)), {
      persistent: true,
      contentType: 'application/json',
    });
    logger.info({ routingKey, event_id: event.event_id }, 'Event published');
  } catch (err) {
    logger.error({ err, routingKey }, 'Failed to publish event');
  }
};

/**
 * Vérifie l'état de la connexion (utilisé par le health check).
 * @returns {boolean}
 */
const isConnected = () => channel !== null && connection !== null;

module.exports = { connect, publish, isConnected };
