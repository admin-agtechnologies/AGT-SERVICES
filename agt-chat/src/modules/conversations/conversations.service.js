/**
 * Service conversations — logique métier pure.
 * Orchestration : vérification capabilities, règles métier, appels repository.
 * Ne contient aucune requête SQL directe (déléguées au repository).
 */
const conversationsRepo = require('./conversations.repository');
const capabilitiesService = require('../capabilities/capabilities.service');
const AppError = require('../../common/errors/AppError');
const logger = require('../../common/utils/logger');

/**
 * Crée une conversation directe ou un canal.
 * Règles métier :
 * - direct : anti-doublon, exactement 1 autre participant, capability direct_enabled
 * - channel : nom obligatoire, max_channel_members respecté, capability channels_enabled
 * @param {object} params - { type, platform_id, name, description, is_public, participant_ids, metadata }
 * @param {string} creatorId - users_auth.id du créateur
 * @returns {Promise<object>} Conversation créée
 */
const createConversation = async (params, creatorId) => {
  const caps = await capabilitiesService.getCapabilities(params.platform_id);

  if (params.type === 'direct') {
    capabilitiesService.requireFeature(caps, 'direct_enabled');

    const otherId = params.participant_ids?.[0];
    if (!otherId) {
      throw new AppError('VALIDATION_ERROR', 'Une conversation directe requiert un participant', 400);
    }

    // Anti-doublon : retourner la conv existante si elle existe déjà
    const existing = await conversationsRepo.findDirectBetween(creatorId, otherId, params.platform_id);
    if (existing) return existing;

    return conversationsRepo.createWithParticipants(
      { ...params, created_by: creatorId },
      [creatorId, otherId]
    );
  }

  if (params.type === 'channel') {
    capabilitiesService.requireFeature(caps, 'channels_enabled');

    if (!params.name) {
      throw new AppError('VALIDATION_ERROR', 'Le nom est obligatoire pour un canal', 400);
    }

    const participantIds = [creatorId, ...(params.participant_ids || [])];
    if (participantIds.length > caps.max_channel_members) {
      throw new AppError('VALIDATION_ERROR', `Le canal ne peut pas dépasser ${caps.max_channel_members} membres`, 400);
    }

    return conversationsRepo.createWithParticipants(
      { ...params, created_by: creatorId },
      participantIds
    );
  }

  throw new AppError('VALIDATION_ERROR', 'Type de conversation invalide (direct ou channel)', 400);
};

/**
 * Liste les conversations de l'utilisateur (paginées, triées par activité).
 * @param {string} userId
 * @param {string} platformId
 * @param {object} opts - { limit, cursor, type }
 * @returns {Promise<object[]>}
 */
const listConversations = async (userId, platformId, opts = {}) => {
  return conversationsRepo.findByUser(userId, platformId, opts);
};

/**
 * Récupère le détail d'une conversation.
 * Vérifie que l'utilisateur est participant.
 * @param {string} conversationId
 * @param {string} userId
 * @returns {Promise<object>}
 */
const getConversation = async (conversationId, userId) => {
  const conv = await conversationsRepo.findById(conversationId);
  if (!conv) throw new AppError('CONVERSATION_NOT_FOUND', 'Conversation introuvable', 404);

  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);

  return conv;
};

/**
 * Met à jour un canal (nom, description, visibilité).
 * Réservé à owner/admin du canal.
 * @param {string} conversationId
 * @param {string} userId
 * @param {object} fields
 * @returns {Promise<object>}
 */
const updateConversation = async (conversationId, userId, fields) => {
  const conv = await conversationsRepo.findById(conversationId);
  if (!conv) throw new AppError('CONVERSATION_NOT_FOUND', 'Conversation introuvable', 404);
  if (conv.type !== 'channel') throw new AppError('FORBIDDEN', 'Seuls les canaux peuvent être modifiés', 403);

  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant || !['owner', 'admin'].includes(participant.role)) {
    throw new AppError('FORBIDDEN', 'Seuls owner/admin peuvent modifier le canal', 403);
  }

  return conversationsRepo.update(conversationId, fields);
};

/**
 * Soft delete d'une conversation (admin uniquement).
 * @param {string} conversationId
 * @param {string} userId
 */
