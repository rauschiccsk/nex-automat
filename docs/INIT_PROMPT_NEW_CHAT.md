# Init Prompt - Btrieve Config Lookup Implementation

**Projekt:** NEX Automat  
**Last Session:** 2025-11-27 (nexdata Package Creation)  
**This Session:** Btrieve Config Lookup + Read Operations  

---

## Quick Context

NEX Automat je projekt pre kompletnú automatizáciu podnikových procesov pre zákazníkov používajúcich NEX Genesis ERP.

**Aktuálny stav:**
- Version: 2.0.0 (tagged)
- GO-LIVE: ✅ COMPLETE (2025-11-27)
- nexdata Package: ✅ CREATED (last session)
- Btrieve Integration: 🟡 CONFIG LOOKUP NEEDED ← **HERE**

---

## What Was Completed Last Session ✅

### nexdata Package Creation
Úspešne vytvorený package s:
- ✅ 6 Btrieve models (TSH, TSI, GSCAT, BARCODE, PAB, MGLST)
- ✅ 7 Repositories s BaseRepository pattern
- ✅ BtrieveClient wrapper (32-bit Pervasive PSQL)
- ✅ Proper Python package structure

**Package Location:**
```
packages/nexdata/
└── nexdata/              ← Python module
    ├── __init__.py
    ├── models/
    │   ├── tsh.py
    │   ├── tsi.py
    │   ├── gscat.py
    │   ├── barcode.py
    │   ├── pab.py
    │   └── mglst.py
    ├── btrieve/
    │   └── btrieve_client.py
    └── repositories/
        ├── base_repository.py
        ├── tsh_repository.py
        ├── tsi_repository.py
        ├── gscat_repository.py
        ├── barcode_repository.py
        ├── pab_repository.py
        └── mglst_repository.py
```

### Current Problem Identified

**Btrieve Status 161 na všetkých open_file() pokusoch!**

**Root Cause:**
- Repositories vracajú filesystem paths: `"C:/NEX/YEARACT/STORES/GSCAT.BTR"`
- BtrieveClient.open_file() posiela path priamo do Btrieve DLL
- **Btrieve očakáva table names + config lookup!**

**Working approach (nex-genesis-server):**
```python
# Repository
@property
def table_name(self) -> str:
    return 'gscat'  # ← just name

# Config (database.yaml)
tables:
  gscat: "C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR"

# BtrieveClient resolves: 'gscat' → full path
```

**Current broken approach:**
```python
# Repository
@property
def table_name(self) -> str:
    return "C:/NEX/YEARACT/STORES/GSCAT.BTR"  # ← direct path

# BtrieveClient receives empty config {}
# Btrieve DLL cannot resolve path → Status 161
```

---

## Solution Implementation Plan

### Priority 1: BtrieveClient Config Lookup ⚡

**File:** `packages/nexdata/nexdata/btrieve/btrieve_client.py`

**Modify `open_file()` method:**
```python
def open_file(self, table_name_or_path: str, owner_name: str = "", mode: int = -2):
    """
    Open Btrieve file by table name or direct path
    
    If config exists and table_name_or_path is in config, use mapped path.
    Otherwise use table_name_or_path as direct filepath.
    """
    # Resolve table name to filepath
    filepath = self._resolve_table_path(table_name_or_path)
    
    # ... rest of open logic with filepath
```

**Add helper method:**
```python
def _resolve_table_path(self, table_name_or_path: str) -> str:
    """
    Resolve table name to filesystem path using config
    
    Args:
        table_name_or_path: Either table name (e.g. 'gscat') or direct path
        
    Returns:
        Filesystem path to .BTR file
    """
    # Check if config has table mapping
    if self.config and 'nex_genesis' in self.config:
        tables = self.config.get('nex_genesis', {}).get('tables', {})
        
        if table_name_or_path in tables:
            # It's a table name - resolve from config
            return tables[table_name_or_path]
    
    # It's already a path, or no config - use as-is
    return table_name_or_path
```

### Priority 2: Repository Updates

**Update all repositories to return table names:**

**Before:**
```python
@property
def table_name(self) -> str:
    return "C:/NEX/YEARACT/STORES/GSCAT.BTR"
```

**After:**
```python
@property
def table_name(self) -> str:
    return 'gscat'
```

