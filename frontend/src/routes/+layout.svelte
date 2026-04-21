<script lang="ts">
  import '../app.css';
  import Sidebar from '$lib/components/Sidebar.svelte';
  import { page } from '$app/stores';
  
  let { children } = $props();
  
  let isAuthRoute = $derived($page.url.pathname === '/login' || $page.url.pathname === '/register');
  let mobileMenuOpen = $state(false);

  $effect(() => {
    $page.url.pathname;
    mobileMenuOpen = false;
  });
</script>

{#if isAuthRoute}
  <main class="min-h-screen bg-slate-50 flex items-center justify-center font-sans antialiased selection:bg-blue-500/30 p-4">
    {@render children()}
  </main>
{:else}
  <div class="flex h-screen bg-slate-50 font-sans text-slate-900 antialiased overflow-hidden selection:bg-blue-500/30">
    <!-- Desktop Sidebar -->
    <div class="hidden md:block fixed top-0 left-0 h-screen z-20">
      <Sidebar />
    </div>

    <!-- Mobile Sidebar overlay -->
    {#if mobileMenuOpen}
    <div class="fixed inset-0 bg-slate-900/50 z-30 md:hidden backdrop-blur-sm" onclick={() => mobileMenuOpen = false}></div>
    <div class="fixed inset-y-0 left-0 z-40 md:hidden shadow-2xl">
      <Sidebar />
    </div>
    {/if}

    <div class="flex-1 flex flex-col md:ml-64 relative w-full">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 md:px-6 sticky top-0 z-10 shadow-sm transition">
        <div class="flex flex-row items-center gap-3">
          <button onclick={() => mobileMenuOpen = true} class="md:hidden p-2 -ml-2 text-slate-500 hover:text-slate-700 transition rounded-lg">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </button>
          <h2 class="text-xl font-semibold text-slate-800 tracking-tight">Overview</h2>
        </div>
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
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-slate-50/50 p-4 md:p-8">
        {@render children()}
      </main>
    </div>
  </div>
{/if}
