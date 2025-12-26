// Invoice Items Grid Configuration
import type { GridConfig } from '../gridTypes';
import type { InvoiceItem } from '@/types/invoice';
import { MATCH_METHOD_CONFIG, VALIDATION_STATUS_CONFIG } from '@/types/invoice';

export const invoiceItemsGridConfig: GridConfig<InvoiceItem> = {
  storageKeyPrefix: 'invoice-items-v3',
  defaultRowHeight: 24,
  enableExport: true,
  columns: [
    // === XML Fields (from ISDOC) ===
    {
      id: 'xml_line_number',
      header: '#',
      type: 'integer',
      size: 40,
      enableFilter: false,
    },
    {
      id: 'xml_product_name',
      header: 'Názov produktu',
      type: 'text',
      size: 200,
    },
    {
      id: 'xml_seller_code',
      header: 'Kód dod.',
      type: 'text',
      size: 80,
    },
    {
      id: 'xml_ean',
      header: 'EAN',
      type: 'text',
      size: 110,
    },
    {
      id: 'xml_quantity',
      header: 'Množstvo',
      type: 'number',
      size: 70,
      align: 'right',
    },
    {
      id: 'xml_unit',
      header: 'MJ',
      type: 'text',
      size: 45,
      align: 'center',
    },
    {
      id: 'xml_unit_price',
      header: 'Nák. cena',
      type: 'currency',
      size: 90,
    },
    {
      id: 'xml_total_price',
      header: 'Nák. celkom',
      type: 'currency',
      size: 100,
      cellClass: 'font-medium',
    },

    // === Pricing (Editable) ===
    {
      id: 'nex_margin_percent',
      header: 'Marža %',
      type: 'percent',
      size: 75,
      editable: true,
      cellClass: 'font-medium text-green-700',
    },
    {
      id: 'nex_sales_price',
      header: 'Pred. cena',
      type: 'currency',
      size: 90,
      editable: true,
      cellClass: 'font-medium text-blue-700',
    },

    // === Tax ===
    {
      id: 'xml_vat_rate',
      header: 'DPH %',
      type: 'percent',
      size: 60,
    },

    // === Matching ===
    {
      id: 'matched',
      header: 'Zhoda',
      type: 'custom',
      size: 90,
      enableFilter: false,
      cell: (value, row) => {
        if (!value) return <span className="text-red-500">✗</span>;
        const method = row.matched_by;
        const confidence = row.match_confidence;
        return (
          <div className="flex items-center gap-1">
            <span className="text-green-500">✓</span>
            {method && (
              <span className="text-slate-500 text-xs">
                {MATCH_METHOD_CONFIG[method]?.label}
              </span>
            )}
            {confidence && (
              <span className="text-slate-400 text-xs">{confidence}%</span>
            )}
          </div>
        );
      },
    },

    // === NEX Fields ===
    {
      id: 'nex_product_name',
      header: 'NEX Produkt',
      type: 'text',
      size: 150,
    },
    {
      id: 'nex_product_id',
      header: 'NEX ID',
      type: 'integer',
      size: 70,
    },
    {
      id: 'nex_ean',
      header: 'NEX EAN',
      type: 'text',
      size: 110,
    },
    {
      id: 'nex_stock_code',
      header: 'Skl. kód',
      type: 'text',
      size: 80,
    },
    {
      id: 'nex_purchase_price',
      header: 'NEX Nák.',
      type: 'currency',
      size: 90,
    },

    // === Validation ===
    {
      id: 'validation_status',
      header: 'Validácia',
      type: 'custom',
      size: 70,
      cell: (value) => {
        if (!value) return '-';
        const config = VALIDATION_STATUS_CONFIG[value as keyof typeof VALIDATION_STATUS_CONFIG];
        return <span className={config?.color}>{config?.label || value}</span>;
      },
    },
  ],
};

// Helper to get editable column IDs
export const invoiceItemsEditableColumns = invoiceItemsGridConfig.columns
  .filter(c => c.editable)
  .map(c => c.id);
