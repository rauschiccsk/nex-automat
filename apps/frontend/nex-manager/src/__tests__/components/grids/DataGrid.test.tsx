import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { createColumnHelper } from '@tanstack/react-table'

// Mock useVirtualizer — jsdom has no real layout, so virtualizer returns 0 items
// We override it to return all rows as virtual items.
vi.mock('@tanstack/react-virtual', () => ({
  useVirtualizer: ({ count }: { count: number }) => ({
    getVirtualItems: () =>
      Array.from({ length: count }, (_, i) => ({
        index: i,
        start: i * 32,
        end: (i + 1) * 32,
        size: 32,
        key: String(i),
        measureElement: vi.fn(),
      })),
    getTotalSize: () => count * 32,
    scrollToIndex: vi.fn(),
  }),
}))

import { DataGrid } from '@renderer/components/grids/DataGrid'

// --- Test data ---

interface TestRow {
  id: number
  name: string
  city: string
  amount: number
}

const testData: TestRow[] = [
  { id: 1, name: 'HOFFER SK s.r.o.', city: 'Komárno', amount: 1000 },
  { id: 2, name: 'Continental Barum', city: 'Otrokovice', amount: 2500 },
  { id: 3, name: 'Ján Kováč', city: 'Košice', amount: 500 },
  { id: 4, name: 'Pirelli Slovakia', city: 'Bratislava', amount: 3000 },
  { id: 5, name: 'Bridgestone CE', city: 'Tatabánya', amount: 1800 },
]

const columnHelper = createColumnHelper<TestRow>()

const testColumns = [
  columnHelper.accessor('id', { header: 'ID', size: 60 }),
  columnHelper.accessor('name', { header: 'Názov', size: 200 }),
  columnHelper.accessor('city', { header: 'Mesto', size: 150 }),
  columnHelper.accessor('amount', { header: 'Suma', size: 100 }),
]

/** DataGrid auto-focuses the first filter input on mount.
 *  Keyboard navigation only works when focus is NOT in a filter input,
 *  so we must blur first before simulating arrow/end/home keys. */
function blurFilters(): void {
  const active = document.activeElement as HTMLElement | null
  if (active && active.tagName === 'INPUT') active.blur()
}

describe('DataGrid', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('renders rows for provided data', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    expect(screen.getByText('HOFFER SK s.r.o.')).toBeInTheDocument()
    expect(screen.getByText('Continental Barum')).toBeInTheDocument()
    expect(screen.getByText('Ján Kováč')).toBeInTheDocument()
  })

  it('renders column headers', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    expect(screen.getByText('ID')).toBeInTheDocument()
    expect(screen.getByText('Názov')).toBeInTheDocument()
    expect(screen.getByText('Mesto')).toBeInTheDocument()
    expect(screen.getByText('Suma')).toBeInTheDocument()
  })

  it('shows empty state when data is empty', () => {
    render(<DataGrid data={[]} columns={testColumns} />)
    expect(screen.getByText('Žiadne záznamy')).toBeInTheDocument()
  })

  it('displays record count in status bar', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    expect(screen.getByText(/5 z 5 záznamov/)).toBeInTheDocument()
  })

  it('selects first row by default', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    const firstRow = screen.getByText('HOFFER SK s.r.o.').closest('tr')!
    expect(firstRow.className).toContain('bg-blue-100')
  })

  it('selects row on click', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    const row3 = screen.getByText('Ján Kováč').closest('tr')!
    fireEvent.click(row3)
    expect(row3.className).toContain('bg-blue-100')
  })

  it('calls onRowClick when row is clicked', () => {
    const onRowClick = vi.fn()
    render(<DataGrid data={testData} columns={testColumns} onRowClick={onRowClick} />)
    const row = screen.getByText('Continental Barum').closest('tr')!
    fireEvent.click(row)
    expect(onRowClick).toHaveBeenCalledWith(
      expect.objectContaining({ id: 2, name: 'Continental Barum' })
    )
  })

  it('calls onRowDoubleClick when row is double-clicked', () => {
    const onDoubleClick = vi.fn()
    render(
      <DataGrid data={testData} columns={testColumns} onRowDoubleClick={onDoubleClick} />
    )
    const row = screen.getByText('Pirelli Slovakia').closest('tr')!
    fireEvent.doubleClick(row)
    expect(onDoubleClick).toHaveBeenCalledWith(expect.objectContaining({ id: 4 }))
  })

  it('navigates down with ArrowDown key', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    blurFilters()
    fireEvent.keyDown(window, { key: 'ArrowDown' })
    const row2 = screen.getByText('Continental Barum').closest('tr')!
    expect(row2.className).toContain('bg-blue-100')
  })

  it('navigates up with ArrowUp key', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    blurFilters()
    fireEvent.keyDown(window, { key: 'ArrowDown' })
    fireEvent.keyDown(window, { key: 'ArrowUp' })
    const row1 = screen.getByText('HOFFER SK s.r.o.').closest('tr')!
    expect(row1.className).toContain('bg-blue-100')
  })

  it('jumps to last row with End key', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    blurFilters()
    fireEvent.keyDown(window, { key: 'End' })
    const lastRow = screen.getByText('Bridgestone CE').closest('tr')!
    expect(lastRow.className).toContain('bg-blue-100')
  })

  it('jumps to first row with Home key', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    blurFilters()
    fireEvent.keyDown(window, { key: 'End' })
    fireEvent.keyDown(window, { key: 'Home' })
    const firstRow = screen.getByText('HOFFER SK s.r.o.').closest('tr')!
    expect(firstRow.className).toContain('bg-blue-100')
  })

  it('does not go past first row on ArrowUp at boundary', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    blurFilters()
    fireEvent.keyDown(window, { key: 'ArrowUp' })
    const firstRow = screen.getByText('HOFFER SK s.r.o.').closest('tr')!
    expect(firstRow.className).toContain('bg-blue-100')
  })

  it('does not go past last row on ArrowDown at boundary', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    blurFilters()
    fireEvent.keyDown(window, { key: 'End' })
    fireEvent.keyDown(window, { key: 'ArrowDown' })
    const lastRow = screen.getByText('Bridgestone CE').closest('tr')!
    expect(lastRow.className).toContain('bg-blue-100')
  })

  it('activates row with Enter key (triggers onRowDoubleClick)', () => {
    const onDoubleClick = vi.fn()
    render(
      <DataGrid data={testData} columns={testColumns} onRowDoubleClick={onDoubleClick} />
    )
    blurFilters()
    fireEvent.keyDown(window, { key: 'Enter' })
    expect(onDoubleClick).toHaveBeenCalledWith(expect.objectContaining({ id: 1 }))
  })

  it('shows keyboard hint bar', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    expect(screen.getByText(/navigácia/)).toBeInTheDocument()
  })

  it('renders settings button for column config', () => {
    render(<DataGrid data={testData} columns={testColumns} />)
    expect(screen.getByTitle('Nastavenie stĺpcov')).toBeInTheDocument()
  })
})
