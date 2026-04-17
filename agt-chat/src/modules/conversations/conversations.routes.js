const express = require('express');
const router = express.Router();
const authMiddleware = require('../../common/middleware/auth.middleware');
const s2sMiddleware = require('../../common/middleware/s2s.middleware');
const capabilitiesMiddleware = require('../../common/middleware/capabilities.middleware');
const ctrl = require('./conversations.controller');
const { validate, createConversationSchema, updateConversationSchema, addParticipantSchema } = require('./conversations.validators');

// Toutes les routes conversations nécessitent JWT
router.use(authMiddleware);
router.use(capabilitiesMiddleware);

// --- Conversations CRUD ---
router.post('/', validate(createConversationSchema), ctrl.createConversation);
router.get('/', ctrl.listConversations);

// Stats — accessible admin/S2S uniquement (vérification dans controller)
router.get('/stats', ctrl.getStats);

router.get('/:id', ctrl.getConversation);
router.put('/:id', validate(updateConversationSchema), ctrl.updateConversation);
router.delete('/:id', ctrl.deleteConversation);

// --- Participants ---
router.post('/:id/participants', validate(addParticipantSchema), ctrl.addParticipant);
router.delete('/:id/participants/:uid', ctrl.removeParticipant);
router.get('/:id/participants', ctrl.listParticipants);
router.post('/:id/leave', ctrl.leaveConversation);

module.exports = router;
