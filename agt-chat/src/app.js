/**
 * Configuration de l'application Express.
 * Ordre des middlewares (CDC MIDDLEWARE CHAIN) :
 * requestLogger → cors → authMiddleware → capabilitiesMiddleware → [route handler] → errorHandler
 */
const express = require('express');
const swaggerUi = require('swagger-ui-express');
const swaggerSpec = require('./swagger');
const cors = require('cors');
const requestLogger = require('./common/middleware/requestLogger.middleware');
const errorHandler = require('./common/errors/errorHandler');
const authMiddleware = require('./common/middleware/auth.middleware');
const s2sMiddleware = require('./common/middleware/s2s.middleware');
const capabilitiesMiddleware = require('./common/middleware/capabilities.middleware');

// Routers
const conversationsRouter = require('./modules/conversations/conversations.routes');
const messagesRouter = require('./modules/messages/messages.routes');
const reactionsRouter = require('./modules/reactions/reactions.routes');
const transfersRouter = require('./modules/transfers/transfers.routes');
const capabilitiesRouter = require('./modules/capabilities/capabilities.routes');

// Controllers inline
const messagesCtrl = require('./modules/messages/messages.controller');
const { validate: validateMsg, markReadSchema } = require('./modules/messages/messages.validators');
const conversationsCtrl = require('./modules/conversations/conversations.controller');
const transfersCtrl = require('./modules/transfers/transfers.controller');
const { validate: validateTransfer, createTransferSchema } = require('./modules/transfers/transfers.validators');
const presenceRepo = require('./modules/presence/presence.repository');
const { success } = require('./common/utils/response');
const { ping: dbPing } = require('./common/db/pool');
const { ping: redisPing } = require('./common/cache/redis');
const { isConnected: rabbitConnected } = require('./common/broker/publisher');

const app = express();

// --- Middlewares globaux ---
app.use(requestLogger);
app.use(cors({
  origin: (process.env.SOCKET_IO_CORS_ORIGIN || 'http://localhost:3000').split(','),
  credentials: true,
}));
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: false }));

// --- Health check (public) ---
/**
 * @swagger
 * /health:
 *   get:
 *     summary: État du service
 *     tags: [Health]
 *     security: []
 *     responses:
 *       200:
 *         description: Service opérationnel
 *       503:
 *         description: Service dégradé
 */
app.get('/api/v1/chat/health', async (req, res) => {
  try {
    const [dbOk, redisOk] = await Promise.all([
      dbPing().catch(() => false),
      redisPing().catch(() => false),
    ]);
    const rabbitOk = rabbitConnected();
    const allOk = dbOk && redisOk && rabbitOk;
    return res.status(allOk ? 200 : 503).json({
      success: allOk,
      data: {
        status: allOk ? 'healthy' : 'degraded',
        database: dbOk ? 'ok' : 'error',
        redis: redisOk ? 'ok' : 'error',
        rabbitmq: rabbitOk ? 'ok' : 'error',
        uptime: process.uptime(),
        timestamp: new Date().toISOString(),
      },
    });
  } catch (err) {
    return res.status(503).json({ success: false, data: { status: 'error', message: err.message } });
  }
});

// Swagger UI
app.use('/api/v1/chat/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
  customSiteTitle: 'AGT Chat API',
  swaggerOptions: { persistAuthorization: true },
}));

// --- IMPORTANT : route S2S transfer AVANT le router conversations ---
// POST /conversations/transfer est S2S uniquement — doit être déclaré avant
// app.use('/conversations') pour éviter que Express le traite comme un ID
app.post('/api/v1/chat/conversations/transfer',
  s2sMiddleware,
  validateTransfer(createTransferSchema),
  transfersCtrl.createTransfer
);

// --- Routes conversations ---
app.use('/api/v1/chat/conversations', conversationsRouter);

// --- Routes messages ---
app.use('/api/v1/chat/conversations/:id/messages', messagesRouter);

// --- Read receipts ---
app.post('/api/v1/chat/conversations/:id/read',
  authMiddleware, capabilitiesMiddleware,
  validateMsg(markReadSchema),
  messagesCtrl.markRead
);
app.get('/api/v1/chat/conversations/:id/read-status',
  authMiddleware, capabilitiesMiddleware,
  messagesCtrl.getReadStatus
);

// --- Réactions ---
app.use('/api/v1/chat/messages/:msgId/reactions', reactionsRouter);

// --- Transfers (opérateurs + stats) ---
app.use('/api/v1/chat/transfers', transfersRouter);

// --- Canaux publics et présence ---
app.get('/api/v1/chat/platforms/:platformId/channels',
  authMiddleware, capabilitiesMiddleware,
  conversationsCtrl.listPublicChannels
);
app.post('/api/v1/chat/channels/:id/join',
  authMiddleware, capabilitiesMiddleware,
  conversationsCtrl.joinChannel
);

app.get('/api/v1/chat/users/:uid/presence', authMiddleware, async (req, res, next) => {
  try {
    const data = await presenceRepo.getPresence(req.params.uid);
    return success(res, { user_id: req.params.uid, ...data });
  } catch (err) { next(err); }
});

// --- Capabilities ---
app.use('/api/v1/chat/capabilities', capabilitiesRouter);

// --- Stats conversations ---
app.get('/api/v1/chat/conversations/stats', authMiddleware, conversationsCtrl.getStats);

// --- Handler d'erreurs global ---
app.use(errorHandler);

module.exports = app;
