/**
 * Runner de migrations SQL.
 * Exécute les fichiers SQL du dossier /migrations dans l'ordre numérique.
 * Idempotent : utilise IF NOT EXISTS dans chaque migration.
 * Appelé au démarrage du service dans server.js.
 */
const fs = require('fs');
const path = require('path');
const { query } = require('./pool');
const logger = require('../utils/logger');

const MIGRATIONS_DIR = path.join(__dirname, '../../../migrations');

const runMigrations = async () => {
  // Lire et trier les fichiers SQL par ordre numérique
  const files = fs
    .readdirSync(MIGRATIONS_DIR)
    .filter((f) => f.endsWith('.sql'))
    .sort();

  logger.info({ count: files.length }, 'Running migrations');

  for (const file of files) {
    const sql = fs.readFileSync(path.join(MIGRATIONS_DIR, file), 'utf8');
    try {
      await query(sql);
      logger.info({ file }, 'Migration applied');
    } catch (err) {
      logger.error({ file, err }, 'Migration failed');
      throw err;
    }
  }

  logger.info('All migrations applied successfully');
};

module.exports = { runMigrations };
