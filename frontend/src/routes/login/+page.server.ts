import { fail, redirect, isRedirect } from '@sveltejs/kit';
import { getApiUrl } from '$lib/api';
import type { Actions } from './$types';
import  type { AuthResponse } from '../../../../shared/types.js';

export const actions: Actions = {
    default: async ({ request, cookies }) => {
        const formData = await request.formData();
        const username = formData.get('username');
        const password = formData.get('password');
        
        if (!username || !password) {
            return fail(400, {
                message: 'Mohon isi semua kolom',
                usernameError: !username ? 'Username wajib diisi' : '',
                passwordError: !password ? 'Password wajib diisi' : ''
            });
        }

        try {
            // 1. Tembak ke Fastify backend
            const res = await fetch(getApiUrl('/api/auth/login'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json() as AuthResponse;

            if (data.success) {
                // 2. SIMPAN DI COOKIE (Aman & Mendukung SSR)
                cookies.set('TOKEN', data.token, {
                    path: '/',
                    httpOnly: true, // Tidak bisa dicuri via Javascript (anti-XSS)
                    secure: process.env.NODE_ENV === 'production', 
                    sameSite: 'strict',
                    maxAge: 60 * 60 * 24 // Berlaku 1 hari
                });

                // 3. Lempar langsung ke halaman sniffer
                throw redirect(303, '/');
            }

            return fail(400, {
                message: data.message || 'Gagal login',
                usernameError: '',
                passwordError: ''
            });
        } catch (error) {
            if (isRedirect(error)) {
                throw error;
            }
            return fail(500, {
                message: 'Gagal terhubung ke server backend',
                usernameError: '',
                passwordError: '' 
            });
        }
    }
};