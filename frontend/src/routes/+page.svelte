<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchAPI } from '$lib/api';
  import { Bar } from 'svelte-chartjs';
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

  let totalBalance = $state(0);
  let envelopedBalance = $state(0);
  let thisMonthIncome = $state(0);
  let thisMonthExpense = $state(0);
  let savingsGoal = $state(0);
  let currentSavings = $state(0);
  let recentTransactions: any[] = $state([]);
  let topSpends: any[] = $state([]);
  let chartData: any = $state({ labels: [], datasets: [] });
  let loading = $state(true);
  
  // Specific Ledger Tracking
  let bankBalance = $state(0);
  let cashBalance = $state(0);

  onMount(async () => {
    try {
        const txData = await fetchAPI('/transactions/entries/');
        recentTransactions = txData.slice(0, 5);
        
        const ledgers = await fetchAPI('/ledgers/');
        const ledgerMap = new Map();
        ledgers.forEach((l: any) => ledgerMap.set(l.id, l));

        const monthlyData = new Map();
        const spendsMap = new Map();
        const currentMonthStr = new Date().toISOString().substring(0, 7);

        for (let i = 5; i >= 0; i--) {
            const d = new Date();
            d.setMonth(d.getMonth() - i);
            const mStr = d.toISOString().substring(0, 7);
            monthlyData.set(mStr, { income: 0, expense: 0 });
        }

        txData.forEach((t: any) => {
            let amount = parseFloat(t.amount);
            let cClass = ledgerMap.get(t.credit_ledger)?.ledger_class;
            let dClass = ledgerMap.get(t.debit_ledger)?.ledger_class;
            let month = t.date.substring(0, 7);

            if (monthlyData.has(month)) {
                if (cClass === 'INCOME') monthlyData.get(month).income += amount;
                if (dClass === 'EXPENSE') monthlyData.get(month).expense += amount;
            }

            if (cClass === 'INCOME' && month === currentMonthStr) thisMonthIncome += amount;
            if (dClass === 'EXPENSE' && month === currentMonthStr) {
                thisMonthExpense += amount;
            }
            
            if (dClass === 'EXPENSE') {
                let lname = ledgerMap.get(t.debit_ledger)?.name || 'Unknown';
                spendsMap.set(lname, (spendsMap.get(lname) || 0) + amount);
            }
            
            if (dClass === 'ASSET') totalBalance += amount;
            if (cClass === 'ASSET') totalBalance -= amount;
            
            if (dClass === 'ENVELOPE') envelopedBalance += amount;
            if (cClass === 'ENVELOPE') envelopedBalance -= amount;
            
            // Hardcoded specific ledgers tracking
            if (Number(t.debit_ledger) === 13) bankBalance += amount;
            if (Number(t.credit_ledger) === 13) bankBalance -= amount;
            
            if (Number(t.debit_ledger) === 12) cashBalance += amount;
            if (Number(t.credit_ledger) === 12) cashBalance -= amount;
        });

        topSpends = Array.from(spendsMap.entries())
            .sort((a, b) => b[1] - a[1]).slice(0, 4)
            .map(e => ({ name: e[0], amount: e[1] }));

        const labels = Array.from(monthlyData.keys());
        chartData = {
            labels: labels,
            datasets: [
                {
                    label: 'Income',
                    data: labels.map(k => monthlyData.get(k).income),
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    borderRadius: 4
                },
                {
                    label: 'Expenses',
                    data: labels.map(k => monthlyData.get(k).expense),
                    backgroundColor: 'rgba(244, 63, 94, 0.7)',
                    borderRadius: 4
                }
            ]
        };

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
  <div class="grid grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 pb-2">
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Available Cash</h3>
        <span class="text-blue-500 bg-blue-50 p-2 rounded-lg">💼</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${totalBalance.toLocaleString()}</p>
      </div>
    </div>
    
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Reserved (Envelopes)</h3>
        <span class="text-indigo-500 bg-indigo-50 p-2 rounded-lg">🔒</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${envelopedBalance.toLocaleString()}</p>
      </div>
    </div>
    
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Monthly Income</h3>
        <span class="text-emerald-500 bg-emerald-50 p-2 rounded-lg">📈</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${thisMonthIncome.toLocaleString()}</p>
      </div>
    </div>
    
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Monthly Expenses</h3>
        <span class="text-rose-500 bg-rose-50 p-2 rounded-lg">📉</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${thisMonthExpense.toLocaleString()}</p>
      </div>
    </div>
    
    <!-- Custom Tracking Cards -->
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Bank Balance</h3>
        <span class="text-indigo-500 bg-indigo-50 p-2 rounded-lg">🏦</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${bankBalance.toLocaleString()}</p>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Pocket Cash</h3>
        <span class="text-emerald-500 bg-emerald-50 p-2 rounded-lg">💵</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${cashBalance.toLocaleString()}</p>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-1 gap-6">
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 mb-2 hover:shadow-md transition">
      <h3 class="text-lg font-bold text-slate-800 mb-6">Income vs Expenses (6 Months)</h3>
      <div class="h-64 w-full">
        <Bar data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />
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

    <div class="grid grid-cols-1 gap-6">
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-slate-800">Recent Transactions</h3>
          <a href="/transactions" class="text-sm text-blue-600 hover:underline">View All</a>
        </div>
        <ul class="space-y-4">
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

      <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-slate-800">Top Spending Categories</h3>
        </div>
        <div class="space-y-4">
          {#each topSpends as spend}
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-slate-700">{spend.name}</span>
            <span class="text-sm font-bold text-rose-500">${spend.amount.toLocaleString()}</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-1.5 mb-2">
            <div class="bg-rose-400 h-1.5 rounded-full" style={`width: ${(spend.amount / (topSpends[0]?.amount || 1)) * 100}%`}></div>
          </div>
          {:else}
          <p class="text-slate-500 text-sm">No expenses analyzed yet.</p>
          {/each}
        </div>
      </div>
    </div>
  </div>
</div>
{/if}
