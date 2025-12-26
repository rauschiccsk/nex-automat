// Grid Types - shared types for BaseGrid system
import type { ColumnDef } from '@tanstack/react-table';

/**
 * Column type definitions
 */
export type GridColumnType = 
  | 'text'      // Default text
  | 'number'    // Number with decimals
  | 'integer'   // Integer without decimals
  | 'currency'  // Currency format (EUR)
  | 'percent'   // Percentage format
  | 'date'      // Date format
  | 'datetime'  // DateTime format
  | 'boolean'   // Checkbox/icon
  | 'enum'      // Select from options
  | 'custom';   // Custom renderer

/**
 * Extended column definition for BaseGrid
 */
export interface GridColumnConfig<T = any> {
  id: string;
  header: string;
  accessorKey?: keyof T;
  type?: GridColumnType;
  size?: number;
  minSize?: number;
  maxSize?: number;
  enableFilter?: boolean;
  enableSort?: boolean;
  editable?: boolean;
  align?: 'left' | 'center' | 'right';
  // For enum type
  enumOptions?: { value: string; label: string }[];
  // For custom type
  cell?: (value: any, row: T) => React.ReactNode;
  // CSS classes
  headerClass?: string;
  cellClass?: string;
}

/**
 * Grid configuration
 */
export interface GridConfig<T = any> {
  storageKeyPrefix: string;
  defaultRowHeight?: number;
  defaultPageSize?: number;
  enableExport?: boolean;
  enablePrint?: boolean;
  columns: GridColumnConfig<T>[];
}

/**
 * Cell edit event
 */
export interface CellEditEvent {
  rowId: string | number;
  columnId: string;
  oldValue: any;
  newValue: any;
}

/**
 * Grid export format
 */
export type ExportFormat = 'csv' | 'xlsx' | 'json';
