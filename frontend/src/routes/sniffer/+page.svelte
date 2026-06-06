<script lang="ts">
    import { invalidate, invalidateAll } from "$app/navigation";
    import Button from "$lib/components/Button.svelte";
    import { toastState } from "$lib/state/Toast.svelte";
    import { slide } from 'svelte/transition';
    import { flip } from 'svelte/animate';
    
    let { data } = $props()

    let isModalAddOpen = $state(false);
    let isSubmitAdd = $state(false);

    let formChannelId = $state("");
    let formWebhookUrl = $state("");
    let showWebhook = $state(false);

    function openModalAdd() {
        isModalAddOpen = true;
    }

    function closeModalAdd(){
        isModalAddOpen = false;
        formChannelId = "";
        formWebhookUrl = "";
    }

    async function saveConfig(e: Event) {
        e.preventDefault();

        if (!formChannelId || !formWebhookUrl) { return }

        isSubmitAdd = true;
        try {
            const response = await fetch("http://localhost:3000/api/sniffer/config/save", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    channelId: formChannelId,
                    webhookUrl: formWebhookUrl
                })
            })

            const result = await response.json();

            if(response.ok) {
                toastState.add("Berhasil menambahkan Sniffer!", "success");
                closeModalAdd()
                invalidateAll();
            }
        } catch (error) {
            toastState.add("Gagal menambahkan Sniffer!", "error");
        } finally {
            isSubmitAdd = false;
        }
    }

    let searchQuery = $state("");

    let filteredSniffers = $derived(
        data.snifferList?.filter(sniffer => 
            sniffer.channelId.includes(searchQuery) || 
            sniffer.channelName.toLowerCase().includes(searchQuery.toLowerCase())
        )
    );
</script>

<svelte:head>
    <title>Sniffer</title>
</svelte:head>

