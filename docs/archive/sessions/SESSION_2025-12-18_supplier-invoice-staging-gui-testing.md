# Session: supplier-invoice-staging-gui-testing

**Dátum:** 2025-12-18
**Projekt:** nex-automat
**Stav:** COMPLETED

---

## Prehľad Session

Testovanie a vylepšovanie GUI aplikácie supplier-invoice-staging (PySide6).

---

## Dokončené Úlohy

### 1. Klávesové skratky
- ✅ Enter v hlavičkách faktúr otvára položky
- ✅ ESC v položkách zatvára okno
- ✅ ESC v hlavičkách zatvára aplikáciu

### 2. Modálne okno položiek
- ✅ InvoiceItemsWindow je teraz ApplicationModal
- ✅ Len jedna faktúra môže byť otvorená naraz
- ✅ Jednotná pozícia okna pre všetky faktúry

### 3. Grid Settings Persistence
- ✅ save_grid_settings_now() volaný pri closeEvent oboch okien
- ✅ Nastavenia sa ukladajú pri zatvorení každého okna

### 4. Initial Row Selection
- ✅ BaseGrid.select_initial_row() - nová metóda
- ✅ Automatický výber prvého riadku po načítaní dát
- ✅ Focus na table_view v InvoiceItemsWindow

### 5. Header Context Menu (BaseGrid)
- ✅ Pravý klik na header → context menu
- ✅ "Premenovať '...'..." - dialóg pre vlastný názov stĺpca
- ✅ "Obnoviť pôvodný názov" - reset custom header
- ✅ "Stĺpce" submenu - checkbox pre viditeľnosť každého stĺpca
- ✅ Custom headers sa ukladajú a načítavajú zo settings
- ✅ Fix: Obnovenie šírky stĺpca pri set_column_visible(True)

### 6. BaseGrid.create_item() - Automatické formátovanie
- ✅ int → doprava zarovnané, bez desatinných miest
- ✅ float → doprava zarovnané, 2 desatinné miesta (vrátane 0.00)
- ✅ bool → ✓ (zelená) / ✗ (červená), centrované
- ✅ string → doľava zarovnané
- ✅ Použité v MainWindow a InvoiceItemsWindow

---

## Modifikované Súbory

### apps/supplier-invoice-staging/
- `ui/main_window.py` - Enter/ESC handlers, modal window, create_item
- `ui/invoice_items_window.py` - ESC handler, focus, create_item, test data floats

### packages/shared-pyside6/shared_pyside6/ui/
- `base_grid.py` - select_initial_row, header context menu, create_item, boolean icons, column visibility fix

---

## Vytvorené Skripty (scripts/)

| # | Skript | Popis |
|---|--------|-------|
| 01 | add_enter_key_handler.py | Enter otvára položky faktúry |
| 02 | add_esc_handler_items_window.py | ESC zatvára okno položiek |
| 03 | make_items_window_modal.py | Modálne okno položiek |
| 04 | fix_items_window_position.py | Jednotná pozícia okna |
| 05 | save_settings_on_close.py | Uloženie settings pri zatvorení |
| 06 | select_first_row_on_load.py | Výber prvého riadku (hlavičky) |
| 07 | select_first_row_items_window.py | Výber prvého riadku (položky) |
| 08 | move_select_row_to_base_grid.py | Presun do BaseGrid |
| 09 | fix_select_row_timing.py | Oprava timing |
| 10 | fix_items_window_active_column.py | Ukladanie aktívneho stĺpca |
| 11 | fix_items_window_focus.py | Focus na table_view |
| 12 | add_header_context_menu.py | Context menu na header |
| 13 | fix_load_custom_headers.py | Načítanie custom headers |
| 14 | fix_column_visibility.py | Oprava šírky pri zobrazení |
| 15 | add_create_item_to_base_grid.py | Automatické formátovanie |
| 16 | fix_zero_decimal_format.py | 0 ako 0.00 |
| 17 | fix_test_data_floats.py | Test dáta 0 → 0.0 |
| 18 | add_boolean_icons.py | ✓/✗ ikony pre boolean |
| 19 | add_esc_to_main_window.py | ESC v hlavnom okne |

---

## Ďalšie Kroky (Nový Chat)

### Priority #1: Connect to Real Data
- Aplikácia pobeží na **Mágerstav serveri**
- **Lokálna PostgreSQL** databáza `invoice_staging`
- Použiť existujúci `PostgresStagingClient` z `nex-shared`
- Nahradiť `_load_test_data()` a `_load_test_items()` reálnymi queries

### Potrebné:
1. Pridať database service do supplier-invoice-staging
2. Konfigurácia pripojenia (config.yaml)
3. Query pre načítanie faktúr z `invoices_pending`
4. Query pre načítanie položiek z `invoice_items_pending`

---

## Technické Poznámky

### Settings DB lokácie
- Development: `C:\Users\ZelenePC\.nex-automat\settings.db`
- App-specific: `apps/supplier-invoice-staging/data/settings.db`

### RAG Workflow
- Claude vypíše URL, user vloží do chatu, Claude fetchne
- Funguje spoľahlivo, nemeníme

---

**Session ukončená:** 2025-12-18
