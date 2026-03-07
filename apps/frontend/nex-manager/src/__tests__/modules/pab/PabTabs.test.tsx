import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, act, fireEvent } from '@testing-library/react'

// --- Inline mock data (avoid import issues with mockApi.ts) ---

const partner = {
  partner_id: 1,
  partner_name: 'HOFFER SK s.r.o.',
  reg_name: null,
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
  bank_account_count: 1,
  facility_count: 0,
  created_at: '2025-01-15T10:00:00Z',
  updated_at: '2025-01-15T10:00:00Z',
}

const extensions = {
  partner_id: 1,
  sale_payment_method_id: null,
  sale_transport_method_id: null,
  sale_payment_due_days: 30,
  sale_currency_code: 'EUR',
  sale_price_category: null,
  sale_discount_percent: 5,
  sale_credit_limit: 50000,
  purchase_payment_method_id: null,
  purchase_transport_method_id: null,
  purchase_payment_due_days: 14,
  purchase_currency_code: 'EUR',
  purchase_price_category: null,
  purchase_discount_percent: 0,
  last_sale_date: '2025-06-01',
  last_purchase_date: '2025-05-15',
  is_active: true,
  created_at: '2025-01-15T10:00:00Z',
  updated_at: '2025-01-15T10:00:00Z',
}

const addresses = [
  {
    id: 1, partner_id: 1, address_type: 'registered' as const,
    street: 'Bratislavská cesta 1798', city: 'Komárno',
    zip_code: '94501', country_code: 'SK',
    is_active: true, created_at: '2025-01-15T10:00:00Z', updated_at: '2025-01-15T10:00:00Z',
  }
]

const contacts = [
  {
    contact_id: 1, partner_id: 1, contact_type: 'person' as const,
    title: 'Ing.', first_name: 'Peter', last_name: 'Novák',
    function_name: 'Obchodný riaditeľ',
    phone_work: '+421 35 1234567', phone_mobile: '+421 905 123456',
    phone_private: null, fax: null, email: 'peter.novak@hoffer.sk',
    street: null, city: null, zip_code: null, country_code: null,
    is_active: true, created_at: '2025-01-15T10:00:00Z', updated_at: '2025-01-15T10:00:00Z',
  }
]

const bankAccounts = [
  {
    account_id: 1, partner_id: 1,
    iban_code: 'SK3112000000198742637541', swift_code: 'TATRSKBX',
    account_number: '198742637541', bank_name: 'Tatra banka',
    bank_seat: 'Bratislava', vs_sale: '12345', vs_purchase: null,
    is_primary: true, is_active: true,
    created_at: '2025-01-15T10:00:00Z', updated_at: '2025-01-15T10:00:00Z',
  }
]

const categories = [
  {
    id: 1, partner_id: 1, category_id: 10, category_type: 'supplier' as const,
    is_active: true, created_at: '2025-01-15T10:00:00Z', updated_at: '2025-01-15T10:00:00Z',
  }
]

const texts = [
  {
    text_id: 1, partner_id: 1, text_type: 'description' as const,
    line_number: 1, language: 'sk', text_content: 'Hlavný dodávateľ pneumatík',
    is_active: true, created_at: '2025-01-15T10:00:00Z', updated_at: '2025-01-15T10:00:00Z',
  }
]

const facilities = [
  {
    facility_id: 1, partner_id: 1, facility_name: 'Sklad Komárno',
    street: 'Priemyselná 5', city: 'Komárno', zip_code: '94501',
    country_code: 'SK', phone: '+421 35 9876543', fax: null,
    email: 'sklad@hoffer.sk', transport_method_id: null,
    is_active: true, created_at: '2025-01-15T10:00:00Z', updated_at: '2025-01-15T10:00:00Z',
  }
]

