<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';
  
  let totalBalance = $state(0);
  let thisMonthIncome = $state(0);
  let thisMonthExpense = $state(0);
  let savingsGoal = $state(0);
  let currentSavings = $state(0);
  let recentTransactions: any[] = $state([]);
  let loading = $state(true);

  onMount(async () => {
    try {
        const txData = await fetchAPI('/transactions/entries/');
        recentTransactions = txData.slice(0, 5);
        
        const ledgers = await fetchAPI('/ledgers/');
        const ledgerMap = new Map();
        ledgers.forEach((l: any) => ledgerMap.set(l.id, l.ledger_class));

        txData.forEach((t: any) => {
            let amount = parseFloat(t.amount);
            let cClass = ledgerMap.get(t.credit_ledger);
            let dClass = ledgerMap.get(t.debit_ledger);

            if (cClass === 'INCOME') thisMonthIncome += amount;
            if (dClass === 'EXPENSE') thisMonthExpense += amount;
            
            if (dClass === 'ASSET') totalBalance += amount;
            if (cClass === 'ASSET') totalBalance -= amount;
        });

        const goals = await fetchAPI('/goals/');
        if (goals.length > 0) {
            savingsGoal = parseFloat(goals[0].target_amount);
            currentSavings = goals[0].current_amount || 0;
        }
    } catch(e) {
        console.error("Dashboard API Error:", e);
    } finally {
        loading = false;
    }
  });
</script>

<svelte:head>
  <title>Dashboard - Financey</title>
</svelte:head>

{#if loading}
<div class="flex justify-center items-center h-64">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
</div>
{:else}
<div class="space-y-8 animate-in fade-in duration-500">
  <!-- Mobile Horizontal Scroll Container / Desktop Grid -->
  <div class="flex overflow-x-auto gap-4 md:grid md:grid-cols-3 md:gap-6 pb-2 snap-x hide-scrollbar">
    <div class="min-w-[85vw] md:min-w-0 shrink-0 snap-center bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Total Balance</h3>
        <span class="text-blue-500 bg-blue-50 p-2 rounded-lg">💼</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${totalBalance.toLocaleString()}</p>
      </div>
    </div>
    
    <div class="min-w-[85vw] md:min-w-0 shrink-0 snap-center bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Monthly Income</h3>
        <span class="text-emerald-500 bg-emerald-50 p-2 rounded-lg">📈</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${thisMonthIncome.toLocaleString()}</p>
      </div>
    </div>
    
    <div class="min-w-[85vw] md:min-w-0 shrink-0 snap-center bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Monthly Expenses</h3>
        <span class="text-rose-500 bg-rose-50 p-2 rounded-lg">📉</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${thisMonthExpense.toLocaleString()}</p>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition">
      <h3 class="text-lg font-bold text-slate-800 mb-6 flex justify-between">
        Savings Goal
        <span class="text-sm font-semibold text-blue-600 bg-blue-50 px-3 py-1 rounded-full">Automated Target</span>
      </h3>
      <div class="relative pt-1">
        <div class="flex mb-2 items-center justify-between">
          <div>
            <span class="text-xs font-semibold inline-block py-1 text-slate-500">
              Target: ${savingsGoal.toLocaleString()}
            </span>
          </div>
          <div class="text-right">
            <span class="text-lg font-bold inline-block text-blue-600">
              {savingsGoal > 0 ? Math.round((currentSavings/savingsGoal)*100) : 0}%
            </span>
          </div>
        </div>
        <div class="overflow-hidden h-4 mb-4 text-xs flex rounded-full bg-slate-100">
          <div style={`width: ${savingsGoal > 0 ? (currentSavings/savingsGoal)*100 : 0}%`} class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full transition-all duration-1000 ease-out"></div>
        </div>
        <p class="text-sm font-medium text-slate-600">Current: <span class="text-slate-800 font-bold">${currentSavings.toLocaleString()}</span></p>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-bold text-slate-800">Recent Transactions</h3>
        <a href="/transactions" class="text-sm text-blue-600 hover:underline">View All</a>
      </div>
      <ul class="space-y-2">
        {#each recentTransactions as tx}
        <li class="flex items-center justify-between p-3 hover:bg-slate-50 rounded-xl transition cursor-pointer">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-lg">💰</div>
            <div>
              <p class="font-semibold text-slate-800 tracking-tight">{tx.notes || 'Transaction'}</p>
              <p class="text-xs text-slate-500 font-medium">{tx.date}</p>
            </div>
          </div>
          <span class="font-bold tracking-tight {parseFloat(tx.amount) > 0 ? 'text-emerald-500' : 'text-slate-800'}">{tx.amount}</span>
        </li>
        {:else}
        <p class="text-slate-500 text-sm">No recent transactions to display.</p>
        {/each}
      </ul>
    </div>
  </div>
</div>
{/if}
