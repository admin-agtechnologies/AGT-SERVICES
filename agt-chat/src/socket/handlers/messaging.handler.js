/**
 * Handler WebSocket pour la messagerie.
 * Événements : message:send, message:edit, message:delete
 *
 * Règle : persistance DB avant émission (garantie par messagesService).
 */
const messagesService = require('../../modules/messages/messages.service');
const logger = require('../../common/utils/logger');

const registerMessagingHandlers = (io, socket) => {
  /**
   * message:send — envoi d'un message via WebSocket (chemin principal)
   * payload: { conversation_id, content, parent_id? }
   */
  socket.on('message:send', async (payload) => {
    try {
      const { conversation_id, content, parent_id } = payload || {};
      if (!conversation_id || !content) {
        return socket.emit('error', { code: 'VALIDATION_ERROR', message: 'conversation_id et content requis' });
      }
      await messagesService.sendMessage(conversation_id, socket.data.user_id, { content, parent_id }, io);
    } catch (err) {
      logger.warn({ err: err.message, user_id: socket.data.user_id }, 'message:send error');
      socket.emit('error', { code: err.code || 'ERROR', message: err.message });
    }
  });

  /**
   * message:edit
   * payload: { message_id, content, conversation_id }
   */
  socket.on('message:edit', async (payload) => {
    try {
      const { message_id, content, conversation_id } = payload || {};
      if (!message_id || !content || !conversation_id) {
        return socket.emit('error', { code: 'VALIDATION_ERROR', message: 'message_id, conversation_id et content requis' });
      }
      await messagesService.editMessage(conversation_id, message_id, socket.data.user_id, content, io);
    } catch (err) {
      socket.emit('error', { code: err.code || 'ERROR', message: err.message });
    }
  });

  /**
   * message:delete
   * payload: { message_id, conversation_id }
   */
  socket.on('message:delete', async (payload) => {
    try {
      const { message_id, conversation_id } = payload || {};
      if (!message_id || !conversation_id) {
        return socket.emit('error', { code: 'VALIDATION_ERROR', message: 'message_id et conversation_id requis' });
      }
      await messagesService.deleteMessage(conversation_id, message_id, socket.data.user_id, io);
    } catch (err) {
      socket.emit('error', { code: err.code || 'ERROR', message: err.message });
    }
  });
};

module.exports = { registerMessagingHandlers };
