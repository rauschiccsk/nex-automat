# Session: Supplier Invoice Staging Web - BaseGrid System

**Dátum:** 2025-12-26
**Status:** ✅ DONE

---

## Dokončené úlohy ✅

1. **Editovateľné bunky v DataGrid**
   - EditableCell komponent (double-click to edit)
   - Props: editableColumns, onCellEdit
   - Enter uloží, Escape zruší

2. **BaseGrid systém** - reusable grid components
   - `gridFormatters.ts` - formatCurrency, formatPercent, formatDate, formatDateTime, formatBoolean
   - `gridFilters.ts` - stringFilter, numericFilter, dateFilter, booleanFilter
   - `gridTypes.ts` - GridColumnConfig, GridConfig typy
   - `BaseGrid.tsx` - hlavný reusable komponent
   - Export do CSV/JSON

3. **Grid konfigurácie**
   - `invoiceItemsGrid.tsx` - položky faktúry (21 stĺpcov)
   - `invoiceHeadsGrid.tsx` - zoznam faktúr (14 stĺpcov)
   - Editovateľné: nex_margin_percent, nex_sales_price

4. **Prepočty marža ↔ predajná cena**
   - Zmena marže → prepočet predajnej ceny
   - Zmena predajnej ceny → prepočet marže
   - Celková hodnota faktúry (nákup/predaj/marža)

5. **UI vylepšenia**
   - Export tlačidlo na oboch gridoch
   - Opravená viditeľnosť tlačidla Zrušiť

## Štruktúra súborov

```
src/components/
├── ui/
│   └── datagrid.tsx              # Základný DataGrid
├── grids/
│   ├── index.ts                  # Centrálne exporty
│   ├── gridFormatters.ts         # Formátovacie funkcie
│   ├── gridFilters.ts            # Filtrovacie funkcie
│   ├── gridTypes.ts              # TypeScript typy
│   ├── BaseGrid.tsx              # Reusable grid wrapper
│   └── configs/
│       ├── index.ts
│       ├── invoiceItemsGrid.tsx  # Konfig položiek
│       └── invoiceHeadsGrid.tsx  # Konfig hlavičiek
```

## Použitie BaseGrid

```typescript
import { BaseGrid, invoiceHeadsGridConfig } from '@/components/grids';

<BaseGrid
  data={invoices}
  config={invoiceHeadsGridConfig}
  onRowDoubleClick={handleRowDoubleClick}
  editableColumns={['nex_margin_percent']}
  onCellEdit={handleCellEdit}
/>
```

## Definícia stĺpcov

```typescript
{
  id: 'xml_unit_price',
  header: 'Nák. cena',
  type: 'currency',    // automatický formát + filter
  size: 90,
  editable: true,      // editovateľné bunky
  cellClass: 'font-medium text-blue-700',
}
```

## Next Steps (nová session)

1. Test s reálnym backendom (FastAPI)
2. Uloženie editácií do DB
3. Schvaľovací workflow
4. Docker deployment

## Umiestnenie

```
C:\Development\nex-automat\apps\supplier-invoice-staging-web\
```

## Spustenie

```powershell
cd C:\Development\nex-automat\apps\supplier-invoice-staging-web
npm run dev
# http://localhost:5173
```
