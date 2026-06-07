import { client, sendInfo } from "./bot/client.js";
import { prisma } from "./lib/prisma.js";
import { startWebServer } from "./api/server.js";
import { snifferCache } from "./lib/cache.js";

const args = process.argv.slice(2);
const runOnlyWeb = args.includes('--only-web');
const runOnlyBot = args.includes('--only-bot');

async function main() {
    try {
        if (!runOnlyBot) {
            console.log("Starting WebServer");
            await startWebServer();
            console.log("WebServer is running.");
        }
        if (!runOnlyWeb) {
            console.log("Starting SelfBot...");
            await client.login(process.env.DISCORD_TOKEN);
            console.log("SelfBot is running.");
        }

        console.log("Connecting to the database...");
        await prisma.$connect();
        console.log("Connected to the database.");
        
        //#region loading caches
        console.log("Loading caches...");
        const allSnifferConfigs = await prisma.sniff.findMany()
        for (const config of allSnifferConfigs) {
            snifferCache.set(config.channelId, config.webhookUrl);
        }
        
        console.log("Caches loaded.");
        //#endregion

    } catch (error) {
        console.error('❌ Terjadi kesalahan fatal saat startup aplikasi:', error);
        await client.destroy();
        await prisma.$disconnect();
        process.exit(1);
    }
    
}

process.on('SIGINT', async () => {
    await sendInfo('⚠️ SelfBot is shutting down gracefully...');
  console.log('\n[System] Mematikan aplikasi secara aman...');
  await prisma.$disconnect();
  process.exit(0);
});

main();