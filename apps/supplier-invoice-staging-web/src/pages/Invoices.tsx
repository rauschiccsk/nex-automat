import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { createColumnHelper } from '@tanstack/react-table';
import { RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { DataGrid } from '@/components/ui/datagrid';
import { getInvoices } from '@/api/invoices';
import { STATUS_CONFIG } from '@/types/invoice';
import type { InvoiceHead } from '@/types/invoice';

const columnHelper = createColumnHelper<InvoiceHead>();

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('sk-SK');
}

function formatAmount(amount: number, currency: string = 'EUR'): string {
  return new Intl.NumberFormat('sk-SK', {
    style: 'currency',
    currency,
  }).format(amount);
}

const columns = [
  columnHelper.accessor('xml_invoice_number', {
    id: 'xml_invoice_number',
    header: 'Číslo faktúry',
    size: 150,
    enableColumnFilter: true,
    filterFn: 'includesString',
    cell: (info) => (
      <span className="font-medium text-blue-600">{info.getValue()}</span>
    ),
  }),
  columnHelper.accessor('xml_supplier_name', {
    id: 'xml_supplier_name',
    header: 'Dodávateľ',
    size: 220,
    enableColumnFilter: true,
    filterFn: 'includesString',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('xml_supplier_ico', {
    id: 'xml_supplier_ico',
    header: 'IČO',
    size: 100,
    enableColumnFilter: true,
    filterFn: 'includesString',
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor('xml_issue_date', {
    id: 'xml_issue_date',
    header: 'Dátum',
    size: 100,
    enableColumnFilter: true,
    filterFn: 'includesString',
    cell: (info) => formatDate(info.getValue()),
  }),
  columnHelper.accessor('xml_total_with_vat', {
    id: 'xml_total_with_vat',
    header: 'Suma',
    size: 110,
    enableColumnFilter: true,
    filterFn: (row, columnId, filterValue) => {
      const value = row.getValue(columnId) as number;
      return String(value).includes(filterValue);
    },
    cell: (info) => (
      <span className="font-medium text-right block">
        {formatAmount(info.getValue(), info.row.original.xml_currency)}
      </span>
    ),
  }),
  columnHelper.accessor('match_percent', {
    id: 'match_percent',
    header: 'Zhoda',
    size: 80,
    enableColumnFilter: true,
    filterFn: (row, columnId, filterValue) => {
      const value = row.getValue(columnId) as number;
      return String(value).includes(filterValue);
    },
    cell: (info) => {
      const value = info.getValue();
      const colorClass = value >= 80 ? 'text-green-600' : value >= 50 ? 'text-yellow-600' : 'text-red-600';
      return <span className={`font-medium ${colorClass}`}>{value.toFixed(0)}%</span>;
    },
  }),
  columnHelper.accessor('status', {
    id: 'status',
    header: 'Stav',
    size: 130,
    enableColumnFilter: true,
    filterFn: (row, columnId, filterValue) => {
      const status = row.getValue(columnId) as string;
      const config = STATUS_CONFIG[status as keyof typeof STATUS_CONFIG];
      const label = config?.label || status;
      return label.toLowerCase().includes(filterValue.toLowerCase());
    },
    cell: (info) => {
      const config = STATUS_CONFIG[info.getValue()] || { label: info.getValue(), bgClass: 'bg-gray-100', color: 'text-gray-600' };
      return (
        <Badge className={`${config.bgClass} ${config.color} text-xs`}>
          {config.label}
        </Badge>
      );
    },
  }),
];

export function Invoices() {
  const navigate = useNavigate();

  const { data, isLoading, refetch, isFetching } = useQuery({
    queryKey: ['invoices'],
    queryFn: () => getInvoices({ limit: 1000 }),
  });

  const invoices = data?.invoices ?? [];

  const handleRowClick = (invoice: InvoiceHead) => {
    console.log('Selected:', invoice.xml_invoice_number);
  };

  const handleRowDoubleClick = (invoice: InvoiceHead) => {
    navigate(`/invoices/${invoice.id}`);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">Načítavam faktúry...</div>
      </div>
    );
  }

  return (
    <div className="space-y-4 h-full flex flex-col">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Faktúry</h1>
          <p className="text-slate-500">{data?.count ?? 0} faktúr celkom</p>
        </div>
        <Button 
          variant="outline" 
          onClick={() => refetch()}
          disabled={isFetching}
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${isFetching ? 'animate-spin' : ''}`} />
          Obnoviť
        </Button>
      </div>

      <DataGrid
        data={invoices}
        columns={columns}
        onRowClick={handleRowClick}
        onRowDoubleClick={handleRowDoubleClick}
        storageKey="invoices-columns"
        className="flex-1"
      />
    </div>
  );
}
