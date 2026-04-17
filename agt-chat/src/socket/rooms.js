/**
 * Gestion des rooms Socket.io.
 * Chaque conversation a sa propre room identifiée par son UUID.
 * À la connexion, l'utilisateur rejoint automatiquement les rooms de ses conversations actives.
 */
const conversationsRepo = require('../modules/conversations/conversations.repository');
const logger = require('../common/utils/logger');

/**
 * Inscrit automatiquement l'utilisateur aux rooms de toutes ses conversations actives.
 * Appelé lors du 'connection' event.
 * @param {import('socket.io').Socket} socket
 */
const joinActiveConversations = async (socket) => {
  try {
    const { user_id, platform_id } = socket.data;
    // Récupérer les conversations actives de l'utilisateur (limite à 50 pour éviter la surcharge)
    const conversations = await conversationsRepo.findByUser(user_id, platform_id, { limit: 50 });
    for (const conv of conversations) {
      socket.join(conv.id);
    }
    logger.info({ user_id, count: conversations.length }, 'Socket joined active conversation rooms');
  } catch (err) {
    logger.error({ err, user_id: socket.data.user_id }, 'Failed to join active conversation rooms');
  }
};

/**
 * Rejoint la room d'une conversation (événement join_conversation).
 * @param {import('socket.io').Socket} socket
 * @param {string} conversationId
 */
const joinRoom = async (socket, conversationId) => {
  try {
    const participant = await conversationsRepo.findParticipant(conversationId, socket.data.user_id);
    if (!participant) {
      socket.emit('error', { code: 'NOT_PARTICIPANT', message: "Vous n'êtes pas membre de cette conversation" });
      return;
    }
    socket.join(conversationId);
  } catch (err) {
    logger.error({ err }, 'joinRoom error');
  }
};

/**
 * Quitte la room d'une conversation (événement leave_conversation).
 * @param {import('socket.io').Socket} socket
 * @param {string} conversationId
 */
const leaveRoom = (socket, conversationId) => {
  socket.leave(conversationId);
};

module.exports = { joinActiveConversations, joinRoom, leaveRoom };
