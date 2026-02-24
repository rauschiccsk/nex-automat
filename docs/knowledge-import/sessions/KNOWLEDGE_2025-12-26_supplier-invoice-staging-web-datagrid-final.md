# Session: Supplier Invoice Staging Web - DataGrid Final

**Dátum:** 2025-12-26
**Status:** ✅ DONE

---

## Dokončené úlohy ✅

1. **Dialog drag & drop** - funguje len z GripVertical ikony (⋮⋮)
2. **Grid resize vs drag konflikt** - opravený, resize neaktivuje drag
3. **Numerický filter** - presná zhoda + rozsahy (>20, <10, >=5, <=100, 10-50)
4. **Všetky stĺpce z DB schémy** - 21 stĺpcov (XML, NEX, Matching, Validation)
5. **Kompaktný layout** - 24px riadky, menšie písmo, menšie paddingy
6. **Správny overflow** - h-screen, overflow-hidden na všetkých úrovniach

## Technické detaily

### Súbory zmenené:
- `src/components/ui/datagrid.tsx` - numericFilter, resize fix, layout fix
- `src/pages/InvoiceDetail.tsx` - všetky stĺpce, kompaktný layout
- `src/components/layout/Layout.tsx` - h-screen overflow fix

### Numerický filter syntax:
- `21` → presná zhoda
- `>20` → väčšie ako 20
- `<10` → menšie ako 10
- `>=5` → väčšie alebo rovné 5
- `<=100` → menšie alebo rovné 100
- `10-50` → rozsah od 10 do 50

## Next Steps (nová session)

1. Editovateľné bunky v gride (marža, predajná cena)
2. Prepočty pri zmene hodnôt
3. Test s reálnym backendom
4. Schvaľovací workflow
5. Docker deployment

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
