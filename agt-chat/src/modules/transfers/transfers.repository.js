/**
 * Repository transfers — accès DB pour les transferts bot→humain.
 */
const { query } = require('../../common/db/pool');

/**
 * Crée un transfert (S2S uniquement).
 * @param {object} params - { conversation_id, user_id, bot_history, context }
 * @returns {Promise<object>}
 */
const create = async (params) => {
  const result = await query(
    `INSERT INTO transfers (conversation_id, user_id, bot_history, context)
     VALUES ($1, $2, $3, $4) RETURNING *`,
    [params.conversation_id, params.user_id, JSON.stringify(params.bot_history || []), JSON.stringify(params.context || {})]
  );
  return result.rows[0];
};

/**
 * Récupère un transfert par ID.
 * @param {string} id
 * @returns {Promise<object|null>}
 */
const findById = async (id) => {
  const result = await query('SELECT * FROM transfers WHERE id = $1', [id]);
  return result.rows[0] || null;
};

/**
 * Liste les transferts en attente (file d'attente opérateurs).
 * @param {string} [platformId]
 * @returns {Promise<object[]>}
 */
const findPending = async (platformId = null) => {
  if (platformId) {
    const result = await query(
      `SELECT t.* FROM transfers t
       JOIN conversations c ON c.id = t.conversation_id
       WHERE t.status = 'pending' AND c.platform_id = $1
       ORDER BY t.created_at ASC`,
      [platformId]
    );
    return result.rows;
  }
  const result = await query(
    "SELECT * FROM transfers WHERE status = 'pending' ORDER BY created_at ASC"
  );
  return result.rows;
};

/**
 * Prise en charge avec verrou optimiste.
 * UPDATE conditionnel : ne met à jour que si status = 'pending'.
 * Retourne null si déjà pris (409 côté service).
 * @param {string} id
 * @param {string} operatorId
 * @returns {Promise<object|null>}
 */
const takeOptimistic = async (id, operatorId) => {
  const result = await query(
    `UPDATE transfers
     SET status = 'taken', operator_id = $2, taken_at = NOW()
     WHERE id = $1 AND status = 'pending'
     RETURNING *`,
    [id, operatorId]
  );
  return result.rows[0] || null;
};

/**
 * Ferme un transfert.
 * @param {string} id
 * @param {string} operatorId - Doit correspondre à l'opérateur ayant pris en charge
 * @returns {Promise<object|null>}
 */
const close = async (id, operatorId) => {
  const result = await query(
    `UPDATE transfers
     SET status = 'closed', closed_at = NOW()
     WHERE id = $1 AND operator_id = $2 AND status = 'taken'
     RETURNING *`,
    [id, operatorId]
  );
  return result.rows[0] || null;
};

/**
 * Remet en attente les transferts expirés (job périodique).
 * @param {number} timeoutMinutes
 * @returns {Promise<number>} Nombre de transferts remis en attente
 */
const requeueTimedOut = async (timeoutMinutes) => {
  const result = await query(
    `UPDATE transfers
     SET status = 'pending', operator_id = NULL, taken_at = NULL
     WHERE status = 'taken'
       AND taken_at < NOW() - INTERVAL '${timeoutMinutes} minutes'
     RETURNING id`
  );
  return result.rowCount;
};

/**
 * Stats agrégées pour admin/S2S.
 * @returns {Promise<object>}
 */
const getStats = async () => {
  const result = await query(
    `SELECT
       COUNT(*) FILTER (WHERE status = 'pending') AS pending_count,
       COUNT(*) FILTER (WHERE status = 'taken') AS taken_count,
       COUNT(*) FILTER (WHERE status = 'closed') AS closed_count,
       COUNT(*) AS total,
       AVG(EXTRACT(EPOCH FROM (taken_at - created_at))/60) FILTER (WHERE taken_at IS NOT NULL) AS avg_wait_minutes
     FROM transfers`
  );
  return result.rows[0];
};

module.exports = { create, findById, findPending, takeOptimistic, close, requeueTimedOut, getStats };
