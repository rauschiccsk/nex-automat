#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update All Index Files - NEX Automat
Location: C:/Development/nex-automat/scripts/update_all_indexes.py

Aktualizuje všetky 00_*_INDEX.md súbory podľa aktuálneho stavu dokumentácie.
"""

from pathlib import Path
from datetime import datetime

# Konfigurácia
MONOREPO_ROOT = Path("C:/Development/nex-automat")
DOCS_ROOT = MONOREPO_ROOT / "docs"

# Index obsahy
INDEXES = {
    "strategic/00_STRATEGIC_INDEX.md": """# Strategic Documentation Index

**Kategória:** Strategic  
**Status:** 🟢 Complete  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Strategická dokumentácia obsahuje dlhodobé plány, víziu projektu, technologické rozhodnutia a roadmap.

---

## Dokumenty v Strategic

### Kompletné Dokumenty

**[AI_ML_TECHNOLOGIES.md](AI_ML_TECHNOLOGIES.md)**
- Schválené AI/ML technológie (PaddleOCR, Camelot, Claude API, DuckDB)
- Implementačný plán, náklady, benefity
- Status: 🟢 Complete
- Veľkosť: ~26 KB, 841 riadkov

**[PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)**
- Kompletný roadmap NEX Automat projektu
- Fázy, milestones, časový harmonogram
- Status: 🟢 Complete
- Veľkosť: ~15 KB, 476 riadkov

**[PROJECT_VISION.md](PROJECT_VISION.md)**
- Vízia a ciele projektu
- Long-term stratégia
- Status: 🟢 Complete
- Veľkosť: ~14 KB, 443 riadkov

**[QUICK_WINS_TECHNOLOGIES.md](QUICK_WINS_TECHNOLOGIES.md)**
- Quick win technológie a implementácie
- Status: 🟢 Complete
- Veľkosť: ~19 KB, 606 riadkov

**[N8N_TO_TEMPORAL_MIGRATION.md](N8N_TO_TEMPORAL_MIGRATION.md)**
- Migrácia z n8n na Temporal workflow orchestration
- Architektúra, implementation roadmap, risks
- Status: 📋 Planned
- Veľkosť: ~12 KB

### Draft Dokumenty

**[TECHNOLOGY_DECISIONS.md](TECHNOLOGY_DECISIONS.md)**
- História technologických rozhodnutí
- Status: 🔴 Draft
- Potrebuje: Doplniť obsah

---

## Quick Links

**Pre plánovanie:**
- [Project Roadmap](PROJECT_ROADMAP.md) - Časový plán projektu
- [Project Vision](PROJECT_VISION.md) - Dlhodobá vízia

**Pre technológie:**
- [AI/ML Technologies](AI_ML_TECHNOLOGIES.md) - Schválené AI/ML nástroje
- [Quick Wins](QUICK_WINS_TECHNOLOGIES.md) - Quick win implementácie
- [N8N to Temporal](N8N_TO_TEMPORAL_MIGRATION.md) - Workflow orchestration migration
- [Technology Decisions](TECHNOLOGY_DECISIONS.md) - História rozhodnutí

---

## Štatistika

- **Total dokumentov:** 6
- **Complete:** 4
- **Planned:** 1
- **Draft:** 1
- **Total veľkosť:** ~86 KB

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Architecture](../system/ARCHITECTURE.md) - Technická architektúra
""",

    "database/00_DATABASE_INDEX.md": """# Database Documentation Index

**Kategória:** Database  
**Status:** 🟢 Complete  
**Vytvorené:** 2025-12-15  
**Aktualizované:** 2025-12-15

---

## Účel

Databázová dokumentácia obsahuje schémy, mappingy NEX Genesis → NEX Automat, migration dokumenty a detailné popisy tabuliek.

---

## Hlavné Dokumenty

### Kompletné Dokumenty

**[DATABASE_PRINCIPLES.md](DATABASE_PRINCIPLES.md)**
- Design principles, naming conventions
- Status: 🟢 Complete
- Veľkosť: ~24 KB, 985 riadkov

**[MIGRATION_MAPPING.md](MIGRATION_MAPPING.md)**
- Btrieve → PostgreSQL mapping
- Status: 🟢 Complete
- Veľkosť: ~23 KB, 657 riadkov

**[RELATIONSHIPS.md](RELATIONSHIPS.md)**
- Relationships medzi tabuľkami
- Status: 🟢 Complete
- Veľkosť: ~24 KB, 707 riadkov

