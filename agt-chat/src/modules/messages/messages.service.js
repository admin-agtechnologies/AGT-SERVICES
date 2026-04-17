/**
 * Service messages — logique métier pour l'envoi, l'édition, la suppression et la lecture.
 *
 * Règle fondamentale (CDC §5.2.1) :
 * La persistance PostgreSQL est TOUJOURS faite avant l'émission WebSocket.
 * En cas d'erreur DB, le message n'est jamais émis.
 */
const messagesRepo = require('./messages.repository');
const conversationsRepo = require('../conversations/conversations.repository');
const capabilitiesService = require('../capabilities/capabilities.service');
const { resolveProfilesId } = require('../../common/clients/usersClient');
const { sendNotification } = require('../../common/clients/notificationClient');
const { publish } = require('../../common/broker/publisher');
const AppError = require('../../common/errors/AppError');
const logger = require('../../common/utils/logger');

const EDIT_DELAY_MIN = () => parseInt(process.env.MESSAGE_EDIT_DELAY_MIN || '15', 10);

/**
 * Envoie un message dans une conversation.
 * Séquence : vérif participant → vérif capabilities → persist DB → emit WS → notif hors ligne → event RabbitMQ.
 * @param {string} conversationId
 * @param {string} senderId - users_auth.id
 * @param {object} body - { content, parent_id? }
 * @param {object} [io] - Instance Socket.io pour émission WS
 * @returns {Promise<object>} Message créé
 */
const sendMessage = async (conversationId, senderId, body, io = null) => {
  const conv = await conversationsRepo.findById(conversationId);
  if (!conv) throw new AppError('CONVERSATION_NOT_FOUND', 'Conversation introuvable', 404);

  const participant = await conversationsRepo.findParticipant(conversationId, senderId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);

  const caps = await capabilitiesService.getCapabilities(conv.platform_id);

  // Vérification taille max du message selon capabilities de la plateforme
  if (body.content && body.content.length > caps.max_message_length) {
    throw new AppError('VALIDATION_ERROR', `Message trop long (max ${caps.max_message_length} caractères)`, 400);
  }

  // 1. Persistance DB en premier — garantit zéro perte
  const message = await messagesRepo.create({
    conversation_id: conversationId,
    sender_id: senderId,
    content: body.content,
    parent_id: body.parent_id || null,
  });

  // 2. Mise à jour de l'activité de la conversation
  await conversationsRepo.touch(conversationId);

  // 3. Émission WebSocket (si io disponible)
  if (io) {
    io.to(conversationId).emit('message:new', {
      message_id: message.id,
      conversation_id: conversationId,
      sender_id: senderId,
      content: message.content,
      parent_id: message.parent_id,
      created_at: message.created_at,
    });
  }

  // 4. Notification hors ligne (non-bloquant, mapping auth→profiles via Users)
  _notifyOfflineParticipants(conv, message, senderId).catch((err) =>
    logger.warn({ err }, 'Offline notification pipeline failed (non-blocking)')
  );

  // 5. Événement RabbitMQ pour les consommateurs externes
  await publish('chat.message.created', {
    conversation_id: conversationId,
    message_id: message.id,
    sender_id: senderId,
  });

  return message;
};

/**
 * Envoie des notifications hors ligne aux participants absents.
 * Mapping users_auth.id → users_profiles.id requis avant appel Notification (CDC §10.4).
 * @private
 */
const _notifyOfflineParticipants = async (conv, message, senderId) => {
  const participants = await conversationsRepo.findParticipants(conv.id);
  for (const p of participants) {
    if (p.user_id === senderId) continue; // Pas de notif à l'expéditeur
    // Résoudre users_profiles.id avant d'appeler Notification
    const profilesId = await resolveProfilesId(p.user_id);
    if (profilesId) {
      await sendNotification(profilesId, conv.platform_id, 'chat_message_offline', {
        conversation_id: conv.id,
        message_id: message.id,
        sender_id: senderId,
      });
    }
  }
};

/**
 * Édite un message.
 * Règles : auteur uniquement, dans le délai MESSAGE_EDIT_DELAY_MIN, capability message_edit_enabled.
 * @param {string} conversationId
 * @param {string} messageId
 * @param {string} userId
 * @param {string} content
 * @param {object} [io]
 * @returns {Promise<object>}
 */
