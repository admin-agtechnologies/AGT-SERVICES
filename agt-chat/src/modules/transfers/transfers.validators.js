const Joi = require('joi');

const createTransferSchema = Joi.object({
  user_id: Joi.string().uuid().required(),
  platform_id: Joi.string().uuid().required(),
  bot_history: Joi.array().optional().default([]),
  context: Joi.object().optional().default({}),
});

const validate = (schema) => (req, res, next) => {
  const { error, value } = schema.validate(req.body, { abortEarly: false });
  if (error) {
    return res.status(400).json({
      success: false,
      error: { code: 'VALIDATION_ERROR', message: error.details.map((d) => d.message).join('; ') },
    });
  }
  req.body = value;
  next();
};

module.exports = { createTransferSchema, validate };
