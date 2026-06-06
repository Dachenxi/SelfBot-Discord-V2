<script lang="ts">
    import './layout.css';
    import favicon from '$lib/assets/favicon.svg';
    import { page } from '$app/state';
    import Pill from '$lib/components/Pill.svelte';
    import ToastContainer from '$lib/components/ToastContainer.svelte';

    let { data, children } = $props();
    
    let isLoading = $state(true);
    
    let botName: string = $state('Bot');
    let botStatus: string = $state('Offline');
</script>

<svelte:head>
    <link rel="icon" href={data.clientInfo?.avatar || favicon} />
    <title>Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Cascadia+Code:ital,wght@0,200..700;1,200..700&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">
</svelte:head>

<div class="flex h-screen font-body antialiased bg-woodsmoke-950">
    <aside class="flex flex-col h-full w-64 bg-woodsmoke-900 border-r border-woodsmoke-700 p-4 shadow shadow-woodsmoke-900">
        <div class="group relative flex mb-5 items-center cursor-pointer p-2 -mx-2 rounded hover:bg-woodsmoke-800 transition-colors ease-in-out">
            {#if data.clientInfo?.avatar}
                <div class="relative w-14 h-14 shrink-0">
                    
                    {#if isLoading}
                        <div class="absolute inset-0 rounded-full bg-woodsmoke-900 border-2 border-woodsmoke-700 animate-pulse flex items-center justify-center z-10">
                            <span class="material-symbols--person-rounded text-3xl text-woodsmoke-400"></span>
                        </div>
                    {/if}
                    
                    <img 
                        src={data.clientInfo.avatar} 
                        alt="" 
                        onload={() => isLoading = false}
                        class="w-full h-full rounded-full bg-woodsmoke-900 border-2 border-woodsmoke-700 object-cover transition-opacity duration-300 {isLoading ? 'opacity-0' : 'opacity-100'}"
                    />
                    
                </div>
            {:else}
                <div class="w-14 h-14 shrink-0 rounded-full bg-woodsmoke-900 border-2 border-woodsmoke-700 flex items-center justify-center">
                    <span class="material-symbols--robot-2-outline text-3xl text-woodsmoke-400"></span>
                </div>
            {/if}
            <div class="flex flex-col justify-center ml-4 gap-1 overflow-hidden">
                <h1 class="text-lg font-medium font-mono text-white truncate w-full">
                    {data.clientInfo?.username || botName}
                </h1>
                <div class="flex items-center gap-1.5">
                    <p class="text-xs text-woodsmoke-400">Status:</p>
                    <Pill status={data.clientInfo?.status || botStatus} />
                </div>
            </div>
        </div>
        <div class="border-b border-woodsmoke-700"></div>
        
        <div class="flex-col">
            <nav class="mt-6">
                <ul>
                    <li class="mb-2">
                        <a href="/" class="flex items-center font-medium transition-colors ease-linear p-2 rounded-lg cursor-pointer w-full {page.url.pathname === '/' ? 'text-woodsmoke-200 bg-woodsmoke-800' : 'text-woodsmoke-200 hover:text-white hover:bg-woodsmoke-800'}">
                            <span class="material-symbols--dashboard-rounded text-2xl mr-2"></span>
                            Dashboard
                        </a>
                    </li>
                    
                    <li class="mb-2">
                        <a href="/setting" class="flex items-center font-medium transition-colors ease-linear p-2 rounded-lg cursor-pointer w-full {page.url.pathname === '/setting' ? 'text-woodsmoke-200 bg-woodsmoke-800' : 'text-woodsmoke-200 hover:text-white hover:bg-woodsmoke-800'}">
                            <span class="material-symbols--settings-rounded text-2xl mr-2"></span>
                            Settings
                        </a>
                    </li>
                    
                    <li class="mb-2">
                        <a href="/sniffer" class="flex items-center font-medium transition-colors ease-linear p-2 rounded-lg cursor-pointer w-full {page.url.pathname === '/sniffer' ? 'text-woodsmoke-200 bg-woodsmoke-800' : 'text-woodsmoke-200 hover:text-white hover:bg-woodsmoke-800'}">
                            <span class="material-symbols--coffee text-2xl mr-2"></span>
                            Sniffer
                        </a>
                    </li>
                    
                    <li class="mb-2">
                        <a href="/profile" class="flex items-center font-medium transition-colors ease-linear p-2 rounded-lg cursor-pointer w-full {page.url.pathname === '/profile' ? 'text-woodsmoke-200 bg-woodsmoke-800' : 'text-woodsmoke-200 hover:text-white hover:bg-woodsmoke-800'}">
                            <span class="material-symbols--person-rounded text-2xl mr-2"></span>
                            Profile
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    </aside>
    
    <main class="flex-1 flex flex-col h-full overflow-hidden">
        
        <div class="p-3">
            <h1 class="text-2xl font-semibold text-woodsmoke-100 items-center flex-col font-mono">
                {#if page.url.pathname === '/'}
                    <span>Dashboard</span>
                    <p class="text-sm text-woodsmoke-500">Berbagai info tentang bot yang sedang berjalan</p>
                {:else if page.url.pathname.startsWith('/setting')}
                    <span>Settings</span>
                    <p class="text-sm text-woodsmoke-500">Pengaturan client bot</p>
                {:else if page.url.pathname.startsWith('/sniffer')}
                    <span>Sniffer</span>
                    <p class="text-sm text-woodsmoke-500">Meneruskan pesan yang di terima</p>
                {:else if page.url.pathname.startsWith('/profile')}
                    <span>Profile</span>
                    <p class="text-sm text-woodsmoke-500">Lihat informasi akun kamu</p>
                {/if}
            </h1>
        </div>
        
        <div class="border-b border-woodsmoke-700"></div>

        <div class="flex-1 overflow-y-auto p-6">
            {@render children()}
        </div>
        
    </main>
</div>

<ToastContainer />