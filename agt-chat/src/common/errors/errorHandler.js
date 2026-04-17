/**
 * Handler global d'erreurs Express.
 * Intercepte toutes les erreurs non gérées et les formate selon CDC §4.1.
 * Doit être enregistré en DERNIER middleware dans app.js.
 */
const AppError = require('./AppError');
const logger = require('../utils/logger');

const errorHandler = (err, req, res, next) => { // eslint-disable-line no-unused-vars
  // Erreur métier connue
  if (err instanceof AppError) {
    logger.warn({ code: err.code, path: req.path, method: req.method }, err.message);
    return res.status(err.httpStatus).json({
      success: false,
      error: { code: err.code, message: err.message },
    });
  }

  // Erreurs de validation Joi
  if (err.name === 'ValidationError' || err.isJoi) {
    return res.status(400).json({
      success: false,
      error: { code: 'VALIDATION_ERROR', message: err.message },
    });
  }

  // Erreur inattendue — log complet mais réponse générique en prod
  logger.error({ err, path: req.path, method: req.method }, 'Unexpected error');
  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production' ? 'Une erreur interne est survenue' : err.message,
    },
  });
};

module.exports = errorHandler;
