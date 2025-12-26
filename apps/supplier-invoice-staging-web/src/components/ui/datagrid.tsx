import { useState, useRef, useEffect, useMemo, useCallback } from 'react';
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
  type ColumnSizingState,
  type ColumnOrderState,
} from '@tanstack/react-table';
import { useVirtualizer } from '@tanstack/react-virtual';
import { ArrowUpDown, ArrowUp, ArrowDown, X, Settings2, Eye, EyeOff, RotateCcw, GripVertical } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
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
  width?: number;
}

// Separate component for editable column header
function ColumnHeaderInput({ 
  value, 
  placeholder, 
  onChange 
}: { 
  value: string; 
  placeholder: string; 
  onChange: (value: string) => void;
}) {
  const [localValue, setLocalValue] = useState(value);

  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  return (
    <input
      type="text"
      value={localValue}
      onChange={(e) => setLocalValue(e.target.value)}
      onBlur={() => onChange(localValue)}
      placeholder={placeholder}
      className="w-full px-2 py-1 h-8 text-sm border rounded border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  );
}

// Component for column width input
function ColumnWidthInput({
  value,
  onChange,
}: {
  value: number;
  onChange: (value: number) => void;
}) {
  const [localValue, setLocalValue] = useState(String(value));

  useEffect(() => {
    setLocalValue(String(value));
  }, [value]);

  const handleBlur = () => {
    const num = parseInt(localValue, 10);
    if (isNaN(num) || num < 30) {
      setLocalValue(String(value));
    } else {
      onChange(Math.min(Math.max(num, 30), 800));
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleBlur();
      (e.target as HTMLInputElement).blur();
    }
  };

  return (
    <div className="flex items-center gap-1">
      <input
        type="text"
        inputMode="numeric"
        pattern="[0-9]*"
        value={localValue}
        onChange={(e) => setLocalValue(e.target.value.replace(/[^0-9]/g, ''))}
        onBlur={handleBlur}
        onKeyDown={handleKeyDown}
        className="w-14 px-2 py-1 h-7 text-xs text-center border rounded border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <span className="text-xs text-slate-400">px</span>
    </div>
  );
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

  // Drag state for column headers in grid
  const [draggedColumnId, setDraggedColumnId] = useState<string | null>(null);
  const [dragOverColumnId, setDragOverColumnId] = useState<string | null>(null);

  // Drag state for dialog
  const [dialogDraggedId, setDialogDraggedId] = useState<string | null>(null);
  const [dialogDragOverId, setDialogDragOverId] = useState<string | null>(null);

  const tableContainerRef = useRef<HTMLDivElement>(null);
  const filterInputRefs = useRef<(HTMLInputElement | null)[]>([]);

  // Extract column metadata with default widths
  const columnsMeta = useMemo(() => 
    columns.map(col => ({
      id: (col as any).id || (col as any).accessorKey || '',
      header: typeof (col as any).header === 'string' ? (col as any).header : '',
      defaultWidth: (col as any).size || 150,
    })).filter(c => c.id),
    [columns]
  );

  // Column configuration state
  const [columnConfig, setColumnConfig] = useState<ColumnConfigItem[]>(() => {
    if (storageKey) {
      try {
        const saved = localStorage.getItem(storageKey);
        if (saved) {
          const parsed = JSON.parse(saved);
          return columnsMeta.map((col, index) => {
            const existing = parsed.find((p: ColumnConfigItem) => p.id === col.id);
            if (existing) {
              return { ...existing, originalHeader: col.header };
            }
            return {
              id: col.id,
              originalHeader: col.header,
              customHeader: undefined,
              visible: true,
              order: parsed.length + index,
              width: undefined,
            };
          }).sort((a: ColumnConfigItem, b: ColumnConfigItem) => a.order - b.order);
        }
      } catch (e) {}
    }
    return columnsMeta.map((col, index) => ({
      id: col.id,
      originalHeader: col.header,
      customHeader: undefined,
      visible: true,
      order: index,
      width: undefined,
    }));
  });

  // Sync config with columns when columns change
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
          width: undefined,
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

  // Column sizing from config
  const columnSizing = useMemo(() => {
    const sizing: ColumnSizingState = {};
    columnConfig.forEach(col => {
      const defaultWidth = columnsMeta.find(c => c.id === col.id)?.defaultWidth || 150;
      sizing[col.id] = col.width ?? defaultWidth;
    });
    return sizing;
  }, [columnConfig, columnsMeta]);

  const columnsWithCustomHeaders = useMemo(() => {
    return columns.map(col => {
      const colId = (col as any).id || (col as any).accessorKey;
      const cfg = columnConfig.find(c => c.id === colId);
      if (cfg?.customHeader) return { ...col, header: cfg.customHeader };
      return col;
    });
  }, [columns, columnConfig]);

  // Update column order from drag & drop
  const handleColumnOrderChange = useCallback((newOrder: ColumnOrderState) => {
    setColumnConfig(prev => {
      return prev.map(col => ({
        ...col,
        order: newOrder.indexOf(col.id),
      })).sort((a, b) => a.order - b.order);
    });
  }, []);

  // Handle column sizing change from resize
  const handleColumnSizingChange = useCallback((updater: any) => {
    const newSizing = typeof updater === 'function' ? updater(columnSizing) : updater;
    setColumnConfig(prev => prev.map(col => ({
      ...col,
      width: newSizing[col.id] ?? col.width,
    })));
  }, [columnSizing]);

  const table = useReactTable({
    data,
    columns: columnsWithCustomHeaders,
    state: { sorting, columnFilters, columnVisibility, columnOrder, columnSizing },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnOrderChange: handleColumnOrderChange,
    onColumnSizingChange: handleColumnSizingChange,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
    columnResizeMode: 'onChange',
    enableColumnResizing: true,
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

  // Column header drag & drop handlers (for grid)
  const handleHeaderDragStart = (e: React.DragEvent, columnId: string) => {
    setDraggedColumnId(columnId);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', columnId);
  };

  const handleHeaderDragEnd = () => {
    setDraggedColumnId(null);
    setDragOverColumnId(null);
  };

  const handleHeaderDragOver = (e: React.DragEvent, columnId: string) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    if (columnId !== draggedColumnId) {
      setDragOverColumnId(columnId);
    }
  };

  const handleHeaderDragLeave = () => {
    setDragOverColumnId(null);
  };

  const handleHeaderDrop = (e: React.DragEvent, targetColumnId: string) => {
    e.preventDefault();

    if (!draggedColumnId || draggedColumnId === targetColumnId) {
      setDraggedColumnId(null);
      setDragOverColumnId(null);
      return;
    }

    const currentOrder = [...columnOrder];
    const draggedIndex = currentOrder.indexOf(draggedColumnId);
    const targetIndex = currentOrder.indexOf(targetColumnId);

    if (draggedIndex < 0 || targetIndex < 0) return;

    currentOrder.splice(draggedIndex, 1);
    currentOrder.splice(targetIndex, 0, draggedColumnId);

    handleColumnOrderChange(currentOrder);

    setDraggedColumnId(null);
    setDragOverColumnId(null);
  };

  // Dialog drag & drop handlers
  const handleDialogDragStart = (e: React.DragEvent, colId: string) => {
    setDialogDraggedId(colId);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', colId);
  };

  const handleDialogDragEnd = () => {
    setDialogDraggedId(null);
    setDialogDragOverId(null);
  };

  const handleDialogDragOver = (e: React.DragEvent, colId: string) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    if (colId !== dialogDraggedId) {
      setDialogDragOverId(colId);
    }
  };

  const handleDialogDragLeave = () => {
    setDialogDragOverId(null);
  };

  const handleDialogDrop = (e: React.DragEvent, targetId: string) => {
    e.preventDefault();

    if (!dialogDraggedId || dialogDraggedId === targetId) {
      setDialogDraggedId(null);
      setDialogDragOverId(null);
      return;
    }

    setColumnConfig(prev => {
      const sorted = [...prev].sort((a, b) => a.order - b.order);
      const draggedIndex = sorted.findIndex(c => c.id === dialogDraggedId);
      const targetIndex = sorted.findIndex(c => c.id === targetId);

      if (draggedIndex < 0 || targetIndex < 0) return prev;

      const newSorted = [...sorted];
      const [draggedItem] = newSorted.splice(draggedIndex, 1);
      newSorted.splice(targetIndex, 0, draggedItem);

      return newSorted.map((col, idx) => ({ ...col, order: idx }));
    });

    setDialogDraggedId(null);
    setDialogDragOverId(null);
  };

  // Column config handlers
  const handleVisibilityToggle = useCallback((id: string) => {
    setColumnConfig(prev => prev.map(col => 
      col.id === id ? { ...col, visible: !col.visible } : col
    ));
  }, []);

  const handleHeaderChange = useCallback((id: string, customHeader: string) => {
    setColumnConfig(prev => prev.map(col =>
      col.id === id ? { ...col, customHeader: customHeader || undefined } : col
    ));
  }, []);

  const handleWidthChange = useCallback((id: string, width: number) => {
    setColumnConfig(prev => prev.map(col =>
      col.id === id ? { ...col, width } : col
    ));
  }, []);

  const handleResetConfig = useCallback(() => {
    const defaultConfig = columnsMeta.map((col, index) => ({
      id: col.id,
      originalHeader: col.header,
      customHeader: undefined,
      visible: true,
      order: index,
      width: undefined,
    }));
    setColumnConfig(defaultConfig);
    if (storageKey) {
      localStorage.removeItem(storageKey);
    }
  }, [columnsMeta, storageKey]);

  const handleSaveConfig = useCallback(() => {
    if (storageKey) {
      localStorage.setItem(storageKey, JSON.stringify(columnConfig));
    }
    setConfigOpen(false);
  }, [storageKey, columnConfig]);

  // Auto-save on changes
  useEffect(() => {
    if (storageKey && !configOpen) {
      localStorage.setItem(storageKey, JSON.stringify(columnConfig));
    }
  }, [columnConfig, storageKey, configOpen]);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (configOpen) return;

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
  }, [rows, selectedRowId, focusedFilterIndex, table, onRowDoubleClick, rowVirtualizer, configOpen]);

  useEffect(() => {
    if (rows.length > 0 && (selectedRowId == null || !rows.find(r => r.original.id === selectedRowId))) {
      setSelectedRowId(rows[0]?.original.id ?? null);
    }
  }, [rows, selectedRowId]);

  useEffect(() => {
    filterInputRefs.current[0]?.focus();
  }, []);

  const sortedConfig = useMemo(() => 
    [...columnConfig].sort((a, b) => a.order - b.order),
    [columnConfig]
  );

  // Get current width for column
  const getColumnWidth = (colId: string) => {
    const cfg = columnConfig.find(c => c.id === colId);
    const defaultWidth = columnsMeta.find(c => c.id === colId)?.defaultWidth || 150;
    return cfg?.width ?? defaultWidth;
  };

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

          {/* Column Config Dialog */}
          <Dialog open={configOpen} onOpenChange={setConfigOpen}>
            <DialogTrigger asChild>
              <button 
                className="p-1.5 rounded hover:bg-slate-200 text-slate-600 hover:text-slate-900"
                title="Nastavenie stĺpcov"
              >
                <Settings2 className="h-4 w-4" />
              </button>
            </DialogTrigger>
            <DialogContent className="max-w-xl">
              <DialogHeader>
                <DialogTitle>Nastavenie stĺpcov</DialogTitle>
              </DialogHeader>
              <p className="text-xs text-slate-500 -mt-2 mb-2">Potiahnutím ⋮⋮ zmeníte poradie stĺpcov</p>
              <div className="space-y-1 max-h-96 overflow-y-auto">
                {sortedConfig.map((col) => (
                  <div 
                    key={col.id}
                    draggable
                    onDragStart={(e) => handleDialogDragStart(e, col.id)}
                    onDragEnd={handleDialogDragEnd}
                    onDragOver={(e) => handleDialogDragOver(e, col.id)}
                    onDragLeave={handleDialogDragLeave}
                    onDrop={(e) => handleDialogDrop(e, col.id)}
                    className={cn(
                      "flex items-center gap-2 p-2 rounded border transition-all",
                      col.visible ? "bg-white" : "bg-slate-50 opacity-60",
                      dialogDraggedId === col.id && "opacity-50 border-dashed border-slate-400",
                      dialogDragOverId === col.id && "border-blue-500 border-2 bg-blue-50"
                    )}
                  >
                    {/* Drag handle */}
                    <div 
                      className="cursor-grab active:cursor-grabbing p-1 text-slate-400 hover:text-slate-600"
                      title="Potiahnite pre zmenu poradia"
                    >
                      <GripVertical className="h-4 w-4" />
                    </div>

                    {/* Visibility toggle */}
                    <button 
                      type="button"
                      onClick={() => handleVisibilityToggle(col.id)}
                      className={cn("p-1 rounded hover:bg-slate-100", col.visible ? "text-green-600" : "text-slate-400")}
                      title={col.visible ? "Skryť stĺpec" : "Zobraziť stĺpec"}
                    >
                      {col.visible ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
                    </button>

                    {/* Column name */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <code className="text-xs px-1.5 py-0.5 bg-slate-100 rounded text-slate-600 font-mono truncate">
                          {col.id}
                        </code>
                      </div>
                      <ColumnHeaderInput
                        value={col.customHeader ?? col.originalHeader}
                        placeholder={col.originalHeader}
                        onChange={(value) => handleHeaderChange(col.id, value)}
                      />
                    </div>

                    {/* Width input */}
                    <div className="flex flex-col items-end gap-1">
                      <span className="text-xs text-slate-400">Šírka</span>
                      <ColumnWidthInput
                        value={getColumnWidth(col.id)}
                        onChange={(width) => handleWidthChange(col.id, width)}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex justify-between pt-4 border-t">
                <Button type="button" variant="ghost" onClick={handleResetConfig}>
                  <RotateCcw className="h-4 w-4 mr-2" /> Obnoviť pôvodné
                </Button>
                <div className="flex gap-2">
                  <Button type="button" variant="outline" onClick={() => setConfigOpen(false)}>Zrušiť</Button>
                  <Button type="button" onClick={handleSaveConfig}>Uložiť</Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Table */}
      <div ref={tableContainerRef} className="overflow-auto flex-1" style={{ maxHeight: '600px' }}>
        <table className="w-full border-collapse" style={{ width: table.getTotalSize() }}>
          <thead className="sticky top-0 z-10">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id} className="bg-slate-100">
                {headerGroup.headers.map((header) => (
                  <th 
                    key={header.id}
                    draggable
                    onDragStart={(e) => handleHeaderDragStart(e, header.column.id)}
                    onDragEnd={handleHeaderDragEnd}
                    onDragOver={(e) => handleHeaderDragOver(e, header.column.id)}
                    onDragLeave={handleHeaderDragLeave}
                    onDrop={(e) => handleHeaderDrop(e, header.column.id)}
                    className={cn(
                      "px-3 py-2 text-left text-sm font-semibold text-slate-700 border-b select-none relative group",
                      "hover:bg-slate-200 cursor-grab active:cursor-grabbing",
                      dragOverColumnId === header.column.id && "bg-blue-100 border-l-2 border-l-blue-500",
                      draggedColumnId === header.column.id && "opacity-50"
                    )}
                    style={{ width: header.getSize() }}
                  >
                    <div 
                      className="flex items-center gap-1 cursor-pointer"
                      onClick={header.column.getToggleSortingHandler()}
                    >
                      {flexRender(header.column.columnDef.header, header.getContext())}
                      {header.column.getCanSort() && (
                        <span className="text-slate-400">
                          {header.column.getIsSorted() === 'asc' ? <ArrowUp className="h-3 w-3" /> :
                           header.column.getIsSorted() === 'desc' ? <ArrowDown className="h-3 w-3" /> :
                           <ArrowUpDown className="h-3 w-3" />}
                        </span>
                      )}
                    </div>
                    {/* Resize handle */}
                    <div
                      onMouseDown={header.getResizeHandler()}
                      onTouchStart={header.getResizeHandler()}
                      onClick={(e) => e.stopPropagation()}
                      className={cn(
                        "absolute right-0 top-0 h-full w-1 cursor-col-resize select-none touch-none",
                        "hover:bg-blue-500 active:bg-blue-600",
                        header.column.getIsResizing() && "bg-blue-500"
                      )}
                    />
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
                    <td key={cell.id} className="px-3 py-1 text-sm text-slate-700" style={{ width: cell.column.getSize() }}>
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
