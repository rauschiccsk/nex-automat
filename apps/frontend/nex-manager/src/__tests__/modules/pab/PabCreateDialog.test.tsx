import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'

// --- Mock API ---
const mockApi = vi.hoisted(() => ({
  createPabPartner: vi.fn(),
  getPabPartners: vi.fn(),
  getPabPartner: vi.fn(),
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
    constructor(msg: string, status = 500) {
      super(msg)
      this.status = status
    }
  },
}))

const mockAddToast = vi.fn()
vi.mock('@renderer/stores/toastStore', () => ({
  useToastStore: () => ({
    addToast: mockAddToast,
  }),
}))

import PabCreateDialog from '@renderer/components/modules/pab/PabCreateDialog'

const mockOnClose = vi.fn()
const mockOnCreated = vi.fn()

beforeEach(() => {
  vi.clearAllMocks()
  mockApi.createPabPartner.mockResolvedValue({ partner_id: 100, partner_name: 'Test' })
})

describe('PabCreateDialog', () => {
  it('renders dialog when open=true', () => {
    render(<PabCreateDialog open={true} onClose={mockOnClose} onCreated={mockOnCreated} />)
    expect(screen.getByText('Nový partner')).toBeInTheDocument()
  })

  it('does not render when open=false', () => {
    render(<PabCreateDialog open={false} onClose={mockOnClose} onCreated={mockOnCreated} />)
    expect(screen.queryByText('Nový partner')).not.toBeInTheDocument()
  })

  it('renders form fields', () => {
    render(<PabCreateDialog open={true} onClose={mockOnClose} onCreated={mockOnCreated} />)
    expect(screen.getByText('ID partnera')).toBeInTheDocument()
    expect(screen.getByText('Názov firmy')).toBeInTheDocument()
    expect(screen.getByText('IČO')).toBeInTheDocument()
    expect(screen.getByText('DIČ')).toBeInTheDocument()
    expect(screen.getByText('IČ DPH')).toBeInTheDocument()
  })

  it('shows validation error for empty partner name', async () => {
    render(<PabCreateDialog open={true} onClose={mockOnClose} onCreated={mockOnCreated} />)
    // Set only ID, leave name empty
    const idInput = screen.getByText('ID partnera').closest('div')!.querySelector('input')!
    fireEvent.change(idInput, { target: { value: '100' } })
    // Click submit
    fireEvent.click(screen.getByText('Vytvoriť'))
    await waitFor(() => {
      expect(screen.getByText('Názov partnera je povinný')).toBeInTheDocument()
    })
  })

  it('shows validation error for non-positive partner ID', async () => {
    render(<PabCreateDialog open={true} onClose={mockOnClose} onCreated={mockOnCreated} />)
    // Leave ID empty, set name
    const nameInput = screen.getByText('Názov firmy').closest('div')!.querySelector('input')!
    fireEvent.change(nameInput, { target: { value: 'Test Partner' } })
    fireEvent.click(screen.getByText('Vytvoriť'))
    await waitFor(() => {
      expect(screen.getByText('ID partnera musí byť kladné číslo')).toBeInTheDocument()
    })
  })

  it('shows validation error for non-numeric IČO', async () => {
    render(<PabCreateDialog open={true} onClose={mockOnClose} onCreated={mockOnCreated} />)
    const idInput = screen.getByText('ID partnera').closest('div')!.querySelector('input')!
    const nameInput = screen.getByText('Názov firmy').closest('div')!.querySelector('input')!
    const icoInput = screen.getByText('IČO').closest('div')!.querySelector('input')!
    fireEvent.change(idInput, { target: { value: '100' } })
    fireEvent.change(nameInput, { target: { value: 'Test' } })
    fireEvent.change(icoInput, { target: { value: 'abc123' } })
    fireEvent.click(screen.getByText('Vytvoriť'))
    await waitFor(() => {
      expect(screen.getByText('IČO musí obsahovať len čísla')).toBeInTheDocument()
    })
  })

  it('submits successfully with valid data', async () => {
    render(<PabCreateDialog open={true} onClose={mockOnClose} onCreated={mockOnCreated} />)
    const idInput = screen.getByText('ID partnera').closest('div')!.querySelector('input')!
    const nameInput = screen.getByText('Názov firmy').closest('div')!.querySelector('input')!
    fireEvent.change(idInput, { target: { value: '100' } })
    fireEvent.change(nameInput, { target: { value: 'Test Partner' } })
    fireEvent.click(screen.getByText('Vytvoriť'))
    await waitFor(() => {
      expect(mockApi.createPabPartner).toHaveBeenCalledWith(
        expect.objectContaining({
          partner_id: 100,
          partner_name: 'Test Partner',
        })
      )
    })
    expect(mockOnCreated).toHaveBeenCalled()
  })

  it('handles 409 duplicate error', async () => {
    const err = new Error('Partner s týmto ID už existuje')
    ;(err as any).status = 409
    mockApi.createPabPartner.mockRejectedValue(err)
    render(<PabCreateDialog open={true} onClose={mockOnClose} onCreated={mockOnCreated} />)
    const idInput = screen.getByText('ID partnera').closest('div')!.querySelector('input')!
    const nameInput = screen.getByText('Názov firmy').closest('div')!.querySelector('input')!
    fireEvent.change(idInput, { target: { value: '1' } })
    fireEvent.change(nameInput, { target: { value: 'Duplicate' } })
    fireEvent.click(screen.getByText('Vytvoriť'))
    await waitFor(() => {
      expect(screen.getByText('Partner s týmto ID už existuje')).toBeInTheDocument()
    })
  })

  it('calls onClose when Zrušiť button clicked', () => {
    render(<PabCreateDialog open={true} onClose={mockOnClose} onCreated={mockOnCreated} />)
    fireEvent.click(screen.getByText('Zrušiť'))
    expect(mockOnClose).toHaveBeenCalled()
  })

  it('renders checkbox defaults correctly', () => {
    render(<PabCreateDialog open={true} onClose={mockOnClose} onCreated={mockOnCreated} />)
    // isCustomer defaults to true, isSupplier to false
    const checkboxes = screen.getAllByRole('checkbox')
    // Find Odberateľ (should be checked) and Dodávateľ (should be unchecked)
    const odberatel = screen.getByText('Odberateľ').closest('label')!.querySelector('input[type="checkbox"]')! as HTMLInputElement
    const dodavatel = screen.getByText('Dodávateľ').closest('label')!.querySelector('input[type="checkbox"]')! as HTMLInputElement
    expect(odberatel.checked).toBe(true)
    expect(dodavatel.checked).toBe(false)
  })
})
