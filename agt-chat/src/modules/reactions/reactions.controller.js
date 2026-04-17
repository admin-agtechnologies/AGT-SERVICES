/**
 * Controller réactions.
 */
const reactionsService = require('./reactions.service');
const { success } = require('../../common/utils/response');

const addReaction = async (req, res, next) => {
  try {
    const io = req.app.get('io');
    await reactionsService.addReaction(req.params.msgId, req.user.user_id, req.body.emoji, io);
    return success(res, { added: true }, 201);
  } catch (err) { next(err); }
};

const removeReaction = async (req, res, next) => {
  try {
    const io = req.app.get('io');
    await reactionsService.removeReaction(req.params.msgId, req.user.user_id, req.params.emoji, io);
    return success(res, { removed: true });
  } catch (err) { next(err); }
};

const getReactions = async (req, res, next) => {
  try {
    const reactions = await reactionsService.getReactions(req.params.msgId);
    return success(res, reactions);
  } catch (err) { next(err); }
};

module.exports = { addReaction, removeReaction, getReactions };