**Reference dokumenty:**
- [CATALOGS_REFERENCE.md](CATALOGS_REFERENCE.md) - ~7 KB, 244 riadkov
- [PARTNERS_REFERENCE.md](PARTNERS_REFERENCE.md) - ~8 KB, 270 riadkov
- [PRODUCTS_REFERENCE.md](PRODUCTS_REFERENCE.md) - ~6 KB, 209 riadkov
- [SALES_REFERENCE.md](SALES_REFERENCE.md) - ~8 KB, 305 riadkov
- [STOCK_REFERENCE.md](STOCK_REFERENCE.md) - ~3 KB, 119 riadkov
- [STOCK_CARDS_REFERENCE.md](STOCK_CARDS_REFERENCE.md) - ~20 KB, 580 riadkov

---

## Database Table Documentation

### Partners Section (9 dokumentov) ✅ COMPLETE

**Location:** `catalogs/partners/tables/`

1. **BANKLST-bank_catalog.md** (~8 KB) - Číselník bánk
2. **PAB-partner_catalog.md** (~20 KB) - Katalóg partnerov
3. **PABACC-partner_catalog_bank_accounts.md** (~10 KB) - Bankové účty
4. **PACNCT-partner_catalog_contacts.md** (~13 KB) - Kontaktné osoby
5. **PAGLST-partner_categories.md** (~7 KB) - Kategórie partnerov
6. **PAYLST-payment_methods.md** (~6 KB) - Spôsoby platby
7. **TRPLST-transport_methods.md** (~6 KB) - Spôsoby dopravy
8. **PANOTI-partner_catalog_texts.md** (~7 KB) - Texty partnerov
9. **PASUBC-partner_catalog_facilities.md** (~8 KB) - Prevádzky partnerov

### Products Section (5 dokumentov) ✅ COMPLETE

**Location:** `catalogs/products/tables/`

1. **BARCODE-product_catalog_identifiers.md** (~11 KB) - Identifikátory produktov
2. **FGLST-product_categories.md** (~8 KB) - Kategórie F
3. **GSCAT-product_catalog.md** (~15 KB) - Katalóg produktov
4. **MGLST-product_categories.md** (~10 KB) - Kategórie M
5. **SGLST-product_categories.md** (~12 KB) - Kategórie S

### Stock Management Section (7 dokumentov) ✅ COMPLETE

**Location:** `stock/cards/tables/` a `stock/documents/tables/`

1. **WRILST-facilities.md** (~9 KB) - Sklady
2. **STKLST-stocks.md** (~9 KB) - Číselník skladov
3. **TSH-supplier_delivery_heads.md** (~15 KB) - Hlavičky dodacích listov
4. **FIF-stock_card_fifos.md** (~12 KB) - FIFO skladových kariet
5. **TSI-supplier_delivery_items.md** (~16 KB) - Položky dodacích listov
6. **STM-stock_card_movements.md** (~15 KB) - Pohyby skladových kariet
7. **STK-stock_cards.md** (~19 KB) - Skladové karty

### Accounting Section (3 dokumenty) ✅ COMPLETE

**Location:** `accounting/tables/`

1. **ISH-supplier_invoice_heads.md** (~22 KB) - Hlavičky faktúr
2. **ISI-supplier_invoice_items.md** (~21 KB) - Položky faktúr
3. **PAYJRN-payment_journal.md** (~18 KB) - Platobný denník

### Sales Section (1 dokument) ✅ COMPLETE

**Location:** `sales/tables/`

1. **PLSnnnnn-price_list_items.md** (~11 KB) - Položky cenníkov

---

## Štatistika

**Database Table Docs:**
- ✅ Partners: 9/9 (100%)
- ✅ Products: 5/5 (100%)
- ✅ Stock Management: 7/7 (100%)
- ✅ Accounting: 3/3 (100%)
- ✅ Sales: 1/1 (100%)
- **TOTAL: 25/25 (100%)** 🎉

**Reference Docs:** 11 dokumentov (100%)

**Total:** 36 kompletných dokumentov

---

## Quick Links

**Katalógy:**
- [Partners Tables](catalogs/partners/tables/) - 9 dokumentov
- [Products Tables](catalogs/products/tables/) - 5 dokumentov

**Doklady:**
- [Stock Cards](stock/cards/tables/) - 5 dokumentov
- [Stock Documents](stock/documents/tables/) - 2 dokumenty
- [Accounting](accounting/tables/) - 3 dokumenty
- [Sales](sales/tables/) - 1 dokument

