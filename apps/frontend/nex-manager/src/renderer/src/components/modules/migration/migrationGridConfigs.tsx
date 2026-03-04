// Grid configurations for Migration (MIG) module
import type { GridConfig } from '@renderer/components/grids'
import type { MigrationBatch, MigrationIdMapping } from '@renderer/types/migration'

// === Status badge colors ===

const STATUS_CLASSES: Record<string, string> = {
  completed: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
  failed: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
  running: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
  pending: 'bg-gray-100 text-gray-600 dark:bg-gray-700/50 dark:text-gray-400'
}

const STATUS_LABELS: Record<string, string> = {
  completed: 'Dokoncene',
  failed: 'Chyba',
  running: 'Prebieha',
  pending: 'Caka'
}

// === Batches grid ===

export const migrationBatchesGridConfig: GridConfig<MigrationBatch> = {
  storageKeyPrefix: 'mig-batches',
  defaultRowHeight: 28,
  columns: [
    {
      id: 'status',
      header: 'Stav',
      type: 'custom',
      size: 100,
      visible: true,
      cell: (value: string) => (
        <span
          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${STATUS_CLASSES[value] ?? STATUS_CLASSES.pending}`}
        >
          {STATUS_LABELS[value] ?? value}
        </span>
      )
    },
    { id: 'started_at', header: 'Spustene', type: 'datetime', size: 160, visible: true },
    { id: 'completed_at', header: 'Dokoncene', type: 'datetime', size: 160, visible: true },
    { id: 'source_count', header: 'Zdrojove', type: 'integer', size: 90, visible: true, align: 'right' },
    { id: 'target_count', header: 'Cielove', type: 'integer', size: 90, visible: true, align: 'right' },
    {
      id: 'error_count',
      header: 'Chyby',
      type: 'custom',
      size: 80,
      visible: true,
      align: 'right',
      cell: (value: number) => (
        <span className={`block text-right ${value > 0 ? 'text-red-600 dark:text-red-400 font-semibold' : ''}`}>
          {value ?? 0}
        </span>
      )
    },
    { id: 'skipped_count', header: 'Preskocene', type: 'integer', size: 90, visible: true, align: 'right' },
    {
      id: 'duration_seconds',
      header: 'Trvanie (s)',
      type: 'custom',
      size: 100,
      visible: true,
      align: 'right',
      cell: (value: number | null) => (
        <span className="block text-right">
          {value != null ? value.toFixed(1) : '-'}
        </span>
      )
    }
  ]
}

// === ID Mappings grid ===

export const migrationMappingsGridConfig: GridConfig<MigrationIdMapping> = {
  storageKeyPrefix: 'mig-mappings',
  defaultRowHeight: 28,
  columns: [
    { id: 'source_table', header: 'Zdrojova tabulka', type: 'text', size: 150, visible: true },
    {
      id: 'source_key',
      header: 'Zdrojovy kluc',
      type: 'custom',
      size: 180,
      visible: true,
      cell: (value: string) => (
        <span className="font-mono text-xs">{value}</span>
      )
    },
    { id: 'target_table', header: 'Cielova tabulka', type: 'text', size: 150, visible: true },
    {
      id: 'target_id',
      header: 'Cielove ID',
      type: 'custom',
      size: 180,
      visible: true,
      cell: (value: string) => (
        <span className="font-mono text-xs truncate block" title={value}>
          {value}
        </span>
      )
    },
    { id: 'migrated_at', header: 'Migrovane', type: 'datetime', size: 160, visible: true }
  ]
}
