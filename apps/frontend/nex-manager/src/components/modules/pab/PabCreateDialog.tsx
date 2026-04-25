import { useState, useCallback, useRef, useEffect, type ReactElement, type FormEvent } from 'react'
import { X, Loader2 } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerCatalogCreate, PartnerClass } from '@renderer/types/pab'

interface PabCreateDialogProps {
  open: boolean
  onClose: () => void
  onCreated: () => void
}

export default function PabCreateDialog({
  open,
  onClose,
  onCreated
}: PabCreateDialogProps): ReactElement | null {
  const { addToast } = useToastStore()

  const [partnerId, setPartnerId] = useState('')
  const [partnerName, setPartnerName] = useState('')
  const [regName, setRegName] = useState('')
  const [companyId, setCompanyId] = useState('')
  const [taxId, setTaxId] = useState('')
  const [vatId, setVatId] = useState('')
  const [isVatPayer, setIsVatPayer] = useState(false)
  const [isSupplier, setIsSupplier] = useState(false)
  const [isCustomer, setIsCustomer] = useState(true)
  const [street, setStreet] = useState('')
  const [city, setCity] = useState('')
  const [zipCode, setZipCode] = useState('')
  const [countryCode, setCountryCode] = useState('SK')
  const [partnerClass, setPartnerClass] = useState<PartnerClass>('business')
  const [isActive, setIsActive] = useState(true)

  const [saving, setSaving] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const firstFieldRef = useRef<HTMLInputElement>(null)

  // Auto-focus first field when dialog opens
  useEffect(() => {
    if (open) {
      // Small delay to ensure dialog is rendered
      const timer = setTimeout(() => firstFieldRef.current?.focus(), 50)
      return () => clearTimeout(timer)
    }
  }, [open])

  const validate = useCallback((): boolean => {
    const errs: Record<string, string> = {}
    const id = parseInt(partnerId, 10)
    if (!partnerId.trim() || isNaN(id) || id <= 0) {
      errs.partner_id = 'ID partnera musí byť kladné číslo'
    }
    if (!partnerName.trim()) errs.partner_name = 'Názov partnera je povinný'
    if (partnerName.length > 100) errs.partner_name = 'Názov partnera max 100 znakov'
    if (companyId.trim() && !/^\d+$/.test(companyId.trim())) {
      errs.company_id = 'IČO musí obsahovať len čísla'
    }
    setErrors(errs)
    return Object.keys(errs).length === 0
  }, [partnerId, partnerName, companyId])

  const handleSubmit = useCallback(
    async (e: FormEvent): Promise<void> => {
      e.preventDefault()
      if (!validate()) return

      setSaving(true)
      try {
        const payload: PartnerCatalogCreate = {
          partner_id: parseInt(partnerId, 10),
          partner_name: partnerName.trim(),
          reg_name: regName.trim() || undefined,
          company_id: companyId.trim() || undefined,
          tax_id: taxId.trim() || undefined,
          vat_id: vatId.trim() || undefined,
          is_vat_payer: isVatPayer,
          is_supplier: isSupplier,
          is_customer: isCustomer,
          street: street.trim() || undefined,
          city: city.trim() || undefined,
          zip_code: zipCode.trim() || undefined,
          country_code: countryCode.trim() || undefined,
          partner_class: partnerClass,
          is_active: isActive
        }

        await api.createPabPartner(payload)
        addToast(`Partner ${partnerId} bol úspešne vytvorený`, 'success')
        onCreated()
      } catch (err) {
        const e = err as ApiError
        if (e.status === 409) {
          setErrors((prev) => ({ ...prev, partner_id: 'Partner s týmto ID už existuje' }))
          addToast('Partner s týmto ID už existuje', 'error')
        } else {
          addToast(e.message || 'Vytvorenie zlyhalo', 'error')
        }
      } finally {
        setSaving(false)
      }
    },
    [
      validate, partnerId, partnerName, regName,
      companyId, taxId, vatId, isVatPayer, isSupplier, isCustomer,
      street, city, zipCode, countryCode, partnerClass, isActive,
      onCreated, addToast
    ]
  )

  if (!open) return null

  const inputCls = (field?: string): string =>
    cn(
      'w-full px-3 py-2 rounded-lg border text-sm transition-colors outline-none',
      'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
      field && errors[field]
        ? 'border-red-500 focus:ring-red-500/20'
        : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
      'disabled:opacity-50'
    )

  const labelCls = 'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'

  const FieldError = ({ field }: { field: string }): ReactElement | null => {
    if (!errors[field]) return null
    return <p className="mt-1 text-xs text-red-500">{errors[field]}</p>
  }

  const clearFieldError = (field: string): void => {
    if (errors[field]) setErrors((prev) => { const n = { ...prev }; delete n[field]; return n })
  }

  return (
    <>
      <div className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div data-testid="create-partner-dialog" className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-xl w-full max-w-3xl max-h-[85vh] flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700 shrink-0">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Nový partner</h2>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Content */}
          <form onSubmit={(e) => void handleSubmit(e)} onKeyDown={(e) => e.stopPropagation()} className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
            {/* Row: ID | Kód | Názov */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className={labelCls}>ID partnera <span className="text-red-500">*</span></label>
                <input ref={firstFieldRef} data-testid="create-partner-id" type="number" value={partnerId} onChange={(e) => { setPartnerId(e.target.value); clearFieldError('partner_id') }} disabled={saving} className={inputCls('partner_id')} min={1} />
                <FieldError field="partner_id" />
              </div>
              <div className="md:col-span-2">
                <label className={labelCls}>Názov firmy <span className="text-red-500">*</span></label>
                <input data-testid="create-partner-name" type="text" value={partnerName} onChange={(e) => { setPartnerName(e.target.value); clearFieldError('partner_name') }} disabled={saving} className={inputCls('partner_name')} maxLength={100} />
                <FieldError field="partner_name" />
              </div>
            </div>

            {/* Reg name */}
            <div>
              <label className={labelCls}>Registračný názov</label>
              <input type="text" value={regName} onChange={(e) => setRegName(e.target.value)} disabled={saving} className={inputCls()} />
            </div>

            {/* IČO, DIČ, IČ DPH */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className={labelCls}>IČO</label>
                <input type="text" value={companyId} onChange={(e) => { setCompanyId(e.target.value); clearFieldError('company_id') }} disabled={saving} className={inputCls('company_id')} maxLength={20} />
                <FieldError field="company_id" />
              </div>
              <div>
                <label className={labelCls}>DIČ</label>
                <input type="text" value={taxId} onChange={(e) => setTaxId(e.target.value)} disabled={saving} className={inputCls()} />
              </div>
              <div>
                <label className={labelCls}>IČ DPH</label>
                <input type="text" value={vatId} onChange={(e) => setVatId(e.target.value)} disabled={saving} className={inputCls()} placeholder="SK2021234567" />
              </div>
            </div>

            {/* Type / Class / Active */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className={labelCls}>Trieda</label>
                <select value={partnerClass} onChange={(e) => setPartnerClass(e.target.value as PartnerClass)} disabled={saving} className={inputCls()}>
                  <option value="business">Obchodný partner</option>
                  <option value="retail">Retail zákazník</option>
                  <option value="guest">Guest zákazník</option>
                </select>
              </div>
              <div className="flex items-end gap-4 pb-2">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" checked={isCustomer} onChange={(e) => setIsCustomer(e.target.checked)} disabled={saving} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">Odberateľ</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" checked={isSupplier} onChange={(e) => setIsSupplier(e.target.checked)} disabled={saving} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">Dodávateľ</span>
                </label>
              </div>
              <div className="flex items-end gap-4 pb-2">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" checked={isActive} onChange={(e) => setIsActive(e.target.checked)} disabled={saving} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">Aktívny</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" checked={isVatPayer} onChange={(e) => setIsVatPayer(e.target.checked)} disabled={saving} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                  <span className="text-sm text-gray-700 dark:text-gray-300">Platca DPH</span>
                </label>
              </div>
            </div>

            {/* Address */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-2">
                <label className={labelCls}>Ulica</label>
                <input type="text" value={street} onChange={(e) => setStreet(e.target.value)} disabled={saving} className={inputCls()} />
              </div>
              <div>
                <label className={labelCls}>Mesto</label>
                <input type="text" value={city} onChange={(e) => setCity(e.target.value)} disabled={saving} className={inputCls()} />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className={labelCls}>PSČ</label>
                  <input type="text" value={zipCode} onChange={(e) => setZipCode(e.target.value)} disabled={saving} className={inputCls()} />
                </div>
                <div>
                  <label className={labelCls}>Krajina</label>
                  <input type="text" value={countryCode} onChange={(e) => setCountryCode(e.target.value)} disabled={saving} className={inputCls()} maxLength={3} placeholder="SK" />
                </div>
              </div>
            </div>
          </form>

          {/* Footer */}
          <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-700 shrink-0">
            <button type="button" data-testid="create-cancel" onClick={onClose} disabled={saving} className={cn('px-4 py-2 rounded-lg text-sm font-medium transition-colors border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50')}>
              Zrušiť
            </button>
            <button type="button" data-testid="create-submit" onClick={(e) => void handleSubmit(e as unknown as FormEvent)} disabled={saving} className={cn('flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed')}>
              {saving && <Loader2 className="h-4 w-4 animate-spin" />}
              Vytvoriť
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
