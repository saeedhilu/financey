<script lang="ts">
    import { onMount } from 'svelte';
    import { fetchAPI } from '$lib/api';
    import * as XLSX from 'xlsx';

    let ledgers: any[] = $state([]);
    let loading = $state(true);
    let showForm = $state(false);
    let editingId: number | null = $state(null);
    let newName = $state('');
    let newClass = $state('EXPENSE');

    function exportToExcel() {
        if (!ledgers.length) return alert('No data to export!');
        const ws = XLSX.utils.json_to_sheet(ledgers.map((l: any) => ({
            ID: l.id,
            Name: l.name,
            Class: l.ledger_class,
            Created: l.created_at
        })));
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Ledgers");
        XLSX.writeFile(wb, "financey_ledgers.xlsx");
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
                    await fetchAPI('/ledgers/', {
                        method: 'POST',
                        body: JSON.stringify({ name: row.Name || row.name, ledger_class: row.Class || row.ledger_class || 'ASSET' })
                    });
                }
                alert('Import successful!');
                window.location.reload();
            } catch(error) {
                alert('Error importing file. Make sure it has Name and Class columns.');
            }
        };
        reader.readAsArrayBuffer(file);
    }

    onMount(async () => {
        try {
            ledgers = await fetchAPI('/ledgers/');
        } catch(e) {
            console.error(e);
        } finally {
            loading = false;
        }
    });

    async function handleSave(e: Event) {
        e.preventDefault();
        try {
            if (editingId) {
                const res = await fetchAPI(`/ledgers/${editingId}/`, {
                    method: 'PUT',
                    body: JSON.stringify({ name: newName, ledger_class: newClass })
                });
                ledgers = ledgers.map(l => l.id === editingId ? res : l);
            } else {
                const res = await fetchAPI('/ledgers/', {
                    method: 'POST',
                    body: JSON.stringify({ name: newName, ledger_class: newClass })
                });
                ledgers = [res, ...ledgers];
            }
            showForm = false;
            editingId = null;
            newName = '';
        } catch(err) {
            alert("Error saving ledger.");
        }
    }

    function startEdit(ledger: any) {
        editingId = ledger.id;
        newName = ledger.name;
        newClass = ledger.ledger_class;
        showForm = true;
    }

    function toggleForm() {
        showForm = !showForm;
        if (!showForm) {
            editingId = null;
            newName = '';
            newClass = 'EXPENSE';
        }
    }
</script>

<svelte:head>
    <title>Ledgers - Financey</title>
</svelte:head>

<div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight">Accounts & Ledgers</h2>
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
                {showForm ? 'Cancel' : 'Create Ledger'}
            </button>
        </div>
    </div>
    
    {#if showForm}
    <form onsubmit={handleSave} class="mb-8 bg-slate-50 p-6 rounded-xl border border-slate-200">
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
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 text-sm rounded-lg transition shadow-md shadow-emerald-500/20">
                    {editingId ? 'Update Ledger' : 'Save Ledger'}
                </button>
            </div>
        </div>
    </form>
    {/if}

    {#if loading}
    <div class="text-slate-400">Loading records...</div>
    {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each ledgers as ledger}
        <div class="p-6 border border-slate-200 rounded-xl hover:border-blue-300 transition relative group">
            <p class="text-xs font-bold uppercase text-slate-400 mb-2 tracking-widest">{ledger.ledger_class}</p>
            <h3 class="text-lg font-semibold text-slate-800 pr-8">{ledger.name}</h3>
            
            <!-- Edit Button -->
            <button onclick={() => startEdit(ledger)} class="absolute top-4 right-4 text-slate-300 hover:text-blue-500 transition opacity-0 group-hover:opacity-100">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
            </button>
        </div>
        {:else}
        <div class="col-span-full py-12 text-center text-slate-500">No ledgers constructed. Add an Income and Bank Asset ledger to get started!</div>
        {/each}
    </div>
    {/if}
</div>
