import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'

// --- Mock API with vi.hoisted ---
const mockApi = vi.hoisted(() => ({
  getMigrationCategories: vi.fn(),
  getMigrationStats: vi.fn(),
  getMigrationBatches: vi.fn(),
  getMigrationMappings: vi.fn(),
  runMigration: vi.fn(),
  resetMigrationCategory: vi.fn(),
}))

vi.mock('@renderer/lib/api', () => ({
  api: mockApi,
  ApiError: class ApiError extends Error {
    status: number
    detail?: string
    constructor(msg: string, status = 500) {
      super(msg)
      this.status = status
    }
  },
}))

// --- Mock stores ---
vi.mock('@renderer/stores/authStore', () => ({
  useAuthStore: () => ({
    checkPermission: vi.fn().mockReturnValue(true),
  }),
}))

const mockAddToast = vi.fn()
vi.mock('@renderer/stores/toastStore', () => ({
  useToastStore: () => ({
    addToast: mockAddToast,
  }),
}))

// --- Mock BaseGrid ---
vi.mock('@renderer/components/grids', () => ({
  BaseGrid: ({ data }: { data: unknown[] }) => (
    <div data-testid="base-grid">rows: {data.length}</div>
  ),
}))

import CategoryDetail from '@renderer/components/modules/migration/CategoryDetail'
import type { MigrationCategory } from '@renderer/types/migration'

// --- Factory ---
function createMockCategory(overrides: Partial<MigrationCategory> = {}): MigrationCategory {
  return {
    code: 'PAB',
    name: 'Obchodni partneri',
    description: 'Migracia partnerov z Btrieve do PostgreSQL',
    source_tables: ['PAB.DAT'],
    target_tables: ['partners'],
    dependency_codes: [],
    dependencies: [],
    level: 0,
    status: 'completed',
    record_count: 164,
    first_migrated_at: '2025-06-01T08:00:00Z',
    last_migrated_at: '2025-06-01T10:00:00Z',
    last_batch_id: 3,
    can_run: true,
    blocked_by: [],
    ...overrides,
  }
}

const mockCategory = createMockCategory()
const mockOnClose = vi.fn()
const mockOnRefresh = vi.fn()

beforeEach(() => {
  vi.clearAllMocks()
  localStorage.clear()
  mockApi.getMigrationBatches.mockResolvedValue({
    batches: [
      {
        id: 1,
        category: 'PAB',
        status: 'completed',
        source_count: 164,
        target_count: 164,
        error_count: 0,
        skipped_count: 0,
        started_at: '2025-06-01T10:00:00Z',
        completed_at: '2025-06-01T10:02:30Z',
        error_log: null,
        metadata: null,
        duration_seconds: 2.5,
      },
    ],
    total: 1,
  })
  mockApi.getMigrationMappings.mockResolvedValue({
    items: [
      {
        source_table: 'PAB.DAT',
        source_key: '1',
        target_table: 'partners',
        target_id: 'uuid-1',
        migrated_at: '2025-06-01T10:00:00Z',
      },
    ],
    total: 1,
    page: 1,
    page_size: 50,
    total_pages: 1,
  })
  mockApi.runMigration.mockResolvedValue({
    batch_id: 2,
    category: 'PAB',
    status: 'completed',
    source_count: 164,
    target_count: 164,
    error_count: 0,
    errors: [],
    warnings: [],
    duration_seconds: 2.5,
    message: 'Migracia dokoncena',
  })
  mockApi.resetMigrationCategory.mockResolvedValue({ message: 'Reset OK' })
})

describe('CategoryDetail', () => {
  it('renders category code and name in header', async () => {
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    expect(screen.getByText('PAB')).toBeInTheDocument()
    expect(screen.getByText('Obchodni partneri')).toBeInTheDocument()
  })

  it('renders 4 tab buttons', async () => {
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    expect(screen.getByText('Info')).toBeInTheDocument()
    expect(screen.getByText('Batche')).toBeInTheDocument()
    expect(screen.getByText('ID Mapovania')).toBeInTheDocument()
    expect(screen.getByText('Spustit')).toBeInTheDocument()
  })

  it('shows Info tab by default with description', async () => {
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    expect(screen.getByText('Popis')).toBeInTheDocument()
    expect(
      screen.getByText('Migracia partnerov z Btrieve do PostgreSQL')
    ).toBeInTheDocument()
  })

  it('shows source and target tables in Info tab', async () => {
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    expect(screen.getByText('PAB.DAT')).toBeInTheDocument()
    expect(screen.getByText('partners')).toBeInTheDocument()
  })

  it('shows "Ziadne" when no dependencies', async () => {
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    expect(screen.getByText('Ziadne')).toBeInTheDocument()
  })

  it('shows dependencies when present', async () => {
    const catWithDeps = createMockCategory({
      code: 'STK',
      dependency_codes: ['GSC'],
      dependencies: [
        {
          code: 'GSC',
          name: 'Kategorie tovaru',
          status: 'completed',
          is_satisfied: true,
        },
      ],
    })
    await act(async () => {
      render(
        <CategoryDetail
          category={catWithDeps}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    expect(screen.getByText('GSC')).toBeInTheDocument()
  })

  it('calls onClose when close button clicked', async () => {
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    // Close button is the X icon button in header
    const closeButtons = screen.getAllByRole('button')
    // The first button in header area is the close X
    const closeBtn = closeButtons.find(
      (btn) =>
        btn.querySelector('svg') !== null &&
        btn.closest('.flex.items-center.justify-between') !== null
    )
    if (closeBtn) {
      fireEvent.click(closeBtn)
      expect(mockOnClose).toHaveBeenCalled()
    }
  })

  it('switches to Batches tab and loads data', async () => {
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    await act(async () => {
      fireEvent.click(screen.getByText('Batche'))
    })
    await waitFor(() => {
      expect(mockApi.getMigrationBatches).toHaveBeenCalledWith('PAB')
    })
  })

  it('switches to Mappings tab and loads data', async () => {
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    await act(async () => {
      fireEvent.click(screen.getByText('ID Mapovania'))
    })
    await waitFor(() => {
      expect(mockApi.getMigrationMappings).toHaveBeenCalledWith('PAB', 1, 50)
    })
  })

  it('shows batches loading state', async () => {
    mockApi.getMigrationBatches.mockReturnValue(new Promise(() => {}))
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    await act(async () => {
      fireEvent.click(screen.getByText('Batche'))
    })
    // Loading spinner should be visible (no grid yet)
    expect(screen.queryByTestId('base-grid')).not.toBeInTheDocument()
  })

  it('shows batches error state', async () => {
    mockApi.getMigrationBatches.mockRejectedValue({ message: 'Batch error' })
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    await act(async () => {
      fireEvent.click(screen.getByText('Batche'))
    })
    await waitFor(() => {
      expect(screen.getByText('Batch error')).toBeInTheDocument()
    })
  })

  it('shows reset button for non-pending category', async () => {
    await act(async () => {
      render(
        <CategoryDetail
          category={mockCategory}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    // Category status is 'completed', so reset button should be visible
    expect(screen.getByText('Resetovat na pending')).toBeInTheDocument()
  })

  it('does not show reset button for pending category', async () => {
    const pendingCat = createMockCategory({ status: 'pending' })
    await act(async () => {
      render(
        <CategoryDetail
          category={pendingCat}
          onClose={mockOnClose}
          onRefresh={mockOnRefresh}
        />
      )
    })
    expect(screen.queryByText('Resetovat na pending')).not.toBeInTheDocument()
  })
})
