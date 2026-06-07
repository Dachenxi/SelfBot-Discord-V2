import { FastifyPluginAsync } from "fastify";
import { getBotStatus } from "../controller/clientController.js";
import { client } from "../../bot/client.js";
import type { ApiErrorResponse, ClientInfoResponse } from "../../../../shared/types.js";

const clientRoutes: FastifyPluginAsync = async (fastify) => {
    fastify.get('/status', async (request, reply) => {
        const status = await getBotStatus();
        return status;
    });

    fastify.get('/info', async (request, reply) => {
        if (!client.isReady() || !client.user) {
            return reply.status(503).send({
                success: false,
                message: 'Client is not ready'
            } satisfies ApiErrorResponse);
        }
        const memoryData = process.memoryUsage();

        // 2. Konversi ke MB dan bulatkan 2 angka di belakang koma
        const heapUsedMB = (memoryData.heapUsed / 1024 / 1024).toFixed(2);
        const rssMB = (memoryData.rss / 1024 / 1024).toFixed(2);
        
        return reply.status(200).send({
            success: true,
            status: "Online",

            id: client.user.id,
            username: client.user.username,
            discriminator: client.user.discriminator,
            avatar: client.user.avatarURL({ size: 512 }) || null,

            uptime: client.uptime,
            ping: client.ws.ping,
            readyAt: client.readyAt,

            serverCount: client.guilds.cache.size,
            userCount: client.users.cache.size,

            memory: {
                heapUsedMB,
                rssMB
            }
        } satisfies ClientInfoResponse)
    })
}
export default clientRoutes;