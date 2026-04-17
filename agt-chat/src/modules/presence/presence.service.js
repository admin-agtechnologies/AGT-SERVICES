/**
 * Service présence — orchestration Redis-only pour présence et typing.
 * Aucune persistance DB (CDC §5.3.2).
 */
const presenceRepo = require('./presence.repository');
const conversationsRepo = require('../conversations/conversations.repository');
const capabilitiesService = require('../capabilities/capabilities.service');
const AppError = require('../../common/errors/AppError');

/**
 * Récupère la présence d'un utilisateur.
 * @param {string} targetUserId - Utilisateur cible
 * @param {string} requesterId - Demandeur (pour vérif plateforme)
 * @param {string} platformId
 */
const getUserPresence = async (targetUserId, platformId) => {
  const caps = await capabilitiesService.getCapabilities(platformId);
  capabilitiesService.requireFeature(caps, 'presence_enabled');
  return presenceRepo.getPresence(targetUserId);
};

/**
 * Met à jour la présence (online/away).
 * @param {string} userId
 * @param {string} status
 * @param {string} platformId
 * @param {object} [io]
 */
const updatePresence = async (userId, status, platformId, io = null) => {
  const caps = await capabilitiesService.getCapabilities(platformId);
  capabilitiesService.requireFeature(caps, 'presence_enabled');

  await presenceRepo.setPresence(userId, status);

  if (io) {
    // Émettre à toutes les conversations de l'utilisateur — simplifié ici via broadcast
    io.emit('presence:update', { user_id: userId, status, last_seen_at: new Date().toISOString() });
  }
};

/**
 * Renouvelle le heartbeat de présence.
 * @param {string} userId
 * @param {string} platformId
 */
const heartbeat = async (userId, platformId) => {
  return presenceRepo.heartbeat(userId);
};

/**
 * Démarre l'indicateur typing.
 * @param {string} conversationId
 * @param {string} userId
 * @param {string} platformId
 * @param {object} [io]
 */
const startTyping = async (conversationId, userId, platformId, io = null) => {
  const caps = await capabilitiesService.getCapabilities(platformId);
  capabilitiesService.requireFeature(caps, 'typing_enabled');

  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);

  await presenceRepo.startTyping(conversationId, userId);

  if (io) {
    io.to(conversationId).emit('typing:update', { user_id: userId, conversation_id: conversationId, is_typing: true });
  }
};

/**
 * Arrête l'indicateur typing.
 * @param {string} conversationId
 * @param {string} userId
 * @param {string} platformId
 * @param {object} [io]
 */
const stopTyping = async (conversationId, userId, platformId, io = null) => {
  await presenceRepo.stopTyping(conversationId, userId);

  if (io) {
    io.to(conversationId).emit('typing:update', { user_id: userId, conversation_id: conversationId, is_typing: false });
  }
};

module.exports = { getUserPresence, updatePresence, heartbeat, startTyping, stopTyping };
