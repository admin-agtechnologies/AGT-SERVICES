/**
 * Controller capabilities — handlers HTTP uniquement.
 * Validation, appel service, formatage réponse.
 */
const capabilitiesService = require('./capabilities.service');
const { checkPermission } = require('../../common/clients/usersClient');
const AppError = require('../../common/errors/AppError');
const { success } = require('../../common/utils/response');

/**
 * GET /api/v1/chat/capabilities/:platformId
 * Lecture libre pour tout token JWT ou S2S valide de la plateforme.
 */
const getCapabilities = async (req, res, next) => {
  try {
    const { platformId } = req.params;
    const caps = await capabilitiesService.getCapabilities(platformId);
    return success(res, caps);
  } catch (err) {
    next(err);
  }
};

/**
 * PUT /api/v1/chat/capabilities/:platformId
 * Écriture réservée aux admins (JWT + permission chat:admin via Users, ou S2S admin).
 */
const updateCapabilities = async (req, res, next) => {
  try {
    const { platformId } = req.params;
    const userId = req.user?.user_id;

    // Vérifier la permission chat:admin via Users (fail-closed)
    const isAdmin = await checkPermission(userId, 'chat:admin', platformId);
    if (!isAdmin) {
      throw new AppError('FORBIDDEN', 'Permission chat:admin requise', 403);
    }

    const updated = await capabilitiesService.updateCapabilities(platformId, req.body);
    return success(res, updated);
  } catch (err) {
    next(err);
  }
};

module.exports = { getCapabilities, updateCapabilities };
