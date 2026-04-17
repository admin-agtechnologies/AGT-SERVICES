/**
 * Repository présence — Redis uniquement.
 * La présence n'est JAMAIS persistée en base (CDC §5.3.2).
 * Clés Redis :
 *   presence:{user_id} → JSON { status, last_seen_at }  TTL 60s
 *   typing:{conversation_id}:{user_id} → "1"             TTL TYPING_TIMEOUT_MS
 */
const { getRedis } = require('../../common/cache/redis');

const PRESENCE_TTL = 60; // secondes

/**
 * Met à jour le statut de présence d'un utilisateur.
 * @param {string} userId
 * @param {'online'|'away'|'offline'} status
 */
const setPresence = async (userId, status) => {
  const redis = getRedis();
  const data = { status, last_seen_at: new Date().toISOString() };
  await redis.set(`presence:${userId}`, JSON.stringify(data), 'EX', PRESENCE_TTL);
};

/**
 * Récupère le statut de présence d'un utilisateur.
 * @param {string} userId
 * @returns {Promise<object>}
 */
const getPresence = async (userId) => {
  const redis = getRedis();
  const data = await redis.get(`presence:${userId}`);
  if (data) return JSON.parse(data);
  return { status: 'offline', last_seen_at: null };
};

/**
 * Renouvelle le TTL de présence (heartbeat).
 * @param {string} userId
 */
const heartbeat = async (userId) => {
  const redis = getRedis();
  const current = await getPresence(userId);
  const data = { status: current.status === 'offline' ? 'online' : current.status, last_seen_at: new Date().toISOString() };
  await redis.set(`presence:${userId}`, JSON.stringify(data), 'EX', PRESENCE_TTL);
  return data;
};

/**
 * Démarre l'indicateur "en train d'écrire".
 * @param {string} conversationId
 * @param {string} userId
 */
const startTyping = async (conversationId, userId) => {
  const redis = getRedis();
  const ttl = Math.ceil(parseInt(process.env.TYPING_TIMEOUT_MS || '3000', 10) / 1000);
  await redis.set(`typing:${conversationId}:${userId}`, '1', 'EX', ttl);
};

/**
 * Arrête l'indicateur "en train d'écrire".
 * @param {string} conversationId
 * @param {string} userId
 */
const stopTyping = async (conversationId, userId) => {
  const redis = getRedis();
  await redis.del(`typing:${conversationId}:${userId}`);
};

module.exports = { setPresence, getPresence, heartbeat, startTyping, stopTyping };
