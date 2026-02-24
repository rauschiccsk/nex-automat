# Supplier Invoice Staging Web UI

**Dátum:** 2025-12-26
**Status:** 🔄 IN PROGRESS

---

## Dokončené úlohy ✅

### Fáza 1: Setup projektu
- Vite + React + TypeScript projekt vytvorený
- Tailwind CSS v4 nakonfigurovaný
- Shadcn/ui nainštalovaný (button, card, badge, table, input, select, dialog, sonner)
- Axios + TanStack Query + React Router + Lucide icons

### Fáza 2: Layout a navigácia
- Header, Sidebar, Layout komponenty
- Routing (Dashboard, Faktúry, Detail faktúry, Nastavenia)
- API klient pripojený na backend (port 8001)

### Fáza 3: DataGrid s rýchlo-vyhľadávačom
- Column filters pod každým stĺpcom (ako v NEX Genesis)
- Keyboard navigation (Tab, Enter, šípky, Esc)
- Virtual scrolling pre veľké datasety
- Sorting kliknutím na hlavičku
- Column configuration (zobraziť/skryť, poradie, premenovať) - ikona ⚙️

### Fáza 4: Detail faktúry
- Hlavička faktúry (dodávateľ, sumy, stav)
- DataGrid s položkami faktúry
- Tlačidlá Schváliť/Zamietnuť (pre pending_approval status)

## Aktuálny problém ❌

Mock data nepoužívajú správnu databázovú štruktúru. Potrebné:
- Aktualizovať TypeScript typy podľa reálnej DB schémy
- Opraviť mock data (xml_* prefixy, správne názvy polí)

## Správna DB schéma (z RAG)

### supplier_invoice_heads
- xml_invoice_number, xml_variable_symbol, xml_issue_date, xml_due_date
- xml_supplier_ico, xml_supplier_name, xml_supplier_dic
- xml_total_without_vat, xml_total_vat, xml_total_with_vat, xml_currency
- status (pending/matched/approved/imported)
- nex_supplier_id, item_count, items_matched, match_percent

### supplier_invoice_items  
- invoice_head_id (FK)
- xml_line_number, xml_product_name, xml_seller_code, xml_ean
- xml_quantity, xml_unit, xml_unit_price, xml_vat_rate
- nex_product_id, nex_product_name, nex_ean
- matched, matched_by, match_confidence

## Štruktúra projektu

```
apps/supplier-invoice-staging-web/
├── src/
│   ├── api/
│   │   ├── client.ts
│   │   ├── invoices.ts
│   │   └── mockData.ts
│   ├── components/
│   │   ├── layout/ (Header, Sidebar, Layout)
│   │   └── ui/ (shadcn + datagrid.tsx)
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Invoices.tsx
│   │   ├── InvoiceDetail.tsx
│   │   └── Settings.tsx
│   ├── types/
│   │   └── invoice.ts
│   └── App.tsx
├── package.json
└── vite.config.ts
```

## Next Steps

1. Aktualizovať TypeScript typy podľa DB schémy (xml_* prefixy)
2. Opraviť mock data
3. Otestovať s reálnym backendom (Mágerstav)
4. Schvaľovací workflow (dialógy)
5. Docker deployment

## Dôležité príkazy

```powershell
# Dev server
cd C:\Development\nex-automat\apps\supplier-invoice-staging-web
npm run dev

# Backend (Mágerstav)
# Port 8001, API Key: andros-api-key-2025
```

## RAG Queries

```
https://rag-api.icc.sk/search?query=supplier_invoice_heads+schema&limit=5
https://rag-api.icc.sk/search?query=supplier-invoice-loader+API+endpoints&limit=5
```
