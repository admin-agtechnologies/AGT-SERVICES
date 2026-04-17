/**
 * Client HTTP vers le Service Auth v2.1.
 * Gère la vérification JWT et l'introspection S2S.
 * Cache Redis TTL AUTH_CACHE_TTL_SEC (défaut 30s) pour éviter de surcharger Auth.
 */
const axios = require("axios");
const { getRedis } = require("../cache/redis");
const AppError = require("../errors/AppError");
const logger = require("../utils/logger");

const AUTH_URL = () => process.env.AUTH_SERVICE_URL || "http://localhost:7000";
const CACHE_TTL = () => parseInt(process.env.AUTH_CACHE_TTL_SEC || "30", 10);

/**
 * Vérifie un JWT utilisateur auprès du Service Auth.
 * Retourne les claims du token : { user_id, platform_id, roles, ... }
 * @param {string} token - Bearer token
 * @returns {Promise<object>} Claims du token
 */
const verifyToken = async (token) => {
  const redis = getRedis();
  const cacheKey = `auth_token:${token}`;

  // Vérifier le cache d'abord
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  try {
    const { data } = await axios.get(`${AUTH_URL()}/api/v1/auth/verify-token`, {
      headers: { Authorization: `Bearer ${token}` },
      timeout: 5000,
    });
    // Mettre en cache pour réduire les appels Auth
    await redis.set(cacheKey, JSON.stringify(data), "EX", CACHE_TTL());
    return data;
  } catch (err) {
    if (err.response?.status === 401) {
      throw new AppError("UNAUTHORIZED", "Token invalide ou expiré", 401);
    }
    logger.error({ err }, "Auth service error during token verification");
    throw new AppError("UNAUTHORIZED", "Impossible de vérifier le token", 401);
  }
};

const getSelfS2SToken = async () => {
  const redis = getRedis();
  const cached = await redis.get("chat:self_s2s_token");
  if (cached) return cached;

  const resp = await axios.post(
    `${AUTH_URL()}/api/v1/auth/s2s/token`,
    {
      client_id: process.env.S2S_CLIENT_ID,
      client_secret: process.env.S2S_CLIENT_SECRET,
    },
    { timeout: 5000 },
  );

  const { access_token, expires_in } = resp.data;
  await redis.set("chat:self_s2s_token", access_token, "EX", expires_in - 60);
  return access_token;
};

const introspectS2S = async (token) => {
  const selfToken = await getSelfS2SToken();
  const { data } = await axios.post(
    `${AUTH_URL()}/api/v1/auth/s2s/introspect`,
    { token },
    {
      headers: { Authorization: `Bearer ${selfToken}` },
      timeout: 5000,
    },
  );
  return data;
};

module.exports = { verifyToken, introspectS2S, getSelfS2SToken };
