/**
 * Schémas de validation Joi pour le module conversations.
 */
const Joi = require('joi');

const createConversationSchema = Joi.object({
  type: Joi.string().valid('direct', 'channel').required(),
  platform_id: Joi.string().uuid().required(),
  name: Joi.string().max(255).when('type', { is: 'channel', then: Joi.required() }),
  description: Joi.string().max(1000).optional().allow(''),
  is_public: Joi.boolean().optional(),
  participant_ids: Joi.array()
    .items(Joi.string().uuid())
    .when('type', { is: 'direct', then: Joi.array().min(1).max(1).required() })
    .optional(),
  metadata: Joi.object().optional(),
});

const updateConversationSchema = Joi.object({
  name: Joi.string().max(255).optional(),
  description: Joi.string().max(1000).optional().allow(''),
  is_public: Joi.boolean().optional(),
}).min(1);

const addParticipantSchema = Joi.object({
  user_id: Joi.string().uuid().required(),
});

/**
 * Middleware de validation Joi générique.
 * @param {Joi.Schema} schema
 */
const validate = (schema) => (req, res, next) => {
  const { error } = schema.validate(req.body, { abortEarly: false });
  if (error) {
    return res.status(400).json({
      success: false,
      error: { code: 'VALIDATION_ERROR', message: error.details.map((d) => d.message).join('; ') },
    });
  }
  next();
};

module.exports = { createConversationSchema, updateConversationSchema, addParticipantSchema, validate };
