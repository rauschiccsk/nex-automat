import apiClient from './client';
import { mockInvoices, mockStats, USE_MOCK_DATA } from './mockData';
import type { Invoice, InvoiceListResponse, InvoiceStats, InvoiceFilters } from '@/types/invoice';

// Get all invoices
export async function getInvoices(filters?: InvoiceFilters): Promise<InvoiceListResponse> {
  try {
    const params = new URLSearchParams();
    if (filters?.limit) params.append('limit', filters.limit.toString());

    const response = await apiClient.get<InvoiceListResponse>('/invoices', { params });

    // If backend returns empty or no invoices, use mock data in dev
    if (USE_MOCK_DATA && (!response.data.invoices || response.data.invoices.length === 0)) {
      console.log('[API] Using mock data - no real invoices found');
      return { count: mockInvoices.length, invoices: mockInvoices };
    }

    return response.data;
  } catch (error) {
    // Fallback to mock data in development
    if (USE_MOCK_DATA) {
      console.log('[API] Using mock data - backend error');
      return { count: mockInvoices.length, invoices: mockInvoices };
    }
    throw error;
  }
}

// Get invoice by ID
export async function getInvoice(id: number): Promise<Invoice | null> {
  try {
    // TODO: Backend endpoint not implemented yet
    // const response = await apiClient.get<Invoice>(`/invoices/${id}`);
    // return response.data;

    // For now, find in mock data
    if (USE_MOCK_DATA) {
      return mockInvoices.find(inv => inv.id === id) || null;
    }
    return null;
  } catch (error) {
    if (USE_MOCK_DATA) {
      return mockInvoices.find(inv => inv.id === id) || null;
    }
    throw error;
  }
}

// Get invoice statistics
export async function getStats(): Promise<InvoiceStats> {
  try {
    const response = await apiClient.get<InvoiceStats>('/stats');

    // If stats show 0 invoices, use mock stats in dev
    if (USE_MOCK_DATA && response.data.total_invoices === 0) {
      console.log('[API] Using mock stats');
      return mockStats;
    }

    return response.data;
  } catch (error) {
    if (USE_MOCK_DATA) {
      console.log('[API] Using mock stats - backend error');
      return mockStats;
    }
    throw error;
  }
}

// Get service status
export async function getStatus(): Promise<any> {
  const response = await apiClient.get('/status');
  return response.data;
}

// Health check
export async function getHealth(): Promise<{ status: string; timestamp: string }> {
  const response = await apiClient.get('/health');
  return response.data;
}

// Approve invoice (placeholder for future backend endpoint)
export async function approveInvoice(id: number, note?: string): Promise<Invoice> {
  // TODO: Implement when backend supports it
  // const response = await apiClient.put<Invoice>(`/invoices/${id}/approve`, { note });
  // return response.data;

  if (USE_MOCK_DATA) {
    const invoice = mockInvoices.find(inv => inv.id === id);
    if (invoice) {
      invoice.status = 'approved';
      invoice.updated_at = new Date().toISOString();
    }
    return invoice!;
  }
  throw new Error('Not implemented');
}

// Reject invoice (placeholder for future backend endpoint)
export async function rejectInvoice(id: number, reason: string): Promise<Invoice> {
  // TODO: Implement when backend supports it
  // const response = await apiClient.put<Invoice>(`/invoices/${id}/reject`, { reason });
  // return response.data;

  if (USE_MOCK_DATA) {
    const invoice = mockInvoices.find(inv => inv.id === id);
    if (invoice) {
      invoice.status = 'rejected';
      invoice.updated_at = new Date().toISOString();
    }
    return invoice!;
  }
  throw new Error('Not implemented');
}
