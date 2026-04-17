/**
 * Handler WebSocket pour l'indicateur de saisie.
 * Événements : typing:start, typing:stop
 * Redis-only, TTL TYPING_TIMEOUT_MS.
 */
const presenceService = require('../../modules/presence/presence.service');

const registerTypingHandlers = (io, socket) => {
  /**
   * typing:start
   * payload: { conversation_id }
   */
  socket.on('typing:start', async (payload) => {
    try {
      const { conversation_id } = payload || {};
      if (!conversation_id) return;
      await presenceService.startTyping(conversation_id, socket.data.user_id, socket.data.platform_id, io);
    } catch (err) {
      socket.emit('error', { code: err.code || 'ERROR', message: err.message });
    }
  });

  /**
   * typing:stop
   * payload: { conversation_id }
   */
  socket.on('typing:stop', async (payload) => {
    try {
      const { conversation_id } = payload || {};
      if (!conversation_id) return;
      await presenceService.stopTyping(conversation_id, socket.data.user_id, socket.data.platform_id, io);
    } catch (err) {
      socket.emit('error', { code: err.code || 'ERROR', message: err.message });
    }
  });
};

module.exports = { registerTypingHandlers };
