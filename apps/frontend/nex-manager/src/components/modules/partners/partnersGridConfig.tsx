// Grid configuration for Partners (PAB) module
import type { GridConfig } from '@renderer/components/grids'
import type { Partner } from '@renderer/types/partner'

const TYPE_LABELS: Record<string, string> = {
  customer: 'Odberateľ',
  supplier: 'Dodávateľ',
  both: 'Oba'
}

const TYPE_CLASSES: Record<string, string> = {
  customer: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
  supplier: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
  both: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400'
}

export const partnersGridConfig: GridConfig<Partner> = {
  storageKeyPrefix: 'partners',
  defaultRowHeight: 28,
  columns: [
    { id: 'code', header: 'Kód', type: 'text', size: 100, visible: true },
    { id: 'name', header: 'Názov', type: 'text', size: 250, visible: true },
    {
      id: 'partner_type',
      header: 'Typ',
      type: 'custom',
      size: 110,
      visible: true,
      enumOptions: [
        { value: 'customer', label: 'Odberateľ' },
        { value: 'supplier', label: 'Dodávateľ' },
        { value: 'both', label: 'Oba' }
      ],
      cell: (value: string) => (
        <span
          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${TYPE_CLASSES[value] ?? TYPE_CLASSES.customer}`}
        >
          {TYPE_LABELS[value] ?? value}
        </span>
      )
    },
    { id: 'company_id', header: 'IČO', type: 'text', size: 120, visible: true },
    { id: 'tax_id', header: 'DIČ', type: 'text', size: 120, visible: false },
    { id: 'vat_id', header: 'IČ DPH', type: 'text', size: 130, visible: false },
    { id: 'is_vat_payer', header: 'Platca DPH', type: 'boolean', size: 100, visible: false },
    { id: 'city', header: 'Mesto', type: 'text', size: 150, visible: true },
    { id: 'zip_code', header: 'PSČ', type: 'text', size: 80, visible: false },
    { id: 'street', header: 'Ulica', type: 'text', size: 200, visible: false },
    { id: 'country_code', header: 'Krajina', type: 'text', size: 70, visible: false },
    { id: 'phone', header: 'Telefón', type: 'text', size: 130, visible: true },
    { id: 'mobile', header: 'Mobil', type: 'text', size: 130, visible: false },
    { id: 'email', header: 'Email', type: 'text', size: 200, visible: true },
    { id: 'website', header: 'Web', type: 'text', size: 180, visible: false },
    { id: 'contact_person', header: 'Kontakt', type: 'text', size: 150, visible: false },
    {
      id: 'is_active',
      header: 'Aktívny',
      type: 'custom',
      size: 80,
      visible: true,
      cell: (value: boolean) =>
        value ? (
          <span className="text-green-600 dark:text-green-400 font-medium">✓</span>
        ) : (
          <span className="text-gray-400 dark:text-gray-500">✗</span>
        )
    },
    {
      id: 'payment_due_days',
      header: 'Splatnosť',
      type: 'integer',
      size: 90,
      visible: false,
      align: 'right'
    },
    {
      id: 'credit_limit',
      header: 'Kredit. limit',
      type: 'currency',
      size: 120,
      visible: false,
      align: 'right'
    },
    {
      id: 'discount_percent',
      header: 'Zľava %',
      type: 'percent',
      size: 80,
      visible: false,
      align: 'right'
    },
    {
      id: 'payment_method',
      header: 'Platba',
      type: 'enum',
      size: 100,
      visible: false,
      enumOptions: [
        { value: 'transfer', label: 'Prevod' },
        { value: 'cash', label: 'Hotovosť' },
        { value: 'cod', label: 'Dobierka' }
      ]
    },
    { id: 'currency', header: 'Mena', type: 'text', size: 60, visible: false },
    { id: 'iban', header: 'IBAN', type: 'text', size: 220, visible: false },
    { id: 'bank_name', header: 'Banka', type: 'text', size: 150, visible: false },
    { id: 'swift_bic', header: 'SWIFT/BIC', type: 'text', size: 100, visible: false },
    { id: 'price_category', header: 'Cen. kategória', type: 'text', size: 110, visible: false },
    { id: 'notes', header: 'Poznámky', type: 'text', size: 200, visible: false },
    { id: 'created_at', header: 'Vytvorený', type: 'datetime', size: 150, visible: false },
    { id: 'updated_at', header: 'Aktualizovaný', type: 'datetime', size: 150, visible: false }
  ]
}
