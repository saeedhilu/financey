<script lang="ts">
    import { onMount } from 'svelte';
    import { fetchAPI } from '$lib/api';

    let emiPlans: any[] = $state([]);
    let ledgers: any[] = $state([]);
    let loading = $state(true);
    let showForm = $state(false);

    let newName = $state('');
    let newAmount = $state('');
    let newMonths = $state('');
    let newLiab = $state('');
    let newDeduct = $state('');
    let newDate = $state(new Date().toISOString().split('T')[0]);

    onMount(async () => {
        try {
            emiPlans = await fetchAPI('/entries/emi-plans/');
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
            const res = await fetchAPI('/entries/emi-plans/', {
                method: 'POST',
                body: JSON.stringify({ 
                    name: newName, 
                    total_months: newMonths, 
                    emi_amount: newAmount, 
                    liability_ledger: newLiab, 
                    deduct_from_ledger: newDeduct, 
                    start_date: newDate 
                })
            });
            emiPlans = [res, ...emiPlans];
            showForm = false;
        } catch(err) {
            alert("Error creating EMI Plan.");
        }
    }

    async function payEMI(id: number) {
        try {
            const res = await fetchAPI(`/entries/emi-plans/${id}/pay/`, { method: 'POST' });
            emiPlans = emiPlans.map(p => p.id === id ? res : p);
        } catch(e) {
            alert("Failed to pay EMI installment.");
        }
    }
</script>

<svelte:head>
    <title>EMI Plans - Financey</title>
</svelte:head>

<div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight">EMI Schedules</h2>
        <button onclick={() => showForm = !showForm} class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition shadow-md shadow-indigo-500/20 text-sm">
            {showForm ? 'Cancel' : 'Register EMI'}
        </button>
    </div>
    
    {#if showForm}
    <form onsubmit={handleCreate} class="mb-8 bg-slate-50 p-6 rounded-xl border border-slate-200">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="col-span-full">
                <label class="block text-sm font-medium text-slate-700 mb-1">Plan Name (e.g. Car Loan)</label>
                <input required bind:value={newName} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500">
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Monthly Amount ($)</label>
                <input type="number" step="0.01" required bind:value={newAmount} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-indigo-500">
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Total Duration (Months)</label>
                <input type="number" required bind:value={newMonths} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-indigo-500" placeholder="12 or 14">
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Liability Ledger (Debt Account)</label>
                <select required bind:value={newLiab} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-indigo-500 bg-white">
                    <option value="" disabled selected>Select Liability</option>
                    {#each ledgers.filter(l => l.ledger_class?.toUpperCase() === 'LIABILITY') as ld}
                    <option value={ld.id}>{ld.name}</option>
                    {/each}
                </select>
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Deduct From (Bank Account)</label>
                 <select required bind:value={newDeduct} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-indigo-500 bg-white">
                    <option value="" disabled selected>Select Asset</option>
                    {#each ledgers.filter(l => l.ledger_class?.toUpperCase() === 'ASSET') as ld}
                    <option value={ld.id}>{ld.name}</option>
                    {/each}
                </select>
            </div>
            <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">Start Date</label>
                <input type="date" required bind:value={newDate} class="w-full border border-slate-300 rounded-lg p-2 outline-none focus:border-indigo-500">
            </div>
            <div class="flex items-end">
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 rounded-lg transition shadow-md shadow-emerald-500/20 text-sm">Save Plan</button>
            </div>
        </div>
    </form>
    {/if}

    {#if loading}
    <div class="text-slate-400">Loading records...</div>
    {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        {#each emiPlans as plan}
        <div class="p-6 border border-slate-200 rounded-xl hover:shadow-md transition relative overflow-hidden bg-white">
            <div class={`absolute top-0 left-0 w-full h-1 ${plan.is_active ? 'bg-indigo-500' : 'bg-slate-300'}`}></div>
            <h3 class="text-lg font-bold text-slate-800 tracking-tight">{plan.name}</h3>
            
            <div class="flex items-center justify-between mt-4">
                <div>
                   <p class="text-xs text-slate-500 uppercase font-semibold">Monthly EMI</p>
                   <p class="text-lg font-bold text-indigo-600">${parseFloat(plan.emi_amount).toLocaleString()}</p>
                </div>
                <div class="text-right">
                   <p class="text-xs text-slate-500 uppercase font-semibold">Progress</p>
                   <p class="text-lg font-bold text-slate-700">{plan.months_paid} / <span class="text-slate-500">{plan.total_months}</span></p>
                </div>
            </div>
            
            <div class="w-full bg-slate-100 rounded-full h-2 mt-4 overflow-hidden">
                <div class="bg-indigo-500 h-2 rounded-full transition-all duration-1000" style={`width: ${(plan.months_paid / plan.total_months) * 100}%`}></div>
            </div>

            {#if plan.is_active}
                <button onclick={() => payEMI(plan.id)} class="mt-5 w-full bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold py-2.5 rounded-lg transition text-sm">
                    Pay Next Installment
                </button>
            {/if}
            
            <p class="text-xs text-slate-400 mt-4 font-medium">Started on: {plan.start_date}</p>
        </div>
        {:else}
        <div class="col-span-full py-12 text-center text-slate-500">No EMI plans found. Create an EMI plan to auto-track installments!</div>
        {/each}
    </div>
    {/if}
</div>
