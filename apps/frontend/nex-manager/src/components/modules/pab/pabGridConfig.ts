// Grid configuration for PAB (Partner Catalog) module
import type { GridConfig } from '@renderer/components/grids'
import type { PartnerCatalog } from '@renderer/types/pab'

export const pabGridConfig: GridConfig<PartnerCatalog> = {
  storageKeyPrefix: 'pab-partners',
  defaultRowHeight: 28,
  columns: [
    { id: 'partner_id', header: 'ID', accessorKey: 'partner_id', type: 'integer', size: 70, visible: true },
    { id: 'partner_name', header: 'Názov firmy', accessorKey: 'partner_name', type: 'text', size: 250, visible: true },
    { id: 'company_id', header: 'IČO', accessorKey: 'company_id', type: 'text', size: 120, visible: true },
    { id: 'tax_id', header: 'DIČ', accessorKey: 'tax_id', type: 'text', size: 120, visible: false },
    { id: 'vat_id', header: 'IČ DPH', accessorKey: 'vat_id', type: 'text', size: 130, visible: false },
    { id: 'city', header: 'Mesto', accessorKey: 'city', type: 'text', size: 150, visible: true },
    { id: 'partner_class', header: 'Trieda', accessorKey: 'partner_class', type: 'text', size: 110, visible: true },
    { id: 'is_active', header: 'Aktívny', accessorKey: 'is_active', type: 'boolean', size: 80, visible: true },
    { id: 'is_supplier', header: 'Dodávateľ', accessorKey: 'is_supplier', type: 'boolean', size: 90, visible: true },
    { id: 'is_customer', header: 'Odberateľ', accessorKey: 'is_customer', type: 'boolean', size: 90, visible: true },
    { id: 'street', header: 'Ulica', accessorKey: 'street', type: 'text', size: 200, visible: false },
    { id: 'zip_code', header: 'PSČ', accessorKey: 'zip_code', type: 'text', size: 80, visible: false },
    { id: 'country_code', header: 'Krajina', accessorKey: 'country_code', type: 'text', size: 70, visible: false },
    { id: 'modify_id', header: 'Verzia', accessorKey: 'modify_id', type: 'integer', size: 70, visible: false },
    { id: 'bank_account_count', header: 'Bankové účty', accessorKey: 'bank_account_count', type: 'integer', size: 100, visible: false },
    { id: 'facility_count', header: 'Prevádzkarne', accessorKey: 'facility_count', type: 'integer', size: 100, visible: false },
    { id: 'created_at', header: 'Vytvorený', accessorKey: 'created_at', type: 'datetime', size: 150, visible: false },
    { id: 'updated_at', header: 'Aktualizovaný', accessorKey: 'updated_at', type: 'datetime', size: 150, visible: false }
  ]
}
