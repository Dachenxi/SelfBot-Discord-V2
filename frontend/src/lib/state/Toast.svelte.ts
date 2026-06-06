// src/lib/state/toast.svelte.ts

export type Toast = { 
    id: number; 
    message: string; 
    type: 'success' | 'error' 
};

// Bungkus $state di dalam objek agar mudah diekspor
export const toastState = $state({
    toasts: [] as Toast[],
    
    // Fungsi untuk menambah notifikasi
    add(message: string, type: 'success' | 'error' = 'success') {
        const id = Date.now(); // Gunakan timestamp agar ID selalu unik
        this.toasts.push({ id, message, type });
        
        // Hapus otomatis setelah 3 detik
        setTimeout(() => {
            this.remove(id);
        }, 3000);
    },

    // Fungsi untuk menghapus notifikasi manual
    remove(id: number) {
        this.toasts = this.toasts.filter(t => t.id !== id);
    }
});