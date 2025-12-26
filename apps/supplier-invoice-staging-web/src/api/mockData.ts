import type { InvoiceHead, InvoiceItem, InvoiceStats, InvoiceStatus, MatchMethod } from '@/types/invoice';

// Seeded random number generator for consistent mock data
class SeededRandom {
  private seed: number;

  constructor(seed: number) {
    this.seed = seed;
  }

  next(): number {
    this.seed = (this.seed * 1103515245 + 12345) & 0x7fffffff;
    return this.seed / 0x7fffffff;
  }

  nextInt(max: number): number {
    return Math.floor(this.next() * max);
  }
}

// Suppliers for generating mock data
const suppliers = [
  { ico: '35850370', name: 'L&Š Slovakia s.r.o.', dic: '2021749064', ic_dph: 'SK2021749064' },
  { ico: '44556677', name: 'METRO Cash & Carry SK', dic: '2022889900', ic_dph: 'SK2022889900' },
  { ico: '12345678', name: 'Bidvest Slovakia s.r.o.', dic: '2020123456', ic_dph: 'SK2020123456' },
  { ico: '98765432', name: 'Kofola a.s.', dic: '2019876543', ic_dph: 'SK2019876543' },
  { ico: '55667788', name: 'Heineken Slovensko', dic: '2055667788', ic_dph: 'SK2055667788' },
  { ico: '11223344', name: 'Nestlé Slovensko s.r.o.', dic: '2011223344', ic_dph: 'SK2011223344' },
  { ico: '33445566', name: 'Coca-Cola HBC Slovensko', dic: '2033445566', ic_dph: 'SK2033445566' },
  { ico: '77889900', name: 'Unilever Slovensko', dic: '2077889900', ic_dph: 'SK2077889900' },
  { ico: '22334455', name: 'Makro Cash & Carry', dic: '2022334455', ic_dph: 'SK2022334455' },
  { ico: '66778899', name: 'CBA Slovakia', dic: '2066778899', ic_dph: 'SK2066778899' },
];

const products = [
  { name: 'Coca-Cola 2L', ean: '5449000000996', unit: 'ks', seller_code: 'CC-2L' },
  { name: 'Kofola Original 2L', ean: '8594001010011', unit: 'ks', seller_code: 'KOF-2L' },
  { name: 'Heineken 0.5L', ean: '8714800000123', unit: 'ks', seller_code: 'HNK-05' },
  { name: 'Sprite 1.5L', ean: '5449000001456', unit: 'ks', seller_code: 'SPR-15' },
  { name: 'Fanta Orange 2L', ean: '5449000002789', unit: 'ks', seller_code: 'FNT-2L' },
  { name: 'Nestlé Čokoláda 100g', ean: '7613031234567', unit: 'ks', seller_code: 'NST-100' },
  { name: 'Minerálna voda 1.5L', ean: '8585001234567', unit: 'ks', seller_code: 'MIN-15' },
  { name: 'Pivo Zlatý Bažant 0.5L', ean: '8586000000001', unit: 'ks', seller_code: 'ZB-05' },
  { name: 'Káva Jacobs 250g', ean: '8711000000002', unit: 'ks', seller_code: 'JAC-250' },
  { name: 'Čaj Lipton 20ks', ean: '8722700000003', unit: 'bal', seller_code: 'LIP-20' },
  { name: 'Maslo 250g', ean: '5901234567890', unit: 'ks', seller_code: 'MAS-250' },
  { name: 'Mlieko 1L', ean: '5901234567891', unit: 'ks', seller_code: 'MLK-1L' },
  { name: 'Chlieb 500g', ean: '5901234567892', unit: 'ks', seller_code: 'CHL-500' },
  { name: 'Jogurt biely 150g', ean: '5901234567893', unit: 'ks', seller_code: 'JOG-150' },
  { name: 'Syr Eidam 100g', ean: '5901234567894', unit: 'ks', seller_code: 'EID-100' },
];

const statuses: InvoiceStatus[] = ['pending', 'matched', 'approved', 'imported'];
const matchMethods: MatchMethod[] = ['ean', 'name', 'code'];

