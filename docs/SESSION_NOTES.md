# NEX Automat - Session Notes

**Date:** 2025-11-27  
**Project:** nex-automat  
**Location:** C:/Development/nex-automat  
**Session:** NEX Shared Package Creation - Btrieve Models ✅

---

## 🎯 Session Summary

**Status:** ✅ **COMPLETE SUCCESS**

Vytvorený a nainštalovaný `nex-shared` package s Btrieve modelmi (TSH, TSI), BtrieveClient wrapper a BaseRepository pre NEX Automat projekt.

---

## ✅ What Was Completed

### 1. Package Structure ✅
```
packages/nex-shared/
├── nex_shared/
│   ├── __init__.py                     # Main exports
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tsh.py                      # TSH model (7KB)
│   │   └── tsi.py                      # TSI model (6.8KB)
│   ├── btrieve/
│   │   ├── __init__.py
│   │   └── btrieve_client.py           # Btrieve wrapper (5.5KB)
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base_repository.py          # Repository pattern (2.8KB)
│   └── utils/
│       └── __init__.py
├── pyproject.toml
└── README.md
```

### 2. Btrieve Models ✅

**TSHRecord** (Dodacie listy - Header):
- ✅ Primary key: doc_number
- ✅ Document info: doc_type, doc_date, delivery_date, due_date
- ✅ Partner: pab_code, pab_name, pab_address, IČO, DIČ, IČ DPH
- ✅ Financial: currency, exchange_rate, amounts (base, VAT, total)
- ✅ VAT breakdown: 20%, 10%, 0% rates
- ✅ Payment: method, terms, paid status, dates
- ✅ References: invoice_number, order_number, notes
- ✅ Status: status, locked, posted, warehouse_code
- ✅ Audit: mod_user, mod_date, created_date
- ✅ Deserialization from Btrieve bytes (cp852 encoding)
- ✅ Delphi date conversion
- ✅ Validation method

**TSIRecord** (Dodacie listy - Items):
- ✅ Composite key: doc_number + line_number
- ✅ Product: gs_code, gs_name, bar_code
- ✅ Quantity: quantity, unit, unit_coef
- ✅ Pricing: price_unit, price_unit_vat, vat_rate, discount_percent
- ✅ Line totals: line_base, line_vat, line_total
- ✅ Stock: warehouse_code, batch_number, serial_number
- ✅ Additional: note, supplier_item_code, status
- ✅ Audit: mod_user, mod_date, mod_time
- ✅ Deserialization from Btrieve bytes
- ✅ Calculate line totals method
- ✅ Validation method

### 3. BtrieveClient ✅

**32-bit Pervasive PSQL Wrapper:**
- ✅ DLL loading (w3btrv7.dll, wbtrv32.dll)
- ✅ BTRCALL signature configuration
- ✅ Operation codes: OPEN, CLOSE, INSERT, UPDATE, DELETE, GET_FIRST, GET_NEXT
- ✅ Status codes: SUCCESS, FILE_NOT_OPEN, KEY_NOT_FOUND, etc.
- ✅ open_file() method (read-only mode default)
- ✅ close_file() method
- ✅ get_first() method
- ✅ get_next() method
- ✅ get_status_message() helper

### 4. BaseRepository ✅

**Repository Pattern:**
- ✅ Generic type support
- ✅ Abstract methods: table_name, from_bytes
- ✅ open() / close() methods
- ✅ get_first() / get_next() methods
- ✅ get_all() method (max 10,000 records)
- ✅ Error handling and logging

### 5. Installation & Testing ✅

**Package Installation:**
- ✅ Created pyproject.toml with hatchling build system
- ✅ Installed via `pip install -e packages/nex-shared`
- ✅ Editable mode working
- ✅ Added to Python path via .pth file

**Import Tests:**
```python
from nex_shared import BtrieveClient, TSHRecord, TSIRecord
✅ All imports successful
✅ Basic functionality OK
```

### 6. Scripts Created ✅

**Setup Scripts:**
1. `scripts/setup_nex_shared_package.py` - Initial setup (obsolete)
2. `scripts/create_nex_shared_files.py` - Creates all Python files ✅
3. `scripts/install_nex_shared.py` - Installation script (obsolete)
4. `scripts/reinstall_nex_shared.py` - Reinstall helper ✅
5. `scripts/test_nex_shared_import.py` - Import verification ✅

