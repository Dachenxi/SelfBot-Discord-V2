<script lang="ts">
    // Impor state global yang baru saja kita buat
    import { toastState } from '$lib/state/Toast.svelte';
</script>

<div class="fixed bottom-6 right-6 z-100 flex flex-col gap-3 pointer-events-none">
    {#each toastState.toasts as toast (toast.id)}
        <div class="pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-lg shadow-2xl border bg-woodsmoke-900 min-w-64 transition-all duration-300
            {toast.type === 'success' ? 'border-green-500/30' : 'border-red-500/30'}">
            
            {#if toast.type === 'success'}
                <span class="material-symbols--check-circle text-green-400 text-2xl"></span>
            {:else}
                <span class="material-symbols--error text-red-400 text-2xl"></span>
            {/if}
            
            <p class="text-sm font-medium text-woodsmoke-100">{toast.message}</p>
            
            <button 
                onclick={() => toastState.remove(toast.id)} 
                class="ml-auto text-woodsmoke-500 hover:text-white transition-colors"
                aria-label="Close notification"
            >
                <span class="material-symbols--close text-lg"></span>
            </button>
        </div>
    {/each}
</div>