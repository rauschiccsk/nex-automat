# Document Types

**Category:** Documents  
**Status:** 🟢 Complete  
**Created:** 2024-12-12  
**Updated:** 2025-12-15  
**Source:** COMMON_DOCUMENT_PRINCIPLES.md

---

## Overview

NEX Automat supports **22 document types**, each with unique two-letter code and English name.

---

## 0. TYPY DOKLADOV

NEX Automat podporuje **22 typov dokladov**, každý s jedinečným dvojpísmenovým kódom a anglickým názvom.

### 0.1 Dodávateľské doklady (3)

| Kód | Názov | Popis |
|-----|-------|-------|
| DD | `supplier_delivery` | Dodávateľský dodací list |
| DF | `supplier_invoice` | Dodávateľská faktúra |
| OB | `supplier_order` | Dodávateľská objednávka |

### 0.2 Odberateľské doklady (4)

| Kód | Názov | Popis |
|-----|-------|-------|
| OD | `customer_delivery` | Odberateľský dodací list |
| OF | `customer_invoice` | Odberateľská faktúra |
| ZK | `customer_order` | Odberateľská objednávka |
| CP | `customer_quote` | Odberateľská ponuka |

### 0.3 Účtovné a finančné doklady (5)

| Kód | Názov | Popis |
|-----|-------|-------|
| ID | `internal_accounting` | Interné účtovné doklady |
| BV | `bank_statement` | Bankový výpis |
| PQ | `payment_order` | Prevodný príkaz |
| PV | `cash_withdrawal` | Pokladničný výdaj |
| PP | `cash_receipt` | Pokladničný príjem |

### 0.4 Skladové doklady (7)

| Kód | Názov | Popis |
|-----|-------|-------|
| SV | `stock_issue` | Interná skladová výdajka |
| SP | `stock_receipt` | Interná skladová príjemka |
| MP | `stock_transfer` | Medziskladový presun |
| MB | `stock_repackaging` | Prebalenie tovaru (kartón → kusy, PLU-11 → PLU-10) |
| DK | `stock_assembly` | Kompletizácia (sady, balíčky, darčekové koše) |
| SA | `cash_register_stock_issue` | Výdajka predaja reg. pokladníc |
| IV | `stock_inventory` | Inventarizácia skladov |

### 0.5 Výrobné doklady (1)

| Kód | Názov | Popis |
|-----|-------|-------|
| CD | `production` | Výrobný doklad |

### 0.6 Majetok (1)

| Kód | Názov | Popis |
|-----|-------|-------|
| IM | `asset_management` | Evidencia majetku |

### 0.7 Použitie v document_type

```sql
-- Každý doklad má document_type
document_type VARCHAR(20) NOT NULL CHECK (
    document_type IN (
        'supplier_delivery', 'supplier_invoice', 'supplier_order',
        'customer_delivery', 'customer_invoice', 'customer_order', 'customer_quote',
        'internal_accounting', 'bank_statement', 'payment_order', 'cash_withdrawal', 'cash_receipt',
        'stock_issue', 'stock_receipt', 'stock_transfer', 'stock_repackaging', 
        'stock_assembly', 'cash_register_stock_issue', 'stock_inventory',
        'production',
        'asset_management'
    )
)
```

---

---

**See Also:**
- [NUMBERING.md](NUMBERING.md) - Document numbering system
- [WORKFLOWS.md](WORKFLOWS.md) - Document workflows
