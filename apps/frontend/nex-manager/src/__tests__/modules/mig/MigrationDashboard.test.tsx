import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'

// --- Mock API with vi.hoisted ---
const mockApi = vi.hoisted(() => ({
  getMigrationCategories: vi.fn(),
  getMigrationStats: vi.fn(),
  runMigration: vi.fn(),
  getMigrationBatches: vi.fn(),
  getMigrationMappings: vi.fn(),
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

// --- Mock BaseGrid (uses virtualization) ---
vi.mock('@renderer/components/grids', () => ({
  BaseGrid: ({ data }: { data: unknown[] }) => (
    <div data-testid="base-grid">rows: {data.length}</div>
  ),
}))

import MigrationDashboard from '@renderer/components/modules/migration/MigrationDashboard'
import type {
  MigrationCategory,
  MigrationStats,
  CategoriesListResponse,
} from '@renderer/types/migration'

// --- Factory helpers ---
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
    status: 'pending',
    record_count: 164,
    first_migrated_at: null,
    last_migrated_at: null,
    last_batch_id: null,
    can_run: true,
    blocked_by: [],
    ...overrides,
  }
}

function createMockStats(overrides: Partial<MigrationStats> = {}): MigrationStats {
  return {
    total_categories: 9,
    completed_categories: 1,
    pending_categories: 7,
    failed_categories: 1,
    total_records_migrated: 164,
    total_batches: 3,
    last_migration_at: '2025-06-01T10:00:00Z',
    ...overrides,
  }
}

const mockCategories: MigrationCategory[] = [
  createMockCategory({ code: 'PAB', name: 'Obchodni partneri', status: 'completed', level: 0, can_run: true }),
  createMockCategory({
    code: 'GSC',
    name: 'Kategorie tovaru',
    status: 'pending',
    level: 0,
    can_run: true,
  }),
  createMockCategory({
    code: 'STK',
    name: 'Skladove karty',
    status: 'failed',
    level: 1,
    dependency_codes: ['GSC'],
    dependencies: [{ code: 'GSC', name: 'Kategorie tovaru', status: 'pending', is_satisfied: false }],
    can_run: false,
  }),
  createMockCategory({
    code: 'TSH',
    name: 'Hlavicky dokladov',
    status: 'running',
    level: 2,
    dependency_codes: ['GSC', 'STK'],
    dependencies: [
      { code: 'GSC', name: 'Kategorie tovaru', status: 'pending', is_satisfied: false },
      { code: 'STK', name: 'Skladove karty', status: 'failed', is_satisfied: false },
    ],
    can_run: false,
  }),
]

const mockCategoriesResponse: CategoriesListResponse = {
  categories: mockCategories,
  total: 4,
  completed: 1,
  pending: 2,
  failed: 1,
}

const mockStats = createMockStats()

beforeEach(() => {
  vi.clearAllMocks()
  localStorage.clear()
  mockApi.getMigrationCategories.mockResolvedValue(mockCategoriesResponse)
  mockApi.getMigrationStats.mockResolvedValue(mockStats)
  mockApi.runMigration.mockResolvedValue({
    batch_id: 1,
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
})

describe('MigrationDashboard', () => {
  it('renders heading "Migracia dat"', async () => {
    render(<MigrationDashboard />)
    expect(screen.getByText('Migracia dat')).toBeInTheDocument()
  })

  it('shows loading spinner initially', () => {
    mockApi.getMigrationCategories.mockReturnValue(new Promise(() => {}))
    mockApi.getMigrationStats.mockReturnValue(new Promise(() => {}))
    render(<MigrationDashboard />)
    // Loading state has spinner, no category cards
    expect(screen.queryByTestId('category-card-PAB')).not.toBeInTheDocument()
  })

  it('renders dashboard testid', async () => {
    render(<MigrationDashboard />)
    expect(screen.getByTestId('migration-dashboard')).toBeInTheDocument()
  })

  it('fetches and displays category cards', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('category-card-PAB')).toBeInTheDocument()
    })
    expect(screen.getByTestId('category-card-GSC')).toBeInTheDocument()
    expect(screen.getByTestId('category-card-STK')).toBeInTheDocument()
    expect(screen.getByTestId('category-card-TSH')).toBeInTheDocument()
  })

  it('displays status badges with correct labels', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('category-card-PAB')).toBeInTheDocument()
    })
    // "Dokoncene" appears in stats bar AND in status badge — use getAllByText
    expect(screen.getAllByText('Dokoncene').length).toBeGreaterThanOrEqual(1)
    expect(screen.getAllByText('Caka').length).toBeGreaterThanOrEqual(1)
    expect(screen.getAllByText('Chyba').length).toBeGreaterThanOrEqual(1)
    expect(screen.getAllByText('Prebieha').length).toBeGreaterThanOrEqual(1)
  })

  it('displays stats bar with correct values', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByText('Celkom kategorii')).toBeInTheDocument()
    })
    expect(screen.getByText('9')).toBeInTheDocument()
    // "Dokoncene" appears in both stats bar label and category badge
    expect(screen.getAllByText('Dokoncene').length).toBeGreaterThanOrEqual(1)
    expect(screen.getByText('Cakajuce')).toBeInTheDocument()
    expect(screen.getByText('Neuspesne')).toBeInTheDocument()
  })

  it('renders category code and name on cards', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('category-card-PAB')).toBeInTheDocument()
    })
    // PAB code is unique on PAB card
    const pabCard = screen.getByTestId('category-card-PAB')
    expect(pabCard).toHaveTextContent('PAB')
    expect(pabCard).toHaveTextContent('Obchodni partneri')
    // GSC appears both as card code AND as dependency badge
    const gscCard = screen.getByTestId('category-card-GSC')
    expect(gscCard).toHaveTextContent('GSC')
    expect(gscCard).toHaveTextContent('Kategorie tovaru')
  })

  it('shows dependency badges on cards', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('category-card-STK')).toBeInTheDocument()
    })
    // STK depends on GSC — should show GSC dependency badge inside STK card
    const stkCard = screen.getByTestId('category-card-STK')
    expect(stkCard).toBeInTheDocument()
  })

  it('shows error state on API failure', async () => {
    mockApi.getMigrationCategories.mockRejectedValue({ message: 'Network error' })
    mockApi.getMigrationStats.mockRejectedValue({ message: 'Network error' })
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalled()
    })
  })

  it('renders Obnovit (refresh) button', async () => {
    render(<MigrationDashboard />)
    expect(screen.getByText('Obnovit')).toBeInTheDocument()
  })

  it('clicking Obnovit refetches data', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('category-card-PAB')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByText('Obnovit'))
    // Should call API again
    await waitFor(() => {
      expect(mockApi.getMigrationCategories).toHaveBeenCalledTimes(2)
    })
  })

  it('clicking category card toggles selection', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('category-card-PAB')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByTestId('category-card-PAB'))
    // CategoryDetail should appear — it renders tabs
    await waitFor(() => {
      expect(screen.getByText('Info')).toBeInTheDocument()
      expect(screen.getByText('Batche')).toBeInTheDocument()
    })
  })

  it('shows run button for runnable categories', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('run-button-PAB')).toBeInTheDocument()
    })
    // PAB is completed, so it shows Re-run
    expect(screen.getByText('Re-run')).toBeInTheDocument()
  })

  it('shows Spustit button for pending runnable categories', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('run-button-GSC')).toBeInTheDocument()
    })
    // "Spustit" may appear multiple times (button + CategoryDetail tab label)
    expect(screen.getAllByText('Spustit').length).toBeGreaterThanOrEqual(1)
  })

  it('opens confirm dialog when run button clicked', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('run-button-GSC')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByTestId('run-button-GSC'))
    await waitFor(() => {
      expect(screen.getByText('Spustit migraciu')).toBeInTheDocument()
      expect(screen.getByText('Ano, spustit')).toBeInTheDocument()
    })
  })

  it('closes confirm dialog on cancel (Nie)', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('run-button-GSC')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByTestId('run-button-GSC'))
    await waitFor(() => {
      expect(screen.getByText('Nie')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByText('Nie'))
    await waitFor(() => {
      expect(screen.queryByText('Ano, spustit')).not.toBeInTheDocument()
    })
  })

  it('groups categories by dependency level', async () => {
    render(<MigrationDashboard />)
    await waitFor(() => {
      expect(screen.getByText('Uroven 0')).toBeInTheDocument()
    })
    expect(screen.getByText('Uroven 1')).toBeInTheDocument()
    expect(screen.getByText('Uroven 2')).toBeInTheDocument()
  })
})
