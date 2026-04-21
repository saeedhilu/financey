<script lang="ts">
    import { onMount } from 'svelte';
    import { fetchAPI } from '$lib/api';

    let ledgers: any[] = $state([]);
    let loading = $state(true);
    let showForm = $state(false);
    let newName = $state('');
    let newClass = $state('EXPENSE');

    onMount(async () => {
        try {
            ledgers = await fetchAPI('/ledgers/');
        } catch(e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });

    async function handleCreate(e: Event) {
        e.preventDefault();
        try {
            const res = await fetchAPI('/ledgers/', {
                method: 'POST',
                body: JSON.stringify({ name: newName, ledger_class: newClass })
            });
            ledgers = [res, ...ledgers];
            showForm = false;
            newName = '';
        } catch(err) {
            alert("Error creating ledger.");
        }
    }
</script>

<svelte:head>
    <title>Ledgers - Financey</title>
</svelte:head>

<div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight">Accounts & Ledgers</h2>
        <button onclick={() => showForm = !showForm} class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition shadow-md shadow-blue-500/20 text-sm">
            {showForm ? 'Cancel' : 'Create Ledger'}
        </button>
    </div>
    
    {#if showForm}
    <form onsubmit={handleCreate} class="mb-8 bg-slate-50 p-6 rounded-xl border border-slate-200">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Ledger Name</label>
                <input required bind:value={newName} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" placeholder="e.g. Groceries">
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Class</label>
                <select bind:value={newClass} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-white">
                    <option value="ASSET">Asset (Bank/Cash)</option>
                    <option value="LIABILITY">Liability (Debt)</option>
                    <option value="INCOME">Income (Salary)</option>
                    <option value="EXPENSE">Expense (Food)</option>
                </select>
            </div>
            <div class="flex items-end">
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 text-sm rounded-lg transition shadow-md shadow-emerald-500/20">Save Ledger</button>
            </div>
        </div>
    </form>
    {/if}

    {#if loading}
    <div class="text-slate-400">Loading records...</div>
    {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each ledgers as ledger}
        <div class="p-6 border border-slate-200 rounded-xl hover:border-blue-300 transition">
            <p class="text-xs font-bold uppercase text-slate-400 mb-2 tracking-widest">{ledger.ledger_class}</p>
            <h3 class="text-lg font-semibold text-slate-800">{ledger.name}</h3>
        </div>
        {:else}
        <div class="col-span-full py-12 text-center text-slate-500">No ledgers constructed. Add an Income and Bank Asset ledger to get started!</div>
        {/each}
    </div>
    {/if}
</div>
