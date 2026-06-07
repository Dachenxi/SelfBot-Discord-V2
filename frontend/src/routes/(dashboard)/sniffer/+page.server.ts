import { fail } from '@sveltejs/kit'; // Wajib import fail
import { getApiUrl } from '$lib/api';
import type { ListSnifferConfigResponse, SaveSnifferConfigResponse } from '../../../../../shared/types';

export const load = async ({ fetch, cookies, parent }) => {
    await parent(); 
    const token = cookies.get('TOKEN');

    try {
        const response = await fetch(getApiUrl('/api/sniffer/config/list'), {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Gagal memuat sniffer');

        const result = await response.json() as ListSnifferConfigResponse;
        
        return { snifferList: result.data || [] }; 
    } catch (error) {
        return { snifferList: [] };
    }
};

export const actions = {
    addSniffer: async ({ request, cookies, fetch }) => {
        const token = cookies.get('TOKEN');

        if (!token) {
            // Gunakan fail(401) agar ditangkap sebagai failure oleh SvelteKit
            return fail(401, { message: 'Sesi tidak valid, silakan login ulang' });
        }

        const formData = await request.formData();
        const channelId = formData.get('channelId') as string;
        const webhookUrl = formData.get('webhookUrl') as string;

        try {
            const response = await fetch(getApiUrl('/api/sniffer/config/save'), {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ channelId, webhookUrl })
            });

            const result = await response.json() as SaveSnifferConfigResponse;
            
            if (!response.ok) {
                return fail(response.status, { message: result.message || 'Gagal menambahkan sniffer' });
            }
            
            return { success: true, message: 'Sniffer berhasil ditambahkan', newSniffer: result.data };

        } catch (error) {
            return fail(500, { message: 'Terjadi kesalahan saat menambahkan sniffer' });
        }
    }
};