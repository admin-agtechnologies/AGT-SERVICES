const express = require('express');
const router = express.Router();
const authMiddleware = require('../../common/middleware/auth.middleware');
const capabilitiesController = require('./capabilities.controller');

// GET /api/v1/chat/capabilities/:platformId — JWT ou S2S
router.get('/:platformId', authMiddleware, capabilitiesController.getCapabilities);

// PUT /api/v1/chat/capabilities/:platformId — admin uniquement (vérifié dans le controller)
router.put('/:platformId', authMiddleware, capabilitiesController.updateCapabilities);

module.exports = router;
