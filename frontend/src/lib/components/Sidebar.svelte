<script lang="ts">
</script>

<aside class="w-64 bg-slate-900 text-slate-300 min-h-screen flex flex-col hidden md:flex fixed top-0 left-0">
  <div class="h-16 flex items-center px-6 border-b border-slate-800 text-white font-bold text-2xl tracking-wide">
    <span class="text-blue-500 mr-2">✦</span><span class="text-white">Fin</span><span class="text-slate-400">ancey</span>
  </div>
  <nav class="flex-1 px-4 py-6 space-y-2">
    <a href="/" class="flex px-4 py-3 rounded-lg bg-blue-600/10 text-blue-400 font-medium transition hover:bg-blue-600/20">Dashboard</a>
    <a href="/transactions" class="flex px-4 py-3 rounded-lg font-medium transition hover:bg-slate-800 hover:text-white">Transactions</a>
    <a href="/ledgers" class="flex px-4 py-3 rounded-lg font-medium transition hover:bg-slate-800 hover:text-white">Ledgers</a>
    <a href="/goals" class="flex px-4 py-3 rounded-lg font-medium transition hover:bg-slate-800 hover:text-white">Savings Goals</a>
    <a href="/reports" class="flex px-4 py-3 rounded-lg font-medium transition hover:bg-slate-800 hover:text-white">Reports</a>
  </nav>
  <div class="p-6 border-t border-slate-800">
    <button class="w-full flex justify-between items-center text-sm font-medium hover:text-white transition group">
      <span>Settings</span>
      <span class="opacity-50 group-hover:opacity-100 transition">⚙️</span>
    </button>
  </div>
</aside>