**Diagnostic Scripts:**
6. `scripts/diagnose_nex_shared.py` - Package diagnostics
7. `scripts/diagnose_site_packages.py` - Site-packages investigation ✅

---

## 🔧 Technical Details

### Source of Models

Models prenesené z **nex-genesis-server** projektu:
- ✅ `src/models/tsh.py` → `nex_shared/models/tsh.py`
- ✅ `src/models/tsi.py` → `nex_shared/models/tsi.py`
- ✅ `src/btrieve/btrieve_client.py` → `nex_shared/btrieve/btrieve_client.py`
- ✅ `src/repositories/base_repository.py` → `nex_shared/repositories/base_repository.py`

**Why reuse?**
- ✅ Overené a otestované v nex-genesis-server
- ✅ Správne field offsety a deserialization
- ✅ Fungujúce s 32-bit Pervasive Btrieve API
- ✅ Konzistentná implementácia naprieč projektami

### Installation Issues Resolved

**Problem 1:** Package installed but import failed
- **Cause:** `nex_shared/` directory missing
- **Fix:** Created all Python files via `create_nex_shared_files.py`

**Problem 2:** Empty .pth file
- **Cause:** No Python package in directory during install
- **Fix:** Reinstall after creating all files

### Python Environment

- **Version:** Python 3.13.7 32-bit
- **Virtual Env:** venv32 (C:/Development/nex-automat/venv32/)
- **Reason:** Btrieve requires 32-bit Python
- **Package Manager:** pip (editable installs)

### Key Dependencies

**nex-shared:**
- pyyaml>=6.0.0 ✅

**Required for Btrieve:**
- Pervasive PSQL 11.30 (w3btrv7.dll)
- 32-bit Python environment

---

## 📊 Project Status

### Monorepo Structure

```
C:/Development/nex-automat/
├── apps/
│   ├── supplier-invoice-loader/        # FastAPI service
│   └── supplier-invoice-editor/        # PyQt5 GUI
├── packages/
│   ├── invoice-shared/                 # ✅ Working
│   └── nex-shared/                     # ✅ NEW - Working
├── docs/
│   ├── SESSION_NOTES.md
│   └── strategy/
│       ├── TERMINOLOGY.md
│       ├── CURRENT_STATE.md
│       ├── VISION.md
│       ├── ARCHITECTURE.md
│       ├── REQUIREMENTS.md
│       └── ROADMAP.md
├── scripts/
│   ├── create_nex_shared_files.py      # ✅ Working
│   ├── reinstall_nex_shared.py         # ✅ Working
│   ├── test_nex_shared_import.py       # ✅ Working
│   └── diagnose_site_packages.py       # ✅ Working
├── venv32/                             # Python 3.13.7 32-bit
├── pyproject.toml                      # UV workspace config
└── README.md
```

### Implementation Roadmap

```
FÁZA 1: Email → Staging → GUI Zobrazenie     ✅ COMPLETE
FÁZA 2: GO-LIVE Preview/Demo                 ✅ COMPLETE (2025-11-27)
FÁZA 3: Btrieve Models (TSH, TSI, PLS, RPC)  🟡 IN PROGRESS
  ├── ✅ nex-shared package created
  ├── ✅ TSH model (Dodacie listy - Header)
  ├── ✅ TSI model (Dodacie listy - Items)
  ├── ✅ BtrieveClient wrapper
  ├── ✅ BaseRepository pattern
  ├── ⚪ TODO: Add nex-shared to apps dependencies
  ├── ⚪ TODO: Create TSH/TSI repositories in apps
  ├── ⚪ TODO: PLS model (Cenníky)
  └── ⚪ TODO: RPC model (Požiadavky na zmenu ceny)
FÁZA 4: GUI Editácia + Farebné rozlíšenie    ⚪ TODO
FÁZA 5: Vytvorenie produktových kariet       ⚪ TODO
FÁZA 6: Zaevidovanie dodávateľského DL       ⚪ TODO
FÁZA 7: Požiadavky na zmenu cien             ⚪ TODO
FÁZA 8: Testovanie + Production Hardening    ⚪ TODO
FÁZA 9: Ďalší zákazníci + Rozšírenia         ⚪ FUTURE
```

### Btrieve Tabuľky Status

