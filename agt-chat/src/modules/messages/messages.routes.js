const express = require('express');
const router = express.Router({ mergeParams: true }); // mergeParams pour accéder à :id de la conv
const authMiddleware = require('../../common/middleware/auth.middleware');
const { rateLimitMessages } = require('../../common/middleware/rateLimit.middleware');
const ctrl = require('./messages.controller');
const { validate, sendMessageSchema, editMessageSchema, markReadSchema } = require('./messages.validators');

router.use(authMiddleware);

// Historique et recherche
router.get('/', ctrl.getHistory);
router.get('/search', ctrl.searchMessages);

// Envoi avec rate limiting
router.post('/', rateLimitMessages, validate(sendMessageSchema), ctrl.sendMessage);

// Édition / suppression
router.put('/:msgId', validate(editMessageSchema), ctrl.editMessage);
router.delete('/:msgId', ctrl.deleteMessage);

// Read receipts (montés directement sur /conversations/:id/read)
module.exports = router;
