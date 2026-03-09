import { useState, useEffect, useCallback, type ReactElement, type FormEvent } from 'react'
import { ArrowLeft, Loader2, Save } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import { useEshopStore } from '@renderer/stores/eshopStore'
import type { EshopProduct, EshopProductCreateRequest } from '@renderer/types/eshop'

interface FormData {
  sku: string
  name: string
  barcode: string
  short_description: string
  description: string
  image_url: string
  price: string
  price_vat: string
  vat_rate: string
  stock_quantity: string
  weight: string
  is_active: boolean
  sort_order: string
}

const DEFAULT_FORM: FormData = {
  sku: '',
  name: '',
  barcode: '',
  short_description: '',
  description: '',
  image_url: '',
  price: '',
  price_vat: '',
  vat_rate: '20',
  stock_quantity: '0',
  weight: '',
  is_active: true,
  sort_order: '0'
}

export default function EshopProductForm(): ReactElement {
  const { addToast } = useToastStore()
  const { selectedProductId, closeProductEdit } = useEshopStore()

  const isNew = selectedProductId === null
  const [form, setForm] = useState<FormData>(DEFAULT_FORM)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(!isNew)
  const [saving, setSaving] = useState(false)

  // Load existing product
  useEffect(() => {
    if (isNew) return
    setLoading(true)
    api
      .getEshopProduct(selectedProductId!)
      .then((p: EshopProduct) => {
        setForm({
          sku: p.sku,
          name: p.name,
          barcode: p.barcode || '',
          short_description: p.short_description || '',
          description: p.description || '',
          image_url: p.image_url || '',
          price: String(p.price),
          price_vat: String(p.price_vat),
          vat_rate: String(p.vat_rate),
          stock_quantity: String(p.stock_quantity),
          weight: p.weight != null ? String(p.weight) : '',
          is_active: p.is_active,
          sort_order: String(p.sort_order)
        })
      })
      .catch((err: ApiError) => {
        addToast(err.message || 'Nepodarilo sa načítať produkt', 'error')
      })
      .finally(() => setLoading(false))
  }, [isNew, selectedProductId, addToast])

  const updateField = (field: keyof FormData, value: string | boolean): void => {
    setForm((prev) => ({ ...prev, [field]: value }))
    setErrors((prev) => {
      const next = { ...prev }
      delete next[field]
      return next
    })
  }

  // Auto-calculate price_vat from price + vat_rate
  const handlePriceChange = (value: string): void => {
    updateField('price', value)
    const price = parseFloat(value)
    const vatRate = parseFloat(form.vat_rate)
    if (!isNaN(price) && !isNaN(vatRate)) {
      const priceVat = price * (1 + vatRate / 100)
      setForm((prev) => ({ ...prev, price: value, price_vat: priceVat.toFixed(2) }))
    }
  }

  const handleVatRateChange = (value: string): void => {
    updateField('vat_rate', value)
    const price = parseFloat(form.price)
    const vatRate = parseFloat(value)
    if (!isNaN(price) && !isNaN(vatRate)) {
      const priceVat = price * (1 + vatRate / 100)
      setForm((prev) => ({ ...prev, vat_rate: value, price_vat: priceVat.toFixed(2) }))
    }
  }

  const validate = (): boolean => {
    const errs: Record<string, string> = {}
    if (!form.sku.trim()) errs.sku = 'SKU je povinné'
    if (!form.name.trim()) errs.name = 'Názov je povinný'
    if (!form.price || isNaN(parseFloat(form.price))) errs.price = 'Cena musí byť číslo'
    if (!form.price_vat || isNaN(parseFloat(form.price_vat))) errs.price_vat = 'Cena s DPH musí byť číslo'
    if (!form.vat_rate || isNaN(parseFloat(form.vat_rate))) errs.vat_rate = 'DPH musí byť číslo'
    if (form.stock_quantity !== '' && isNaN(parseInt(form.stock_quantity))) errs.stock_quantity = 'Sklad musí byť celé číslo'
    if (form.weight && isNaN(parseFloat(form.weight))) errs.weight = 'Hmotnosť musí byť číslo'
    setErrors(errs)
    return Object.keys(errs).length === 0
  }

  const handleSubmit = useCallback(
    async (e: FormEvent): Promise<void> => {
      e.preventDefault()
      if (!validate()) return
      setSaving(true)
      try {
        const data: EshopProductCreateRequest = {
          sku: form.sku.trim(),
          name: form.name.trim(),
          barcode: form.barcode.trim() || undefined,
          short_description: form.short_description.trim() || undefined,
          description: form.description.trim() || undefined,
          image_url: form.image_url.trim() || undefined,
          price: parseFloat(form.price),
          price_vat: parseFloat(form.price_vat),
          vat_rate: parseFloat(form.vat_rate),
          stock_quantity: parseInt(form.stock_quantity) || 0,
          weight: form.weight ? parseFloat(form.weight) : undefined,
          is_active: form.is_active,
          sort_order: parseInt(form.sort_order) || 0
        }
        if (isNew) {
          await api.createEshopProduct(data)
          addToast('Produkt bol vytvorený', 'success')
        } else {
          await api.updateEshopProduct(selectedProductId!, data)
          addToast('Produkt bol aktualizovaný', 'success')
        }
        closeProductEdit()
      } catch (err) {
        const e = err as ApiError
        addToast(e.message || 'Chyba pri ukladaní produktu', 'error')
      } finally {
        setSaving(false)
      }
    },
    [form, isNew, selectedProductId, addToast, closeProductEdit]
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-3 text-gray-500 dark:text-gray-400">Načítavam...</span>
      </div>
    )
  }

  return (
    <div data-testid="product-form" className="flex flex-col gap-4 max-w-3xl">
      {/* Header */}
      <div className="flex items-center gap-3 shrink-0">
        <button
          data-testid="cancel-button"
          onClick={closeProductEdit}
          className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          title="Späť na zoznam"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
          {isNew ? 'Nový produkt' : `Upraviť produkt: ${form.sku}`}
        </h1>
      </div>

      <form onSubmit={(e) => void handleSubmit(e)} className="space-y-4">
        {/* Row: SKU + Barcode */}
        <div className="grid grid-cols-2 gap-4">
          <Field label="SKU *" error={errors.sku}>
            <input
              data-testid="field-sku"
              value={form.sku}
              onChange={(e) => updateField('sku', e.target.value)}
              className={fieldClass(errors.sku)}
            />
          </Field>
          <Field label="Čiarový kód">
            <input
              value={form.barcode}
              onChange={(e) => updateField('barcode', e.target.value)}
              className={fieldClass()}
            />
          </Field>
        </div>

        {/* Name */}
        <Field label="Názov *" error={errors.name}>
          <input
            data-testid="field-name"
            value={form.name}
            onChange={(e) => updateField('name', e.target.value)}
            className={fieldClass(errors.name)}
          />
        </Field>

        {/* Short description */}
        <Field label="Krátky popis">
          <input
            value={form.short_description}
            onChange={(e) => updateField('short_description', e.target.value)}
            className={fieldClass()}
          />
        </Field>

        {/* Description */}
        <Field label="Popis">
          <textarea
            value={form.description}
            onChange={(e) => updateField('description', e.target.value)}
            rows={3}
            className={fieldClass()}
          />
        </Field>

        {/* Row: Price, VAT rate, Price VAT */}
        <div className="grid grid-cols-3 gap-4">
          <Field label="Cena bez DPH *" error={errors.price}>
            <input
              data-testid="field-price"
              type="number"
              step="0.01"
              value={form.price}
              onChange={(e) => handlePriceChange(e.target.value)}
              className={fieldClass(errors.price)}
            />
          </Field>
          <Field label="DPH % *" error={errors.vat_rate}>
            <input
              data-testid="field-vat-rate"
              type="number"
              step="0.01"
              value={form.vat_rate}
              onChange={(e) => handleVatRateChange(e.target.value)}
              className={fieldClass(errors.vat_rate)}
            />
          </Field>
          <Field label="Cena s DPH *" error={errors.price_vat}>
            <input
              data-testid="field-price-vat"
              type="number"
              step="0.01"
              value={form.price_vat}
              onChange={(e) => updateField('price_vat', e.target.value)}
              className={fieldClass(errors.price_vat)}
            />
          </Field>
        </div>

        {/* Row: Stock, Weight, Sort order */}
        <div className="grid grid-cols-3 gap-4">
          <Field label="Sklad (ks)" error={errors.stock_quantity}>
            <input
              data-testid="field-stock"
              type="number"
              value={form.stock_quantity}
              onChange={(e) => updateField('stock_quantity', e.target.value)}
              className={fieldClass(errors.stock_quantity)}
            />
          </Field>
          <Field label="Hmotnosť (kg)" error={errors.weight}>
            <input
              type="number"
              step="0.001"
              value={form.weight}
              onChange={(e) => updateField('weight', e.target.value)}
              className={fieldClass(errors.weight)}
            />
          </Field>
          <Field label="Poradie">
            <input
              type="number"
              value={form.sort_order}
              onChange={(e) => updateField('sort_order', e.target.value)}
              className={fieldClass()}
            />
          </Field>
        </div>

        {/* Image URL */}
        <Field label="URL obrázka">
          <input
            value={form.image_url}
            onChange={(e) => updateField('image_url', e.target.value)}
            placeholder="https://..."
            className={fieldClass()}
          />
        </Field>

        {/* Active checkbox */}
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={form.is_active}
            onChange={(e) => updateField('is_active', e.target.checked)}
            className="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span className="text-sm text-gray-700 dark:text-gray-300">Aktívny produkt</span>
        </label>

        {/* Buttons */}
        <div className="flex justify-end gap-3 pt-2">
          <button
            type="button"
            onClick={closeProductEdit}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            Zrušiť
          </button>
          <button
            data-testid="save-button"
            type="submit"
            disabled={saving}
            className={cn(
              'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              'bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50'
            )}
          >
            <Save className="h-4 w-4" />
            {saving ? 'Ukladám...' : 'Uložiť'}
          </button>
        </div>
      </form>
    </div>
  )
}

// ── Helpers ──

function fieldClass(error?: string): string {
  return cn(
    'w-full px-3 py-2 rounded-lg border text-sm outline-none transition-colors',
    'bg-white dark:bg-gray-700 text-gray-900 dark:text-white',
    error
      ? 'border-red-500 focus:border-red-500 focus:ring-2 focus:ring-red-500/20'
      : 'border-gray-300 dark:border-gray-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20'
  )
}

function Field({
  label,
  error,
  children
}: {
  label: string
  error?: string
  children: ReactElement
}): ReactElement {
  return (
    <div>
      <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
        {label}
      </label>
      {children}
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  )
}
