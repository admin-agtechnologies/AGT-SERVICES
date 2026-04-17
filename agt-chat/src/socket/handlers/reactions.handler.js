/**
 * Handler WebSocket pour les réactions emoji.
 * Événements : reaction:add, reaction:remove
 */
const reactionsService = require('../../modules/reactions/reactions.service');

const registerReactionsHandlers = (io, socket) => {
  /**
   * reaction:add
   * payload: { message_id, emoji }
   */
  socket.on('reaction:add', async (payload) => {
    try {
      const { message_id, emoji } = payload || {};
      if (!message_id || !emoji) return;
      await reactionsService.addReaction(message_id, socket.data.user_id, emoji, io);
    } catch (err) {
      socket.emit('error', { code: err.code || 'ERROR', message: err.message });
    }
  });

  /**
   * reaction:remove
   * payload: { message_id, emoji }
   */
  socket.on('reaction:remove', async (payload) => {
    try {
      const { message_id, emoji } = payload || {};
      if (!message_id || !emoji) return;
      await reactionsService.removeReaction(message_id, socket.data.user_id, emoji, io);
    } catch (err) {
      socket.emit('error', { code: err.code || 'ERROR', message: err.message });
    }
  });
};

module.exports = { registerReactionsHandlers };