<div class="flex flex-col gap-3">
    <div class="bg-woodsmoke-900 border border-woodsmoke-700 p-2 font-mono rounded flex justify-between">
        <div class="relative w-full max-w-sm">
    
            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <span class="material-symbols--search text-xl text-woodsmoke-400"></span>
            </div>

            <input 
                type="text" 
                placeholder="Channel ID" 
                bind:value={searchQuery}
                class="w-full pl-10 pr-4 py-2 bg-woodsmoke-900 border border-woodsmoke-700 rounded-md text-woodsmoke-200 placeholder-woodsmoke-500 focus:outline-none focus:border-woodsmoke-500 focus:ring-1 focus:ring-woodsmoke-500 transition-colors"
            />
        </div>
        <Button ButtonName="Add New Sniffer" variant="primary" class="ml-2" Icon="add" onclick={openModalAdd}/>
    </div>
    <div class="overflow-hidden rounded-lg border border-woodsmoke-700 bg-woodsmoke-900">
        
        <div class="grid grid-cols-4 bg-woodsmoke-800 text-woodsmoke-400 font-mono divide-x divide-woodsmoke-700 border-b border-woodsmoke-700">
            <div class="px-4 py-3 font-semibold">Channel Name</div>
            <div class="px-4 py-3 font-semibold">Channel ID</div>
            <div class="px-4 py-3 font-semibold">Created At</div>
            <div class="px-4 py-3 font-semibold text-center">Actions</div>
        </div>

        <div class="divide-y divide-woodsmoke-700">
            {#each filteredSniffers as sniffer (sniffer.channelId)}
                
                <div 
                    transition:slide={{ duration: 200 }} 
                    animate:flip={{ duration: 300 }}
                    class="grid grid-cols-4 items-center hover:bg-woodsmoke-800 transition-colors font-mono text-woodsmoke-300"
                >
                    <div class="px-4 py-3 truncate">{sniffer.channelName}</div>
                    <div class="px-4 py-3 truncate">{sniffer.channelId}</div>
                    <div class="px-4 py-3 truncate">{new Date(sniffer.createdAt).toLocaleString()}</div>
                    <div class="px-4 py-3 flex justify-center gap-2">
                        <Button ButtonName="" variant="warning" Icon="edit" class="px-2" onlyIcon={true} />
                        <Button ButtonName="" variant="danger" Icon="delete" class="px-2" onlyIcon={true} />
                    </div>
                </div>
                
            {:else}
                <div transition:slide={{ duration: 300 }} class="px-4 py-8 text-center text-woodsmoke-500 font-mono">
                    {#if searchQuery}
                        Tidak ada sniffer yang cocok dengan "{searchQuery}"
                    {:else}
                        Data sniffer kosong.
                    {/if}
                </div>
            {/each}
        </div>
        
</div>
</div>
{#if isModalAddOpen}
    <div class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto overflow-x-hidden bg-black/60 backdrop-blur-sm transition-opacity">
        
        <div class="relative w-full max-w-lg p-4">
            <div class="relative bg-woodsmoke-900 border border-woodsmoke-700 rounded-xl shadow-2xl overflow-hidden">
                
                <div class="flex items-center justify-between p-4 border-b border-woodsmoke-700 bg-woodsmoke-950/50">
                    <h3 class="text-xl font-semibold text-white flex items-center gap-2">
                        <span class="material-symbols--add-link text-cloud-burst-400"></span>
                        Register Sniffer
                    </h3>
                    <button onclick={closeModalAdd} class="text-woodsmoke-400 hover:text-white transition-colors " aria-label="Close Modal">
                        <span class="material-symbols--close text-2xl"></span>
                    </button>
                </div>

                <form onsubmit={saveConfig} class="p-6 flex flex-col gap-5">
                    
                    <div>
                        <label for="channelId" class="block mb-2 text-sm font-medium text-woodsmoke-300">Channel ID Discord</label>
                        <input 
                            type="text" 
                            id="channelId"
                            bind:value={formChannelId}
                            autocomplete="off"
                            required
                            placeholder="Contoh: 1171172048756822056" 
                            class="w-full px-4 py-2.5 bg-woodsmoke-950 border border-woodsmoke-700 rounded-lg text-white focus:outline-none focus:border-cloud-burst-500 focus:ring-1 focus:ring-cloud-burst-500 transition-colors font-mono text-sm"
                        />
                    </div>

                    <div>
                        <label for="webhookUrl" class="block mb-2 text-sm font-medium text-woodsmoke-300">Webhook URL</label>
                        
                        <div class="relative w-full">
                            <input 
                                id="webhookUrl"
                                required
                                bind:value={formWebhookUrl}
                                placeholder="https://discord.com/api/webhooks/..." 
                                
                                type={showWebhook ? "text" : "password"} 
                                
                                class="w-full pl-4 pr-10 py-2.5 bg-woodsmoke-950 border border-woodsmoke-700 rounded-lg text-white focus:outline-none focus:border-cloud-burst-500 focus:ring-1 focus:ring-cloud-burst-500 transition-colors font-mono text-sm"
                            />
                            
                            <button 
                                type="button" 
                                onclick={() => showWebhook = !showWebhook}
                                class="absolute inset-y-0 right-0 flex items-center pr-3 text-woodsmoke-400 hover:text-white focus:outline-none"
                                aria-label={showWebhook ? "Hide Webhook URL" : "Show Webhook URL"}
                            >
                                <span class="material-symbols--{showWebhook ? 'visibility-off' : 'visibility'} text-xl"></span>
                            </button>
                        </div>
                        
                        <p class="mt-2 text-xs text-woodsmoke-500">URL webhook rahasia dari integrasi Discord.</p>
                    </div>

                    <div class="flex justify-end gap-3 mt-2 pt-4 border-t border-woodsmoke-700">
                        <Button 
                            type="button" 
                            ButtonName="Batal" 
                            class="bg-transparent hover:bg-woodsmoke-800 text-woodsmoke-300 border-transparent" 
                            onclick={closeModalAdd} 
                            disabled={isSubmitAdd} 
                        />
                        <Button 
                            type="submit" 
                            ButtonName={isSubmitAdd ? "Menyimpan..." : "Simpan Konfigurasi"} 
                            variant="primary" 
                            Icon={isSubmitAdd ? "sync" : "save"} 
                            disabled={isSubmitAdd} 
                        />
                    </div>

                </form>
            </div>
        </div>

    </div>
{/if}