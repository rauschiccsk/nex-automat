import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'

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

const mockProducts = [
  {
    product_id: 1,
    tenant_id: 1,
    sku: 'PROD-001',
    barcode: '8591234567890',
    name: 'Zimná pneumatika 205/55 R16',
    short_description: 'Zimná pneumatika',
    description: 'Zimná pneumatika pre osobné vozidlá',
    image_url: null,
    price: 49.99,
    price_vat: 59.99,
    vat_rate: 20,
    stock_quantity: 100,
    weight: 8.5,
    is_active: true,
    sort_order: 1,
    created_at: '2025-01-10T10:00:00Z',
    updated_at: '2025-01-10T10:00:00Z',
  },
  {
    product_id: 2,
    tenant_id: 1,
    sku: 'PROD-002',
    barcode: null,
    name: 'Letná pneumatika 195/65 R15',
    short_description: 'Letná pneumatika',
    description: null,
    image_url: null,
    price: 39.99,
    price_vat: 47.99,
    vat_rate: 20,
    stock_quantity: 50,
    weight: 7.2,
    is_active: true,
    sort_order: 2,
    created_at: '2025-01-11T10:00:00Z',
    updated_at: '2025-01-11T10:00:00Z',
  },
  {
    product_id: 3,
    tenant_id: 1,
    sku: 'PROD-003',
    barcode: null,
    name: 'Celoročná pneumatika',
    short_description: null,
    description: null,
    image_url: null,
    price: 55.00,
    price_vat: 66.00,
    vat_rate: 20,
    stock_quantity: 0,
    weight: null,
    is_active: false,
    sort_order: 3,
    created_at: '2025-01-12T10:00:00Z',
    updated_at: '2025-01-12T10:00:00Z',
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
const mockOpenProductEdit = vi.fn()
const mockSetProductActiveFilter = vi.fn()
const mockSetProductsPage = vi.fn()

vi.mock('@renderer/stores/eshopStore', () => ({
  useEshopStore: () => ({
    productActiveFilter: null,
    setProductActiveFilter: mockSetProductActiveFilter,
    productsPage: 1,
    setProductsPage: mockSetProductsPage,
    openProductEdit: mockOpenProductEdit,
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

import EshopProductList from '@renderer/components/modules/eshop/EshopProductList'

beforeEach(() => {
  vi.clearAllMocks()
  localStorage.clear()
  mockApi.getEshopProducts.mockResolvedValue({
    products: mockProducts,
    total: mockProducts.length,
    page: 1,
    page_size: 20,
  })
})

describe('EshopProductList', () => {
  it('renders heading "Produkty"', async () => {
    render(<EshopProductList />)
    expect(screen.getByText('Produkty')).toBeInTheDocument()
  })

  it('fetches and displays product data', async () => {
    render(<EshopProductList />)
    await waitFor(() => {
      expect(screen.getByText('Zimná pneumatika 205/55 R16')).toBeInTheDocument()
    })
    expect(screen.getByText('Letná pneumatika 195/65 R15')).toBeInTheDocument()
    expect(mockApi.getEshopProducts).toHaveBeenCalled()
  })

  it('renders "Nový produkt" create button', async () => {
    render(<EshopProductList />)
    expect(screen.getByText('Nový produkt')).toBeInTheDocument()
  })

  it('renders active/inactive filter dropdown', async () => {
    render(<EshopProductList />)
    expect(screen.getByTestId('product-active-filter')).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    mockApi.getEshopProducts.mockReturnValue(new Promise(() => {}))
    render(<EshopProductList />)
    expect(screen.getByText('Načítavam...')).toBeInTheDocument()
  })

  it('shows error state on API failure', async () => {
    mockApi.getEshopProducts.mockRejectedValue(new Error('Chyba siete'))
    render(<EshopProductList />)
    await waitFor(() => {
      expect(screen.getByText('Chyba siete')).toBeInTheDocument()
    })
    expect(screen.getByText('Skúsiť znova')).toBeInTheDocument()
  })
})
