import { useState, useEffect, useCallback, type ReactElement } from 'react'
import { Plus, Loader2, Pencil, Trash2, Save, X } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerAddress, PartnerAddressCreate, PartnerAddressUpdate, AddressType } from '@renderer/types/pab'

const ADDRESS_TYPE_LABELS: Record<string, string> = {
  registered: 'Sídlo',
  correspondence: 'Korešpondenčná',
  invoice: 'Fakturačná'
}

const ALL_ADDRESS_TYPES: AddressType[] = ['registered', 'correspondence', 'invoice']

interface PabAddressesTabProps {
  partnerId: number
}

export default function PabAddressesTab({ partnerId }: PabAddressesTabProps): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const canEdit = checkPermission('PAB', 'edit')
  const canDelete = checkPermission('PAB', 'delete')

  const [addresses, setAddresses] = useState<PartnerAddress[]>([])
  const [loading, setLoading] = useState(true)
  const [editingType, setEditingType] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  // Edit form
  const [street, setStreet] = useState('')
  const [city, setCity] = useState('')
  const [zipCode, setZipCode] = useState('')
  const [countryCode, setCountryCode] = useState('SK')
  const [addType, setAddType] = useState<AddressType | null>(null)

  const loadAddresses = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const data = await api.getPabAddresses(partnerId)
      setAddresses(data)
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Nepodarilo sa načítať adresy', 'error')
    } finally {
      setLoading(false)
    }
  }, [partnerId, addToast])

  useEffect(() => {
    void loadAddresses()
  }, [loadAddresses])

  const existingTypes = new Set(addresses.map((a) => a.address_type))
  const availableTypes = ALL_ADDRESS_TYPES.filter((t) => !existingTypes.has(t))

  const startEdit = (addr: PartnerAddress): void => {
    setEditingType(addr.address_type)
    setStreet(addr.street ?? '')
    setCity(addr.city ?? '')
    setZipCode(addr.zip_code ?? '')
    setCountryCode(addr.country_code ?? 'SK')
    setAddType(null)
  }

  const startAdd = (type: AddressType): void => {
    setAddType(type)
    setEditingType(null)
    setStreet('')
    setCity('')
    setZipCode('')
    setCountryCode('SK')
  }

  const cancelEdit = (): void => {
    setEditingType(null)
    setAddType(null)
  }

  const handleSave = useCallback(async (): Promise<void> => {
    setSaving(true)
    try {
      if (addType) {
        const payload: PartnerAddressCreate = {
          address_type: addType,
          street: street.trim() || undefined,
          city: city.trim() || undefined,
          zip_code: zipCode.trim() || undefined,
          country_code: countryCode.trim() || undefined
        }
        await api.createPabAddress(partnerId, payload)
        addToast('Adresa bola pridaná', 'success')
      } else if (editingType) {
        const payload: PartnerAddressUpdate = {
          street: street.trim() || undefined,
          city: city.trim() || undefined,
          zip_code: zipCode.trim() || undefined,
          country_code: countryCode.trim() || undefined
        }
        await api.updatePabAddress(partnerId, editingType, payload)
        addToast('Adresa bola aktualizovaná', 'success')
      }
      cancelEdit()
      void loadAddresses()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Uloženie zlyhalo', 'error')
    } finally {
      setSaving(false)
    }
  }, [partnerId, addType, editingType, street, city, zipCode, countryCode, addToast, loadAddresses])

  const handleDelete = useCallback(async (addressType: string): Promise<void> => {
    if (!confirm('Naozaj chcete odstrániť túto adresu?')) return
    try {
      await api.deletePabAddress(partnerId, addressType)
      addToast('Adresa bola odstránená', 'success')
      void loadAddresses()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Odstránenie zlyhalo', 'error')
    }
  }, [partnerId, addToast, loadAddresses])

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-6 w-6 animate-spin text-blue-500" />
      </div>
    )
  }

  const inputCls = 'w-full px-3 py-2 rounded-lg border text-sm transition-colors outline-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-50'
  const labelCls = 'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'

  const renderEditForm = (): ReactElement => (
    <div className="p-4 border rounded-lg border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 space-y-3">
      <h4 className="text-sm font-semibold text-gray-900 dark:text-white">
        {addType ? `Nová adresa: ${ADDRESS_TYPE_LABELS[addType]}` : `Upraviť: ${ADDRESS_TYPE_LABELS[editingType ?? '']}`}
      </h4>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <div className="md:col-span-2">
          <label className={labelCls}>Ulica</label>
          <input type="text" value={street} onChange={(e) => setStreet(e.target.value)} disabled={saving} className={inputCls} />
        </div>
        <div>
          <label className={labelCls}>Mesto</label>
          <input type="text" value={city} onChange={(e) => setCity(e.target.value)} disabled={saving} className={inputCls} />
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className={labelCls}>PSČ</label>
            <input type="text" value={zipCode} onChange={(e) => setZipCode(e.target.value)} disabled={saving} className={inputCls} />
          </div>
          <div>
            <label className={labelCls}>Krajina</label>
            <input type="text" value={countryCode} onChange={(e) => setCountryCode(e.target.value)} disabled={saving} className={inputCls} maxLength={3} />
          </div>
        </div>
      </div>
      <div className="flex gap-2 justify-end">
        <button type="button" onClick={cancelEdit} disabled={saving} className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">
          <X className="h-3.5 w-3.5" /> Zrušiť
        </button>
        <button type="button" onClick={() => void handleSave()} disabled={saving} className={cn('flex items-center gap-1 px-3 py-1.5 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50')}>
          {saving ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Save className="h-3.5 w-3.5" />}
          Uložiť
        </button>
      </div>
    </div>
  )

  return (
    <div className="space-y-4 max-w-4xl">
      {/* Existing addresses */}
      {addresses.length === 0 && !addType && (
        <p className="text-sm text-gray-500 dark:text-gray-400">Žiadne adresy</p>
      )}

      {addresses.map((addr) => (
        <div key={addr.address_type} className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
          {editingType === addr.address_type ? (
            renderEditForm()
          ) : (
            <div className="flex items-start justify-between">
              <div>
                <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-1">
                  {ADDRESS_TYPE_LABELS[addr.address_type] ?? addr.address_type}
                </h4>
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  {[addr.street, addr.zip_code, addr.city, addr.country_code].filter(Boolean).join(', ') || '—'}
                </p>
              </div>
              <div className="flex gap-1">
                {canEdit && (
                  <button onClick={() => startEdit(addr)} className="p-1.5 rounded text-gray-500 hover:bg-gray-200 dark:hover:bg-gray-700" title="Upraviť">
                    <Pencil className="h-4 w-4" />
                  </button>
                )}
                {canDelete && (
                  <button onClick={() => void handleDelete(addr.address_type)} className="p-1.5 rounded text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20" title="Odstrániť">
                    <Trash2 className="h-4 w-4" />
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      ))}

      {/* Add form */}
      {addType && renderEditForm()}

      {/* Add buttons */}
      {canEdit && availableTypes.length > 0 && !addType && !editingType && (
        <div className="flex gap-2">
          {availableTypes.map((type) => (
            <button key={type} onClick={() => startAdd(type)} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium border border-dashed border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
              <Plus className="h-3.5 w-3.5" />
              {ADDRESS_TYPE_LABELS[type]}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
