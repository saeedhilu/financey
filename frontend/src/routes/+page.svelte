<script lang="ts">
  import { onMount } from 'svelte';
  
  let totalBalance = 24500.50;
  let thisMonthIncome = 8200.00;
  let thisMonthExpense = 3400.75;
  let savingsGoal = 50000;
  let currentSavings = 12000;
</script>

<svelte:head>
  <title>Dashboard - Financey</title>
</svelte:head>

<div class="space-y-8 animate-in fade-in duration-500">
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Total Balance</h3>
        <span class="text-blue-500 bg-blue-50 p-2 rounded-lg">💼</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${totalBalance.toLocaleString()}</p>
        <p class="text-sm text-emerald-500 mt-2 font-medium flex items-center">
          <span class="mr-1">↗</span> +2.5% from last month
        </p>
      </div>
    </div>
    
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Monthly Income</h3>
        <span class="text-emerald-500 bg-emerald-50 p-2 rounded-lg">📈</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${thisMonthIncome.toLocaleString()}</p>
        <p class="text-sm text-slate-400 mt-2 font-medium flex items-center">
          Projected salary processing...
        </p>
      </div>
    </div>
    
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-slate-500 font-medium tracking-wide text-sm uppercase">Monthly Expenses</h3>
        <span class="text-rose-500 bg-rose-50 p-2 rounded-lg">📉</span>
      </div>
      <div>
        <p class="text-4xl font-extrabold text-slate-800 tracking-tight">${thisMonthExpense.toLocaleString()}</p>
        <p class="text-sm text-rose-500 mt-2 font-medium flex items-center">
          <span class="mr-1">↘</span> -1.2% from last month
        </p>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition">
      <h3 class="text-lg font-bold text-slate-800 mb-6 flex justify-between">
        Savings Goal
        <span class="text-sm font-semibold text-blue-600 bg-blue-50 px-3 py-1 rounded-full">New House Downpayment</span>
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
              {Math.round((currentSavings/savingsGoal)*100)}%
            </span>
          </div>
        </div>
        <div class="overflow-hidden h-4 mb-4 text-xs flex rounded-full bg-slate-100">
          <div style={`width: ${(currentSavings/savingsGoal)*100}%`} class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full transition-all duration-1000 ease-out"></div>
        </div>
        <p class="text-sm font-medium text-slate-600">Current: <span class="text-slate-800 font-bold">${currentSavings.toLocaleString()}</span></p>
      </div>
    </div>

    <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-md transition">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-bold text-slate-800">Recent Transactions</h3>
        <button class="text-sm text-blue-600 hover:underline">View All</button>
      </div>
      <ul class="space-y-2">
        <li class="flex items-center justify-between p-3 hover:bg-slate-50 rounded-xl transition cursor-pointer">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center font-bold text-lg">🍔</div>
            <div>
              <p class="font-semibold text-slate-800 tracking-tight">McDonalds</p>
              <p class="text-xs text-slate-500 font-medium">Food & Dining • Today</p>
            </div>
          </div>
          <span class="font-bold text-slate-800 tracking-tight">-$24.50</span>
        </li>
        <li class="flex items-center justify-between p-3 hover:bg-slate-50 rounded-xl transition cursor-pointer">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold text-lg">🏢</div>
            <div>
              <p class="font-semibold text-slate-800 tracking-tight">Tech Corp Salary</p>
              <p class="text-xs text-slate-500 font-medium">Income • Yesterday</p>
            </div>
          </div>
          <span class="font-bold text-emerald-500 tracking-tight">+$8,200.00</span>
        </li>
      </ul>
    </div>
  </div>
</div>
