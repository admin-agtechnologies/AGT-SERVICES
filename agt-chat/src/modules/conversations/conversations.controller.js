/**
 * Controller conversations — handlers HTTP.
 * Responsabilités : valider les params/query, appeler le service, formater la réponse.
 * Aucune logique métier ici.
 */
const conversationsService = require('./conversations.service');
const conversationsRepo = require('./conversations.repository');
const { success, successPaginated } = require('../../common/utils/response');
const { buildPagination, decodeCursor } = require('../../common/utils/pagination');

/**
 * POST /api/v1/chat/conversations
 */
const createConversation = async (req, res, next) => {
  try {
    const conversation = await conversationsService.createConversation(req.body, req.user.user_id);
    return success(res, conversation, 201);
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/conversations
 */
const listConversations = async (req, res, next) => {
  try {
    const { limit = 20, cursor, type } = req.query;
    const parsedLimit = Math.min(parseInt(limit, 10) || 20, 100);
    const cursorDate = cursor ? decodeCursor(cursor) : null;

    const rows = await conversationsService.listConversations(
      req.user.user_id,
      req.user.platform_id,
      { limit: parsedLimit, cursor: cursorDate, type }
    );
    return successPaginated(res, rows, buildPagination(rows, parsedLimit));
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/conversations/:id
 */
const getConversation = async (req, res, next) => {
  try {
    const conv = await conversationsService.getConversation(req.params.id, req.user.user_id);
    return success(res, conv);
  } catch (err) { next(err); }
};

/**
 * PUT /api/v1/chat/conversations/:id
 */
const updateConversation = async (req, res, next) => {
  try {
    const updated = await conversationsService.updateConversation(req.params.id, req.user.user_id, req.body);
    return success(res, updated);
  } catch (err) { next(err); }
};

/**
 * DELETE /api/v1/chat/conversations/:id
 */
const deleteConversation = async (req, res, next) => {
  try {
    await conversationsService.deleteConversation(req.params.id, req.user.user_id);
    return success(res, { deleted: true });
  } catch (err) { next(err); }
};

/**
 * POST /api/v1/chat/conversations/:id/participants
 */
const addParticipant = async (req, res, next) => {
  try {
    const participant = await conversationsService.addParticipant(req.params.id, req.user.user_id, req.body.user_id);
    return success(res, participant, 201);
  } catch (err) { next(err); }
};

/**
 * DELETE /api/v1/chat/conversations/:id/participants/:uid
 */
const removeParticipant = async (req, res, next) => {
  try {
    await conversationsService.removeParticipant(req.params.id, req.user.user_id, req.params.uid);
    return success(res, { removed: true });
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/conversations/:id/participants
 */
const listParticipants = async (req, res, next) => {
  try {
    const participants = await conversationsService.listParticipants(req.params.id, req.user.user_id);
    return success(res, participants);
  } catch (err) { next(err); }
};

/**
 * POST /api/v1/chat/conversations/:id/leave
 */
const leaveConversation = async (req, res, next) => {
  try {
    await conversationsService.leaveConversation(req.params.id, req.user.user_id);
    return success(res, { left: true });
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/platforms/:platformId/channels
 */
const listPublicChannels = async (req, res, next) => {
  try {
    const { limit = 20, cursor } = req.query;
    const parsedLimit = Math.min(parseInt(limit, 10) || 20, 100);
    const cursorDate = cursor ? decodeCursor(cursor) : null;
    const rows = await conversationsRepo.findPublicChannels(req.params.platformId, { limit: parsedLimit, cursor: cursorDate });
    return successPaginated(res, rows, buildPagination(rows, parsedLimit));
  } catch (err) { next(err); }
};

/**
 * POST /api/v1/chat/channels/:id/join
 */
const joinChannel = async (req, res, next) => {
  try {
    const participant = await conversationsService.joinChannel(req.params.id, req.user.user_id);
    return success(res, participant, 201);
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/conversations/stats (admin/S2S)
 */
const getStats = async (req, res, next) => {
  try {
    const platformId = req.query.platform_id || null;
    const stats = await conversationsRepo.getStats(platformId);
    return success(res, stats);
  } catch (err) { next(err); }
};

module.exports = {
  createConversation, listConversations, getConversation, updateConversation,
  deleteConversation, addParticipant, removeParticipant, listParticipants,
  leaveConversation, listPublicChannels, joinChannel, getStats,
};
