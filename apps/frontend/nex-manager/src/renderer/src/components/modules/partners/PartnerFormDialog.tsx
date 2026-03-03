import { useState, useCallback, type ReactElement, type FormEvent } from 'react'
import { X, Loader2 } from 'lucide-react'
import { cn } from '@renderer/lib/utils'
import { api, type ApiError } from '@renderer/lib/api'
import { useToastStore } from '@renderer/stores/toastStore'
import type { Partner, PartnerCreate, PartnerType, PaymentMethod } from '@renderer/types/partner'

interface PartnerFormDialogProps {
  open: boolean
  onClose: () => void
  onSaved: () => void
  partner?: Partner | null
}

type TabId = 'basic' | 'addresses' | 'contact' | 'trade' | 'bank' | 'notes'

const TABS: { id: TabId; label: string }[] = [
  { id: 'basic', label: 'Základné' },
  { id: 'addresses', label: 'Adresy' },
  { id: 'contact', label: 'Kontakt' },
  { id: 'trade', label: 'Obchod' },
  { id: 'bank', label: 'Banka' },
  { id: 'notes', label: 'Poznámky' }
]

// Validation field → tab mapping
const FIELD_TAB: Record<string, TabId> = {
  code: 'basic',
  name: 'basic',
  company_id: 'basic',
  vat_id: 'basic',
  email: 'contact',
  iban: 'bank',
  payment_due_days: 'trade',
  credit_limit: 'trade',
  discount_percent: 'trade'
}

