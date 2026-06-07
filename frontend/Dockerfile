FROM node:20-slim AS base
RUN npm install -g pnpm@10


FROM base AS deps
WORKDIR /app/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile


FROM base AS build

WORKDIR /app
COPY --from=deps /app/frontend/node_modules ./frontend/node_modules
COPY frontend/package.json frontend/pnpm-lock.yaml frontend/svelte.config.js frontend/tsconfig.json frontend/vite.config.ts ./frontend/
COPY frontend/src ./frontend/src
COPY frontend/static ./frontend/static
COPY shared ./shared


WORKDIR /app/frontend
RUN pnpm build
RUN pnpm prune --prod


FROM node:20-slim AS runtime
ENV NODE_ENV=production

WORKDIR /app/frontend

COPY --from=build /app/frontend/package.json ./
COPY --from=build /app/frontend/node_modules ./node_modules
COPY --from=build /app/frontend/build ./build

EXPOSE 4173

CMD ["node", "build"]