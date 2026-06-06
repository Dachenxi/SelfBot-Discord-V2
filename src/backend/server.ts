import fastify from "fastify";
import clientRoutes from "./routes/clientRoutes";
import snifferRoutes from "./routes/snifferRoutes";
import cors from "@fastify/cors";

const server = fastify()
server.register(cors, {
    origin: 'http://localhost:5173', // Ganti dengan alamat frontend kamu jika berbeda
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], // Sesuaikan dengan metode yang kamu butuhkan
    credentials: true, // Jika kamu perlu mengirim cookies atau header otentikasi
})

server.register(clientRoutes, { prefix: '/api/client' })
server.register(snifferRoutes, { prefix: '/api/sniffer' })
server.get('/', async (request, reply) => {
    return { hello: 'world' }
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