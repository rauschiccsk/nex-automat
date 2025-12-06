# Init Prompt - Next Session

## Current Status

**Achieved in previous session:**
- ✅ Window size persistence works for main window
- ✅ Window size persistence works for detail window
- ✅ Window position drift fixed
- ✅ Grid settings error fixed (dict → int)
- ✅ ENTER key opens invoice detail
- ✅ ESC key closes application

**All systems operational - no blocking issues**

---

## Project Structure

**Location:** `C:\Development\nex-automat`

**Key directories:**
```
nex-automat/
├── apps/
│   └── supplier-invoice-editor/
│       ├── main.py
│       └── src/
│           └── ui/
│               ├── main_window.py (BaseWindow - główne okno)
│               ├── invoice_detail_window.py (BaseWindow - detail okno)
│               └── widgets/
│                   ├── invoice_list_widget.py
│                   └── invoice_items_grid.py
├── packages/
│   └── nex-shared/
│       ├── ui/
│       │   ├── base_window.py (window persistence core)
│       │   └── window_persistence.py
│       └── database/
│           └── window_settings_db.py
└── docs/
    ├── SESSION_NOTES.md
    └── INIT_PROMPT_NEW_CHAT.md
```

---

## Database

**Window Settings DB:**
- Path: `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db`
- Table: `window_settings`
- Records: `sie_main_window`, `sie_invoice_detail`

**PostgreSQL:**
- Database: `invoice_staging`
- Host: localhost:5432
- Used for: invoice data, supplier data

---

## Important Implementation Details

### BaseWindow Usage
```python
class MyWindow(BaseWindow):
    def __init__(self, parent=None):
        super().__init__(
            window_name="unique_id",  # Required
            default_size=(800, 600),
            default_pos=(100, 100),
            parent=parent
        )
        # QMainWindow requires central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
```

### Critical Rules
- ❌ **NEVER** use `self.resize()` after BaseWindow init
- ❌ **NEVER** use `setGeometry()` - causes position drift
- ✅ **ALWAYS** use `move()` + `resize()` for positioning
- ✅ **ALWAYS** use `pos()` + `size()` for getting dimensions
- ✅ **ALWAYS** use `central_widget` for QMainWindow layouts

---

## Recent Changes (2025-12-06)

**Modified files:**
1. `packages/nex-shared/ui/base_window.py`
   - Changed to `pos()` + `resize()` instead of `setGeometry()`
   
2. `packages/nex-shared/ui/window_persistence.py`
   - Fixed `get_safe_position()` to preserve size when position invalid

3. `apps/supplier-invoice-editor/src/ui/main_window.py`
   - Removed `resize(1400, 900)` call
   - Added ENTER key handler for opening invoice detail

4. `apps/supplier-invoice-editor/src/ui/invoice_detail_window.py`
   - Changed from `QDialog` to `BaseWindow`
   - Fixed layout to use `central_widget`
   - Changed `accept()/reject()` to `close()`

5. `apps/supplier-invoice-editor/src/ui/widgets/invoice_items_grid.py`
   - Fixed `save_grid_settings()` call: int instead of dict

---

## Quick Commands

**Test application:**
```powershell
cd apps/supplier-invoice-editor
python main.py
```

**Database check:**
```sql
-- View window settings
SELECT * FROM window_settings WHERE user_id = 'Server';
```

**Package status:**
```powershell
# Verify nex-shared is installed as editable
pip list | findstr nex-shared
# Should show: nex-shared 1.0.0 C:\Development\nex-automat\packages\nex-shared
```

---

## Potential Future Tasks

### Enhancement Ideas
1. **Multi-monitor support**
   - Better validation for multiple screens
   - Remember which monitor window was on

2. **Window templates**
   - Predefined layouts (small/medium/large)
   - Quick switch between templates

3. **Grid column persistence**
   - Save/restore column order in grids
   - Save/restore column visibility

4. **Per-user preferences**
   - Different window sizes for different users
   - User-specific grid layouts

### Known Non-Critical Issues
- None currently

---

## Development Workflow

**Standard process:**
1. Make changes in `C:\Development\nex-automat` (Development)
2. Test locally
3. Commit to Git
4. Push to repository
5. Pull in Deployment environment
6. Restart applications

**Package changes:**
- Changes to `packages/nex-shared` automatically visible (editable install)
- No reinstall needed after code changes
- Only reinstall if `setup.py` changes

---

## Common Tasks

### Add new window with persistence
```python
from nex_shared.ui import BaseWindow
from ..utils.constants import WINDOW_MY_NEW

class MyNewWindow(BaseWindow):
    def __init__(self, parent=None):
        super().__init__(
            window_name=WINDOW_MY_NEW,
            default_size=(1000, 700),
            parent=parent
        )
        # Setup central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add your widgets to layout
```

### Debug window persistence
```python
# Add to base_window.py for debugging
print(f"🔍 LOAD: {settings}")  # In _load_and_apply_settings()
print(f"🔍 SAVE: x={x}, y={y}, w={width}, h={height}")  # In _save_settings()
```

---

## Session Scripts Cleanup

**Temporary scripts created:** 01-43 in `scripts/` directory

**To cleanup after commit:**
```powershell
# Delete temporary session scripts
Remove-Item scripts/0[1-4]*.py
Remove-Item scripts/[1-4][0-9]_*.py
```

**Permanent scripts to keep:**
- None from this session (all were diagnostic/fix scripts)

---

## Notes for Next Developer

1. **Window persistence is working** - don't modify unless necessary
2. **BaseWindow pattern is established** - follow it for new windows
3. **All windows should use BaseWindow** - no raw QDialog/QMainWindow
4. **Grid settings use integer active_column** - not dict
5. **ENTER opens detail, ESC closes app** - keyboard shortcuts working

---

**Last updated:** 2025-12-06  
**Next session ready:** ✅  
**Blocking issues:** None