/**
 * Pool de connexions PostgreSQL partagé.
 * Toutes les requêtes SQL passent par ce pool — jamais de connexion directe ailleurs.
 */
const { Pool } = require('pg');
const logger = require('../utils/logger');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  // Taille du pool adaptée à la charge attendue (MVP : 10 connexions max)
  max: parseInt(process.env.DB_POOL_MAX || '10', 10),
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('error', (err) => {
  logger.error({ err }, 'Unexpected PostgreSQL pool error');
});

/**
 * Exécute une requête SQL paramétrée.
 * @param {string} text - Requête SQL avec placeholders $1, $2, ...
 * @param {Array} [params] - Paramètres
 * @returns {Promise<import('pg').QueryResult>}
 */
const query = (text, params) => pool.query(text, params);

/**
 * Acquiert un client pour les transactions multi-requêtes.
 * Toujours libérer avec client.release() dans un finally.
 */
const getClient = () => pool.connect();

/**
 * Vérifie la connexion à la base de données (utilisé par le health check).
 * @returns {Promise<boolean>}
 */
const ping = async () => {
  const result = await query('SELECT 1');
  return result.rowCount === 1;
};

module.exports = { query, getClient, pool, ping };
