# Init Prompt - Dokončenie Window Maximize State

## Aktuálny stav

**Vyriešené:**
- ✅ Grid settings persistence (active column)
- ✅ Window position persistence (normal window)
- ✅ Multi-monitor support
- ✅ Invalid position validation

**Zostáva vyriešiť:**
- ❌ Window maximize state persistence

---

## Problém: Window Maximize State

### Symptóm
Aplikácia nezapamätá maximalizovaný stav okna. Po reštarte sa okno otvorí v normálnom stave aj keď bolo zatvorené maximalizované.

### Root Cause (predpoklad)
`window_state=2` sa **NEUKLADÁ do databázy** aj keď:
- closeEvent() detekuje `isMaximized()=True` ✅
- closeEvent() volá `save_window_settings(..., window_state=2)` ✅
- Log hovorí "Window settings saved: ... maximized" ✅
- Ale SQL query ukazuje `window_state=0` v DB ❌

**Podozrenie:** Problém v `save_window_settings()` funkcii alebo INSERT statement.

### Aktuálna implementácia

**Databáza:**
```sql
-- C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db
CREATE TABLE window_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    window_name TEXT NOT NULL,
    x INTEGER,
    y INTEGER,
    width INTEGER,
    height INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    window_state INTEGER DEFAULT 0,
    UNIQUE(user_id, window_name)
)
```

**closeEvent() - main_window.py (riadok ~272):**
```python
def closeEvent(self, event):
    if self.isMaximized():
        norm_geom = self.normalGeometry()
        save_window_settings(
            window_name=WINDOW_MAIN,
            x=norm_geom.x(), y=norm_geom.y(),
            width=norm_geom.width(), height=norm_geom.height(),
            window_state=2  # Maximalized
        )
        self.logger.info(f"Window settings saved: maximized on monitor at ...")
    else:
        # Normal window
        save_window_settings(..., window_state=0)
```

**save_window_settings() - window_settings.py (riadok ~138):**
```python
def save_window_settings(window_name: str, x: int, y: int, width: int, height: int,
                        window_state: int = 0, user_id: Optional[str] = None) -> bool:
    cursor.execute("""
        INSERT OR REPLACE INTO window_settings
        (user_id, window_name, x, y, width, height, window_state, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, window_name, x, y, width, height, window_state, datetime.now()))
```

**load_geometry() - main_window.py (riadok ~40):**
```python
def _load_geometry(self):
    settings = load_window_settings(window_name=WINDOW_MAIN)
    if settings:
        # Vždy aplikuj geometriu (určuje monitor)
        if settings.get('x') is not None and settings.get('width'):
            self.setGeometry(settings['x'], settings['y'], 
                           settings['width'], settings['height'])
        
        # Potom maximalizuj ak treba
        if settings.get('window_state', 0) == 2:
            self.setWindowState(Qt.WindowMaximized)
            self.logger.info(f"Window maximized on monitor ...")
```

---

## Diagnostické kroky

### Krok 1: Overiť INSERT statement
```powershell
python -c "with open('apps/supplier-invoice-editor/src/utils/window_settings.py', 'r') as f: lines = f.readlines(); start = next(i for i, l in enumerate(lines) if 'INSERT OR REPLACE' in l); print(''.join(lines[start:start+5]))"
```

### Krok 2: Pridať debug do save_window_settings()
Pred `cursor.execute()`:
```python
self.logger.info(f"DEBUG save: window_state={window_state}, VALUES={values}")
```

### Krok 3: Overiť DB po save
```powershell
python -c "import sqlite3; conn = sqlite3.connect(r'C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db'); print(conn.execute('SELECT window_state, updated_at FROM window_settings WHERE window_name=\"sie_main_window\" ORDER BY updated_at DESC LIMIT 1').fetchone())"
```

### Krok 4: Test UNIQUE constraint
Možno `INSERT OR REPLACE` nefunguje správne? Skúsiť:
1. DELETE pred INSERT
2. Alebo UPDATE WHERE EXISTS

---

## Možné riešenia

### Riešenie A: Debug a fix save chain
1. Pridať debug output do `save_window_settings()`
2. Overiť že parameter `window_state=2` prichádza správne
3. Overiť že INSERT statement je správny
4. Overiť že commit prebehol
5. Fix ak nájdeme chybu

### Riešenie B: Alternatívny prístup
Ak save reťazec nefunguje, zvážiť:
1. Separátna tabuľka len pre window_state?
2. Použiť config file namiesto DB?
3. Qt QSettings API?

### Riešenie C: Zjednodušenie
Možno problém je že `normalGeometry()` vráti iné hodnoty a UNIQUE constraint vyberie starý záznam?
- Skúsiť DELETE + INSERT namiesto INSERT OR REPLACE

---

## Súbory na kontrolu

**Python súbory:**
- `apps/supplier-invoice-editor/src/utils/window_settings.py` (save funkcia)
- `apps/supplier-invoice-editor/src/ui/main_window.py` (close & load)

**Databáza:**
- `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db`

**Utility scripts:**
- `scripts/clean_invalid_window_positions.py`
- `scripts/03_diagnose_window_settings.py`

---

## Quick Start Commands

```powershell
# 1. Diagnostika DB
python scripts\03_diagnose_window_settings.py

# 2. Vyčistenie DB
python scripts\clean_invalid_window_positions.py

# 3. Test aplikácie
cd apps\supplier-invoice-editor
python main.py

# 4. SQL query - overenie window_state
python -c "import sqlite3; conn = sqlite3.connect(r'C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db'); print(conn.execute('SELECT * FROM window_settings WHERE window_name=\"sie_main_window\"').fetchone())"
```

---

## Expected Workflow

1. **Diagnostika** - overiť aktuálny stav DB
2. **Debug** - pridať výpisy do save_window_settings()
3. **Test** - maximize, close, check DB
4. **Fix** - opraviť identifikovaný problém
5. **Verify** - test celého cyklu
6. **Cleanup** - odstrániť debug, cleanup scripts
7. **Commit** - git commit všetkých zmien

---

## Notes pre Claude

- Používaj krok-po-kroku approach
- Jeden fix = jeden script
- Debug output je CRITICAL
- Overuj DB VŽDY SQL query
- Nerobať predpoklady - overuj!