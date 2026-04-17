/**
 * Controller transfers.
 */
const transfersService = require('./transfers.service');
const { success } = require('../../common/utils/response');

/**
 * POST /api/v1/chat/conversations/transfer — S2S uniquement
 */
const createTransfer = async (req, res, next) => {
  try {
    const io = req.app.get('io');
    const result = await transfersService.createTransfer(req.body, io);
    return success(res, result, 201);
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/transfers/pending
 */
const getPendingTransfers = async (req, res, next) => {
  try {
    const platformId = req.query.platform_id || req.user?.platform_id || null;
    const transfers = await transfersService.getPendingTransfers(platformId);
    return success(res, transfers);
  } catch (err) { next(err); }
};

/**
 * POST /api/v1/chat/transfers/:id/take
 */
const takeTransfer = async (req, res, next) => {
  try {
    const io = req.app.get('io');
    const platformId = req.user.platform_id;
    const transfer = await transfersService.takeTransfer(req.params.id, req.user.user_id, platformId, io);
    return success(res, transfer);
  } catch (err) { next(err); }
};

/**
 * POST /api/v1/chat/transfers/:id/close
 */
const closeTransfer = async (req, res, next) => {
  try {
    const io = req.app.get('io');
    const transfer = await transfersService.closeTransfer(req.params.id, req.user.user_id, io);
    return success(res, transfer);
  } catch (err) { next(err); }
};

/**
 * GET /api/v1/chat/transfers/stats — admin/S2S
 */
const getStats = async (req, res, next) => {
  try {
    const stats = await transfersService.getStats();
    return success(res, stats);
  } catch (err) { next(err); }
};

module.exports = { createTransfer, getPendingTransfers, takeTransfer, closeTransfer, getStats };