const history = [
  {
    history_id: 1, partner_id: 1, modify_id: 0,
    partner_name: 'HOFFER SK s.r.o.', reg_name: null,
    company_id: '36529214', tax_id: '2021897584',
    vat_id: 'SK2021897584', is_vat_payer: true,
    is_supplier: true, is_customer: true,
    street: 'Bratislavská cesta 1798', city: 'Komárno',
    zip_code: '94501', country_code: 'SK',
    partner_class: 'business' as const,
    valid_from: '2025-01-15T10:00:00Z', valid_to: null, changed_by: 'migration',
  },
  {
    history_id: 2, partner_id: 1, modify_id: 1,
    partner_name: 'HOFFER SK s.r.o. (starý)', reg_name: null,
    company_id: '36529214', tax_id: null,
    vat_id: null, is_vat_payer: false,
    is_supplier: true, is_customer: false,
    street: 'Stará 1', city: 'Bratislava',
    zip_code: '81101', country_code: 'SK',
    partner_class: 'business' as const,
    valid_from: '2024-06-01T08:00:00Z', valid_to: '2025-01-15T09:59:59Z', changed_by: 'admin',
  }
]

// --- Mock API ---

const mockApi = vi.hoisted(() => ({
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
  assignPabCategory: vi.fn(),
  unassignPabCategory: vi.fn(),
  getPabTexts: vi.fn(),
  upsertPabTexts: vi.fn(),
  getPabFacilities: vi.fn(),
  createPabFacility: vi.fn(),
  updatePabFacility: vi.fn(),
  deletePabFacility: vi.fn(),
  getPabHistory: vi.fn(),
  getPabHistoryVersion: vi.fn(),
  updatePabPartner: vi.fn(),
  deletePabPartner: vi.fn(),
}))

vi.mock('@renderer/lib/api', () => ({
  api: mockApi,
  ApiError: class ApiError extends Error {
    status: number
    constructor(msg: string, status = 500) { super(msg); this.status = status }
  }
}))

vi.mock('@renderer/stores/authStore', () => ({
  useAuthStore: () => ({
    checkPermission: vi.fn().mockReturnValue(true)
  })
}))

const mockAddToast = vi.fn()
vi.mock('@renderer/stores/toastStore', () => ({
  useToastStore: () => ({
    addToast: mockAddToast
  })
}))

// Tab components
let PabBasicTab: any
let PabExtensionsTab: any
let PabAddressesTab: any
let PabContactsTab: any
let PabBankAccountsTab: any
let PabCategoriesTab: any
let PabTextsTab: any
let PabFacilitiesTab: any
let PabHistoryTab: any

beforeEach(async () => {
  vi.clearAllMocks()

  mockApi.getPabExtensions.mockResolvedValue(extensions)
  mockApi.upsertPabExtensions.mockResolvedValue(extensions)
  mockApi.getPabAddresses.mockResolvedValue(addresses)
  mockApi.createPabAddress.mockResolvedValue(addresses[0])
  mockApi.updatePabAddress.mockResolvedValue(addresses[0])
  mockApi.deletePabAddress.mockResolvedValue({ message: 'deleted' })
  mockApi.getPabContacts.mockResolvedValue(contacts)
  mockApi.createPabContact.mockResolvedValue(contacts[0])
  mockApi.updatePabContact.mockResolvedValue(contacts[0])
  mockApi.deletePabContact.mockResolvedValue({ message: 'deleted' })
  mockApi.getPabBankAccounts.mockResolvedValue(bankAccounts)
  mockApi.createPabBankAccount.mockResolvedValue(bankAccounts[0])
  mockApi.updatePabBankAccount.mockResolvedValue(bankAccounts[0])
  mockApi.deletePabBankAccount.mockResolvedValue({ message: 'deleted' })
  mockApi.getPabCategories.mockResolvedValue(categories)
  mockApi.assignPabCategory.mockResolvedValue(categories[0])
  mockApi.unassignPabCategory.mockResolvedValue({ message: 'deleted' })
  mockApi.getPabTexts.mockResolvedValue(texts)
  mockApi.upsertPabTexts.mockResolvedValue(texts[0])
  mockApi.getPabFacilities.mockResolvedValue(facilities)
  mockApi.createPabFacility.mockResolvedValue(facilities[0])
  mockApi.updatePabFacility.mockResolvedValue(facilities[0])
  mockApi.deletePabFacility.mockResolvedValue({ message: 'deleted' })
  mockApi.getPabHistory.mockResolvedValue(history)
  mockApi.getPabHistoryVersion.mockResolvedValue(history[0])
  mockApi.updatePabPartner.mockResolvedValue({ ...partner, modify_id: 1 })
  mockApi.deletePabPartner.mockResolvedValue({ message: 'deleted' })

  const [basic, ext, addr, cont, bank, cat, txt, fac, hist] = await Promise.all([
    import('@renderer/components/modules/pab/tabs/PabBasicTab'),
    import('@renderer/components/modules/pab/tabs/PabExtensionsTab'),
    import('@renderer/components/modules/pab/tabs/PabAddressesTab'),
    import('@renderer/components/modules/pab/tabs/PabContactsTab'),
    import('@renderer/components/modules/pab/tabs/PabBankAccountsTab'),
    import('@renderer/components/modules/pab/tabs/PabCategoriesTab'),
    import('@renderer/components/modules/pab/tabs/PabTextsTab'),
    import('@renderer/components/modules/pab/tabs/PabFacilitiesTab'),
    import('@renderer/components/modules/pab/tabs/PabHistoryTab'),
  ])
  PabBasicTab = basic.default
  PabExtensionsTab = ext.default
  PabAddressesTab = addr.default
  PabContactsTab = cont.default
  PabBankAccountsTab = bank.default
  PabCategoriesTab = cat.default
  PabTextsTab = txt.default
  PabFacilitiesTab = fac.default
  PabHistoryTab = hist.default
})

