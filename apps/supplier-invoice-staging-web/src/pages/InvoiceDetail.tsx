import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { createColumnHelper } from '@tanstack/react-table';
import { ArrowLeft, Check, Upload, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { DataGrid } from '@/components/ui/datagrid';
import { getInvoice } from '@/api/invoices';
import { STATUS_CONFIG, MATCH_METHOD_CONFIG } from '@/types/invoice';
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
  columnHelper.accessor('xml_line_number', {
    id: 'xml_line_number',
    header: '#',
    size: 50,
    enableColumnFilter: false,
  }),
  columnHelper.accessor('xml_product_name', {
    id: 'xml_product_name',
    header: 'Názov',
    size: 220,
    enableColumnFilter: true,
    filterFn: stringFilter,
  }),
  columnHelper.accessor('xml_ean', {
    id: 'xml_ean',
    header: 'EAN',
    size: 130,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => info.getValue() || '-',
  }),
  columnHelper.accessor('xml_quantity', {
    id: 'xml_quantity',
    header: 'Množstvo',
    size: 80,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => (
      <span className="text-right block">{info.getValue()}</span>
    ),
  }),
  columnHelper.accessor('xml_unit', {
    id: 'xml_unit',
    header: 'MJ',
    size: 50,
    enableColumnFilter: true,
    filterFn: stringFilter,
  }),
  columnHelper.accessor('xml_unit_price', {
    id: 'xml_unit_price',
    header: 'Cena/MJ',
    size: 100,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => (
      <span className="text-right block">{formatAmount(info.getValue())}</span>
    ),
  }),
  columnHelper.accessor('xml_total_price', {
    id: 'xml_total_price',
    header: 'Celkom',
    size: 100,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => (
      <span className="text-right block font-medium">{formatAmount(info.getValue())}</span>
    ),
  }),
  columnHelper.accessor('xml_vat_rate', {
    id: 'xml_vat_rate',
    header: 'DPH %',
    size: 70,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => (
      <span className="text-right block">{info.getValue()}%</span>
    ),
  }),
  columnHelper.accessor('matched', {
    id: 'matched',
    header: 'Zhoda',
    size: 80,
    enableColumnFilter: false,
    cell: (info) => {
      const matched = info.getValue();
      const method = info.row.original.matched_by;
      const confidence = info.row.original.match_confidence;
      if (!matched) return <span className="text-red-500">✗</span>;
      return (
        <div className="flex items-center gap-1">
          <span className="text-green-500">✓</span>
          {method && (
            <span className="text-xs text-slate-500">
              {MATCH_METHOD_CONFIG[method]?.label}
            </span>
          )}
          {confidence && (
            <span className="text-xs text-slate-400">
              {confidence}%
            </span>
          )}
        </div>
      );
    },
  }),
  columnHelper.accessor('nex_product_name', {
    id: 'nex_product_name',
    header: 'NEX Produkt',
    size: 180,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => {
      const value = info.getValue();
      if (!value) return <span className="text-slate-400">-</span>;
      return <span>{value}</span>;
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
    <div className="space-y-4 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate('/invoices')}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-3">
              <FileText className="h-6 w-6 text-blue-600" />
              {invoice.xml_invoice_number}
            </h1>
            <p className="text-slate-500">{invoice.xml_supplier_name}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {invoice.status === 'matched' && (
            <Button onClick={handleApprove} className="bg-green-600 hover:bg-green-700">
              <Check className="h-4 w-4 mr-2" />
              Schváliť
            </Button>
          )}
          {invoice.status === 'approved' && (
            <Button onClick={handleImport} className="bg-blue-600 hover:bg-blue-700">
              <Upload className="h-4 w-4 mr-2" />
              Import do NEX
            </Button>
          )}
        </div>
      </div>

      {/* Invoice Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Dodávateľ</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="font-semibold">{invoice.xml_supplier_name}</div>
            <div className="text-sm text-slate-500">IČO: {invoice.xml_supplier_ico}</div>
            <div className="text-sm text-slate-500">DIČ: {invoice.xml_supplier_dic || '-'}</div>
            <div className="text-sm text-slate-500">IČ DPH: {invoice.xml_supplier_ic_dph || '-'}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Dátumy</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-sm">
              <span className="text-slate-500">Vystavená:</span>{' '}
              <span className="font-medium">{new Date(invoice.xml_issue_date).toLocaleDateString('sk-SK')}</span>
            </div>
            <div className="text-sm">
              <span className="text-slate-500">DUZP:</span>{' '}
              <span className="font-medium">{invoice.xml_tax_point_date ? new Date(invoice.xml_tax_point_date).toLocaleDateString('sk-SK') : '-'}</span>
            </div>
            <div className="text-sm">
              <span className="text-slate-500">Splatnosť:</span>{' '}
              <span className="font-medium">{invoice.xml_due_date ? new Date(invoice.xml_due_date).toLocaleDateString('sk-SK') : '-'}</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Sumy</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-sm">
              <span className="text-slate-500">Základ:</span>{' '}
              <span className="font-medium">{formatAmount(invoice.xml_total_without_vat)}</span>
            </div>
            <div className="text-sm">
              <span className="text-slate-500">DPH:</span>{' '}
              <span className="font-medium">{formatAmount(invoice.xml_total_vat)}</span>
            </div>
            <div className="text-lg font-bold text-blue-600">
              {formatAmount(invoice.xml_total_with_vat)}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Stav</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Status:</span>
              <Badge className={`${statusConfig.bgClass} ${statusConfig.color}`}>
                {statusConfig.label}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Zhoda:</span>
              <span className="font-medium">{invoice.match_percent.toFixed(0)}%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Položky:</span>
              <span className="font-medium">{invoice.items_matched}/{invoice.item_count}</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Items DataGrid */}
      <div className="flex-1 flex flex-col min-h-0">
        <h2 className="text-lg font-semibold text-slate-900 mb-2">
          Položky faktúry ({items.length})
        </h2>
        <DataGrid
          data={items}
          columns={itemColumns}
          rowHeight={32}
          storageKey="invoice-items-columns"
          className="flex-1"
        />
      </div>
    </div>
  );
}
