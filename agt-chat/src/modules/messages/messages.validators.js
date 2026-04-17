const Joi = require('joi');

const sendMessageSchema = Joi.object({
  content: Joi.string().max(4096).required(),
  parent_id: Joi.string().uuid().optional().allow(null),
});

const editMessageSchema = Joi.object({
  content: Joi.string().max(4096).required(),
});

const markReadSchema = Joi.object({
  last_message_id: Joi.string().uuid().required(),
});

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

module.exports = { sendMessageSchema, editMessageSchema, markReadSchema, validate };
