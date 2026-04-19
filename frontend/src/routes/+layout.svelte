<script lang="ts">
  import '../app.css';
  import Sidebar from '$lib/components/Sidebar.svelte';
  import { page } from '$app/stores';
  
  let { children } = $props();
  
  let isAuthRoute = $derived($page.url.pathname === '/login' || $page.url.pathname === '/register');
</script>

{#if isAuthRoute}
  <main class="min-h-screen bg-slate-50 flex items-center justify-center font-sans antialiased selection:bg-blue-500/30 p-4">
    {@render children()}
  </main>
{:else}
  <div class="flex h-screen bg-slate-50 font-sans text-slate-900 antialiased overflow-hidden selection:bg-blue-500/30">
    <Sidebar />
    <div class="flex-1 flex flex-col md:ml-64 relative">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 sticky top-0 z-10 shadow-sm transition">
        <h2 class="text-xl font-semibold text-slate-800 tracking-tight">Overview</h2>
        <div class="flex items-center space-x-4">
          <button class="relative p-2 text-slate-400 hover:text-slate-600 transition outline-none rounded-full focus:bg-slate-100">
            <span class="absolute top-1 right-1 w-2 h-2 bg-rose-500 rounded-full"></span>
            🔔
          </button>
          <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-indigo-600 text-white flex items-center justify-center font-semibold text-sm shadow-md cursor-pointer" onclick={() => {localStorage.removeItem('access_token'); window.location.href='/login';}}>
            ⏻
          </div>
        </div>
      </header>
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-slate-50/50 p-8">
        {@render children()}
      </main>
    </div>
  </div>
{/if}
