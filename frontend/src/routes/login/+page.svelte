<script lang="ts">
    import '../layout.css'
    import { enhance } from '$app/forms';
    import ToastContainer from '$lib/components/ToastContainer.svelte';

    // $props() ini otomatis menangkap balikan fail() dari +page.server.ts
    let { form } = $props();

    // Kita tetap mempertahankan $state agar UI (seperti border merah) langsung reaktif saat diketik
    let username = $state(''); 
    let password = $state('');

</script>

<svelte:head>
    <title>Login</title>
</svelte:head>

<div class="h-screen bg-woodsmoke-950 px-4 text-woodsmoke-100 flex items-center justify-center font-body overflow-y-auto">
    <div class="w-full max-w-md border border-woodsmoke-700 bg-woodsmoke-900 shadow-lg shadow-black/20 rounded-md p-6 sm:p-8">
        
        <div class="flex flex-col gap-2">
            <h1 class="text-2xl font-bold text-white">Login</h1>
            <p class="text-sm text-woodsmoke-400 font-mono">Masukkan username dan password untuk masuk ke dashboard.</p>
        </div>
        <div class="border-2 border-woodsmoke-700 my-3"></div>
        {#if form?.message}
            <div class="mb-5 border border-falu-red-800 bg-falu-red-950/40 px-4 py-3 text-sm text-falu-red-200 rounded-md">
                {form.message}
            </div>
        {/if}

        <form class="space-y-4" method="POST" use:enhance novalidate>
            <div>
                <label for="username" class="mb-2 block text-sm font-medium text-woodsmoke-300">Username</label>
                <input
                    id="username"
                    name="username"  type="text"
                    bind:value={username}
                    placeholder="Username"
                    autocomplete="username"
                    aria-invalid={form?.usernameError ? 'true' : 'false'}
                    class="w-full rounded-md border bg-woodsmoke-950 px-3 py-2.5 font-mono text-sm text-white placeholder-woodsmoke-500 focus:outline-none focus:ring-1 {form?.usernameError ? 'border-falu-red-700 focus:border-falu-red-500 focus:ring-falu-red-500' : 'border-woodsmoke-700 focus:border-cloud-burst-500 focus:ring-cloud-burst-500'}"
                />
                {#if form?.usernameError}
                    <p class="mt-2 text-xs text-falu-red-300">{form.usernameError}</p>
                {/if}
            </div>

            <div>
                <label for="password" class="mb-2 block text-sm font-medium text-woodsmoke-300">Password</label>
                <input
                    id="password"
                    name="password" type="password"
                    bind:value={password}
                    placeholder="Password"
                    autocomplete="current-password"
                    aria-invalid={form?.passwordError ? 'true' : 'false'}
                    class="w-full rounded-md border bg-woodsmoke-950 px-3 py-2.5 font-mono text-sm text-white placeholder-woodsmoke-500 focus:outline-none focus:ring-1 {form?.passwordError ? 'border-falu-red-700 focus:border-falu-red-500 focus:ring-falu-red-500' : 'border-woodsmoke-700 focus:border-cloud-burst-500 focus:ring-cloud-burst-500'}"
                />
                {#if form?.passwordError}
                    <p class="mt-2 text-xs text-falu-red-300">{form.passwordError}</p>
                {/if}
            </div>
            <div class="border-2 border-woodsmoke-700 my-3"></div>
            <button
                type="submit"
                class="w-full rounded-md border border-woodsmoke-700 bg-woodsmoke-800 px-4 py-2.5 font-medium text-white transition-colors hover:bg-woodsmoke-700 focus:outline-none focus:ring-1 focus:ring-cloud-burst-500"
            >
                Masuk
            </button>
        </form>
    </div>
</div>

<ToastContainer />