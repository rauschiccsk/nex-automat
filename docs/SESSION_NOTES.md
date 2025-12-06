# Session Notes - Universal Window Persistence Implementation

**Dátum:** 2025-12-06  
**Projekt:** nex-automat v2.0.0  
**Status:** 🟡 V PROCESE (95% hotové)

## Úspešne Vyriešené

### 1. Window Maximize State Fix (supplier-invoice-editor)
✅ **HOTOVO** - Window maximize state persistence funguje perfektne

**Problém:** Aplikácia nezapamätala maximalizovaný stav okna.

**Root Cause:**
1. `INSERT OR REPLACE` nezapisoval `window_state=2` do DB
2. `SELECT` nečítal `window_state` stĺpec
3. `return` dictionary neobsahoval `window_state`

**Riešenie:**
- DELETE + INSERT pattern v `save_window_settings()`
- SELECT s `window_state` stĺpcom
- Return dictionary s `window_state` kľúčom

**Verifikácia:** ✅ Okno sa otvorí maximalizované ak bolo zatvorené maximalizované

### 2. Universal BaseWindow Implementation
✅ **HOTOVO** - BaseWindow trieda implementovaná v nex-shared package

**Vytvorená štruktúra:**
```
packages/nex-shared/
├── ui/
│   ├── base_window.py          # BaseWindow trieda
│   └── window_persistence.py   # Persistence manager
├── database/
│   └── window_settings_db.py   # DB layer
└── utils/
    └── monitor_utils.py         # Multi-monitor support
```

**BaseWindow Features:**
- Auto-load settings v `__init__`
- Auto-save settings v `closeEvent`
- Maximize state support
- Multi-monitor support
- Position validation
- Singleton DB manager

**API:**
```python
class MyWindow(BaseWindow):
    def __init__(self):
        super().__init__(
            window_name="my_window",
            default_size=(800, 600),
            default_pos=(100, 100)
        )
```

**Test:** ✅ Standalone test script funguje perfektne (scripts/22_test_base_window_fixed.py)

## Zostáva Vyriešiť

### Module Import Issues
🟡 **V PROCESE** - sys.path a import chain problémy

**Problém:**
```
ModuleNotFoundError: No module named 'ui.base_window'
```

**Identifikované príčiny:**
1. sys.path fix sa volá príliš neskoro v import chain
2. Relative vs absolute imports konflikty
3. Package structure nie je Python package (chýba proper setup)

**Možné riešenia:**
1. **Option A:** Konvertovať nex-shared na proper Python package s setup.py
2. **Option B:** Použiť editable install: `pip install -e packages/nex-shared`
3. **Option C:** sys.path fix na úplnom začiatku main.py (pred všetkými imports)
4. **Option D:** Kopírovať BaseWindow kód priamo do aplikácie (temporary)

## Vytvorené Scripts

**Diagnostika a Fix (01-15):**
- Window settings debugging a opravy
- DELETE + INSERT pattern implementation
- SELECT window_state fix

**nex-shared Implementation (16-21):**
- 16: Create nex-shared structure
- 17: WindowSettingsDB implementation
- 18: WindowPersistenceManager implementation
- 19: BaseWindow implementation
- 20: __init__.py exports
- 21: Test BaseWindow (✅ funguje)

**Migration Scripts (22-38):**
- 22: Test BaseWindow fixed (✅ funguje standalone)
- 23-38: Migration supplier-invoice-editor → BaseWindow
  - Import fixes, syntax fixes, sys.path attempts

## Next Steps

### Immediate (High Priority)
1. **Fix module import chain** - vyriešiť ModuleNotFoundError
   - Najlepšia option: pip install -e packages/nex-shared
   - Alternative: sys.path fix na absolute začiatku
   
2. **Verify migration works** - supplier-invoice-editor funguje s BaseWindow

3. **Cleanup** - odstrániť temporary scripts (01-38)

### Short Term
1. Migrate supplier-invoice-loader → BaseWindow
2. Documentation pre BaseWindow usage
3. Unit tests pre nex-shared package

### Long Term
1. Grid persistence integration do BaseWindow
2. Multi-user support testing
3. Performance optimization

## Súbory Zmenené

**nex-shared package (NEW):**
- `packages/nex-shared/ui/base_window.py`
- `packages/nex-shared/ui/window_persistence.py`
- `packages/nex-shared/database/window_settings_db.py`
- `packages/nex-shared/ui/__init__.py`
- `packages/nex-shared/database/__init__.py`
- `packages/nex-shared/__init__.py`

**supplier-invoice-editor:**
- `apps/supplier-invoice-editor/src/ui/main_window.py` (migrated to BaseWindow)
- `apps/supplier-invoice-editor/src/utils/window_settings.py` (simplified - grid only)
- `apps/supplier-invoice-editor/src/utils/__init__.py` (removed window functions)
- `apps/supplier-invoice-editor/main.py` (added sys.path fix)
- `apps/supplier-invoice-editor/src/ui/__init__.py` (added sys.path fix)

## Lessons Learned

1. **Python packaging je critical** - sys.path hacks sú fragile
2. **Import chain testing** - testovať import pred plnou migráciou
3. **Relative vs absolute imports** - absolute imports sú safer pre shared packages
4. **Test standalone first** - BaseWindow standalone test bol úspešný, integration je problem
5. **Module structure matters** - proper package setup od začiatku je better than retrofitting

## Recommendations

**Pre ďalšiu session:**
1. Začať s `pip install -e packages/nex-shared` (proper package install)
2. Ak to nevyriešiť, rollback migration a použiť BaseWindow kód inline
3. Potom refaktorovať keď je proper packaging setup