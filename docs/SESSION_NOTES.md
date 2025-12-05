# Session Notes - 2025-12-05/06: Grid & Window Settings Persistence

## Zhrnutie session

Session riešila problémy s persistenciou nastavení v NEX Automat v2.1 - Supplier Invoice Editor:
1. **Grid Settings API Mismatch** - dict namiesto int parameter ✅ VYRIEŠENÉ
2. **Window Position Persistence** - nevalidné pozície mimo obrazovky ✅ VYRIEŠENÉ  
3. **Multi-Monitor Support** - MIN_X rozšírené pre dual monitor ✅ VYRIEŠENÉ
4. **Window Maximize State** - maximalizované okno ⚠️ ČIASTOČNE (problém zostáva)

---

## Vyriešené problémy

### ✅ Problém 1: Grid Settings API Mismatch

**Symptóm:**
- Error: "Error binding parameter 4: type 'dict' is not supported"
- Grid settings sa neukladali

**Root Cause:**
1. `save_grid_settings()` očakával `int` parameter ale dostával `dict`
2. Load používal nesprávny kľúč `'active_column'` namiesto `'active_column_index'`

**Riešenie:**
- Script `01_fix_grid_settings_api_mismatch.py` - opravil save volanie
- Script `04_fix_load_grid_settings_key.py` - opravil load kľúč

**Súbory upravené:**
- `apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py`

**Status:** ✅ FUNGUJE - aktívny stĺpec sa zapamätáva

---

### ✅ Problém 2: Window Position - Nevalidné pozície

**Symptóm:**
- "Invalid position: x=-1660" warning pri štarte
- Okno sa otváralo mimo obrazovky
- Nevalidné pozície sa ukladali do databázy

**Root Cause:**
1. `window_settings.py` nemal validáciu pri load
2. `closeEvent()` neukladal validáciu pred save
3. Qt OS cache spôsoboval že okno sa otváralo mimo aj po vymazaní DB

**Riešenie:**
- Script `05_fix_close_event_validation.py` - validácia v closeEvent
- Script `06_fix_default_window_position.py` - safe default (100, 100)
- Script `clean_invalid_window_positions.py` - utility na vyčistenie DB

**Súbory upravené:**
- `apps/supplier-invoice-editor/src/utils/window_settings.py`
- `apps/supplier-invoice-editor/src/ui/main_window.py`

**Status:** ✅ FUNGUJE - nevalidné pozície sa neukladajú, default je safe

---

### ✅ Problém 3: Multi-Monitor Support

**Symptóm:**
- Ľavý monitor (negatívne X súradnice) označované ako invalid
- Okno sa nedalo uložiť na ľavom monitore

**Root Cause:**
- MIN_X = -50 bolo príliš málo pre dual monitor setup
- Ľavý monitor môže mať X od -1920 do 0

**Riešenie:**
- Script `07_fix_multimonitor_support.py` - MIN_X = -3840 (dual 4K)

**Súbory upravené:**
- `apps/supplier-invoice-editor/src/utils/window_settings.py`
- `apps/supplier-invoice-editor/src/ui/main_window.py`

**Status:** ✅ FUNGUJE - dual monitor support

---

## ⚠️ Problém 4: Window Maximize State (NEDOKONČENÉ)

**Cieľ:**
- Zapamätať si maximalizovaný stav okna
- Otvoriť okno maximalizované na správnom monitore

**Vykonané kroky:**

1. **Databáza rozšírená:**
   - Script `08_add_window_state_persistence.py`
   - Pridaný stĺpec `window_state INTEGER DEFAULT 0`
   - 0 = normal, 2 = maximized

2. **Kód upravený:**
   - Scripts 09-20 - úpravy save/load logiky
   - closeEvent() - detekcia `isMaximized()`
   - load_geometry() - aplikácia `setWindowState(Qt.WindowMaximized)`

3. **Finálna logika (po zjednodušení):**
   - Maximalizované: uloží normalGeometry() + window_state=2
   - Load: najprv setGeometry(), potom setWindowState() ak state=2

**Aktuálny stav:**
- ❌ Maximize state sa stále neukladá správne do DB
- ❌ Po reštarte sa okno neotvorí maximalizované
- Debug ukazuje že closeEvent detekuje isMaximized()=True
- Ale window_state=0 v databáze

