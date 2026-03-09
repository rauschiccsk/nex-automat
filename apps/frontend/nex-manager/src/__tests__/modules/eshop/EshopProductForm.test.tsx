import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'

// --- Mock API ---
const mockApi = vi.hoisted(() => ({
  getEshopOrders: vi.fn(),
  getEshopOrderDetail: vi.fn(),
  updateEshopOrder: vi.fn(),
  getEshopProducts: vi.fn(),
  getEshopProduct: vi.fn(),
  createEshopProduct: vi.fn(),
  updateEshopProduct: vi.fn(),
  deleteEshopProduct: vi.fn(),
  getEshopTenants: vi.fn(),
}))

vi.mock('@renderer/lib/api', () => ({
  api: mockApi,
  ApiError: class ApiError extends Error {
    status: number
    constructor(msg: string, status = 500) { super(msg); this.status = status }
  },
}))

// --- Mock stores ---
const mockCloseProductEdit = vi.fn()

vi.mock('@renderer/stores/eshopStore', () => ({
  useEshopStore: () => ({
    selectedProductId: null, // new product mode
    closeProductEdit: mockCloseProductEdit,
  }),
}))

const mockAddToast = vi.fn()
vi.mock('@renderer/stores/toastStore', () => ({
  useToastStore: () => ({
    addToast: mockAddToast,
  }),
}))

import EshopProductForm from '@renderer/components/modules/eshop/EshopProductForm'

beforeEach(() => {
  vi.clearAllMocks()
  mockApi.createEshopProduct.mockResolvedValue({ product_id: 99 })
})

describe('EshopProductForm', () => {
  it('renders form with all fields for new product', () => {
    render(<EshopProductForm />)
    expect(screen.getByText('Nový produkt')).toBeInTheDocument()
    expect(screen.getByTestId('field-sku')).toBeInTheDocument()
    expect(screen.getByTestId('field-name')).toBeInTheDocument()
    expect(screen.getByTestId('field-price')).toBeInTheDocument()
    expect(screen.getByTestId('field-price-vat')).toBeInTheDocument()
    expect(screen.getByTestId('field-vat-rate')).toBeInTheDocument()
    expect(screen.getByTestId('field-stock')).toBeInTheDocument()
  })

  it('shows validation errors for required fields', async () => {
    render(<EshopProductForm />)
    fireEvent.click(screen.getByTestId('save-button'))
    await waitFor(() => {
      expect(screen.getByText('SKU je povinné')).toBeInTheDocument()
      expect(screen.getByText('Názov je povinný')).toBeInTheDocument()
    })
  })

  it('auto-calculates price_vat from price + vat_rate', async () => {
    render(<EshopProductForm />)
    const priceField = screen.getByTestId('field-price') as HTMLInputElement
    fireEvent.change(priceField, { target: { value: '100' } })
    await waitFor(() => {
      const priceVatField = screen.getByTestId('field-price-vat') as HTMLInputElement
      expect(priceVatField.value).toBe('120.00')
    })
  })

  it('calls createEshopProduct on valid submit', async () => {
    render(<EshopProductForm />)
    fireEvent.change(screen.getByTestId('field-sku'), { target: { value: 'NEW-001' } })
    fireEvent.change(screen.getByTestId('field-name'), { target: { value: 'Nový produkt' } })
    fireEvent.change(screen.getByTestId('field-price'), { target: { value: '100' } })
    // Wait for auto-calc
    await waitFor(() => {
      const vatField = screen.getByTestId('field-price-vat') as HTMLInputElement
      expect(vatField.value).toBe('120.00')
    })
    fireEvent.click(screen.getByTestId('save-button'))
    await waitFor(() => {
      expect(mockApi.createEshopProduct).toHaveBeenCalled()
    })
  })

  it('calls closeProductEdit when cancel button clicked', () => {
    render(<EshopProductForm />)
    fireEvent.click(screen.getByTestId('cancel-button'))
    expect(mockCloseProductEdit).toHaveBeenCalled()
  })
})
