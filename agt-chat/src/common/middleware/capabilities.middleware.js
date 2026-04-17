/**
 * Middleware capabilities : charge les capacités de la plateforme et les injecte dans req.capabilities.
 * Utilisé sur toutes les routes authentifiées.
 * La plateforme est extraite du JWT (req.user.platform_id).
 */
const capabilitiesService = require('../../modules/capabilities/capabilities.service');
const logger = require('../utils/logger');

const capabilitiesMiddleware = async (req, res, next) => {
  try {
    const platformId = req.user?.platform_id;
    if (!platformId) {
      // Pas de plateforme (ex: route health) → capabilities vides
      req.capabilities = null;
      return next();
    }
    req.capabilities = await capabilitiesService.getCapabilities(platformId);
    next();
  } catch (err) {
    logger.warn({ err }, 'Failed to load capabilities — using defaults');
    req.capabilities = capabilitiesService.getDefaults();
    next();
  }
};

module.exports = capabilitiesMiddleware;
