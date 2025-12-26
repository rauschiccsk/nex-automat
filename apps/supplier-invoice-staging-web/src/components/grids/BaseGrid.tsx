// BaseGrid - Reusable grid component with common features
import { useMemo, useCallback } from 'react';
import { createColumnHelper, type ColumnDef } from '@tanstack/react-table';
import { DataGrid } from '@/components/ui/datagrid';
import { stringFilter, numericFilter, dateFilter, booleanFilter } from './gridFilters';
import { 
  formatCurrency, 
  formatPercent, 
  formatNumber, 
  formatInteger,
  formatDate, 
  formatDateTime, 
  formatBoolean 
} from './gridFormatters';
import type { GridColumnConfig, GridConfig } from './gridTypes';
import { cn } from '@/lib/utils';

// =============================================================================
// Helper to build TanStack columns from GridColumnConfig
// =============================================================================
function buildColumns<T extends { id: number | string }>(
  configs: GridColumnConfig<T>[]
): ColumnDef<T, any>[] {
  const columnHelper = createColumnHelper<T>();

  return configs.map((cfg) => {
    const accessorKey = cfg.accessorKey || cfg.id;

    // Determine filter function based on type
    const getFilterFn = () => {
      switch (cfg.type) {
        case 'number':
        case 'integer':
        case 'currency':
        case 'percent':
          return numericFilter;
        case 'date':
        case 'datetime':
          return dateFilter;
        case 'boolean':
          return booleanFilter;
        default:
          return stringFilter;
      }
    };

    // Determine cell renderer based on type
    const getCellRenderer = () => {
      const align = cfg.align || (
        ['number', 'integer', 'currency', 'percent'].includes(cfg.type || '') 
          ? 'right' 
          : 'left'
      );
      const alignClass = align === 'right' ? 'text-right' : align === 'center' ? 'text-center' : '';

      return (info: any) => {
        const value = info.getValue();

        // Custom renderer
        if (cfg.type === 'custom' && cfg.cell) {
          return cfg.cell(value, info.row.original);
        }

        let displayValue: React.ReactNode;

        switch (cfg.type) {
          case 'currency':
            displayValue = formatCurrency(value);
            break;
          case 'percent':
            displayValue = formatPercent(value);
            break;
          case 'number':
            displayValue = formatNumber(value);
            break;
          case 'integer':
            displayValue = formatInteger(value);
            break;
          case 'date':
            displayValue = formatDate(value);
            break;
          case 'datetime':
            displayValue = formatDateTime(value);
            break;
          case 'boolean':
            displayValue = (
              <span className={value ? 'text-green-600' : 'text-red-500'}>
                {formatBoolean(value)}
              </span>
            );
            break;
          default:
            displayValue = value ?? '-';
        }

        return (
          <span className={cn('block', alignClass, cfg.cellClass)}>
            {displayValue}
          </span>
        );
      };
    };

    return columnHelper.accessor(accessorKey as any, {
      id: cfg.id,
      header: cfg.header,
      size: cfg.size ?? 100,
      minSize: cfg.minSize ?? 50,
      maxSize: cfg.maxSize ?? 500,
      enableColumnFilter: cfg.enableFilter ?? true,
      enableSorting: cfg.enableSort ?? true,
      filterFn: getFilterFn(),
      cell: getCellRenderer(),
    });
  });
}

// =============================================================================
// BaseGrid Props
// =============================================================================
interface BaseGridProps<T extends { id: number | string }> {
  data: T[];
  config: GridConfig<T>;
  onRowClick?: (row: T) => void;
  onRowDoubleClick?: (row: T) => void;
  editableColumns?: string[];
  onCellEdit?: (rowId: string | number, columnId: string, newValue: any) => void;
  className?: string;
  rowHeight?: number;
}

// =============================================================================
// BaseGrid Component
// =============================================================================
export function BaseGrid<T extends { id: number | string }>({
  data,
  config,
  onRowClick,
  onRowDoubleClick,
  editableColumns,
  onCellEdit,
  className,
  rowHeight,
}: BaseGridProps<T>) {
  // Build columns from config
  const columns = useMemo(
    () => buildColumns(config.columns),
    [config.columns]
  );

  // Storage key
  const storageKey = `grid-${config.storageKeyPrefix}`;

  return (
    <DataGrid
      data={data}
      columns={columns}
      storageKey={storageKey}
      rowHeight={rowHeight ?? config.defaultRowHeight ?? 24}
      onRowClick={onRowClick}
      onRowDoubleClick={onRowDoubleClick}
      editableColumns={editableColumns}
      onCellEdit={onCellEdit}
      className={className}
    />
  );
}

// =============================================================================
// Export utilities
// =============================================================================
export function exportToCSV<T>(data: T[], columns: GridColumnConfig<T>[], filename: string) {
  const headers = columns.map(c => c.header).join(';');
  const rows = data.map(row => 
    columns.map(c => {
      const value = (row as any)[c.accessorKey || c.id];
      if (value == null) return '';
      if (typeof value === 'string' && value.includes(';')) {
        return `"${value}"`;
      }
      return String(value);
    }).join(';')
  );

  const csv = [headers, ...rows].join('\n');
  const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${filename}.csv`;
  link.click();
}

export function exportToJSON<T>(data: T[], filename: string) {
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${filename}.json`;
  link.click();
}
