/**
 * Utilitaires UUID.
 */
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

/**
 * Valide qu'une chaîne est un UUID v4 valide.
 * @param {string} value
 * @returns {boolean}
 */
const isValidUUID = (value) => {
  return typeof value === 'string' && UUID_REGEX.test(value);
};

module.exports = { isValidUUID };
