/**
 * Client HTTP vers le Service Users v1.0.
 * Récupère les profils et vérifie les permissions.
 *
 * IMPORTANT (CDC §10.3) :
 * - Chat travaille avec users_auth.id (= sub du JWT)
 * - Notification attend users_profiles.id
 * - Ce client retourne les deux pour permettre le mapping
 *
 * Cache Redis :
 * - Profils : TTL USERS_CACHE_TTL_SEC (défaut 300s)
 * - Permissions : TTL 30s (données critiques)
 */
const axios = require("axios");
const { getSelfS2SToken } = require("./authClient");
const { getRedis } = require("../cache/redis");
const logger = require("../utils/logger");

const USERS_URL = () =>
  process.env.USERS_SERVICE_URL || "http://localhost:7001";
const PROFILE_TTL = () =>
  parseInt(process.env.USERS_CACHE_TTL_SEC || "300", 10);
const PERMS_TTL = 30;

// Token S2S pour appels inter-services
const s2sHeaders = async () => {
  const token = await getSelfS2SToken();
  return { Authorization: `Bearer ${token}` };
};

/**
 * Récupère le profil d'un utilisateur par son users_auth.id.
 * En cas d'erreur Users, retourne un profil minimal plutôt que de bloquer (fail-open sur profil).
 * @param {string} authUserId - users_auth.id
 * @returns {Promise<object>} { id (users_auth.id), profiles_id (users_profiles.id), first_name, last_name, avatar_url, ... }
 */
const getUserProfile = async (authUserId) => {
  const redis = getRedis();
  const cacheKey = `user_profile:${authUserId}`;

  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  try {
    const { data } = await axios.get(
      `${USERS_URL()}/api/v1/users/by-auth/${authUserId}`,
      { headers: await s2sHeaders(), timeout: 5000 },
    );
    const profile = data.data || data;
    await redis.set(cacheKey, JSON.stringify(profile), "EX", PROFILE_TTL());
    return profile;
  } catch (err) {
    logger.warn(
      { authUserId, err: err.message },
      "Users service unavailable — returning fallback profile",
    );
    // Fail-open sur profil : retourne un profil minimal pour ne pas bloquer l'affichage
    return {
      id: authUserId,
      first_name: "Utilisateur",
      last_name: "inconnu",
      avatar_url: null,
    };
  }
};

/**
 * Vérifie si un utilisateur possède une permission donnée sur une plateforme.
 * Fail-closed : en cas d'erreur Users, REFUSE la permission (sécurité).
 * @param {string} authUserId - users_auth.id
 * @param {string} permission - Ex: 'chat:transfer:take', 'chat:admin'
 * @param {string} [platformId] - Contexte de la plateforme
 * @returns {Promise<boolean>}
 */
const checkPermission = async (authUserId, permission, platformId = null) => {
  const redis = getRedis();
  const cacheKey = `user_perm:${authUserId}:${permission}:${platformId}`;

  const cached = await redis.get(cacheKey);
  if (cached !== null) return cached === "true";

  try {
    const profile = await getUserProfile(authUserId);
    const profilesId = profile?.id || authUserId;
    logger.info(
      { authUserId, profilesId, permission, platformId },
      "checkPermission — URL appelée",
    );
    const params = platformId
      ? `?platform_id=${platformId}&permission=${permission}`
      : `?permission=${permission}`;
    const { data } = await axios.get(
      `${USERS_URL()}/api/v1/users/${profilesId}/permissions/check${params}`,
      { headers: await s2sHeaders(), timeout: 5000 },
    );
    const hasPermission =
      data.data?.granted === true || data.granted === true;
    await redis.set(cacheKey, String(hasPermission), "EX", PERMS_TTL);
    return hasPermission;
  } catch (err) {
    // Fail-closed sur permissions : refus en cas d'erreur (sécurité)
    logger.warn(
      { authUserId, permission, err: err.message },
      "Users service error — denying permission (fail-closed)",
    );
    return false;
  }
};

/**
 * Résout le users_profiles.id à partir du users_auth.id.
 * Nécessaire pour appeler le Service Notification (qui attend profiles.id).
 * @param {string} authUserId - users_auth.id
 * @returns {Promise<string|null>} users_profiles.id ou null
 */
const resolveProfilesId = async (authUserId) => {
  const profile = await getUserProfile(authUserId);
  return profile?.profiles_id || profile?.profile_id || null;
};

module.exports = { getUserProfile, checkPermission, resolveProfilesId };
