const express = require('express');
const router = express.Router({ mergeParams: true });
const authMiddleware = require('../../common/middleware/auth.middleware');
const ctrl = require('./reactions.controller');

router.use(authMiddleware);

router.post('/', ctrl.addReaction);
router.delete('/:emoji', ctrl.removeReaction);
router.get('/', ctrl.getReactions);

module.exports = router;
