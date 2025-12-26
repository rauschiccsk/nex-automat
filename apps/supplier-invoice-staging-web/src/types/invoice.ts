// Invoice Types - based on FastAPI backend models

export type InvoiceStatus = 
  | 'received'
  | 'staged' 
  | 'pending_approval'
  | 'approved'
  | 'rejected'
  | 'processed'
  | 'error';

export type NexStatus = 
  | 'pending'
  | 'enriched'
  | 'imported'
  | 'error';

export interface InvoiceItem {
  id: number;
  invoice_id: number;
  line_number: number;
  original_name: string;
  edited_name?: string;
  quantity: number;
  unit: string;
  price_per_unit: number;
  original_ean?: string;
  edited_ean?: string;
  vat_rate: number;
  // NEX enrichment
  nex_gs_index?: number;
  nex_gs_name?: string;
  nex_matched_by?: string;
  nex_match_confidence?: number;
}

export interface Invoice {
  id: number;
  supplier_ico: string;
  supplier_name: string;
  supplier_dic?: string;
  invoice_number: string;
  invoice_date: string;
  due_date?: string;
  total_amount: number;
  total_vat?: number;
  total_without_vat?: number;
  currency: string;
  status: InvoiceStatus;
  nex_status: NexStatus;
  file_basename: string;
  file_status: string;
  pdf_file_path?: string;
  xml_file_path?: string;
  created_at: string;
  updated_at: string;
  items?: InvoiceItem[];
}

export interface InvoiceListResponse {
  count: number;
  invoices: Invoice[];
}

export interface InvoiceStats {
  total: number;
  total_invoices: number;
  by_status: Record<string, number>;
  by_nex_status: Record<string, number>;
  duplicates: number;
}

export interface InvoiceFilters {
  status?: InvoiceStatus;
  nex_status?: NexStatus;
  supplier_name?: string;
  date_from?: string;
  date_to?: string;
  search?: string;
  limit?: number;
}

// Status display configuration
export const STATUS_CONFIG: Record<InvoiceStatus, { label: string; color: string; icon: string }> = {
  received: { label: 'Prijatá', color: 'bg-gray-500', icon: '📥' },
  staged: { label: 'Pripravená', color: 'bg-blue-500', icon: '📄' },
  pending_approval: { label: 'Čaká na schválenie', color: 'bg-yellow-500', icon: '🟡' },
  approved: { label: 'Schválená', color: 'bg-green-500', icon: '✅' },
  rejected: { label: 'Zamietnutá', color: 'bg-red-500', icon: '❌' },
  processed: { label: 'Spracovaná', color: 'bg-purple-500', icon: '📤' },
  error: { label: 'Chyba', color: 'bg-red-700', icon: '⚠️' },
};

export const NEX_STATUS_CONFIG: Record<NexStatus, { label: string; color: string }> = {
  pending: { label: 'Čaká', color: 'bg-gray-500' },
  enriched: { label: 'Obohatená', color: 'bg-blue-500' },
  imported: { label: 'Importovaná', color: 'bg-green-500' },
  error: { label: 'Chyba', color: 'bg-red-500' },
};
