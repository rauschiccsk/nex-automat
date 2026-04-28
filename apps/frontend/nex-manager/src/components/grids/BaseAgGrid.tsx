/**
 * BaseAgGrid — AG Grid Community wrapper with same GridConfig API as BaseGrid.
 *
 * Why AG Grid: native virtualization at the row-model level (not just rendering)
 * lets us hold 250k+ rows in browser memory and apply per-column quick-filter
 * + sort instantly — matches the NEX Genesis grid UX that customers expect.
 * BaseGrid (@tanstack/react-table) struggles past ~10k rows on remote browsers.
 *
 * Drop-in replacement for <BaseGrid>: same data + config + onRowDoubleClick.
 * Extras specific to AG Grid:
 *   - Floating filter row above each column (NEX Genesis-style quick-filter)
 *   - Built-in column header click → sort
 *   - localStorage persistence: column widths, order, visibility, sort, filters
 */

import { useCallback, useEffect, useMemo, useRef, useState, type ReactElement } from 'react'
import { AgGridReact } from 'ag-grid-react'
import type {
  ColDef,
  GridReadyEvent,
  ColumnState,
  FilterChangedEvent,
  SortChangedEvent,
  ColumnMovedEvent,
  ColumnResizedEvent,
  ColumnVisibleEvent,
} from 'ag-grid-community'
import {
  ModuleRegistry,
  AllCommunityModule,
  themeBalham,
  colorSchemeDark,
} from 'ag-grid-community'
import type { GridConfig, GridColumnConfig, GridColumnType } from './gridTypes'

// AG Grid Community v33+ requires explicit module registration
ModuleRegistry.registerModules([AllCommunityModule])

// ----------------------------------------------------------------------------
// Type → AG Grid colDef mapping
// ----------------------------------------------------------------------------

function colDefTypeProps(type: GridColumnType | undefined): Partial<ColDef> {
  switch (type) {
    case 'number':
    case 'integer':
    case 'currency':
    case 'percent':
      return { filter: 'agNumberColumnFilter', cellDataType: 'number' }
    case 'date':
    case 'datetime':
      return { filter: 'agDateColumnFilter', cellDataType: 'dateString' }
    case 'boolean':
      return {
        filter: 'agSetColumnFilter',
        cellDataType: 'boolean',
        cellRenderer: (params: { value: unknown }) =>
          params.value === true ? '✓' : params.value === false ? '✗' : '',
      }
    case 'text':
    default:
      return { filter: 'agTextColumnFilter', cellDataType: 'text' }
  }
}

function buildAgColumns<T extends object>(
  configCols: GridColumnConfig<T>[]
): ColDef<T>[] {
  // AG Grid's ColDefField<T> is a strict template-literal type that doesn't
  // accept arbitrary keyof T from a generic context. We rely on the runtime
  // contract — accessorKey IS a key of T per GridColumnConfig — and cast
  // the whole produced array.
  return configCols.map((c) => {
    const def = {
      colId: c.id,
      headerName: c.header,
      field: c.accessorKey,
      width: c.size,
      minWidth: c.minSize,
      maxWidth: c.maxSize,
      sortable: c.enableSort !== false,
      filter: true,
      floatingFilter: c.enableFilter !== false,
      hide: c.visible === false,
      editable: c.editable === true,
      cellClass: c.cellClass,
      headerClass: c.headerClass,
      ...colDefTypeProps(c.type),
    } as Record<string, unknown>
    if (c.cell) {
      def.cellRenderer = (params: { value: unknown; data: T | undefined }) =>
        params.data ? c.cell!(params.value, params.data) : null
    }
    return def as unknown as ColDef<T>
  })
}

// ----------------------------------------------------------------------------
// Persistence helpers
// ----------------------------------------------------------------------------

interface PersistedState {
  columnState: ColumnState[]
  filterModel: Record<string, unknown>
}

function persistKey(storageKeyPrefix: string): string {
  return `aggrid-${storageKeyPrefix}`
}

function loadPersistedState(key: string): PersistedState | null {
  try {
    const raw = localStorage.getItem(key)
    return raw ? (JSON.parse(raw) as PersistedState) : null
  } catch {
    return null
  }
}

function savePersistedState(key: string, state: PersistedState): void {
  try {
    localStorage.setItem(key, JSON.stringify(state))
  } catch {
    // Quota exceeded or storage unavailable — silently continue
  }
}

// ----------------------------------------------------------------------------
// Component
// ----------------------------------------------------------------------------

interface BaseAgGridProps<T extends { id: number | string }> {
  data: T[]
  config: GridConfig<T>
  onRowClick?: (row: T) => void
  onRowDoubleClick?: (row: T) => void
  className?: string
  rowHeight?: number
  // Localized text (defaults to Slovak)
  localeText?: Record<string, string>
}

const SK_LOCALE: Record<string, string> = {
  // Filters
  contains: 'Obsahuje',
  notContains: 'Neobsahuje',
  startsWith: 'Začína na',
  endsWith: 'Končí na',
  equals: 'Rovná sa',
  notEqual: 'Nerovná sa',
  blank: 'Prázdne',
  notBlank: 'Nie prázdne',
  greaterThan: 'Väčšie ako',
  lessThan: 'Menšie ako',
  inRange: 'V rozsahu',
  // Generic
  loadingOoo: 'Načítavam...',
  noRowsToShow: 'Žiadne záznamy',
  applyFilter: 'Použiť',
  resetFilter: 'Reset',
  clearFilter: 'Vymazať',
  // Pagination — disabled for our use case but locales kept
  page: 'Strana',
  to: 'do',
  of: 'z',
}

