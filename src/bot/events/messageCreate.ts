import { Message, WebhookClient } from "discord.js-selfbot-v13";
import { client, sendInfo } from "../client";
import { snifferCache } from "../../lib/cache";

const messageCreate = async (message: Message) => {
    if (message.author.id == client.user?.id) return;
    const webhookUrl = snifferCache.get(message.channelId);
    if (!webhookUrl) return;

    try {
        const webhookClient = new WebhookClient({ url: webhookUrl });
        const payload: any = {
            username: message.author.username,
            avatarURL: message.author.displayAvatarURL(),
        };

        if (!message.author.bot) {
            payload.username = `${message.author.displayName}`;
        }

        if (message.content && message.content.trim().length > 0) {
            payload.content = message.content;
        }

        if (message.embeds.length > 0) {
            payload.embeds = message.embeds.map(embed => embed.toJSON());
        }

        if (!payload.content && !payload.embeds) {
            console.log('[Sniffer] Pesan diabaikan (kosong/tidak ada konten/embed)');
            return;
        }

        await webhookClient.send(payload);
    
    } catch (error) {
        console.error('[Sniffer] Terjadi kesalahan saat mengirim pesan ke webhook:', error);
        
        await sendInfo(`⚠️ Terjadi kesalahan saat mengirim pesan dari channel <#${message.channelId}> ke webhook. Error: ${error instanceof Error ? error.message : String(error)}`);
    }
}

export default messageCreate;