<script lang="ts">
    let { data } = $props();
</script>

<svelte:head>
    <title>Dashboard</title>
</svelte:head>

<div class="max-w-5xl">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 grow">
        <div class="p-6 bg-woodsmoke-900 border border-cloud-burst-900 rounded-xl  flex flex-col gap-3">
            <div class="bg-woodsmoke-800 p-2 inline-flex items-center gap-4 max-w-max border border-woodsmoke-700 ">
                <span class="material-symbols--dns text-3xl text-cloud-burst-500"></span>
            </div>
            <p class=" font-mono text-woodsmoke-500">Servers</p>
            <h2 class="text-3xl font-bold text-white">{data.clientInfo?.serverCount || 0}</h2>
        </div>
        <div class="p-6 bg-woodsmoke-900 border border-woodsmoke-700 rounded-xl  flex flex-col gap-3">
            <div class="bg-woodsmoke-800 p-2 inline-flex items-center gap-4 max-w-max border border-woodsmoke-700 ">
                <span class="material-symbols--person-rounded text-3xl text-cloud-burst-500"></span>
            </div>
            <p class=" font-mono text-woodsmoke-500">User</p>
            <h2 class="text-3xl font-bold text-white">{data.clientInfo?.userCount || 0}</h2>
        </div>
        <div class="p-6 bg-woodsmoke-900 border border-woodsmoke-700 rounded-xl flex flex-col gap-3">
            <div class="bg-woodsmoke-800 p-2 inline-flex items-center gap-4 max-w-max border border-woodsmoke-700 ">
                <span class="material-symbols--speed-rounded text-3xl text-cloud-burst-500"></span>
            </div>
            <p class=" font-mono text-woodsmoke-500">Ping</p>
            <h2 class="text-3xl font-bold text-white">{data.clientInfo?.ping || 0}</h2>
        </div>
        <div class="p-6 bg-woodsmoke-900 border border-woodsmoke-700 rounded-xl flex flex-col gap-3">
    
            <div class="bg-woodsmoke-800 p-2 inline-flex items-center gap-4 max-w-max border border-woodsmoke-700 rounded-md">
                <span class="material-symbols--memory text-3xl text-cloud-burst-500"></span>
            </div>
            
            <p class="font-mono text-woodsmoke-500">RAM Usage</p>
            
            <div class="flex items-baseline gap-1.5 -mt-1">
                <h2 class="text-3xl font-bold text-white">{data.clientInfo?.memory.heapUsedMB || 0}</h2>
                <span class="font-mono text-sm text-woodsmoke-500">MB</span>
            </div>

            <div class="flex flex-col gap-1.5 mt-auto pt-2">
                <div class="w-full bg-woodsmoke-950 border border-woodsmoke-800 rounded-full h-1.5">
                    <div 
                        class="bg-cloud-burst-500 h-1.5 rounded-full transition-all duration-500" 
                        style="width: {Math.min(((Number(data.clientInfo?.memory.heapUsedMB || 0)) / 512) * 100, 100)}%"
                    ></div>
                </div>
                <p class="text-[11px] font-mono text-woodsmoke-600">
                    Alokasi OS: {data.clientInfo?.memory.rssMB || 0} MB
                </p>
            </div>

        </div>
    </div>
    
</div>