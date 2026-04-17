const express = require('express');
const router = express.Router();
const authMiddleware = require('../../common/middleware/auth.middleware');
const ctrl = require('./transfers.controller');

// Ces routes sont montées sur /api/v1/chat/transfers
// La route POST (création) est montée directement dans app.js avec s2sMiddleware

// GET /transfers/pending — opérateurs authentifiés
router.get('/pending', authMiddleware, ctrl.getPendingTransfers);

// GET /transfers/stats — admin/S2S
router.get('/stats', authMiddleware, ctrl.getStats);

// POST /transfers/:id/take — opérateur avec permission chat:transfer:take
router.post('/:id/take', authMiddleware, ctrl.takeTransfer);

// POST /transfers/:id/close — opérateur assigné uniquement
router.post('/:id/close', authMiddleware, ctrl.closeTransfer);

module.exports = router;
