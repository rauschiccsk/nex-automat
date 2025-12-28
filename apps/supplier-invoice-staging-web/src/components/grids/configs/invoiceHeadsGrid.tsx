// Invoice Heads Grid Configuration
import type { GridConfig } from '../gridTypes';
import type { InvoiceHead } from '@/types/invoice';
import { STATUS_CONFIG, VALIDATION_STATUS_CONFIG } from '@/types/invoice';
import { Badge } from '@/components/ui/badge';

export const invoiceHeadsGridConfig: GridConfig<InvoiceHead> = {
  storageKeyPrefix: 'invoice-heads-v3',
  defaultRowHeight: 32,
  enableExport: true,
  columns: [
    // === XML fields (from ISDOC) ===
    {
      id: 'xml_invoice_number',
      header: 'Číslo faktúry',
      type: 'text',
      size: 130,
      cellClass: 'font-medium text-blue-600',
    },
    {
      id: 'xml_variable_symbol',
      header: 'VS',
      type: 'text',
      size: 100,
    },
    {
      id: 'xml_supplier_name',
      header: 'Dodávateľ',
      type: 'text',
      size: 220,
    },
    {
      id: 'xml_supplier_ico',
      header: 'IČO',
      type: 'text',
      size: 100,
    },
    {
      id: 'xml_supplier_dic',
      header: 'DIČ',
      type: 'text',
      size: 120,
      visible: false,
    },
    {
      id: 'xml_supplier_ic_dph',
      header: 'IČ DPH',
      type: 'text',
      size: 130,
      visible: false,
    },
    {
      id: 'xml_issue_date',
      header: 'Dátum vystavenia',
      type: 'date',
      size: 110,
    },
    {
      id: 'xml_tax_point_date',
      header: 'Dátum zdan. plnenia',
      type: 'date',
      size: 120,
      visible: false,
    },
    {
      id: 'xml_due_date',
      header: 'Dátum splatnosti',
      type: 'date',
      size: 110,
    },
    {
      id: 'xml_currency',
      header: 'Mena',
      type: 'text',
      size: 60,
      align: 'center',
      visible: false,
    },
    {
      id: 'xml_total_without_vat',
      header: 'Základ',
      type: 'currency',
      size: 100,
    },
    {
      id: 'xml_total_vat',
      header: 'DPH',
      type: 'currency',
      size: 90,
    },
    {
      id: 'xml_total_with_vat',
      header: 'Celkom',
      type: 'currency',
      size: 110,
      cellClass: 'font-bold',
    },
    {
      id: 'xml_iban',
      header: 'IBAN',
      type: 'text',
      size: 180,
      visible: false,
    },
    {
      id: 'xml_swift',
      header: 'SWIFT',
      type: 'text',
      size: 100,
      visible: false,
    },
    {
      id: 'xml_file_path',
      header: 'XML súbor',
      type: 'text',
      size: 200,
      visible: false,
    },
    {
      id: 'pdf_file_path',
      header: 'PDF súbor',
      type: 'text',
      size: 200,
      visible: false,
    },

    // === NEX fields (enrichment) ===
    {
      id: 'nex_supplier_id',
      header: 'NEX Dodávateľ ID',
      type: 'integer',
      size: 100,
      visible: false,
    },
    {
      id: 'nex_supplier_modify_id',
      header: 'NEX Modify ID',
      type: 'integer',
      size: 100,
      visible: false,
    },
    {
      id: 'nex_iban',
      header: 'NEX IBAN',
      type: 'text',
      size: 180,
      visible: false,
    },
    {
      id: 'nex_swift',
      header: 'NEX SWIFT',
      type: 'text',
      size: 100,
      visible: false,
    },
    {
      id: 'nex_stock_id',
      header: 'Sklad ID',
      type: 'integer',
      size: 80,
      visible: false,
    },
    {
      id: 'nex_book_num',
      header: 'Číslo knihy',
      type: 'integer',
      size: 90,
      visible: false,
    },
    {
      id: 'nex_payment_method_id',
      header: 'Spôsob platby',
      type: 'integer',
      size: 100,
      visible: false,
    },
    {
      id: 'nex_price_list_id',
      header: 'Cenník ID',
      type: 'integer',
      size: 80,
      visible: false,
    },
    {
      id: 'nex_document_id',
      header: 'NEX Dokument ID',
      type: 'integer',
      size: 110,
      visible: false,
    },

    // === Workflow ===
    {
      id: 'status',
      header: 'Stav',
      type: 'custom',
      size: 120,
      cell: (value) => {
        const config = STATUS_CONFIG[value as keyof typeof STATUS_CONFIG] || {
          label: value,
          bgClass: 'bg-gray-100',
          color: 'text-gray-600',
        };
        return (
          <Badge className={`${config.bgClass} ${config.color} text-xs`}>
            {config.label}
          </Badge>
        );
      },
    },
    {
      id: 'item_count',
      header: 'Položiek',
      type: 'integer',
      size: 70,
      align: 'center',
    },
    {
      id: 'items_matched',
      header: 'Spárované',
      type: 'integer',
      size: 80,
      align: 'center',
      visible: false,
    },
    {
      id: 'match_percent',
      header: 'Zhoda',
      type: 'custom',
      size: 75,
      cell: (value) => {
        if (value == null) return '-';
        const colorClass = value >= 80 ? 'text-green-600' : value >= 50 ? 'text-yellow-600' : 'text-red-600';
        return <span className={`font-medium ${colorClass}`}>{value.toFixed(0)}%</span>;
      },
    },

    // === Validation ===
    {
      id: 'validation_status',
      header: 'Validácia',
      type: 'custom',
      size: 90,
      visible: false,
      cell: (value) => {
        if (!value) return '-';
        const config = VALIDATION_STATUS_CONFIG[value as keyof typeof VALIDATION_STATUS_CONFIG];
        return <span className={`font-medium ${config?.color || ''}`}>{config?.label || value}</span>;
      },
    },
    {
      id: 'validation_errors',
      header: 'Chyby validácie',
      type: 'text',
      size: 200,
      visible: false,
    },

    // === Timestamps ===
    {
      id: 'created_at',
      header: 'Vytvorené',
      type: 'datetime',
      size: 140,
    },
    {
      id: 'updated_at',
      header: 'Aktualizované',
      type: 'datetime',
      size: 140,
      visible: false,
    },
    {
      id: 'processed_at',
      header: 'Spracované',
      type: 'datetime',
      size: 140,
      visible: false,
    },
    {
      id: 'imported_at',
      header: 'Importované',
      type: 'datetime',
      size: 140,
      visible: false,
    },
  ],
};
