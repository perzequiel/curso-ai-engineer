# syntax=docker/dockerfile:1.6

# ---------- Deps: instala dependencias (cacheable por package.json) ----------
# Node 22 es requerido por pnpm >= 11 (usa el builtin node:sqlite).
FROM node:22-alpine AS deps

WORKDIR /app

COPY package.json package-lock.json* pnpm-lock.yaml* pnpm-workspace.yaml* ./

# Soporta npm o pnpm segun el lockfile presente
RUN if [ -f pnpm-lock.yaml ]; then \
        corepack enable && pnpm install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then \
        npm ci; \
    else \
        npm install; \
    fi

# ---------- Builder: compila la app con next build ----------
FROM node:22-alpine AS builder

WORKDIR /app

# La URL del backend que el browser usa para llamar a FastAPI.
# Por ser NEXT_PUBLIC_*, queda inlineada en el bundle en build-time.
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL} \
    NEXT_TELEMETRY_DISABLED=1

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN if [ -f pnpm-lock.yaml ]; then \
        corepack enable && pnpm run build; \
    else \
        npm run build; \
    fi

# ---------- Runner: imagen final liviana corriendo next start ----------
FROM node:22-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOSTNAME=0.0.0.0

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json
COPY --from=builder --chown=nextjs:nodejs /app/next.config.mjs ./next.config.mjs

USER nextjs

EXPOSE 3000

CMD ["npm", "run", "start", "--", "-H", "0.0.0.0", "-p", "3000"]
