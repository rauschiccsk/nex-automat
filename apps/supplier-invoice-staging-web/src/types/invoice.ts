// Invoice Types - based on supplier_invoice_staging DB schema
// Convention: xml_* = from ISDOC XML (immutable), nex_* = from NEX Genesis (enrichment)

export type InvoiceStatus = 'pending' | 'matched' | 'approved' | 'imported';

export type ValidationStatus = 'valid' | 'warning' | 'error';

export type MatchMethod = 'ean' | 'name' | 'code' | 'manual';

// =============================================================================
// supplier_invoice_heads
// =============================================================================
export interface InvoiceHead {
  id: number;

  // XML fields (from ISDOC - immutable)
  xml_invoice_number: string;
  xml_variable_symbol?: string;
  xml_issue_date: string;
  xml_tax_point_date?: string;
  xml_due_date?: string;
  xml_currency: string;
  xml_supplier_ico: string;
  xml_supplier_name: string;
  xml_supplier_dic?: string;
  xml_supplier_ic_dph?: string;
  xml_iban?: string;
  xml_swift?: string;
  xml_total_without_vat: number;
  xml_total_vat: number;
  xml_total_with_vat: number;

  // NEX fields (enrichment from NEX Genesis)
  nex_supplier_id?: number;
  nex_supplier_modify_id?: number;
  nex_iban?: string;
  nex_swift?: string;
  nex_stock_id?: number;
  nex_book_num?: number;
  nex_payment_method_id?: number;
  nex_price_list_id?: number;

  // Workflow
  status: InvoiceStatus;
  item_count: number;
  items_matched: number;
  match_percent: number;

  // Validation
  validation_status?: ValidationStatus;
  validation_errors?: string;

  // Files
  xml_file_path?: string;
  pdf_file_path?: string;

  // Timestamps
  created_at: string;
  updated_at: string;
  processed_at?: string;
  imported_at?: string;

  // After import
  nex_document_id?: number;

  // Joined data (optional)
  items?: InvoiceItem[];
}

// =============================================================================
// supplier_invoice_items
// =============================================================================
export interface InvoiceItem {
  id: number;
  invoice_head_id: number;

  // XML fields (from ISDOC - immutable)
  xml_line_number: number;
  xml_product_name: string;
  xml_seller_code?: string;
  xml_ean?: string;
  xml_quantity: number;
  xml_unit: string;
  xml_unit_price: number;
  xml_total_price: number;
  xml_unit_price_vat?: number;
  xml_total_price_vat?: number;
  xml_vat_rate: number;

  // NEX fields (enrichment from NEX Genesis)
  nex_product_id?: number;
  nex_product_modify_id?: number;
  nex_product_name?: string;
  nex_product_category_id?: number;
  nex_ean?: string;
  nex_stock_code?: string;
  nex_stock_id?: number;
  nex_facility_id?: number;
  nex_purchase_price?: number;
  nex_sales_price?: number;
  nex_margin_percent?: number;  // NEW: Obchodná marža v %

  // Matching
  matched: boolean;
  matched_by?: MatchMethod;
  match_confidence?: number;
  match_attempts?: number;

  // Validation
  validation_status?: ValidationStatus;
  validation_errors?: string;

  // User edits
  edited_product_name?: string;
  edited_quantity?: number;
  edited_unit_price?: number;

  // Timestamps
  created_at: string;
  updated_at: string;
  matched_at?: string;
  matched_by_user?: string;
}

// =============================================================================
// API Response types
// =============================================================================
export interface InvoiceListResponse {
  count: number;
  invoices: InvoiceHead[];
}

export interface InvoiceDetailResponse {
  invoice: InvoiceHead;
  items: InvoiceItem[];
}

export interface InvoiceStats {
  total: number;
  by_status: Record<InvoiceStatus, number>;
  total_amount: number;
  avg_match_percent: number;
}

// =============================================================================
// Filter types
// =============================================================================
export interface InvoiceFilters {
  status?: InvoiceStatus;
  xml_supplier_ico?: string;
  xml_supplier_name?: string;
  date_from?: string;
  date_to?: string;
  search?: string;
  limit?: number;
  offset?: number;
}

// =============================================================================
// Status display configuration
// =============================================================================
export const STATUS_CONFIG: Record<string, { label: string; color: string; bgClass: string }> = {
  staged: { label: 'Nová', color: 'text-orange-600', bgClass: 'bg-orange-100' },
  pending: { label: 'Čaká', color: 'text-gray-600', bgClass: 'bg-gray-100' },
  matched: { label: 'Spárovaná', color: 'text-blue-600', bgClass: 'bg-blue-100' },
  approved: { label: 'Schválená', color: 'text-green-600', bgClass: 'bg-green-100' },
  imported: { label: 'Importovaná', color: 'text-purple-600', bgClass: 'bg-purple-100' },
};

export const VALIDATION_STATUS_CONFIG: Record<ValidationStatus, { label: string; color: string }> = {
  valid: { label: 'OK', color: 'text-green-600' },
  warning: { label: 'Varovanie', color: 'text-yellow-600' },
  error: { label: 'Chyba', color: 'text-red-600' },
};

export const MATCH_METHOD_CONFIG: Record<MatchMethod, { label: string }> = {
  ean: { label: 'EAN' },
  name: { label: 'Názov' },
  code: { label: 'Kód' },
  manual: { label: 'Manuálne' },
};
