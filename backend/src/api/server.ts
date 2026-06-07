import fastify from "fastify";
import cors from "@fastify/cors";
import jwt from "@fastify/jwt";
import clientRoutes from "./routes/clientRoutes.js";
import snifferRoutes from "./routes/snifferRoutes.js";
import authRoutes from "./routes/authRoutes.js";

const server = fastify()


server.register(jwt, {
    secret: process.env.JWT_SECRET || 'f/354]&/.v-h=|z/ZT,ka^._$5AFR+3d6^o%KkAuB6+GFy=nshEH7v)Iwg6_GbH&q]R(2nOfcpFn97uB7c<xj]'
})


server.register(cors, {
    origin: [`${process.env.CORS_ORIGIN}`, "http://localhost:5173", "http://backend:5173"], // Ganti dengan alamat frontend kamu jika berbeda
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], // Sesuaikan dengan metode yang kamu butuhkan
    credentials: true, // Jika kamu perlu mengirim cookies atau header otentikasi
})


server.register(authRoutes, { prefix: '/api/auth' })

server.get('/', async (request, reply) => {
    return { hello: 'world' }
})


server.register(async function (protectedServer) {
    protectedServer.addHook('onRequest', async (request, reply) => {
        try {
            await request.jwtVerify(); // Cek apakah tiketnya asli
        } catch (err) {
            reply.code(401).send({ error: 'Sesi habis atau tidak valid, harap login!' });
        }
    });
    protectedServer.register(clientRoutes, { prefix: '/api/client' })
    protectedServer.register(snifferRoutes, { prefix: '/api/sniffer' })
})


export const startWebServer = async () => {
    try {
        // Gunakan port dari file .env jika ada, jika tidak gunakan port 3000
        const port = process.env.PORT ? parseInt(process.env.PORT) : 3000;
        
        // host '0.0.0.0' penting agar bisa diakses jika nanti di-hosting (VPS)
        await server.listen({ port: port, host: '0.0.0.0' });
        console.log(`[Web] Dashboard berjalan di http://localhost:${port}`);
    } catch (err) {
        console.error('[Web] Gagal menyalakan server:', err);
        process.exit(1);
    }
}