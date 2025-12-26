import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { createColumnHelper } from '@tanstack/react-table';
import { ArrowLeft, Check, X, FileText } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { DataGrid } from '@/components/ui/datagrid';
import { getInvoice } from '@/api/invoices';
import { STATUS_CONFIG, NEX_STATUS_CONFIG } from '@/types/invoice';
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
  columnHelper.accessor('line_number', {
    id: 'line_number',
    header: '#',
    size: 50,
    enableColumnFilter: false,
  }),
  columnHelper.accessor('original_name', {
    id: 'original_name',
    header: 'Názov',
    size: 220,
    enableColumnFilter: true,
    filterFn: stringFilter,
  }),
  columnHelper.accessor('original_ean', {
    id: 'original_ean',
    header: 'EAN',
    size: 130,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => info.getValue() || '-',
  }),
  columnHelper.accessor('quantity', {
    id: 'quantity',
    header: 'Množstvo',
    size: 80,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => (
      <span className="text-right block">{info.getValue()}</span>
    ),
  }),
  columnHelper.accessor('unit', {
    id: 'unit',
    header: 'MJ',
    size: 50,
    enableColumnFilter: true,
    filterFn: stringFilter,
  }),
  columnHelper.accessor('price_per_unit', {
    id: 'price_per_unit',
    header: 'Cena/MJ',
    size: 100,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => (
      <span className="text-right block">{formatAmount(info.getValue())}</span>
    ),
  }),
  columnHelper.accessor('vat_rate', {
    id: 'vat_rate',
    header: 'DPH %',
    size: 70,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => (
      <span className="text-right block">{info.getValue()}%</span>
    ),
  }),
  columnHelper.accessor('nex_gs_name', {
    id: 'nex_gs_name',
    header: 'NEX Produkt',
    size: 180,
    enableColumnFilter: true,
    filterFn: stringFilter,
    cell: (info) => {
      const value = info.getValue();
      const confidence = info.row.original.nex_match_confidence;
      if (!value) return <span className="text-slate-400">-</span>;
      return (
        <div>
          <span>{value}</span>
          {confidence && (
            <span className="ml-2 text-xs text-slate-500">
              ({Math.round(confidence * 100)}%)
            </span>
          )}
        </div>
      );
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
  const nexStatusConfig = NEX_STATUS_CONFIG[invoice.nex_status];
  const items = invoice.items || [];

  const handleApprove = () => {
    console.log('Approve invoice:', invoice.id);
  };

  const handleReject = () => {
    console.log('Reject invoice:', invoice.id);
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
              {invoice.invoice_number}
            </h1>
            <p className="text-slate-500">{invoice.supplier_name}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {invoice.status === 'pending_approval' && (
            <>
              <Button variant="outline" onClick={handleReject} className="text-red-600 hover:bg-red-50">
                <X className="h-4 w-4 mr-2" />
                Zamietnuť
              </Button>
              <Button onClick={handleApprove} className="bg-green-600 hover:bg-green-700">
                <Check className="h-4 w-4 mr-2" />
                Schváliť
              </Button>
            </>
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
            <div className="font-semibold">{invoice.supplier_name}</div>
            <div className="text-sm text-slate-500">IČO: {invoice.supplier_ico}</div>
            <div className="text-sm text-slate-500">DIČ: {invoice.supplier_dic}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Dátumy</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-sm">
              <span className="text-slate-500">Vystavená:</span>{' '}
              <span className="font-medium">{new Date(invoice.invoice_date).toLocaleDateString('sk-SK')}</span>
            </div>
            <div className="text-sm">
              <span className="text-slate-500">Splatnosť:</span>{' '}
              <span className="font-medium">{new Date(invoice.due_date!).toLocaleDateString('sk-SK')}</span>
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
              <span className="font-medium">{formatAmount(invoice.total_without_vat!)}</span>
            </div>
            <div className="text-sm">
              <span className="text-slate-500">DPH:</span>{' '}
              <span className="font-medium">{formatAmount(invoice.total_vat!)}</span>
            </div>
            <div className="text-lg font-bold text-blue-600">
              {formatAmount(invoice.total_amount)}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Stavy</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Faktúra:</span>
              <Badge className={`${statusConfig.color} text-white`}>
                {statusConfig.label}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">NEX:</span>
              <Badge className={`${nexStatusConfig.color} text-white`}>
                {nexStatusConfig.label}
              </Badge>
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
