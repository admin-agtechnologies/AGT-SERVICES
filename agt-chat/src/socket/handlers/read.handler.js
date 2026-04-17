/**
 * Handler WebSocket pour les accusés de lecture.
 * Événement : read:mark
 */
const messagesService = require('../../modules/messages/messages.service');

const registerReadHandlers = (io, socket) => {
  /**
   * read:mark
   * payload: { conversation_id, last_message_id }
   */
  socket.on('read:mark', async (payload) => {
    try {
      const { conversation_id, last_message_id } = payload || {};
      if (!conversation_id || !last_message_id) return;
      await messagesService.markRead(conversation_id, socket.data.user_id, last_message_id, io);
    } catch (err) {
      socket.emit('error', { code: err.code || 'ERROR', message: err.message });
    }
  });
};

module.exports = { registerReadHandlers };
