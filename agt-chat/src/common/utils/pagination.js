/**
 * Helper pour la pagination cursor-based.
 * Le curseur est le created_at du dernier élément encodé en base64.
 * Ce mécanisme est plus stable que l'offset pour des données qui changent fréquemment.
 */

/**
 * Encode un curseur à partir d'un timestamp ISO8601.
 * @param {string} createdAt - Timestamp du dernier élément
 * @returns {string} Curseur encodé en base64
 */
const encodeCursor = (createdAt) => {
  return Buffer.from(createdAt).toString('base64');
};

/**
 * Décode un curseur base64 en timestamp.
 * @param {string} cursor - Curseur encodé
 * @returns {string|null} Timestamp ou null si invalide
 */
const decodeCursor = (cursor) => {
  try {
    return Buffer.from(cursor, 'base64').toString('utf8');
  } catch {
    return null;
  }
};

/**
 * Construit l'objet pagination à partir d'une liste de résultats.
 * @param {Array} rows - Résultats de la requête
 * @param {number} limit - Nombre max demandé
 * @param {number} [total] - Total optionnel
 * @returns {{ cursor: string|null, has_more: boolean, total: number|null }}
 */
const buildPagination = (rows, limit, total = null) => {
  const hasMore = rows.length === limit;
  const lastRow = hasMore ? rows[rows.length - 1] : null;
  return {
    cursor: lastRow ? encodeCursor(lastRow.created_at) : null,
    has_more: hasMore,
    total,
  };
};

module.exports = { encodeCursor, decodeCursor, buildPagination };
