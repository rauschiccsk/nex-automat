import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'

const mockOrderDetail = {
  order_id: 1,
  order_number: 'ICC-2025-0001',
  tenant_id: 1,
  customer_name: 'Ján Novák',
  customer_email: 'jan@example.com',
  customer_phone: '+421901234567',
  lang: 'sk',
  billing_name: 'Ján Novák',
  billing_name2: '',
  billing_street: 'Hlavná 15',
  billing_city: 'Bratislava',
  billing_zip: '81101',
  billing_country: 'SK',
  shipping_name: 'Ján Novák',
  shipping_name2: '',
  shipping_street: 'Košická 42',
  shipping_city: 'Košice',
  shipping_zip: '04001',
  shipping_country: 'SK',
  ico: '12345678',
  dic: '2012345678',
  eu_vat_number: '',
  total_amount: 49.99,
  total_amount_vat: 59.99,
  currency: 'EUR',
  payment_method: 'credit_card',
  payment_status: 'paid',
  comgate_transaction_id: 'TXN-123',
  shipping_type: 'courier',
  shipping_price: 0,
  delivery_point_group: '',
  delivery_point_id: '',
  tracking_number: 'SK1234567890',
  tracking_link: 'https://tracking.example.com/SK1234567890',
  multiple_packages: false,
  status: 'shipped',
  note: 'Prosím doručiť poobede',
  created_at: '2025-01-15T10:00:00Z',
  updated_at: '2025-01-16T14:30:00Z',
  items: [
    { sku: 'PROD-001', name: 'Testovací produkt', quantity: 2, unit_price_vat: 24.99, vat_rate: 20 },
    { sku: 'PROD-002', name: 'Druhý produkt', quantity: 1, unit_price_vat: 10.01, vat_rate: 20 },
  ],
  status_history: [
    { old_status: null, new_status: 'new', changed_by: 'system', note: '', created_at: '2025-01-15T10:00:00Z' },
    { old_status: 'new', new_status: 'paid', changed_by: 'comgate', note: '', created_at: '2025-01-15T10:05:00Z' },
    { old_status: 'paid', new_status: 'shipped', changed_by: 'admin', note: 'Odoslané', created_at: '2025-01-16T14:30:00Z' },
  ],
}

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
const mockCloseOrderDetail = vi.fn()

vi.mock('@renderer/stores/eshopStore', () => ({
  useEshopStore: () => ({
    selectedOrderId: 1,
    closeOrderDetail: mockCloseOrderDetail,
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

import EshopOrderDetail from '@renderer/components/modules/eshop/EshopOrderDetail'

beforeEach(() => {
  vi.clearAllMocks()
  mockApi.getEshopOrderDetail.mockResolvedValue(mockOrderDetail)
})

describe('EshopOrderDetail', () => {
  it('renders order header with order number and badges', async () => {
    render(<EshopOrderDetail />)
    await waitFor(() => {
      expect(screen.getByText(/ICC-2025-0001/)).toBeInTheDocument()
    })
    // Status badges
    const badges = screen.getAllByTestId('order-status-badge')
    expect(badges.length).toBeGreaterThanOrEqual(1)
  })

  it('displays customer info (name, email, phone)', async () => {
    render(<EshopOrderDetail />)
    await waitFor(() => {
      expect(screen.getByTestId('customer-name')).toHaveTextContent('Ján Novák')
    })
    expect(screen.getByTestId('customer-email')).toHaveTextContent('jan@example.com')
    expect(screen.getByText('+421901234567')).toBeInTheDocument()
  })

  it('displays billing address', async () => {
    render(<EshopOrderDetail />)
    await waitFor(() => {
      expect(screen.getByTestId('billing-address')).toBeInTheDocument()
    })
    const billing = screen.getByTestId('billing-address')
    expect(billing).toHaveTextContent('Hlavná 15')
    expect(billing).toHaveTextContent('Bratislava')
  })

  it('displays shipping address', async () => {
    render(<EshopOrderDetail />)
    await waitFor(() => {
      expect(screen.getByTestId('shipping-address')).toBeInTheDocument()
    })
    const shipping = screen.getByTestId('shipping-address')
    expect(shipping).toHaveTextContent('Košická 42')
    expect(shipping).toHaveTextContent('Košice')
  })

  it('displays order items table', async () => {
    render(<EshopOrderDetail />)
    await waitFor(() => {
      expect(screen.getByTestId('order-items-table')).toBeInTheDocument()
    })
    expect(screen.getByText('Testovací produkt')).toBeInTheDocument()
    expect(screen.getByText('Druhý produkt')).toBeInTheDocument()
    expect(screen.getByText('PROD-001')).toBeInTheDocument()
  })

  it('displays order total', async () => {
    render(<EshopOrderDetail />)
    await waitFor(() => {
      expect(screen.getByTestId('order-total')).toBeInTheDocument()
    })
    expect(screen.getByTestId('order-total')).toHaveTextContent('59.99 EUR')
  })

  it('displays status history timeline', async () => {
    render(<EshopOrderDetail />)
    await waitFor(() => {
      expect(screen.getByTestId('status-history')).toBeInTheDocument()
    })
    expect(screen.getByText(/new → paid/)).toBeInTheDocument()
    expect(screen.getByText(/paid → shipped/)).toBeInTheDocument()
  })

  it('calls closeOrderDetail when back button clicked', async () => {
    render(<EshopOrderDetail />)
    await waitFor(() => {
      expect(screen.getByTestId('back-button')).toBeInTheDocument()
    })
    fireEvent.click(screen.getByTestId('back-button'))
    expect(mockCloseOrderDetail).toHaveBeenCalled()
  })
})
