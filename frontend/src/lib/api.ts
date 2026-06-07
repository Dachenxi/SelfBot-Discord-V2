import { browser } from '$app/environment';
import { PUBLIC_API_URL } from '$env/static/public';

export const AUTH_TOKEN_KEY = 'TOKEN';

export function getApiUrl(endpoint: string) {
    const baseUrl = PUBLIC_API_URL || (!browser ? 'http://localhost:3000' : 'http://backend:3000')
    
    if (endpoint.startsWith('/')) {
        return `${baseUrl}${endpoint}`;
    }
    
    return `${baseUrl}/${endpoint}`;
}

export function getAuthToken() {
    if (!browser) {
        return null;
    }

    const cookieMatch = document.cookie.match(new RegExp(`(?:^|; )${AUTH_TOKEN_KEY}=([^;]*)`));
    return localStorage.getItem(AUTH_TOKEN_KEY) ?? (cookieMatch ? decodeURIComponent(cookieMatch[1]) : null);
}

export function setAuthToken(token: string) {
    if (!browser) {
        return;
    }

    localStorage.setItem(AUTH_TOKEN_KEY, token);
    document.cookie = `${AUTH_TOKEN_KEY}=${encodeURIComponent(token)}; Path=/; Max-Age=${60 * 60 * 24 * 7}; SameSite=Lax`;
}

export function clearAuthToken() {
    if (!browser) {
        return;
    }

    localStorage.removeItem(AUTH_TOKEN_KEY);
    document.cookie = `${AUTH_TOKEN_KEY}=; Path=/; Max-Age=0; SameSite=Lax`;
}

export async function apiFetch(endpoint: string, init: RequestInit = {}) {
    const headers = new Headers(init.headers);
    const token = getAuthToken();

    if (token && !headers.has('Authorization')) {
        headers.set('Authorization', `Bearer ${token}`);
    }

    return fetch(getApiUrl(endpoint), {
        ...init,
        headers
    });
}