**Reference:**
- [Database Principles](DATABASE_PRINCIPLES.md)
- [Migration Mapping](MIGRATION_MAPPING.md)
- [Relationships](RELATIONSHIPS.md)

---

**See Also:**
- [Documentation Index](../00_DOCUMENTATION_INDEX.md) - Hlavný index
- [System Architecture](../system/ARCHITECTURE.md) - Systémová architektúra
""",

    "archive/00_ARCHIVE_INDEX.md": """# Archive Index

**Last Updated:** 2025-12-15  
**Purpose:** Index všetkých archivovaných dokumentov  

---

## SESSION ARCHIVES

### December 2025

**2025-12-15 - Database Table Docs Batch 6 (FINAL):**
- [Database Table Docs - Batch 6 Sales Final](sessions/SESSION_2025-12-15_database-table-docs-batch6-sales-final.md)
  - Status: ✅ COMPLETE
  - Topics: Sales section complete (PLSnnnnn)
  - Progress: 24/28 dokumentov (85.7%)
  - **ALL DATABASE TABLE DOCS COMPLETE!** 🎉

- [Database Table Docs - Batch 6 Accounting Complete](sessions/SESSION_2025-12-15_database-table-docs-batch6-accounting-complete.md)
  - Status: ✅ COMPLETE
  - Topics: Accounting section complete (ISH, ISI, PAYJRN)
  - Progress: 23/28 dokumentov (82.1%)

- [Database Table Docs - Batch 6 Stock Complete](sessions/SESSION_2025-12-15_database-table-docs-batch6-stock-complete.md)
  - Status: ✅ COMPLETE
  - Topics: Stock Management complete (STM, STK)
  - Progress: 20/28 dokumentov (71.4%)

- [Database Table Docs - Batch 6 Stock Management](sessions/SESSION_2025-12-15_database-table-docs-batch6-stock-management.md)
  - Status: ✅ COMPLETE
  - Topics: Stock Management section (WRILST, STKLST, TSH, FIF, TSI)
  - Progress: 18/28 dokumentov (64.3%)

- [Database Table Docs - Batch 6 Products](sessions/SESSION_2025-12-15_database-table-docs-batch6-products.md)
  - Status: ✅ COMPLETE
  - Topics: Products section (BARCODE, FGLST, GSCAT, MGLST, SGLST)
  - Progress: 13/28 dokumentov (46.4%)

- [Database Table Docs - Batch 6 Partners](sessions/SESSION_2025-12-15_database-table-docs-batch6-partners.md)
  - Status: ✅ COMPLETE
  - Topics: Partners section (PAGLST, PAYLST, TRPLST, PANOTI, PASUBC)
  - Progress: 8/28 dokumentov

- [Database Table Docs - Batch 6 Start](sessions/SESSION_2025-12-15_database-table-docs-batch6-start.md)
  - Status: ✅ COMPLETE
  - Topics: BANKLST, PAB, PABACC, PACNCT

**2025-12-15 - Documentation Migration:**
- [Documentation Migration - Batch 5](sessions/SESSION_2025-12-15_documentation-migration-batch5.md)
  - Status: ✅ COMPLETE
  - Topics: Database indexes (7 dokumentov)

- [Documentation Migration - Batch 4](sessions/SESSION_2025-12-15_documentation-migration-batch4.md)
  - Status: ✅ COMPLETE
  - Topics: Database docs (3 dokumenty)

- [Documentation Migration - Batch 3](sessions/SESSION_2025-12-15_documentation-migration-batch3.md)
  - Status: ✅ COMPLETE
  - Topics: Database docs (6 dokumentov)

- [Documentation Migration - Batch 2](sessions/SESSION_2025-12-15_documentation-migration-batch2.md)
  - Status: ✅ COMPLETE
  - Topics: Database general (4 dokumenty)

**2025-12-09:**
- [v2.4 Implementation Complete](sessions/SESSION_2025-12-09_v24-implementation-complete.md)
  - Status: ✅ COMPLETE
  - Topics: Product enrichment, implementation

- [v2.4 Phase 4 Deployment](sessions/SESSION_2025-12-09_v24-phase4-deployment.md)
  - Status: ✅ COMPLETE
  - Topics: Production deployment

**2025-12-08:**
- [v2.4 Product Enrichment](sessions/SESSION_2025-12-08_v24-product-enrichment.md)
  - Status: ✅ COMPLETE
  - Topics: EAN matching, product enrichment

