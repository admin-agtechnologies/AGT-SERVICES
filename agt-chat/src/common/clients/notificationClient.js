/**
 * Client HTTP vers le Service Notification v1.2.
 *
 * IMPORTANT (CDC §10.4) :
 * Chat travaille avec users_auth.id mais Notification attend users_profiles.id.
 * Ce client attend déjà le profiles_id résolu — la résolution est faite en amont (usersClient).
 * L'échec Notification ne bloque JAMAIS l'envoi d'un message (fail-silent).
 */
const axios = require('axios');
const logger = require('../utils/logger');

const NOTIF_URL = () => process.env.NOTIFICATION_SERVICE_URL || 'http://localhost:7002';

const s2sHeaders = () => ({
  'X-Service-Token': process.env.S2S_SECRET || '',
  'Content-Type': 'application/json',
});

/**
 * Envoie une notification à un utilisateur hors ligne.
 * @param {string} profilesUserId - users_profiles.id (PAS users_auth.id)
 * @param {string} platformId
 * @param {string} templateCode - Ex: 'chat_message_offline'
 * @param {object} payload - Données contextuelles de la notification
 */
const sendNotification = async (profilesUserId, platformId, templateCode, payload = {}) => {
  try {
    await axios.post(
      `${NOTIF_URL()}/api/v1/notifications/send`,
      { user_id: profilesUserId, platform_id: platformId, type: templateCode, payload },
      { headers: s2sHeaders(), timeout: 5000 }
    );
    logger.info({ profilesUserId, templateCode }, 'Notification sent');
  } catch (err) {
    // Fail-silent : une notification ratée ne doit jamais bloquer le flux principal
    logger.warn({ profilesUserId, templateCode, err: err.message }, 'Notification failed (non-blocking)');
  }
};

module.exports = { sendNotification };
