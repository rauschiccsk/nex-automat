# NEX Automat — Development History

## Session 18: Order Fix O-2 — Audit GAP-02+03+04+05 (2026-03-18)

**Order system audit gap fixes:** GAP-02, GAP-03, GAP-04, GAP-05

### Zmeny

**GAP-02: Shipping order item (KRITICKY):**
- `shipping_price` field v `OrderCreateRequest` schema
- Ak `shipping_price > 0`, vytvorí sa order item s `item_type='shipping'`
- Automatický výpočet ceny bez DPH z ceny s DPH
- Totaly objednávky sa aktualizujú o poštovné

**GAP-03: billing_postal_code sync (STREDNY):**
- `billing_postal_code` sa automaticky nastaví na hodnotu `billing_zip`
- Eliminuje NULL v duplicitnom stĺpci

**GAP-04: Company billing address (STREDNY):**
- 4 nové polia v schema: `company_billing_street/city/postal_code/country`
- Ak `is_company_order=True` + company billing polia vyplnené → billing override
- Firemná fakturačná adresa sa správne uloží do billing stĺpcov

**GAP-05: ico/dic/eu_vat_number sync (STREDNY):**
- `ico` = `company_ico`, `dic` = `company_dic`, `eu_vat_number` = `company_ic_dph`
- MuFis getOrder vracia správny `eu_vat_number` bez ďalšej logiky

### Testy

**+5 nových testov (celkom ESHOP: 105):**
- `test_create_order_with_shipping_price` — shipping item existuje
- `test_create_order_zero_shipping` — žiadny shipping item
- `test_create_order_billing_postal_code_sync` — postal code sync
- `test_create_order_company_billing_address` — company billing override
- `test_create_order_company_vat_sync` — VAT number sync

**Celkový počet backend testov:** 182

---

## Session 18: MuFis Fix B-2 — setProduct Batch + Webhook Trigger (2026-03-17)

**MuFis audit gap fixes:** SP1, SP3, W1

### Zmeny

**setProduct batch mode (SP1 + SP3):**
- `_process_set_product()` helper funkcia pre zdieľanú logiku
- Batch mode cez `data` parameter (JSON array)
- Batch response: `{"products": [{"sku": "...", "ok": 1, "error": ""}, ...]}`
- Single mode backward compatible: `{"ok": 1, "error": ""}`
- `updated_at = CURRENT_TIMESTAMP` pri stock update
- Per-item error handling (missing sku, missing stock_quantity, invalid value)

**Webhook trigger (W1):**
- Nový modul `eshop/mufis_webhook.py` — fire-and-forget HTTP GET na MuFis URL
- Integrácia do `create_order` (POST /api/eshop/orders)
- Integrácia do `admin_update_order` (PATCH /api/eshop/admin/orders/{id})
- Dry-run podpora cez `MUFIS_DRY_RUN` env var
- Non-blocking, timeout 10s, zlyhanie je len WARNING log
- httpx dependency pridaná do requirements.txt

### Testy

**+6 nových testov (celkom MuFis: 39):**
- SP1: Batch mode, invalid JSON, partial success
- SP3: Single mode stock_quantity + updated_at
- W1: Webhook dry-run (GET sa nevolá), webhook sends GET

**Celkový počet backend testov:** 177

---

## F3.1: ESHOP Admin Panel (2026-03-09)

**ESHOP admin frontend** v NEX Manager (Electron/React) pre správu objednávok, produktov a tenantov.

### Nové súbory

**TypeScript types:**
- `src/renderer/src/types/eshop.ts` — EshopOrder, EshopOrderDetail, EshopProduct, EshopTenant + enums

**Zustand store:**
- `src/renderer/src/stores/eshopStore.ts` — ESHOP module UI state (view, filters, pagination, navigation)

**Components (6):**
- `src/renderer/src/components/modules/eshop/EshopModuleView.tsx` — hlavný view s tabmi Objednávky | Produkty | Tenanty
- `src/renderer/src/components/modules/eshop/EshopOrderList.tsx` — DataGrid objednávok + status/payment badges + filter + search
- `src/renderer/src/components/modules/eshop/EshopOrderDetail.tsx` — detail objednávky: zákazník, adresy, položky, tracking, status change, história
- `src/renderer/src/components/modules/eshop/EshopProductList.tsx` — DataGrid produktov + active/inactive filter + CRUD
- `src/renderer/src/components/modules/eshop/EshopProductForm.tsx` — create/edit formulár s auto-výpočtom DPH
- `src/renderer/src/components/modules/eshop/EshopTenantList.tsx` — read-only tabuľka tenantov
- `src/renderer/src/components/modules/eshop/eshopGridConfigs.ts` — grid konfigurácie pre objednávky a produkty

**Registrácia modulu:**
- `App.tsx` — ESHOP routing (activeTab.id === 'ESHOP')
- `lib/iconMap.ts` — ShoppingBag ikona
- `lib/api.ts` — 8 nových ESHOP Admin API endpointov

### Testy

**27 nových frontend testov:**
- `EshopOrderList.test.tsx` — 8 testov (render, data, loading, error, search, filter, retry)
- `EshopOrderDetail.test.tsx` — 8 testov (header, customer, addresses, items, total, history, back)
- `EshopProductList.test.tsx` — 6 testov (render, data, create button, filter, loading, error)
- `EshopProductForm.test.tsx` — 5 testov (form fields, validation, auto-calc, save, cancel)

**Celkový počet testov:** 304 frontend + 77 backend = 381 testov

---

### F4.4c: ESHOP Product Fixes + Lead Capture System
- **Dátum:** 2026-03-10
- **Commit:** 065113f
- **Typ:** Backend (NEX Automat)
- **Zmeny:**
  - Migration 009: DPH 20%→23%, produkty Bajkal→Oasis EM-1
  - EM-5L deaktivovaný, nový EM-500-3PACK (akcia 2+1)
  - Nová tabuľka eshop_leads (lead capture + discount)
  - 2 nové verejné API endpointy (leads register, validate)
  - Discount code integrácia do objednávkového flow
  - 2 nové email šablóny (welcome, reminder)
  - +19 testov (celkom ESHOP backend: 96)
- **CI:** 9/10 jobov GREEN (E2E Tests skipped — no trigger)
