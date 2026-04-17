/**
 * Handler WebSocket pour la présence.
 * Événements : presence:update, presence:heartbeat
 */
const presenceService = require('../../modules/presence/presence.service');
const presenceRepo = require('../../modules/presence/presence.repository');
const logger = require('../../common/utils/logger');

const registerPresenceHandlers = (io, socket) => {
  // Marquer l'utilisateur comme online à la connexion
  presenceRepo.setPresence(socket.data.user_id, 'online').catch(() => {});

  /**
   * presence:heartbeat — renouvelle le TTL de présence toutes les 30s
   */
  socket.on('presence:heartbeat', async () => {
    try {
      const data = await presenceService.heartbeat(socket.data.user_id, socket.data.platform_id);
      // Diffuser la mise à jour de présence
      io.emit('presence:update', { user_id: socket.data.user_id, ...data });
    } catch (err) {
      logger.warn({ err: err.message }, 'presence:heartbeat error');
    }
  });

  // À la déconnexion, marquer offline
  socket.on('disconnect', async () => {
    try {
      await presenceRepo.setPresence(socket.data.user_id, 'offline');
      io.emit('presence:update', {
        user_id: socket.data.user_id,
        status: 'offline',
        last_seen_at: new Date().toISOString(),
      });
      logger.info({ user_id: socket.data.user_id }, 'WebSocket disconnected — presence set offline');
    } catch (err) {
      logger.warn({ err: err.message }, 'disconnect presence update error');
    }
  });
};

module.exports = { registerPresenceHandlers };
