import { client } from '../../bot/client.js';
import type { BotStatusResponse } from '../../../../shared/types.js';

async function getBotStatus(): Promise<BotStatusResponse> {
    return {
        isReady: client.isReady(),
        user: client.user?.displayName
    };
}

export { getBotStatus };