// ===== BasicTab =====
describe('PabBasicTab', () => {
  it('renders partner basic data', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    expect(screen.getByDisplayValue('HOFFER SK s.r.o.')).toBeInTheDocument()
    expect(screen.getByDisplayValue('36529214')).toBeInTheDocument()
  })

  it('shows Vymazať button', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    expect(screen.getByText('Vymazať')).toBeInTheDocument()
  })

  it('shows Uložiť button', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    expect(screen.getByText('Uložiť')).toBeInTheDocument()
  })

  it('shows delete confirmation dialog', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    fireEvent.click(screen.getByText('Vymazať'))
    await waitFor(() => {
      expect(screen.getByText('Potvrdenie vymazania')).toBeInTheDocument()
    })
  })

  it('calls deletePabPartner on confirm', async () => {
    const onDeleted = vi.fn()
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={onDeleted} />)
    })
    fireEvent.click(screen.getByText('Vymazať'))
    await waitFor(() => expect(screen.getByText('Áno, vymazať')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Áno, vymazať')) })
    await waitFor(() => {
      expect(mockApi.deletePabPartner).toHaveBeenCalledWith(1)
    })
  })

  it('cancels delete on Nie', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    fireEvent.click(screen.getByText('Vymazať'))
    await waitFor(() => expect(screen.getByText('Nie')).toBeInTheDocument())
    fireEvent.click(screen.getByText('Nie'))
    expect(mockApi.deletePabPartner).not.toHaveBeenCalled()
  })
})

// ===== ExtensionsTab =====
describe('PabExtensionsTab', () => {
  it('renders sale/purchase sections', async () => {
    await act(async () => { render(<PabExtensionsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Predajné parametre')).toBeInTheDocument()
      expect(screen.getByText('Nákupné parametre')).toBeInTheDocument()
    })
  })

  it('loads extension data from API', async () => {
    await act(async () => { render(<PabExtensionsTab partnerId={1} />) })
    await waitFor(() => {
      expect(mockApi.getPabExtensions).toHaveBeenCalledWith(1)
    })
    expect(screen.getByDisplayValue('30')).toBeInTheDocument()
  })

  it('shows default values when extensions not found', async () => {
    mockApi.getPabExtensions.mockRejectedValue({ status: 404 })
    await act(async () => { render(<PabExtensionsTab partnerId={99} />) })
    await waitFor(() => {
      expect(screen.getAllByDisplayValue('14').length).toBeGreaterThan(0)
    })
  })
})

// ===== AddressesTab =====
describe('PabAddressesTab', () => {
  it('renders existing addresses', async () => {
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Sídlo')).toBeInTheDocument()
      expect(screen.getByText(/Komárno/)).toBeInTheDocument()
    })
  })

  it('shows empty state when no addresses', async () => {
    mockApi.getPabAddresses.mockResolvedValue([])
    await act(async () => { render(<PabAddressesTab partnerId={99} />) })
    await waitFor(() => {
      expect(screen.getByText('Žiadne adresy')).toBeInTheDocument()
    })
  })

  it('shows add buttons for available types', async () => {
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Korešpondenčná')).toBeInTheDocument()
      expect(screen.getByText('Fakturačná')).toBeInTheDocument()
    })
  })
})