const editMessage = async (conversationId, messageId, userId, content, io = null) => {
  const message = await messagesRepo.findById(messageId);
  if (!message || message.conversation_id !== conversationId) {
    throw new AppError('MESSAGE_NOT_FOUND', 'Message introuvable', 404);
  }
  if (message.is_deleted) throw new AppError('MESSAGE_NOT_FOUND', 'Message supprimé', 404);
  if (message.sender_id !== userId) throw new AppError('FORBIDDEN', 'Seul l\'auteur peut éditer son message', 403);

  const conv = await conversationsRepo.findById(conversationId);
  const caps = await capabilitiesService.getCapabilities(conv.platform_id);
  capabilitiesService.requireFeature(caps, 'message_edit_enabled');

  // Vérification du délai d'édition
  const editDeadline = new Date(message.created_at);
  editDeadline.setMinutes(editDeadline.getMinutes() + EDIT_DELAY_MIN());
  if (new Date() > editDeadline) {
    throw new AppError('MESSAGE_EDIT_WINDOW_EXPIRED', `Le délai d'édition de ${EDIT_DELAY_MIN()} minutes est dépassé`, 403);
  }

  if (content.length > caps.max_message_length) {
    throw new AppError('VALIDATION_ERROR', `Message trop long (max ${caps.max_message_length} caractères)`, 400);
  }

  const updated = await messagesRepo.edit(messageId, content);

  if (io) {
    io.to(conversationId).emit('message:updated', {
      message_id: updated.id,
      content: updated.content,
      edited_at: updated.edited_at,
    });
  }

  return updated;
};

/**
 * Soft delete d'un message.
 * Auteur peut supprimer le sien ; admin/owner peut supprimer n'importe quel message.
 * @param {string} conversationId
 * @param {string} messageId
 * @param {string} userId
 * @param {object} [io]
 */
const deleteMessage = async (conversationId, messageId, userId, io = null) => {
  const message = await messagesRepo.findById(messageId);
  if (!message || message.conversation_id !== conversationId) {
    throw new AppError('MESSAGE_NOT_FOUND', 'Message introuvable', 404);
  }
  if (message.is_deleted) return; // Idempotent

  const conv = await conversationsRepo.findById(conversationId);
  const caps = await capabilitiesService.getCapabilities(conv.platform_id);
  capabilitiesService.requireFeature(caps, 'message_delete_enabled');

  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  const isAuthor = message.sender_id === userId;
  const isAdmin = participant && ['owner', 'admin'].includes(participant.role);
  if (!isAuthor && !isAdmin) {
    throw new AppError('FORBIDDEN', 'Vous ne pouvez pas supprimer ce message', 403);
  }

  await messagesRepo.softDelete(messageId);

  if (io) {
    io.to(conversationId).emit('message:deleted', { message_id: messageId });
  }
};

/**
 * Historique paginé d'une conversation.
 * @param {string} conversationId
 * @param {string} userId
 * @param {object} opts - { limit, cursor }
 * @returns {Promise<object[]>}
 */
const getHistory = async (conversationId, userId, opts = {}) => {
  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);
  return messagesRepo.findByConversation(conversationId, opts);
};

/**
 * Recherche full-text dans une conversation.
 * @param {string} conversationId
 * @param {string} userId
 * @param {string} q
 * @param {object} opts
 */
const searchMessages = async (conversationId, userId, q, opts = {}) => {
  if (!q || q.trim().length < 2) {
    throw new AppError('VALIDATION_ERROR', 'La recherche doit contenir au moins 2 caractères', 400);
  }
  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);

  const conv = await conversationsRepo.findById(conversationId);
  const caps = await capabilitiesService.getCapabilities(conv.platform_id);
  capabilitiesService.requireFeature(caps, 'message_search_enabled');

  return messagesRepo.search(conversationId, q, opts);
};

/**
 * Marque une conversation comme lue jusqu'à un message donné.
 * @param {string} conversationId
 * @param {string} userId
 * @param {string} lastMessageId
 * @param {object} [io]
 */
const markRead = async (conversationId, userId, lastMessageId, io = null) => {
  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);

  const conv = await conversationsRepo.findById(conversationId);
  const caps = await capabilitiesService.getCapabilities(conv.platform_id);
  capabilitiesService.requireFeature(caps, 'read_receipts_enabled');

  await messagesRepo.upsertReadCursor(conversationId, userId, lastMessageId);

  if (io) {
    io.to(conversationId).emit('read:updated', {
      conversation_id: conversationId,
      user_id: userId,
      last_read_message_id: lastMessageId,
    });
  }
};

/**
 * Récupère les curseurs de lecture de tous les participants.
 * @param {string} conversationId
 * @param {string} userId
 */
const getReadStatus = async (conversationId, userId) => {
  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);
  return messagesRepo.findReadCursors(conversationId);
};

module.exports = { sendMessage, editMessage, deleteMessage, getHistory, searchMessages, markRead, getReadStatus };