| Tabuľka | Súbor | Model | READ | WRITE | Status |
|---------|-------|-------|------|-------|--------|
| GSCAT | GSCAT.BTR | ✅ | ✅ | ⚪ | In invoice-shared |
| BARCODE | BARCODE.BTR | ✅ | ✅ | ⚪ | In invoice-shared |
| PAB | PAB.BTR | ✅ | ✅ | — | In invoice-shared |
| MGLST | MGLST.BTR | ✅ | ✅ | — | In invoice-shared |
| **TSH** | **TSHA-001.BTR** | **✅** | **⚪** | **⚪** | **NEW in nex-shared** |
| **TSI** | **TSIA-001.BTR** | **✅** | **⚪** | **⚪** | **NEW in nex-shared** |
| PLS | PLSnnnnn.BTR | ⚪ | ⚪ | — | TODO |
| RPC | RPCnnnnn.BTR | ⚪ | ⚪ | ⚪ | TODO |

---

## 📋 Next Steps

### Priority 1: Integration (Next Session)

**Add nex-shared to Apps:**
1. Update `supplier-invoice-loader/pyproject.toml`:
   ```toml
   dependencies = [
       ...
       "nex-shared",
   ]
   ```

2. Update `supplier-invoice-editor/pyproject.toml`:
   ```toml
   dependencies = [
       ...
       "nex-shared",
   ]
   ```

3. Reinstall apps:
   ```bash
   pip install -e apps/supplier-invoice-loader
   pip install -e apps/supplier-invoice-editor
   ```

### Priority 2: Repositories

**Create TSH/TSI Repositories:**
1. `supplier-invoice-loader/src/repositories/tsh_repository.py`
2. `supplier-invoice-loader/src/repositories/tsi_repository.py`
3. Test čítanie dokladov z NEX Genesis

### Priority 3: PLS & RPC Models

**Create Additional Models:**
1. PLS model (Cenníky) - pre editáciu cien
2. RPC model (Požiadavky na zmenu ceny) - pre workflow

### Priority 4: GUI Integration

**Supplier Invoice Editor:**
1. Zobrazenie TSH/TSI záznamov v GUI
2. Editácia položiek dokladov
3. Farebné rozlíšenie stavov
4. Validácia pred zápisom

---

## 💡 Lessons Learned

### 1. Package Installation Issues

**Problem:** Editable install without Python files
**Lesson:** Always verify directory structure before pip install
**Solution:** Create all files first, then install

### 2. .pth File Behavior

**Problem:** Empty .pth file if no Python package exists
**Lesson:** pip install needs valid Python package to create .pth entry
**Solution:** Package must have `__init__.py` before install

### 3. Reusing Existing Code

**Success:** Reusing tested models from nex-genesis-server
**Benefit:** Saved hours of development and testing
**Approach:** Copy-paste with import path updates

### 4. Diagnostic Scripts

**Value:** Diagnostic scripts critical for troubleshooting
**Examples:** diagnose_site_packages.py revealed .pth issue
**Best Practice:** Create diagnostics early when issues arise

### 5. Step-by-Step Workflow

**Approach:** Create → Install → Test → Iterate
**Success:** Systematic approach identified and fixed all issues
**Tools:** Separate scripts for each step (create, reinstall, test)

---

## 🎉 Session Achievements

**Created:**
- ✅ Complete nex-shared package structure
- ✅ TSH model (Dodacie listy - Header) - 7KB
- ✅ TSI model (Dodacie listy - Items) - 6.8KB
- ✅ BtrieveClient wrapper - 5.5KB
- ✅ BaseRepository pattern - 2.8KB
- ✅ 7 helper scripts for setup/testing

**Tested:**
- ✅ Package installation (editable mode)
- ✅ Import verification
- ✅ Basic functionality
- ✅ Model creation

**Documented:**
- ✅ README.md with usage examples
- ✅ Comprehensive session notes
- ✅ Next steps clearly defined

---

## 🔗 Related Projects

**nex-genesis-server:**
- Source of Btrieve models
- Location: C:/Development/nex-genesis-server
- GitHub: rauschiccsk/nex-genesis-server

**nex-automat:**
- Current project (monorepo)
- Location: C:/Development/nex-automat
- GitHub: rauschiccsk/nex-automat
- Version: 2.0.0

---

## 📊 Statistics

**Files Created:** 9 Python files
**Total Code:** ~22KB
**Scripts:** 7 helper scripts
**Session Duration:** ~1.5 hours
**Tokens Used:** ~110k / 190k
**Status:** ✅ 100% Success

---

**Last Updated:** 2025-11-27 (Session Complete)  
**Next Session:** Integration of nex-shared into apps  
**Status:** 🎯 **READY FOR INTEGRATION**