export function BaseAgGrid<T extends { id: number | string }>({
  data,
  config,
  onRowClick,
  onRowDoubleClick,
  className,
  rowHeight,
  localeText,
}: BaseAgGridProps<T>): ReactElement {
  const storageKey = persistKey(config.storageKeyPrefix)
  const gridRef = useRef<AgGridReact<T>>(null)

  const columnDefs = useMemo(() => buildAgColumns(config.columns), [config.columns])

  // Track app-level dark mode (Tailwind sets `dark` class on documentElement
  // via App.tsx). We pass the resolved AG Grid theme object as a prop so
  // the v35 JS Theming API rebuilds the grid styles correctly on toggle.
  const [isDark, setIsDark] = useState<boolean>(() =>
    typeof document !== 'undefined' &&
    document.documentElement.classList.contains('dark')
  )
  useEffect(() => {
    const root = document.documentElement
    setIsDark(root.classList.contains('dark'))
    const observer = new MutationObserver(() => {
      setIsDark(root.classList.contains('dark'))
    })
    observer.observe(root, { attributes: true, attributeFilter: ['class'] })
    return () => observer.disconnect()
  }, [])

  // Tailwind palette overrides for dark mode — match the app shell so the
  // grid blends in. Picked to align with:
  //   shell + sidebar:  dark:bg-gray-900   #111827
  //   header + tabbar:  dark:bg-gray-800   #1f2937
  //   row hover/active: dark:bg-gray-700   #374151
  //   borders:          dark:border-gray-700 / 600
  //   foreground text:  dark:text-white    #ffffff (gray-100 #f3f4f6 for body)
  // Light mode uses balham defaults which already match the white shell.
  const theme = useMemo(() => {
    if (!isDark) return themeBalham
    return themeBalham.withPart(colorSchemeDark).withParams({
      backgroundColor: '#111827', // gray-900 — main grid bg matches shell
      foregroundColor: '#f3f4f6', // gray-100 — body text
      headerBackgroundColor: '#1f2937', // gray-800 — match TabBar/Header
      headerTextColor: '#f3f4f6',
      borderColor: '#374151', // gray-700
      rowHoverColor: '#1f2937', // gray-800 — same as header (subtle hover)
      oddRowBackgroundColor: '#111827', // gray-900 — flat (no zebra to keep clean)
      selectedRowBackgroundColor: '#1e3a8a', // blue-900 — visible but on-theme
      chromeBackgroundColor: '#1f2937', // gray-800 — toolbar/filter chrome
    })
  }, [isDark])

  const defaultColDef = useMemo<ColDef>(
    () => ({
      resizable: true,
      sortable: true,
      filter: true,
      floatingFilter: true,
      suppressHeaderMenuButton: true, // hide hamburger — keep header tight
      // Floating filter default = 'startsWith' (NEX Genesis convention —
      // user types and grid shows rows whose value starts with the input).
      // 'contains' remains available via the dropdown next to the input
      // for cases where user needs substring search.
      filterParams: {
        defaultOption: 'startsWith',
        buttons: ['reset'],
      },
    }),
    []
  )

  const onGridReady = useCallback(
    (event: GridReadyEvent<T>) => {
      const persisted = loadPersistedState(storageKey)
      if (persisted) {
        if (persisted.columnState && event.api.applyColumnState) {
          event.api.applyColumnState({
            state: persisted.columnState,
            applyOrder: true,
          })
        }
        if (persisted.filterModel) {
          event.api.setFilterModel(persisted.filterModel)
        }
      }
    },
    [storageKey]
  )

  const persistNow = useCallback(() => {
    const api = gridRef.current?.api
    if (!api) return
    const columnState = api.getColumnState()
    const filterModel = api.getFilterModel()
    savePersistedState(storageKey, { columnState, filterModel })
  }, [storageKey])

  const onSortChanged = useCallback((_: SortChangedEvent<T>) => persistNow(), [persistNow])
  const onFilterChanged = useCallback(
    (_: FilterChangedEvent<T>) => persistNow(),
    [persistNow]
  )
  const onColumnMoved = useCallback((_: ColumnMovedEvent<T>) => persistNow(), [persistNow])
  const onColumnResized = useCallback(
    (e: ColumnResizedEvent<T>) => {
      // Only persist on user-finished resize (not while dragging)
      if (e.finished) persistNow()
    },
    [persistNow]
  )
  const onColumnVisible = useCallback(
    (_: ColumnVisibleEvent<T>) => persistNow(),
    [persistNow]
  )

  return (
    <div className={className ?? ''} style={{ height: '100%', width: '100%' }}>
      <AgGridReact<T>
        ref={gridRef}
        theme={theme}
        rowData={data}
        columnDefs={columnDefs}
        defaultColDef={defaultColDef}
        rowHeight={rowHeight ?? config.defaultRowHeight ?? 24}
        headerHeight={28}
        floatingFiltersHeight={28}
        animateRows={false}
        suppressCellFocus
        rowSelection={{ mode: 'singleRow' }}
        onRowClicked={(e) => {
          if (e.data && onRowClick) onRowClick(e.data)
        }}
        onRowDoubleClicked={(e) => {
          if (e.data && onRowDoubleClick) onRowDoubleClick(e.data)
        }}
        onGridReady={onGridReady}
        onSortChanged={onSortChanged}
        onFilterChanged={onFilterChanged}
        onColumnMoved={onColumnMoved}
        onColumnResized={onColumnResized}
        onColumnVisible={onColumnVisible}
        localeText={localeText ?? SK_LOCALE}
        getRowId={(params) => String((params.data as { id: number | string }).id)}
      />
    </div>
  )
}
