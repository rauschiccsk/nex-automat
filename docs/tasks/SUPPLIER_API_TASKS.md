# Supplier API Integration - TODO Checklist

## Referencia
Špecifikácia: `docs/specs/SUPPLIER_API_INTEGRATION_SPEC.md`

---

## Fáza 1: Príprava štruktúry (DNES)

### 1.1 Refaktoring existujúceho workflow
- [x] Premenovať `invoice_workflow.py` → `pdf_invoice_workflow.py`
- [x] Aktualizovať importy a referencie
- [ ] Overiť že PDF workflow stále funguje

### 1.2 Vytvorenie adresárovej štruktúry
- [x] Vytvoriť `apps/supplier-invoice-worker/adapters/`
- [x] Vytvoriť `apps/supplier-invoice-worker/models/`
- [x] Vytvoriť `apps/supplier-invoice-worker/config/suppliers/`

### 1.3 Základné modely
- [x] Vytvoriť `models/__init__.py`
- [x] Vytvoriť `models/unified_invoice.py`
  - [x] `InvoiceStatus` enum
  - [x] `InvoiceItem` dataclass
  - [x] `UnifiedInvoice` dataclass

### 1.4 Adapter základ
- [x] Vytvoriť `adapters/__init__.py`
- [x] Vytvoriť `adapters/base_adapter.py`
  - [x] `AuthType` enum
  - [x] `SupplierConfig` dataclass
  - [x] `BaseSupplierAdapter` abstraktná trieda

### 1.5 Konfigurácia
- [x] Vytvoriť `config/suppliers/_template.yaml`
- [x] Vytvoriť `config/suppliers/marso.yaml` (skeleton)

### 1.6 Skeleton workflow a activities
- [x] Vytvoriť `activities/supplier_api_activities.py` (skeleton)
- [x] Vytvoriť `workflows/api_invoice_workflow.py` (skeleton)

---

## Fáza 2: MARSO implementácia (ZAJTRA - po dokumentácii)

### 2.1 Analýza dokumentácie
- [ ] Analyzovať MARSO API dokumentáciu
- [ ] Analyzovať vzorový XML súbor
- [ ] Identifikovať pole s product code v XML
- [ ] Overiť názov stĺpca MARSO kód v NEX Genesis

### 2.2 Aktualizácia konfigurácie
- [ ] Doplniť `marso.yaml` s reálnymi hodnotami
- [ ] Pridať MARSO credentials do `.env.example`

### 2.3 MARSO Adapter
- [ ] Vytvoriť `adapters/marso_adapter.py`
  - [ ] `authenticate()` implementácia
  - [ ] `fetch_invoice_list()` implementácia
  - [ ] `fetch_invoice()` implementácia
  - [ ] `acknowledge_invoice()` implementácia
  - [ ] `parse_invoice()` XML parser

### 2.4 Product matching rozšírenie
- [ ] Upraviť `match_products()` pre MARSO kód
- [ ] Overiť mapovanie MARSO kód → NEX Genesis produkt

---

## Fáza 3: Temporal integration

### 3.1 Activities implementácia
- [x] `load_supplier_config()` - načítanie YAML (config/config_loader.py)
- [ ] `authenticate_supplier()` - autentifikácia
- [ ] `fetch_pending_invoices()` - zoznam faktúr
- [ ] `fetch_invoice_xml()` - stiahnutie XML
- [ ] `archive_raw_xml()` - archivácia
- [ ] `parse_invoice_xml()` - parsing
- [ ] `acknowledge_invoice()` - potvrdenie

### 3.2 Workflow implementácia
- [ ] Implementovať `api_invoice_workflow.py`
- [ ] Integrovať zdieľané activities
- [ ] Error handling a retry logika

### 3.3 Worker registrácia
- [ ] Registrovať nové activities v worker
- [ ] Registrovať nový workflow v worker

---

## Fáza 4: Testovanie

### 4.1 Unit testy
- [ ] Testy pre `UnifiedInvoice` model
- [ ] Testy pre `BaseSupplierAdapter`
- [ ] Testy pre `MarsoAdapter` (mock API)
- [ ] Testy pre XML parsing

### 4.2 Integration testy
- [ ] Test celého workflow s mock MARSO API
- [ ] Test archivácie XML súborov
- [ ] Test product matching

### 4.3 E2E test s MARSO
- [ ] Test s reálnym MARSO API (sandbox ak existuje)
- [ ] Overenie acknowledge mechanizmu

---

## Fáza 5: Deployment ANDROS

### 5.1 Konfigurácia
- [ ] Pridať MARSO credentials do ANDROS `.env`
- [ ] Overiť cesty k archivácii na ANDROS serveri

### 5.2 Deployment
- [ ] Deploy na Dell PowerEdge R740XD
- [ ] Registrácia workflow v Temporal
- [ ] Nastavenie schedule (ak automatický trigger)

### 5.3 Monitoring
- [ ] Overiť v Temporal UI
- [ ] Test prvej reálnej faktúry

---

## Fáza 6: Dokumentácia

- [ ] Aktualizovať PROJECT_STRUCTURE.md
- [ ] Pridať do RAG
- [ ] Návod na pridanie nového dodávateľa

---

## Budúcnosť: CONTINENTAL

- [ ] Získať CONTINENTAL API dokumentáciu
- [ ] Vytvoriť `continental_adapter.py`
- [ ] Vytvoriť `continental.yaml`
- [ ] Testovanie a deployment

---

## Quick Reference - Claude Code príkazy

```bash
# Fáza 1.1 - Refaktoring
"Premenuj invoice_workflow.py na pdf_invoice_workflow.py a aktualizuj všetky importy"

# Fáza 1.2 - Štruktúra
"Vytvor adresárovú štruktúru podľa SUPPLIER_API_INTEGRATION_SPEC.md"

# Fáza 1.3 - Modely
"Implementuj models/unified_invoice.py podľa špecifikácie"

# Fáza 1.4 - Adapter
"Implementuj adapters/base_adapter.py podľa špecifikácie"
```

---

## Poznámky

_Sem zapisuj poznámky počas implementácie_

-