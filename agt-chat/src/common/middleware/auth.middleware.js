/**
 * Middleware d'authentification JWT pour les routes REST.
 * Vérifie le token Bearer via GET /auth/verify-token (avec cache Redis).
 * Injecte req.user = { user_id, platform_id, roles, ... }
 */
const { verifyToken } = require('../clients/authClient');
const AppError = require('../errors/AppError');

const authMiddleware = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      throw new AppError('UNAUTHORIZED', 'Token manquant ou malformé', 401);
    }
    const token = authHeader.slice(7);
    const claims = await verifyToken(token);
    req.user = claims;
    next();
  } catch (err) {
    next(err);
  }
};

module.exports = authMiddleware;
