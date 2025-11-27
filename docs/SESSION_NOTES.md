# Session Notes - Btrieve Status 161 → Status 30 Investigation

**Dátum:** 2025-11-27  
**Projekt:** NEX Automat v2.0.0  
**Úloha:** Diagnostika a riešenie Btrieve problémov

---

## Session Overview

Táto session riešila kritický blocker - nefungujúci Btrieve access v NEX Automat projekte. Začali sme so status 161 (FILE_NOT_FOUND) a postúpili k status 30 (NOT_A_BTRIEVE_FILE).

---

## Chronológia riešenia

### 1. Počiatočný stav (Status 161)

**Problém:**
- Všetky Btrieve open operácie zlyhávajú so status 161
- Python kód identický s fungujúcim invoice-editor projektom
- NEX Genesis server má rovnaký problém
- BUTIL utility zlyhalo s permission error

**Diagnóza:**
```
Status: 161 (FILE_NOT_FOUND)
Files exist: ✅ C:\NEX\YEARACT\STORES\GSCAT.BTR (29.7 MB)
Service running: ✅ psqlWGE
DLL loaded: ✅ w3btrv7.dll
```

### 2. Prvé zistenia - BUTIL test

**BUTIL test z C:\Program Files:**
```
BUTIL -stat C:\NEX\YEARACT\STORES\GSCAT.BTR
Error: Cannot create temporary file (permission denied)
```

**BUTIL test z C:\NEX\YEARACT\STORES:**
```
✅ SUCCESS!
File Statistics:
- Version: 9.50
- Records: 12,454
- Keys: 18
- Page Size: 4096
```

**Kľúčové zistenie:** BUTIL funguje z NEX directory, ale Python dostáva status 161 aj odtiaľ.

### 3. ROOT CAUSE identifikovaný

**Zistenie:** Expirovaná Pervasive 11 Trial verzia!

Používateľ uviedol:
> "Mali sme nainštalovaný Pervasive workgroup 11 (Trial version). Inštalácia expirovaná. Preto nefungoval nám."

**Riešenie:**
- Odinštalovanie Pervasive 11 Trial
- Inštalácia licencovanej Pervasive v9
- NEX Genesis server začal fungovať ✅

### 4. Nový problém - Status 30

Po inštalácii Pervasive v9:

**Test v nex-automat:**
```python
venv32\Scripts\python.exe scripts/04_test_config_lookup.py

Results:
✅ Config Loading (2/4)
✅ Path Resolution (2/4)
❌ GSCAT Read - Status 30
❌ TSH Read - Status 30
```

**Test rôznych open modes:**
```
Mode -2 (Read-only): Status 30
Mode -1 (Accelerated): Status 30
Mode  0 (Normal): Status 30
Mode -3 (Exclusive): Status 30
```

**Test owner names:**
```
Owner '': Status 30
Owner 'NEX': Status 30
Owner 'GENESIS': Status 30
Owner 'ADMIN': Status 30
[... všetky ostatné: Status 30]
```

### 5. Porovnanie s invoice-editor

**Invoice-editor test (na tom istom systéme):**
```python
python -c "from src.btrieve.btrieve_client import BtrieveClient; ..."
Status: 30
```

**Záver:** Invoice-editor TIEŽ dostáva status 30 po downgrade na Pervasive v9!

### 6. Analýza Delphi source code

**Kritické zistenie z BtrConst.pas:**

Pôvodná interpretácia (chybná):
```python
# Python mapping (nesprávny!)
30: "PERMISSION_ERROR"
```

**Skutočná definícia z Delphi:**
```pascal
B_NOT_A_BTRIEVE_FILE = 30;
```

**Status 30 = NOT_A_BTRIEVE_FILE!**

Nie je to permission error, ale **file format incompatibility**!

### 7. Finálna hypotéza

**Problém:** Súbory vytvorené/upravené Pervasive v11 Trial nie sú kompatibilné s Pervasive v9!

**Dôkazy:**
1. BUTIL (súčasť Pervasive v9) dokáže čítať file metadata
2. Python/Delphi BTRCALL API hlási "NOT_A_BTRIEVE_FILE"
3. Rovnaký problém vo všetkých projektoch (nex-automat, invoice-editor)
4. File existuje, permissions OK, service beží

**Vysvetlenie:**
- BUTIL používa nižšiu úroveň prístupu (direct file I/O)
- BTRCALL API používa Btrieve engine validáciu
- Engine v9 nerozpoznáva file format z v11

---

## Diagnostické skripty vytvorené

### 1. test_open_modes.py ✅
Testovanie rôznych Btrieve open modes (-2, -1, 0, -3)

### 2. test_owner_names.py ✅
Testovanie owner names (NEX, GENESIS, ADMIN, ...)

### 3. fix_btrieve_owner_name.py ✅
Oprava open_file() na podporu owner_name v data_buffer