// ===== ContactsTab =====
describe('PabContactsTab', () => {
  it('renders contacts from API', async () => {
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => {
      expect(mockApi.getPabContacts).toHaveBeenCalledWith(1)
      expect(screen.getByText(/Peter/)).toBeInTheDocument()
    })
  })

  it('calls API for empty contacts', async () => {
    mockApi.getPabContacts.mockResolvedValue([])
    await act(async () => { render(<PabContactsTab partnerId={99} />) })
    await waitFor(() => { expect(mockApi.getPabContacts).toHaveBeenCalledWith(99) })
  })
})

// ===== BankAccountsTab =====
describe('PabBankAccountsTab', () => {
  it('renders IBAN and bank name', async () => {
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText(/SK3112000000198742637541/)).toBeInTheDocument()
      expect(screen.getByText(/Tatra banka/)).toBeInTheDocument()
    })
  })

  it('calls API for empty accounts', async () => {
    mockApi.getPabBankAccounts.mockResolvedValue([])
    await act(async () => { render(<PabBankAccountsTab partnerId={99} />) })
    await waitFor(() => { expect(mockApi.getPabBankAccounts).toHaveBeenCalledWith(99) })
  })
})

// ===== CategoriesTab =====
describe('PabCategoriesTab', () => {
  it('fetches categories', async () => {
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => { expect(mockApi.getPabCategories).toHaveBeenCalledWith(1) })
  })

  it('calls API for empty categories', async () => {
    mockApi.getPabCategories.mockResolvedValue([])
    await act(async () => { render(<PabCategoriesTab partnerId={99} />) })
    await waitFor(() => { expect(mockApi.getPabCategories).toHaveBeenCalledWith(99) })
  })
})

// ===== TextsTab =====
describe('PabTextsTab', () => {
  it('fetches texts', async () => {
    await act(async () => { render(<PabTextsTab partnerId={1} />) })
    await waitFor(() => { expect(mockApi.getPabTexts).toHaveBeenCalledWith(1) })
  })

  it('calls API for empty texts', async () => {
    mockApi.getPabTexts.mockResolvedValue([])
    await act(async () => { render(<PabTextsTab partnerId={99} />) })
    await waitFor(() => { expect(mockApi.getPabTexts).toHaveBeenCalledWith(99) })
  })
})

// ===== FacilitiesTab =====
describe('PabFacilitiesTab', () => {
  it('renders facilities', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText(/Sklad Komárno/)).toBeInTheDocument()
    })
  })

  it('calls API for empty facilities', async () => {
    mockApi.getPabFacilities.mockResolvedValue([])
    await act(async () => { render(<PabFacilitiesTab partnerId={99} />) })
    await waitFor(() => { expect(mockApi.getPabFacilities).toHaveBeenCalledWith(99) })
  })
})

// ===== HistoryTab =====
describe('PabHistoryTab', () => {
  it('renders history timeline', async () => {
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText(/Verzia 0/)).toBeInTheDocument()
      expect(screen.getByText(/Verzia 1/)).toBeInTheDocument()
    })
  })

  it('shows empty state', async () => {
    mockApi.getPabHistory.mockResolvedValue([])
    await act(async () => { render(<PabHistoryTab partnerId={99} />) })
    await waitFor(() => {
      expect(screen.getByText('Žiadna história zmien')).toBeInTheDocument()
    })
  })

  it('marks current version', async () => {
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Aktuálna')).toBeInTheDocument()
    })
  })

  it('shows Detail buttons', async () => {
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getAllByText('Detail').length).toBe(2)
    })
  })

  it('loads version detail on click', async () => {
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => expect(screen.getAllByText('Detail').length).toBe(2))
    await act(async () => { fireEvent.click(screen.getAllByText('Detail')[0]) })
    await waitFor(() => { expect(mockApi.getPabHistoryVersion).toHaveBeenCalled() })
  })
})
