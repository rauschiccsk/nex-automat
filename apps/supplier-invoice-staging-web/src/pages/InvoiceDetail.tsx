import { useState, useMemo, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, Check, Upload, FileText, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  BaseGrid,
  exportToCSV,
  formatCurrency,
  formatDate,
  invoiceItemsGridConfig,
} from '@/components/grids';
import { getInvoice } from '@/api/invoices';
import { getStagingConfig, type StagingConfig } from '@/api/config';
import { STATUS_CONFIG } from '@/types/invoice';
import type { InvoiceItem } from '@/types/invoice';

export function InvoiceDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: invoice, isLoading } = useQuery({
    queryKey: ['invoice', id],
    queryFn: () => getInvoice(Number(id)),
    enabled: !!id,
  });

  // Load staging config for permissions
  const { data: stagingConfig } = useQuery({
    queryKey: ['stagingConfig'],
    queryFn: getStagingConfig,
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  });

  // Determine editable columns based on config
  const editableColumns = useMemo(() => {
    if (!stagingConfig) return []; // No editing until config loaded

    const columns: string[] = [];
    if (stagingConfig.allow_margin_edit) {
      columns.push('nex_margin_percent');
    }
    if (stagingConfig.allow_price_edit) {
      columns.push('nex_sales_price');
    }
    return columns;
  }, [stagingConfig]);

  // Local state for edited items
  const [editedItems, setEditedItems] = useState<Map<number, Partial<InvoiceItem>>>(new Map());

  // Merge original items with edits
  const items = useMemo(() => {
    if (!invoice?.items) return [];
    return invoice.items.map(item => {
      const edits = editedItems.get(item.id);
      if (!edits) return item;
      return { ...item, ...edits };
    });
  }, [invoice?.items, editedItems]);

  // Calculate totals
  const totals = useMemo(() => {
    const purchaseTotal = items.reduce((sum, item) => sum + (item.xml_total_price || 0), 0);
    const salesTotal = items.reduce((sum, item) => {
      const salesPrice = item.nex_sales_price ?? item.xml_unit_price;
      return sum + (salesPrice * item.xml_quantity);
    }, 0);
    const marginTotal = purchaseTotal > 0 ? ((salesTotal - purchaseTotal) / purchaseTotal) * 100 : 0;
    return { purchaseTotal, salesTotal, marginTotal };
  }, [items]);

  // Handle cell edit with recalculations
  const handleCellEdit = useCallback((rowId: string | number, columnId: string, newValue: any) => {
    const numericId = typeof rowId === 'string' ? parseInt(rowId, 10) : rowId;
    const item = items.find(i => i.id === numericId);
    if (!item) return;

    const purchasePrice = item.xml_unit_price;
    let updates: Partial<InvoiceItem> = {};

    if (columnId === 'nex_margin_percent') {
      const margin = parseFloat(newValue) || 0;
      const salesPrice = purchasePrice * (1 + margin / 100);
      updates = {
        nex_margin_percent: margin,
        nex_sales_price: Math.round(salesPrice * 100) / 100,
      };
    } else if (columnId === 'nex_sales_price') {
      const salesPrice = parseFloat(newValue) || 0;
      const margin = purchasePrice > 0 ? ((salesPrice - purchasePrice) / purchasePrice) * 100 : 0;
      updates = {
        nex_sales_price: salesPrice,
        nex_margin_percent: Math.round(margin * 10) / 10,
      };
    }

    setEditedItems(prev => {
      const next = new Map(prev);
      const existing = next.get(numericId) || {};
      next.set(numericId, { ...existing, ...updates });
      return next;
    });
  }, [items]);

  // Export handler
  const handleExport = useCallback(() => {
    if (items.length === 0) return;
    const filename = `faktura-${invoice?.xml_invoice_number || id}-polozky`;
    exportToCSV(items, invoiceItemsGridConfig.columns, filename);
  }, [items, invoice, id]);

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
  const hasEdits = editedItems.size > 0;

  const handleApprove = () => {
    console.log('Approve invoice:', invoice.id, 'with edits:', Object.fromEntries(editedItems));
  };

  const handleImport = () => {
    console.log('Import invoice:', invoice.id);
  };

  const handleSaveEdits = () => {
    console.log('Save edits:', Object.fromEntries(editedItems));
    // TODO: API call to save edits
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
          <Button variant="outline" size="sm" onClick={handleExport} title="Export do CSV">
            <Download className="h-4 w-4 mr-1" /> Export
          </Button>
          {hasEdits && (
            <Button onClick={handleSaveEdits} size="sm" variant="outline" className="border-orange-400 text-orange-600">
              Uložiť zmeny ({editedItems.size})
            </Button>
          )}
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

      {/* Invoice Info Cards */}
      <div className="grid grid-cols-5 gap-2 flex-shrink-0 mb-2">
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
            <div><span className="text-slate-500">Vyst:</span> {formatDate(invoice.xml_issue_date)}</div>
            <div><span className="text-slate-500">Splat:</span> {formatDate(invoice.xml_due_date)}</div>
          </CardContent>
        </Card>

        <Card className="py-2">
          <CardHeader className="pb-1 pt-0 px-3">
            <CardTitle className="text-xs font-medium text-slate-600">Nákup</CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0 text-xs">
            <div className="text-base font-bold">{formatCurrency(totals.purchaseTotal)}</div>
            <div className="text-slate-500">bez DPH</div>
          </CardContent>
        </Card>

        <Card className="py-2 border-green-200 bg-green-50">
          <CardHeader className="pb-1 pt-0 px-3">
            <CardTitle className="text-xs font-medium text-green-700">Predaj / Marža</CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0 text-xs">
            <div className="text-base font-bold text-green-700">{formatCurrency(totals.salesTotal)}</div>
            <div className="text-green-600 font-medium">Marža: {totals.marginTotal.toFixed(1)}%</div>
          </CardContent>
        </Card>

        <Card className="py-2">
          <CardHeader className="pb-1 pt-0 px-3">
            <CardTitle className="text-xs font-medium text-slate-600">Stav</CardTitle>
          </CardHeader>
          <CardContent className="px-3 py-0 text-xs space-y-1">
            <Badge className={`${(STATUS_CONFIG[invoice.status] || STATUS_CONFIG['staged']).bgClass} ${(STATUS_CONFIG[invoice.status] || STATUS_CONFIG['staged']).color} text-xs`}>{(STATUS_CONFIG[invoice.status] || STATUS_CONFIG['staged']).label}</Badge>
            <div><span className="text-slate-500">Zhoda:</span> <span className="font-medium">{(invoice.match_percent ?? 0).toFixed(0)}%</span></div>
          </CardContent>
        </Card>
      </div>

      {/* Items Grid - using BaseGrid */}
      <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
        <h2 className="text-sm font-semibold text-slate-900 mb-1 flex-shrink-0">
          Položky ({items.length})
          {hasEdits && <span className="ml-2 text-orange-500 font-normal">• {editedItems.size} upravených</span>}
        </h2>
        <BaseGrid
          data={items}
          config={invoiceItemsGridConfig}
          editableColumns={editableColumns}
          onCellEdit={handleCellEdit}
          className="flex-1 min-h-0"
        />
      </div>
    </div>
  );
}
