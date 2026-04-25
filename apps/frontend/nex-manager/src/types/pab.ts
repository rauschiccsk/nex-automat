/**
 * Types for PAB (Partner Catalog) module.
 * Matches API schemas from nex-manager-api/pab/schemas.py
 *
 * Uses /api/pab/partners endpoints with INTEGER partner_id,
 * 8-table model, and version history.
 */

// ---------------------------------------------------------------------------
// Enums / Literals
// ---------------------------------------------------------------------------

export type PartnerClass = 'business' | 'retail' | 'guest'
export type AddressType = 'registered' | 'correspondence' | 'invoice'
export type ContactType = 'address' | 'person'
export type CategoryType = 'supplier' | 'customer'
export type TextType = 'owner_name' | 'description' | 'notice'
export type PabSortField = 'partner_id' | 'partner_name' | 'city' | 'created_at'
export type SortOrder = 'asc' | 'desc'

// ---------------------------------------------------------------------------
// Partner Catalog — main table
// ---------------------------------------------------------------------------

export interface PartnerCatalog {
  partner_id: number
  partner_name: string
  reg_name: string | null

  company_id: string | null // ICO
  tax_id: string | null // DIC
  vat_id: string | null // IC DPH
  is_vat_payer: boolean

  is_supplier: boolean
  is_customer: boolean

  street: string | null
  city: string | null
  zip_code: string | null
  country_code: string | null

  partner_class: PartnerClass
  modify_id: number

  bank_account_count: number
  facility_count: number

  is_active: boolean
  created_at: string
  updated_at: string

  // Aggregated child data (only in detail endpoint)
  extensions?: PartnerExtensions | null
  addresses?: PartnerAddress[] | null
  contacts?: PartnerContact[] | null
  texts?: PartnerText[] | null
  bank_accounts?: PartnerBankAccount[] | null
  facilities?: PartnerFacility[] | null
  categories?: PartnerCategoryMapping[] | null
}

export interface PartnerCatalogCreate {
  partner_id: number
  partner_name: string
  reg_name?: string
  company_id?: string
  tax_id?: string
  vat_id?: string
  is_vat_payer?: boolean
  is_supplier?: boolean
  is_customer?: boolean
  street?: string
  city?: string
  zip_code?: string
  country_code?: string
  partner_class?: PartnerClass
  is_active?: boolean
}

export interface PartnerCatalogUpdate {
  partner_name?: string
  reg_name?: string
  company_id?: string
  tax_id?: string
  vat_id?: string
  is_vat_payer?: boolean
  is_supplier?: boolean
  is_customer?: boolean
  street?: string
  city?: string
  zip_code?: string
  country_code?: string
  partner_class?: PartnerClass
  is_active?: boolean
}

export interface PartnerCatalogListResponse {
  items: PartnerCatalog[]
  total: number
  limit: number
  offset: number
}

export interface PartnerListParams {
  search?: string
  partner_class?: PartnerClass
  is_active?: boolean
  is_supplier?: boolean
  is_customer?: boolean
  limit?: number
  offset?: number
  sort_by?: PabSortField
  sort_order?: SortOrder
}

// ---------------------------------------------------------------------------
// Extensions (1:1)
// ---------------------------------------------------------------------------

export interface PartnerExtensions {
  partner_id: number
  sale_payment_method_id: number | null
  sale_transport_method_id: number | null
  sale_payment_due_days: number | null
  sale_currency_code: string | null
  sale_price_category: string | null
  sale_discount_percent: number | null
  sale_credit_limit: number | null

  purchase_payment_method_id: number | null
  purchase_transport_method_id: number | null
  purchase_payment_due_days: number | null
  purchase_currency_code: string | null
  purchase_price_category: string | null
  purchase_discount_percent: number | null

  last_sale_date: string | null
  last_purchase_date: string | null

  is_active: boolean
  created_at: string | null
  updated_at: string | null
}

export interface PartnerExtensionsUpsert {
  sale_payment_method_id?: number | null
  sale_transport_method_id?: number | null
  sale_payment_due_days?: number
  sale_currency_code?: string
  sale_price_category?: string | null
  sale_discount_percent?: number
  sale_credit_limit?: number

  purchase_payment_method_id?: number | null
  purchase_transport_method_id?: number | null
  purchase_payment_due_days?: number
  purchase_currency_code?: string
  purchase_price_category?: string | null
  purchase_discount_percent?: number

  last_sale_date?: string | null
  last_purchase_date?: string | null
}

