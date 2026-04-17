/**
 * Middleware d'authentification JWT pour le handshake WebSocket.
 * Exécuté une seule fois à la connexion — résultat stocké dans socket.data.
 * Le token peut être passé via :
 *   - Query param : ?token=...
 *   - Header Authorization: Bearer ...
 */
const { verifyToken } = require('../common/clients/authClient');
const capabilitiesService = require('../modules/capabilities/capabilities.service');
const logger = require('../common/utils/logger');

const socketAuthMiddleware = async (socket, next) => {
  try {
    // Extraire le token depuis query param ou header
    const token =
      socket.handshake.query?.token ||
      socket.handshake.auth?.token ||
      socket.handshake.headers?.authorization?.replace('Bearer ', '');

    if (!token) {
      return next(new Error('UNAUTHORIZED: Token manquant'));
    }

    // Valider le token via Auth Service (avec cache Redis)
    const claims = await verifyToken(token);
    socket.data.user = claims;
    socket.data.user_id = claims.user_id;
    socket.data.platform_id = claims.platform_id;

    // Charger les capabilities de la plateforme une fois au handshake
    socket.data.capabilities = await capabilitiesService.getCapabilities(claims.platform_id);

    logger.info({ user_id: claims.user_id, platform_id: claims.platform_id }, 'WebSocket connected');
    next();
  } catch (err) {
    logger.warn({ err: err.message }, 'WebSocket auth failed');
    next(new Error('UNAUTHORIZED: ' + err.message));
  }
};

module.exports = socketAuthMiddleware;
