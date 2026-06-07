FROM node:20-slim AS base
RUN npm install -g pnpm@10

# Install depedencies
FROM base AS deps
WORKDIR /app/backend
COPY backend/package.json backend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Build
FROM base AS build
WORKDIR /app/backend

COPY backend/package.json backend/tsconfig.json ./
COPY --from=deps /app/backend/node_modules ./node_modules
COPY backend/prisma prisma/
COPY backend/src src/
COPY shared /app/shared

RUN pnpm dlx prisma generate
RUN pnpm run build
RUN pnpm prune --prod

# Runtime
FROM node:20-slim AS runtime
ENV NODE_ENV=production
WORKDIR /app/backend

COPY --from=build /app/backend/package.json ./
COPY --from=build /app/backend/node_modules ./node_modules
COPY --from=build /app/backend/dist ./dist
COPY --from=build /app/backend/generated ./generated 
EXPOSE 3000

CMD ["npm", "run", "start"]