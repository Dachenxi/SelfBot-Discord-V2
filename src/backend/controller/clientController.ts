import { client } from '../../bot/client';
import type { BotStatusResponse } from '../../../shared/types';

async function getBotStatus(): Promise<BotStatusResponse> {
    return {
        isReady: client.isReady(),
        user: client.user?.displayName
    };
}

export { getBotStatus };