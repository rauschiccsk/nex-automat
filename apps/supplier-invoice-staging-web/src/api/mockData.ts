import type { Invoice, InvoiceItem, InvoiceStats } from '@/types/invoice';

// Suppliers for generating mock data
const suppliers = [
  { ico: '35850370', name: 'L&Š Slovakia s.r.o.', dic: '2021749064' },
  { ico: '44556677', name: 'METRO Cash & Carry SK', dic: '2022889900' },
  { ico: '12345678', name: 'Bidvest Slovakia s.r.o.', dic: '2020123456' },
  { ico: '98765432', name: 'Kofola a.s.', dic: '2019876543' },
  { ico: '55667788', name: 'Heineken Slovensko', dic: '2055667788' },
  { ico: '11223344', name: 'Nestlé Slovensko s.r.o.', dic: '2011223344' },
  { ico: '33445566', name: 'Coca-Cola HBC Slovensko', dic: '2033445566' },
  { ico: '77889900', name: 'Unilever Slovensko', dic: '2077889900' },
  { ico: '22334455', name: 'Makro Cash & Carry', dic: '2022334455' },
  { ico: '66778899', name: 'CBA Slovakia', dic: '2066778899' },
];

const products = [
  { name: 'Coca-Cola 2L', ean: '5449000000996', unit: 'ks' },
  { name: 'Kofola Original 2L', ean: '8594001010011', unit: 'ks' },
  { name: 'Heineken 0.5L', ean: '8714800000123', unit: 'ks' },
  { name: 'Sprite 1.5L', ean: '5449000001456', unit: 'ks' },
  { name: 'Fanta Orange 2L', ean: '5449000002789', unit: 'ks' },
  { name: 'Nestlé Čokoláda 100g', ean: '7613031234567', unit: 'ks' },
  { name: 'Minerálna voda 1.5L', ean: '8585001234567', unit: 'ks' },
  { name: 'Pivo Zlatý Bažant 0.5L', ean: '8586000000001', unit: 'ks' },
  { name: 'Káva Jacobs 250g', ean: '8711000000002', unit: 'ks' },
  { name: 'Čaj Lipton 20ks', ean: '8722700000003', unit: 'bal' },
  { name: 'Maslo 250g', ean: '5901234567890', unit: 'ks' },
  { name: 'Mlieko 1L', ean: '5901234567891', unit: 'ks' },
  { name: 'Chlieb 500g', ean: '5901234567892', unit: 'ks' },
  { name: 'Jogurt biely 150g', ean: '5901234567893', unit: 'ks' },
  { name: 'Syr Eidam 100g', ean: '5901234567894', unit: 'ks' },
];

const statuses: Invoice['status'][] = ['received', 'staged', 'pending_approval', 'approved', 'rejected', 'processed'];
const nexStatuses: Invoice['nex_status'][] = ['pending', 'enriched', 'imported', 'error'];

// Generate mock items for invoice
function generateMockItems(invoiceId: number, count: number): InvoiceItem[] {
  const items: InvoiceItem[] = [];

  for (let i = 1; i <= count; i++) {
    const product = products[Math.floor(Math.random() * products.length)];
    const quantity = Math.floor(Math.random() * 50) + 1;
    const pricePerUnit = Math.round((Math.random() * 10 + 0.5) * 100) / 100;
    const vatRate = Math.random() > 0.3 ? 20 : 10;

    items.push({
      id: invoiceId * 1000 + i,
      invoice_id: invoiceId,
      line_number: i,
      original_name: product.name,
      edited_name: undefined,
      quantity,
      unit: product.unit,
      price_per_unit: pricePerUnit,
      original_ean: product.ean,
      edited_ean: undefined,
      vat_rate: vatRate,
      nex_gs_index: Math.random() > 0.3 ? Math.floor(Math.random() * 10000) : undefined,
      nex_gs_name: Math.random() > 0.3 ? product.name : undefined,
      nex_matched_by: Math.random() > 0.3 ? 'ean' : undefined,
      nex_match_confidence: Math.random() > 0.3 ? Math.round(Math.random() * 40 + 60) / 100 : undefined,
    });
  }

  return items;
}

// Generate mock invoices
function generateMockInvoices(count: number): Invoice[] {
  const invoices: Invoice[] = [];
  const now = new Date();

  for (let i = 1; i <= count; i++) {
    const supplier = suppliers[Math.floor(Math.random() * suppliers.length)];
    const daysAgo = Math.floor(Math.random() * 60);
    const invoiceDate = new Date(now);
    invoiceDate.setDate(invoiceDate.getDate() - daysAgo);

    const dueDate = new Date(invoiceDate);
    dueDate.setDate(dueDate.getDate() + 30);

    const itemCount = Math.floor(Math.random() * 15) + 3; // 3-17 items
    const items = generateMockItems(i, itemCount);

    // Calculate totals from items
    const totalWithoutVat = items.reduce((sum, item) => sum + (item.quantity * item.price_per_unit), 0);
    const vat = Math.round(totalWithoutVat * 0.2 * 100) / 100;
    const total = Math.round((totalWithoutVat + vat) * 100) / 100;

    const status = statuses[Math.floor(Math.random() * statuses.length)];
    const nexStatus = nexStatuses[Math.floor(Math.random() * nexStatuses.length)];

    const invoiceNumber = `${supplier.name.substring(0, 3).toUpperCase()}-2025-${String(i).padStart(5, '0')}`;

    invoices.push({
      id: i,
      supplier_ico: supplier.ico,
      supplier_name: supplier.name,
      supplier_dic: supplier.dic,
      invoice_number: invoiceNumber,
      invoice_date: invoiceDate.toISOString().split('T')[0],
      due_date: dueDate.toISOString().split('T')[0],
      total_amount: total,
      total_vat: vat,
      total_without_vat: totalWithoutVat,
      currency: 'EUR',
      status,
      nex_status: nexStatus,
      file_basename: `${invoiceDate.toISOString().split('T')[0].replace(/-/g, '')}_${invoiceNumber}`,
      file_status: status === 'processed' ? 'archived' : 'staged',
      created_at: invoiceDate.toISOString(),
      updated_at: invoiceDate.toISOString(),
      items,
    });
  }

  return invoices.sort((a, b) => new Date(b.invoice_date).getTime() - new Date(a.invoice_date).getTime());
}

// Generate 50 mock invoices
export const mockInvoices: Invoice[] = generateMockInvoices(50);

// Calculate mock stats
export const mockStats: InvoiceStats = {
  total: mockInvoices.length,
  total_invoices: mockInvoices.length,
  by_status: mockInvoices.reduce((acc, inv) => {
    acc[inv.status] = (acc[inv.status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>),
  by_nex_status: mockInvoices.reduce((acc, inv) => {
    acc[inv.nex_status] = (acc[inv.nex_status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>),
  duplicates: 0,
};

export const USE_MOCK_DATA = import.meta.env.DEV;
