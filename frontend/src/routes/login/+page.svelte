<script lang="ts">
    import { fetchAPI } from '$lib/api';

    let username = $state('');
    let password = $state('');
    let error = $state('');

    async function handleLogin(e: Event) {
        e.preventDefault();
        error = '';
        try {
            const data = await fetchAPI('/auth/token/', {
                method: 'POST',
                body: JSON.stringify({ username, password })
            });
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            window.location.href = '/';
        } catch (err: any) {
            error = 'Invalid username or password';
        }
    }
</script>

<svelte:head>
    <title>Login - Financey</title>
</svelte:head>

<div class="w-full max-w-md bg-white rounded-2xl shadow-xl border border-slate-100 p-8 animate-in slide-in-from-bottom-4 duration-500">
    <div class="text-center mb-8">
        <h2 class="text-2xl font-extrabold text-slate-800">Welcome Back</h2>
        <p class="text-slate-500 text-sm mt-2">Sign in to your Financey dashboard.</p>
    </div>
    
    {#if error}
    <div class="mb-4 bg-rose-50 text-rose-500 p-3 rounded-lg text-sm font-medium">{error}</div>
    {/if}

    <form onsubmit={handleLogin} class="space-y-5">
        <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Username</label>
            <input type="text" bind:value={username} required class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" placeholder="Enter your username">
        </div>
        <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Password</label>
            <input type="password" bind:value={password} required class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" placeholder="••••••••">
        </div>
        
        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl shadow-lg shadow-blue-500/30 transition transform hover:-translate-y-0.5">Sign In</button>
    </form>
    
    <p class="text-center text-sm text-slate-500 mt-6">
        Don't have an account? <a href="/register" class="text-blue-600 font-semibold hover:underline">Register</a>
    </p>
</div>
