import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Plus, Loader2, Pencil, Trash2, Save, X } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerFacility, PartnerFacilityCreate, PartnerFacilityUpdate } from '@renderer/types/pab'

interface PabFacilitiesTabProps {
  partnerId: number
}

interface FacilityFormState {
  facility_name: string
  street: string
  city: string
  zip_code: string
  country_code: string
  phone: string
  fax: string
  email: string
}

const emptyForm: FacilityFormState = {
  facility_name: '', street: '', city: '', zip_code: '',
  country_code: 'SK', phone: '', fax: '', email: ''
}

export default function PabFacilitiesTab({ partnerId }: PabFacilitiesTabProps): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const canEdit = checkPermission('PAB', 'edit')
  const canDelete = checkPermission('PAB', 'delete')

  const [facilities, setFacilities] = useState<PartnerFacility[]>([])
  const [loading, setLoading] = useState(true)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [adding, setAdding] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState<FacilityFormState>(emptyForm)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const loadFacilities = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const data = await api.getPabFacilities(partnerId)
      setFacilities(data)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Nepodarilo sa načítať prevádzkarne', 'error')
    } finally {
      setLoading(false)
    }
  }, [partnerId, addToast])

  useEffect(() => { void loadFacilities() }, [loadFacilities])

  const startEdit = (f: PartnerFacility): void => {
    setEditingId(f.facility_id)
    setAdding(false)
    setForm({
      facility_name: f.facility_name, street: f.street ?? '', city: f.city ?? '',
      zip_code: f.zip_code ?? '', country_code: f.country_code ?? 'SK',
      phone: f.phone ?? '', fax: f.fax ?? '', email: f.email ?? ''
    })
    setErrors({})
  }

  const startAdd = (): void => { setAdding(true); setEditingId(null); setForm(emptyForm); setErrors({}) }
  const cancel = (): void => { setEditingId(null); setAdding(false); setErrors({}) }

  const updateForm = (field: keyof FacilityFormState, value: string): void => {
    setForm((prev) => ({ ...prev, [field]: value }))
    if (errors[field]) setErrors((prev) => { const n = { ...prev }; delete n[field]; return n })
  }

  const handleSave = useCallback(async (): Promise<void> => {
    if (!form.facility_name.trim()) {
      setErrors({ facility_name: 'Názov prevádzky je povinný' })
      return
    }
    setSaving(true)
    try {
      const trimmed = (s: string): string | undefined => s.trim() || undefined
      if (adding) {
        const payload: PartnerFacilityCreate = {
          facility_name: form.facility_name.trim(),
          street: trimmed(form.street), city: trimmed(form.city),
          zip_code: trimmed(form.zip_code), country_code: trimmed(form.country_code),
          phone: trimmed(form.phone), fax: trimmed(form.fax), email: trimmed(form.email)
        }
        await api.createPabFacility(partnerId, payload)
        addToast('Prevádzka bola pridaná', 'success')
      } else if (editingId !== null) {
        const payload: PartnerFacilityUpdate = {
          facility_name: form.facility_name.trim(),
          street: trimmed(form.street), city: trimmed(form.city),
          zip_code: trimmed(form.zip_code), country_code: trimmed(form.country_code),
          phone: trimmed(form.phone), fax: trimmed(form.fax), email: trimmed(form.email)
        }
        await api.updatePabFacility(partnerId, editingId, payload)
        addToast('Prevádzka bola aktualizovaná', 'success')
      }
      cancel()
      void loadFacilities()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Uloženie zlyhalo', 'error')
    } finally {
      setSaving(false)
    }
  }, [partnerId, adding, editingId, form, addToast, loadFacilities])

  const handleDelete = useCallback(async (facilityId: number): Promise<void> => {
    if (!confirm('Naozaj chcete odstrániť túto prevádzku?')) return
    try {
      await api.deletePabFacility(partnerId, facilityId)
      addToast('Prevádzka bola odstránená', 'success')
      void loadFacilities()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Odstránenie zlyhalo', 'error')
    }
  }, [partnerId, addToast, loadFacilities])

  if (loading) {
    return <div className="flex items-center justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-blue-500" /></div>
  }

  const inputCls = (field?: string): string => cn(
    'w-full px-3 py-2 rounded-lg border text-sm outline-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white disabled:opacity-50',
    field && errors[field]
      ? 'border-red-500 focus:ring-red-500/20'
      : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'
  )
  const labelCls = 'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'

  const renderForm = (): ReactElement => (
    <div className="p-4 border rounded-lg border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 space-y-3">
      <h4 className="text-sm font-semibold text-gray-900 dark:text-white">{adding ? 'Nová prevádzka' : 'Upraviť prevádzku'}</h4>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="md:col-span-2">
          <label className={labelCls}>Názov prevádzky <span className="text-red-500">*</span></label>
          <input type="text" value={form.facility_name} onChange={(e) => updateForm('facility_name', e.target.value)} disabled={saving} className={inputCls('facility_name')} maxLength={100} />
          {errors.facility_name && <p className="mt-1 text-xs text-red-500">{errors.facility_name}</p>}
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <div className="md:col-span-2"><label className={labelCls}>Ulica</label><input type="text" value={form.street} onChange={(e) => updateForm('street', e.target.value)} disabled={saving} className={inputCls()} /></div>
        <div><label className={labelCls}>Mesto</label><input type="text" value={form.city} onChange={(e) => updateForm('city', e.target.value)} disabled={saving} className={inputCls()} /></div>
        <div className="grid grid-cols-2 gap-2">
          <div><label className={labelCls}>PSČ</label><input type="text" value={form.zip_code} onChange={(e) => updateForm('zip_code', e.target.value)} disabled={saving} className={inputCls()} /></div>
          <div><label className={labelCls}>Krajina</label><input type="text" value={form.country_code} onChange={(e) => updateForm('country_code', e.target.value)} disabled={saving} className={inputCls()} maxLength={3} /></div>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div><label className={labelCls}>Telefón</label><input type="text" value={form.phone} onChange={(e) => updateForm('phone', e.target.value)} disabled={saving} className={inputCls()} /></div>
        <div><label className={labelCls}>Fax</label><input type="text" value={form.fax} onChange={(e) => updateForm('fax', e.target.value)} disabled={saving} className={inputCls()} /></div>
        <div><label className={labelCls}>Email</label><input type="text" value={form.email} onChange={(e) => updateForm('email', e.target.value)} disabled={saving} className={inputCls()} /></div>
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
      {facilities.length === 0 && !adding && (
        <p className="text-sm text-gray-500 dark:text-gray-400">Žiadne prevádzkarne</p>
      )}

      {facilities.map((f) => (
        <div key={f.facility_id} className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
          {editingId === f.facility_id ? renderForm() : (
            <div className="flex items-start justify-between">
              <div>
                <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-1">{f.facility_name}</h4>
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  {[f.street, f.zip_code, f.city, f.country_code].filter(Boolean).join(', ') || '—'}
                </p>
                {(f.phone || f.email) && (
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-1 space-x-3">
                    {f.phone && <span>Tel: {f.phone}</span>}
                    {f.email && <span>Email: {f.email}</span>}
                  </div>
                )}
              </div>
              <div className="flex gap-1">
                {canEdit && <button onClick={() => startEdit(f)} className="p-1.5 rounded text-gray-500 hover:bg-gray-200 dark:hover:bg-gray-700" title="Upraviť"><Pencil className="h-4 w-4" /></button>}
                {canDelete && <button onClick={() => void handleDelete(f.facility_id)} className="p-1.5 rounded text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20" title="Odstrániť"><Trash2 className="h-4 w-4" /></button>}
              </div>
            </div>
          )}
        </div>
      ))}

      {adding && renderForm()}

      {canEdit && !adding && editingId === null && (
        <button onClick={startAdd} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium border border-dashed border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
          <Plus className="h-3.5 w-3.5" /> Pridať prevádzku
        </button>
      )}
    </div>
  )
}