// Generate mock items for invoice
function generateMockItems(rng: SeededRandom, invoiceHeadId: number, count: number): InvoiceItem[] {
  const items: InvoiceItem[] = [];

  for (let i = 1; i <= count; i++) {
    const product = products[rng.nextInt(products.length)];
    const quantity = rng.nextInt(50) + 1;
    const unitPrice = Math.round((rng.next() * 10 + 0.5) * 100) / 100;
    const vatRate = rng.next() > 0.3 ? 20 : 10;
    const totalPrice = Math.round(quantity * unitPrice * 100) / 100;
    const unitPriceVat = Math.round(unitPrice * (1 + vatRate / 100) * 100) / 100;
    const totalPriceVat = Math.round(totalPrice * (1 + vatRate / 100) * 100) / 100;
    const isMatched = rng.next() > 0.3;

    items.push({
      id: invoiceHeadId * 1000 + i,
      invoice_head_id: invoiceHeadId,

      // XML fields
      xml_line_number: i,
      xml_product_name: product.name,
      xml_seller_code: product.seller_code,
      xml_ean: product.ean,
      xml_quantity: quantity,
      xml_unit: product.unit,
      xml_unit_price: unitPrice,
      xml_total_price: totalPrice,
      xml_unit_price_vat: unitPriceVat,
      xml_total_price_vat: totalPriceVat,
      xml_vat_rate: vatRate,

      // NEX fields (enrichment)
      nex_product_id: isMatched ? rng.nextInt(10000) : undefined,
      nex_product_name: isMatched ? product.name : undefined,
      nex_ean: isMatched ? product.ean : undefined,
      nex_stock_code: isMatched ? `STK-${rng.nextInt(1000)}` : undefined,

      // Matching
      matched: isMatched,
      matched_by: isMatched ? matchMethods[rng.nextInt(matchMethods.length)] : undefined,
      match_confidence: isMatched ? Math.round(rng.next() * 40 + 60) : undefined,

      // Timestamps
      created_at: '2025-12-20T10:00:00Z',
      updated_at: '2025-12-20T10:00:00Z',
    });
  }

  return items;
}

// Generate mock invoices with seeded random
function generateMockInvoices(count: number): InvoiceHead[] {
  const rng = new SeededRandom(12345); // Fixed seed for consistent data
  const invoices: InvoiceHead[] = [];
  const baseDate = new Date('2025-12-20');

  for (let i = 1; i <= count; i++) {
    const supplier = suppliers[rng.nextInt(suppliers.length)];
    const daysAgo = rng.nextInt(60);
    const issueDate = new Date(baseDate);
    issueDate.setDate(issueDate.getDate() - daysAgo);

    const dueDate = new Date(issueDate);
    dueDate.setDate(dueDate.getDate() + 30);

    const taxPointDate = new Date(issueDate);

    const itemCount = rng.nextInt(15) + 3;
    const items = generateMockItems(rng, i, itemCount);

    // Calculate totals from items
    const totalWithoutVat = Math.round(items.reduce((sum, item) => sum + item.xml_total_price, 0) * 100) / 100;
    const totalVat = Math.round(totalWithoutVat * 0.2 * 100) / 100;
    const totalWithVat = Math.round((totalWithoutVat + totalVat) * 100) / 100;

    const status = statuses[rng.nextInt(statuses.length)];
    const matchedItems = items.filter(item => item.matched).length;
    const matchPercent = Math.round((matchedItems / items.length) * 100 * 100) / 100;

    const invoiceNumber = `FV-2025-${String(i).padStart(5, '0')}`;
    const variableSymbol = `${issueDate.getFullYear()}${String(i).padStart(6, '0')}`;

    invoices.push({
      id: i,

      // XML fields
      xml_invoice_number: invoiceNumber,
      xml_variable_symbol: variableSymbol,
      xml_issue_date: issueDate.toISOString().split('T')[0],
      xml_tax_point_date: taxPointDate.toISOString().split('T')[0],
      xml_due_date: dueDate.toISOString().split('T')[0],
      xml_currency: 'EUR',
      xml_supplier_ico: supplier.ico,
      xml_supplier_name: supplier.name,
      xml_supplier_dic: supplier.dic,
      xml_supplier_ic_dph: supplier.ic_dph,
      xml_iban: `SK89${String(1000000000 + i * 123456).slice(0, 10)}`,
      xml_total_without_vat: totalWithoutVat,
      xml_total_vat: totalVat,
      xml_total_with_vat: totalWithVat,

      // NEX fields
      nex_supplier_id: rng.next() > 0.2 ? rng.nextInt(1000) : undefined,
      nex_stock_id: 1,
      nex_book_num: 1,

      // Workflow
      status,
      item_count: items.length,
      items_matched: matchedItems,
      match_percent: matchPercent,

      // Files
      xml_file_path: `/data/staged/${issueDate.toISOString().split('T')[0].replace(/-/g, '')}/${invoiceNumber}.xml`,
      pdf_file_path: `/data/staged/${issueDate.toISOString().split('T')[0].replace(/-/g, '')}/${invoiceNumber}.pdf`,

      // Timestamps
      created_at: issueDate.toISOString(),
      updated_at: issueDate.toISOString(),

      // Items
      items,
    });
  }

  return invoices.sort((a, b) => new Date(b.xml_issue_date).getTime() - new Date(a.xml_issue_date).getTime());
}

// Generate 50 mock invoices (generated once, not on every import)
export const mockInvoices: InvoiceHead[] = generateMockInvoices(50);

// Calculate mock stats
export const mockStats: InvoiceStats = {
  total: mockInvoices.length,
  by_status: mockInvoices.reduce((acc, inv) => {
    acc[inv.status] = (acc[inv.status] || 0) + 1;
    return acc;
  }, {} as Record<InvoiceStatus, number>),
  total_amount: Math.round(mockInvoices.reduce((sum, inv) => sum + inv.xml_total_with_vat, 0) * 100) / 100,
  avg_match_percent: Math.round(mockInvoices.reduce((sum, inv) => sum + inv.match_percent, 0) / mockInvoices.length * 100) / 100,
};

export const USE_MOCK_DATA = import.meta.env.DEV;
