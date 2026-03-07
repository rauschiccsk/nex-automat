import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, act, fireEvent, within } from '@testing-library/react'

/**
 * Helper to find an input/select by its sibling label text.
 * Components use <div><label>Text</label><input/></div> pattern without htmlFor,
 * so getByLabelText does not work.
 */
function getInputByLabel(labelText: string): HTMLInputElement | HTMLSelectElement {
  // Find all labels matching the text
  const labels = Array.from(document.querySelectorAll('label'))
  const label = labels.find((l) => l.textContent?.trim() === labelText)
  if (!label) throw new Error(`Could not find label with text "${labelText}"`)
  const parent = label.parentElement!
  const input = parent.querySelector('input, select, textarea')
  if (!input) throw new Error(`Could not find input/select sibling for label "${labelText}"`)
  return input as HTMLInputElement | HTMLSelectElement
}

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

  it('submits form and calls updatePabPartner', async () => {
    const onUpdated = vi.fn()
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={onUpdated} onDeleted={vi.fn()} />)
    })
    await act(async () => {
      fireEvent.click(screen.getByTestId('save-button'))
    })
    await waitFor(() => {
      expect(mockApi.updatePabPartner).toHaveBeenCalledWith(1, expect.objectContaining({
        partner_name: 'HOFFER SK s.r.o.',
      }))
    })
    await waitFor(() => { expect(onUpdated).toHaveBeenCalled() })
  })

  it('shows validation error when partner name is empty', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    const nameInput = screen.getByTestId('partner-name')
    fireEvent.change(nameInput, { target: { value: '' } })
    await act(async () => {
      fireEvent.click(screen.getByTestId('save-button'))
    })
    await waitFor(() => {
      expect(screen.getByText('Názov partnera je povinný')).toBeInTheDocument()
    })
    expect(mockApi.updatePabPartner).not.toHaveBeenCalled()
  })

  it('shows validation error for non-numeric company_id', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    const icoInput = screen.getByDisplayValue('36529214')
    fireEvent.change(icoInput, { target: { value: 'abc' } })
    await act(async () => {
      fireEvent.click(screen.getByTestId('save-button'))
    })
    await waitFor(() => {
      expect(screen.getByText('IČO musí obsahovať len čísla')).toBeInTheDocument()
    })
    expect(mockApi.updatePabPartner).not.toHaveBeenCalled()
  })

  it('clears field error on input change', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    const nameInput = screen.getByTestId('partner-name')
    fireEvent.change(nameInput, { target: { value: '' } })
    await act(async () => { fireEvent.click(screen.getByTestId('save-button')) })
    await waitFor(() => { expect(screen.getByText('Názov partnera je povinný')).toBeInTheDocument() })
    fireEvent.change(nameInput, { target: { value: 'New Name' } })
    await waitFor(() => {
      expect(screen.queryByText('Názov partnera je povinný')).not.toBeInTheDocument()
    })
  })

  it('shows error toast when save fails', async () => {
    mockApi.updatePabPartner.mockRejectedValue({ message: 'Server error' })
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    await act(async () => { fireEvent.click(screen.getByTestId('save-button')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Server error', 'error')
    })
  })

  it('shows error toast when delete fails', async () => {
    mockApi.deletePabPartner.mockRejectedValue({ message: 'Delete failed' })
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    fireEvent.click(screen.getByText('Vymazať'))
    await waitFor(() => expect(screen.getByText('Áno, vymazať')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Áno, vymazať')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Delete failed', 'error')
    })
  })

  it('renders all form fields including checkboxes', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    expect(screen.getByDisplayValue('2021897584')).toBeInTheDocument()
    expect(screen.getByDisplayValue('SK2021897584')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Bratislavská cesta 1798')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Komárno')).toBeInTheDocument()
    expect(screen.getByDisplayValue('94501')).toBeInTheDocument()
    expect(screen.getByText('Odberateľ')).toBeInTheDocument()
    expect(screen.getByText('Dodávateľ')).toBeInTheDocument()
    expect(screen.getByText('Aktívny')).toBeInTheDocument()
    expect(screen.getByText('Platca DPH')).toBeInTheDocument()
  })

  it('changes checkbox values', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    const checkboxes = screen.getAllByRole('checkbox')
    // customer, supplier, active, vatPayer = 4 checkboxes
    expect(checkboxes.length).toBe(4)
    fireEvent.click(checkboxes[0]) // toggle customer
    fireEvent.click(checkboxes[1]) // toggle supplier
  })

  it('changes select value for partner class', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    const select = screen.getByDisplayValue('Obchodný partner')
    fireEvent.change(select, { target: { value: 'retail' } })
    expect(screen.getByDisplayValue('Retail zákazník')).toBeInTheDocument()
  })

  it('renders readonly partner_id and modify_id', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    expect(screen.getByText('1')).toBeInTheDocument()
    expect(screen.getByText('0')).toBeInTheDocument()
  })

  it('closes delete dialog on backdrop click', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    fireEvent.click(screen.getByText('Vymazať'))
    await waitFor(() => expect(screen.getByText('Potvrdenie vymazania')).toBeInTheDocument())
    // The backdrop is the div with bg-black/40 class
    const backdrop = document.querySelector('.fixed.inset-0.z-40')!
    fireEvent.click(backdrop)
    await waitFor(() => {
      expect(screen.queryByText('Potvrdenie vymazania')).not.toBeInTheDocument()
    })
  })

  it('updates address fields', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    const streetInput = screen.getByDisplayValue('Bratislavská cesta 1798')
    fireEvent.change(streetInput, { target: { value: 'Nová ulica 123' } })
    expect(screen.getByDisplayValue('Nová ulica 123')).toBeInTheDocument()
    const cityInput = screen.getByDisplayValue('Komárno')
    fireEvent.change(cityInput, { target: { value: 'Bratislava' } })
    const zipInput = screen.getByDisplayValue('94501')
    fireEvent.change(zipInput, { target: { value: '81101' } })
    const countryInput = screen.getByDisplayValue('SK')
    fireEvent.change(countryInput, { target: { value: 'CZ' } })
  })

  it('updates reg_name, tax_id, vat_id inputs', async () => {
    await act(async () => {
      render(<PabBasicTab partner={partner} onUpdated={vi.fn()} onDeleted={vi.fn()} />)
    })
    const taxInput = screen.getByDisplayValue('2021897584')
    fireEvent.change(taxInput, { target: { value: '9999999' } })
    const vatInput = screen.getByDisplayValue('SK2021897584')
    fireEvent.change(vatInput, { target: { value: 'CZ1234' } })
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

  it('submits extensions form', async () => {
    await act(async () => { render(<PabExtensionsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Predajné parametre')).toBeInTheDocument())
    await act(async () => { fireEvent.submit(screen.getByText('Uložiť').closest('form')!) })
    await waitFor(() => {
      expect(mockApi.upsertPabExtensions).toHaveBeenCalledWith(1, expect.objectContaining({
        sale_payment_due_days: 30,
        sale_currency_code: 'EUR',
      }))
    })
  })

  it('shows error toast when save fails', async () => {
    mockApi.upsertPabExtensions.mockRejectedValue({ message: 'Save failed' })
    await act(async () => { render(<PabExtensionsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Predajné parametre')).toBeInTheDocument())
    await act(async () => { fireEvent.submit(screen.getByText('Uložiť').closest('form')!) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Save failed', 'error')
    })
  })

  it('shows last_sale_date and last_purchase_date when present', async () => {
    await act(async () => { render(<PabExtensionsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Posledný predaj')).toBeInTheDocument()
      expect(screen.getByText('2025-06-01')).toBeInTheDocument()
      expect(screen.getByText('Posledný nákup')).toBeInTheDocument()
      expect(screen.getByText('2025-05-15')).toBeInTheDocument()
    })
  })

  it('updates sale input fields', async () => {
    await act(async () => { render(<PabExtensionsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByDisplayValue('30')).toBeInTheDocument())
    const salePayment = screen.getByDisplayValue('30')
    fireEvent.change(salePayment, { target: { value: '45' } })
    expect(screen.getByDisplayValue('45')).toBeInTheDocument()
  })

  it('updates purchase input fields', async () => {
    await act(async () => { render(<PabExtensionsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Nákupné parametre')).toBeInTheDocument())
    // Change purchase discount
    const discountInputs = screen.getAllByDisplayValue('0')
    fireEvent.change(discountInputs[0], { target: { value: '10' } })
  })

  it('updates currency to uppercase', async () => {
    await act(async () => { render(<PabExtensionsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Predajné parametre')).toBeInTheDocument())
    const currencyInputs = screen.getAllByDisplayValue('EUR')
    fireEvent.change(currencyInputs[0], { target: { value: 'usd' } })
  })

  it('updates price category and credit limit', async () => {
    await act(async () => { render(<PabExtensionsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByDisplayValue('50000')).toBeInTheDocument())
    fireEvent.change(screen.getByDisplayValue('50000'), { target: { value: '75000' } })
    fireEvent.change(screen.getByDisplayValue('5'), { target: { value: '8' } })
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

  it('opens add form for new address type', async () => {
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Korešpondenčná')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Korešpondenčná')) })
    await waitFor(() => {
      expect(screen.getByText('Nová adresa: Korešpondenčná')).toBeInTheDocument()
    })
  })

  it('saves new address via API', async () => {
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Fakturačná')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Fakturačná')) })
    await waitFor(() => expect(screen.getByText('Nová adresa: Fakturačná')).toBeInTheDocument())
    const streetInput = getInputByLabel('Ulica')
    fireEvent.change(streetInput, { target: { value: 'Testová 5' } })
    const cityInput = getInputByLabel('Mesto')
    fireEvent.change(cityInput, { target: { value: 'TestCity' } })
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockApi.createPabAddress).toHaveBeenCalledWith(1, expect.objectContaining({
        address_type: 'invoice',
        street: 'Testová 5',
        city: 'TestCity',
      }))
    })
  })

  it('opens edit form for existing address', async () => {
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Sídlo')).toBeInTheDocument())
    const editBtn = screen.getByTitle('Upraviť')
    await act(async () => { fireEvent.click(editBtn) })
    await waitFor(() => {
      expect(screen.getByText(/Upraviť: Sídlo/)).toBeInTheDocument()
    })
  })

  it('updates existing address via API', async () => {
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Sídlo')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => expect(screen.getByText(/Upraviť: Sídlo/)).toBeInTheDocument())
    const streetInput = getInputByLabel('Ulica')
    fireEvent.change(streetInput, { target: { value: 'Nová 99' } })
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockApi.updatePabAddress).toHaveBeenCalledWith(1, 'registered', expect.objectContaining({
        street: 'Nová 99',
      }))
    })
  })

  it('cancels edit form', async () => {
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Sídlo')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => expect(screen.getByText('Zrušiť')).toBeInTheDocument())
    fireEvent.click(screen.getByText('Zrušiť'))
    await waitFor(() => {
      expect(screen.queryByText(/Upraviť: Sídlo/)).not.toBeInTheDocument()
    })
  })

  it('deletes address via API', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockApi.deletePabAddress).toHaveBeenCalledWith(1, 'registered')
    })
    vi.restoreAllMocks()
  })

  it('shows error toast when address load fails', async () => {
    mockApi.getPabAddresses.mockRejectedValue({ message: 'Load error' })
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Load error', 'error')
    })
  })

  it('shows error toast when address save fails', async () => {
    mockApi.createPabAddress.mockRejectedValue({ message: 'Save error' })
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Fakturačná')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Fakturačná')) })
    await waitFor(() => expect(screen.getByText('Uložiť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Save error', 'error')
    })
  })

  it('shows error toast when address delete fails', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    mockApi.deletePabAddress.mockRejectedValue({ message: 'Del error' })
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Del error', 'error')
    })
    vi.restoreAllMocks()
  })

  it('cancels delete when confirm returns false', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(false)
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    expect(mockApi.deletePabAddress).not.toHaveBeenCalled()
    vi.restoreAllMocks()
  })

  it('updates zip and country in edit form', async () => {
    await act(async () => { render(<PabAddressesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => expect(getInputByLabel('PSČ')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('PSČ'), { target: { value: '12345' } })
    fireEvent.change(getInputByLabel('Krajina'), { target: { value: 'CZ' } })
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

  it('shows empty state text', async () => {
    mockApi.getPabContacts.mockResolvedValue([])
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Žiadne kontakty')).toBeInTheDocument()
    })
  })

  it('renders contact details including phone and email', async () => {
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText(/Ing./)).toBeInTheDocument()
      expect(screen.getByText(/Obchodný riaditeľ/)).toBeInTheDocument()
      expect(screen.getByText(/\+421 35 1234567/)).toBeInTheDocument()
      expect(screen.getByText(/\+421 905 123456/)).toBeInTheDocument()
      expect(screen.getByText(/peter.novak@hoffer.sk/)).toBeInTheDocument()
    })
  })

  it('opens add contact form', async () => {
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať kontakt')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať kontakt')) })
    await waitFor(() => {
      expect(screen.getByText('Nový kontakt')).toBeInTheDocument()
    })
  })

  it('saves new contact via API', async () => {
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať kontakt')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať kontakt')) })
    await waitFor(() => expect(screen.getByText('Nový kontakt')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('Meno'), { target: { value: 'Ján' } })
    fireEvent.change(getInputByLabel('Priezvisko'), { target: { value: 'Tester' } })
    fireEvent.change(getInputByLabel('Email'), { target: { value: 'test@test.sk' } })
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockApi.createPabContact).toHaveBeenCalledWith(1, expect.objectContaining({
        contact_type: 'person',
        first_name: 'Ján',
        last_name: 'Tester',
        email: 'test@test.sk',
      }))
    })
  })

  it('opens edit form for existing contact', async () => {
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => {
      expect(screen.getByText('Upraviť kontakt')).toBeInTheDocument()
      expect(screen.getByDisplayValue('Peter')).toBeInTheDocument()
    })
  })

  it('updates existing contact via API', async () => {
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => expect(screen.getByDisplayValue('Peter')).toBeInTheDocument())
    fireEvent.change(screen.getByDisplayValue('Peter'), { target: { value: 'Pavol' } })
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockApi.updatePabContact).toHaveBeenCalledWith(1, 1, expect.objectContaining({
        first_name: 'Pavol',
      }))
    })
  })

  it('cancels edit form', async () => {
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => expect(screen.getByText('Zrušiť')).toBeInTheDocument())
    fireEvent.click(screen.getByText('Zrušiť'))
    await waitFor(() => {
      expect(screen.queryByText('Upraviť kontakt')).not.toBeInTheDocument()
    })
  })

  it('deletes contact via API', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockApi.deletePabContact).toHaveBeenCalledWith(1, 1)
    })
    vi.restoreAllMocks()
  })

  it('shows error toast when contact save fails', async () => {
    mockApi.createPabContact.mockRejectedValue({ message: 'Save fail' })
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať kontakt')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať kontakt')) })
    await waitFor(() => expect(screen.getByText('Uložiť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Save fail', 'error')
    })
  })

  it('shows error toast when contact delete fails', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    mockApi.deletePabContact.mockRejectedValue({ message: 'Del fail' })
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Del fail', 'error')
    })
    vi.restoreAllMocks()
  })

  it('shows error toast when contacts load fails', async () => {
    mockApi.getPabContacts.mockRejectedValue({ message: 'Load contacts error' })
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Load contacts error', 'error')
    })
  })

  it('fills additional form fields: title, function, phone fields, fax', async () => {
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať kontakt')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať kontakt')) })
    await waitFor(() => expect(getInputByLabel('Titul')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('Titul'), { target: { value: 'Dr.' } })
    fireEvent.change(getInputByLabel('Funkcia'), { target: { value: 'CEO' } })
    fireEvent.change(getInputByLabel('Telefón (práca)'), { target: { value: '+421111' } })
    fireEvent.change(getInputByLabel('Mobil'), { target: { value: '+421222' } })
    fireEvent.change(getInputByLabel('Fax'), { target: { value: '+421333' } })
  })

  it('changes contact type in add form', async () => {
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať kontakt')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať kontakt')) })
    await waitFor(() => expect(getInputByLabel('Typ')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('Typ'), { target: { value: 'address' } })
  })

  it('cancels delete when confirm returns false', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(false)
    await act(async () => { render(<PabContactsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    expect(mockApi.deletePabContact).not.toHaveBeenCalled()
    vi.restoreAllMocks()
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

  it('shows empty state text', async () => {
    mockApi.getPabBankAccounts.mockResolvedValue([])
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Žiadne bankové účty')).toBeInTheDocument()
    })
  })

  it('shows primary badge', async () => {
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Primárny')).toBeInTheDocument()
    })
  })

  it('shows SWIFT code', async () => {
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText(/SWIFT: TATRSKBX/)).toBeInTheDocument()
    })
  })

  it('opens add bank account form', async () => {
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať bankový účet')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať bankový účet')) })
    await waitFor(() => {
      expect(screen.getByText('Nový bankový účet')).toBeInTheDocument()
    })
  })

  it('saves new bank account via API', async () => {
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať bankový účet')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať bankový účet')) })
    await waitFor(() => expect(screen.getByText('Nový bankový účet')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('IBAN'), { target: { value: 'SK1234567890' } })
    fireEvent.change(getInputByLabel('SWIFT/BIC'), { target: { value: 'GIBASKBX' } })
    fireEvent.change(getInputByLabel('Názov banky'), { target: { value: 'Slovenská sporiteľňa' } })
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockApi.createPabBankAccount).toHaveBeenCalledWith(1, expect.objectContaining({
        iban_code: 'SK1234567890',
        swift_code: 'GIBASKBX',
        bank_name: 'Slovenská sporiteľňa',
      }))
    })
  })

  it('opens edit form for existing bank account', async () => {
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => {
      expect(screen.getByText('Upraviť bankový účet')).toBeInTheDocument()
      expect(screen.getByDisplayValue('SK3112000000198742637541')).toBeInTheDocument()
    })
  })

  it('updates existing bank account via API', async () => {
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => expect(screen.getByDisplayValue('SK3112000000198742637541')).toBeInTheDocument())
    fireEvent.change(screen.getByDisplayValue('SK3112000000198742637541'), { target: { value: 'SK9999' } })
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockApi.updatePabBankAccount).toHaveBeenCalledWith(1, 1, expect.objectContaining({
        iban_code: 'SK9999',
      }))
    })
  })

  it('cancels bank account edit', async () => {
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => expect(screen.getByText('Zrušiť')).toBeInTheDocument())
    fireEvent.click(screen.getByText('Zrušiť'))
    await waitFor(() => {
      expect(screen.queryByText('Upraviť bankový účet')).not.toBeInTheDocument()
    })
  })

  it('deletes bank account via API', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockApi.deletePabBankAccount).toHaveBeenCalledWith(1, 1)
    })
    vi.restoreAllMocks()
  })

  it('shows error when bank account save fails', async () => {
    mockApi.createPabBankAccount.mockRejectedValue({ message: 'Bank save err' })
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať bankový účet')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať bankový účet')) })
    await waitFor(() => expect(screen.getByText('Uložiť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Bank save err', 'error')
    })
  })

  it('shows error when bank account delete fails', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    mockApi.deletePabBankAccount.mockRejectedValue({ message: 'Bank del err' })
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Bank del err', 'error')
    })
    vi.restoreAllMocks()
  })

  it('shows error when bank accounts load fails', async () => {
    mockApi.getPabBankAccounts.mockRejectedValue({ message: 'Load bank err' })
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Load bank err', 'error')
    })
  })

  it('fills additional form fields: account_number, bank_seat, vs_sale, vs_purchase, is_primary', async () => {
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať bankový účet')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať bankový účet')) })
    await waitFor(() => expect(getInputByLabel('Číslo účtu')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('Číslo účtu'), { target: { value: '1234567890' } })
    fireEvent.change(getInputByLabel('Sídlo banky'), { target: { value: 'Košice' } })
    fireEvent.change(getInputByLabel('VS predaj'), { target: { value: '111' } })
    fireEvent.change(getInputByLabel('VS nákup'), { target: { value: '222' } })
    // "Primárny účet" uses a wrapping label pattern: <label><input type="checkbox"/><span>Primárny účet</span></label>
    const primaryLabel = Array.from(document.querySelectorAll('label')).find((l) => l.textContent?.includes('Primárny účet'))!
    const checkbox = primaryLabel.querySelector('input[type="checkbox"]')!
    fireEvent.click(checkbox)
  })

  it('cancels delete when confirm returns false', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(false)
    await act(async () => { render(<PabBankAccountsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    expect(mockApi.deletePabBankAccount).not.toHaveBeenCalled()
    vi.restoreAllMocks()
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

  it('shows empty state text', async () => {
    mockApi.getPabCategories.mockResolvedValue([])
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Žiadne priradené skupiny')).toBeInTheDocument()
    })
  })

  it('renders category with type badge', async () => {
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Kategória #10')).toBeInTheDocument()
      expect(screen.getByText('Dodávateľ')).toBeInTheDocument()
    })
  })

  it('opens add category form', async () => {
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať skupinu')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať skupinu')) })
    await waitFor(() => {
      expect(screen.getByText('Pridať skupinu')).toBeInTheDocument()
      expect(getInputByLabel('ID kategórie')).toBeInTheDocument()
    })
  })

  it('assigns category via API', async () => {
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať skupinu')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať skupinu')) })
    await waitFor(() => expect(getInputByLabel('ID kategórie')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('ID kategórie'), { target: { value: '20' } })
    fireEvent.change(getInputByLabel('Typ'), { target: { value: 'supplier' } })
    await act(async () => { fireEvent.click(screen.getByText('Priradiť')) })
    await waitFor(() => {
      expect(mockApi.assignPabCategory).toHaveBeenCalledWith(1, {
        category_id: 20,
        category_type: 'supplier',
      })
    })
  })

  it('shows validation error for invalid category ID', async () => {
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať skupinu')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať skupinu')) })
    await waitFor(() => expect(screen.getByText('Priradiť')).toBeInTheDocument())
    // Submit without entering a valid ID
    await act(async () => { fireEvent.click(screen.getByText('Priradiť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Zadajte platné ID kategórie', 'error')
    })
    expect(mockApi.assignPabCategory).not.toHaveBeenCalled()
  })

  it('unassigns category via API', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockApi.unassignPabCategory).toHaveBeenCalledWith(1, 10)
    })
    vi.restoreAllMocks()
  })

  it('cancels category form', async () => {
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať skupinu')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať skupinu')) })
    await waitFor(() => expect(screen.getByText('Zrušiť')).toBeInTheDocument())
    fireEvent.click(screen.getByText('Zrušiť'))
    await waitFor(() => {
      expect(document.querySelectorAll('label').length === 0 || !Array.from(document.querySelectorAll('label')).some((l) => l.textContent?.trim() === 'ID kategórie')).toBe(true)
    })
  })

  it('shows error when assign fails', async () => {
    mockApi.assignPabCategory.mockRejectedValue({ message: 'Assign err' })
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať skupinu')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať skupinu')) })
    await waitFor(() => expect(getInputByLabel('ID kategórie')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('ID kategórie'), { target: { value: '5' } })
    await act(async () => { fireEvent.click(screen.getByText('Priradiť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Assign err', 'error')
    })
  })

  it('shows error when unassign fails', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    mockApi.unassignPabCategory.mockRejectedValue({ message: 'Unassign err' })
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Unassign err', 'error')
    })
    vi.restoreAllMocks()
  })

  it('shows error when categories load fails', async () => {
    mockApi.getPabCategories.mockRejectedValue({ message: 'Load cat err' })
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Load cat err', 'error')
    })
  })

  it('cancels unassign when confirm returns false', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(false)
    await act(async () => { render(<PabCategoriesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    expect(mockApi.unassignPabCategory).not.toHaveBeenCalled()
    vi.restoreAllMocks()
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

  it('renders all text type sections', async () => {
    await act(async () => { render(<PabTextsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Meno vlastníka')).toBeInTheDocument()
      expect(screen.getByText('Popis')).toBeInTheDocument()
      expect(screen.getByText('Poznámka')).toBeInTheDocument()
    })
  })

  it('renders existing text content', async () => {
    await act(async () => { render(<PabTextsTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByDisplayValue('Hlavný dodávateľ pneumatík')).toBeInTheDocument()
    })
  })

  it('shows save button when text is dirty', async () => {
    await act(async () => { render(<PabTextsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByDisplayValue('Hlavný dodávateľ pneumatík')).toBeInTheDocument())
    const textarea = screen.getByDisplayValue('Hlavný dodávateľ pneumatík')
    fireEvent.change(textarea, { target: { value: 'Zmenený text' } })
    await waitFor(() => {
      expect(screen.getByText('Uložiť')).toBeInTheDocument()
    })
  })

  it('saves text via API', async () => {
    await act(async () => { render(<PabTextsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByDisplayValue('Hlavný dodávateľ pneumatík')).toBeInTheDocument())
    const textarea = screen.getByDisplayValue('Hlavný dodávateľ pneumatík')
    fireEvent.change(textarea, { target: { value: 'Nový popis' } })
    await waitFor(() => expect(screen.getByText('Uložiť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockApi.upsertPabTexts).toHaveBeenCalledWith(1, expect.objectContaining({
        text_type: 'description',
        text_content: 'Nový popis',
      }))
    })
  })

  it('shows error toast when text save fails', async () => {
    mockApi.upsertPabTexts.mockRejectedValue({ message: 'Text save err' })
    await act(async () => { render(<PabTextsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByDisplayValue('Hlavný dodávateľ pneumatík')).toBeInTheDocument())
    const textarea = screen.getByDisplayValue('Hlavný dodávateľ pneumatík')
    fireEvent.change(textarea, { target: { value: 'Changed' } })
    await waitFor(() => expect(screen.getByText('Uložiť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Text save err', 'error')
    })
  })

  it('does not show save button when text is not dirty', async () => {
    await act(async () => { render(<PabTextsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByDisplayValue('Hlavný dodávateľ pneumatík')).toBeInTheDocument())
    // No save button visible when text hasn't changed
    expect(screen.queryByText('Uložiť')).not.toBeInTheDocument()
  })

  it('edits owner_name text type', async () => {
    await act(async () => { render(<PabTextsTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Meno vlastníka')).toBeInTheDocument())
    const ownerTextarea = screen.getByPlaceholderText('Zadajte meno vlastníka...')
    fireEvent.change(ownerTextarea, { target: { value: 'Ján Novák' } })
    await waitFor(() => expect(screen.getAllByText('Uložiť').length).toBeGreaterThan(0))
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

  it('shows empty state text', async () => {
    mockApi.getPabFacilities.mockResolvedValue([])
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText('Žiadne prevádzkarne')).toBeInTheDocument()
    })
  })

  it('renders facility details: address, phone, email', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => {
      expect(screen.getByText(/Sklad Komárno/)).toBeInTheDocument()
      expect(screen.getByText(/Priemyselná 5/)).toBeInTheDocument()
      expect(screen.getByText(/\+421 35 9876543/)).toBeInTheDocument()
      expect(screen.getByText(/sklad@hoffer.sk/)).toBeInTheDocument()
    })
  })

  it('opens add facility form', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať prevádzku')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať prevádzku')) })
    await waitFor(() => {
      expect(screen.getByText('Nová prevádzka')).toBeInTheDocument()
    })
  })

  it('saves new facility via API', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať prevádzku')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať prevádzku')) })
    await waitFor(() => expect(screen.getByText('Nová prevádzka')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('Názov prevádzky *'), { target: { value: 'Nový sklad' } })
    fireEvent.change(getInputByLabel('Ulica'), { target: { value: 'Testová 1' } })
    fireEvent.change(getInputByLabel('Mesto'), { target: { value: 'Nitra' } })
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockApi.createPabFacility).toHaveBeenCalledWith(1, expect.objectContaining({
        facility_name: 'Nový sklad',
        street: 'Testová 1',
        city: 'Nitra',
      }))
    })
  })

  it('shows validation error when facility name is empty', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať prevádzku')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať prevádzku')) })
    await waitFor(() => expect(screen.getByText('Nová prevádzka')).toBeInTheDocument())
    // Don't fill name, just click save
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(screen.getByText('Názov prevádzky je povinný')).toBeInTheDocument()
    })
    expect(mockApi.createPabFacility).not.toHaveBeenCalled()
  })

  it('opens edit form for existing facility', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => {
      expect(screen.getByText('Upraviť prevádzku')).toBeInTheDocument()
      expect(screen.getByDisplayValue('Sklad Komárno')).toBeInTheDocument()
    })
  })

  it('updates existing facility via API', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => expect(screen.getByDisplayValue('Sklad Komárno')).toBeInTheDocument())
    fireEvent.change(screen.getByDisplayValue('Sklad Komárno'), { target: { value: 'Sklad Bratislava' } })
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockApi.updatePabFacility).toHaveBeenCalledWith(1, 1, expect.objectContaining({
        facility_name: 'Sklad Bratislava',
      }))
    })
  })

  it('cancels facility edit', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Upraviť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Upraviť')) })
    await waitFor(() => expect(screen.getByText('Zrušiť')).toBeInTheDocument())
    fireEvent.click(screen.getByText('Zrušiť'))
    await waitFor(() => {
      expect(screen.queryByText('Upraviť prevádzku')).not.toBeInTheDocument()
    })
  })

  it('deletes facility via API', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockApi.deletePabFacility).toHaveBeenCalledWith(1, 1)
    })
    vi.restoreAllMocks()
  })

  it('shows error when facility save fails', async () => {
    mockApi.createPabFacility.mockRejectedValue({ message: 'Fac save err' })
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať prevádzku')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať prevádzku')) })
    await waitFor(() => expect(screen.getByText('Nová prevádzka')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('Názov prevádzky *'), { target: { value: 'Test' } })
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Fac save err', 'error')
    })
  })

  it('shows error when facility delete fails', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    mockApi.deletePabFacility.mockRejectedValue({ message: 'Fac del err' })
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Fac del err', 'error')
    })
    vi.restoreAllMocks()
  })

  it('shows error when facilities load fails', async () => {
    mockApi.getPabFacilities.mockRejectedValue({ message: 'Load fac err' })
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Load fac err', 'error')
    })
  })

  it('clears validation error on input change', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať prevádzku')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať prevádzku')) })
    await waitFor(() => expect(screen.getByText('Nová prevádzka')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Uložiť')) })
    await waitFor(() => expect(screen.getByText('Názov prevádzky je povinný')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('Názov prevádzky *'), { target: { value: 'Valid' } })
    await waitFor(() => {
      expect(screen.queryByText('Názov prevádzky je povinný')).not.toBeInTheDocument()
    })
  })

  it('fills additional form fields: zip, country, phone, fax, email', async () => {
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByText('Pridať prevádzku')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByText('Pridať prevádzku')) })
    await waitFor(() => expect(getInputByLabel('PSČ')).toBeInTheDocument())
    fireEvent.change(getInputByLabel('PSČ'), { target: { value: '94900' } })
    fireEvent.change(getInputByLabel('Krajina'), { target: { value: 'CZ' } })
    fireEvent.change(getInputByLabel('Telefón'), { target: { value: '+421999' } })
    fireEvent.change(getInputByLabel('Fax'), { target: { value: '+421888' } })
    fireEvent.change(getInputByLabel('Email'), { target: { value: 'new@test.sk' } })
  })

  it('cancels delete when confirm returns false', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(false)
    await act(async () => { render(<PabFacilitiesTab partnerId={1} />) })
    await waitFor(() => expect(screen.getByTitle('Odstrániť')).toBeInTheDocument())
    await act(async () => { fireEvent.click(screen.getByTitle('Odstrániť')) })
    expect(mockApi.deletePabFacility).not.toHaveBeenCalled()
    vi.restoreAllMocks()
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

  it('displays version detail overlay with partner data', async () => {
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => expect(screen.getAllByText('Detail').length).toBe(2))
    await act(async () => { fireEvent.click(screen.getAllByText('Detail')[0]) })
    await waitFor(() => {
      // Version detail overlay shows heading and badge
      const h4 = Array.from(document.querySelectorAll('h4')).find(
        (el) => el.textContent?.includes('Detail verzie')
      )
      expect(h4).toBeTruthy()
      // "Aktuálna" appears both in overlay and timeline; verify at least 2 badges
      expect(screen.getAllByText('Aktuálna').length).toBeGreaterThanOrEqual(2)
    })
  })

  it('closes version detail overlay', async () => {
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => expect(screen.getAllByText('Detail').length).toBe(2))
    await act(async () => { fireEvent.click(screen.getAllByText('Detail')[0]) })
    await waitFor(() => expect(screen.getByText(/Detail verzie #0/)).toBeInTheDocument())
    // Click close button (X)
    const closeBtn = screen.getByText(/Detail verzie/).closest('div')!.querySelector('button')!
    await act(async () => { fireEvent.click(closeBtn) })
    await waitFor(() => {
      expect(screen.queryByText(/Detail verzie #0/)).not.toBeInTheDocument()
    })
  })

  it('shows error toast when version load fails', async () => {
    mockApi.getPabHistoryVersion.mockRejectedValue({ message: 'Version err' })
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => expect(screen.getAllByText('Detail').length).toBe(2))
    await act(async () => { fireEvent.click(screen.getAllByText('Detail')[0]) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('Version err', 'error')
    })
  })

  it('shows error toast when history load fails', async () => {
    mockApi.getPabHistory.mockRejectedValue({ message: 'History err' })
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => {
      expect(mockAddToast).toHaveBeenCalledWith('History err', 'error')
    })
  })

  it('renders changed_by and company_id in history items', async () => {
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => {
      // "Zmenil: " and the name are separate text nodes in the same <span>; use function matcher
      const spans = Array.from(document.querySelectorAll('span'))
      expect(spans.some((s) => s.textContent?.includes('Zmenil:') && s.textContent?.includes('migration'))).toBe(true)
      expect(spans.some((s) => s.textContent?.includes('Zmenil:') && s.textContent?.includes('admin'))).toBe(true)
      // Both history entries share the same company_id, so use getAllByText
      expect(screen.getAllByText(/IČO: 36529214/).length).toBeGreaterThanOrEqual(1)
    })
  })

  it('renders non-current version without Aktuálna badge', async () => {
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => {
      // Only one "Aktuálna" badge for the current version
      const badges = screen.getAllByText('Aktuálna')
      expect(badges.length).toBe(1)
    })
  })

  it('shows valid_to date for past versions', async () => {
    await act(async () => { render(<PabHistoryTab partnerId={1} />) })
    await waitFor(() => {
      // Past version has a valid_to date displayed
      expect(screen.getByText(/Do:.*2025/)).toBeInTheDocument()
    })
  })
})