**Súbory upravené:**
- `apps/supplier-invoice-editor/src/utils/window_settings.py`
- `apps/supplier-invoice-editor/src/ui/main_window.py`

**Status:** ⚠️ NEFUNGUJE - problém v save reťazci

---

## Vytvorené scripty

### Session Scripts (číslované, temporary)

1. `01_fix_grid_settings_api_mismatch.py` - grid API fix ✅
2. `04_fix_load_grid_settings_key.py` - load kľúč fix ✅
3. `05_fix_close_event_validation.py` - window validácia ✅
4. `06_fix_default_window_position.py` - default pozícia ✅
5. `07_fix_multimonitor_support.py` - MIN_X rozšírenie ✅
6. `08_add_window_state_persistence.py` - DB stĺpec ✅
7. `09_update_window_state_code.py` - window_state kód ⚠️
8. `10_fix_save_window_settings_signature.py` - signature ⚠️
9. `11_manual_fix_save_function.py` - manuálny fix ⚠️
10. `12_fix_maximized_geometry.py` - normalGeometry() ⚠️
11. `13_update_diagnose_script.py` - diagnostika ✅
12. `14_add_debug_to_load.py` - debug load ⚠️
13. `15_fix_load_window_settings_return.py` - return fix ⚠️
14. `16_fix_window_state_variable.py` - premenná fix ⚠️
15. `17_add_debug_to_close.py` - debug close ⚠️
16. `18_simplify_maximize_logic.py` - zjednodušenie ⚠️
17. `19_fix_close_event_simple.py` - closeEvent rewrite ⚠️
18. `20_fix_maximize_on_correct_monitor.py` - monitor fix ⚠️

### Permanent Scripts (bez číslovania)

- `clean_invalid_window_positions.py` - vyčistenie nevalidných pozícií ✅
- `03_diagnose_window_settings.py` - diagnostika DB (ešte číslovaný) ✅

---

## Databázy

### Window Settings Database
**Location:** `C:\NEX\YEARACT\SYSTEM\SQLITE\window_settings.db`

**Štruktúra tabuľky:**
```sql
CREATE TABLE window_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    window_name TEXT NOT NULL,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    window_state INTEGER DEFAULT 0,  -- Pridané v session
    UNIQUE(user_id, window_name)
)
```

**Validačné limity:**
- MIN_X = -3840 (dual 4K)
- MIN_Y = 0
- MIN_WIDTH = 400, MAX_WIDTH = 3840
- MIN_HEIGHT = 300, MAX_HEIGHT = 2160
- window_state: 0=normal, 2=maximized

### Grid Settings Database
**Location:** `C:\NEX\YEARACT\SYSTEM\SQLITE\grid_settings.db`

**Status:** ✅ Funguje správne
- Ukladá šírky stĺpcov
- Ukladá poradie stĺpcov
- Ukladá viditeľnosť stĺpcov
- Ukladá aktívny stĺpec pre quick search

---

## Testing Checklist

### ✅ Test 1: Grid Settings Persistence
- [x] Active column sa zapamätáva
- [x] Šírky stĺpcov sa zapamätávajú
- [x] Žiadne "dict is not supported" errory

### ✅ Test 2: Window Position (Normal)
- [x] Validné pozície sa zapamätávajú
- [x] Nevalidné pozície sa neukladajú
- [x] Default pozícia (100, 100) funguje
- [x] Multi-monitor support funguje

### ❌ Test 3: Window Maximize State
- [x] closeEvent() detekuje isMaximized()
- [x] DB má window_state stĺpec
- [ ] window_state=2 sa ukladá do DB
- [ ] Okno sa otvorí maximalizované
- [ ] Maximalizuje na správnom monitore

---

## Ďalšie kroky (Priority pre ďalší chat)

### Priorita 1: Dokončiť Window Maximize ⚠️ URGENT

**Problém:** window_state sa neukladá do DB aj keď closeEvent() detekuje isMaximized()=True

**Debug kroky:**
1. Pridať debug do `save_window_settings()` funkcie
2. Overiť že INSERT statement dostáva window_state=2
3. Overiť že DB skutočne zapisuje hodnotu
4. Možno problém v INSERT OR REPLACE logike?

