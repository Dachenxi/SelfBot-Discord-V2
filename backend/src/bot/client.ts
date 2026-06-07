import { Client, WebhookClient } from "discord.js-selfbot-v13";
import messageCreate from "./events/messageCreate.js";

const client = new Client();

const webhookInfoClient = process.env.INFO_WEBHOOK ? new WebhookClient({ url: process.env.INFO_WEBHOOK }) : null;


client.login(process.env.DISCORD_TOKEN).catch((error) => {
    console.error("Failed to login:", error);
    process.exit(1);
});

const sendInfo = async (message: string) => {
    await webhookInfoClient?.send({
        username: "SelfBot Info",
        content: message
    });
}

client.on('ready', async () => {
    if (!client.user) { return; }
    await sendInfo(`✅ ${client.user.username} has started successfully!`);
    console.log(`${client.user.username} is ready!`);
});
client.on('messageCreate', messageCreate);

export { client, sendInfo };