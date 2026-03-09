/**
 * Zustand store for ESHOP module UI state.
 */
import { create } from 'zustand'

export type EshopView =
  | 'orders'
  | 'order-detail'
  | 'products'
  | 'product-edit'
  | 'tenants'

interface EshopState {
  // View mode
  view: EshopView

  // Selected items
  selectedOrderId: number | null
  selectedProductId: number | null

  // Filters
  orderStatusFilter: string | null
  orderSearch: string
  productActiveFilter: boolean | null

  // Pagination
  ordersPage: number
  productsPage: number

  // Actions
  setView: (view: EshopView) => void
  setSelectedOrderId: (id: number | null) => void
  setSelectedProductId: (id: number | null) => void
  setOrderStatusFilter: (status: string | null) => void
  setOrderSearch: (search: string) => void
  setProductActiveFilter: (active: boolean | null) => void
  setOrdersPage: (page: number) => void
  setProductsPage: (page: number) => void

  // Navigation helpers
  openOrderDetail: (orderId: number) => void
  closeOrderDetail: () => void
  openProductEdit: (productId: number | null) => void
  closeProductEdit: () => void
  resetFilters: () => void
}

export const useEshopStore = create<EshopState>((set) => ({
  view: 'orders',
  selectedOrderId: null,
  selectedProductId: null,

  orderStatusFilter: null,
  orderSearch: '',
  productActiveFilter: null,

  ordersPage: 1,
  productsPage: 1,

  setView: (view): void => set({ view }),
  setSelectedOrderId: (id): void => set({ selectedOrderId: id }),
  setSelectedProductId: (id): void => set({ selectedProductId: id }),
  setOrderStatusFilter: (status): void => set({ orderStatusFilter: status, ordersPage: 1 }),
  setOrderSearch: (search): void => set({ orderSearch: search, ordersPage: 1 }),
  setProductActiveFilter: (active): void => set({ productActiveFilter: active, productsPage: 1 }),
  setOrdersPage: (page): void => set({ ordersPage: page }),
  setProductsPage: (page): void => set({ productsPage: page }),

  openOrderDetail: (orderId): void =>
    set({
      view: 'order-detail',
      selectedOrderId: orderId
    }),

  closeOrderDetail: (): void =>
    set({
      view: 'orders',
      selectedOrderId: null
    }),

  openProductEdit: (productId): void =>
    set({
      view: 'product-edit',
      selectedProductId: productId
    }),

  closeProductEdit: (): void =>
    set({
      view: 'products',
      selectedProductId: null
    }),

  resetFilters: (): void =>
    set({
      orderStatusFilter: null,
      orderSearch: '',
      productActiveFilter: null,
      ordersPage: 1,
      productsPage: 1
    })
}))