const deleteConversation = async (conversationId, userId) => {
  const conv = await conversationsRepo.findById(conversationId);
  if (!conv) throw new AppError('CONVERSATION_NOT_FOUND', 'Conversation introuvable', 404);

  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant || !['owner', 'admin'].includes(participant.role)) {
    throw new AppError('FORBIDDEN', 'Seuls owner/admin peuvent supprimer la conversation', 403);
  }

  await conversationsRepo.softDelete(conversationId);
  logger.info({ conversationId, userId }, 'Conversation soft-deleted');
};

/**
 * Ajoute un participant à un canal.
 * @param {string} conversationId
 * @param {string} requesterId - Utilisateur qui ajoute
 * @param {string} targetUserId - Utilisateur à ajouter
 */
const addParticipant = async (conversationId, requesterId, targetUserId) => {
  const conv = await conversationsRepo.findById(conversationId);
  if (!conv) throw new AppError('CONVERSATION_NOT_FOUND', 'Conversation introuvable', 404);

  const requester = await conversationsRepo.findParticipant(conversationId, requesterId);
  if (!requester) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);

  const caps = await capabilitiesService.getCapabilities(conv.platform_id);
  const count = await conversationsRepo.countParticipants(conversationId);
  if (count >= caps.max_channel_members) {
    throw new AppError('VALIDATION_ERROR', `Le canal a atteint la limite de ${caps.max_channel_members} membres`, 400);
  }

  return conversationsRepo.addParticipant(conversationId, targetUserId);
};

/**
 * Retire un participant d'un canal.
 * @param {string} conversationId
 * @param {string} requesterId
 * @param {string} targetUserId
 */
const removeParticipant = async (conversationId, requesterId, targetUserId) => {
  const conv = await conversationsRepo.findById(conversationId);
  if (!conv) throw new AppError('CONVERSATION_NOT_FOUND', 'Conversation introuvable', 404);

  const requester = await conversationsRepo.findParticipant(conversationId, requesterId);
  // Peut retirer soi-même, ou owner/admin peut retirer quelqu'un d'autre
  const isSelf = requesterId === targetUserId;
  if (!requester) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);
  if (!isSelf && !['owner', 'admin'].includes(requester.role)) {
    throw new AppError('FORBIDDEN', 'Seuls owner/admin peuvent retirer des membres', 403);
  }

  await conversationsRepo.removeParticipant(conversationId, targetUserId);
};

/**
 * L'utilisateur quitte lui-même une conversation.
 * @param {string} conversationId
 * @param {string} userId
 */
const leaveConversation = async (conversationId, userId) => {
  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);
  await conversationsRepo.removeParticipant(conversationId, userId);
};

/**
 * Liste les participants actifs d'une conversation.
 * @param {string} conversationId
 * @param {string} userId - Pour vérifier l'accès
 * @returns {Promise<object[]>}
 */
const listParticipants = async (conversationId, userId) => {
  const participant = await conversationsRepo.findParticipant(conversationId, userId);
  if (!participant) throw new AppError('NOT_PARTICIPANT', "Vous n'êtes pas membre de cette conversation", 403);
  return conversationsRepo.findParticipants(conversationId);
};

/**
 * Rejoindre un canal public.
 * @param {string} conversationId
 * @param {string} userId
 */
const joinChannel = async (conversationId, userId) => {
  const conv = await conversationsRepo.findById(conversationId);
  if (!conv) throw new AppError('CONVERSATION_NOT_FOUND', 'Conversation introuvable', 404);
  if (conv.type !== 'channel') throw new AppError('FORBIDDEN', 'Seuls les canaux peuvent être rejoints', 403);
  if (!conv.is_public) throw new AppError('FORBIDDEN', 'Ce canal est privé', 403);

  const caps = await capabilitiesService.getCapabilities(conv.platform_id);
  capabilitiesService.requireFeature(caps, 'channels_enabled');

  const count = await conversationsRepo.countParticipants(conversationId);
  if (count >= caps.max_channel_members) {
    throw new AppError('VALIDATION_ERROR', `Le canal a atteint la limite de ${caps.max_channel_members} membres`, 400);
  }

  return conversationsRepo.addParticipant(conversationId, userId, 'member');
};

module.exports = {
  createConversation, listConversations, getConversation, updateConversation,
  deleteConversation, addParticipant, removeParticipant, leaveConversation,
  listParticipants, joinChannel,
};
