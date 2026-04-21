<script lang="ts">
    import { onMount } from 'svelte';
    import { fetchAPI } from '$lib/api';

    let goals: any[] = $state([]);
    let loading = $state(true);
    let showForm = $state(false);
    let newName = $state('');
    let newTarget = $state('');
    let newDate = $state(new Date().toISOString().split('T')[0]);

    onMount(async () => {
        try {
            goals = await fetchAPI('/goals/');
        } catch(e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });

    async function handleCreate(e: Event) {
        e.preventDefault();
        try {
            const res = await fetchAPI('/goals/', {
                method: 'POST',
                body: JSON.stringify({ name: newName, target_amount: newTarget, target_date: newDate })
            });
            goals = [res, ...goals];
            showForm = false;
            newName = '';
            newTarget = '';
        } catch(err) {
            alert("Error creating goal.");
        }
    }
</script>

<svelte:head>
    <title>Savings Goals - Financey</title>
</svelte:head>

<div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight">Savings Milestones</h2>
        <button onclick={() => showForm = !showForm} class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition shadow-md shadow-blue-500/20 text-sm">
            {showForm ? 'Cancel' : 'Add Milestone'}
        </button>
    </div>
    
    {#if showForm}
    <form onsubmit={handleCreate} class="mb-8 bg-slate-50 p-6 rounded-xl border border-slate-200">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="col-span-2">
                <label class="block text-sm font-medium text-slate-700 mb-1">Goal Name</label>
                <input required bind:value={newName} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" placeholder="e.g. New Car">
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Target Amount ($)</label>
                <input type="number" required bind:value={newTarget} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" placeholder="5000">
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Target Date</label>
                <input type="date" required bind:value={newDate} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
            </div>
            <div class="md:col-start-4 flex items-end">
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 rounded-lg transition shadow-md shadow-emerald-500/20 text-sm">Save Milestone</button>
            </div>
        </div>
    </form>
    {/if}

    {#if loading}
    <div class="text-slate-400">Loading records...</div>
    {:else}
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {#each goals as goal}
        <div class="p-6 border border-slate-200 rounded-xl hover:shadow-md transition">
            <h3 class="text-lg font-semibold text-slate-800">{goal.name}</h3>
            <p class="text-sm font-semibold text-blue-600 mb-4">${parseFloat(goal.target_amount).toLocaleString()}</p>
        </div>
        {:else}
        <div class="col-span-full py-12 text-center text-slate-500">No goals discovered.</div>
        {/each}
    </div>
    {/if}
</div>
