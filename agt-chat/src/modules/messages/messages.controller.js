/**
 * Controller messages — handlers HTTP pour les messages, read receipts et recherche.
 */
const messagesService = require('./messages.service');
const { success, successPaginated } = require('../../common/utils/response');
const { buildPagination, decodeCursor } = require('../../common/utils/pagination');

/**
 * POST /api/v1/chat/conversations/:id/messages
 */
const sendMessage = async (req, res, next) => {
  try {
    // Récupérer l'instance Socket.io depuis app pour les émissions WS
    const io = req.app.get('io');
    const message = await messagesService.sendMessage(req.params.id, req.user.user_id, req.body, io);
    return success(res, message, 201);
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/conversations/:id/messages
 */
const getHistory = async (req, res, next) => {
  try {
    const { limit = 50, cursor } = req.query;
    const parsedLimit = Math.min(parseInt(limit, 10) || 50, 100);
    const cursorDate = cursor ? decodeCursor(cursor) : null;
    const rows = await messagesService.getHistory(req.params.id, req.user.user_id, { limit: parsedLimit, cursor: cursorDate });
    return successPaginated(res, rows, buildPagination(rows, parsedLimit));
  } catch (err) { next(err); }
};

/**
 * PUT /api/v1/chat/conversations/:id/messages/:msgId
 */
const editMessage = async (req, res, next) => {
  try {
    const io = req.app.get('io');
    const message = await messagesService.editMessage(req.params.id, req.params.msgId, req.user.user_id, req.body.content, io);
    return success(res, message);
  } catch (err) { next(err); }
};

/**
 * DELETE /api/v1/chat/conversations/:id/messages/:msgId
 */
const deleteMessage = async (req, res, next) => {
  try {
    const io = req.app.get('io');
    await messagesService.deleteMessage(req.params.id, req.params.msgId, req.user.user_id, io);
    return success(res, { deleted: true });
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/conversations/:id/messages/search
 */
const searchMessages = async (req, res, next) => {
  try {
    const { q, limit = 20 } = req.query;
    const rows = await messagesService.searchMessages(req.params.id, req.user.user_id, q, { limit: parseInt(limit, 10) || 20 });
    return success(res, rows);
  } catch (err) { next(err); }
};

/**
 * POST /api/v1/chat/conversations/:id/read
 */
const markRead = async (req, res, next) => {
  try {
    const io = req.app.get('io');
    await messagesService.markRead(req.params.id, req.user.user_id, req.body.last_message_id, io);
    return success(res, { marked: true });
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/conversations/:id/read-status
 */
const getReadStatus = async (req, res, next) => {
  try {
    const cursors = await messagesService.getReadStatus(req.params.id, req.user.user_id);
    return success(res, cursors);
  } catch (err) { next(err); }
};

module.exports = { sendMessage, getHistory, editMessage, deleteMessage, searchMessages, markRead, getReadStatus };
