# ============================================================
#  AGT Media Service — Dockerfile multi-stage
#  Node.js 20 LTS + Sharp (traitement images)
# ============================================================

# --- Étape 1 : Build ---
FROM node:20-alpine AS builder

# Sharp requiert des libs natives (libvips)
RUN apk add --no-cache python3 make g++ vips-dev

WORKDIR /app

COPY package*.json ./
RUN npm ci --include=dev

COPY . .
RUN npm run build

# --- Étape 2 : Runtime ---
FROM node:20-alpine AS runner

RUN apk add --no-cache vips-dev

WORKDIR /app

# Copier uniquement les dépendances de production
COPY package*.json ./
RUN npm ci --only=production

# Copier le build
COPY --from=builder /app/dist ./dist

# Dossier de stockage local
RUN mkdir -p /app/uploads && chown -R node:node /app/uploads

USER node

EXPOSE 7003

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD wget -qO- http://localhost:7003/api/v1/media/health || exit 1

CMD ["node", "dist/src/main"]
