/**
 * Repository réactions — accès DB pour les réactions emoji.
 */
const { query } = require('../../common/db/pool');

/**
 * Ajoute une réaction (idempotent via ON CONFLICT DO NOTHING).
 * @param {string} messageId
 * @param {string} userId
 * @param {string} emoji
 * @returns {Promise<object>}
 */
const add = async (messageId, userId, emoji) => {
  const result = await query(
    `INSERT INTO message_reactions (message_id, user_id, emoji)
     VALUES ($1, $2, $3)
     ON CONFLICT (message_id, user_id, emoji) DO NOTHING
     RETURNING *`,
    [messageId, userId, emoji]
  );
  return result.rows[0] || null;
};

/**
 * Retire une réaction.
 * @param {string} messageId
 * @param {string} userId
 * @param {string} emoji
 */
const remove = async (messageId, userId, emoji) => {
  await query(
    'DELETE FROM message_reactions WHERE message_id = $1 AND user_id = $2 AND emoji = $3',
    [messageId, userId, emoji]
  );
};

/**
 * Liste les réactions d'un message, groupées par emoji avec compteurs.
 * @param {string} messageId
 * @returns {Promise<object[]>} [{ emoji, count, users: [userId, ...] }]
 */
const findByMessage = async (messageId) => {
  const result = await query(
    `SELECT emoji, COUNT(*) AS count, array_agg(user_id) AS users
     FROM message_reactions WHERE message_id = $1
     GROUP BY emoji ORDER BY count DESC`,
    [messageId]
  );
  return result.rows;
};

module.exports = { add, remove, findByMessage };
