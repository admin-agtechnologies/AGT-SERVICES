/**
 * Point d'entrée du service Chat.
 * Séquence de démarrage :
 * 1. Chargement des variables d'environnement
 * 2. Connexion Redis
 * 3. Exécution des migrations PostgreSQL
 * 4. Connexion RabbitMQ (publisher + consumer)
 * 5. Démarrage HTTP + Socket.io
 * 6. Démarrage du job de requeue des transferts expirés
 */

// Charger .env si présent (dev uniquement — en production, variables injectées par Docker)
if (process.env.NODE_ENV !== 'production') {
  try { require('fs').accessSync('.env'); require('dotenv').config(); } catch { /* pas de .env */ }
}

const http = require('http');
const app = require('./app');
const { initSocket } = require('./socket');
const { runMigrations } = require('./common/db/migrate');
const { getRedis } = require('./common/cache/redis');
const { connect: connectPublisher } = require('./common/broker/publisher');
const { connect: connectConsumer } = require('./common/broker/consumer');
const { requeueTimedOutTransfers } = require('./modules/transfers/transfers.service');
const logger = require('./common/utils/logger');

const PORT = parseInt(process.env.PORT || '7008', 10);
const TRANSFER_TIMEOUT_MIN = parseInt(process.env.TRANSFER_TIMEOUT_MIN || '10', 10);

const start = async () => {
  try {
    // 1. Initialiser Redis (connexion eager)
    getRedis();
    logger.info('Redis client initialized');

    // 2. Exécuter les migrations SQL
    await runMigrations();

    // 3. Connecter RabbitMQ publisher
    await connectPublisher();

    // 4. Connecter RabbitMQ consumer (pas de handlers entrants pour l'instant)
    await connectConsumer({});

    // 5. Créer le serveur HTTP et initialiser Socket.io
    const httpServer = http.createServer(app);
    const io = initSocket(httpServer);

    // Rendre l'instance io accessible depuis les controllers via app.get('io')
    app.set('io', io);

    // 6. Démarrer le serveur
    httpServer.listen(PORT, () => {
      logger.info({ port: PORT, env: process.env.NODE_ENV }, 'AGT Chat Service started');
    });

    // 7. Job périodique : remettre en attente les transferts expirés
    // Vérifie toutes les minutes (largement suffisant pour un timeout de 10 min)
    setInterval(async () => {
      try {
        await requeueTimedOutTransfers();
      } catch (err) {
        logger.error({ err }, 'Transfer requeue job failed');
      }
    }, 60 * 1000);

    // Gestion propre des signaux d'arrêt (SIGTERM pour Docker/K8s)
    const shutdown = (signal) => {
      logger.info({ signal }, 'Shutdown signal received');
      httpServer.close(() => {
        logger.info('HTTP server closed');
        process.exit(0);
      });
      // Forcer la sortie après 10s si des connexions restent ouvertes
      setTimeout(() => process.exit(1), 10000);
    };

    process.on('SIGTERM', () => shutdown('SIGTERM'));
    process.on('SIGINT', () => shutdown('SIGINT'));

  } catch (err) {
    logger.error({ err }, 'Failed to start AGT Chat Service');
    process.exit(1);
  }
};

start();
