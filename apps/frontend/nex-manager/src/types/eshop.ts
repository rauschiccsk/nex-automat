/**
 * ESHOP module TypeScript types — matching backend schemas.py exactly.
 */

// ============================================================================
// Admin — Orders
// ============================================================================

/** Admin order list item (matches AdminOrderListItem). */
export interface EshopOrder {
  order_id: number
  order_number: string
  customer_name: string
  customer_email: string
  total_amount_vat: number
  currency: string
  status: EshopOrderStatus
  payment_status: EshopPaymentStatus
  created_at: string
  updated_at: string
}

/** Admin order list response (matches AdminOrderListResponse). */
export interface EshopOrderListResponse {
  orders: EshopOrder[]
  total: number
  page: number
  page_size: number
}

/** Order item (matches OrderItemResponse). */
export interface EshopOrderItem {
  sku: string
  name: string
  quantity: number
  unit_price_vat: number
  vat_rate: number
}

/** Status history entry (matches AdminStatusHistoryItem). */
export interface EshopOrderStatusHistory {
  old_status: string | null
  new_status: string
  changed_by: string | null
  note: string
  created_at: string
}

/** Admin order detail (matches AdminOrderDetailResponse). */
export interface EshopOrderDetail extends EshopOrder {
  tenant_id: number
  customer_phone: string | null
  lang: string
  billing_name: string
  billing_name2: string
  billing_street: string
  billing_city: string
  billing_zip: string
  billing_country: string
  shipping_name: string
  shipping_name2: string
  shipping_street: string
  shipping_city: string
  shipping_zip: string
  shipping_country: string
  ico: string
  dic: string
  eu_vat_number: string
  total_amount: number
  payment_method: string | null
  comgate_transaction_id: string | null
  shipping_type: string
  shipping_price: number
  delivery_point_group: string
  delivery_point_id: string
  tracking_number: string
  tracking_link: string
  multiple_packages: boolean
  note: string
  items: EshopOrderItem[]
  status_history: EshopOrderStatusHistory[]
}

/** Admin order update request (matches AdminOrderUpdateRequest). */
export interface EshopOrderUpdateRequest {
  status?: string
  note?: string
}

// ============================================================================
// Admin — Products
// ============================================================================

/** Admin product (matches admin_list_products response shape). */
export interface EshopProduct {
  product_id: number
  tenant_id: number
  sku: string
  barcode: string | null
  name: string
  short_description: string | null
  description: string | null
  image_url: string | null
  price: number
  price_vat: number
  vat_rate: number
  stock_quantity: number
  weight: number | null
  is_active: boolean
  sort_order: number
  created_at: string | null
  updated_at: string | null
}

/** Admin product list response. */
export interface EshopProductListResponse {
  products: EshopProduct[]
  total: number
  page: number
  page_size: number
}

/** Admin product create request (matches AdminProductCreateRequest). */
export interface EshopProductCreateRequest {
  sku: string
  name: string
  barcode?: string | null
  short_description?: string | null
  description?: string | null
  image_url?: string | null
  price: number
  price_vat: number
  vat_rate: number
  stock_quantity?: number
  weight?: number | null
  is_active?: boolean
  sort_order?: number
}

/** Admin product update request (matches AdminProductUpdateRequest). */
export interface EshopProductUpdateRequest {
  sku?: string
  name?: string
  barcode?: string | null
  short_description?: string | null
  description?: string | null
  image_url?: string | null
  price?: number
  price_vat?: number
  vat_rate?: number
  stock_quantity?: number
  weight?: number | null
  is_active?: boolean
  sort_order?: number
}

// ============================================================================
// Admin — Tenants
// ============================================================================

/** Admin tenant response (matches AdminTenantResponse — no secrets). */
export interface EshopTenant {
  tenant_id: number
  company_name: string
  domain: string
  brand_name: string
  logo_url: string | null
  primary_color: string | null
  currency: string
  vat_rate_default: number
  default_lang: string
  is_active: boolean
  created_at: string
}

/** Tenant list response. */
export interface EshopTenantListResponse {
  tenants: EshopTenant[]
}

// ============================================================================
// Enums
// ============================================================================

export type EshopOrderStatus =
  | 'new'
  | 'paid'
  | 'processing'
  | 'shipped'
  | 'delivered'
  | 'cancelled'
  | 'returned'

export type EshopPaymentStatus =
  | 'pending'
  | 'paid'
  | 'failed'
  | 'authorized'
