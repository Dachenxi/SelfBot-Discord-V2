FROM node:20-slim
RUN npm install -g pnpm

# Install openssl untuk engine Prisma
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Ambil file package & Prisma dari ROOT
COPY package.json pnpm-lock.yaml ./
COPY prisma ./prisma/

# 2. Install dependensi secara ketat (sekarang lockfile pasti ketemu!)
RUN pnpm install --frozen-lockfile

# 3. Bawa masuk folder shared dan src
COPY shared ./shared/
COPY src ./src/
COPY tsconfig.json ./

# 4. Generate Prisma Client
RUN pnpm prisma generate

# 5. Build TypeScript
RUN pnpm run build
RUN pnpm prune --prod

EXPOSE 3000

# CATATAN: Tergantung pengaturan rootDir di tsconfig.json-mu, 
# Hasil build tsc bisa jadi di "dist/index.js" atau "dist/src/index.js". 
# Sesuaikan CMD di bawah jika saat dijalankan terjadi error "module not found".
CMD ["node", "dist/src/index.js"]