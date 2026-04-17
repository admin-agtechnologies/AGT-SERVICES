/**
 * Service réactions.
 */
const reactionsRepo = require('./reactions.repository');
const messagesRepo = require('../messages/messages.repository');
const conversationsRepo = require('../conversations/conversations.repository');
const capabilitiesService = require('../capabilities/capabilities.service');
const AppError = require('../../common/errors/AppError');

/**
 * Ajoute une réaction à un message.
 * @param {string} messageId
 * @param {string} userId
 * @param {string} emoji
 * @param {object} [io]
 */
const addReaction = async (messageId, userId, emoji, io = null) => {
  const message = await messagesRepo.findById(messageId);
  if (!message || message.is_deleted) throw new AppError('MESSAGE_NOT_FOUND', 'Message introuvable', 404);

  const conv = await conversationsRepo.findById(message.conversation_id);
  const caps = await capabilitiesService.getCapabilities(conv.platform_id);
  capabilitiesService.requireFeature(caps, 'reactions_enabled');

  const participant = await conversationsRepo.findParticipant(message.conversation_id, userId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);

  await reactionsRepo.add(messageId, userId, emoji);

  if (io) {
    const reactions = await reactionsRepo.findByMessage(messageId);
    io.to(message.conversation_id).emit('reaction:updated', { message_id: messageId, reactions });
  }
};

/**
 * Retire une réaction.
 * @param {string} messageId
 * @param {string} userId
 * @param {string} emoji
 * @param {object} [io]
 */
const removeReaction = async (messageId, userId, emoji, io = null) => {
  const message = await messagesRepo.findById(messageId);
  if (!message) throw new AppError('MESSAGE_NOT_FOUND', 'Message introuvable', 404);

  await reactionsRepo.remove(messageId, userId, emoji);

  if (io) {
    const reactions = await reactionsRepo.findByMessage(messageId);
    io.to(message.conversation_id).emit('reaction:updated', { message_id: messageId, reactions });
  }
};

/**
 * Liste les réactions d'un message.
 * @param {string} messageId
 */
const getReactions = async (messageId) => {
  const message = await messagesRepo.findById(messageId);
  if (!message) throw new AppError('MESSAGE_NOT_FOUND', 'Message introuvable', 404);
  return reactionsRepo.findByMessage(messageId);
};

module.exports = { addReaction, removeReaction, getReactions };
