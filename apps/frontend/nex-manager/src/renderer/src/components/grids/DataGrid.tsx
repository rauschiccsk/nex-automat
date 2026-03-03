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
import { ArrowUpDown, ArrowUp, ArrowDown, X, Settings2, Eye, EyeOff, RotateCcw, GripVertical, ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@renderer/lib/utils';

// === COLUMN CONFIG DIALOG (native, no Radix) ===
interface ColumnConfigDialogProps {
  open: boolean;
  onClose: () => void;
  sortedConfig: ColumnConfigItem[];
  columnsMeta: { id: string; header: string; defaultWidth: number }[];
  getColumnWidth: (colId: string) => number;
  onVisibilityToggle: (id: string) => void;
  onHeaderChange: (id: string, customHeader: string) => void;
  onWidthChange: (id: string, width: number) => void;
  onResetConfig: () => void;
  onSaveConfig: () => void;
  onDialogDragStart: (e: React.DragEvent, colId: string) => void;
  onDialogDragEnd: () => void;
  onDialogDragOver: (e: React.DragEvent, colId: string) => void;
  onDialogDragLeave: () => void;
  onDialogDrop: (e: React.DragEvent, targetId: string) => void;
  dialogDraggedId: string | null;
  dialogDragOverId: string | null;
}

function ColumnConfigDialog({
  open, onClose, sortedConfig, onVisibilityToggle, onHeaderChange,
  onWidthChange, onResetConfig, onSaveConfig, getColumnWidth,
  onDialogDragStart, onDialogDragEnd, onDialogDragOver, onDialogDragLeave, onDialogDrop,
  dialogDraggedId, dialogDragOverId,
}: ColumnConfigDialogProps) {
  useEffect(() => {
    if (!open) return;
    const handleKeyDown = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      {/* Dialog */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-xl w-full max-w-xl max-h-[85vh] flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700 shrink-0">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Nastavenie stĺpcov</h2>
            <button onClick={onClose} className="p-1.5 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto px-6 py-4">
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">Potiahnutím ⋮⋮ zmeníte poradie stĺpcov</p>
            <div className="space-y-1">
              {sortedConfig.map((col) => (
                <div key={col.id}
                  onDragOver={(e) => onDialogDragOver(e, col.id)}
                  onDragLeave={onDialogDragLeave}
                  onDrop={(e) => onDialogDrop(e, col.id)}
                  className={cn(
                    "flex items-center gap-2 p-2 rounded border transition-all",
                    col.visible
                      ? "bg-white dark:bg-gray-800"
                      : "bg-gray-50 dark:bg-gray-700/50 opacity-60",
                    dialogDraggedId === col.id && "opacity-50 border-dashed border-gray-400 dark:border-gray-500",
                    dialogDragOverId === col.id && "border-blue-500 border-2 bg-blue-50 dark:bg-blue-900/30",
                    dialogDraggedId !== col.id && dialogDragOverId !== col.id && "border-gray-200 dark:border-gray-600"
                  )}
                >
                  <div draggable
                    onDragStart={(e) => onDialogDragStart(e, col.id)}
                    onDragEnd={onDialogDragEnd}
                    className="cursor-grab active:cursor-grabbing p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"
                    title="Potiahnite pre zmenu poradia"
                  >
                    <GripVertical className="h-4 w-4" />
                  </div>
                  <button type="button" onClick={() => onVisibilityToggle(col.id)}
                    className={cn("p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700", col.visible ? "text-green-600 dark:text-green-400" : "text-gray-400 dark:text-gray-500")}
                    title={col.visible ? "Skryť stĺpec" : "Zobraziť stĺpec"}
                  >
                    {col.visible ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
                  </button>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <code className="text-xs px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-gray-600 dark:text-gray-400 font-mono truncate">{col.id}</code>
                    </div>
                    <ColumnHeaderInput
                      value={col.customHeader ?? col.originalHeader}
                      placeholder={col.originalHeader}
                      onChange={(value) => onHeaderChange(col.id, value)}
                    />
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <span className="text-xs text-gray-400 dark:text-gray-500">Šírka</span>
                    <ColumnWidthInput value={getColumnWidth(col.id)} onChange={(width) => onWidthChange(col.id, width)} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Footer */}
          <div className="flex justify-between px-6 py-4 border-t border-gray-200 dark:border-gray-700 shrink-0">
            <button type="button" onClick={onResetConfig}
              className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              <RotateCcw className="h-4 w-4" /> Obnoviť pôvodné
            </button>
            <div className="flex gap-2">
              <button type="button" onClick={onClose}
                className="px-4 py-2 rounded-lg text-sm font-medium border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              >
                Zrušiť
              </button>
              <button type="button" onClick={onSaveConfig}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-blue-600 text-white hover:bg-blue-700 transition-colors"
              >
                Uložiť
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

// === COLUMN CONFIG ITEM ===
interface ColumnConfigItem {
  id: string;
  originalHeader: string;
  customHeader?: string;
  visible: boolean;
  order: number;
  width?: number;
}

// === INPUT HELPERS ===
function ColumnHeaderInput({ value, placeholder, onChange }: { value: string; placeholder: string; onChange: (value: string) => void }) {
  const [localValue, setLocalValue] = useState(value);
  useEffect(() => { setLocalValue(value); }, [value]);
  return (
    <input type="text" value={localValue} onChange={(e) => setLocalValue(e.target.value)} onBlur={() => onChange(localValue)} placeholder={placeholder}
      className="w-full px-2 py-1 h-8 text-sm border rounded border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
  );
}

function ColumnWidthInput({ value, onChange }: { value: number; onChange: (value: number) => void }) {
  const [localValue, setLocalValue] = useState(String(value));
  useEffect(() => { setLocalValue(String(value)); }, [value]);
  const handleBlur = () => {
    const num = parseInt(localValue, 10);
    if (isNaN(num) || num < 30) setLocalValue(String(value));
    else onChange(Math.min(Math.max(num, 30), 800));
  };
  const handleKeyDown = (e: React.KeyboardEvent) => { if (e.key === 'Enter') { handleBlur(); (e.target as HTMLInputElement).blur(); } };
  return (
    <div className="flex items-center gap-1">
      <input type="text" inputMode="numeric" pattern="[0-9]*" value={localValue}
        onChange={(e) => setLocalValue(e.target.value.replace(/[^0-9]/g, ''))}
        onBlur={handleBlur} onKeyDown={handleKeyDown}
        className="w-14 px-2 py-1 h-7 text-xs text-center border rounded border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
      <span className="text-xs text-gray-400 dark:text-gray-500">px</span>
    </div>
  );
}

// === EDITABLE CELL COMPONENT ===
interface EditableCellProps {
  value: any;
  rowId: string | number;
  columnId: string;
  onSave: (rowId: string | number, columnId: string, value: any) => void;
  type?: 'text' | 'number';
  formatDisplay?: (value: any) => string;
}

function EditableCell({ value, rowId, columnId, onSave, type = 'number', formatDisplay }: EditableCellProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [isEditing]);

  const startEdit = () => {
    setEditValue(value != null ? String(value) : '');
    setIsEditing(true);
  };

  const cancelEdit = () => {
    setIsEditing(false);
    setEditValue('');
  };

  const saveEdit = () => {
    if (!isEditing) return;
    let newValue: any = editValue;
    if (type === 'number') {
      const parsed = parseFloat(editValue.replace(',', '.'));
      newValue = isNaN(parsed) ? value : parsed;
    }
    if (newValue !== value) {
      onSave(rowId, columnId, newValue);
    }
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') { e.preventDefault(); saveEdit(); }
    else if (e.key === 'Escape') { e.preventDefault(); cancelEdit(); }
    e.stopPropagation();
  };

  if (isEditing) {
    return (
      <input
        ref={inputRef}
        type="text"
        value={editValue}
        onChange={(e) => setEditValue(e.target.value)}
        onBlur={saveEdit}
        onKeyDown={handleKeyDown}
        className="w-full px-1 py-0 text-xs border border-blue-500 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-blue-500 text-right"
      />
    );
  }

  const displayValue = formatDisplay ? formatDisplay(value) : (value != null ? String(value) : '-');

  return (
    <div
      onDoubleClick={startEdit}
      className="text-right cursor-pointer hover:bg-blue-50 dark:hover:bg-blue-900/30 px-1 py-0.5 rounded -mx-1 -my-0.5"
      title="Double-click to edit"
    >
      {displayValue}
    </div>
  );
}

// === PAGINATION BAR (server-side mode) ===
interface PaginationBarProps {
  currentPage: number;
  totalRows: number;
  pageSize: number;
  onPageChange: (page: number) => void;
  onPageSizeChange: (size: number) => void;
}

function PaginationBar({ currentPage, totalRows, pageSize, onPageChange, onPageSizeChange }: PaginationBarProps) {
  const totalPages = Math.max(1, Math.ceil(totalRows / pageSize));
  const from = totalRows === 0 ? 0 : (currentPage - 1) * pageSize + 1;
  const to = Math.min(currentPage * pageSize, totalRows);

  return (
    <div className="px-3 py-1.5 bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between text-xs">
      <span className="text-gray-600 dark:text-gray-400">
        Zobrazených {from}–{to} z {totalRows} celkom
      </span>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1">
          <span className="text-gray-500 dark:text-gray-400">Na stránku:</span>
          <select
            value={pageSize}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
            className="px-1 py-0.5 text-xs border rounded border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none"
          >
            {[25, 50, 100, 200].map(s => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage <= 1}
            className="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-30 text-gray-600 dark:text-gray-400"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <span className="text-gray-700 dark:text-gray-300 min-w-[80px] text-center">
            Strana {currentPage} z {totalPages}
          </span>
          <button
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage >= totalPages}
            className="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-600 disabled:opacity-30 text-gray-600 dark:text-gray-400"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

// === DATAGRID PROPS ===
interface DataGridProps<T> {
  data: T[];
  columns: ColumnDef<T, any>[];
  onRowClick?: (row: T) => void;
  onRowDoubleClick?: (row: T) => void;
  rowHeight?: number;
  className?: string;
  storageKey?: string;
  editableColumns?: string[];
  onCellEdit?: (rowId: string | number, columnId: string, newValue: any) => void;

  // Server-side pagination (optional)
  serverSide?: boolean;
  totalRows?: number;
  currentPage?: number;
  pageSize?: number;
  onPageChange?: (page: number) => void;
  onPageSizeChange?: (size: number) => void;
  onSortChange?: (sortBy: string, sortOrder: 'asc' | 'desc') => void;
  onFilterChange?: (filters: Record<string, string>) => void;
}

export function DataGrid<T extends { id: number | string }>({
  data,
  columns,
  onRowClick,
  onRowDoubleClick,
  rowHeight = 32,
  className,
  storageKey,
  editableColumns = [],
  onCellEdit,
  // Server-side props
  serverSide = false,
  totalRows: externalTotalRows,
  currentPage: externalCurrentPage = 1,
  pageSize: externalPageSize = 50,
  onPageChange,
  onPageSizeChange,
  onSortChange,
  onFilterChange,
}: DataGridProps<T>) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [selectedRowId, setSelectedRowId] = useState<string | number | null>(null);
  const [focusedFilterIndex, setFocusedFilterIndex] = useState<number>(0);
  const [configOpen, setConfigOpen] = useState(false);
  const [draggedColumnId, setDraggedColumnId] = useState<string | null>(null);
  const [dragOverColumnId, setDragOverColumnId] = useState<string | null>(null);
  const [dialogDraggedId, setDialogDraggedId] = useState<string | null>(null);
  const [dialogDragOverId, setDialogDragOverId] = useState<string | null>(null);
  const [isResizing, setIsResizing] = useState(false);

  const tableContainerRef = useRef<HTMLDivElement>(null);
  const filterInputRefs = useRef<(HTMLInputElement | null)[]>([]);

  // Server-side: debounced filter callback
  const filterDebounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const columnsMeta = useMemo(() =>
    columns.map(col => ({
      id: (col as any).id || (col as any).accessorKey || '',
      header: typeof (col as any).header === 'string' ? (col as any).header : '',
      defaultWidth: (col as any).size || 150,
    })).filter(c => c.id),
    [columns]
  );

  const [columnConfig, setColumnConfig] = useState<ColumnConfigItem[]>(() => {
    if (storageKey) {
      try {
        const saved = localStorage.getItem(storageKey);
        if (saved) {
          const parsed = JSON.parse(saved);
          return columnsMeta.map((col, index) => {
            const existing = parsed.find((p: ColumnConfigItem) => p.id === col.id);
            if (existing) return { ...existing, originalHeader: col.header };
            return { id: col.id, originalHeader: col.header, customHeader: undefined, visible: true, order: parsed.length + index, width: undefined };
          }).sort((a: ColumnConfigItem, b: ColumnConfigItem) => a.order - b.order);
        }
      } catch (_e) { /* ignore */ }
    }
    return columnsMeta.map((col, index) => ({ id: col.id, originalHeader: col.header, customHeader: undefined, visible: true, order: index, width: undefined }));
  });

  useEffect(() => {
    setColumnConfig(prev => {
      const newConfig = columnsMeta.map((col, index) => {
        const existing = prev.find(p => p.id === col.id);
        if (existing) return { ...existing, originalHeader: col.header };
        return { id: col.id, originalHeader: col.header, customHeader: undefined, visible: true, order: prev.length + index, width: undefined };
      });
      return newConfig.sort((a, b) => a.order - b.order);
    });
  }, [columnsMeta]);

  const columnVisibility = useMemo(() => {
    const vis: VisibilityState = {};
    columnConfig.forEach(col => { vis[col.id] = col.visible; });
    return vis;
  }, [columnConfig]);

  const columnOrder = useMemo(() => [...columnConfig].sort((a, b) => a.order - b.order).map(c => c.id), [columnConfig]);

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

  const handleColumnOrderChange = useCallback((updater: ColumnOrderState | ((old: ColumnOrderState) => ColumnOrderState)) => {
    const resolveOrder = (current: ColumnOrderState) => typeof updater === 'function' ? updater(current) : updater;
    setColumnConfig(prev => {
      const currentOrder = [...prev].sort((a, b) => a.order - b.order).map(c => c.id);
      const newOrder = resolveOrder(currentOrder);
      return prev.map(col => ({ ...col, order: newOrder.indexOf(col.id) })).sort((a, b) => a.order - b.order);
    });
  }, []);

  const handleColumnSizingChange = useCallback((updater: any) => {
    const newSizing = typeof updater === 'function' ? updater(columnSizing) : updater;
    setColumnConfig(prev => prev.map(col => ({ ...col, width: newSizing[col.id] ?? col.width })));
  }, [columnSizing]);

  // Server-side: handle sorting changes
  const handleSortingChange = useCallback((updater: any) => {
    const newSorting = typeof updater === 'function' ? updater(sorting) : updater;
    setSorting(newSorting);
    if (serverSide && onSortChange && newSorting.length > 0) {
      onSortChange(newSorting[0].id, newSorting[0].desc ? 'desc' : 'asc');
    }
  }, [sorting, serverSide, onSortChange]);

  // Server-side: handle filter changes
  const handleColumnFiltersChange = useCallback((updater: any) => {
    const newFilters = typeof updater === 'function' ? updater(columnFilters) : updater;
    setColumnFilters(newFilters);
    if (serverSide && onFilterChange) {
      if (filterDebounceRef.current) clearTimeout(filterDebounceRef.current);
      filterDebounceRef.current = setTimeout(() => {
        const filtersObj: Record<string, string> = {};
        newFilters.forEach((f: { id: string; value: unknown }) => {
          if (f.value) filtersObj[f.id] = String(f.value);
        });
        onFilterChange(filtersObj);
      }, 300);
    }
  }, [columnFilters, serverSide, onFilterChange]);

  const table = useReactTable({
    data,
    columns: columnsWithCustomHeaders,
    state: { sorting, columnFilters, columnVisibility, columnOrder, columnSizing },
    onSortingChange: handleSortingChange,
    onColumnFiltersChange: serverSide ? handleColumnFiltersChange : setColumnFilters,
    onColumnOrderChange: handleColumnOrderChange,
    onColumnSizingChange: handleColumnSizingChange,
    getCoreRowModel: getCoreRowModel(),
    // Client-side only: enable filter and sort models
    ...(serverSide ? {} : {
      getFilteredRowModel: getFilteredRowModel(),
      getSortedRowModel: getSortedRowModel(),
    }),
    columnResizeMode: 'onChange',
    enableColumnResizing: true,
  });

  const { rows } = table.getRowModel();
  const rowVirtualizer = useVirtualizer({ count: rows.length, getScrollElement: () => tableContainerRef.current, estimateSize: () => rowHeight, overscan: 10 });
  const virtualRows = rowVirtualizer.getVirtualItems();
  const totalSize = rowVirtualizer.getTotalSize();
  const activeFiltersCount = columnFilters.filter(f => f.value).length;

  const clearAllFilters = () => {
    setColumnFilters([]);
    if (serverSide && onFilterChange) onFilterChange({});
    filterInputRefs.current[0]?.focus();
  };

  // === Header DnD ===
  const handleHeaderDragStart = (e: React.DragEvent, columnId: string) => { setDraggedColumnId(columnId); e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', columnId); };
  const handleHeaderDragEnd = () => { setDraggedColumnId(null); setDragOverColumnId(null); };
  const handleHeaderDragOver = (e: React.DragEvent, columnId: string) => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; if (columnId !== draggedColumnId) setDragOverColumnId(columnId); };
  const handleHeaderDragLeave = () => { setDragOverColumnId(null); };
  const handleHeaderDrop = (e: React.DragEvent, targetColumnId: string) => {
    e.preventDefault();
    if (!draggedColumnId || draggedColumnId === targetColumnId) { setDraggedColumnId(null); setDragOverColumnId(null); return; }
    const currentOrder = [...columnOrder];
    const draggedIndex = currentOrder.indexOf(draggedColumnId);
    const targetIndex = currentOrder.indexOf(targetColumnId);
    if (draggedIndex < 0 || targetIndex < 0) return;
    currentOrder.splice(draggedIndex, 1);
    currentOrder.splice(targetIndex, 0, draggedColumnId);
    handleColumnOrderChange(currentOrder);
    setDraggedColumnId(null); setDragOverColumnId(null);
  };

  // === Dialog DnD ===
  const handleDialogDragStart = (e: React.DragEvent, colId: string) => { setDialogDraggedId(colId); e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', colId); };
  const handleDialogDragEnd = () => { setDialogDraggedId(null); setDialogDragOverId(null); };
  const handleDialogDragOver = (e: React.DragEvent, colId: string) => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; if (colId !== dialogDraggedId) setDialogDragOverId(colId); };
  const handleDialogDragLeave = () => { setDialogDragOverId(null); };
  const handleDialogDrop = (e: React.DragEvent, targetId: string) => {
    e.preventDefault();
    if (!dialogDraggedId || dialogDraggedId === targetId) { setDialogDraggedId(null); setDialogDragOverId(null); return; }
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
    setDialogDraggedId(null); setDialogDragOverId(null);
  };

  // === Config actions ===
  const handleVisibilityToggle = useCallback((id: string) => { setColumnConfig(prev => prev.map(col => col.id === id ? { ...col, visible: !col.visible } : col)); }, []);
  const handleHeaderChange = useCallback((id: string, customHeader: string) => { setColumnConfig(prev => prev.map(col => col.id === id ? { ...col, customHeader: customHeader || undefined } : col)); }, []);
  const handleWidthChange = useCallback((id: string, width: number) => { setColumnConfig(prev => prev.map(col => col.id === id ? { ...col, width } : col)); }, []);
  const handleResetConfig = useCallback(() => {
    const defaultConfig = columnsMeta.map((col, index) => ({ id: col.id, originalHeader: col.header, customHeader: undefined, visible: true, order: index, width: undefined }));
    setColumnConfig(defaultConfig);
    if (storageKey) localStorage.removeItem(storageKey);
  }, [columnsMeta, storageKey]);
  const handleSaveConfig = useCallback(() => { if (storageKey) localStorage.setItem(storageKey, JSON.stringify(columnConfig)); setConfigOpen(false); }, [storageKey, columnConfig]);

  useEffect(() => { if (storageKey && !configOpen) localStorage.setItem(storageKey, JSON.stringify(columnConfig)); }, [columnConfig, storageKey, configOpen]);

  useEffect(() => {
    const handleGlobalMouseUp = () => { if (isResizing) { setIsResizing(false); document.body.style.cursor = ''; document.body.style.userSelect = ''; } };
    document.addEventListener('mouseup', handleGlobalMouseUp);
    return () => document.removeEventListener('mouseup', handleGlobalMouseUp);
  }, [isResizing]);

  // === Keyboard navigation ===
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (configOpen) return;
      const isInFilterInput = filterInputRefs.current.some(ref => ref === document.activeElement);
      const isEditingCell = document.activeElement?.closest('[data-editing-cell]');
      if (isEditingCell) return;

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
          if (currentCol?.getFilterValue()) currentCol.setFilterValue('');
          else (document.activeElement as HTMLElement)?.blur();
        } else setSelectedRowId(null);
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
        if (e.key === 'ArrowDown') { e.preventDefault(); const next = currentIndex < rows.length - 1 ? currentIndex + 1 : 0; setSelectedRowId(rows[next]?.original.id ?? null); rowVirtualizer.scrollToIndex(next, { align: 'auto' }); }
        if (e.key === 'ArrowUp') { e.preventDefault(); const prev = currentIndex > 0 ? currentIndex - 1 : rows.length - 1; setSelectedRowId(rows[prev]?.original.id ?? null); rowVirtualizer.scrollToIndex(prev, { align: 'auto' }); }
        if (e.key === 'Enter' && selectedRowId != null) { const row = rows.find(r => r.original.id === selectedRowId); if (row) onRowDoubleClick?.(row.original); }
        if (e.key.length === 1 && !e.ctrlKey && !e.altKey && !e.metaKey) { setFocusedFilterIndex(0); filterInputRefs.current[0]?.focus(); }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [rows, selectedRowId, focusedFilterIndex, table, onRowDoubleClick, rowVirtualizer, configOpen]);

  useEffect(() => { if (rows.length > 0 && (selectedRowId == null || !rows.find(r => r.original.id === selectedRowId))) setSelectedRowId(rows[0]?.original.id ?? null); }, [rows, selectedRowId]);
  useEffect(() => { filterInputRefs.current[0]?.focus(); }, []);

  const sortedConfig = useMemo(() => [...columnConfig].sort((a, b) => a.order - b.order), [columnConfig]);
  const getColumnWidth = (colId: string) => { const cfg = columnConfig.find(c => c.id === colId); const defaultWidth = columnsMeta.find(c => c.id === colId)?.defaultWidth || 150; return cfg?.width ?? defaultWidth; };

  const renderCell = (cell: any, row: any) => {
    const columnId = cell.column.id;
    const isEditable = editableColumns.includes(columnId) && onCellEdit;

    if (isEditable) {
      const value = cell.getValue();
      const colDef = cell.column.columnDef;
      const formatFn = colDef.meta?.formatDisplay;

      return (
        <div data-editing-cell>
          <EditableCell
            value={value}
            rowId={row.original.id}
            columnId={columnId}
            onSave={onCellEdit!}
            type="number"
            formatDisplay={formatFn}
          />
        </div>
      );
    }

    return flexRender(cell.column.columnDef.cell, cell.getContext());
  };

  // Status bar info
  const displayedCount = rows.length;
  const totalCount = serverSide ? (externalTotalRows ?? data.length) : data.length;

  return (
    <div className={cn('flex flex-col border rounded-lg bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700 overflow-hidden max-w-full', className)}>
      {/* Status bar top */}
      <div className="px-3 py-1 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between text-xs">
        <span className="text-gray-600 dark:text-gray-400">
          {serverSide
            ? `${totalCount} záznamov`
            : `${displayedCount} z ${totalCount} záznamov`
          }
          {activeFiltersCount > 0 && <span className="ml-2 text-blue-600 dark:text-blue-400">• {activeFiltersCount} {activeFiltersCount === 1 ? 'filter' : 'filtre'} aktívne</span>}
        </span>
        <div className="flex items-center gap-2">
          {activeFiltersCount > 0 && (
            <button onClick={clearAllFilters} className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 flex items-center gap-1">
              <X className="h-3 w-3" /> Zrušiť filtre
            </button>
          )}
          <button onClick={() => setConfigOpen(true)}
            className="p-1.5 rounded hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
            title="Nastavenie stĺpcov"
          >
            <Settings2 className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Column Config Dialog */}
      <ColumnConfigDialog
        open={configOpen}
        onClose={() => setConfigOpen(false)}
        sortedConfig={sortedConfig}
        columnsMeta={columnsMeta}
        getColumnWidth={getColumnWidth}
        onVisibilityToggle={handleVisibilityToggle}
        onHeaderChange={handleHeaderChange}
        onWidthChange={handleWidthChange}
        onResetConfig={handleResetConfig}
        onSaveConfig={handleSaveConfig}
        onDialogDragStart={handleDialogDragStart}
        onDialogDragEnd={handleDialogDragEnd}
        onDialogDragOver={handleDialogDragOver}
        onDialogDragLeave={handleDialogDragLeave}
        onDialogDrop={handleDialogDrop}
        dialogDraggedId={dialogDraggedId}
        dialogDragOverId={dialogDragOverId}
      />

      {/* Table */}
      <div ref={tableContainerRef} className="overflow-auto flex-1 min-h-0">
        <table className="w-full border-collapse" style={{ width: table.getTotalSize() }}>
          <thead className="sticky top-0 z-10">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id} className="bg-gray-100 dark:bg-gray-800">
                {headerGroup.headers.map((header) => (
                  <th key={header.id} draggable={!isResizing}
                    onDragStart={(e) => { if (!isResizing) handleHeaderDragStart(e, header.column.id); }}
                    onDragEnd={handleHeaderDragEnd}
                    onDragOver={(e) => { if (!isResizing) handleHeaderDragOver(e, header.column.id); }}
                    onDragLeave={handleHeaderDragLeave}
                    onDrop={(e) => { if (!isResizing) handleHeaderDrop(e, header.column.id); }}
                    className={cn(
                      "px-2 py-1 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-700 select-none relative group",
                      !isResizing && "hover:bg-gray-200 dark:hover:bg-gray-700 cursor-grab active:cursor-grabbing",
                      isResizing && "cursor-col-resize",
                      !isResizing && dragOverColumnId === header.column.id && "bg-blue-100 dark:bg-blue-900/40 border-l-2 border-l-blue-500",
                      draggedColumnId === header.column.id && "opacity-50"
                    )}
                    style={{ width: header.getSize() }}
                  >
                    <div className="flex items-center gap-1 cursor-pointer" onClick={header.column.getToggleSortingHandler()}>
                      {flexRender(header.column.columnDef.header, header.getContext())}
                      {header.column.getCanSort() && (
                        <span className="text-gray-400 dark:text-gray-500">
                          {header.column.getIsSorted() === 'asc' ? <ArrowUp className="h-3 w-3" /> : header.column.getIsSorted() === 'desc' ? <ArrowDown className="h-3 w-3" /> : <ArrowUpDown className="h-3 w-3" />}
                        </span>
                      )}
                    </div>
                    <div
                      onMouseDown={(e) => { e.stopPropagation(); setIsResizing(true); document.body.style.cursor = 'col-resize'; document.body.style.userSelect = 'none'; header.getResizeHandler()(e); }}
                      onTouchStart={header.getResizeHandler()}
                      onClick={(e) => e.stopPropagation()}
                      className={cn("absolute right-0 top-0 h-full w-1 cursor-col-resize select-none touch-none", "hover:bg-blue-500 active:bg-blue-600", header.column.getIsResizing() && "bg-blue-500")}
                    />
                  </th>
                ))}
              </tr>
            ))}
            {/* Filter row */}
            <tr className="bg-gray-50 dark:bg-gray-800/80 border-b-2 border-gray-200 dark:border-gray-700">
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
                        <input
                          ref={(el) => { if (filterIndex >= 0) filterInputRefs.current[filterIndex] = el; }}
                          type="text"
                          value={filterValue}
                          onChange={(e) => {
                            if (serverSide) {
                              handleColumnFiltersChange((prev: ColumnFiltersState) => {
                                const existing = prev.filter(f => f.id !== column.id);
                                return e.target.value ? [...existing, { id: column.id, value: e.target.value }] : existing;
                              });
                            } else {
                              column.setFilterValue(e.target.value);
                            }
                          }}
                          onFocus={() => setFocusedFilterIndex(filterIndex)}
                          placeholder="..."
                          className={cn(
                            "w-full px-1 py-0.5 text-xs border rounded text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500",
                            "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                            filterValue
                              ? "bg-yellow-50 dark:bg-yellow-900/30 border-yellow-400 dark:border-yellow-600"
                              : "bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600"
                          )}
                        />
                        {filterValue && (
                          <button
                            onClick={() => {
                              if (serverSide) {
                                handleColumnFiltersChange((prev: ColumnFiltersState) => prev.filter(f => f.id !== column.id));
                              } else {
                                column.setFilterValue('');
                              }
                            }}
                            className="absolute right-1 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"
                          >
                            <X className="h-3 w-3" />
                          </button>
                        )}
                      </div>
                    ) : <div className="h-5" />}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody>
            {virtualRows.length > 0 && virtualRows[0].start > 0 && <tr><td colSpan={columns.length} style={{ height: virtualRows[0].start }} /></tr>}
            {virtualRows.map((virtualRow) => {
              const row = rows[virtualRow.index];
              const isSelected = row.original.id === selectedRowId;
              return (
                <tr key={row.id} data-index={virtualRow.index}
                  className={cn(
                    'border-b border-gray-100 dark:border-gray-800 transition-colors cursor-pointer',
                    isSelected
                      ? 'bg-blue-100 dark:bg-blue-900/30 hover:bg-blue-150 dark:hover:bg-blue-900/40'
                      : virtualRow.index % 2 === 0
                        ? 'bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800'
                        : 'bg-gray-50/50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-700/50'
                  )}
                  style={{ height: rowHeight }}
                  onClick={() => { setSelectedRowId(row.original.id); onRowClick?.(row.original); }}
                  onDoubleClick={() => onRowDoubleClick?.(row.original)}
                >
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-2 py-0.5 text-xs text-gray-700 dark:text-gray-300" style={{ width: cell.column.getSize() }}>
                      {renderCell(cell, row)}
                    </td>
                  ))}
                </tr>
              );
            })}
            {virtualRows.length > 0 && <tr><td colSpan={columns.length} style={{ height: totalSize - (virtualRows[virtualRows.length - 1]?.end ?? 0) }} /></tr>}
          </tbody>
        </table>
        {rows.length === 0 && (
          <div className="flex items-center justify-center py-12 text-gray-500 dark:text-gray-400">
            {activeFiltersCount > 0 ? 'Žiadne výsledky pre zadané filtre' : 'Žiadne záznamy'}
          </div>
        )}
      </div>

      {/* Server-side pagination bar */}
      {serverSide && onPageChange && onPageSizeChange && (
        <PaginationBar
          currentPage={externalCurrentPage}
          totalRows={externalTotalRows ?? data.length}
          pageSize={externalPageSize}
          onPageChange={onPageChange}
          onPageSizeChange={onPageSizeChange}
        />
      )}

      {/* Client-side keyboard hints bar */}
      {!serverSide && (
        <div className="px-3 py-0.5 bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400 flex gap-4">
          <span><kbd className="px-1 bg-gray-200 dark:bg-gray-700 rounded">Tab</kbd> ďalší filter</span>
          <span><kbd className="px-1 bg-gray-200 dark:bg-gray-700 rounded">Enter</kbd> do tabuľky</span>
          <span><kbd className="px-1 bg-gray-200 dark:bg-gray-700 rounded">↑↓</kbd> navigácia</span>
          <span><kbd className="px-1 bg-gray-200 dark:bg-gray-700 rounded">Esc</kbd> zrušiť</span>
        </div>
      )}
    </div>
  );
}
