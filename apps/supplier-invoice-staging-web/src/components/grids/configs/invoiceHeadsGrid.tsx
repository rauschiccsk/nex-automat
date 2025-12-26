// Invoice Heads Grid Configuration
import type { GridConfig } from '../gridTypes';
import type { InvoiceHead } from '@/types/invoice';
import { STATUS_CONFIG } from '@/types/invoice';
import { Badge } from '@/components/ui/badge';

export const invoiceHeadsGridConfig: GridConfig<InvoiceHead> = {
  storageKeyPrefix: 'invoice-heads-v2',
  defaultRowHeight: 32,
  enableExport: true,
  columns: [
    {
      id: 'xml_invoice_number',
      header: 'Číslo faktúry',
      type: 'text',
      size: 130,
      cellClass: 'font-medium text-blue-600',
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
      id: 'xml_issue_date',
      header: 'Dátum vystavenia',
      type: 'date',
      size: 110,
    },
    {
      id: 'xml_due_date',
      header: 'Dátum splatnosti',
      type: 'date',
      size: 110,
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
      id: 'item_count',
      header: 'Položiek',
      type: 'integer',
      size: 70,
      align: 'center',
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
      id: 'xml_variable_symbol',
      header: 'VS',
      type: 'text',
      size: 100,
    },
    {
      id: 'xml_iban',
      header: 'IBAN',
      type: 'text',
      size: 180,
    },
    {
      id: 'created_at',
      header: 'Vytvorené',
      type: 'datetime',
      size: 140,
    },
  ],
};