### 4. test_file_version.py ✅
Analýza Btrieve file header a version info

---

## Porovnanie kódu: invoice-editor vs nex-automat

### DLL Setup - IDENTICKÉ ✅

**Obe projekty:**
```python
self.btrcall.argtypes = [
    ctypes.c_uint16,
    ctypes.POINTER(ctypes.c_char),
    ctypes.POINTER(ctypes.c_char),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_uint8,
    ctypes.c_uint8
]
self.btrcall.restype = ctypes.c_int16
```

### open_file() - IDENTICKÉ jadro ✅

**Jediný rozdiel:** nex-automat má `_resolve_table_path()` ale ak dáš priamu cestu, vráti ju as-is.

---

## Aktuálny stav

### Status
- ❌ Btrieve access nefunguje v žiadnom projekte
- ✅ BUTIL funguje (môže čítať file metadata)
- ✅ NEX Genesis server funguje (používa iné API?)
- ❌ Python BTRCALL dostáva status 30

### Environment
- Pervasive: v9 (Licensed) ← downgrade z v11 Trial
- Python: 3.13.7 32-bit (venv32)
- DLL: w3btrv7.dll from C:\PVSW\bin
- Service: psqlWGE ✅ Running

### Hypotéza
Súbory C:\NEX\YEARACT\STORES\*.BTR boli vytvorené/modifikované Pervasive v11 a sú nekompatibilné s Pervasive v9 API.

---

## Next Steps (pre novú session)

### Priority 1: File Version Analysis ⚡
Spustiť `scripts/test_file_version.py` na analýzu Btrieve file headers:
- Zistiť file format version
- Porovnať s očakávanou verziou pre Pervasive v9
- Identifikovať rozdiel

### Priority 2: File Conversion
Ak sú súbory v11 format:
- Použiť BUTIL na rebuild do v9 format
- Kontaktovať NEX Genesis support
- Nájsť migration tool

### Priority 3: NEX Genesis Analysis
Zistiť ako NEX Genesis pristupuje k Btrieve:
- Používa iné DLL?
- Iná API metóda?
- Špeciálna konfigurácia?

### Priority 4: Fallback Options
Ak conversion nefunguje:
- ODBC driver?
- Direct file parsing?
- Kontakt s Pervasive/Actian support

---

## Dôležité súbory a cesty

### NEX Automat
```
C:\Development\nex-automat\
├── packages/nexdata/nexdata/btrieve/btrieve_client.py
├── config/database.yaml
└── scripts/
    ├── test_open_modes.py
    ├── test_owner_names.py
    ├── fix_btrieve_owner_name.py
    └── test_file_version.py (nový)
```

### Invoice Editor
```
C:\Development\invoice-editor\
├── src/btrieve/btrieve_client.py
└── config/config.yaml
```

### NEX Genesis
```
C:\Development\nex-genesis-server\
├── BtrConst.pas (Btrieve constants)
├── BtrAPI32.pas (API definitions)
├── BtrHand.pas (High-level wrappers)
└── BtrTable.pas (Table component)
```

### Data Files
```
C:\NEX\YEARACT\STORES\
├── GSCAT.BTR (29.7 MB, 12,454 records)
├── BARCODE.BTR
├── MGLST.BTR
└── ...
```

---

## Kľúčové poznatky

1. **Status codes precision matters!**
   - Status 161 ≠ Status 30
   - Správna interpretácia je kritická
   - Treba vždy checkovat official documentation

2. **Kód nebol problém**
   - Python implementácia bola správna
   - Problém v external dependencies

3. **Version compatibility je kritická**
   - Pervasive v11 → v9 downgrade spôsobil incompatibility
   - File format verzie musia match

4. **BUTIL vs BTRCALL API**
   - Rôzne úrovne validácie
   - BUTIL môže čítať aj "neplatné" súbory

---

## Technické detaily

### Btrieve Status Codes (správne!)

```pascal
// Z BtrConst.pas
B_NO_ERROR                = 0;
B_INVALID_FUNCTION        = 1;
B_IO_ERROR                = 2;
B_FILE_NOT_OPEN           = 3;
...
B_NOT_A_BTRIEVE_FILE      = 30;  // ← Náš problém!
...
B_PERMISSION_ERROR        = 94;  // ← Toto je iný!
...
```

### File Header Info (z BUTIL)

```
File Version = 9.50
Page Size = 4096
Record Length = 705
Total Records = 12454
Keys = 18
Segments = 21
```

---

## Lessons Learned

1. **Vždy verifikovať status code meanings** z official source code
2. **Environment changes môžu byť root cause** (expirovaný trial)
3. **Version downgrades sú risky** - file format compatibility
4. **BUTIL je užitočný diagnostic tool** aj keď API zlyhá
5. **Source code analysis** (Delphi pas súbory) poskytol kritické info

---

**Session End:** 2025-11-27  
**Next Session Focus:** File version analysis a conversion strategy