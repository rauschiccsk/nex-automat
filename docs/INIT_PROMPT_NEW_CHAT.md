# Init Prompt - NEX Shared Integration

**Projekt:** NEX Automat  
**Last Session:** 2025-11-27 (NEX Shared Package Creation)  
**This Session:** Integration & Repositories  

---

## Quick Context

NEX Automat je projekt pre kompletnú automatizáciu podnikových procesov pre zákazníkov používajúcich NEX Genesis ERP.

**Aktuálny stav:**
- Version: 2.0.0 (tagged)
- GO-LIVE: ✅ COMPLETE (2025-11-27)
- NEX Shared Package: ✅ CREATED (last session)
- Integration: ⚪ TODO (this session)

---

## What Was Completed Last Session

### NEX Shared Package ✅

Vytvorený a nainštalovaný `nex-shared` package:

```
packages/nex-shared/
├── nex_shared/
│   ├── __init__.py
│   ├── models/
│   │   ├── tsh.py          # TSH model (7KB) ✅
│   │   └── tsi.py          # TSI model (6.8KB) ✅
│   ├── btrieve/
│   │   └── btrieve_client.py  # Btrieve wrapper (5.5KB) ✅
│   └── repositories/
│       └── base_repository.py  # Repository pattern (2.8KB) ✅
├── pyproject.toml ✅
└── README.md ✅
```

**Models:**
- ✅ TSHRecord (Dodacie listy - Header)
- ✅ TSIRecord (Dodacie listy - Items)
- ✅ BtrieveClient (32-bit Pervasive PSQL wrapper)
- ✅ BaseRepository (Generic repository pattern)

**Installation:**
- ✅ `pip install -e packages/nex-shared` - SUCCESS
- ✅ Import test - PASSED
- ✅ Basic functionality - OK

---

## Implementation Roadmap

```
FÁZA 1: Email → Staging → GUI Zobrazenie     ✅ COMPLETE
FÁZA 2: GO-LIVE Preview/Demo                 ✅ COMPLETE
FÁZA 3: Btrieve Models (TSH, TSI, PLS, RPC)  🟡 IN PROGRESS ← HERE
  ├── ✅ nex-shared package created
  ├── ✅ TSH/TSI models
  ├── ⚪ TODO: Add to apps dependencies
  ├── ⚪ TODO: Create repositories
  ├── ⚪ TODO: Test read operations
  └── ⚪ TODO: PLS, RPC models
FÁZA 4: GUI Editácia + Farebné rozlíšenie    ⚪ TODO
FÁZA 5: Vytvorenie produktových kariet       ⚪ TODO
FÁZA 6: Zaevidovanie dodávateľského DL       ⚪ TODO
FÁZA 7: Požiadavky na zmenu cien             ⚪ TODO
FÁZA 8: Testovanie + Production Hardening    ⚪ TODO
FÁZA 9: Ďalší zákazníci + Rozšírenia         ⚪ FUTURE
```

---

## Project Structure

```
C:\Development\nex-automat\
├── docs\
│   ├── SESSION_NOTES.md        ← Updated last session
│   └── strategy\
│       ├── TERMINOLOGY.md
│       ├── CURRENT_STATE.md
│       ├── VISION.md
│       ├── ARCHITECTURE.md
│       ├── REQUIREMENTS.md
│       └── ROADMAP.md
├── apps\
│   ├── supplier-invoice-loader\   # FastAPI service
│   └── supplier-invoice-editor\   # PyQt5 GUI
├── packages\
│   ├── invoice-shared\           # ✅ Working
│   └── nex-shared\               # ✅ NEW - Working
└── scripts\
    ├── create_nex_shared_files.py      # ✅ Used last session
    ├── reinstall_nex_shared.py         # ✅ Helper script
    ├── test_nex_shared_import.py       # ✅ Test script
    └── diagnose_site_packages.py       # ✅ Diagnostic
```

---

## Btrieve Tabuľky

