import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Plus, Loader2, Pencil, Trash2, Save, X } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerContact, PartnerContactCreate, PartnerContactUpdate, ContactType } from '@renderer/types/pab'

const CONTACT_TYPE_LABELS: Record<string, string> = {
  address: 'Adresa',
  person: 'Kontaktná osoba'
}

interface PabContactsTabProps {
  partnerId: number
}

interface ContactFormState {
  contact_type: ContactType
  title: string
  first_name: string
  last_name: string
  function_name: string
  phone_work: string
  phone_mobile: string
  phone_private: string
  fax: string
  email: string
  street: string
  city: string
  zip_code: string
  country_code: string
}

const emptyForm: ContactFormState = {
  contact_type: 'person',
  title: '', first_name: '', last_name: '', function_name: '',
  phone_work: '', phone_mobile: '', phone_private: '', fax: '', email: '',
  street: '', city: '', zip_code: '', country_code: 'SK'
}

export default function PabContactsTab({ partnerId }: PabContactsTabProps): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const canEdit = checkPermission('PAB', 'edit')
  const canDelete = checkPermission('PAB', 'delete')

  const [contacts, setContacts] = useState<PartnerContact[]>([])
  const [loading, setLoading] = useState(true)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [adding, setAdding] = useState(false)
  const [saving, setSaving] = useState(false)
  const [form, setForm] = useState<ContactFormState>(emptyForm)

  const loadContacts = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const data = await api.getPabContacts(partnerId)
      setContacts(data)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Nepodarilo sa načítať kontakty', 'error')
    } finally {
      setLoading(false)
    }
  }, [partnerId, addToast])

  useEffect(() => { void loadContacts() }, [loadContacts])

  const startEdit = (c: PartnerContact): void => {
    setEditingId(c.contact_id)
    setAdding(false)
    setForm({
      contact_type: c.contact_type as ContactType,
      title: c.title ?? '', first_name: c.first_name ?? '', last_name: c.last_name ?? '',
      function_name: c.function_name ?? '', phone_work: c.phone_work ?? '',
      phone_mobile: c.phone_mobile ?? '', phone_private: c.phone_private ?? '',
      fax: c.fax ?? '', email: c.email ?? '', street: c.street ?? '',
      city: c.city ?? '', zip_code: c.zip_code ?? '', country_code: c.country_code ?? 'SK'
    })
  }

  const startAdd = (): void => {
    setAdding(true)
    setEditingId(null)
    setForm(emptyForm)
  }

  const cancel = (): void => { setEditingId(null); setAdding(false) }

  const handleSave = useCallback(async (): Promise<void> => {
    setSaving(true)
    try {
      const trimmed = (s: string): string | undefined => s.trim() || undefined
      if (adding) {
        const payload: PartnerContactCreate = {
          contact_type: form.contact_type,
          title: trimmed(form.title), first_name: trimmed(form.first_name),
          last_name: trimmed(form.last_name), function_name: trimmed(form.function_name),
          phone_work: trimmed(form.phone_work), phone_mobile: trimmed(form.phone_mobile),
          phone_private: trimmed(form.phone_private), fax: trimmed(form.fax),
          email: trimmed(form.email), street: trimmed(form.street),
          city: trimmed(form.city), zip_code: trimmed(form.zip_code),
          country_code: trimmed(form.country_code)
        }
        await api.createPabContact(partnerId, payload)
        addToast('Kontakt bol pridaný', 'success')
      } else if (editingId !== null) {
        const payload: PartnerContactUpdate = {
          title: trimmed(form.title), first_name: trimmed(form.first_name),
          last_name: trimmed(form.last_name), function_name: trimmed(form.function_name),
          phone_work: trimmed(form.phone_work), phone_mobile: trimmed(form.phone_mobile),
          phone_private: trimmed(form.phone_private), fax: trimmed(form.fax),
          email: trimmed(form.email), street: trimmed(form.street),
          city: trimmed(form.city), zip_code: trimmed(form.zip_code),
          country_code: trimmed(form.country_code)
        }
        await api.updatePabContact(partnerId, editingId, payload)
        addToast('Kontakt bol aktualizovaný', 'success')
      }
      cancel()
      void loadContacts()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Uloženie zlyhalo', 'error')
    } finally {
      setSaving(false)
    }
  }, [partnerId, adding, editingId, form, addToast, loadContacts])

  const handleDelete = useCallback(async (contactId: number): Promise<void> => {
    if (!confirm('Naozaj chcete odstrániť tento kontakt?')) return
    try {
      await api.deletePabContact(partnerId, contactId)
      addToast('Kontakt bol odstránený', 'success')
      void loadContacts()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Odstránenie zlyhalo', 'error')
    }
  }, [partnerId, addToast, loadContacts])

  const updateForm = (field: keyof ContactFormState, value: string): void => {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  if (loading) {
    return <div className="flex items-center justify-center py-12"><Loader2 className="h-6 w-6 animate-spin text-blue-500" /></div>
  }

  const inputCls = 'w-full px-3 py-2 rounded-lg border text-sm outline-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-50'
  const labelCls = 'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'

  const renderForm = (): ReactElement => (
    <div className="p-4 border rounded-lg border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 space-y-3">
      <h4 className="text-sm font-semibold text-gray-900 dark:text-white">
        {adding ? 'Nový kontakt' : 'Upraviť kontakt'}
      </h4>
      {adding && (
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className={labelCls}>Typ</label>
            <select value={form.contact_type} onChange={(e) => updateForm('contact_type', e.target.value)} disabled={saving} className={inputCls}>
              <option value="person">Kontaktná osoba</option>
              <option value="address">Adresa</option>
            </select>
          </div>
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <div><label className={labelCls}>Titul</label><input type="text" value={form.title} onChange={(e) => updateForm('title', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div><label className={labelCls}>Meno</label><input type="text" value={form.first_name} onChange={(e) => updateForm('first_name', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div><label className={labelCls}>Priezvisko</label><input type="text" value={form.last_name} onChange={(e) => updateForm('last_name', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div><label className={labelCls}>Funkcia</label><input type="text" value={form.function_name} onChange={(e) => updateForm('function_name', e.target.value)} disabled={saving} className={inputCls} /></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <div><label className={labelCls}>Telefón (práca)</label><input type="text" value={form.phone_work} onChange={(e) => updateForm('phone_work', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div><label className={labelCls}>Mobil</label><input type="text" value={form.phone_mobile} onChange={(e) => updateForm('phone_mobile', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div><label className={labelCls}>Email</label><input type="text" value={form.email} onChange={(e) => updateForm('email', e.target.value)} disabled={saving} className={inputCls} /></div>
        <div><label className={labelCls}>Fax</label><input type="text" value={form.fax} onChange={(e) => updateForm('fax', e.target.value)} disabled={saving} className={inputCls} /></div>
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
      {contacts.length === 0 && !adding && (
        <p className="text-sm text-gray-500 dark:text-gray-400">Žiadne kontakty</p>
      )}

      {contacts.map((c) => (
        <div key={c.contact_id} className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
          {editingId === c.contact_id ? renderForm() : (
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                    {CONTACT_TYPE_LABELS[c.contact_type] ?? c.contact_type}
                  </span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {[c.title, c.first_name, c.last_name].filter(Boolean).join(' ') || '—'}
                  </span>
                  {c.function_name && <span className="text-xs text-gray-500">({c.function_name})</span>}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400 space-x-3">
                  {c.phone_work && <span>Tel: {c.phone_work}</span>}
                  {c.phone_mobile && <span>Mob: {c.phone_mobile}</span>}
                  {c.email && <span>Email: {c.email}</span>}
                </div>
              </div>
              <div className="flex gap-1">
                {canEdit && <button onClick={() => startEdit(c)} className="p-1.5 rounded text-gray-500 hover:bg-gray-200 dark:hover:bg-gray-700" title="Upraviť"><Pencil className="h-4 w-4" /></button>}
                {canDelete && <button onClick={() => void handleDelete(c.contact_id)} className="p-1.5 rounded text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20" title="Odstrániť"><Trash2 className="h-4 w-4" /></button>}
              </div>
            </div>
          )}
        </div>
      ))}

      {adding && renderForm()}

      {canEdit && !adding && editingId === null && (
        <button onClick={startAdd} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium border border-dashed border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
          <Plus className="h-3.5 w-3.5" /> Pridať kontakt
        </button>
      )}
    </div>
  )
}
