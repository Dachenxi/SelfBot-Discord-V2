import type { ClientInfoResponse } from '../../../shared/types';

export const load = async ({ fetch }) => {
    try {
        const response = await fetch('http://localhost:3000/api/client/info');

        if (!response.ok) {
            throw new Error('Failed to fetch dashboard data');
        }

        const data = await response.json();
        return { clientInfo: data as ClientInfoResponse };
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        return { clientInfo: null };
    }

}
