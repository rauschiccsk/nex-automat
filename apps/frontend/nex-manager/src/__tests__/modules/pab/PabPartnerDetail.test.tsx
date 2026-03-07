import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'

// --- Inline mock data ---
const mockPartner = {
  partner_id: 1,
  partner_name: 'HOFFER SK s.r.o.',
  reg_name: 'HOFFER SK s.r.o.',
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
  modify_id: 0
}

// --- Mock API with vi.hoisted ---
const mockApi = vi.hoisted(() => ({
  getPabPartner: vi.fn(),
  getPabPartners: vi.fn(),
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
  }
}))

// Mock partner catalog store
const mockSetActiveTab = vi.fn()
const mockCloseDetail = vi.fn()
let activeTab = 'basic'

vi.mock('@renderer/stores/partnerCatalogStore', () => ({
  usePartnerCatalogStore: () => ({
    selectedPartnerId: 1,
    activeTab,
    setActiveTab: (tab: string) => {
      activeTab = tab
      mockSetActiveTab(tab)
    },
    closeDetail: mockCloseDetail
  })
}))

vi.mock('@renderer/stores/authStore', () => ({
  useAuthStore: () => ({
    checkPermission: vi.fn().mockReturnValue(true)
  })
}))

vi.mock('@renderer/stores/toastStore', () => ({
  useToastStore: () => ({
    addToast: vi.fn()
  })
}))

import PabPartnerDetail from '@renderer/components/modules/pab/PabPartnerDetail'

beforeEach(() => {
  vi.clearAllMocks()
  activeTab = 'basic'
  mockApi.getPabPartner.mockResolvedValue(mockPartner)
  mockApi.getPabExtensions.mockResolvedValue({
    payment_due_days: 30,
    credit_limit: 50000,
    discount_percent: 5,
    currency: 'EUR'
  })
  mockApi.getPabAddresses.mockResolvedValue([])
  mockApi.getPabContacts.mockResolvedValue([])
  mockApi.getPabBankAccounts.mockResolvedValue([])
  mockApi.getPabCategories.mockResolvedValue([])
  mockApi.getPabTexts.mockResolvedValue({ owner_name: null, description: null, notice: null })
  mockApi.getPabFacilities.mockResolvedValue([])
  mockApi.getPabHistory.mockResolvedValue([])
})

describe('PabPartnerDetail', () => {
  it('shows loading state initially', () => {
    mockApi.getPabPartner.mockReturnValue(new Promise(() => {}))
    render(<PabPartnerDetail />)
    expect(screen.getByText('Načítavam...')).toBeInTheDocument()
  })

  it('fetches and displays partner name', async () => {
    render(<PabPartnerDetail />)
    await waitFor(() => {
      expect(screen.getByText(/HOFFER SK s.r.o./)).toBeInTheDocument()
    })
    expect(mockApi.getPabPartner).toHaveBeenCalledWith(1)
  })

  it('shows partner ID and version', async () => {
    render(<PabPartnerDetail />)
    await waitFor(() => {
      expect(screen.getByText(/ID: 1/)).toBeInTheDocument()
      expect(screen.getByText(/Verzia: 0/)).toBeInTheDocument()
    })
  })

  it('renders all 9 tab buttons', async () => {
    render(<PabPartnerDetail />)
    await waitFor(() => {
      expect(screen.getByText('Základné')).toBeInTheDocument()
    })
    const tabLabels = ['Základné', 'Rozšírené', 'Adresy', 'Kontakty', 'Bankové účty', 'Skupiny', 'Texty', 'Prevádzkarne', 'História']
    for (const label of tabLabels) {
      expect(screen.getByText(label)).toBeInTheDocument()
    }
  })

  it('tab buttons are clickable and call setActiveTab', async () => {
    render(<PabPartnerDetail />)
    await waitFor(() => {
      expect(screen.getByText('Základné')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByText('Adresy'))
    expect(mockSetActiveTab).toHaveBeenCalledWith('addresses')
  })

  it('shows error state when API fails', async () => {
    mockApi.getPabPartner.mockRejectedValue(new Error('Server error'))
    render(<PabPartnerDetail />)
    await waitFor(() => {
      expect(screen.getByText('Server error')).toBeInTheDocument()
    })
  })

  it('shows back-to-list button on error', async () => {
    mockApi.getPabPartner.mockRejectedValue(new Error('Not found'))
    render(<PabPartnerDetail />)
    await waitFor(() => {
      expect(screen.getByText('Späť na zoznam')).toBeInTheDocument()
    })
  })

  it('clicking back button calls closeDetail', async () => {
    render(<PabPartnerDetail />)
    await waitFor(() => {
      expect(screen.getByTitle('Späť na zoznam')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByTitle('Späť na zoznam'))
    expect(mockCloseDetail).toHaveBeenCalled()
  })

  it('renders basic tab content by default', async () => {
    render(<PabPartnerDetail />)
    await waitFor(() => {
      // Basic tab shows "Názov firmy" label
      expect(screen.getByText('Názov firmy')).toBeInTheDocument()
    })
  })
})
