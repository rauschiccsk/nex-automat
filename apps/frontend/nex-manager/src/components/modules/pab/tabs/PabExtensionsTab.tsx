import { useState, useEffect, useCallback, type ReactElement, type FormEvent } from 'react'
import { Loader2 } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useAuthStore } from '@renderer/stores/authStore'
import { useToastStore } from '@renderer/stores/toastStore'
import type { PartnerExtensions, PartnerExtensionsUpsert } from '@renderer/types/pab'

interface PabExtensionsTabProps {
  partnerId: number
}

export default function PabExtensionsTab({ partnerId }: PabExtensionsTabProps): ReactElement {
  const { checkPermission } = useAuthStore()
  const { addToast } = useToastStore()
  const canEdit = checkPermission('PAB', 'edit')

  const [ext, setExt] = useState<PartnerExtensions | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  // Form state
  const [salePaymentDueDays, setSalePaymentDueDays] = useState(14)
  const [saleCurrencyCode, setSaleCurrencyCode] = useState('EUR')
  const [salePriceCategory, setSalePriceCategory] = useState('')
  const [saleDiscountPercent, setSaleDiscountPercent] = useState(0)
  const [saleCreditLimit, setSaleCreditLimit] = useState(0)
  const [purchasePaymentDueDays, setPurchasePaymentDueDays] = useState(14)
  const [purchaseCurrencyCode, setPurchaseCurrencyCode] = useState('EUR')
  const [purchasePriceCategory, setPurchasePriceCategory] = useState('')
  const [purchaseDiscountPercent, setPurchaseDiscountPercent] = useState(0)

  const loadExtensions = useCallback(async (): Promise<void> => {
    setLoading(true)
    try {
      const data = await api.getPabExtensions(partnerId)
      setExt(data)
      setSalePaymentDueDays(data.sale_payment_due_days ?? 14)
      setSaleCurrencyCode(data.sale_currency_code ?? 'EUR')
      setSalePriceCategory(data.sale_price_category ?? '')
      setSaleDiscountPercent(data.sale_discount_percent ?? 0)
      setSaleCreditLimit(data.sale_credit_limit ?? 0)
      setPurchasePaymentDueDays(data.purchase_payment_due_days ?? 14)
      setPurchaseCurrencyCode(data.purchase_currency_code ?? 'EUR')
      setPurchasePriceCategory(data.purchase_price_category ?? '')
      setPurchaseDiscountPercent(data.purchase_discount_percent ?? 0)
    } catch {
      // Extensions may not exist yet — that's OK
      setExt(null)
    } finally {
      setLoading(false)
    }
  }, [partnerId])

  useEffect(() => {
    void loadExtensions()
  }, [loadExtensions])

  const handleSubmit = useCallback(
    async (e: FormEvent): Promise<void> => {
      e.preventDefault()
      setSaving(true)
      try {
        const payload: PartnerExtensionsUpsert = {
          sale_payment_due_days: salePaymentDueDays,
          sale_currency_code: saleCurrencyCode.trim() || 'EUR',
          sale_price_category: salePriceCategory.trim() || null,
          sale_discount_percent: saleDiscountPercent,
          sale_credit_limit: saleCreditLimit,
          purchase_payment_due_days: purchasePaymentDueDays,
          purchase_currency_code: purchaseCurrencyCode.trim() || 'EUR',
          purchase_price_category: purchasePriceCategory.trim() || null,
          purchase_discount_percent: purchaseDiscountPercent
        }
        await api.upsertPabExtensions(partnerId, payload)
        addToast('Rozšírené údaje boli uložené', 'success')
        void loadExtensions()
      } catch (err) {
        const e = err as ApiError
        addToast(e.message || 'Uloženie zlyhalo', 'error')
      } finally {
        setSaving(false)
      }
    },
    [
      partnerId, salePaymentDueDays, saleCurrencyCode, salePriceCategory,
      saleDiscountPercent, saleCreditLimit, purchasePaymentDueDays,
      purchaseCurrencyCode, purchasePriceCategory, purchaseDiscountPercent,
      addToast, loadExtensions
    ]
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-6 w-6 animate-spin text-blue-500" />
      </div>
    )
  }

  const inputCls = 'w-full px-3 py-2 rounded-lg border text-sm transition-colors outline-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 disabled:opacity-50'
  const labelCls = 'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'
  const sectionCls = 'p-4 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50'

  return (
    <form onSubmit={(e) => void handleSubmit(e)} className="space-y-6 max-w-4xl">
      {/* Predajné parametre */}
      <div className={sectionCls}>
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">Predajné parametre</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className={labelCls}>Splatnosť (dní)</label>
            <input type="number" value={salePaymentDueDays} onChange={(e) => setSalePaymentDueDays(Number(e.target.value))} disabled={saving || !canEdit} className={inputCls} min={0} />
          </div>
          <div>
            <label className={labelCls}>Mena</label>
            <input type="text" value={saleCurrencyCode} onChange={(e) => setSaleCurrencyCode(e.target.value.toUpperCase())} disabled={saving || !canEdit} className={inputCls} maxLength={3} />
          </div>
          <div>
            <label className={labelCls}>Cenová kategória</label>
            <input type="text" value={salePriceCategory} onChange={(e) => setSalePriceCategory(e.target.value)} disabled={saving || !canEdit} className={inputCls} />
          </div>
          <div>
            <label className={labelCls}>Zľava (%)</label>
            <input type="number" value={saleDiscountPercent} onChange={(e) => setSaleDiscountPercent(Number(e.target.value))} disabled={saving || !canEdit} className={inputCls} min={0} max={100} step={0.1} />
          </div>
          <div>
            <label className={labelCls}>Kreditný limit</label>
            <input type="number" value={saleCreditLimit} onChange={(e) => setSaleCreditLimit(Number(e.target.value))} disabled={saving || !canEdit} className={inputCls} min={0} step={0.01} />
          </div>
          {ext?.last_sale_date && (
            <div>
              <label className={labelCls}>Posledný predaj</label>
              <div className="px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-sm text-gray-500 dark:text-gray-400">{ext.last_sale_date}</div>
            </div>
          )}
        </div>
      </div>

      {/* Nákupné parametre */}
      <div className={sectionCls}>
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">Nákupné parametre</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className={labelCls}>Splatnosť (dní)</label>
            <input type="number" value={purchasePaymentDueDays} onChange={(e) => setPurchasePaymentDueDays(Number(e.target.value))} disabled={saving || !canEdit} className={inputCls} min={0} />
          </div>
          <div>
            <label className={labelCls}>Mena</label>
            <input type="text" value={purchaseCurrencyCode} onChange={(e) => setPurchaseCurrencyCode(e.target.value.toUpperCase())} disabled={saving || !canEdit} className={inputCls} maxLength={3} />
          </div>
          <div>
            <label className={labelCls}>Cenová kategória</label>
            <input type="text" value={purchasePriceCategory} onChange={(e) => setPurchasePriceCategory(e.target.value)} disabled={saving || !canEdit} className={inputCls} />
          </div>
          <div>
            <label className={labelCls}>Zľava (%)</label>
            <input type="number" value={purchaseDiscountPercent} onChange={(e) => setPurchaseDiscountPercent(Number(e.target.value))} disabled={saving || !canEdit} className={inputCls} min={0} max={100} step={0.1} />
          </div>
          {ext?.last_purchase_date && (
            <div>
              <label className={labelCls}>Posledný nákup</label>
              <div className="px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-sm text-gray-500 dark:text-gray-400">{ext.last_purchase_date}</div>
            </div>
          )}
        </div>
      </div>

      {canEdit && (
        <div className="flex justify-end">
          <button type="submit" disabled={saving} className={cn('flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed')}>
            {saving && <Loader2 className="h-4 w-4 animate-spin" />}
            Uložiť
          </button>
        </div>
      )}
    </form>
  )
}
