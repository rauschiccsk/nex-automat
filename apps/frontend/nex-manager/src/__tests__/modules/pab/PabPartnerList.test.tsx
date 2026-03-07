import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'

// Mock useVirtualizer for jsdom (no layout engine)
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

// --- Inline mock data ---
const mockPartners = [
  {
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

// --- Mock API ---
const mockApi = vi.hoisted(() => ({
  getPabPartners: vi.fn(),
  getPabPartner: vi.fn(),
  createPabPartner: vi.fn(),
  updatePabPartner: vi.fn(),
  deletePabPartner: vi.fn(),
  getPabExtensions: vi.fn(),
  upsertPabExtensions: vi.fn(),
  getPabAddresses: vi.fn(),
  createPabAddress: vi.fn(),
  updatePabAddress: vi.fn(),
  deletePabAddress: vi.fn(),
  getPabContacts: vi.fn(),
  createPabContact: vi.fn(),
  updatePabContact: vi.fn(),
  deletePabContact: vi.fn(),
  getPabBankAccounts: vi.fn(),
  createPabBankAccount: vi.fn(),
  updatePabBankAccount: vi.fn(),
  deletePabBankAccount: vi.fn(),
  getPabCategories: vi.fn(),
  addPabCategory: vi.fn(),
  removePabCategory: vi.fn(),
  getPabTexts: vi.fn(),
  upsertPabTexts: vi.fn(),
  getPabFacilities: vi.fn(),
  createPabFacility: vi.fn(),
  updatePabFacility: vi.fn(),
  deletePabFacility: vi.fn(),
  getPabHistory: vi.fn(),
  getPabHistoryVersion: vi.fn(),
}))

vi.mock('@renderer/lib/api', () => ({
  api: mockApi,
  ApiError: class ApiError extends Error {
    status: number
    constructor(msg: string, status = 500) { super(msg); this.status = status }
  },
}))

// --- Mock stores ---
const mockOpenDetail = vi.fn()
const mockSetSearchQuery = vi.fn()
const mockSetFilterPartnerClass = vi.fn()
const mockSetFilterIsActive = vi.fn()

vi.mock('@renderer/stores/partnerCatalogStore', () => ({
  usePartnerCatalogStore: () => ({
    searchQuery: '',
    setSearchQuery: mockSetSearchQuery,
    filterPartnerClass: 'business',
    setFilterPartnerClass: mockSetFilterPartnerClass,
    filterIsActive: null,
    setFilterIsActive: mockSetFilterIsActive,
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
  useToastStore: () => ({
    addToast: mockAddToast,
  }),
}))

import PabPartnerList from '@renderer/components/modules/pab/PabPartnerList'

beforeEach(() => {
  vi.clearAllMocks()
  localStorage.clear()
  mockApi.getPabPartners.mockResolvedValue({
    items: mockPartners,
    total: mockPartners.length,
  })
})

describe('PabPartnerList', () => {
  it('renders heading "Katalóg partnerov"', async () => {
    render(<PabPartnerList />)
    expect(screen.getByText('Katalóg partnerov')).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    mockApi.getPabPartners.mockReturnValue(new Promise(() => {}))
    render(<PabPartnerList />)
    expect(screen.getByText('Načítavam...')).toBeInTheDocument()
  })

  it('fetches and displays partner data', async () => {
    render(<PabPartnerList />)
    await waitFor(() => {
      expect(screen.getByText('HOFFER SK s.r.o.')).toBeInTheDocument()
    })
    expect(screen.getByText('Continental Barum s.r.o.')).toBeInTheDocument()
    expect(mockApi.getPabPartners).toHaveBeenCalled()
  })

  it('shows total partner count', async () => {
    render(<PabPartnerList />)
    await waitFor(() => {
      expect(screen.getByText(/Celkom: 3 partnerov/)).toBeInTheDocument()
    })
  })

  it('shows error state on API failure', async () => {
    mockApi.getPabPartners.mockRejectedValue(new Error('Network error'))
    render(<PabPartnerList />)
    await waitFor(() => {
      expect(screen.getByText('Network error')).toBeInTheDocument()
    })
  })

  it('shows retry button on error', async () => {
    mockApi.getPabPartners.mockRejectedValue(new Error('Chyba'))
    render(<PabPartnerList />)
    await waitFor(() => {
      expect(screen.getByText('Skúsiť znova')).toBeInTheDocument()
    })
  })

  it('calls fetchPartners again when retry button clicked', async () => {
    mockApi.getPabPartners.mockRejectedValueOnce(new Error('Err'))
    render(<PabPartnerList />)
    await waitFor(() => {
      expect(screen.getByText('Skúsiť znova')).toBeInTheDocument()
    })
    // Second call should succeed
    mockApi.getPabPartners.mockResolvedValueOnce({ items: mockPartners, total: 3 })
    fireEvent.click(screen.getByText('Skúsiť znova'))
    expect(mockApi.getPabPartners).toHaveBeenCalledTimes(2)
  })

  it('renders search input with placeholder', async () => {
    render(<PabPartnerList />)
    expect(screen.getByPlaceholderText('Hľadať partnera...')).toBeInTheDocument()
  })

  it('renders partner class filter select', async () => {
    render(<PabPartnerList />)
    expect(screen.getByText('Obchodní partneri')).toBeInTheDocument()
  })

  it('renders "Nový partner" create button', async () => {
    render(<PabPartnerList />)
    expect(screen.getByText('Nový partner')).toBeInTheDocument()
  })

  it('opens create dialog when "Nový partner" clicked', async () => {
    render(<PabPartnerList />)
    await waitFor(() => {
      expect(screen.getByText('HOFFER SK s.r.o.')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByText('Nový partner'))
    await waitFor(() => {
      // Dialog renders heading "Nový partner" as h2 + the button "Nový partner" — verify dialog form fields
      expect(screen.getByText('ID partnera')).toBeInTheDocument()
      expect(screen.getByText('Vytvoriť')).toBeInTheDocument()
    })
  })
})