**Files to update:**
- `gscat_repository.py` → `'gscat'`
- `barcode_repository.py` → `'barcode'`
- `mglst_repository.py` → `'mglst'`
- `pab_repository.py` → `'pab'`
- `tsh_repository.py` → `'tsh'` (dynamic: needs book_id)
- `tsi_repository.py` → `'tsi'` (dynamic: needs book_id)

**Note:** TSH/TSI sú dynamické - používajú `{book_id}` placeholder

### Priority 3: Database Config File

**Create:** `config/database.yaml`

**Content (from nex-genesis-server):**
```yaml
nex_genesis:
  root_path: "C:\\NEX"
  yearact_path: "C:\\NEX\\YEARACT"
  
  tables:
    gscat: "C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR"
    barcode: "C:\\NEX\\YEARACT\\STORES\\BARCODE.BTR"
    mglst: "C:\\NEX\\YEARACT\\STORES\\MGLST.BTR"
    pab: "C:\\NEX\\YEARACT\\DIALS\\PAB00000.BTR"
    
    # Dynamic tables (use {book_id} placeholder)
    tsh: "C:\\NEX\\YEARACT\\STORES\\TSHA-{book_id}.BTR"
    tsi: "C:\\NEX\\YEARACT\\STORES\\TSIA-{book_id}.BTR"
  
  books:
    delivery_notes_book: "001"
    book_type: "A"
```

### Priority 4: Test Scripts Update

**Update test scripts to use config:**
```python
# OLD
client = BtrieveClient(config_or_path={})

# NEW
client = BtrieveClient(config_or_path="config/database.yaml")
```

### Priority 5: Dynamic Book IDs for TSH/TSI

**TSH/TSI repositories need book_id:**
```python
class TSHRepository(BaseRepository[TSHRecord]):
    def __init__(self, btrieve_client: BtrieveClient, book_id: str = "001"):
        self.book_id = book_id
        super().__init__(btrieve_client)
    
    @property
    def table_name(self) -> str:
        return f'tsh-{self.book_id}'  # Will resolve via config
```

---

## Available Resources

### Test Scripts (Need Update)
- `scripts/test_tsh_tsi_read.py` - TSH/TSI integration test
- `scripts/test_gscat_read.py` - GSCAT simple test
- `scripts/test_gscat_with_config.py` - Config approach test
- `scripts/diagnose_btrieve_paths.py` - Path diagnostic

### Reference Implementation
- Location: `C:/Development/nex-genesis-server`
- Working BtrieveClient with config lookup
- Working repositories with table names
- database.yaml with mappings

### Environment
- Python: 3.13.7 32-bit (venv32)
- Btrieve DLL: w3btrv7.dll (Pervasive PSQL)
- Service: psqlWGE (Running ✅)

---

## How to Start This Session

1. **Load SESSION_NOTES.md** for full context
2. **Priority Order:**
   - **Start with:** BtrieveClient config lookup implementation
   - **Then:** Update repositories to use table names
   - **Then:** Create config/database.yaml
   - **Finally:** Test read operations

3. **Follow workflow:**
   - Development → Test → Git
   - Jeden krok naraz
   - Testovať po každej zmene

---

## Expected Outcomes

Po dokončení tejto session:
- ✅ BtrieveClient podporuje config lookup
- ✅ Všetky repositories používajú table names
- ✅ config/database.yaml vytvorený
- ✅ Test read operations fungujú
- ✅ Môžeme čítať z GSCAT, TSH, TSI, PAB, atď.

---

## Important Technical Notes

### Btrieve Status Codes
- **0** = SUCCESS
- **161** = File not found / Invalid path
- **3** = File not open

### Path Formats
```python
# Windows paths - any format works:
"C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR"  # Escaped
r"C:\NEX\YEARACT\STORES\GSCAT.BTR"     # Raw string
"C:/NEX/YEARACT/STORES/GSCAT.BTR"      # Forward slash
```

### Config Resolution Logic
```
Input: 'gscat'
 ↓
Check config['nex_genesis']['tables']['gscat']
 ↓
Found: "C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR"
 ↓
Use this path
```

---

**Last Updated:** 2025-11-27 14:30  
**Version:** 1.0  
**Status:** 🟢 Ready for Implementation  
**Difficulty:** ⚡ Medium (Clear path forward)