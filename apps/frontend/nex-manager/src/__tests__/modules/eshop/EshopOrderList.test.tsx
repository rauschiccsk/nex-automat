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
const mockOrders = [
  {
    order_id: 1,
    order_number: 'ICC-2025-0001',
    customer_name: 'Ján Novák',
    customer_email: 'jan@example.com',
    total_amount_vat: 59.99,
    currency: 'EUR',
    status: 'new',
    payment_status: 'pending',
    created_at: '2025-01-15T10:00:00Z',
    updated_at: '2025-01-15T10:00:00Z',
  },
  {
    order_id: 2,
    order_number: 'ICC-2025-0002',
    customer_name: 'Peter Horváth',
    customer_email: 'peter@example.com',
    total_amount_vat: 129.50,
    currency: 'EUR',
    status: 'paid',
    payment_status: 'paid',
    created_at: '2025-01-16T14:30:00Z',
    updated_at: '2025-01-16T14:30:00Z',
  },
  {
    order_id: 3,
    order_number: 'ICC-2025-0003',
    customer_name: 'Mária Kováčová',
    customer_email: 'maria@example.com',
    total_amount_vat: 45.00,
    currency: 'EUR',
    status: 'shipped',
    payment_status: 'paid',
    created_at: '2025-01-17T09:15:00Z',
    updated_at: '2025-01-17T09:15:00Z',
  },
]

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
const mockOpenOrderDetail = vi.fn()
const mockSetOrderStatusFilter = vi.fn()
const mockSetOrderSearch = vi.fn()
const mockSetOrdersPage = vi.fn()

vi.mock('@renderer/stores/eshopStore', () => ({
  useEshopStore: () => ({
    orderStatusFilter: null,
    setOrderStatusFilter: mockSetOrderStatusFilter,
    orderSearch: '',
    setOrderSearch: mockSetOrderSearch,
    ordersPage: 1,
    setOrdersPage: mockSetOrdersPage,
    openOrderDetail: mockOpenOrderDetail,
  }),
}))

const mockAddToast = vi.fn()
vi.mock('@renderer/stores/toastStore', () => ({
  useToastStore: () => ({
    addToast: mockAddToast,
  }),
}))

import EshopOrderList from '@renderer/components/modules/eshop/EshopOrderList'

beforeEach(() => {
  vi.clearAllMocks()
  localStorage.clear()
  mockApi.getEshopOrders.mockResolvedValue({
    orders: mockOrders,
    total: mockOrders.length,
    page: 1,
    page_size: 20,
  })
})

describe('EshopOrderList', () => {
  it('renders heading "Objednávky"', async () => {
    render(<EshopOrderList />)
    expect(screen.getByText('Objednávky')).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    mockApi.getEshopOrders.mockReturnValue(new Promise(() => {}))
    render(<EshopOrderList />)
    expect(screen.getByText('Načítavam...')).toBeInTheDocument()
  })

  it('fetches and displays order data', async () => {
    render(<EshopOrderList />)
    await waitFor(() => {
      expect(screen.getByText('ICC-2025-0001')).toBeInTheDocument()
    })
    expect(screen.getByText('Ján Novák')).toBeInTheDocument()
    expect(screen.getByText('Peter Horváth')).toBeInTheDocument()
    expect(mockApi.getEshopOrders).toHaveBeenCalled()
  })

  it('shows total order count', async () => {
    render(<EshopOrderList />)
    await waitFor(() => {
      expect(screen.getByText(/Celkom: 3 objednávok/)).toBeInTheDocument()
    })
  })

  it('renders status filter dropdown', async () => {
    render(<EshopOrderList />)
    expect(screen.getByText('Všetky stavy')).toBeInTheDocument()
  })

  it('renders search input with placeholder', async () => {
    render(<EshopOrderList />)
    expect(screen.getByPlaceholderText('Hľadať objednávku...')).toBeInTheDocument()
  })

  it('shows error state on API failure', async () => {
    mockApi.getEshopOrders.mockRejectedValue(new Error('Network error'))
    render(<EshopOrderList />)
    await waitFor(() => {
      expect(screen.getByText('Network error')).toBeInTheDocument()
    })
  })

  it('shows retry button on error and retries when clicked', async () => {
    mockApi.getEshopOrders.mockRejectedValueOnce(new Error('Chyba'))
    render(<EshopOrderList />)
    await waitFor(() => {
      expect(screen.getByText('Skúsiť znova')).toBeInTheDocument()
    })
    mockApi.getEshopOrders.mockResolvedValueOnce({ orders: mockOrders, total: 3, page: 1, page_size: 20 })
    fireEvent.click(screen.getByText('Skúsiť znova'))
    expect(mockApi.getEshopOrders).toHaveBeenCalledTimes(2)
  })
})