- [v2.3 Loader Migration](sessions/SESSION_2025-12-08_v23-loader-migration.md)
  - Status: ✅ COMPLETE
  - Topics: Loader architecture

- [v2.2 Cleanup & Mágerstav Deployment Attempt](sessions/SESSION_2025-12-08_v22-cleanup-mágerstav-deployment-attempt.md)
  - Status: ✅ COMPLETE
  - Topics: Code cleanup, deployment

- [Documentation Restructure v2.3 Planning](sessions/SESSION_2025-12-08_documentation-restructure-v23-planning.md)
  - Status: ✅ COMPLETE
  - Topics: Documentation structure

**2025-12-06:**
- [BaseGrid Persistence Implementation](sessions/SESSION_2025-12-06_basegrid-persistence-implementation.md)
  - Status: ✅ COMPLETE
  - Topics: Grid persistence

---

## DEPLOYMENT ARCHIVES

### Mágerstav Deployments

**2025-12-02:**
- [User Guide](deployments/USER_GUIDE_MAGERSTAV_2025-12-02.md)

**2025-11-29:**
- [Deployment](deployments/DEPLOYMENT_MAGERSTAV_2025-11-29.md)

**2025-11-27:**
- [Deployment Guide](deployments/DEPLOYMENT_GUIDE_MAGERSTAV_2025-11-27.md)
- [Training Guide](deployments/TRAINING_GUIDE_MAGERSTAV_2025-11-27.md)
- [Pre-Deployment Checklist](deployments/PRE_DEPLOYMENT_CHECKLIST_MAGERSTAV_2025-11-27.md)
- [Checklist](deployments/CHECKLIST_MAGERSTAV_2025-11-27.md)

**2025-11-24:**
- [Operations Guide](deployments/OPERATIONS_GUIDE_MAGERSTAV_2025-11-24.md)
- [Recovery Procedures](deployments/RECOVERY_PROCEDURES_MAGERSTAV_2025-11-24.md)

**2025-11-21:**
- [Recovery Guide](deployments/RECOVERY_GUIDE_MAGERSTAV_2025-11-21.md)
- [Troubleshooting](deployments/TROUBLESHOOTING_MAGERSTAV_2025-11-21.md)

---

## PROJECT STATUS ARCHIVES

**2025-12-02:**
- [Project Status v2.1](PROJECT_STATUS_v2.1_2025-12-02.md)

**2025-11-26:**
- [Current State](CURRENT_STATE_2025-11-26.md)

---

## STATISTICS

**Total Sessions:** 25+ (včetne Database Table Docs Batch 6)  
**Total Deployments:** 10  
**Completed Milestones:** 
- ✅ Database Table Documentation (25/25 - 100%)
- ✅ Strategic Documentation (N8N to Temporal migration added)

---

**Last Updated:** 2025-12-15  
**Maintainer:** Zoltán & Claude
"""
}


def main():
    """Hlavná funkcia scriptu"""
    print("=" * 80)
    print("📋 AKTUALIZÁCIA VŠETKÝCH INDEX SÚBOROV - NEX AUTOMAT")
    print("=" * 80)
    print()
    print(f"Monorepo: {MONOREPO_ROOT}")
    print(f"Docs:     {DOCS_ROOT}")
    print()

    # Aktualizuj indexy
    print("1️⃣ Aktualizácia index súborov...")
    print("=" * 80)

    updated_count = 0

    for relative_path, content in INDEXES.items():
        file_path = DOCS_ROOT / relative_path

        # Vytvor adresár ak neexistuje
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Ulož súbor
        file_path.write_text(content, encoding='utf-8')
        print(f"   ✅ Aktualizovaný: {relative_path}")
        updated_count += 1

    print()
    print(f"   Aktualizovaných indexov: {updated_count}")
    print()

    # Sumár
    print("=" * 80)
    print("✅ VŠETKY INDEXY AKTUALIZOVANÉ!")
    print("=" * 80)
    print()
    print("📊 Štatistika:")
    print(f"   Aktualizovaných súborov: {updated_count}")
    print()
    print("📋 Aktualizované indexy:")
    for relative_path in INDEXES.keys():
        print(f"   - {relative_path}")
    print()
    print("🎉 KEY MILESTONE:")
    print("   - Database Table Docs: 25/25 (100%) COMPLETE!")
    print("   - Strategic: N8N to Temporal migration added")
    print()
    print("📄 Ďalší krok:")
    print("   1. git add docs/")
    print('   2. git commit -m "docs: Update indexes - database tables complete, strategic migration added"')
    print("   3. git push origin develop")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()