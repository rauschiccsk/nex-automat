# Session Notes - NEX Automat Integration

**Date:** 2025-11-27  
**Session:** nexdata Package Creation & Repository Integration  
**Status:** 🟡 IN PROGRESS - Btrieve Config Lookup Needed

---

## What Was Completed ✅

### 1. Package Rename: nex-shared → nexdata
- **Problem:** Mätúci názov `nex-shared` vs `nex_shared` (package vs module)
- **Solution:** Premenovanie na `nexdata` (jednoznačný, bez konfúzie)
- **Structure:**
  ```
  packages/nexdata/
  └── nexdata/              ← Python module
      ├── __init__.py
      ├── models/           ← 6 models
      ├── btrieve/          ← BtrieveClient
      └── repositories/     ← 7 repositories
  ```

### 2. Models Migration
Úspešne prenесené z nex-genesis-server:
- ✅ TSH (Dodacie listy - Header)
- ✅ TSI (Dodacie listy - Items)
- ✅ GSCAT (Katalóg produktov)
- ✅ BARCODE (Čiarové kódy)
- ✅ PAB (Obchodní partneri)
- ✅ MGLST (Tovarové skupiny)

### 3. Repositories Created
Vytvorené pre všetky modely:
- `tsh_repository.py` - Dodacie listy header
- `tsi_repository.py` - Dodacie listy items
- `gscat_repository.py` - Produktový katalóg
- `barcode_repository.py` - Čiarové kódy
- `pab_repository.py` - Obchodní partneri
- `mglst_repository.py` - Tovarové skupiny

**Pridané metódy:**
```python
def to_bytes(self, record) -> bytes:
    return record.to_bytes()
```

### 4. Import Fixes
- Opravené importy: `nex_shared` → `nexdata`
- Opravené class names: `BARCODERecord` → `BarcodeRecord`
- Opravený BtrieveClient `__init__`: `if config_or_path:` → `if config_or_path is not None:`

### 5. Dependencies Updated
```toml
# apps/supplier-invoice-loader/pyproject.toml
# apps/supplier-invoice-editor/pyproject.toml
dependencies = [
    ...
    "nexdata",  # ← updated
]
```

### 6. Btrieve Testing
- ✅ Btrieve DLL loaded: `w3btrv7.dll`
- ✅ Pervasive PSQL service running
- ✅ Files exist and accessible
- ❌ Status 161 on open - **Config lookup missing**

---

## Current Problem ⚠️

### Issue: Btrieve Status 161 (File Not Found)

**Root Cause Identified:**

**nex-genesis-server approach (WORKING):**
```python
# Repository
return 'gscat'  # ← just table name

# BtrieveClient uses config:
tables:
  gscat: "C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR"
```

**Current nex-automat approach (NOT WORKING):**
```python
# Repository
return "C:/NEX/YEARACT/STORES/GSCAT.BTR"  # ← filesystem path

# BtrieveClient receives empty config {}
```

**Problem:** Btrieve očakáva table names + config mapping, nie priame filesystem paths!

---

## Solution Plan 🎯

### Phase 1: BtrieveClient Config Lookup
1. Modify `BtrieveClient.open_file()` to support table name lookup:
   ```python
   def open_file(self, table_name_or_path: str, ...):
       # If config exists and table name in config
       if self.config and 'nex_genesis' in self.config:
           tables = self.config['nex_genesis']['tables']
           if table_name_or_path in tables:
               filepath = tables[table_name_or_path]
           else:
               filepath = table_name_or_path
       else:
           filepath = table_name_or_path
   ```

### Phase 2: Repository Updates
Change all repositories:
```python
# OLD
@property
def table_name(self) -> str:
    return "C:/NEX/YEARACT/STORES/GSCAT.BTR"

# NEW
@property
def table_name(self) -> str:
    return 'gscat'
```

### Phase 3: Config File
Create `config/database.yaml` with mappings:
```yaml
nex_genesis:
  tables:
    gscat: "C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR"
    barcode: "C:\\NEX\\YEARACT\\STORES\\BARCODE.BTR"
    mglst: "C:\\NEX\\YEARACT\\STORES\\MGLST.BTR"
    pab: "C:\\NEX\\YEARACT\\DIALS\\PAB00000.BTR"
    tsh: "C:\\NEX\\YEARACT\\STORES\\TSHA-001.BTR"
    tsi: "C:\\NEX\\YEARACT\\STORES\\TSIA-001.BTR"
```

### Phase 4: Test Scripts Update
Update test scripts to pass config:
```python
client = BtrieveClient(config_or_path="config/database.yaml")
```

---

## Files Modified This Session

### Created:
- `packages/nexdata/` - Complete package
- `packages/nexdata/nexdata/models/` - 6 models
- `packages/nexdata/nexdata/repositories/` - 7 repositories
- `scripts/test_tsh_tsi_read.py` - Test script
- `scripts/test_gscat_read.py` - GSCAT test
- `scripts/test_gscat_with_config.py` - Config test
- `scripts/diagnose_btrieve_paths.py` - Diagnostic
- Multiple fix scripts

### Modified:
- `packages/nexdata/nexdata/__init__.py` - Exports
- `packages/nexdata/nexdata/repositories/__init__.py` - Exports
- `packages/nexdata/nexdata/btrieve/btrieve_client.py` - Fixed __init__
- `apps/supplier-invoice-loader/pyproject.toml` - Dependencies
- `apps/supplier-invoice-editor/pyproject.toml` - Dependencies

### Deleted:
- `packages/invoice-shared/` - No longer needed

---

## Statistics

**Lines of Code:**
- Models: ~6,000 lines (6 files)
- Repositories: ~1,400 lines (7 files)
- Total new code: ~7,400 lines

**Test Results:**
- ✅ Import test: `from nexdata import *` - OK
- ✅ Btrieve DLL loading - OK
- ✅ Repository instantiation - OK
- ❌ Table open - Status 161 (config issue)

---

## Next Session Priorities

1. **HIGH:** Implement config lookup in BtrieveClient
2. **HIGH:** Update all repositories to use table names
3. **MEDIUM:** Create config/database.yaml
4. **MEDIUM:** Test read operations with config
5. **LOW:** GUI integration

---

## Technical Notes

### Python Environment
- Python 3.13.7 32-bit (venv32)
- Pervasive PSQL Workgroup Engine: Running
- Btrieve DLL: `w3btrv7.dll` from Pervasive Software

### Key Learnings
1. Btrieve používa config-based table name lookup
2. Filesystem paths directly nie sú podporované
3. Repository pattern needs alignment s nex-genesis-server
4. 32-bit Python je potrebný pre 32-bit Btrieve DLL

### Memory Updated
```
CRITICAL: nex-shared package uses FLAT structure - "nex-shared" 
appears ONLY ONCE in path: packages/nex-shared/models/ 
NOT packages/nex-shared/nex_shared/models/
```
Note: Package premenovaný na `nexdata`, flat structure zachovaná.

---

**Last Updated:** 2025-11-27 14:30  
**Next Session:** Config Lookup Implementation  
**Status:** 🟡 Ready for Phase 1