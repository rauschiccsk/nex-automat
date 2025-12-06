# Init Prompt - Window Size Persistence Fix

## Current Status

**Achieved:**
- ✅ nex-shared package properly installed (`pip install -e packages/nex-shared`)
- ✅ All import errors fixed (relative imports throughout)
- ✅ Database connection working (invoice_staging via POSTGRES_PASSWORD)
- ✅ Application launches successfully with data from PostgreSQL
- ✅ Window position persistence works
- ✅ Maximized state persistence works

**Blocking Issue:**
- ❌ Window size (width/height) NOT persisting for normal windows
- When user resizes window and closes, reopens at default 1400x900

---

## Problem Details

### Error Pattern
User resizes window → closes app → reopens → **default size (1400x900)**, not resized dimensions

### Root Cause (Identified)
```python
# BaseWindow._save_settings() line 23:
if self._persistence.validate_position(x, y, width, height):
    self._db.save(...)  # Only saves if validation PASSES
else:
    logger.warning("Invalid position not saved")  # Dimensions LOST!
```

**Log evidence:**
```
Invalid window position: (-1659, -27) [1400x900]
Invalid position not saved for 'sie_main_window': (-1659, -27) [1400x900]
```

Position is invalid (y=-27 below 0, x=-1659 off monitor) → **entire record NOT SAVED** including dimensions.

### Previous Fix Attempt
**Script 46:** Modified `_save_settings()` to ALWAYS save dimensions (correct invalid position but keep actual size)

**Result:** Did NOT work - dimensions still not persisting

**Hypotheses:**
1. Script 46 not properly applied? Syntax error?
2. Need to reinstall package after changes? (`pip install -e packages/nex-shared`)
3. Problem in `_load_settings()` not `_save_settings()`?
4. Validation logic still blocking save despite modifications?

---

## Files Location

**nex-shared package:**
- `packages/nex-shared/ui/base_window.py` (contains _save_settings, _load_settings)
- `packages/nex-shared/ui/window_persistence.py` (WindowPersistenceManager)
- `packages/nex-shared/database/window_settings_db.py` (DB layer)

**Database:**
- Path: `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db`
- Table: window_settings (user_id, window_name, x, y, width, height, window_state)

**Application:**
- `apps/supplier-invoice-editor/src/ui/main_window.py` (extends BaseWindow)
- Window name: 'sie_main_window'
- Default size: (1400, 900)

---

## Recommended Solutions (Priority Order)

### Option 1: Debug Why Script 46 Failed (BEST)
**Investigate:**
1. Check if script 46 changes are actually in base_window.py
2. Verify package was reinstalled after changes
3. Add extensive logging to see exact flow
4. Manual DB test: INSERT dimensions, verify load works

**Steps:**
```python
# 1. Verify _save_settings() code
# 2. Add logging:
logger.info(f"SAVE: x={x}, y={y}, w={width}, h={height}, state={state}")
# 3. Test: resize window, close, check DB actual values
# 4. Test: manual INSERT, verify load restores dimensions
```

### Option 2: Separate Position/Size Validation
**Approach:**
- Validate position separately from size
- ALWAYS save width/height (they're always valid if > 0)
- Only correct/validate x/y coordinates

```python
# Validate and correct position
x = max(0, min(x, screen_width - width))
y = max(0, min(y, screen_height - height))

# ALWAYS save (position now valid, size preserved)
self._db.save(window_name, x, y, width, height, state)
```

### Option 3: Remove Validation Entirely (Quick Fix)
**Approach:**
- Trust that dimensions are reasonable
- Save everything without validation
- Let Qt/OS handle invalid positions

**Trade-off:** Windows might open off-screen, but dimensions preserved

---

## Database Structure

```sql
CREATE TABLE window_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    window_name TEXT NOT NULL,
    x INTEGER,
    y INTEGER,
    width INTEGER,
    height INTEGER,
    window_state INTEGER DEFAULT 0,  -- 0=Normal, 2=Maximized
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, window_name)
);
```

**Current record for sie_main_window:**
```
user_id: "Server"
window_name: "sie_main_window"
x: -1634
y: 90
width: 1400  ← Default, not actual resized size
height: 900  ← Default, not actual resized size
window_state: 0
```

---

## Quick Start Commands

```powershell
# Test current behavior
cd apps/supplier-invoice-editor
python main.py
# Resize window, close, reopen → verify size NOT saved

# Check DB content
python scripts/41_diagnose_window_settings_db.py

# Check base_window.py code
python scripts/45_show_save_settings_method.py

# Verify script 46 was applied
# (check for "ALWAYS save" logic in _save_settings)
```

---

## Expected Workflow

1. **Diagnose current state**
   - Verify script 46 changes are in base_window.py
   - Check if package needs reinstall
   - Add logging to track save/load flow

2. **Implement fix** (based on diagnosis)
   - If script 46 not applied: reapply properly
   - If applied but not working: separate position/size validation
   - Test with manual DB INSERT/SELECT

3. **Verify fix works**
   - Resize window to 800x600
   - Close application
   - Reopen → should be 800x600 ✅

4. **Cleanup**
   - Remove temporary scripts (01-46)
   - Commit changes
   - Update documentation

---

## Success Criteria

✅ User resizes window to any dimensions  
✅ Closes application  
✅ Reopens application  
✅ Window opens with RESIZED dimensions (not default 1400x900)  
✅ Window position still correct  
✅ Maximized state still works  

---

## Notes

- Position persistence: **WORKING** ✅
- Maximized persistence: **WORKING** ✅
- Size persistence: **BROKEN** ❌ (this session's focus)

- Database path: `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db`
- PostgreSQL DB: `invoice_staging` on localhost:5432
- Package installed: `pip install -e packages/nex-shared`

**Key insight:** Validation failure blocks save of BOTH position AND size. Need to decouple these.