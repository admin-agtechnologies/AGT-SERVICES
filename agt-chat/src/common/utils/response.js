/**
 * Helpers pour formater les réponses HTTP selon le standard CDC §4.1.
 * Toutes les réponses passent par ces helpers pour garantir la cohérence.
 */

/**
 * Réponse succès simple.
 * @param {object} res - Express response
 * @param {any} data - Données à retourner
 * @param {number} [status=200] - Code HTTP
 */
const success = (res, data, status = 200) => {
  return res.status(status).json({ success: true, data });
};

/**
 * Réponse succès avec pagination cursor-based.
 * @param {object} res - Express response
 * @param {Array} data - Liste de résultats
 * @param {object} pagination - { cursor, has_more, total }
 */
const successPaginated = (res, data, pagination) => {
  return res.status(200).json({ success: true, data, pagination });
};

/**
 * Réponse erreur standardisée.
 * @param {object} res - Express response
 * @param {string} code - Code d'erreur métier (ex: CONVERSATION_NOT_FOUND)
 * @param {string} message - Message lisible
 * @param {number} [status=400] - Code HTTP
 */
const error = (res, code, message, status = 400) => {
  return res.status(status).json({ success: false, error: { code, message } });
};

module.exports = { success, successPaginated, error };
