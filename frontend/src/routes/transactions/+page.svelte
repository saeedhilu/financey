<script lang="ts">
    import { onMount } from 'svelte';
    import { fetchAPI } from '$lib/api';
    import * as XLSX from 'xlsx';

    let transactions: any[] = $state([]);
    let ledgers: any[] = $state([]);
    let loading = $state(true);
    let showForm = $state(false);
    let editingId: number | null = $state(null);

    let newNotes = $state('');
    let newAmount = $state('');
    let newDate = $state(new Date().toISOString().split('T')[0]);
    let newCredit = $state('');
    let newDebit = $state('');

    function exportToExcel() {
        if (!transactions.length) return alert('No data to export!');
        const ws = XLSX.utils.json_to_sheet(transactions.map((t: any) => ({
            ID: t.id,
            Date: t.date,
            Notes: t.notes,
            Amount: t.amount,
            Credit_Ledger_ID: t.credit_ledger,
            Debit_Ledger_ID: t.debit_ledger,
        })));
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Transactions");
        XLSX.writeFile(wb, "financey_transactions.xlsx");
    }

    function importExcel(e: Event) {
        const target = e.target as HTMLInputElement;
        const file = target.files?.[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = async (evt) => {
            try {
                const data = new Uint8Array(evt.target?.result as ArrayBuffer);
                const workbook = XLSX.read(data, { type: 'array' });
                const ws = workbook.Sheets[workbook.SheetNames[0]];
                const json: any[] = XLSX.utils.sheet_to_json(ws);
                
                for (let row of json) {
                    await fetchAPI('/transactions/entries/', {
                        method: 'POST',
                        body: JSON.stringify({ 
                            amount: row.Amount || row.amount, 
                            date: row.Date || row.date,
                            notes: row.Notes || row.notes || 'Imported Transaction',
                            credit_ledger: row.Credit_Ledger_ID || row.credit_ledger,
                            debit_ledger: row.Debit_Ledger_ID || row.debit_ledger
                        })
                    });
                }
                alert('Import successful!');
                window.location.reload();
            } catch(error) {
                alert('Error importing file. Make sure columns match export template exactly.');
            }
        };
        reader.readAsArrayBuffer(file);
    }

    async function handleDelete(id: any) {
        if (!confirm("Are you sure you want to delete this transaction? This action cannot be undone.")) return;
        try {
            await fetchAPI(`/transactions/entries/${id}/`, { method: 'DELETE' });
            transactions = transactions.filter((t: any) => t.id !== id);
        } catch(e) {
            console.error("Delete Error:", e);
            alert("Failed to delete transaction.");
        }
    }

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

    async function handleSave(e: Event) {
        e.preventDefault();
        const payload = {
            amount: newAmount, 
            date: newDate, 
            notes: newNotes, 
            credit_ledger: newCredit, 
            debit_ledger: newDebit 
        };
        try {
            if (editingId) {
                const res = await fetchAPI(`/transactions/entries/${editingId}/`, {
                    method: 'PUT',
                    body: JSON.stringify(payload)
                });
                transactions = transactions.map(t => t.id === editingId ? res : t);
            } else {
                const res = await fetchAPI('/transactions/entries/', {
                    method: 'POST',
                    body: JSON.stringify(payload)
                });
                transactions = [res, ...transactions];
            }
            showForm = false;
            editingId = null;
            newNotes = '';
            newAmount = '';
        } catch(err) {
            alert("Error saving transaction.");
        }
    }

    function startEdit(tx: any) {
        editingId = tx.id;
        newNotes = tx.notes || '';
        newAmount = tx.amount;
        newDate = tx.date;
        newCredit = tx.credit_ledger;
        newDebit = tx.debit_ledger;
        showForm = true;
    }

    function toggleForm() {
        showForm = !showForm;
        if (!showForm) {
            editingId = null;
            newNotes = '';
            newAmount = '';
        }
    }
</script>

<svelte:head>
    <title>Transactions - Financey</title>
</svelte:head>

<div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight">Ledger Transactions</h2>
        <div class="flex flex-wrap gap-2">
            <button onclick={exportToExcel} class="bg-emerald-100 hover:bg-emerald-200 text-emerald-700 px-4 py-2 rounded-lg font-medium transition text-sm flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                Export
            </button>
            <label class="bg-blue-50 hover:bg-blue-100 text-blue-700 px-4 py-2 rounded-lg font-medium transition text-sm cursor-pointer flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                Import
                <input type="file" accept=".xlsx,.xls,.csv" class="hidden" onchange={importExcel} />
            </label>
            <button onclick={toggleForm} class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition shadow-md shadow-blue-500/20 text-sm">
                {showForm ? 'Cancel' : 'New Entry'}
            </button>
        </div>
    </div>
    
    {#if showForm}
    <form onsubmit={handleSave} class="mb-8 bg-slate-50 p-6 rounded-xl border border-slate-200">
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
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 rounded-lg transition shadow-md shadow-emerald-500/20 text-sm">
                    {editingId ? 'Update Transaction' : 'Post Transaction'}
                </button>
            </div>
        </div>
    </form>
    {/if}

    {#if loading}
    <div class="text-slate-400">Loading records...</div>
    {:else}
    <div class="divide-y divide-slate-100">
        {#each transactions as tx}
        <div class="py-4 flex justify-between items-center group relative">
            <div>
                <p class="font-semibold text-slate-800">{tx.notes || 'Uncategorized'}</p>
                <p class="text-sm text-slate-500">{tx.date}</p>
            </div>
            <div class="flex items-center space-x-4">
                <div class="flex items-center space-x-2 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
                    <button onclick={() => startEdit(tx)} class="text-slate-300 hover:text-blue-500 transition" title="Edit Transaction">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                    </button>
                    <button onclick={() => handleDelete(tx.id)} class="text-slate-300 hover:text-rose-500 transition" title="Delete Transaction">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    </button>
                </div>
                <span class="font-bold {parseFloat(tx.amount) > 0 ? 'text-rose-500' : 'text-slate-800'}">${parseFloat(tx.amount).toLocaleString()}</span>
            </div>
        </div>
        {:else}
        <div class="py-12 text-center text-slate-500">No transactions recorded yet. Remember to create your income and expense ledgers first!</div>
        {/each}
    </div>
    {/if}
</div>
