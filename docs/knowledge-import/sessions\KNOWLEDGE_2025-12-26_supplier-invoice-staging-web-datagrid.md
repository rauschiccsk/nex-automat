# Session: Supplier Invoice Staging Web - DataGrid Improvements

**Dátum:** 2025-12-26
**Status:** 🔄 IN PROGRESS

---

## Dokončené úlohy ✅

1. **TypeScript typy opravené** - xml_* prefixy podľa DB schémy
   - `Invoice` → `InvoiceHead`
   - Všetky polia s `xml_*` a `nex_*` prefixami
   - Status enum: `pending | matched | approved | imported`

2. **Mock data opravené** - SeededRandom pre stabilné dáta pri F5

3. **API invoices.ts** - používa nové typy `InvoiceHead`

4. **Invoices.tsx** - stĺpce s xml_* prefixami, pridaná match_percent

5. **InvoiceDetail.tsx** - kompletne prepracovaný s novými typmi

6. **DataGrid vylepšenia**:
   - Column config dialog (⚙️)
   - Zobrazenie column ID (anglický názov)
   - Editovateľné názvy stĺpcov
   - Zmena šírky stĺpcov (input + resize drag)
   - Drag & drop zmena poradia v gride (hlavičky)
   - Drag & drop zmena poradia v dialógu
   - Visibility toggle
   - Auto-save do localStorage

## Aktuálny problém ❌

Pri drag & drop v dialógu konflikt medzi:
- Ťahaním celého riadku (GripVertical ikona)
- Ťahaním za iné časti riadku

Treba opraviť aby drag fungoval IBA z GripVertical ikony.

## Next Steps

1. Fix drag & drop v dialógu - len z GripVertical handle
2. Test s reálnym backendom
3. Schvaľovací workflow
4. Docker deployment

## Umiestnenie

```
C:\Development\nex-automat\apps\supplier-invoice-staging-web\
```

## Spustenie

```bash
cd C:\Development\nex-automat\apps\supplier-invoice-staging-web
npm run dev
# http://localhost:5173
```

## Dôležité súbory

- `src/types/invoice.ts` - TypeScript typy
- `src/api/mockData.ts` - Mock data
- `src/components/ui/datagrid.tsx` - DataGrid komponent
- `src/pages/Invoices.tsx` - Zoznam faktúr
- `src/pages/InvoiceDetail.tsx` - Detail faktúry
