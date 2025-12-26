import apiClient from './client';
import { mockInvoices, mockStats, USE_MOCK_DATA } from './mockData';
import type { InvoiceHead, InvoiceListResponse, InvoiceStats, InvoiceFilters } from '@/types/invoice';

// Get all invoices
export async function getInvoices(filters?: InvoiceFilters): Promise<InvoiceListResponse> {
  try {
    const params = new URLSearchParams();
    if (filters?.limit) params.append('limit', filters.limit.toString());
    if (filters?.offset) params.append('offset', filters.offset.toString());
    if (filters?.status) params.append('status', filters.status);

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
export async function getInvoice(id: number): Promise<InvoiceHead | null> {
  try {
    const response = await apiClient.get<InvoiceHead>(`/invoices/${id}`);
    return response.data;
  } catch (error) {
    // Fallback to mock data in development
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
    if (USE_MOCK_DATA && response.data.total === 0) {
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
export async function getStatus(): Promise<{ status: string; version: string }> {
  const response = await apiClient.get('/status');
  return response.data;
}

// Health check
export async function getHealth(): Promise<{ status: string; timestamp: string }> {
  const response = await apiClient.get('/health');
  return response.data;
}

// Approve invoice
export async function approveInvoice(id: number): Promise<InvoiceHead> {
  try {
    const response = await apiClient.put<InvoiceHead>(`/invoices/${id}/approve`);
    return response.data;
  } catch (error) {
    if (USE_MOCK_DATA) {
      const invoice = mockInvoices.find(inv => inv.id === id);
      if (invoice) {
        invoice.status = 'approved';
        invoice.updated_at = new Date().toISOString();
      }
      return invoice!;
    }
    throw error;
  }
}

// Import invoice to NEX Genesis
export async function importInvoice(id: number): Promise<InvoiceHead> {
  try {
    const response = await apiClient.put<InvoiceHead>(`/invoices/${id}/import`);
    return response.data;
  } catch (error) {
    if (USE_MOCK_DATA) {
      const invoice = mockInvoices.find(inv => inv.id === id);
      if (invoice) {
        invoice.status = 'imported';
        invoice.imported_at = new Date().toISOString();
        invoice.updated_at = new Date().toISOString();
      }
      return invoice!;
    }
    throw error;
  }
}
