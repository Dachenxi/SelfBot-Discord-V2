<script lang="ts">
    import type { HTMLButtonAttributes } from 'svelte/elements';

    interface Props extends HTMLButtonAttributes {
        ButtonName?: string;
        Icon?: string;
        onlyIcon?: boolean;
        variant?: 'primary' | 'danger' | 'ghost' | 'warning'; // Tambahkan pilihan variant
    }

    let { 
        ButtonName = "Button", 
        Icon = "", 
        variant = 'primary', // Default-nya adalah primary
        onlyIcon = false,
        class: className = "", 
        ...rest 
    }: Props = $props();

    // Kamus warna berdasarkan variant
    const variantClasses = {
        primary: "bg-woodsmoke-800 hover:bg-woodsmoke-700 text-white border-woodsmoke-700",
        danger: "bg-falu-red-700 hover:bg-falu-red-800 text-white border-falu-red-600",
        ghost: "bg-transparent hover:bg-woodsmoke-800 text-woodsmoke-300 border-transparent",
        warning: "bg-amber-700 hover:bg-amber-800 text-white border-amber-600"
    };
</script>

<button 
    {...rest}
    class="px-4 py-2 rounded-lg font-medium transition-colors border inline-flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer {variantClasses[variant]} {className}"
>
    {#if Icon}
        <span class="material-symbols--{Icon} text-xl"></span>
    {/if}
    {#if !onlyIcon}
        {ButtonName}
    {/if}
</button>