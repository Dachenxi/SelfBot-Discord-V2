import { redirect } from '@sveltejs/kit';
import { getApiUrl } from '$lib/api';
import type { ClientInfoResponse } from '../../../../shared/types.js';

export const load = async ({ fetch, cookies }) => {
    // 1. Ambil token langsung dari Cookie di Sisi Server
    const token = cookies.get('TOKEN');

    // 2. Jika token tidak ada, langsung tendang balik ke halaman login sebelum halaman sempat dimuat
    if (!token) {
        throw redirect(302, '/login');
    }

    try {
        const response = await fetch(getApiUrl('/api/client/info'), {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                // Token kadaluarsa, hapus cookie lalu lempar ke login
                cookies.delete('TOKEN', { path: '/' });
                throw redirect(302, '/login');
            }
            throw new Error();
        }

        const result = await response.json() as ClientInfoResponse;
        return { clientInfo: result || null };

    } catch (error: any) {
        if (error.status === 302) throw error;
        return { clientInfo: null };
    }
};