| Tabuľka | Súbor | Model | Package | Status |
|---------|-------|-------|---------|--------|
| GSCAT | GSCAT.BTR | ✅ | invoice-shared | READ OK |
| BARCODE | BARCODE.BTR | ✅ | invoice-shared | READ OK |
| PAB | PAB.BTR | ✅ | invoice-shared | READ OK |
| MGLST | MGLST.BTR | ✅ | invoice-shared | READ OK |
| **TSH** | **TSHA-001.BTR** | **✅** | **nex-shared** | **NEW** ← Next |
| **TSI** | **TSIA-001.BTR** | **✅** | **nex-shared** | **NEW** ← Next |
| PLS | PLSnnnnn.BTR | ⚪ | nex-shared | TODO |
| RPC | RPCnnnnn.BTR | ⚪ | nex-shared | TODO |

---

## Next Steps (This Session)

### Priority 1: Add nex-shared Dependency

**Update apps dependencies:**

1. **supplier-invoice-loader/pyproject.toml:**
   ```toml
   dependencies = [
       ...
       "nex-shared",
   ]
   ```

2. **supplier-invoice-editor/pyproject.toml:**
   ```toml
   dependencies = [
       ...
       "nex-shared",
   ]
   ```

3. **Reinstall apps:**
   ```bash
   pip install -e apps/supplier-invoice-loader
   pip install -e apps/supplier-invoice-editor
   ```

### Priority 2: Create TSH/TSI Repositories

**Location:** `apps/supplier-invoice-loader/src/repositories/`

**Files to create:**
1. `tsh_repository.py` - Repository pre TSH (Dodacie listy - Header)
2. `tsi_repository.py` - Repository pre TSI (Dodacie listy - Items)

**Pattern:**
```python
from nex_shared.repositories.base_repository import BaseRepository
from nex_shared.models.tsh import TSHRecord
from nex_shared.btrieve.btrieve_client import BtrieveClient

class TSHRepository(BaseRepository[TSHRecord]):
    @property
    def table_name(self) -> str:
        return "C:/NEX/YEARACT/STORES/TSHA-001.BTR"
    
    def from_bytes(self, data: bytes) -> TSHRecord:
        return TSHRecord.from_bytes(data)
```

### Priority 3: Test Read Operations

**Create test script:**
- Read TSH records from NEX Genesis
- Read TSI records (items) for specific document
- Verify deserialization
- Display results

### Priority 4: GUI Integration (Optional)

**If time permits:**
- Display TSH/TSI in supplier-invoice-editor
- Basic list view of documents
- Show document details

---

## Available Resources

### Scripts

**Helper Scripts:**
- `scripts/create_nex_shared_files.py` - Package file creator
- `scripts/reinstall_nex_shared.py` - Reinstall helper
- `scripts/test_nex_shared_import.py` - Import test

**Diagnostic Scripts:**
- `scripts/diagnose_site_packages.py` - Site-packages check

### Documentation

**Strategy Docs:**
- `docs/strategy/CURRENT_STATE.md` - Workflow definition
- `docs/strategy/ARCHITECTURE.md` - System architecture
- `docs/strategy/REQUIREMENTS.md` - Requirements

**Package Docs:**
- `packages/nex-shared/README.md` - Usage examples

### Related Project

**nex-genesis-server:**
- Source of Btrieve models
- Location: C:/Development/nex-genesis-server
- Has working examples of repositories

---

## How to Start This Session

1. **Load SESSION_NOTES.md** for full context
2. **Choose priority:**
   - **Option A:** Add nex-shared to apps dependencies
   - **Option B:** Create TSH/TSI repositories
   - **Option C:** Test read operations
   - **Option D:** Other

3. **Follow workflow:**
   - Development → Git → Deployment
   - Test after each change
   - Document progress

---

## Important Notes

- **nex-shared package:** Fully functional, tested
- **Models:** TSH, TSI ready for use
- **BtrieveClient:** 32-bit compatible, tested with w3btrv7.dll
- **Installation:** Editable mode (`pip install -e`)
- **Python:** 3.13.7 32-bit (venv32)

**Repository Pattern:**
- Inherit from `BaseRepository[T]`
- Implement `table_name` property
- Implement `from_bytes()` method
- Use `get_first()`, `get_next()`, `get_all()`

**Btrieve Connection:**
```python
from nex_shared import BtrieveClient
client = BtrieveClient()
status, pos_block = client.open_file("C:/NEX/...")
```

---

**Last Updated:** 2025-11-27  
**Version:** 1.0  
**Status:** 🟢 Ready for Integration