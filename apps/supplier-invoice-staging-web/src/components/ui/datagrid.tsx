import { useState, useRef, useEffect, useMemo } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  flexRender,
  type ColumnDef,
  type SortingState,
  type ColumnFiltersState,
  type VisibilityState,
} from '@tanstack/react-table';
import { useVirtualizer } from '@tanstack/react-virtual';
import { ArrowUpDown, ArrowUp, ArrowDown, X, Settings2, Eye, EyeOff, ChevronUp, ChevronDown, RotateCcw } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

// Column config types
interface ColumnConfigItem {
  id: string;
  originalHeader: string;
  customHeader?: string;
  visible: boolean;
  order: number;
}

interface DataGridProps<T> {
  data: T[];
  columns: ColumnDef<T, any>[];
  onRowClick?: (row: T) => void;
  onRowDoubleClick?: (row: T) => void;
  rowHeight?: number;
  className?: string;
  storageKey?: string;
}

export function DataGrid<T extends { id: number | string }>({
  data,
  columns,
  onRowClick,
  onRowDoubleClick,
  rowHeight = 32,
  className,
  storageKey,
}: DataGridProps<T>) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [selectedRowId, setSelectedRowId] = useState<string | number | null>(null);
  const [focusedFilterIndex, setFocusedFilterIndex] = useState<number>(0);
  const [configOpen, setConfigOpen] = useState(false);

  const tableContainerRef = useRef<HTMLDivElement>(null);
  const filterInputRefs = useRef<(HTMLInputElement | null)[]>([]);

  // Extract column metadata
  const columnsMeta = useMemo(() => 
    columns.map(col => ({
      id: (col as any).id || (col as any).accessorKey || '',
      header: typeof (col as any).header === 'string' ? (col as any).header : '',
    })).filter(c => c.id),
    [columns]
  );

  // Column configuration state
  const [columnConfig, setColumnConfig] = useState<ColumnConfigItem[]>(() => {
    if (storageKey) {
      try {
        const saved = localStorage.getItem(storageKey);
        if (saved) return JSON.parse(saved);
      } catch (e) {}
    }
    return columnsMeta.map((col, index) => ({
      id: col.id,
      originalHeader: col.header,
      customHeader: undefined,
      visible: true,
      order: index,
    }));
  });

  // Sync config with columns
  useEffect(() => {
    setColumnConfig(prev => {
      const newConfig = columnsMeta.map((col, index) => {
        const existing = prev.find(p => p.id === col.id);
        if (existing) return { ...existing, originalHeader: col.header };
        return {
          id: col.id,
          originalHeader: col.header,
          customHeader: undefined,
          visible: true,
          order: prev.length + index,
        };
      });
      return newConfig.sort((a, b) => a.order - b.order);
    });
  }, [columnsMeta]);

  // Apply config to table
  const columnVisibility = useMemo(() => {
    const vis: VisibilityState = {};
    columnConfig.forEach(col => { vis[col.id] = col.visible; });
    return vis;
  }, [columnConfig]);

  const columnOrder = useMemo(() => 
    [...columnConfig].sort((a, b) => a.order - b.order).map(c => c.id),
    [columnConfig]
  );

  const columnsWithCustomHeaders = useMemo(() => {
    return columns.map(col => {
      const colId = (col as any).id || (col as any).accessorKey;
      const cfg = columnConfig.find(c => c.id === colId);
      if (cfg?.customHeader) return { ...col, header: cfg.customHeader };
      return col;
    });
  }, [columns, columnConfig]);

  const table = useReactTable({
    data,
    columns: columnsWithCustomHeaders,
    state: { sorting, columnFilters, columnVisibility, columnOrder },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  const { rows } = table.getRowModel();

  const rowVirtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => tableContainerRef.current,
    estimateSize: () => rowHeight,
    overscan: 10,
  });

  const virtualRows = rowVirtualizer.getVirtualItems();
  const totalSize = rowVirtualizer.getTotalSize();
  const activeFiltersCount = columnFilters.filter(f => f.value).length;

  const clearAllFilters = () => {
    setColumnFilters([]);
    filterInputRefs.current[0]?.focus();
  };

  // Column config handlers
  const handleVisibilityToggle = (id: string) => {
    setColumnConfig(prev => prev.map(col => 
      col.id === id ? { ...col, visible: !col.visible } : col
    ));
  };

  const handleHeaderChange = (id: string, customHeader: string) => {
    setColumnConfig(prev => prev.map(col =>
      col.id === id ? { ...col, customHeader: customHeader || undefined } : col
    ));
  };

  const handleMoveUp = (index: number) => {
    if (index === 0) return;
    setColumnConfig(prev => {
      const sorted = [...prev].sort((a, b) => a.order - b.order);
      const temp = sorted[index].order;
      sorted[index].order = sorted[index - 1].order;
      sorted[index - 1].order = temp;
      return sorted.sort((a, b) => a.order - b.order);
    });
  };

  const handleMoveDown = (index: number) => {
    const sorted = [...columnConfig].sort((a, b) => a.order - b.order);
    if (index === sorted.length - 1) return;
    setColumnConfig(prev => {
      const s = [...prev].sort((a, b) => a.order - b.order);
      const temp = s[index].order;
      s[index].order = s[index + 1].order;
      s[index + 1].order = temp;
      return s.sort((a, b) => a.order - b.order);
    });
  };

  const handleResetConfig = () => {
    const defaultConfig = columnsMeta.map((col, index) => ({
      id: col.id,
      originalHeader: col.header,
      customHeader: undefined,
      visible: true,
      order: index,
    }));
    setColumnConfig(defaultConfig);
  };

  const handleSaveConfig = () => {
    if (storageKey) {
      localStorage.setItem(storageKey, JSON.stringify(columnConfig));
    }
    setConfigOpen(false);
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const isInFilterInput = filterInputRefs.current.some(ref => ref === document.activeElement);

      if (e.key === 'Tab' && isInFilterInput) {
        e.preventDefault();
        const filterableCols = table.getAllColumns().filter(col => col.getCanFilter() && col.getIsVisible());
        const dir = e.shiftKey ? -1 : 1;
        const next = (focusedFilterIndex + dir + filterableCols.length) % filterableCols.length;
        setFocusedFilterIndex(next);
        filterInputRefs.current[next]?.focus();
        return;
      }

      if (e.key === 'Escape') {
        if (isInFilterInput) {
          const filterableCols = table.getAllColumns().filter(col => col.getCanFilter() && col.getIsVisible());
          const currentCol = filterableCols[focusedFilterIndex];
          if (currentCol?.getFilterValue()) {
            currentCol.setFilterValue('');
          } else {
            (document.activeElement as HTMLElement)?.blur();
          }
        } else {
          setSelectedRowId(null);
        }
        return;
      }

      if ((e.key === 'F2' || e.key === 'Enter') && isInFilterInput) {
        e.preventDefault();
        (document.activeElement as HTMLElement)?.blur();
        if (rows.length > 0) setSelectedRowId(rows[0].original.id);
        return;
      }

      if (!isInFilterInput) {
        const currentIndex = rows.findIndex(r => r.original.id === selectedRowId);

        if (e.key === 'ArrowDown') {
          e.preventDefault();
          const next = currentIndex < rows.length - 1 ? currentIndex + 1 : 0;
          setSelectedRowId(rows[next]?.original.id ?? null);
          rowVirtualizer.scrollToIndex(next, { align: 'auto' });
        }

        if (e.key === 'ArrowUp') {
          e.preventDefault();
          const prev = currentIndex > 0 ? currentIndex - 1 : rows.length - 1;
          setSelectedRowId(rows[prev]?.original.id ?? null);
          rowVirtualizer.scrollToIndex(prev, { align: 'auto' });
        }

        if (e.key === 'Enter' && selectedRowId != null) {
          const row = rows.find(r => r.original.id === selectedRowId);
          if (row) onRowDoubleClick?.(row.original);
        }

        if (e.key.length === 1 && !e.ctrlKey && !e.altKey && !e.metaKey) {
          setFocusedFilterIndex(0);
          filterInputRefs.current[0]?.focus();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [rows, selectedRowId, focusedFilterIndex, table, onRowDoubleClick, rowVirtualizer]);

  useEffect(() => {
    if (rows.length > 0 && (selectedRowId == null || !rows.find(r => r.original.id === selectedRowId))) {
      setSelectedRowId(rows[0]?.original.id ?? null);
    }
  }, [rows, selectedRowId]);

  useEffect(() => {
    filterInputRefs.current[0]?.focus();
  }, []);

  const sortedConfig = [...columnConfig].sort((a, b) => a.order - b.order);

  return (
    <div className={cn('flex flex-col border rounded-lg bg-white overflow-hidden', className)}>
      {/* Status bar */}
      <div className="px-4 py-2 bg-slate-50 border-b flex items-center justify-between text-sm">
        <span className="text-slate-600">
          {rows.length} z {data.length} záznamov
          {activeFiltersCount > 0 && (
            <span className="ml-2 text-blue-600">
              • {activeFiltersCount} {activeFiltersCount === 1 ? 'filter' : 'filtre'} aktívne
            </span>
          )}
        </span>
        <div className="flex items-center gap-2">
          {activeFiltersCount > 0 && (
            <button onClick={clearAllFilters} className="text-slate-500 hover:text-slate-700 flex items-center gap-1">
              <X className="h-3 w-3" /> Zrušiť filtre
            </button>
          )}

          {/* Column Config Button - Always Visible */}
          <button 
            onClick={() => setConfigOpen(true)}
            className="p-1.5 rounded hover:bg-slate-200 text-slate-600 hover:text-slate-900"
            title="Nastavenie stĺpcov"
          >
            <Settings2 className="h-4 w-4" />
          </button>

          {/* Column Config Dialog */}
          <Dialog open={configOpen} onOpenChange={setConfigOpen}>
            <DialogTrigger asChild>
              <span></span>
            </DialogTrigger>
            <DialogContent className="max-w-md">
              <DialogHeader>
                <DialogTitle>Nastavenie stĺpcov</DialogTitle>
              </DialogHeader>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {sortedConfig.map((col, index) => (
                  <div key={col.id} className={cn(
                    "flex items-center gap-2 p-2 rounded border",
                    col.visible ? "bg-white" : "bg-slate-50 opacity-60"
                  )}>
                    <div className="flex flex-col">
                      <button onClick={() => handleMoveUp(index)} disabled={index === 0}
                        className="text-slate-400 hover:text-slate-600 disabled:opacity-30">
                        <ChevronUp className="h-3 w-3" />
                      </button>
                      <button onClick={() => handleMoveDown(index)} disabled={index === sortedConfig.length - 1}
                        className="text-slate-400 hover:text-slate-600 disabled:opacity-30">
                        <ChevronDown className="h-3 w-3" />
                      </button>
                    </div>
                    <button onClick={() => handleVisibilityToggle(col.id)}
                      className={cn("p-1 rounded", col.visible ? "text-green-600" : "text-slate-400")}>
                      {col.visible ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
                    </button>
                    <div className="flex-1">
                      <Input value={col.customHeader ?? col.originalHeader}
                        onChange={(e) => handleHeaderChange(col.id, e.target.value)}
                        placeholder={col.originalHeader} className="h-8 text-sm" />
                      {col.customHeader && (
                        <div className="text-xs text-slate-400 mt-0.5">Pôvodný: {col.originalHeader}</div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex justify-between pt-4 border-t">
                <Button variant="ghost" onClick={handleResetConfig}>
                  <RotateCcw className="h-4 w-4 mr-2" /> Obnoviť pôvodné
                </Button>
                <div className="flex gap-2">
                  <Button variant="outline" onClick={() => setConfigOpen(false)}>Zrušiť</Button>
                  <Button onClick={handleSaveConfig}>Uložiť</Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Table */}
      <div ref={tableContainerRef} className="overflow-auto flex-1" style={{ maxHeight: '600px' }}>
        <table className="w-full border-collapse">
          <thead className="sticky top-0 z-10">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id} className="bg-slate-100">
                {headerGroup.headers.map((header) => (
                  <th key={header.id}
                    className="px-3 py-2 text-left text-sm font-semibold text-slate-700 border-b cursor-pointer hover:bg-slate-200 select-none"
                    style={{ width: header.getSize() }}
                    onClick={header.column.getToggleSortingHandler()}>
                    <div className="flex items-center gap-1">
                      {flexRender(header.column.columnDef.header, header.getContext())}
                      {header.column.getCanSort() && (
                        <span className="text-slate-400">
                          {header.column.getIsSorted() === 'asc' ? <ArrowUp className="h-3 w-3" /> :
                           header.column.getIsSorted() === 'desc' ? <ArrowDown className="h-3 w-3" /> :
                           <ArrowUpDown className="h-3 w-3" />}
                        </span>
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            ))}
            <tr className="bg-slate-50 border-b-2 border-slate-200">
              {table.getHeaderGroups()[0]?.headers.map((header) => {
                const column = header.column;
                const canFilter = column.getCanFilter();
                const filterValue = column.getFilterValue() as string ?? '';
                const visibleFilterable = table.getAllColumns().filter(c => c.getCanFilter() && c.getIsVisible());
                const filterIndex = visibleFilterable.findIndex(c => c.id === column.id);
                return (
                  <th key={header.id} className="px-1 py-1" style={{ width: header.getSize() }}>
                    {canFilter ? (
                      <div className="relative">
                        <input ref={(el) => { if (filterIndex >= 0) filterInputRefs.current[filterIndex] = el; }}
                          type="text" value={filterValue}
                          onChange={(e) => column.setFilterValue(e.target.value)}
                          onFocus={() => setFocusedFilterIndex(filterIndex)}
                          placeholder="..."
                          className={cn(
                            "w-full px-2 py-1 text-sm border rounded text-slate-900 placeholder-slate-400",
                            "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                            filterValue ? "bg-yellow-50 border-yellow-400" : "bg-white border-slate-300"
                          )} />
                        {filterValue && (
                          <button onClick={() => column.setFilterValue('')}
                            className="absolute right-1 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                            <X className="h-3 w-3" />
                          </button>
                        )}
                      </div>
                    ) : <div className="h-7" />}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody>
            {virtualRows.length > 0 && virtualRows[0].start > 0 && (
              <tr><td colSpan={columns.length} style={{ height: virtualRows[0].start }} /></tr>
            )}
            {virtualRows.map((virtualRow) => {
              const row = rows[virtualRow.index];
              const isSelected = row.original.id === selectedRowId;
              return (
                <tr key={row.id} data-index={virtualRow.index}
                  className={cn('border-b transition-colors cursor-pointer',
                    isSelected ? 'bg-blue-100 hover:bg-blue-150' :
                    virtualRow.index % 2 === 0 ? 'bg-white hover:bg-slate-50' : 'bg-slate-50/50 hover:bg-slate-100'
                  )}
                  style={{ height: rowHeight }}
                  onClick={() => { setSelectedRowId(row.original.id); onRowClick?.(row.original); }}
                  onDoubleClick={() => onRowDoubleClick?.(row.original)}>
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-3 py-1 text-sm text-slate-700">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              );
            })}
            {virtualRows.length > 0 && (
              <tr><td colSpan={columns.length} style={{ height: totalSize - (virtualRows[virtualRows.length - 1]?.end ?? 0) }} /></tr>
            )}
          </tbody>
        </table>
        {rows.length === 0 && (
          <div className="flex items-center justify-center py-12 text-slate-500">
            {activeFiltersCount > 0 ? 'Žiadne výsledky pre zadané filtre' : 'Žiadne záznamy'}
          </div>
        )}
      </div>
      <div className="px-4 py-1 bg-slate-50 border-t text-xs text-slate-500 flex gap-4">
        <span><kbd className="px-1 bg-slate-200 rounded">Tab</kbd> ďalší filter</span>
        <span><kbd className="px-1 bg-slate-200 rounded">Enter</kbd> do tabuľky</span>
        <span><kbd className="px-1 bg-slate-200 rounded">↑↓</kbd> navigácia</span>
        <span><kbd className="px-1 bg-slate-200 rounded">Esc</kbd> zrušiť</span>
      </div>
    </div>
  );
}
