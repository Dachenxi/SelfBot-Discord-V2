import type { ListSnifferConfigResponse } from '../../../../shared/types.js';

export const load = async ({ fetch, depends }) => {
    depends('api:sniffer')

    try {
        const response = await fetch('http://localhost:3000/api/sniffer/config/list');
        const data = await response.json() as ListSnifferConfigResponse;
        return { 
            snifferList: data.data || [] 
        };
    } catch (error) {
        console.error('Error fetching sniffer config:', error);
    }
}