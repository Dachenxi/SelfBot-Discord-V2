<script lang="ts">
    let { status = "Offline" } = $props<{ status: string }>();
</script>

{#if status === 'Online' || status === 'online'}
    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 select-none">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        Online
    </span>
{:else}
    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20 select-none">
        <span class="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
        Offline
    </span>
{/if}