export default function PartnerFormDialog({
  open,
  onClose,
  onSaved,
  partner
}: PartnerFormDialogProps): ReactElement | null {
  const { addToast } = useToastStore()
  const isEdit = partner != null

  // ── Active tab ──
  const [activeTab, setActiveTab] = useState<TabId>('basic')

  // ── Form state ──
  const [code, setCode] = useState(partner?.code ?? '')
  const [name, setName] = useState(partner?.name ?? '')
  const [partnerType, setPartnerType] = useState<PartnerType>(partner?.partner_type ?? 'customer')
  const [isActive, setIsActive] = useState(partner?.is_active ?? true)
  const [isVatPayer, setIsVatPayer] = useState(partner?.is_vat_payer ?? false)
  const [companyId, setCompanyId] = useState(partner?.company_id ?? '')
  const [taxId, setTaxId] = useState(partner?.tax_id ?? '')
  const [vatId, setVatId] = useState(partner?.vat_id ?? '')

  // Sídlo
  const [street, setStreet] = useState(partner?.street ?? '')
  const [city, setCity] = useState(partner?.city ?? '')
  const [zipCode, setZipCode] = useState(partner?.zip_code ?? '')
  const [countryCode, setCountryCode] = useState(partner?.country_code ?? 'SK')

  // Fakturačná adresa
  const hasBillingInit =
    isEdit &&
    !!(partner?.billing_street || partner?.billing_city || partner?.billing_zip_code)
  const [billingDifferent, setBillingDifferent] = useState(hasBillingInit)
  const [billingStreet, setBillingStreet] = useState(partner?.billing_street ?? '')
  const [billingCity, setBillingCity] = useState(partner?.billing_city ?? '')
  const [billingZipCode, setBillingZipCode] = useState(partner?.billing_zip_code ?? '')
  const [billingCountryCode, setBillingCountryCode] = useState(
    partner?.billing_country_code ?? 'SK'
  )

  // Dodacia adresa
  const hasShippingInit =
    isEdit &&
    !!(partner?.shipping_street || partner?.shipping_city || partner?.shipping_zip_code)
  const [shippingDifferent, setShippingDifferent] = useState(hasShippingInit)
  const [shippingStreet, setShippingStreet] = useState(partner?.shipping_street ?? '')
  const [shippingCity, setShippingCity] = useState(partner?.shipping_city ?? '')
  const [shippingZipCode, setShippingZipCode] = useState(partner?.shipping_zip_code ?? '')
  const [shippingCountryCode, setShippingCountryCode] = useState(
    partner?.shipping_country_code ?? 'SK'
  )

  // Kontakt
  const [phone, setPhone] = useState(partner?.phone ?? '')
  const [mobile, setMobile] = useState(partner?.mobile ?? '')
  const [email, setEmail] = useState(partner?.email ?? '')
  const [website, setWebsite] = useState(partner?.website ?? '')
  const [contactPerson, setContactPerson] = useState(partner?.contact_person ?? '')

  // Obchod
  const [paymentDueDays, setPaymentDueDays] = useState(partner?.payment_due_days ?? 14)
  const [creditLimit, setCreditLimit] = useState(partner?.credit_limit ?? 0)
  const [discountPercent, setDiscountPercent] = useState(partner?.discount_percent ?? 0)
  const [priceCategory, setPriceCategory] = useState(partner?.price_category ?? '')
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>(
    partner?.payment_method ?? 'transfer'
  )
  const [currency, setCurrency] = useState(partner?.currency ?? 'EUR')

  // Banka
  const [iban, setIban] = useState(partner?.iban ?? '')
  const [bankName, setBankName] = useState(partner?.bank_name ?? '')
  const [swiftBic, setSwiftBic] = useState(partner?.swift_bic ?? '')

  // Poznámky
  const [notes, setNotes] = useState(partner?.notes ?? '')

  // ── UI state ──
  const [saving, setSaving] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [warnings, setWarnings] = useState<Record<string, string>>({})

  // ── Validation ──
  const validate = useCallback((): boolean => {
    const errs: Record<string, string> = {}

    if (!code.trim()) errs.code = 'Kód partnera je povinný'
    if (!name.trim()) errs.name = 'Názov partnera je povinný'

    if (email.trim() && (!email.includes('@') || !email.includes('.'))) {
      errs.email = 'Neplatný formát emailu'
    }

    if (companyId.trim() && !/^\d+$/.test(companyId.trim())) {
      errs.company_id = 'IČO musí obsahovať len čísla'
    }

    if (vatId.trim() && !/^[A-Z]{2}\d{8,10}$/.test(vatId.trim())) {
      errs.vat_id = 'IČ DPH musí byť vo formáte SK/CZ (napr. SK2021234567)'
    }

    if (iban.trim()) {
      const cleanIban = iban.replace(/\s/g, '')
      if (cleanIban.length > 34) {
        errs.iban = 'IBAN môže mať maximálne 34 znakov'
      }
    }

    if (discountPercent < 0 || discountPercent > 100) {
      errs.discount_percent = 'Zľava musí byť 0-100%'
    }

    if (paymentDueDays < 0) {
      errs.payment_due_days = 'Splatnosť musí byť >= 0'
    }

    if (creditLimit < 0) {
      errs.credit_limit = 'Kreditný limit musí byť >= 0'
    }

    setErrors(errs)

    // Navigate to first tab with error
    if (Object.keys(errs).length > 0) {
      const firstErrorField = Object.keys(errs)[0]
      const targetTab = FIELD_TAB[firstErrorField]
      if (targetTab) setActiveTab(targetTab)
    }

    return Object.keys(errs).length === 0
  }, [code, name, email, companyId, vatId, iban, discountPercent, paymentDueDays, creditLimit])

  // ── Submit ──
  const handleSubmit = useCallback(
    async (e: FormEvent): Promise<void> => {
      e.preventDefault()
      if (!validate()) return

      setSaving(true)
      setWarnings({})
      try {
        const payload: PartnerCreate = {
          code: code.trim(),
          name: name.trim(),
          partner_type: partnerType,
          is_vat_payer: isVatPayer,
          company_id: companyId.trim() || undefined,
          tax_id: taxId.trim() || undefined,
          vat_id: vatId.trim() || undefined,
          street: street.trim() || undefined,
          city: city.trim() || undefined,
          zip_code: zipCode.trim() || undefined,
          country_code: countryCode.trim() || undefined,
          billing_street: billingDifferent ? billingStreet.trim() || undefined : undefined,
          billing_city: billingDifferent ? billingCity.trim() || undefined : undefined,
          billing_zip_code: billingDifferent ? billingZipCode.trim() || undefined : undefined,
          billing_country_code: billingDifferent
            ? billingCountryCode.trim() || undefined
            : undefined,
          shipping_street: shippingDifferent ? shippingStreet.trim() || undefined : undefined,
          shipping_city: shippingDifferent ? shippingCity.trim() || undefined : undefined,
          shipping_zip_code: shippingDifferent ? shippingZipCode.trim() || undefined : undefined,
          shipping_country_code: shippingDifferent
            ? shippingCountryCode.trim() || undefined
            : undefined,
          phone: phone.trim() || undefined,
          mobile: mobile.trim() || undefined,
          email: email.trim() || undefined,
          website: website.trim() || undefined,
          contact_person: contactPerson.trim() || undefined,
          payment_due_days: paymentDueDays,
          credit_limit: creditLimit,
          discount_percent: discountPercent,
          price_category: priceCategory.trim() || undefined,
          payment_method: paymentMethod,
          currency: currency.trim() || 'EUR',
          iban: iban.replace(/\s/g, '').trim() || undefined,
          bank_name: bankName.trim() || undefined,
          swift_bic: swiftBic.trim() || undefined,
          notes: notes.trim() || undefined,
          is_active: isActive
        }

        let result: Partner
        if (isEdit && partner) {
          // For update: omit code, send only changed fields
          const { code: _code, ...updatePayload } = payload
          result = await api.updatePartner(partner.id, updatePayload)
          addToast(`Partner ${partner.code} bol aktualizovaný`, 'success')
        } else {
          result = await api.createPartner(payload)
          addToast(`Partner ${result.code} bol vytvorený`, 'success')
        }

        // Show backend warnings (e.g. duplicate IČO)
        if (result.warnings && result.warnings.length > 0) {
          for (const w of result.warnings) {
            addToast(w, 'warning', 6000)
            if (w.toLowerCase().includes('ičo') || w.toLowerCase().includes('ico')) {
              setWarnings((prev) => ({ ...prev, company_id: w }))
            }
          }
        }

        onSaved()
      } catch (err) {
        const e = err as ApiError
        if (e.status === 409) {
          setErrors((prev) => ({ ...prev, code: 'Kód partnera už existuje' }))
          setActiveTab('basic')
          addToast('Partner s takýmto kódom už existuje', 'error')
        } else if (e.status === 422) {
          // Backend validation errors
          addToast(e.message || 'Chyba validácie', 'error')
          // Try to parse detail for field-level errors
          if (e.detail) {
            try {
              const details = JSON.parse(e.detail)
              if (Array.isArray(details)) {
                const fieldErrors: Record<string, string> = {}
                for (const d of details) {
                  const fieldName = d.loc?.[d.loc.length - 1]
                  if (fieldName && d.msg) {
                    fieldErrors[fieldName] = d.msg
                  }
                }
                setErrors((prev) => ({ ...prev, ...fieldErrors }))
                // Navigate to first error tab
                const firstField = Object.keys(fieldErrors)[0]
                if (firstField && FIELD_TAB[firstField]) {
                  setActiveTab(FIELD_TAB[firstField])
                }
              }
            } catch {
              // Ignore parse errors
            }
          }
        } else {
          addToast(e.message || 'Uloženie zlyhalo', 'error')
        }
      } finally {
        setSaving(false)
      }
    },
    [
      validate,
      isEdit,
      partner,
      code,
      name,
      partnerType,
      isVatPayer,
      companyId,
      taxId,
      vatId,
      street,
      city,
      zipCode,
      countryCode,
      billingDifferent,
      billingStreet,
      billingCity,
      billingZipCode,
      billingCountryCode,
      shippingDifferent,
      shippingStreet,
      shippingCity,
      shippingZipCode,
      shippingCountryCode,
      phone,
      mobile,
      email,
      website,
      contactPerson,
      paymentDueDays,
      creditLimit,
      discountPercent,
      priceCategory,
      paymentMethod,
      currency,
      iban,
      bankName,
      swiftBic,
      notes,
      isActive,
      onSaved,
      addToast
    ]
  )

  if (!open) return null

  // ── Shared input classes ──
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

  const clearFieldError = (field: string): void => {
    if (errors[field]) {
      setErrors((prev) => {
        const next = { ...prev }
        delete next[field]
        return next
      })
    }
  }

  const FieldError = ({ field }: { field: string }): ReactElement | null => {
    if (!errors[field]) return null
    return <p className="mt-1 text-xs text-red-500">{errors[field]}</p>
  }

  const FieldWarning = ({ field }: { field: string }): ReactElement | null => {
    if (!warnings[field]) return null
    return <p className="mt-1 text-xs text-yellow-600 dark:text-yellow-400">{warnings[field]}</p>
  }

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm" onClick={onClose} />

      {/* Dialog */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-xl w-full max-w-4xl max-h-[85vh] flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700 shrink-0">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              {isEdit ? `Upraviť partner: ${partner?.code}` : 'Nový partner'}
            </h2>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Tabs */}
          <div className="flex border-b border-gray-200 dark:border-gray-700 px-6 shrink-0 overflow-x-auto">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={cn(
                  'px-4 py-2.5 text-sm font-medium border-b-2 transition-colors whitespace-nowrap',
                  activeTab === tab.id
                    ? 'border-blue-600 text-blue-600 dark:text-blue-400 dark:border-blue-400'
                    : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                )}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Content — scrollable */}
          <form
            onSubmit={(e) => void handleSubmit(e)}
            className="flex-1 overflow-y-auto px-6 py-4"
          >
            {/* ── Tab: Základné ── */}
            {activeTab === 'basic' && (
              <div className="space-y-4">
                {/* Row 1: Kód (1/3) | Názov (2/3) */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className={labelCls}>
                      Kód partnera <span className="text-red-500">*</span>
                    </label>
                    {isEdit ? (
                      <div className={readonlyCls}>{partner?.code}</div>
                    ) : (
                      <>
                        <input
                          type="text"
                          value={code}
                          onChange={(e) => {
                            setCode(e.target.value)
                            clearFieldError('code')
                          }}
                          disabled={saving}
                          className={inputCls('code')}
                          maxLength={30}
                        />
                        <FieldError field="code" />
                      </>
                    )}
                  </div>
                  <div className="md:col-span-2">
                    <label className={labelCls}>
                      Názov <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => {
                        setName(e.target.value)
                        clearFieldError('name')
                      }}
                      disabled={saving}
                      className={inputCls('name')}
                      maxLength={100}
                    />
                    <FieldError field="name" />
                  </div>
                </div>

                {/* Row 2: Typ (1/3) | Aktívny (1/3) | Platca DPH (1/3) */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className={labelCls}>Typ partnera</label>
                    <select
                      value={partnerType}
                      onChange={(e) => setPartnerType(e.target.value as PartnerType)}
                      disabled={saving}
                      className={inputCls()}
                    >
                      <option value="customer">Odberateľ</option>
                      <option value="supplier">Dodávateľ</option>
                      <option value="both">Oba</option>
                    </select>
                  </div>
                  <div className="flex items-end pb-2">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={isActive}
                        onChange={(e) => setIsActive(e.target.checked)}
                        disabled={saving}
                        className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300">Aktívny</span>
                    </label>
                  </div>
                  <div className="flex items-end pb-2">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={isVatPayer}
                        onChange={(e) => setIsVatPayer(e.target.checked)}
                        disabled={saving}
                        className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300">Platca DPH</span>
                    </label>
                  </div>
                </div>

                {/* Row 3: IČO | DIČ | IČ DPH */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className={labelCls}>IČO</label>
                    <input
                      type="text"
                      value={companyId}
                      onChange={(e) => {
                        setCompanyId(e.target.value)
                        clearFieldError('company_id')
                      }}
                      disabled={saving}
                      className={inputCls('company_id')}
                      maxLength={20}
                    />
                    <FieldError field="company_id" />
                    <FieldWarning field="company_id" />
                  </div>
                  <div>
                    <label className={labelCls}>DIČ</label>
                    <input
                      type="text"
                      value={taxId}
                      onChange={(e) => setTaxId(e.target.value)}
                      disabled={saving}
                      className={inputCls()}
                    />
                  </div>
                  <div>
                    <label className={labelCls}>IČ DPH</label>
                    <input
                      type="text"
                      value={vatId}
                      onChange={(e) => {
                        setVatId(e.target.value)
                        clearFieldError('vat_id')
                      }}
                      disabled={saving}
                      className={inputCls('vat_id')}
                      placeholder="SK2021234567"
                    />
                    <FieldError field="vat_id" />
                  </div>
                </div>
              </div>
            )}

            {/* ── Tab: Adresy ── */}
            {activeTab === 'addresses' && (
              <div className="space-y-6">
                {/* Sídlo */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">
                    Sídlo
                  </h3>
                  <div className="space-y-4">
                    <div>
                      <label className={labelCls}>Ulica</label>
                      <input
                        type="text"
                        value={street}
                        onChange={(e) => setStreet(e.target.value)}
                        disabled={saving}
                        className={inputCls()}
                      />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div>
                        <label className={labelCls}>PSČ</label>
                        <input
                          type="text"
                          value={zipCode}
                          onChange={(e) => setZipCode(e.target.value)}
                          disabled={saving}
                          className={inputCls()}
                        />
                      </div>
                      <div>
                        <label className={labelCls}>Mesto</label>
                        <input
                          type="text"
                          value={city}
                          onChange={(e) => setCity(e.target.value)}
                          disabled={saving}
                          className={inputCls()}
                        />
                      </div>
                      <div>
                        <label className={labelCls}>Krajina</label>
                        <input
                          type="text"
                          value={countryCode}
                          onChange={(e) => setCountryCode(e.target.value)}
                          disabled={saving}
                          className={inputCls()}
                          maxLength={3}
                          placeholder="SK"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Fakturačná adresa toggle */}
                <div>
                  <label className="flex items-center gap-2 cursor-pointer mb-3">
                    <input
                      type="checkbox"
                      checked={billingDifferent}
                      onChange={(e) => setBillingDifferent(e.target.checked)}
                      disabled={saving}
                      className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Fakturačná adresa iná ako sídlo
                    </span>
                  </label>

                  {billingDifferent && (
                    <div className="pl-6 border-l-2 border-blue-200 dark:border-blue-800 space-y-4">
                      <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
                        Fakturačná adresa
                      </h3>
                      <div>
                        <label className={labelCls}>Ulica</label>
                        <input
                          type="text"
                          value={billingStreet}
                          onChange={(e) => setBillingStreet(e.target.value)}
                          disabled={saving}
                          className={inputCls()}
                        />
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                          <label className={labelCls}>PSČ</label>
                          <input
                            type="text"
                            value={billingZipCode}
                            onChange={(e) => setBillingZipCode(e.target.value)}
                            disabled={saving}
                            className={inputCls()}
                          />
                        </div>
                        <div>
                          <label className={labelCls}>Mesto</label>
                          <input
                            type="text"
                            value={billingCity}
                            onChange={(e) => setBillingCity(e.target.value)}
                            disabled={saving}
                            className={inputCls()}
                          />
                        </div>
                        <div>
                          <label className={labelCls}>Krajina</label>
                          <input
                            type="text"
                            value={billingCountryCode}
                            onChange={(e) => setBillingCountryCode(e.target.value)}
                            disabled={saving}
                            className={inputCls()}
                            maxLength={3}
                            placeholder="SK"
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Dodacia adresa toggle */}
                <div>
                  <label className="flex items-center gap-2 cursor-pointer mb-3">
                    <input
                      type="checkbox"
                      checked={shippingDifferent}
                      onChange={(e) => setShippingDifferent(e.target.checked)}
                      disabled={saving}
                      className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Dodacia adresa iná ako sídlo
                    </span>
                  </label>

                  {shippingDifferent && (
                    <div className="pl-6 border-l-2 border-green-200 dark:border-green-800 space-y-4">
                      <h3 className="text-sm font-semibold text-gray-900 dark:text-white">
                        Dodacia adresa
                      </h3>
                      <div>
                        <label className={labelCls}>Ulica</label>
                        <input
                          type="text"
                          value={shippingStreet}
                          onChange={(e) => setShippingStreet(e.target.value)}
                          disabled={saving}
                          className={inputCls()}
                        />
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                          <label className={labelCls}>PSČ</label>
                          <input
                            type="text"
                            value={shippingZipCode}
                            onChange={(e) => setShippingZipCode(e.target.value)}
                            disabled={saving}
                            className={inputCls()}
                          />
                        </div>
                        <div>
                          <label className={labelCls}>Mesto</label>
                          <input
                            type="text"
                            value={shippingCity}
                            onChange={(e) => setShippingCity(e.target.value)}
                            disabled={saving}
                            className={inputCls()}
                          />
                        </div>
                        <div>
                          <label className={labelCls}>Krajina</label>
                          <input
                            type="text"
                            value={shippingCountryCode}
                            onChange={(e) => setShippingCountryCode(e.target.value)}
                            disabled={saving}
                            className={inputCls()}
                            maxLength={3}
                            placeholder="SK"
                          />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* ── Tab: Kontakt ── */}
            {activeTab === 'contact' && (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={labelCls}>Telefón</label>
                    <input
                      type="text"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      disabled={saving}
                      className={inputCls()}
                    />
                  </div>
                  <div>
                    <label className={labelCls}>Mobil</label>
                    <input
                      type="text"
                      value={mobile}
                      onChange={(e) => setMobile(e.target.value)}
                      disabled={saving}
                      className={inputCls()}
                    />
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={labelCls}>Email</label>
                    <input
                      type="text"
                      value={email}
                      onChange={(e) => {
                        setEmail(e.target.value)
                        clearFieldError('email')
                      }}
                      disabled={saving}
                      className={inputCls('email')}
                    />
                    <FieldError field="email" />
                  </div>
                  <div>
                    <label className={labelCls}>Web</label>
                    <input
                      type="text"
                      value={website}
                      onChange={(e) => setWebsite(e.target.value)}
                      disabled={saving}
                      className={inputCls()}
                      placeholder="https://"
                    />
                  </div>
                </div>
                <div>
                  <label className={labelCls}>Kontaktná osoba</label>
                  <input
                    type="text"
                    value={contactPerson}
                    onChange={(e) => setContactPerson(e.target.value)}
                    disabled={saving}
                    className={inputCls()}
                  />
                </div>
              </div>
            )}

            {/* ── Tab: Obchod ── */}
            {activeTab === 'trade' && (
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={labelCls}>Splatnosť faktúr (dní)</label>
                    <input
                      type="number"
                      value={paymentDueDays}
                      onChange={(e) => {
                        setPaymentDueDays(Number(e.target.value))
                        clearFieldError('payment_due_days')
                      }}
                      disabled={saving}
                      className={inputCls('payment_due_days')}
                      min={0}
                    />
                    <FieldError field="payment_due_days" />
                  </div>
                  <div>
                    <label className={labelCls}>Kreditný limit (EUR)</label>
                    <input
                      type="number"
                      value={creditLimit}
                      onChange={(e) => {
                        setCreditLimit(Number(e.target.value))
                        clearFieldError('credit_limit')
                      }}
                      disabled={saving}
                      className={inputCls('credit_limit')}
                      min={0}
                      step="0.01"
                    />
                    <FieldError field="credit_limit" />
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={labelCls}>Zľava (%)</label>
                    <input
                      type="number"
                      value={discountPercent}
                      onChange={(e) => {
                        setDiscountPercent(Number(e.target.value))
                        clearFieldError('discount_percent')
                      }}
                      disabled={saving}
                      className={inputCls('discount_percent')}
                      min={0}
                      max={100}
                      step="0.1"
                    />
                    <FieldError field="discount_percent" />
                  </div>
                  <div>
                    <label className={labelCls}>Cenová kategória</label>
                    <input
                      type="text"
                      value={priceCategory}
                      onChange={(e) => setPriceCategory(e.target.value)}
                      disabled={saving}
                      className={inputCls()}
                    />
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={labelCls}>Spôsob platby</label>
                    <select
                      value={paymentMethod}
                      onChange={(e) => setPaymentMethod(e.target.value as PaymentMethod)}
                      disabled={saving}
                      className={inputCls()}
                    >
                      <option value="transfer">Prevod</option>
                      <option value="cash">Hotovosť</option>
                      <option value="cod">Dobierka</option>
                    </select>
                  </div>
                  <div>
                    <label className={labelCls}>Mena</label>
                    <input
                      type="text"
                      value={currency}
                      onChange={(e) => setCurrency(e.target.value.toUpperCase())}
                      disabled={saving}
                      className={inputCls()}
                      maxLength={3}
                      placeholder="EUR"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* ── Tab: Banka ── */}
            {activeTab === 'bank' && (
              <div className="space-y-4">
                <div>
                  <label className={labelCls}>IBAN</label>
                  <input
                    type="text"
                    value={iban}
                    onChange={(e) => {
                      setIban(e.target.value)
                      clearFieldError('iban')
                    }}
                    disabled={saving}
                    className={inputCls('iban')}
                    maxLength={40}
                    placeholder="SK89 0200 0000 0000 1234 5678"
                  />
                  <FieldError field="iban" />
                </div>
                <div>
                  <label className={labelCls}>Názov banky</label>
                  <input
                    type="text"
                    value={bankName}
                    onChange={(e) => setBankName(e.target.value)}
                    disabled={saving}
                    className={inputCls()}
                  />
                </div>
                <div>
                  <label className={labelCls}>SWIFT/BIC</label>
                  <input
                    type="text"
                    value={swiftBic}
                    onChange={(e) => setSwiftBic(e.target.value)}
                    disabled={saving}
                    className={inputCls()}
                    placeholder="SUBASKBX"
                  />
                </div>
              </div>
            )}

            {/* ── Tab: Poznámky ── */}
            {activeTab === 'notes' && (
              <div>
                <label className={labelCls}>Poznámky</label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  disabled={saving}
                  rows={6}
                  className={cn(inputCls(), 'resize-y min-h-[100px]')}
                />
              </div>
            )}
          </form>

          {/* Footer */}
          <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200 dark:border-gray-700 shrink-0">
            <button
              type="button"
              onClick={onClose}
              disabled={saving}
              className={cn(
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                'border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300',
                'hover:bg-gray-50 dark:hover:bg-gray-700',
                'disabled:opacity-50'
              )}
            >
              Zrušiť
            </button>
            <button
              type="button"
              onClick={(e) => void handleSubmit(e as unknown as FormEvent)}
              disabled={saving}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                'bg-blue-600 text-white hover:bg-blue-700',
                'disabled:opacity-50 disabled:cursor-not-allowed'
              )}
            >
              {saving && <Loader2 className="h-4 w-4 animate-spin" />}
              {isEdit ? 'Uložiť' : 'Vytvoriť'}
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
