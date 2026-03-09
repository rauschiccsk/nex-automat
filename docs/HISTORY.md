# NEX Automat — Development History

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
