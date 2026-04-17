/**
 * Initialisation de Socket.io avec Redis Adapter pour le scaling multi-instances.
 * Redis Adapter permet aux événements d'être distribués entre toutes les instances
 * via Redis Pub/Sub (indispensable pour le déploiement horizontal).
 */
const { Server } = require('socket.io');
const { createAdapter } = require('@socket.io/redis-adapter');
const { getRedis } = require('../common/cache/redis');
const socketAuthMiddleware = require('./auth.middleware');
const { joinActiveConversations, joinRoom, leaveRoom } = require('./rooms');
const { registerMessagingHandlers } = require('./handlers/messaging.handler');
const { registerPresenceHandlers } = require('./handlers/presence.handler');
const { registerTypingHandlers } = require('./handlers/typing.handler');
const { registerReactionsHandlers } = require('./handlers/reactions.handler');
const { registerReadHandlers } = require('./handlers/read.handler');
const logger = require('../common/utils/logger');

const WS_EVENTS_PER_SEC = () => parseInt(process.env.RATE_LIMIT_WS_EVENTS_PER_SEC || '10', 10);

/**
 * Initialise Socket.io sur le serveur HTTP.
 * @param {import('http').Server} httpServer
 * @returns {import('socket.io').Server}
 */
const initSocket = (httpServer) => {
  const corsOrigins = (process.env.SOCKET_IO_CORS_ORIGIN || 'http://localhost:3000').split(',');

  const io = new Server(httpServer, {
    cors: {
      origin: corsOrigins,
      methods: ['GET', 'POST'],
      credentials: true,
    },
    // Sticky sessions requises avec le Redis Adapter (LB doit router par socket)
    transports: ['websocket', 'polling'],
  });

  // Redis Adapter pour la synchronisation multi-instances
  try {
    const pubClient = getRedis().duplicate();
    const subClient = getRedis().duplicate();
    io.adapter(createAdapter(pubClient, subClient));
    logger.info('Socket.io Redis Adapter configured');
  } catch (err) {
    logger.error({ err }, 'Failed to configure Redis Adapter — running single-instance only');
  }

  // Middleware d'authentification JWT au handshake
  io.use(socketAuthMiddleware);

  // Anti-flood WebSocket : limite le nombre d'événements par client/seconde
  io.use((socket, next) => {
    let eventCount = 0;
    const limit = WS_EVENTS_PER_SEC();

    // Réinitialiser le compteur chaque seconde
    const interval = setInterval(() => { eventCount = 0; }, 1000);

    socket.onAny(() => {
      eventCount++;
      if (eventCount > limit) {
        socket.emit('error', { code: 'RATE_LIMIT_EXCEEDED', message: 'Trop d\'événements WebSocket' });
        socket.disconnect(true);
        clearInterval(interval);
      }
    });

    socket.on('disconnect', () => clearInterval(interval));
    next();
  });

  io.on('connection', async (socket) => {
    logger.info({ user_id: socket.data.user_id }, 'Socket connected');

    // Rejoindre les rooms des conversations actives automatiquement
    await joinActiveConversations(socket);

    // Gestion des rooms explicites
    socket.on('join_conversation', ({ conversation_id }) => joinRoom(socket, conversation_id));
    socket.on('leave_conversation', ({ conversation_id }) => leaveRoom(socket, conversation_id));

    // Enregistrer tous les handlers métier
    registerMessagingHandlers(io, socket);
    registerPresenceHandlers(io, socket);
    registerTypingHandlers(io, socket);
    registerReactionsHandlers(io, socket);
    registerReadHandlers(io, socket);
  });

  return io;
};

module.exports = { initSocket };
