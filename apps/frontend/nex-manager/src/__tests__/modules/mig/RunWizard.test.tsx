import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'

// --- Mock API with vi.hoisted ---
const mockApi = vi.hoisted(() => ({
  runMigration: vi.fn(),
}))

vi.mock('@renderer/lib/api', () => ({
  api: mockApi,
  ApiError: class ApiError extends Error {
    status: number
    detail?: string
    constructor(msg: string, status = 500) {
      super(msg)
      this.status = status
      this.detail = msg
    }
  },
}))

import RunWizard from '@renderer/components/modules/migration/RunWizard'
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

const mockOnClose = vi.fn()
const mockOnCompleted = vi.fn()

beforeEach(() => {
  vi.clearAllMocks()
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

describe('RunWizard', () => {
  it('renders step 1 — dependency check', () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    expect(screen.getByText('Kontrola predpokladov')).toBeInTheDocument()
    expect(
      screen.getByText(/Kontrola zavislosti pre PAB/)
    ).toBeInTheDocument()
  })

  it('shows "no dependencies" message when category has none', () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    expect(
      screen.getByText(/nema ziadne zavislosti/)
    ).toBeInTheDocument()
  })

  it('shows dependency list when category has dependencies', () => {
    const category = createMockCategory({
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
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    expect(screen.getByText('GSC')).toBeInTheDocument()
    expect(screen.getByText('Kategorie tovaru')).toBeInTheDocument()
  })

  it('disables Dalej when unsatisfied dependencies', () => {
    const category = createMockCategory({
      code: 'STK',
      dependency_codes: ['GSC'],
      dependencies: [
        {
          code: 'GSC',
          name: 'Kategorie tovaru',
          status: 'pending',
          is_satisfied: false,
        },
      ],
    })
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    const dalejButton = screen.getByText('Dalej').closest('button')!
    expect(dalejButton).toBeDisabled()
  })

  it('shows warning when dependencies not satisfied', () => {
    const category = createMockCategory({
      dependency_codes: ['GSC'],
      dependencies: [
        {
          code: 'GSC',
          name: 'Kategorie tovaru',
          status: 'pending',
          is_satisfied: false,
        },
      ],
    })
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    expect(
      screen.getByText(/Nie vsetky zavislosti su splnene/)
    ).toBeInTheDocument()
  })

  it('navigates to step 2 on Dalej click', () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    fireEvent.click(screen.getByText('Dalej'))
    expect(screen.getByText('Informacie')).toBeInTheDocument()
    expect(
      screen.getByText(/Informacie o migracii/)
    ).toBeInTheDocument()
  })

  it('navigates to step 3 (confirmation) and shows checkbox', () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    // Go to step 2
    fireEvent.click(screen.getByText('Dalej'))
    // Go to step 3
    fireEvent.click(screen.getByText('Dalej'))
    expect(screen.getByText('Potvrdenie')).toBeInTheDocument()
    expect(
      screen.getByText(/Rozumiem, ze migracia prepise existujuce data/)
    ).toBeInTheDocument()
  })

  it('Spustit migraciu button is disabled until checkbox checked', () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    fireEvent.click(screen.getByText('Dalej')) // step 2
    fireEvent.click(screen.getByText('Dalej')) // step 3
    const runButton = screen.getByText('Spustit migraciu').closest('button')!
    expect(runButton).toBeDisabled()
  })

  it('Spustit migraciu button enables after checkbox checked', () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    fireEvent.click(screen.getByText('Dalej')) // step 2
    fireEvent.click(screen.getByText('Dalej')) // step 3
    // Check the confirmation checkbox
    const checkbox = screen.getByRole('checkbox')
    fireEvent.click(checkbox)
    const runButton = screen.getByText('Spustit migraciu').closest('button')!
    expect(runButton).not.toBeDisabled()
  })

  it('runs migration and shows result on step 4', async () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    fireEvent.click(screen.getByText('Dalej')) // step 2
    fireEvent.click(screen.getByText('Dalej')) // step 3
    fireEvent.click(screen.getByRole('checkbox'))
    await act(async () => {
      fireEvent.click(screen.getByText('Spustit migraciu'))
    })
    await waitFor(() => {
      expect(mockApi.runMigration).toHaveBeenCalledWith({
        category: 'PAB',
        dry_run: false,
      })
    })
    await waitFor(() => {
      // "Migracia dokoncena" appears in both heading and message
      expect(screen.getAllByText('Migracia dokoncena').length).toBeGreaterThanOrEqual(1)
    })
  })

  it('shows error on migration failure', async () => {
    const ApiError = (await import('@renderer/lib/api')).ApiError as any
    mockApi.runMigration.mockRejectedValue(
      Object.assign(new Error('Migracia zlyhala'), { status: 500, detail: 'Migracia zlyhala' })
    )
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    fireEvent.click(screen.getByText('Dalej')) // step 2
    fireEvent.click(screen.getByText('Dalej')) // step 3
    fireEvent.click(screen.getByRole('checkbox'))
    await act(async () => {
      fireEvent.click(screen.getByText('Spustit migraciu'))
    })
    await waitFor(() => {
      // "Migracia zlyhala" appears in both heading and error text
      expect(screen.getAllByText('Migracia zlyhala').length).toBeGreaterThanOrEqual(1)
    })
  })

  it('shows 501 not implemented state', async () => {
    mockApi.runMigration.mockRejectedValue(
      Object.assign(new Error('Extractor nie je implementovany'), {
        status: 501,
        detail: 'Extractor nie je implementovany',
      })
    )
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    fireEvent.click(screen.getByText('Dalej'))
    fireEvent.click(screen.getByText('Dalej'))
    fireEvent.click(screen.getByRole('checkbox'))
    await act(async () => {
      fireEvent.click(screen.getByText('Spustit migraciu'))
    })
    await waitFor(() => {
      expect(screen.getByText('Este nie je implementovane')).toBeInTheDocument()
    })
  })

  it('Zrusit button calls onClose on step 1', () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    fireEvent.click(screen.getByText('Zrusit'))
    expect(mockOnClose).toHaveBeenCalled()
  })

  it('Spat button goes back to previous step', () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    fireEvent.click(screen.getByText('Dalej')) // step 2
    expect(screen.getByText('Informacie')).toBeInTheDocument()
    fireEvent.click(screen.getByText('Spat'))
    expect(screen.getByText('Kontrola predpokladov')).toBeInTheDocument()
  })

  it('step 2 shows source and target tables', () => {
    const category = createMockCategory()
    render(
      <RunWizard
        category={category}
        onClose={mockOnClose}
        onCompleted={mockOnCompleted}
      />
    )
    fireEvent.click(screen.getByText('Dalej')) // step 2
    expect(screen.getByText('PAB.DAT')).toBeInTheDocument()
    expect(screen.getByText('partners')).toBeInTheDocument()
  })
})
