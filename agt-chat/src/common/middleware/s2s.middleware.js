/**
 * Middleware d'authentification S2S (Service-to-Service).
 * Utilisé sur les routes réservées aux services internes :
 * - POST /conversations/transfer (Chatbot → Chat)
 * - GET /conversations/stats, GET /transfers/stats
 * Injecte req.s2s = { service, ... }
 */
const { introspectS2S } = require('../clients/authClient');
const AppError = require('../errors/AppError');

const s2sMiddleware = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      throw new AppError('UNAUTHORIZED', 'Token S2S manquant', 401);
    }
    const token = authHeader.slice(7);
    const result = await introspectS2S(token);

    if (!result || !result.active) {
      throw new AppError('UNAUTHORIZED', 'Token S2S invalide', 401);
    }

    req.s2s = result;
    next();
  } catch (err) {
    next(err);
  }
};

module.exports = s2sMiddleware;
