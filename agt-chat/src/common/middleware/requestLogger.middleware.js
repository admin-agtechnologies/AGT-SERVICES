/**
 * Middleware de logging structuré des requêtes HTTP.
 * Log : method, path, status, durée en ms, user_id si disponible.
 */
const logger = require('../utils/logger');

const requestLogger = (req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    logger.info({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      ms: Date.now() - start,
      user_id: req.user?.user_id || null,
    }, 'HTTP request');
  });
  next();
};

module.exports = requestLogger;
