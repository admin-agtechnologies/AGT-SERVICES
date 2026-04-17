/**
 * Repository messages — accès DB uniquement pour les messages et read_cursors.
 */
const { query } = require('../../common/db/pool');

/**
 * Persiste un nouveau message en base.
 * La persistance AVANT l'émission WebSocket est garantie par l'ordre des appels dans le service.
 * @param {object} params - { conversation_id, sender_id, content, parent_id, media_ids }
 * @returns {Promise<object>}
 */
const create = async (params) => {
  const result = await query(
    `INSERT INTO messages (conversation_id, sender_id, content, parent_id, media_ids)
     VALUES ($1, $2, $3, $4, $5) RETURNING *`,
    [params.conversation_id, params.sender_id, params.content, params.parent_id || null, params.media_ids || []]
  );
  return result.rows[0];
};

/**
 * Récupère un message par ID (incluant les supprimés pour les admins).
 * @param {string} id
 * @returns {Promise<object|null>}
 */
const findById = async (id) => {
  const result = await query('SELECT * FROM messages WHERE id = $1', [id]);
  return result.rows[0] || null;
};

/**
 * Liste les messages d'une conversation avec pagination cursor-based.
 * Ordre : du plus récent au plus ancien (DESC), puis inversé côté client.
 * @param {string} conversationId
 * @param {object} opts - { limit, cursor }
 * @returns {Promise<object[]>}
 */
const findByConversation = async (conversationId, opts = {}) => {
  const { limit = 50, cursor = null } = opts;
  const params = [conversationId, limit];
  let cursorClause = '';
  if (cursor) {
    cursorClause = ' AND created_at < $3';
    params.push(cursor);
  }
  const result = await query(
    `SELECT * FROM messages WHERE conversation_id = $1${cursorClause}
     ORDER BY created_at DESC LIMIT $2`,
    params
  );
  return result.rows;
};

/**
 * Édite le contenu d'un message (auteur uniquement, dans le délai configuré).
 * @param {string} id
 * @param {string} content
 * @returns {Promise<object>}
 */
const edit = async (id, content) => {
  const result = await query(
    'UPDATE messages SET content = $2, edited_at = NOW() WHERE id = $1 RETURNING *',
    [id, content]
  );
  return result.rows[0];
};

/**
 * Soft delete d'un message : content = null, is_deleted = true.
 * Le message reste en base pour préserver les threads de réponses.
 * @param {string} id
 * @returns {Promise<object>}
 */
const softDelete = async (id) => {
  const result = await query(
    'UPDATE messages SET is_deleted = true, content = NULL WHERE id = $1 RETURNING *',
    [id]
  );
  return result.rows[0];
};

/**
 * Recherche full-text dans les messages d'une conversation via index GIN.
 * La recherche reste locale au Chat (pas de Search Service — CDC §1.4).
 * @param {string} conversationId
 * @param {string} q - Terme recherché
 * @param {object} opts - { limit }
 * @returns {Promise<object[]>}
 */
const search = async (conversationId, q, opts = {}) => {
  const { limit = 20 } = opts;
  const result = await query(
    `SELECT *, ts_rank(to_tsvector('french', COALESCE(content, '')), plainto_tsquery('french', $2)) AS rank
     FROM messages
     WHERE conversation_id = $1
       AND is_deleted = false
       AND to_tsvector('french', COALESCE(content, '')) @@ plainto_tsquery('french', $2)
     ORDER BY rank DESC, created_at DESC
     LIMIT $3`,
    [conversationId, q, limit]
  );
  return result.rows;
};

/**
 * Upsert du curseur de lecture d'un utilisateur.
 * @param {string} conversationId
 * @param {string} userId
 * @param {string} messageId
 */
const upsertReadCursor = async (conversationId, userId, messageId) => {
  await query(
    `INSERT INTO read_cursors (conversation_id, user_id, last_read_message_id, updated_at)
     VALUES ($1, $2, $3, NOW())
     ON CONFLICT (conversation_id, user_id)
     DO UPDATE SET last_read_message_id = $3, updated_at = NOW()`,
    [conversationId, userId, messageId]
  );
};

/**
 * Récupère les curseurs de lecture de tous les participants.
 * @param {string} conversationId
 * @returns {Promise<object[]>}
 */
const findReadCursors = async (conversationId) => {
  const result = await query(
    'SELECT * FROM read_cursors WHERE conversation_id = $1',
    [conversationId]
  );
  return result.rows;
};

module.exports = { create, findById, findByConversation, edit, softDelete, search, upsertReadCursor, findReadCursors };
