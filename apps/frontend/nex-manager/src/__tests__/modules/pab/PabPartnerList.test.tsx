import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'

// Mock useVirtualizer for jsdom (legacy BaseGrid path — kept for compat with
// any unrelated grid usage in this test file)
vi.mock('@tanstack/react-virtual', () => ({
  useVirtualizer: ({ count }: { count: number }) => ({
    getVirtualItems: () =>
      Array.from({ length: count }, (_, i) => ({
        index: i,
        start: i * 28,
        end: (i + 1) * 28,
        size: 28,
        key: String(i),
        measureElement: vi.fn(),
      })),
    getTotalSize: () => count * 28,
    scrollToIndex: vi.fn(),
  }),
}))

// --- Inline mock partner data ---
const mockPartners = [
  {
    id: 1,
    partner_id: 1,
    partner_name: 'HOFFER SK s.r.o.',
    company_id: '36529214',
    tax_id: '2021897584',
    vat_id: 'SK2021897584',
    is_vat_payer: true,
    is_supplier: true,
    is_customer: true,
    partner_class: 'business' as const,
    street: 'Bratislavská cesta 1798',
    city: 'Komárno',
    zip_code: '94501',
    country_code: 'SK',
    is_active: true,
    modify_id: 0,
  },
  {
    id: 2,
    partner_id: 2,
    partner_name: 'Continental Barum s.r.o.',
    company_id: '45357846',
    tax_id: '2022984561',
    vat_id: 'CZ2022984561',
    is_vat_payer: true,
    is_supplier: true,
    is_customer: false,
    partner_class: 'business' as const,
    street: 'Objízdná 1628',
    city: 'Otrokovice',
    zip_code: '76502',
    country_code: 'CZ',
    is_active: true,
    modify_id: 0,
  },
  {
    id: 3,
    partner_id: 3,
    partner_name: 'Ján Kováč',
    company_id: null,
    tax_id: null,
    vat_id: null,
    is_vat_payer: false,
    is_supplier: false,
    is_customer: true,
    partner_class: 'retail' as const,
    street: 'Hlavná 15',
    city: 'Košice',
    zip_code: '04001',
    country_code: 'SK',
    is_active: true,
    modify_id: 0,
  },
]

// --- Mock pabCatalogStore (Phase J.5.b) ---
// Component now reads from this Zustand store, not the API directly.
// Tests control store state via setStoreState() between scenarios.
const storeState = vi.hoisted(() => ({
  partners: [] as any[],
  syncStatus: 'idle' as string,
  error: null as string | null,
  lastSyncedAt: null as number | null,
  ensureLoaded: vi.fn(async () => {}),
  syncFromServer: vi.fn(async () => {}),
  upsertPartner: vi.fn(),
  removePartner: vi.fn(),
  clear: vi.fn(),
  reset(): void {
    this.partners = []
    this.syncStatus = 'idle'
    this.error = null
    this.lastSyncedAt = null
  },
}))

vi.mock('@renderer/stores/pabCatalogStore', () => ({
  usePabCatalogStore: <T,>(selector?: (s: typeof storeState) => T): T | typeof storeState => {
    return selector ? selector(storeState) : storeState
  },
}))

// --- Mock stores ---
const mockOpenDetail = vi.fn()
vi.mock('@renderer/stores/partnerCatalogStore', () => ({
  usePartnerCatalogStore: () => ({
    searchQuery: '',
    setSearchQuery: vi.fn(),
    filterPartnerClass: 'business',
    setFilterPartnerClass: vi.fn(),
    filterIsActive: null,
    setFilterIsActive: vi.fn(),
    openDetail: mockOpenDetail,
  }),
}))

vi.mock('@renderer/stores/authStore', () => ({
  useAuthStore: () => ({
    checkPermission: vi.fn().mockReturnValue(true),
  }),
}))

const mockAddToast = vi.fn()
vi.mock('@renderer/stores/toastStore', () => ({
  useToastStore: () => ({ addToast: mockAddToast }),
}))

import PabPartnerList from '@renderer/components/modules/pab/PabPartnerList'

beforeEach(() => {
  vi.clearAllMocks()
  storeState.reset()
})

describe('PabPartnerList', () => {
  it('renders heading "Katalóg partnerov"', () => {
    storeState.partners = mockPartners
    storeState.syncStatus = 'fresh'
    render(<PabPartnerList />)
    expect(screen.getByText('Katalóg partnerov')).toBeInTheDocument()
  })

  it('shows loading state when store is empty + fetching', () => {
    storeState.syncStatus = 'fetching'
    render(<PabPartnerList />)
    expect(screen.getByText(/Načítavam/)).toBeInTheDocument()
  })

  it('renders partner count when store has data', () => {
    storeState.partners = mockPartners
    storeState.syncStatus = 'fresh'
    render(<PabPartnerList />)
    expect(screen.getByText(/Celkom: 3 partnerov/)).toBeInTheDocument()
  })

  it('calls ensureLoaded on mount', () => {
    storeState.partners = mockPartners
    storeState.syncStatus = 'fresh'
    render(<PabPartnerList />)
    expect(storeState.ensureLoaded).toHaveBeenCalled()
  })

  it('shows error state when store has error and no partners', () => {
    storeState.error = 'Network error'
    storeState.syncStatus = 'error'
    render(<PabPartnerList />)
    expect(screen.getByText('Network error')).toBeInTheDocument()
    expect(screen.getByText('Skúsiť znova')).toBeInTheDocument()
  })

  it('calls syncFromServer when retry button clicked', async () => {
    storeState.error = 'Err'
    storeState.syncStatus = 'error'
    render(<PabPartnerList />)
    fireEvent.click(screen.getByText('Skúsiť znova'))
    await waitFor(() => {
      expect(storeState.syncFromServer).toHaveBeenCalled()
    })
  })

  it('renders refresh button', () => {
    storeState.partners = mockPartners
    storeState.syncStatus = 'fresh'
    render(<PabPartnerList />)
    expect(screen.getByText('Obnoviť')).toBeInTheDocument()
  })

  it('renders "Nový partner" create button', () => {
    storeState.partners = mockPartners
    storeState.syncStatus = 'fresh'
    render(<PabPartnerList />)
    expect(screen.getByText('Nový partner')).toBeInTheDocument()
  })

  it('opens create dialog when "Nový partner" clicked', async () => {
    storeState.partners = mockPartners
    storeState.syncStatus = 'fresh'
    render(<PabPartnerList />)
    fireEvent.click(screen.getByText('Nový partner'))
    await waitFor(() => {
      expect(screen.getByText('ID partnera')).toBeInTheDocument()
      expect(screen.getByText('Vytvoriť')).toBeInTheDocument()
    })
  })

  it('refresh button triggers syncFromServer', async () => {
    storeState.partners = mockPartners
    storeState.syncStatus = 'fresh'
    render(<PabPartnerList />)
    fireEvent.click(screen.getByText('Obnoviť'))
    await waitFor(() => {
      expect(storeState.syncFromServer).toHaveBeenCalled()
    })
  })
})
