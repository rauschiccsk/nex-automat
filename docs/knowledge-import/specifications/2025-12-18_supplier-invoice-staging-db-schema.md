# Supplier Invoice Staging - Database Schema

**Dátum:** 2025-12-18  
**Databáza:** supplier_invoice_staging  
**Verzia:** 1.0

---

## Konvencie názvov polí

### Prefixy

| Prefix | Zdroj | Popis |
|--------|-------|-------|
| `xml_*` | ISDOC XML | Polia načítané z XML - **IMMUTABLE**, len ukladáme |
| `nex_*` | NEX Genesis | Polia z ERP systému - obohatenie/párovanie |

**PRAVIDLO:** XML údaje len ukladáme, nič nepočítame, nič nemeníme!

---

## Tabuľky

### supplier_invoice_heads

Hlavičky dodávateľských faktúr.

**XML polia:**
- `xml_invoice_number` - Číslo faktúry (ID element)
- `xml_variable_symbol` - Variabilný symbol (len 0-9)
- `xml_issue_date` - Dátum vystavenia
- `xml_tax_point_date` - Dátum zdaniteľného plnenia
- `xml_due_date` - Dátum splatnosti
- `xml_currency` - Mena (EUR)
- `xml_supplier_ico` - IČO dodávateľa
- `xml_supplier_name` - Názov dodávateľa
- `xml_supplier_dic` - DIČ
- `xml_supplier_ic_dph` - IČ DPH
- `xml_iban` - IBAN z XML
- `xml_swift` - SWIFT z XML
- `xml_total_without_vat` - Suma bez DPH
- `xml_total_vat` - DPH
- `xml_total_with_vat` - Suma s DPH

**NEX polia:**
- `nex_supplier_id` - ID partnera v NEX
- `nex_supplier_modify_id` - Verzia partnera (versioning)
- `nex_iban` - IBAN z NEX
- `nex_swift` - SWIFT z NEX
- `nex_stock_id` - Cieľový sklad
- `nex_book_num` - Kniha dokladov
- `nex_payment_method_id` - Platobný spôsob
- `nex_price_list_id` - Cenník

**Workflow:**
- `status` - pending → matched → approved → imported
- `item_count`, `items_matched`, `match_percent` - agregované štatistiky

---

### supplier_invoice_items

Položky dodávateľských faktúr.

**XML polia:**
- `xml_line_number` - Číslo riadku
- `xml_product_name` - Názov produktu (Description)
- `xml_seller_code` - Kód u dodávateľa (SellersItemIdentification)
- `xml_ean` - EAN kód (StandardItemIdentification)
- `xml_quantity` - Množstvo
- `xml_unit` - Merná jednotka (KS, L, KG...)
- `xml_unit_price` - Jednotková cena bez DPH
- `xml_total_price` - Celkom bez DPH
- `xml_unit_price_vat` - Jednotková cena s DPH
- `xml_total_price_vat` - Celkom s DPH
- `xml_vat_rate` - Sadzba DPH (20, 10, 0)

**NEX polia:**
- `nex_product_id` - ID produktu v NEX (gs_code z GSCAT)
- `nex_product_modify_id` - Verzia produktu
- `nex_product_name` - Názov z NEX
- `nex_product_category_id` - Tovarová skupina
- `nex_ean` - EAN z NEX
- `nex_stock_code` - Skladový kód
- `nex_stock_id` - Sklad
- `nex_facility_id` - Prevádzka
- `nex_purchase_price` - Nákupná cena z cenníka
- `nex_sales_price` - Predajná cena z cenníka

**Matching:**
- `matched` - Boolean, či je napárovaný
- `matched_by` - Metóda: 'ean', 'seller_code', 'name', 'manual'
- `match_confidence` - Skóre zhody (0-100%)

---

## Workflow stavy

| Stav | Popis |
|------|-------|
| `pending` | Čaká na spracovanie |
| `matched` | Položky napárované s NEX |
| `approved` | Schválené operátorom |
| `imported` | Importované do NEX Genesis |

---

## Matching metódy

| Metóda | Priorita | Popis |
|--------|----------|-------|
| `ean` | 1 (najvyššia) | Presná zhoda EAN kódu |
| `seller_code` | 2 | Zhoda kódu dodávateľa |
| `name` | 3 | Fuzzy matching názvu |
| `manual` | 4 | Manuálne priradenie operátorom |

---

## Triggery

- `tr_sih_updated_at` - Automatická aktualizácia `updated_at`
- `tr_sii_updated_at` - Automatická aktualizácia `updated_at`
- `tr_sii_update_head_stats` - Aktualizácia štatistík v hlavičke pri zmene položiek

---

## Unique constraints

- `supplier_invoice_heads`: `(xml_supplier_ico, xml_invoice_number)` - deduplikácia faktúr
- `supplier_invoice_items`: `(invoice_head_id, xml_line_number)` - unikátne riadky

---

**Súvisiace dokumenty:**
- ISH-supplier_invoice_heads.md (migrácia z Btrieve)
- ISI-supplier_invoice_items.md (migrácia z Btrieve)