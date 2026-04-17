/**
 * Repository conversations — toutes les requêtes SQL relatives aux conversations.
 * Aucune logique métier ici, uniquement des accès DB nommés et paramétrés.
 */
const { query, getClient } = require('../../common/db/pool');

/**
 * Crée une conversation et ses participants dans une transaction.
 * @param {object} params - { type, platform_id, name, description, is_public, created_by, metadata }
 * @param {string[]} participantIds - Liste des users_auth.id à ajouter
 * @returns {Promise<object>} Conversation créée
 */
const createWithParticipants = async (params, participantIds) => {
  const client = await getClient();
  try {
    await client.query('BEGIN');

    const convResult = await client.query(
      `INSERT INTO conversations (type, platform_id, name, description, is_public, created_by, metadata)
       VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *`,
      [params.type, params.platform_id, params.name || null, params.description || null,
       params.is_public || false, params.created_by, params.metadata || {}]
    );
    const conversation = convResult.rows[0];

    // Ajouter le créateur comme owner + les autres comme members
    for (const userId of participantIds) {
      const role = userId === params.created_by ? 'owner' : 'member';
      await client.query(
        `INSERT INTO conversation_participants (conversation_id, user_id, role)
         VALUES ($1, $2, $3) ON CONFLICT (conversation_id, user_id) DO NOTHING`,
        [conversation.id, userId, role]
      );
    }

    await client.query('COMMIT');
    return conversation;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
};

/**
 * Recherche une conversation directe existante entre deux utilisateurs sur une plateforme.
 * Anti-doublon CDC §5.1.1.
 * @param {string} userId1
 * @param {string} userId2
 * @param {string} platformId
 * @returns {Promise<object|null>}
 */
const findDirectBetween = async (userId1, userId2, platformId) => {
  const result = await query(
    `SELECT c.* FROM conversations c
     JOIN conversation_participants p1 ON p1.conversation_id = c.id AND p1.user_id = $1
     JOIN conversation_participants p2 ON p2.conversation_id = c.id AND p2.user_id = $2
     WHERE c.type = 'direct' AND c.platform_id = $3 AND c.deleted_at IS NULL
       AND p1.left_at IS NULL AND p2.left_at IS NULL
     LIMIT 1`,
    [userId1, userId2, platformId]
  );
  return result.rows[0] || null;
};

/**
 * Liste les conversations d'un utilisateur (paginées, triées par dernière activité).
 * @param {string} userId - users_auth.id
 * @param {string} platformId
 * @param {object} opts - { limit, cursor, type }
 * @returns {Promise<object[]>}
 */
const findByUser = async (userId, platformId, opts = {}) => {
  const { limit = 20, cursor = null, type = null } = opts;
  const params = [userId, platformId, limit];
  let whereExtra = '';
  let cursorClause = '';
  let paramIdx = 4;

  if (type) {
    whereExtra += ` AND c.type = $${paramIdx++}`;
    params.push(type);
  }
  if (cursor) {
    cursorClause = ` AND c.updated_at < $${paramIdx++}`;
    params.push(cursor);
  }

  const result = await query(
    `SELECT c.* FROM conversations c
     JOIN conversation_participants p ON p.conversation_id = c.id
     WHERE p.user_id = $1 AND c.platform_id = $2 AND c.deleted_at IS NULL AND p.left_at IS NULL
     ${whereExtra}${cursorClause}
     ORDER BY c.updated_at DESC
     LIMIT $3`,
    params
  );
  return result.rows;
};

/**
 * Récupère une conversation par ID.
 * @param {string} id
 * @returns {Promise<object|null>}
 */
const findById = async (id) => {
  const result = await query('SELECT * FROM conversations WHERE id = $1 AND deleted_at IS NULL', [id]);
  return result.rows[0] || null;
};

/**
 * Soft delete d'une conversation.
 * @param {string} id
 * @returns {Promise<object>}
 */
const softDelete = async (id) => {
  const result = await query(
    'UPDATE conversations SET deleted_at = NOW(), updated_at = NOW() WHERE id = $1 RETURNING *',
    [id]
  );
  return result.rows[0];
};

/**
 * Met à jour les métadonnées d'un canal (nom, description, visibilité).
 * @param {string} id
 * @param {object} fields
 * @returns {Promise<object>}
 */
const update = async (id, fields) => {
  const allowed = ['name', 'description', 'is_public', 'metadata'];
  const keys = Object.keys(fields).filter((k) => allowed.includes(k));
  if (keys.length === 0) return findById(id);
  const values = keys.map((k) => fields[k]);
  const setClauses = keys.map((k, i) => `${k} = $${i + 2}`).join(', ');
  const result = await query(
    `UPDATE conversations SET ${setClauses}, updated_at = NOW() WHERE id = $1 RETURNING *`,
    [id, ...values]
  );
  return result.rows[0];
};

/**
 * Touch updated_at pour remonter la conversation dans la liste.
 * @param {string} id
 */
const touch = async (id) => {
  await query('UPDATE conversations SET updated_at = NOW() WHERE id = $1', [id]);
};

/**
 * Ajoute un participant à une conversation.
 * @param {string} conversationId
 * @param {string} userId
 * @param {string} [role='member']
 * @returns {Promise<object>}
 */
const addParticipant = async (conversationId, userId, role = 'member') => {
  const result = await query(
    `INSERT INTO conversation_participants (conversation_id, user_id, role)
     VALUES ($1, $2, $3)
     ON CONFLICT (conversation_id, user_id) DO UPDATE SET left_at = NULL, role = $3
     RETURNING *`,
    [conversationId, userId, role]
  );
  return result.rows[0];
};

/**
 * Retire un participant (left_at = NOW()).
 * @param {string} conversationId
 * @param {string} userId
 */
const removeParticipant = async (conversationId, userId) => {
  await query(
    'UPDATE conversation_participants SET left_at = NOW() WHERE conversation_id = $1 AND user_id = $2',
    [conversationId, userId]
  );
};

/**
 * Liste les participants actifs d'une conversation.
 * @param {string} conversationId
 * @returns {Promise<object[]>}
 */
const findParticipants = async (conversationId) => {
  const result = await query(
    'SELECT * FROM conversation_participants WHERE conversation_id = $1 AND left_at IS NULL',
    [conversationId]
  );
  return result.rows;
};

/**
 * Vérifie qu'un utilisateur est participant actif d'une conversation.
 * @param {string} conversationId
 * @param {string} userId
 * @returns {Promise<object|null>} L'entrée participant ou null
 */
const findParticipant = async (conversationId, userId) => {
  const result = await query(
    'SELECT * FROM conversation_participants WHERE conversation_id = $1 AND user_id = $2 AND left_at IS NULL',
    [conversationId, userId]
  );
  return result.rows[0] || null;
};

/**
 * Compte les participants actifs.
 * @param {string} conversationId
 * @returns {Promise<number>}
 */
const countParticipants = async (conversationId) => {
  const result = await query(
    'SELECT COUNT(*) FROM conversation_participants WHERE conversation_id = $1 AND left_at IS NULL',
    [conversationId]
  );
  return parseInt(result.rows[0].count, 10);
};

/**
 * Liste les canaux publics d'une plateforme.
 * @param {string} platformId
 * @param {object} opts - { limit, cursor }
 * @returns {Promise<object[]>}
 */
const findPublicChannels = async (platformId, opts = {}) => {
  const { limit = 20, cursor = null } = opts;
  const params = [platformId, limit];
  let cursorClause = '';
  if (cursor) {
    cursorClause = ` AND c.updated_at < $3`;
    params.push(cursor);
  }
  const result = await query(
    `SELECT c.* FROM conversations c
     WHERE c.platform_id = $1 AND c.type = 'channel' AND c.is_public = true AND c.deleted_at IS NULL
     ${cursorClause}
     ORDER BY c.updated_at DESC LIMIT $2`,
    params
  );
  return result.rows;
};

/**
 * Stats agrégées pour admin/S2S.
 * @param {string} [platformId]
 * @returns {Promise<object>}
 */
const getStats = async (platformId = null) => {
  const filter = platformId ? 'WHERE platform_id = $1 AND deleted_at IS NULL' : 'WHERE deleted_at IS NULL';
  const params = platformId ? [platformId] : [];
  const result = await query(
    `SELECT
       COUNT(*) FILTER (WHERE type = 'direct') AS direct_count,
       COUNT(*) FILTER (WHERE type = 'channel') AS channel_count,
       COUNT(*) FILTER (WHERE type = 'transfer') AS transfer_count,
       COUNT(*) AS total
     FROM conversations ${filter}`,
    params
  );
  return result.rows[0];
};

module.exports = {
  createWithParticipants, findDirectBetween, findByUser, findById,
  softDelete, update, touch, addParticipant, removeParticipant,
  findParticipants, findParticipant, countParticipants, findPublicChannels, getStats,
};
