/**
 * Rate limiting via Redis sliding window.
 * - Par utilisateur : RATE_LIMIT_USER_MSG_PER_MIN messages/min
 * - Par conversation : RATE_LIMIT_CONV_MSG_PER_MIN messages/min
 * Utilisé sur les endpoints d'envoi de messages.
 */
const { getRedis } = require('../cache/redis');
const AppError = require('../errors/AppError');

const USER_LIMIT = () => parseInt(process.env.RATE_LIMIT_USER_MSG_PER_MIN || '30', 10);
const CONV_LIMIT = () => parseInt(process.env.RATE_LIMIT_CONV_MSG_PER_MIN || '100', 10);

/**
 * Incrémente un compteur Redis et vérifie la limite.
 * Clé : rate:{scope}:{id}:{minute_bucket}
 * @param {string} key - Clé Redis unique pour ce bucket
 * @param {number} limit - Limite autorisée
 */
const checkLimit = async (key, limit) => {
  const redis = getRedis();
  const count = await redis.incr(key);
  if (count === 1) {
    // Expiration à 70s pour couvrir la fenêtre de 60s avec marge
    await redis.expire(key, 70);
  }
  if (count > limit) {
    throw new AppError('RATE_LIMIT_EXCEEDED', 'Trop de messages envoyés, veuillez patienter', 429);
  }
};

/**
 * Middleware de rate limiting pour l'envoi de messages.
 * Vérifie les deux limites (user + conversation).
 */
const rateLimitMessages = async (req, res, next) => {
  try {
    const userId = req.user?.user_id;
    const conversationId = req.params.id;
    const minuteBucket = Math.floor(Date.now() / 60000);

    if (userId) {
      await checkLimit(`rate:user:${userId}:${minuteBucket}`, USER_LIMIT());
    }
    if (conversationId) {
      await checkLimit(`rate:conv:${conversationId}:${minuteBucket}`, CONV_LIMIT());
    }
    next();
  } catch (err) {
    next(err);
  }
};

module.exports = { rateLimitMessages, checkLimit };
