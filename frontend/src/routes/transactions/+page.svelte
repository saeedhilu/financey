<script lang="ts">
    import { onMount } from 'svelte';
    import { fetchAPI } from '$lib/api';

    let transactions: any[] = $state([]);
    let ledgers: any[] = $state([]);
    let loading = $state(true);
    let showForm = $state(false);

    let newNotes = $state('');
    let newAmount = $state('');
    let newDate = $state(new Date().toISOString().split('T')[0]);
    let newCredit = $state('');
    let newDebit = $state('');

    onMount(async () => {
        try {
            transactions = await fetchAPI('/transactions/entries/');
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
            const res = await fetchAPI('/transactions/entries/', {
                method: 'POST',
                body: JSON.stringify({ 
                    amount: newAmount, 
                    date: newDate, 
                    notes: newNotes, 
                    credit_ledger: newCredit, 
                    debit_ledger: newDebit 
                })
            });
            transactions = [res, ...transactions];
            showForm = false;
            newNotes = '';
            newAmount = '';
        } catch(err) {
            alert("Error creating transaction.");
        }
    }
</script>

<svelte:head>
    <title>Transactions - Financey</title>
</svelte:head>

<div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight">Ledger Transactions</h2>
        <button onclick={() => showForm = !showForm} class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition shadow-md shadow-blue-500/20 text-sm">
            {showForm ? 'Cancel' : 'New Entry'}
        </button>
    </div>
    
    {#if showForm}
    <form onsubmit={handleCreate} class="mb-8 bg-slate-50 p-6 rounded-xl border border-slate-200">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Memo/Notes</label>
                <input required bind:value={newNotes} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" placeholder="e.g. Target Shopping">
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Amount ($)</label>
                <input type="number" step="0.01" required bind:value={newAmount} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" placeholder="240.50">
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Withdraw From (Credit)</label>
                <select required bind:value={newCredit} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500 bg-white">
                    <option value="" disabled selected>Select Ledger</option>
                    {#each ledgers as ld}
                    <option value={ld.id}>{ld.name} ({ld.ledger_class})</option>
                    {/each}
                </select>
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Deposit To (Debit)</label>
                 <select required bind:value={newDebit} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500 bg-white">
                    <option value="" disabled selected>Select Ledger</option>
                    {#each ledgers as ld}
                    <option value={ld.id}>{ld.name} ({ld.ledger_class})</option>
                    {/each}
                </select>
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Date</label>
                <input type="date" required bind:value={newDate} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-blue-500">
            </div>
            <div class="flex items-end">
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 rounded-lg transition shadow-md shadow-emerald-500/20 text-sm">Post Transaction</button>
            </div>
        </div>
    </form>
    {/if}

    {#if loading}
    <div class="text-slate-400">Loading records...</div>
    {:else}
    <div class="divide-y divide-slate-100">
        {#each transactions as tx}
        <div class="py-4 flex justify-between items-center group">
            <div>
                <p class="font-semibold text-slate-800">{tx.notes || 'Uncategorized'}</p>
                <p class="text-sm text-slate-500">{tx.date}</p>
            </div>
            <span class="font-bold {parseFloat(tx.amount) > 0 ? 'text-rose-500' : 'text-slate-800'}">${parseFloat(tx.amount).toLocaleString()}</span>
        </div>
        {:else}
        <div class="py-12 text-center text-slate-500">No transactions recorded yet. Remember to create your income and expense ledgers first!</div>
        {/each}
    </div>
    {/if}
</div>