// ---------------------------------------------------------------------------
// Addresses
// ---------------------------------------------------------------------------

export interface PartnerAddress {
  id: number
  partner_id: number
  address_type: AddressType
  street: string | null
  city: string | null
  zip_code: string | null
  country_code: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface PartnerAddressCreate {
  address_type: AddressType
  street?: string
  city?: string
  zip_code?: string
  country_code?: string
}

export interface PartnerAddressUpdate {
  street?: string
  city?: string
  zip_code?: string
  country_code?: string
}

// ---------------------------------------------------------------------------
// Contacts
// ---------------------------------------------------------------------------

export interface PartnerContact {
  contact_id: number
  partner_id: number
  contact_type: ContactType
  title: string | null
  first_name: string | null
  last_name: string | null
  function_name: string | null
  phone_work: string | null
  phone_mobile: string | null
  phone_private: string | null
  fax: string | null
  email: string | null
  street: string | null
  city: string | null
  zip_code: string | null
  country_code: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface PartnerContactCreate {
  contact_type: ContactType
  title?: string
  first_name?: string
  last_name?: string
  function_name?: string
  phone_work?: string
  phone_mobile?: string
  phone_private?: string
  fax?: string
  email?: string
  street?: string
  city?: string
  zip_code?: string
  country_code?: string
}

export interface PartnerContactUpdate {
  title?: string
  first_name?: string
  last_name?: string
  function_name?: string
  phone_work?: string
  phone_mobile?: string
  phone_private?: string
  fax?: string
  email?: string
  street?: string
  city?: string
  zip_code?: string
  country_code?: string
}

// ---------------------------------------------------------------------------
// Bank Accounts
// ---------------------------------------------------------------------------

export interface PartnerBankAccount {
  account_id: number
  partner_id: number
  iban_code: string | null
  swift_code: string | null
  account_number: string | null
  bank_name: string | null
  bank_seat: string | null
  vs_sale: string | null
  vs_purchase: string | null
  is_primary: boolean
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface PartnerBankAccountCreate {
  iban_code?: string
  swift_code?: string
  account_number?: string
  bank_name?: string
  bank_seat?: string
  vs_sale?: string
  vs_purchase?: string
  is_primary?: boolean
}

export interface PartnerBankAccountUpdate {
  iban_code?: string
  swift_code?: string
  account_number?: string
  bank_name?: string
  bank_seat?: string
  vs_sale?: string
  vs_purchase?: string
  is_primary?: boolean
}

// ---------------------------------------------------------------------------
// Categories (M:N)
// ---------------------------------------------------------------------------

export interface PartnerCategoryMapping {
  id: number
  partner_id: number
  category_id: number
  category_type: CategoryType
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface PartnerCategoryAssign {
  category_id: number
  category_type: CategoryType
}

// ---------------------------------------------------------------------------
// Texts
// ---------------------------------------------------------------------------

export interface PartnerText {
  text_id: number
  partner_id: number
  text_type: TextType
  line_number: number
  language: string
  text_content: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface PartnerTextUpsert {
  text_type: TextType
  line_number?: number
  language?: string
  text_content?: string | null
}

// ---------------------------------------------------------------------------
// Facilities
// ---------------------------------------------------------------------------

export interface PartnerFacility {
  facility_id: number
  partner_id: number
  facility_name: string
  street: string | null
  city: string | null
  zip_code: string | null
  country_code: string | null
  phone: string | null
  fax: string | null
  email: string | null
  transport_method_id: number | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface PartnerFacilityCreate {
  facility_name: string
  street?: string
  city?: string
  zip_code?: string
  country_code?: string
  phone?: string
  fax?: string
  email?: string
  transport_method_id?: number
}

export interface PartnerFacilityUpdate {
  facility_name?: string
  street?: string
  city?: string
  zip_code?: string
  country_code?: string
  phone?: string
  fax?: string
  email?: string
  transport_method_id?: number
}

// ---------------------------------------------------------------------------
// History (versioning)
// ---------------------------------------------------------------------------

export interface PartnerHistory {
  history_id: number
  partner_id: number
  modify_id: number

  partner_name: string
  reg_name: string | null

  company_id: string | null
  tax_id: string | null
  vat_id: string | null
  is_vat_payer: boolean

  is_supplier: boolean
  is_customer: boolean

  street: string | null
  city: string | null
  zip_code: string | null
  country_code: string | null

  partner_class: PartnerClass

  valid_from: string
  valid_to: string | null
  changed_by: string | null
}
