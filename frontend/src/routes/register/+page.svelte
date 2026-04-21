<script lang="ts">
    import { fetchAPI } from '$lib/api';

    let username = $state('');
    let password = $state('');
    let email = $state('');
    let error = $state('');

    async function handleRegister(e: Event) {
        e.preventDefault();
        error = '';
        try {
            await fetchAPI('/auth/register/', {
                method: 'POST',
                body: JSON.stringify({ username, email, password })
            });
            // Auto login after register
            const data = await fetchAPI('/auth/token/', {
                method: 'POST',
                body: JSON.stringify({ username, password })
            });
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            window.location.href = '/';
        } catch (err: any) {
            error = err.data ? JSON.stringify(err.data) : 'Registration failed';
        }
    }
</script>

<div class="w-full max-w-md bg-white rounded-2xl shadow-xl border border-slate-100 p-8 animate-in slide-in-from-bottom-4 duration-500">
    <div class="text-center mb-8">
        <h2 class="text-2xl font-extrabold text-slate-800">Create an Account</h2>
        <p class="text-slate-500 text-sm mt-2">Join Financey to manage your wealth.</p>
    </div>
    
    {#if error}
    <div class="mb-4 bg-rose-50 text-rose-500 p-3 rounded-lg text-sm font-medium">{error}</div>
    {/if}

    <form onsubmit={handleRegister} class="space-y-5">
        <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Username</label>
            <input type="text" bind:value={username} required class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" placeholder="johndoe">
        </div>
        <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
            <input type="email" bind:value={email} required class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" placeholder="john@example.com">
        </div>
        <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Password</label>
            <input type="password" bind:value={password} required class="w-full px-4 py-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" placeholder="••••••••">
        </div>
        
        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl shadow-lg shadow-blue-500/30 transition transform hover:-translate-y-0.5">Register</button>
    </form>
    
    <p class="text-center text-sm text-slate-500 mt-6">
        Already have an account? <a href="/login" class="text-blue-600 font-semibold hover:underline">Sign In</a>
    </p>
</div>
