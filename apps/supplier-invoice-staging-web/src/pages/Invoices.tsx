import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { RefreshCw, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { 
  BaseGrid, 
  exportToCSV, 
  invoiceHeadsGridConfig 
} from '@/components/grids';
import { getInvoices } from '@/api/invoices';
import type { InvoiceHead } from '@/types/invoice';

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

  const handleExport = () => {
    if (invoices.length === 0) return;
    exportToCSV(invoices, invoiceHeadsGridConfig.columns, 'faktury-export');
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
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={handleExport}>
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button 
            variant="outline" 
            onClick={() => refetch()}
            disabled={isFetching}
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${isFetching ? 'animate-spin' : ''}`} />
            Obnoviť
          </Button>
        </div>
      </div>

      <BaseGrid
        data={invoices}
        config={invoiceHeadsGridConfig}
        onRowClick={handleRowClick}
        onRowDoubleClick={handleRowDoubleClick}
        rowHeight={32}
        className="flex-1"
      />
    </div>
  );
}
