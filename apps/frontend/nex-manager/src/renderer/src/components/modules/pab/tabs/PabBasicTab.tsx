import { useState, useCallback, type ReactElement, type FormEvent } from 'react'
import { Loader2, Trash2 } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerCatalog, PartnerCatalogUpdate, PartnerClass } from '@renderer/types/pab'

interface PabBasicTabProps {
  partner: PartnerCatalog
  onUpdated: () => void
  onDeleted?: () => void
}

export default function PabBasicTab({ partner, onUpdated, onDeleted }: PabBasicTabProps): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const canEdit = checkPermission('PAB', 'edit')
  const canDelete = checkPermission('PAB', 'delete')

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const [partnerName, setPartnerName] = useState(partner.partner_name)
  const [regName, setRegName] = useState(partner.reg_name ?? '')
  const [companyId, setCompanyId] = useState(partner.company_id ?? '')
  const [taxId, setTaxId] = useState(partner.tax_id ?? '')
  const [vatId, setVatId] = useState(partner.vat_id ?? '')
  const [isVatPayer, setIsVatPayer] = useState(partner.is_vat_payer)
  const [isSupplier, setIsSupplier] = useState(partner.is_supplier)
  const [isCustomer, setIsCustomer] = useState(partner.is_customer)
  const [street, setStreet] = useState(partner.street ?? '')
  const [city, setCity] = useState(partner.city ?? '')
  const [zipCode, setZipCode] = useState(partner.zip_code ?? '')
  const [countryCode, setCountryCode] = useState(partner.country_code ?? 'SK')
  const [partnerClass, setPartnerClass] = useState<PartnerClass>(partner.partner_class)
  const [isActive, setIsActive] = useState(partner.is_active)

  const [saving, setSaving] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const validate = useCallback((): boolean => {
    const errs: Record<string, string> = {}
    if (!partnerName.trim()) errs.partner_name = 'Názov partnera je povinný'
    if (companyId.trim() && !/^\d+$/.test(companyId.trim())) {
      errs.company_id = 'IČO musí obsahovať len čísla'
    }
    setErrors(errs)
    return Object.keys(errs).length === 0
  }, [partnerName, companyId])

  const handleSubmit = useCallback(
    async (e: FormEvent): Promise<void> => {
      e.preventDefault()
      if (!validate()) return

      setSaving(true)
      try {
        const payload: PartnerCatalogUpdate = {
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

        await api.updatePabPartner(partner.partner_id, payload)
        addToast(`Partner ${partner.partner_id} bol aktualizovaný`, 'success')
        onUpdated()
      } catch (err) {
        const e = err as ApiError
        addToast(e.message || 'Uloženie zlyhalo', 'error')
      } finally {
        setSaving(false)
      }
    },
    [
      validate, partner, partnerName, regName, companyId, taxId, vatId,
      isVatPayer, isSupplier, isCustomer, street, city, zipCode,
      countryCode, partnerClass, isActive, onUpdated, addToast
    ]
  )

  const handleDelete = useCallback(async (): Promise<void> => {
    setDeleting(true)
    try {
      await api.deletePabPartner(partner.partner_id)
      addToast('Partner vymazaný', 'success')
      setShowDeleteConfirm(false)
      onDeleted?.()
    } catch (err) {
      const e = err as ApiError
      addToast(e.message || 'Vymazanie zlyhalo', 'error')
    } finally {
      setDeleting(false)
    }
  }, [partner.partner_id, addToast, onDeleted])

  const inputCls = (field?: string): string =>
    cn(
      'w-full px-3 py-2 rounded-lg border text-sm transition-colors outline-none',
      'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
      field && errors[field]
        ? 'border-red-500 focus:ring-red-500/20'
        : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20',
      'disabled:opacity-50'
    )

  const readonlyCls =
    'w-full px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-sm text-gray-500 dark:text-gray-400'

  const labelCls = 'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'

  const FieldError = ({ field }: { field: string }): ReactElement | null => {
    if (!errors[field]) return null
    return <p className="mt-1 text-xs text-red-500">{errors[field]}</p>
  }

  const clearFieldError = (field: string): void => {
    if (errors[field]) setErrors((prev) => { const n = { ...prev }; delete n[field]; return n })
  }

  return (
    <form onSubmit={(e) => void handleSubmit(e)} className="space-y-4 max-w-4xl">
      {/* Read-only fields */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className={labelCls}>ID partnera</label>
          <div className={readonlyCls}>{partner.partner_id}</div>
        </div>
        <div>
          <label className={labelCls}>Verzia</label>
          <div className={readonlyCls}>{partner.modify_id}</div>
        </div>
      </div>

      {/* Name */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className={labelCls}>Názov firmy <span className="text-red-500">*</span></label>
          <input type="text" value={partnerName} onChange={(e) => { setPartnerName(e.target.value); clearFieldError('partner_name') }} disabled={saving || !canEdit} className={inputCls('partner_name')} maxLength={100} />
          <FieldError field="partner_name" />
        </div>
        <div>
          <label className={labelCls}>Registračný názov</label>
          <input type="text" value={regName} onChange={(e) => setRegName(e.target.value)} disabled={saving || !canEdit} className={inputCls()} />
        </div>
      </div>

      {/* IČO, DIČ, IČ DPH */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className={labelCls}>IČO</label>
          <input type="text" value={companyId} onChange={(e) => { setCompanyId(e.target.value); clearFieldError('company_id') }} disabled={saving || !canEdit} className={inputCls('company_id')} maxLength={20} />
          <FieldError field="company_id" />
        </div>
        <div>
          <label className={labelCls}>DIČ</label>
          <input type="text" value={taxId} onChange={(e) => setTaxId(e.target.value)} disabled={saving || !canEdit} className={inputCls()} />
        </div>
        <div>
          <label className={labelCls}>IČ DPH</label>
          <input type="text" value={vatId} onChange={(e) => setVatId(e.target.value)} disabled={saving || !canEdit} className={inputCls()} placeholder="SK2021234567" />
        </div>
      </div>

      {/* Class / Type / Active */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className={labelCls}>Trieda</label>
          <select value={partnerClass} onChange={(e) => setPartnerClass(e.target.value as PartnerClass)} disabled={saving || !canEdit} className={inputCls()}>
            <option value="business">Obchodný partner</option>
            <option value="retail">Retail zákazník</option>
            <option value="guest">Guest zákazník</option>
          </select>
        </div>
        <div className="flex items-end gap-4 pb-2">
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={isCustomer} onChange={(e) => setIsCustomer(e.target.checked)} disabled={saving || !canEdit} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
            <span className="text-sm text-gray-700 dark:text-gray-300">Odberateľ</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={isSupplier} onChange={(e) => setIsSupplier(e.target.checked)} disabled={saving || !canEdit} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
            <span className="text-sm text-gray-700 dark:text-gray-300">Dodávateľ</span>
          </label>
        </div>
        <div className="flex items-end gap-4 pb-2">
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={isActive} onChange={(e) => setIsActive(e.target.checked)} disabled={saving || !canEdit} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
            <span className="text-sm text-gray-700 dark:text-gray-300">Aktívny</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={isVatPayer} onChange={(e) => setIsVatPayer(e.target.checked)} disabled={saving || !canEdit} className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
            <span className="text-sm text-gray-700 dark:text-gray-300">Platca DPH</span>
          </label>
        </div>
      </div>

      {/* Address */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="md:col-span-2">
          <label className={labelCls}>Ulica</label>
          <input type="text" value={street} onChange={(e) => setStreet(e.target.value)} disabled={saving || !canEdit} className={inputCls()} />
        </div>
        <div>
          <label className={labelCls}>Mesto</label>
          <input type="text" value={city} onChange={(e) => setCity(e.target.value)} disabled={saving || !canEdit} className={inputCls()} />
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className={labelCls}>PSČ</label>
            <input type="text" value={zipCode} onChange={(e) => setZipCode(e.target.value)} disabled={saving || !canEdit} className={inputCls()} />
          </div>
          <div>
            <label className={labelCls}>Krajina</label>
            <input type="text" value={countryCode} onChange={(e) => setCountryCode(e.target.value)} disabled={saving || !canEdit} className={inputCls()} maxLength={3} />
          </div>
        </div>
      </div>

      {/* Action buttons */}
      {(canEdit || canDelete) && (
        <div className="flex justify-between items-center pt-4">
          <div>
            {canDelete && (
              <button
                type="button"
                onClick={() => setShowDeleteConfirm(true)}
                disabled={saving || deleting}
                className={cn(
                  'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  'bg-red-600 text-white hover:bg-red-700',
                  'disabled:opacity-50 disabled:cursor-not-allowed'
                )}
              >
                <Trash2 className="h-4 w-4" />
                Vymazať
              </button>
            )}
          </div>
          <div>
            {canEdit && (
              <button
                type="submit"
                disabled={saving}
                className={cn(
                  'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  'bg-blue-600 text-white hover:bg-blue-700',
                  'disabled:opacity-50 disabled:cursor-not-allowed'
                )}
              >
                {saving && <Loader2 className="h-4 w-4 animate-spin" />}
                Uložiť
              </button>
            )}
          </div>
        </div>
      )}

      {/* Delete confirmation dialog */}
      {showDeleteConfirm && (
        <>
          <div className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm" onClick={() => setShowDeleteConfirm(false)} />
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-xl p-6 max-w-sm w-full">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                Potvrdenie vymazania
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
                Naozaj chceš vymazať partnera <strong>{partner.partner_name}</strong>?
              </p>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowDeleteConfirm(false)}
                  disabled={deleting}
                  className="px-4 py-2 rounded-lg text-sm font-medium border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  Nie
                </button>
                <button
                  type="button"
                  onClick={() => void handleDelete()}
                  disabled={deleting}
                  className={cn(
                    'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                    'bg-red-600 text-white hover:bg-red-700',
                    'disabled:opacity-50 disabled:cursor-not-allowed'
                  )}
                >
                  {deleting && <Loader2 className="h-4 w-4 animate-spin" />}
                  Áno, vymazať
                </button>
              </div>
            </div>
          </div>
        </>
      )}
    </form>
  )
}
