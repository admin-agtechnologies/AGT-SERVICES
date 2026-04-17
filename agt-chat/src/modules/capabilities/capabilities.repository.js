/**
 * Repository capabilities — accès DB uniquement.
 * Toutes les requêtes SQL relatives aux platform_capabilities sont ici.
 */
const { query } = require('../../common/db/pool');

/**
 * Récupère les capabilities d'une plateforme.
 * @param {string} platformId
 * @returns {Promise<object|null>}
 */
const findByPlatformId = async (platformId) => {
  const result = await query(
    'SELECT * FROM platform_capabilities WHERE platform_id = $1',
    [platformId]
  );
  return result.rows[0] || null;
};

/**
 * Crée ou met à jour les capabilities d'une plateforme (upsert).
 * @param {string} platformId
 * @param {object} fields - Champs à mettre à jour
 * @returns {Promise<object>}
 */
const upsert = async (platformId, fields) => {
  const keys = Object.keys(fields);
  const values = Object.values(fields);

  // Construction dynamique de la requête upsert
  const setClauses = keys.map((k, i) => `${k} = $${i + 2}`).join(', ');
  const result = await query(
    `INSERT INTO platform_capabilities (platform_id, ${keys.join(', ')}, updated_at)
     VALUES ($1, ${keys.map((_, i) => `$${i + 2}`).join(', ')}, NOW())
     ON CONFLICT (platform_id) DO UPDATE SET ${setClauses}, updated_at = NOW()
     RETURNING *`,
    [platformId, ...values]
  );
  return result.rows[0];
};

module.exports = { findByPlatformId, upsert };
