import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Plus, Loader2, Pencil, Trash2, Save, X, Star } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerBankAccount, PartnerBankAccountCreate, PartnerBankAccountUpdate } from '@renderer/types/pab'

interface PabBankAccountsTabProps {
  partnerId: number
}

interface BankFormState {
  iban_code: string
  swift_code: string
  account_number: string
  bank_name: string
  bank_seat: string
  vs_sale: string
  vs_purchase: string
  is_primary: boolean
}

const emptyForm: BankFormState = {
  iban_code: '', swift_code: '', account_number: '',
  bank_name: '', bank_seat: '', vs_sale: '', vs_purchase: '',
  is_primary: false
}

export default function PabBankAccountsTab({ partnerId }: PabBankAccountsTabProps): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const canEdit = checkPermission('PAB', 'edit')
  const canDelete = checkPermission('PAB', 'delete')

  const [accounts, setAccounts] = useState<PartnerBankAccount[]>([])
  const [loading, setLoading] = useState(true)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [adding, setAdding] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState<BankFormState>(emptyForm)

  const loadAccounts = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const data = await api.getPabBankAccounts(partnerId)
      setAccounts(data)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Nepodarilo sa načítať bankové účty', 'error')
    } finally {
      setLoading(false)
    }
  }, [partnerId, addToast])

  useEffect(() => { void loadAccounts() }, [loadAccounts])

  const startEdit = (a: PartnerBankAccount): void => {
    setEditingId(a.account_id)
    setAdding(false)
    setForm({
      iban_code: a.iban_code ?? '', swift_code: a.swift_code ?? '',
      account_number: a.account_number ?? '', bank_name: a.bank_name ?? '',
      bank_seat: a.bank_seat ?? '', vs_sale: a.vs_sale ?? '',
      vs_purchase: a.vs_purchase ?? '', is_primary: a.is_primary
    })
  }

  const startAdd = (): void => { setAdding(true); setEditingId(null); setForm(emptyForm) }
  const cancel = (): void => { setEditingId(null); setAdding(false) }

  const updateForm = (field: keyof BankFormState, value: string | boolean): void => {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  const handleSave = useCallback(async (): Promise<void> => {
    setSaving(true)
    try {
      const trimmed = (s: string): string | undefined => s.trim() || undefined
      if (adding) {
        const payload: PartnerBankAccountCreate = {
          iban_code: trimmed(form.iban_code), swift_code: trimmed(form.swift_code),
          account_number: trimmed(form.account_number), bank_name: trimmed(form.bank_name),
          bank_seat: trimmed(form.bank_seat), vs_sale: trimmed(form.vs_sale),
          vs_purchase: trimmed(form.vs_purchase), is_primary: form.is_primary
        }
        await api.createPabBankAccount(partnerId, payload)
        addToast('Bankový účet bol pridaný', 'success')
      } else if (editingId !== null) {
        const payload: PartnerBankAccountUpdate = {
          iban_code: trimmed(form.iban_code), swift_code: trimmed(form.swift_code),
          account_number: trimmed(form.account_number), bank_name: trimmed(form.bank_name),
          bank_seat: trimmed(form.bank_seat), vs_sale: trimmed(form.vs_sale),
          vs_purchase: trimmed(form.vs_purchase), is_primary: form.is_primary
        }
        await api.updatePabBankAccount(partnerId, editingId, payload)
        addToast('Bankový účet bol aktualizovaný', 'success')
      }
      cancel()
      void loadAccounts()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Uloženie zlyhalo', 'error')
    } finally {
      setSaving(false)
    }
  }, [partnerId, adding, editingId, form, addToast, loadAccounts])

  const handleDelete = useCallback(async (accountId: number): Promise<void> => {
    if (!confirm('Naozaj chcete odstrániť tento bankový účet?')) return
    try {
      await api.deletePabBankAccount(partnerId, accountId)
      addToast('Bankový účet bol odstránený', 'success')
      void loadAccounts()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Odstránenie zlyhalo', 'error')
    }
  }, [partnerId, addToast, loadAccounts])

  if (loading) {
    return <div className="flex items-center justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-blue-500" /></div>
  }

  const inputCls = 'w-full px-3 py-2 rounded-lg border text-sm outline-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-50'
  const labelCls = 'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'

  const renderForm = (): ReactElement => (
    <div className="p-4 border rounded-lg border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 space-y-3">
      <h4 className="text-sm font-semibold text-gray-900 dark:text-white">{adding ? 'Nový bankový účet' : 'Upraviť bankový účet'}</h4>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div><label className={labelCls}>IBAN</label><input type="text" value={form.iban_code} onChange={(e) => updateForm('iban_code', e.target.value)} disabled={saving} className={inputCls} placeholder="SK89 0200 0000 0000 1234 5678" /></div>
        <div><label className={labelCls}>SWIFT/BIC</label><input type="text" value={form.swift_code} onChange={(e) => updateForm('swift_code', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div><label className={labelCls}>Číslo účtu</label><input type="text" value={form.account_number} onChange={(e) => updateForm('account_number', e.target.value)} disabled={saving} className={inputCls} /></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div><label className={labelCls}>Názov banky</label><input type="text" value={form.bank_name} onChange={(e) => updateForm('bank_name', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div><label className={labelCls}>Sídlo banky</label><input type="text" value={form.bank_seat} onChange={(e) => updateForm('bank_seat', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div className="flex items-end pb-2">
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={form.is_primary} onChange={(e) => updateForm('is_primary', e.target.checked as unknown as string)} disabled={saving} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
            <span className="text-sm text-gray-700 dark:text-gray-300">Primárny účet</span>
          </label>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div><label className={labelCls}>VS predaj</label><input type="text" value={form.vs_sale} onChange={(e) => updateForm('vs_sale', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div><label className={labelCls}>VS nákup</label><input type="text" value={form.vs_purchase} onChange={(e) => updateForm('vs_purchase', e.target.value)} disabled={saving} className={inputCls} /></div>
      </div>
      <div className="flex gap-2 justify-end">
        <button type="button" onClick={cancel} disabled={saving} className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">
          <X className="h-3.5 w-3.5" /> Zrušiť
        </button>
        <button type="button" onClick={() => void handleSave()} disabled={saving} className={cn('flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50')}>
          {saving ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Save className="h-3.5 w-3.5" />} Uložiť
        </button>
      </div>
    </div>
  )

  return (
    <div className="space-y-4 max-w-4xl">
      {accounts.length === 0 && !adding && (
        <p className="text-sm text-gray-500 dark:text-gray-400">Žiadne bankové účty</p>
      )}

      {accounts.map((a) => (
        <div key={a.account_id} className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
          {editingId === a.account_id ? renderForm() : (
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  {a.is_primary && <Star className="h-4 w-4 text-yellow-500 fill-yellow-500" />}
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {a.iban_code || a.account_number || '—'}
                  </span>
                  {a.is_primary && <span className="text-xs text-yellow-600 dark:text-yellow-400 font-medium">Primárny</span>}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400 space-x-3">
                  {a.bank_name && <span>{a.bank_name}</span>}
                  {a.swift_code && <span>SWIFT: {a.swift_code}</span>}
                </div>
              </div>
              <div className="flex gap-1">
                {canEdit && <button onClick={() => startEdit(a)} className="p-1.5 rounded text-gray-500 hover:bg-gray-200 dark:hover:bg-gray-700" title="Upraviť"><Pencil className="h-4 w-4" /></button>}
                {canDelete && <button onClick={() => void handleDelete(a.account_id)} className="p-1.5 rounded text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20" title="Odstrániť"><Trash2 className="h-4 w-4" /></button>}
              </div>
            </div>
          )}
        </div>
      ))}

      {adding && renderForm()}

      {canEdit && !adding && editingId === null && (
        <button onClick={startAdd} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium border border-dashed border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
          <Plus className="h-3.5 w-3.5" /> Pridať bankový účet
        </button>
      )}
    </div>
  )
}
