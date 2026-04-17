/**
 * Service transfers — logique métier pour les transferts bot→humain.
 *
 * Règles clés (CDC §5.4, §5.4.1) :
 * - Création : S2S uniquement (Chatbot → Chat)
 * - Prise en charge : verrou optimiste (UPDATE WHERE status='pending') → 409 si concurrent
 * - Clôture : uniquement par l'opérateur ayant pris en charge
 * - Timeout : job périodique remet en 'pending' si opérateur déconnecté sans clôturer
 */
const transfersRepo = require('./transfers.repository');
const conversationsRepo = require('../conversations/conversations.repository');
const capabilitiesService = require('../capabilities/capabilities.service');
const { checkPermission } = require('../../common/clients/usersClient');
const { resolveProfilesId } = require('../../common/clients/usersClient');
const { sendNotification } = require('../../common/clients/notificationClient');
const { publish } = require('../../common/broker/publisher');
const AppError = require('../../common/errors/AppError');
const logger = require('../../common/utils/logger');

const TRANSFER_TIMEOUT_MIN = () => parseInt(process.env.TRANSFER_TIMEOUT_MIN || '10', 10);

/**
 * Crée un transfert bot→humain.
 * Appelé uniquement via S2S par le Service Chatbot.
 * Crée d'abord la conversation de type 'transfer', puis le transfert associé.
 * @param {object} body - { user_id, platform_id, bot_history, context }
 * @param {object} [io]
 * @returns {Promise<object>}
 */
const createTransfer = async (body, io = null) => {
  const { user_id, platform_id, bot_history = [], context = {} } = body;

  const caps = await capabilitiesService.getCapabilities(platform_id);
  capabilitiesService.requireFeature(caps, 'transfer_enabled');

  // Créer la conversation de type 'transfer' dédiée
  const conversation = await conversationsRepo.createWithParticipants(
    { type: 'transfer', platform_id, created_by: user_id, metadata: { source: 'chatbot' } },
    [user_id]
  );

  const transfer = await transfersRepo.create({
    conversation_id: conversation.id,
    user_id,
    bot_history,
    context,
  });

  logger.info({ transfer_id: transfer.id, user_id, platform_id }, 'Transfer created');

  // Notifier les opérateurs via WebSocket
  if (io) {
    io.emit('transfer:new', { transfer_id: transfer.id, conversation_id: conversation.id, user_id });
  }

  // Notification push aux opérateurs hors ligne
  const profilesId = await resolveProfilesId(user_id);
  if (profilesId) {
    await sendNotification(profilesId, platform_id, 'chat_transfer_new', {
      transfer_id: transfer.id,
      conversation_id: conversation.id,
    });
  }

  // Événement RabbitMQ
  await publish('chat.transfer.created', {
    transfer_id: transfer.id,
    conversation_id: conversation.id,
    user_id,
  });

  return { transfer, conversation };
};

/**
 * Prise en charge d'un transfert par un opérateur.
 * Verrou optimiste : UPDATE WHERE status='pending' → 409 si déjà pris.
 * Vérifie la permission chat:transfer:take via Users.
 * @param {string} transferId
 * @param {string} operatorId - users_auth.id
 * @param {string} platformId
 * @param {object} [io]
 */
const takeTransfer = async (transferId, operatorId, platformId, io = null) => {
  // Vérification permission opérateur (fail-closed)
  const canTake = await checkPermission(operatorId, 'chat:transfer:take', platformId);
  if (!canTake) {
    throw new AppError('FORBIDDEN', 'Permission chat:transfer:take requise', 403);
  }

  // Verrou optimiste — ne met à jour que si status = 'pending'
  const transfer = await transfersRepo.takeOptimistic(transferId, operatorId);
  if (!transfer) {
    throw new AppError('TRANSFER_ALREADY_TAKEN', 'Ce transfert a déjà été pris en charge', 409);
  }

  logger.info({ transfer_id: transferId, operator_id: operatorId }, 'Transfer taken');

  // Ajouter l'opérateur comme participant à la conversation
  await conversationsRepo.addParticipant(transfer.conversation_id, operatorId, 'admin');

  if (io) {
    io.emit('transfer:taken', { transfer_id: transferId, operator_id: operatorId });
  }

  await publish('chat.transfer.taken', { transfer_id: transferId, operator_id: operatorId });

  return transfer;
};

/**
 * Clôture un transfert.
 * Uniquement par l'opérateur ayant pris en charge (CDC §5.4.1).
 * @param {string} transferId
 * @param {string} operatorId
 * @param {object} [io]
 */
const closeTransfer = async (transferId, operatorId, io = null) => {
  const transfer = await transfersRepo.close(transferId, operatorId);
  if (!transfer) {
    throw new AppError('TRANSFER_NOT_FOUND', 'Transfert introuvable ou vous n\'êtes pas l\'opérateur assigné', 404);
  }

  logger.info({ transfer_id: transferId, operator_id: operatorId }, 'Transfer closed');

  if (io) {
    io.to(transfer.conversation_id).emit('transfer:closed', { transfer_id: transferId });
  }

  await publish('chat.transfer.closed', { transfer_id: transferId });

  return transfer;
};

/**
 * Liste les transferts en attente (file d'attente opérateurs).
 * @param {string} [platformId]
 */
const getPendingTransfers = async (platformId = null) => {
  return transfersRepo.findPending(platformId);
};

/**
 * Job de requeue : remet en 'pending' les transferts expirés.
 * Appelé périodiquement par un setInterval dans server.js.
 */
const requeueTimedOutTransfers = async () => {
  const count = await transfersRepo.requeueTimedOut(TRANSFER_TIMEOUT_MIN());
  if (count > 0) {
    logger.info({ count, timeout_min: TRANSFER_TIMEOUT_MIN() }, 'Timed-out transfers requeued');
  }
};

/**
 * Stats pour admin/S2S.
 */
const getStats = async () => {
  return transfersRepo.getStats();
};

module.exports = { createTransfer, takeTransfer, closeTransfer, getPendingTransfers, requeueTimedOutTransfers, getStats };