**Súbory na kontrolu:**
- `apps/supplier-invoice-editor/src/utils/window_settings.py` (save funkcia)
- Možno je problém s UNIQUE constraint?

### Priorita 2: Cleanup a Testing

Po vyriešení maximize:
1. Odstrániť debug výpisy z kódu
2. Kompletné testovanie všetkých scenárov
3. Cleanup temporary scripts (01-20)
4. Update diagnostického scriptu (odčíslovať)

### Priorita 3: Git Commit

**Súbory na commit:**
```
Modified:
- apps/supplier-invoice-editor/src/ui/widgets/invoice_list_widget.py
- apps/supplier-invoice-editor/src/utils/window_settings.py
- apps/supplier-invoice-editor/src/ui/main_window.py
- apps/supplier-invoice-editor/src/utils/grid_settings.py

New:
- scripts/clean_invalid_window_positions.py
- scripts/diagnose_window_settings.py (premenovať z 03_)
```

### Priorita 4: Deployment

Po úspešnom testingu:
1. Git commit a push
2. Pull v Production (Mágerstav server)
3. Production testing
4. Vyčistiť production DB pomocou clean script

---

## Lessons Learned

### Čo fungovalo dobre ✅

1. **Systematická diagnostika** - utility scripty (diagnose, clean) veľmi pomohli
2. **Krok po kroku** - po jednom probléme, nie všetko naraz
3. **Debug output** - pomohol identifikovať kde presne je problém
4. **Multi-monitor awareness** - rozšírenie MIN_X bolo správne rozhodnutie

### Čo nefungovalo ❌

1. **Príliš veľa scripts** - 20 temporary scripts je chaos
2. **Nedokončený maximize** - 12 scripts na jeden problém a stále nefunguje
3. **Neoverovanie save chain** - predpokladali sme že INSERT funguje bez overenia
4. **Komplexná logika** - normalGeometry(), multi-monitor, validácia = príliš komplikované

### Odporúčania pre budúcnosť 💡

1. **SQL debug VŽDY** - pri DB operáciách VŽDY overiť že zápis prebehol
2. **Jedna vec = jeden script** - nie 12 verzií toho istého
3. **Testing pred merge** - každý fix otestovať IHNEĎ
4. **Dokumentácia postupu** - lepšie session notes priebežne
5. **Možno Qt window state je broken?** - zvážiť iný prístup (custom flag?)

---

## Technické poznámky

### Window State Values (Qt)
```python
Qt.WindowNoState = 0      # Normal
Qt.WindowMinimized = 1    # Minimized  
Qt.WindowMaximized = 2    # Maximized
Qt.WindowFullScreen = 4   # Fullscreen
```

### Geometry vs WindowState
- `setGeometry()` - nastaví pozíciu a veľkosť
- `setWindowState()` - nastaví stav (max/min/full)
- `normalGeometry()` - vráti geometriu pred maximize/fullscreen
- **POZOR:** setWindowState() po setGeometry() môže ignorovať geometriu!

### Multi-Monitor Súradnice
- Primary monitor (right): X=0 až 1920, Y=0 až 1080
- Secondary monitor (left): X=-1920 až 0, Y=0 až 1080
- Negatívne X je validné!

---

## Connection Details

### Development Server (ICC Komárno)
- **Location:** C:\Development\nex-automat
- **Python:** C:\Development\nex-automat\venv32\Scripts\python.exe
- **Database:** C:\NEX\YEARACT\SYSTEM\SQLITE\
- **User:** Server (Windows USERNAME)
- **Status:** ⚠️ Grid funguje, Window maximize nefunguje

### Production Server (Mágerstav)
- **Location:** C:\Deployment\nex-automat
- **Database:** C:\NEX\YEARACT\SYSTEM\SQLITE\
- **Status:** ⏸️ Čaká na dokončenie vývoja

### GitHub Repository
- **Repo:** rauschiccsk/nex-automat
- **Branch:** develop (aktívny vývoj)
- **Status:** 🔴 Lokálne zmeny nie sú commitnuté

---

**Session Type:** Bug Fixes & Feature Development  
**Version:** v2.1 (Grid & Window Settings era)  
**Duration:** ~3 hodiny
**Next Session:** Dokončiť Window Maximize State  
**Status:** ⚠️ **PARTIALLY COMPLETE** - Grid ✅, Position ✅, Maximize ❌