/**
 * Spécification OpenAPI 3.0 complète du Chat Service.
 * Tous les paths sont préfixés par /api/v1/chat pour correspondre
 * exactement aux routes réelles du service.
 */
const swaggerJsdoc = require("swagger-jsdoc");

const options = {
  definition: {
    openapi: "3.0.0",
    info: {
      title: "AGT Chat Service",
      version: "1.2.0",
      description: `
## AGT Chat Service — API REST

**Base URL :** \`http://localhost:7008\`

**Authentification :**
- La plupart des endpoints requièrent un **JWT Bearer** (token utilisateur)
- Les endpoints de transfert (création) requièrent un **token S2S** (service-to-service)

**WebSocket :** \`ws://localhost:7008?token=<JWT>\`
      `,
    },
    servers: [
      { url: "http://localhost:7008", description: "Local — production" },
    ],
    components: {
      securitySchemes: {
        BearerAuth: {
          type: "http",
          scheme: "bearer",
          bearerFormat: "JWT",
          description: "Token JWT utilisateur (sub = users_auth.id)",
        },
        S2SAuth: {
          type: "http",
          scheme: "bearer",
          bearerFormat: "JWT",
          description: "Token S2S service-to-service (émis par Auth Service)",
        },
      },
      schemas: {
        Error: {
          type: "object",
          properties: {
            success: { type: "boolean", example: false },
            error: {
              type: "object",
              properties: {
                code: { type: "string", example: "UNAUTHORIZED" },
                message: {
                  type: "string",
                  example: "Token invalide ou expiré",
                },
              },
            },
          },
        },
        Conversation: {
          type: "object",
          properties: {
            id: { type: "string", format: "uuid" },
            type: { type: "string", enum: ["direct", "channel"] },
            platform_id: { type: "string", format: "uuid" },
            name: { type: "string", nullable: true },
            created_at: { type: "string", format: "date-time" },
            updated_at: { type: "string", format: "date-time" },
          },
        },
        Message: {
          type: "object",
          properties: {
            id: { type: "string", format: "uuid" },
            conversation_id: { type: "string", format: "uuid" },
            sender_id: { type: "string", format: "uuid" },
            content: { type: "string" },
            parent_id: { type: "string", format: "uuid", nullable: true },
            edited_at: { type: "string", format: "date-time", nullable: true },
            deleted_at: { type: "string", format: "date-time", nullable: true },
            created_at: { type: "string", format: "date-time" },
          },
        },
        Transfer: {
          type: "object",
          properties: {
            id: { type: "string", format: "uuid" },
            conversation_id: { type: "string", format: "uuid" },
            user_id: { type: "string", format: "uuid" },
            status: { type: "string", enum: ["pending", "taken", "closed"] },
            operator_id: { type: "string", format: "uuid", nullable: true },
            context: { type: "object", nullable: true },
            created_at: { type: "string", format: "date-time" },
          },
        },
        Capabilities: {
          type: "object",
          properties: {
            platform_id: { type: "string", format: "uuid" },
            direct_enabled: { type: "boolean" },
            channels_enabled: { type: "boolean" },
            transfer_enabled: { type: "boolean" },
            reactions_enabled: { type: "boolean" },
            typing_enabled: { type: "boolean" },
            presence_enabled: { type: "boolean" },
            read_receipts_enabled: { type: "boolean" },
            message_edit_enabled: { type: "boolean" },
            message_delete_enabled: { type: "boolean" },
            message_search_enabled: { type: "boolean" },
            attachments_enabled: { type: "boolean" },
            max_message_length: { type: "integer", example: 4096 },
            max_channel_members: { type: "integer", example: 500 },
            rate_limit_per_user: { type: "integer", example: 30 },
            rate_limit_per_conv: { type: "integer", example: 100 },
            updated_at: { type: "string", format: "date-time" },
          },
        },
        Participant: {
          type: "object",
          properties: {
            user_id: { type: "string", format: "uuid" },
            role: { type: "string", enum: ["owner", "member"] },
            joined_at: { type: "string", format: "date-time" },
          },
        },
        Reaction: {
          type: "object",
          properties: {
            emoji: { type: "string", example: "👍" },
            count: { type: "integer" },
            user_ids: {
              type: "array",
              items: { type: "string", format: "uuid" },
            },
          },
        },
        Presence: {
          type: "object",
          properties: {
            user_id: { type: "string", format: "uuid" },
            status: { type: "string", enum: ["online", "offline"] },
            last_seen_at: {
              type: "string",
              format: "date-time",
              nullable: true,
            },
          },
        },
      },
    },
    security: [{ BearerAuth: [] }],

    paths: {
      // ── HEALTH ─────────────────────────────────────────────────────────────
      "/api/v1/chat/health": {
        get: {
          summary: "État du service",
          description:
            "Vérifie la connectivité DB, Redis et RabbitMQ. Pas d'authentification requise.",
          tags: ["Health"],
          security: [],
          responses: {
            200: {
              description: "Service opérationnel",
              content: {
                "application/json": {
                  schema: {
                    type: "object",
                    properties: {
                      success: { type: "boolean", example: true },
                      data: {
                        type: "object",
                        properties: {
                          status: { type: "string", example: "healthy" },
                          database: { type: "string", example: "ok" },
                          redis: { type: "string", example: "ok" },
                          rabbitmq: { type: "string", example: "ok" },
                          uptime: { type: "number" },
                        },
                      },
                    },
                  },
                },
              },
            },
            503: { description: "Service dégradé" },
          },
        },
      },

      // ── CONVERSATIONS ──────────────────────────────────────────────────────
      "/api/v1/chat/conversations": {
        post: {
          summary: "Créer une conversation",
          description:
            "Crée une conversation directe ou un canal. Vérifie les capabilities de la plateforme.",
          tags: ["Conversations"],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  required: ["type", "platform_id"],
                  properties: {
                    type: {
                      type: "string",
                      enum: ["direct", "channel"],
                      example: "direct",
                    },
                    platform_id: { type: "string", format: "uuid" },
                    participant_ids: {
                      type: "array",
                      items: { type: "string", format: "uuid" },
                      description: "Requis pour type=direct",
                    },
                    name: {
                      type: "string",
                      description: "Requis pour type=channel",
                    },
                  },
                },
              },
            },
          },
          responses: {
            201: {
              description: "Conversation créée",
              content: {
                "application/json": {
                  schema: {
                    properties: {
                      success: { type: "boolean" },
                      data: { $ref: "#/components/schemas/Conversation" },
                    },
                  },
                },
              },
            },
            400: {
              description: "Validation error",
              content: {
                "application/json": {
                  schema: { $ref: "#/components/schemas/Error" },
                },
              },
            },
            401: { description: "Non authentifié" },
            403: {
              description:
                "Feature désactivée (direct_enabled=false ou channels_enabled=false)",
            },
          },
        },
        get: {
          summary: "Lister mes conversations",
          tags: ["Conversations"],
          parameters: [
            {
              in: "query",
              name: "limit",
              schema: { type: "integer", default: 20 },
            },
            {
              in: "query",
              name: "offset",
              schema: { type: "integer", default: 0 },
            },
          ],
          responses: {
            200: { description: "Liste paginée des conversations" },
            401: { description: "Non authentifié" },
          },
        },
      },

      "/api/v1/chat/conversations/stats": {
        get: {
          summary: "Statistiques des conversations",
          tags: ["Conversations"],
          responses: { 200: { description: "Stats globales" } },
        },
      },

      "/api/v1/chat/conversations/transfer": {
        post: {
          summary: "Créer un transfert bot→humain",
          description:
            "**S2S uniquement.** Appelé par le Chatbot Service. Doit être appelé avant les routes /:id.",
          tags: ["Transfers"],
          security: [{ S2SAuth: [] }],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  required: ["conversation_id", "user_id"],
                  properties: {
                    conversation_id: { type: "string", format: "uuid" },
                    user_id: {
                      type: "string",
                      format: "uuid",
                      description: "users_auth.id du client",
                    },
                    context: {
                      type: "object",
                      description: "Contexte optionnel transmis par le bot",
                    },
                  },
                },
              },
            },
          },
          responses: {
            201: {
              description:
                "Transfert créé. Émet transfer:new via WebSocket et chat.transfer.created via RabbitMQ.",
              content: {
                "application/json": {
                  schema: {
                    properties: {
                      success: { type: "boolean" },
                      data: { $ref: "#/components/schemas/Transfer" },
                    },
                  },
                },
              },
            },
            403: { description: "Token S2S invalide ou manquant" },
            422: { description: "Feature transfer_enabled=false" },
          },
        },
      },

      "/api/v1/chat/conversations/{id}": {
        get: {
          summary: "Détail d'une conversation",
          tags: ["Conversations"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: { description: "Conversation trouvée" },
            403: { description: "Non participant" },
            404: { description: "Non trouvée" },
          },
        },
        put: {
          summary: "Modifier une conversation",
          tags: ["Conversations"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          requestBody: {
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  properties: { name: { type: "string" } },
                },
              },
            },
          },
          responses: {
            200: { description: "Conversation mise à jour" },
            403: { description: "Non autorisé" },
          },
        },
        delete: {
          summary: "Supprimer une conversation",
          tags: ["Conversations"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: { description: "Supprimée" },
            403: { description: "Non owner/admin" },
          },
        },
      },

      "/api/v1/chat/conversations/{id}/participants": {
        post: {
          summary: "Ajouter des participants",
          tags: ["Conversations"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  required: ["user_ids"],
                  properties: {
                    user_ids: {
                      type: "array",
                      items: { type: "string", format: "uuid" },
                    },
                  },
                },
              },
            },
          },
          responses: { 200: { description: "Participants ajoutés" } },
        },
        get: {
          summary: "Lister les participants",
          tags: ["Conversations"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: {
              description: "Liste des participants",
              content: {
                "application/json": {
                  schema: {
                    type: "array",
                    items: { $ref: "#/components/schemas/Participant" },
                  },
                },
              },
            },
          },
        },
      },

      "/api/v1/chat/conversations/{id}/participants/{uid}": {
        delete: {
          summary: "Retirer un participant",
          tags: ["Conversations"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
            {
              in: "path",
              name: "uid",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: { 200: { description: "Participant retiré" } },
        },
      },

      "/api/v1/chat/conversations/{id}/leave": {
        post: {
          summary: "Quitter une conversation",
          tags: ["Conversations"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: { 200: { description: "Quitté avec succès" } },
        },
      },

      // ── MESSAGES ───────────────────────────────────────────────────────────
      "/api/v1/chat/conversations/{id}/messages": {
        post: {
          summary: "Envoyer un message",
          description:
            "Rate limité : 30 msg/min par user, 100 msg/min par conversation.",
          tags: ["Messages"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  required: ["content"],
                  properties: {
                    content: {
                      type: "string",
                      maxLength: 4096,
                      example: "Bonjour !",
                    },
                    parent_id: {
                      type: "string",
                      format: "uuid",
                      description: "Réponse à un message existant",
                    },
                  },
                },
              },
            },
          },
          responses: {
            201: {
              description: "Message envoyé",
              content: {
                "application/json": {
                  schema: {
                    properties: {
                      success: { type: "boolean" },
                      data: { $ref: "#/components/schemas/Message" },
                    },
                  },
                },
              },
            },
            403: { description: "Non participant" },
            429: { description: "Rate limit atteint" },
          },
        },
        get: {
          summary: "Historique des messages",
          description:
            "Pagination par curseur (before). Ordre décroissant (plus récent en premier).",
          tags: ["Messages"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
            {
              in: "query",
              name: "limit",
              schema: { type: "integer", default: 50, maximum: 100 },
            },
            {
              in: "query",
              name: "before",
              schema: {
                type: "string",
                format: "uuid",
                description: "ID curseur pour pagination",
              },
            },
          ],
          responses: { 200: { description: "Liste des messages" } },
        },
      },

      "/api/v1/chat/conversations/{id}/messages/search": {
        get: {
          summary: "Recherche full-text dans une conversation",
          description: "Utilise l'index GIN PostgreSQL.",
          tags: ["Messages"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
            {
              in: "query",
              name: "q",
              required: true,
              schema: { type: "string", example: "bonjour" },
            },
            {
              in: "query",
              name: "limit",
              schema: { type: "integer", default: 20 },
            },
          ],
          responses: {
            200: { description: "Résultats de recherche" },
            403: { description: "Feature message_search_enabled=false" },
          },
        },
      },

      "/api/v1/chat/conversations/{id}/messages/{msgId}": {
        put: {
          summary: "Modifier un message",
          description:
            "Édition possible uniquement dans le délai configuré (MESSAGE_EDIT_DELAY_MIN, défaut 15 min).",
          tags: ["Messages"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
            {
              in: "path",
              name: "msgId",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  required: ["content"],
                  properties: { content: { type: "string" } },
                },
              },
            },
          },
          responses: {
            200: { description: "Message modifié" },
            403: { description: "Délai dépassé ou non auteur" },
            404: { description: "Message introuvable" },
          },
        },
        delete: {
          summary: "Supprimer un message (soft delete)",
          tags: ["Messages"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
            {
              in: "path",
              name: "msgId",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: { description: "Message supprimé" },
            403: { description: "Non auteur ni admin" },
          },
        },
      },

      "/api/v1/chat/conversations/{id}/read": {
        post: {
          summary: "Marquer les messages comme lus",
          description:
            "Met à jour le curseur de lecture. Émet read:updated via WebSocket.",
          tags: ["Messages"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  required: ["last_message_id"],
                  properties: {
                    last_message_id: { type: "string", format: "uuid" },
                  },
                },
              },
            },
          },
          responses: { 200: { description: "Curseur de lecture mis à jour" } },
        },
      },

      "/api/v1/chat/conversations/{id}/read-status": {
        get: {
          summary: "Statut de lecture de tous les participants",
          tags: ["Messages"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: { description: "Statuts de lecture par participant" },
          },
        },
      },

      // ── REACTIONS ──────────────────────────────────────────────────────────
      "/api/v1/chat/messages/{msgId}/reactions": {
        post: {
          summary: "Ajouter une réaction emoji",
          tags: ["Reactions"],
          parameters: [
            {
              in: "path",
              name: "msgId",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  required: ["emoji"],
                  properties: { emoji: { type: "string", example: "👍" } },
                },
              },
            },
          },
          responses: {
            200: {
              description:
                "Réaction ajoutée. Émet reaction:updated via WebSocket.",
            },
            403: { description: "Feature reactions_enabled=false" },
          },
        },
        get: {
          summary: "Lister les réactions d'un message",
          tags: ["Reactions"],
          parameters: [
            {
              in: "path",
              name: "msgId",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: {
              description: "Réactions groupées par emoji",
              content: {
                "application/json": {
                  schema: {
                    type: "array",
                    items: { $ref: "#/components/schemas/Reaction" },
                  },
                },
              },
            },
          },
        },
      },

      "/api/v1/chat/messages/{msgId}/reactions/{emoji}": {
        delete: {
          summary: "Retirer une réaction",
          tags: ["Reactions"],
          parameters: [
            {
              in: "path",
              name: "msgId",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
            {
              in: "path",
              name: "emoji",
              required: true,
              schema: { type: "string", example: "👍" },
            },
          ],
          responses: { 200: { description: "Réaction retirée" } },
        },
      },

      // ── TRANSFERS ──────────────────────────────────────────────────────────
      "/api/v1/chat/transfers/pending": {
        get: {
          summary: "Lister les transferts en attente",
          description:
            "Accessible aux opérateurs ayant la permission `chat:transfer:take`.",
          tags: ["Transfers"],
          responses: {
            200: {
              description: "Liste des transferts pending",
              content: {
                "application/json": {
                  schema: {
                    type: "array",
                    items: { $ref: "#/components/schemas/Transfer" },
                  },
                },
              },
            },
            401: { description: "Non authentifié" },
          },
        },
      },

      "/api/v1/chat/transfers/stats": {
        get: {
          summary: "Statistiques des transferts",
          description: "Accessible aux admins JWT ou via S2S.",
          tags: ["Transfers"],
          responses: {
            200: { description: "Stats : pending, taken, closed, avg_time" },
          },
        },
      },

      "/api/v1/chat/transfers/{id}/take": {
        post: {
          summary: "Prendre en charge un transfert",
          description:
            "Verrou optimiste — renvoie 409 si déjà pris simultanément par un autre opérateur.",
          tags: ["Transfers"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: {
              description:
                "Transfert pris en charge. Émet transfer:taken via WebSocket.",
            },
            403: { description: "Permission chat:transfer:take manquante" },
            404: { description: "Transfert introuvable" },
            409: { description: "Conflit — déjà pris par un autre opérateur" },
          },
        },
      },

      "/api/v1/chat/transfers/{id}/close": {
        post: {
          summary: "Clôturer un transfert",
          description: "Seul l'opérateur assigné peut clôturer.",
          tags: ["Transfers"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: {
              description:
                "Transfert clôturé. Émet transfer:closed via WebSocket.",
            },
            403: { description: "Non assigné à ce transfert" },
          },
        },
      },

      // ── CAPABILITIES ───────────────────────────────────────────────────────
      "/api/v1/chat/capabilities/{platformId}": {
        get: {
          summary: "Lire les capabilities d'une plateforme",
          description: "Accessible avec JWT utilisateur ou token S2S.",
          tags: ["Capabilities"],
          parameters: [
            {
              in: "path",
              name: "platformId",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: {
              description: "Capabilities de la plateforme",
              content: {
                "application/json": {
                  schema: {
                    properties: {
                      success: { type: "boolean" },
                      data: { $ref: "#/components/schemas/Capabilities" },
                    },
                  },
                },
              },
            },
            404: {
              description:
                "Plateforme inconnue — retourne les valeurs par défaut",
            },
          },
        },
        put: {
          summary: "Mettre à jour les capabilities",
          description:
            "Requiert la permission `chat:admin` vérifiée via Users Service.",
          tags: ["Capabilities"],
          parameters: [
            {
              in: "path",
              name: "platformId",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: { $ref: "#/components/schemas/Capabilities" },
              },
            },
          },
          responses: {
            200: { description: "Capabilities mises à jour" },
            403: { description: "Permission chat:admin manquante" },
          },
        },
      },

      // ── CANAUX ─────────────────────────────────────────────────────────────
      "/api/v1/chat/platforms/{platformId}/channels": {
        get: {
          summary: "Lister les canaux publics d'une plateforme",
          tags: ["Conversations"],
          parameters: [
            {
              in: "path",
              name: "platformId",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: { 200: { description: "Liste des canaux publics" } },
        },
      },

      "/api/v1/chat/channels/{id}/join": {
        post: {
          summary: "Rejoindre un canal public",
          tags: ["Conversations"],
          parameters: [
            {
              in: "path",
              name: "id",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: { description: "Canal rejoint" },
            403: { description: "Capacité max atteinte" },
          },
        },
      },

      // ── PRESENCE ───────────────────────────────────────────────────────────
      "/api/v1/chat/users/{uid}/presence": {
        get: {
          summary: "Présence d'un utilisateur",
          description: "Données Redis-only — jamais persistées en DB.",
          tags: ["Presence"],
          parameters: [
            {
              in: "path",
              name: "uid",
              required: true,
              schema: { type: "string", format: "uuid" },
            },
          ],
          responses: {
            200: {
              description: "Statut de présence",
              content: {
                "application/json": {
                  schema: {
                    properties: {
                      success: { type: "boolean" },
                      data: { $ref: "#/components/schemas/Presence" },
                    },
                  },
                },
              },
            },
          },
        },
      },
    },
  },
  apis: [], // Spec 100% inline
};

const swaggerSpec = swaggerJsdoc(options);
module.exports = swaggerSpec;
