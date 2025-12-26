import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { createColumnHelper } from '@tanstack/react-table';
import { ArrowLeft, Check, Upload, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { DataGrid, numericFilter } from '@/components/ui/datagrid';
import { getInvoice } from '@/api/invoices';
import { STATUS_CONFIG, MATCH_METHOD_CONFIG, VALIDATION_STATUS_CONFIG } from '@/types/invoice';
import type { InvoiceItem } from '@/types/invoice';

const columnHelper = createColumnHelper<InvoiceItem>();

function formatAmount(amount: number): string {
  return new Intl.NumberFormat('sk-SK', {
    style: 'currency',
    currency: 'EUR',
  }).format(amount);
}

const stringFilter = (row: any, columnId: string, filterValue: string) => {
  const value = row.getValue(columnId);
  if (value == null) return false;
  return String(value).toLowerCase().includes(filterValue.toLowerCase());
};

const itemColumns = [
  // === XML fields ===
  columnHelper.accessor('xml_line_number', {
    id: 'xml_line_number',
    header: '#',
    size: 40,
    enableColumnFilter: false,
  }),
  columnHelper.accessor('xml_product_name', {
    id: 'xml_product_name',
    header: 'Názov',
    size: 180,
    enableColumnFilter: true,
    filterFn: stringFilter,
  }),
  columnHelper.accessor('xml_seller_code', {
    id: 'xml_seller_code',
    header: 'Kód dod.',
    size: 80,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => info.getValue() || '-',
  }),
  columnHelper.accessor('xml_ean', {
    id: 'xml_ean',
    header: 'EAN',
    size: 110,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => info.getValue() || '-',
  }),
  columnHelper.accessor('xml_quantity', {
    id: 'xml_quantity',
    header: 'Množ.',
    size: 60,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => <span className="text-right block">{info.getValue()}</span>,
  }),
  columnHelper.accessor('xml_unit', {
    id: 'xml_unit',
    header: 'MJ',
    size: 40,
    enableColumnFilter: true,
    filterFn: stringFilter,
  }),
  columnHelper.accessor('xml_unit_price', {
    id: 'xml_unit_price',
    header: 'Cena/MJ',
    size: 80,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => <span className="text-right block">{formatAmount(info.getValue())}</span>,
  }),
  columnHelper.accessor('xml_total_price', {
    id: 'xml_total_price',
    header: 'Celkom',
    size: 80,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => <span className="text-right block font-medium">{formatAmount(info.getValue())}</span>,
  }),
  columnHelper.accessor('xml_vat_rate', {
    id: 'xml_vat_rate',
    header: 'DPH%',
    size: 50,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => <span className="text-right block">{info.getValue()}%</span>,
  }),
  columnHelper.accessor('xml_unit_price_vat', {
    id: 'xml_unit_price_vat',
    header: 'Cena+DPH',
    size: 80,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => <span className="text-right block">{info.getValue() ? formatAmount(info.getValue()!) : '-'}</span>,
  }),
  columnHelper.accessor('xml_total_price_vat', {
    id: 'xml_total_price_vat',
    header: 'Celk+DPH',
    size: 80,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => <span className="text-right block">{info.getValue() ? formatAmount(info.getValue()!) : '-'}</span>,
  }),
  // === Matching ===
  columnHelper.accessor('matched', {
    id: 'matched',
    header: 'Zhoda',
    size: 70,
    enableColumnFilter: false,
    cell: (info) => {
      const matched = info.getValue();
      const method = info.row.original.matched_by;
      const confidence = info.row.original.match_confidence;
      if (!matched) return <span className="text-red-500">✗</span>;
      return (
        <div className="flex items-center gap-1">
          <span className="text-green-500">✓</span>
          {method && <span className="text-slate-500">{MATCH_METHOD_CONFIG[method]?.label}</span>}
          {confidence && <span className="text-slate-400">{confidence}%</span>}
        </div>
      );
    },
  }),
  columnHelper.accessor('match_confidence', {
    id: 'match_confidence',
    header: 'Konf.',
    size: 50,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => info.getValue() ? `${info.getValue()}%` : '-',
  }),
  // === NEX fields ===
  columnHelper.accessor('nex_product_name', {
    id: 'nex_product_name',
    header: 'NEX Produkt',
    size: 150,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => info.getValue() || '-',
  }),
  columnHelper.accessor('nex_product_id', {
    id: 'nex_product_id',
    header: 'NEX ID',
    size: 60,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => info.getValue() || '-',
  }),
  columnHelper.accessor('nex_ean', {
    id: 'nex_ean',
    header: 'NEX EAN',
    size: 110,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => info.getValue() || '-',
  }),
  columnHelper.accessor('nex_stock_code', {
    id: 'nex_stock_code',
    header: 'Skl.kód',
    size: 70,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => info.getValue() || '-',
  }),
  columnHelper.accessor('nex_purchase_price', {
    id: 'nex_purchase_price',
    header: 'Nák.cena',
    size: 80,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => <span className="text-right block">{info.getValue() ? formatAmount(info.getValue()!) : '-'}</span>,
  }),
  columnHelper.accessor('nex_sales_price', {
    id: 'nex_sales_price',
    header: 'Pred.cena',
    size: 80,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => <span className="text-right block">{info.getValue() ? formatAmount(info.getValue()!) : '-'}</span>,
  }),
  columnHelper.accessor('nex_stock_id', {
    id: 'nex_stock_id',
    header: 'Sklad',
    size: 50,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => info.getValue() || '-',
  }),
  columnHelper.accessor('nex_facility_id', {
    id: 'nex_facility_id',
    header: 'Prev.',
    size: 50,
    enableColumnFilter: true,
    filterFn: numericFilter,
    cell: (info) => info.getValue() || '-',
  }),
  // === Validation ===
  columnHelper.accessor('validation_status', {
    id: 'validation_status',
    header: 'Valid.',
    size: 60,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => {
      const status = info.getValue();
      if (!status) return '-';
      const config = VALIDATION_STATUS_CONFIG[status];
      return <span className={config?.color}>{config?.label || status}</span>;
    },
  }),
];

export function InvoiceDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: invoice, isLoading } = useQuery({
    queryKey: ['invoice', id],
    queryFn: () => getInvoice(Number(id)),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">Načítavam faktúru...</div>
      </div>
    );
  }

  if (!invoice) {
    return (
      <div className="flex flex-col items-center justify-center h-64 gap-4">
        <div className="text-slate-500">Faktúra nenájdená</div>
        <Button variant="outline" onClick={() => navigate('/invoices')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Späť na zoznam
        </Button>
      </div>
    );
  }

  const statusConfig = STATUS_CONFIG[invoice.status];
  const items = invoice.items || [];

  const handleApprove = () => {
    console.log('Approve invoice:', invoice.id);
  };

  const handleImport = () => {
    console.log('Import invoice:', invoice.id);
  };

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between py-2 flex-shrink-0">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" onClick={() => navigate('/invoices')}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-xl font-bold text-slate-900 flex items-center gap-2">
              <FileText className="h-5 w-5 text-blue-600" />
              {invoice.xml_invoice_number}
            </h1>
            <p className="text-sm text-slate-500">{invoice.xml_supplier_name}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {invoice.status === 'matched' && (
            <Button onClick={handleApprove} size="sm" className="bg-green-600 hover:bg-green-700">
              <Check className="h-4 w-4 mr-1" /> Schváliť
            </Button>
          )}
          {invoice.status === 'approved' && (
            <Button onClick={handleImport} size="sm" className="bg-blue-600 hover:bg-blue-700">
              <Upload className="h-4 w-4 mr-1" /> Import
            </Button>
          )}
        </div>
      </div>

      {/* Invoice Info Cards - kompaktnejšie */}
      <div className="grid grid-cols-4 gap-2 flex-shrink-0 mb-2">
        <Card className="py-2">
          <CardHeader className="pb-1 pt-0 px-3">
            <CardTitle className="text-xs font-medium text-slate-600">Dodávateľ</CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0 text-xs">
            <div className="font-semibold truncate">{invoice.xml_supplier_name}</div>
            <div className="text-slate-500">IČO: {invoice.xml_supplier_ico}</div>
          </CardContent>
        </Card>

        <Card className="py-2">
          <CardHeader className="pb-1 pt-0 px-3">
            <CardTitle className="text-xs font-medium text-slate-600">Dátumy</CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0 text-xs">
            <div><span className="text-slate-500">Vyst:</span> {new Date(invoice.xml_issue_date).toLocaleDateString('sk-SK')}</div>
            <div><span className="text-slate-500">Splat:</span> {invoice.xml_due_date ? new Date(invoice.xml_due_date).toLocaleDateString('sk-SK') : '-'}</div>
          </CardContent>
        </Card>

        <Card className="py-2">
          <CardHeader className="pb-1 pt-0 px-3">
            <CardTitle className="text-xs font-medium text-slate-600">Sumy</CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0 text-xs">
            <div><span className="text-slate-500">Základ:</span> {formatAmount(invoice.xml_total_without_vat)}</div>
            <div className="text-base font-bold text-blue-600">{formatAmount(invoice.xml_total_with_vat)}</div>
          </CardContent>
        </Card>

        <Card className="py-2">
          <CardHeader className="pb-1 pt-0 px-3">
            <CardTitle className="text-xs font-medium text-slate-600">Stav</CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0 text-xs space-y-1">
            <Badge className={`${statusConfig.bgClass} ${statusConfig.color} text-xs`}>{statusConfig.label}</Badge>
            <div><span className="text-slate-500">Zhoda:</span> <span className="font-medium">{invoice.match_percent.toFixed(0)}%</span> ({invoice.items_matched}/{invoice.item_count})</div>
          </CardContent>
        </Card>
      </div>

      {/* Items DataGrid - flex-1 pre vyplnenie zvyšku */}
      <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
        <h2 className="text-sm font-semibold text-slate-900 mb-1 flex-shrink-0">
          Položky ({items.length})
        </h2>
        <DataGrid
          data={items}
          columns={itemColumns}
          rowHeight={24}
          storageKey="invoice-items-columns"
          className="flex-1 min-h-0"
        />
      </div>
    </div>
  );
}
