/**
 * Service capabilities — source de vérité pour toutes les feature flags et limites.
 * AUCUN autre service ne définit ses propres quotas (CDC §5.1).
 * Cache Redis pour éviter une requête DB à chaque action.
 */
const capabilitiesRepo = require('./capabilities.repository');
const { getRedis } = require('../../common/cache/redis');
const AppError = require('../../common/errors/AppError');
const logger = require('../../common/utils/logger');

const CACHE_TTL = 60; // 60s : acceptable pour des feature flags rarement modifiés

/**
 * Valeurs par défaut (CDC §8 — table platform_capabilities).
 * Retournées si une plateforme n'a pas encore de config.
 */
const getDefaults = () => ({
  direct_enabled: true,
  channels_enabled: true,
  read_receipts_enabled: true,
  typing_enabled: true,
  presence_enabled: true,
  reactions_enabled: true,
  transfer_enabled: false,
  message_edit_enabled: true,
  message_delete_enabled: true,
  message_search_enabled: true,
  attachments_enabled: false,
  max_message_length: 4096,
  rate_limit_per_user: 30,
  rate_limit_per_conv: 100,
  max_channel_members: 500,
});

/**
 * Récupère les capabilities d'une plateforme avec cache Redis.
 * Si la plateforme est inconnue, retourne les valeurs par défaut.
 * @param {string} platformId
 * @returns {Promise<object>}
 */
const getCapabilities = async (platformId) => {
  const redis = getRedis();
  const cacheKey = `capabilities:${platformId}`;

  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const row = await capabilitiesRepo.findByPlatformId(platformId);
  const caps = row ? { ...getDefaults(), ...row } : getDefaults();

  await redis.set(cacheKey, JSON.stringify(caps), 'EX', CACHE_TTL);
  return caps;
};

/**
 * Met à jour les capabilities d'une plateforme (admin uniquement).
 * Invalide le cache Redis après la mise à jour.
 * @param {string} platformId
 * @param {object} updates - Champs à modifier
 * @returns {Promise<object>}
 */
const updateCapabilities = async (platformId, updates) => {
  // Filtrer pour n'accepter que les champs connus
  const allowed = Object.keys(getDefaults());
  const sanitized = Object.fromEntries(
    Object.entries(updates).filter(([k]) => allowed.includes(k))
  );

  if (Object.keys(sanitized).length === 0) {
    throw new AppError('VALIDATION_ERROR', 'Aucun champ valide à mettre à jour', 400);
  }

  const result = await capabilitiesRepo.upsert(platformId, sanitized);

  // Invalider le cache pour forcer un rechargement à la prochaine requête
  const redis = getRedis();
  await redis.del(`capabilities:${platformId}`);

  logger.info({ platformId, updates: sanitized }, 'Capabilities updated');
  return { ...getDefaults(), ...result };
};

/**
 * Vérifie qu'une feature est activée, lance une AppError 403 sinon.
 * @param {object} capabilities - Objet capabilities de la plateforme
 * @param {string} feature - Nom de la feature (ex: 'reactions_enabled')
 */
const requireFeature = (capabilities, feature) => {
  if (!capabilities || capabilities[feature] === false) {
    throw new AppError('FEATURE_DISABLED', `La fonctionnalité '${feature}' est désactivée pour cette plateforme`, 403);
  }
};

module.exports = { getCapabilities, updateCapabilities, getDefaults, requireFeature };
