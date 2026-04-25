/**
 * Types for partner management module (PAB).
 * Matches API schemas from nex-manager-api/partners/schemas.py
 *
 * IMPORTANT: Backend uses `name` (not `partner_name`).
 */

export type PartnerType = 'customer' | 'supplier' | 'both'
export type PaymentMethod = 'transfer' | 'cash' | 'cod'
export type SortField = 'code' | 'name' | 'city' | 'created_at'
export type SortOrder = 'asc' | 'desc'

export interface Partner {
  id: string // UUID
  code: string
  name: string // Backend: `name` (nie partner_name)

  // Typ
  partner_type: PartnerType
  is_customer: boolean
  is_supplier: boolean

  // Identifikácia
  company_id: string | null // IČO
  tax_id: string | null // DIČ
  vat_id: string | null // IČ DPH
  is_vat_payer: boolean

  // Sídlo
  street: string | null
  city: string | null
  zip_code: string | null
  country_code: string | null

  // Fakturačná adresa
  billing_street: string | null
  billing_city: string | null
  billing_zip_code: string | null
  billing_country_code: string | null

  // Dodacia adresa
  shipping_street: string | null
  shipping_city: string | null
  shipping_zip_code: string | null
  shipping_country_code: string | null

  // Kontakt
  phone: string | null
  mobile: string | null
  email: string | null
  website: string | null
  contact_person: string | null

  // Obchodné podmienky
  payment_due_days: number
  credit_limit: number
  discount_percent: number
  price_category: string | null
  payment_method: PaymentMethod
  currency: string

  // Banka
  iban: string | null
  bank_name: string | null
  swift_bic: string | null

  // Poznámky
  notes: string | null

  // System
  is_active: boolean
  created_at: string
  updated_at: string

  // Backend warnings (e.g. duplicate IČO)
  warnings?: string[] | null
}

export interface PartnerCreate {
  code: string
  name: string
  partner_type?: PartnerType
  company_id?: string
  tax_id?: string
  vat_id?: string
  is_vat_payer?: boolean
  street?: string
  city?: string
  zip_code?: string
  country_code?: string
  billing_street?: string
  billing_city?: string
  billing_zip_code?: string
  billing_country_code?: string
  shipping_street?: string
  shipping_city?: string
  shipping_zip_code?: string
  shipping_country_code?: string
  phone?: string
  mobile?: string
  email?: string
  website?: string
  contact_person?: string
  payment_due_days?: number
  credit_limit?: number
  discount_percent?: number
  price_category?: string
  payment_method?: PaymentMethod
  currency?: string
  iban?: string
  bank_name?: string
  swift_bic?: string
  notes?: string
  is_active?: boolean
}

export type PartnerUpdate = Partial<Omit<PartnerCreate, 'code'>>

export interface PartnerListResponse {
  items: Partner[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface PartnerListParams {
  partner_type?: PartnerType
  is_active?: boolean
  search?: string
  page?: number
  page_size?: number
  sort_by?: SortField
  sort_order?: SortOrder
}
