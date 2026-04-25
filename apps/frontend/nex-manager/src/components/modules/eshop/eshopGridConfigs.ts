// Grid configurations for ESHOP module
import type { GridConfig } from '@renderer/components/grids'
import type { EshopOrder, EshopProduct } from '@renderer/types/eshop'

export const eshopOrderGridConfig: GridConfig<EshopOrder> = {
  storageKeyPrefix: 'eshop-orders',
  defaultRowHeight: 28,
  columns: [
    { id: 'order_number', header: 'Číslo obj.', accessorKey: 'order_number', type: 'text', size: 140, visible: true },
    { id: 'customer_name', header: 'Zákazník', accessorKey: 'customer_name', type: 'text', size: 200, visible: true },
    { id: 'customer_email', header: 'Email', accessorKey: 'customer_email', type: 'text', size: 200, visible: false },
    { id: 'status', header: 'Stav', accessorKey: 'status', type: 'text', size: 110, visible: true },
    { id: 'payment_status', header: 'Platba', accessorKey: 'payment_status', type: 'text', size: 100, visible: true },
    { id: 'total_amount_vat', header: 'Suma s DPH', accessorKey: 'total_amount_vat', type: 'currency', size: 120, visible: true },
    { id: 'currency', header: 'Mena', accessorKey: 'currency', type: 'text', size: 60, visible: true },
    { id: 'created_at', header: 'Vytvorená', accessorKey: 'created_at', type: 'datetime', size: 150, visible: true }
  ]
}

export const eshopProductGridConfig: GridConfig<EshopProduct> = {
  storageKeyPrefix: 'eshop-products',
  defaultRowHeight: 28,
  columns: [
    { id: 'sku', header: 'SKU', accessorKey: 'sku', type: 'text', size: 120, visible: true },
    { id: 'name', header: 'Názov', accessorKey: 'name', type: 'text', size: 250, visible: true },
    { id: 'price_vat', header: 'Cena s DPH', accessorKey: 'price_vat', type: 'currency', size: 120, visible: true },
    { id: 'stock_quantity', header: 'Sklad', accessorKey: 'stock_quantity', type: 'integer', size: 80, visible: true },
    { id: 'is_active', header: 'Aktívny', accessorKey: 'is_active', type: 'boolean', size: 80, visible: true },
    { id: 'sort_order', header: 'Poradie', accessorKey: 'sort_order', type: 'integer', size: 80, visible: true },
    { id: 'barcode', header: 'Čiarový kód', accessorKey: 'barcode', type: 'text', size: 130, visible: false },
    { id: 'price', header: 'Cena bez DPH', accessorKey: 'price', type: 'currency', size: 120, visible: false },
    { id: 'vat_rate', header: 'DPH %', accessorKey: 'vat_rate', type: 'percent', size: 80, visible: false },
    { id: 'created_at', header: 'Vytvorený', accessorKey: 'created_at', type: 'datetime', size: 150, visible: false }
  ]
}
