import { client } from "../../bot/client";
import { FastifyPluginAsync } from "fastify";
import { prisma } from "../../lib/prisma";
import { TextChannel } from "discord.js-selfbot-v13";
import { snifferCache } from "../../lib/cache";
import type {
    ApiErrorResponse,
    ListSnifferConfigResponse,
    SaveSnifferConfigBody,
    SaveSnifferConfigResponse,
} from "../../../shared/types";

const snifferRoutes: FastifyPluginAsync = async (fastify) => {
    fastify.post('/config/save', async (request, reply) => {
        const { channelId, webhookUrl } = request.body as SaveSnifferConfigBody;

        if (!channelId || !webhookUrl) {
            return reply.status(400).send({
                success: false,
                error: 'channelId and webhookUrl are required'
            } satisfies ApiErrorResponse);
        }

        const channelName = await client?.channels.cache.get(channelId) as TextChannel | undefined;
        if (!channelName) {
            return reply.status(404).send({
                success: false,
                error: 'Channel not found'
            } satisfies ApiErrorResponse);
        }

        try {
            const config = await prisma.sniff.upsert({
                where: { channelId },
                update: { webhookUrl, channelName: channelName.name },
                create: { channelId, webhookUrl, channelName: channelName.name }
            });

            snifferCache.set(channelId, webhookUrl);

            return reply.status(200).send({
                success: true,
                message: 'Configuration saved successfully',
                data: config
            } satisfies SaveSnifferConfigResponse);
        } catch (error) {
            return reply.status(500).send({
                success: false,
                message: 'Failed to save configuration',
            } satisfies ApiErrorResponse)
        }

        })
    
    fastify.get('/config/list', async (request, reply) => {
        try {
            const listConfig = await prisma.sniff.findMany({
                orderBy: {
                    createdAt: 'desc'
                }
            })
            return reply.status(200).send({
                success: true,
                message: 'Configuration list retrieved successfully',
                data: listConfig
            } satisfies ListSnifferConfigResponse);
        } catch (error) {
            return reply.status(500).send({
                success: false,
                message: 'Failed to retrieve configuration list',
            } satisfies ApiErrorResponse)
        }})
    };

export default snifferRoutes;