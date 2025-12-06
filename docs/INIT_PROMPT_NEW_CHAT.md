# Init Prompt - BaseWindow Module Import Fix

## Current Status

**Achieved:**
- ✅ BaseWindow trieda implementovaná v `packages/nex-shared/`
- ✅ WindowSettingsDB, WindowPersistenceManager hotové
- ✅ Standalone test funguje (scripts/22_test_base_window_fixed.py)
- ✅ supplier-invoice-editor migrovaný na BaseWindow syntax

**Blocking Issue:**
- ❌ ModuleNotFoundError: No module named 'ui.base_window'
- ❌ sys.path fixes nefungujú (príliš neskoro v import chain)

---

## Problem Details

### Error
```
ModuleNotFoundError: No module named 'ui.base_window'
```

### Import Chain
```
main.py
  → ui/__init__.py (added sys.path fix)
    → main_window.py (added sys.path fix)
      → from ui.base_window import BaseWindow  ❌ FAILS
```

### Root Cause
**packages/nex-shared** NIE JE proper Python package:
- Chýba `setup.py` / `pyproject.toml`
- Nie je installed cez pip
- sys.path hacks sú fragile a fail v import chain

---

## Recommended Solutions (Priority Order)

### Option 1: Proper Package Install (BEST)
Konvertovať nex-shared na proper package a install editable:

```powershell
# Vytvoriť setup.py alebo pyproject.toml
# Potom:
pip install -e packages/nex-shared
```

**Výhody:**
- Clean imports: `from nex_shared.ui import BaseWindow`
- Works everywhere v projekte
- Professional solution
- Future-proof

**Kroky:**
1. Vytvoriť `packages/nex-shared/setup.py`
2. `pip install -e packages/nex-shared`
3. Zmeniť imports v main_window.py: `from nex_shared.ui import BaseWindow`
4. Odstrániť všetky sys.path hacks

### Option 2: PYTHONPATH Environment Variable
Nastaviť PYTHONPATH globálne:

```powershell
$env:PYTHONPATH = "C:\Development\nex-automat\packages\nex-shared"
```

**Výhody:**
- Jednoduchý fix
- Funguje pre všetky aplikácie

**Nevýhody:**
- Environment-specific
- Nestačí pre deployment

### Option 3: sys.path Fix v main.py (Absolute Start)
sys.path fix na ÚPLNOM začiatku main.py PRED akýmikoľvek imports:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "packages" / "nex-shared"))

# POTOM ostatné imports
from ui.main_window import MainWindow
```

**Výhody:**
- Quick fix
- No package setup needed

**Nevýhody:**
- Hack, nie clean solution
- Treba v každej aplikácii

### Option 4: Copy BaseWindow Code (Temporary)
Skopírovať BaseWindow kód priamo do aplikácie:

```
apps/supplier-invoice-editor/src/ui/
  ├── base_window.py  (copied)
  └── main_window.py
```

**Výhody:**
- Guaranteed works
- Quick unblock

**Nevýhody:**
- Duplicita kódu
- Nie univerzálne
- Proti pôvodnému cieľu

---

## Files Location

**nex-shared package:**
- `packages/nex-shared/ui/base_window.py`
- `packages/nex-shared/ui/window_persistence.py`
- `packages/nex-shared/database/window_settings_db.py`
- `packages/nex-shared/ui/__init__.py`
- `packages/nex-shared/database/__init__.py`

**Migrated app:**
- `apps/supplier-invoice-editor/src/ui/main_window.py`
- `apps/supplier-invoice-editor/main.py`

**Test script (WORKS):**
- `scripts/22_test_base_window_fixed.py` ✅

---

## Quick Start Commands

```powershell
# Verify nex-shared structure
ls packages\nex-shared\ui\

# Test standalone (works)
python scripts\22_test_base_window_fixed.py

# Current failure
cd apps\supplier-invoice-editor
python main.py  # ❌ ModuleNotFoundError

# Option 1: Package install
cd packages\nex-shared
# (create setup.py first)
pip install -e .

# Option 2: PYTHONPATH
$env:PYTHONPATH = "C:\Development\nex-automat\packages\nex-shared"
```

---

## Expected Workflow

1. **Choose solution** (recommend Option 1: proper package)
2. **Implement** chosen solution
3. **Test** supplier-invoice-editor spustenie
4. **Verify** maximize state persistence works
5. **Cleanup** remove temporary scripts (01-38)
6. **Document** BaseWindow usage guide
7. **Commit** all changes

---

## Success Criteria

✅ `python main.py` spustí aplikáciu  
✅ Maximize + Close + Run again → opens MAXIMIZED  
✅ Clean imports (no sys.path hacks)  
✅ BaseWindow reusable pre všetky aplikácie  

---

## Notes

- BaseWindow kód je kvalitný a kompletný ✅
- Standalone test dokazuje že BaseWindow funguje ✅
- Problem je PURELY v module import/packaging ✅
- Solution je technical, nie design issue ✅