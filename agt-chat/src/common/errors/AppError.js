/**
 * Classe d'erreur custom du service Chat.
 * Toutes les erreurs métier doivent être lancées avec cette classe.
 * Ne jamais faire res.json() directement dans un service — toujours throw new AppError(...).
 */
class AppError extends Error {
  /**
   * @param {string} code - Code métier (ex: CONVERSATION_NOT_FOUND)
   * @param {string} message - Message lisible
   * @param {number} [httpStatus=400] - Code HTTP à retourner
   */
  constructor(code, message, httpStatus = 400) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.httpStatus = httpStatus;
    // Capture la stack trace proprement
    Error.captureStackTrace(this, this.constructor);
  }
}

module.exports = AppError;
