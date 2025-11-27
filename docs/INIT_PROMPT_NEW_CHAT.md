# Init Prompt - Btrieve Status 30 (NOT_A_BTRIEVE_FILE) Resolution

**Projekt:** NEX Automat  
**Last Session:** 2025-11-27 (Status 161 → Status 30 Investigation)  
**This Session:** File Version Analysis & Conversion Strategy  

---

## Quick Context

NEX Automat je projekt pre kompletnú automatizáciu podnikových procesov pre zákazníkov používajúcich NEX Genesis ERP.

**Aktuálny stav:**
- Version: 2.0.0 (tagged)
- GO-LIVE: ✅ COMPLETE (2025-11-27)
- nexdata Package: ✅ CREATED
- Btrieve Config Lookup: ✅ IMPLEMENTED
- Btrieve Access: ❌ BLOCKED BY STATUS 30 ← **HERE**

---

## Critical Problem Summary

### Status 30 = B_NOT_A_BTRIEVE_FILE

**Symptom:**
```python
client = BtrieveClient()
status, pos_block = client.open_file(r"C:\NEX\YEARACT\STORES\GSCAT.BTR")
# Result: status=30 (NOT_A_BTRIEVE_FILE)
```

**Verified Facts:**
- ✅ Súbory existujú: C:\NEX\YEARACT\STORES\GSCAT.BTR (29.7 MB)
- ✅ Pervasive v9 service beží: psqlWGE RUNNING
- ✅ BUTIL funguje: Dokáže čítať file metadata
- ✅ NEX Genesis funguje: Používa Btrieve úspešne
- ❌ Python BTRCALL API: Status 30 vo VŠETKÝCH projektoch
- ❌ Invoice-editor: TIEŽ status 30 (predtým fungoval)

**Root Cause Hypothesis:**

Súbory boli vytvorené/modifikované **Pervasive v11 Trial** (expirovaná) a sú nekompatibilné s **Pervasive v9 Licensed** API.

---

## What Happened Last Session ✅

### 1. Status 161 → Expirovaný Trial Identified

**Original problem:**
- Status 161 (FILE_NOT_FOUND) všade
- Expirovaná Pervasive 11 Trial verzia

**Solution:**
- Odinštalovanie Pervasive 11 Trial
- Inštalácia Pervasive v9 Licensed
- NEX Genesis začal fungovať ✅

### 2. New Problem: Status 30

**Po downgrade na v9:**
- Status 30 vo všetkých Python projektoch
- BUTIL funguje, BTRCALL API nie

### 3. Code Analysis

**Porovnanie invoice-editor (fungujúce predtým) vs nex-automat:**
- ✅ DLL setup: IDENTICKÝ
- ✅ open_file(): IDENTICKÝ (až na config lookup)
- ✅ Kód je správny!

### 4. Status Code Discovery

**Z BtrConst.pas (Delphi source):**
```pascal
B_NOT_A_BTRIEVE_FILE = 30;  // NIE permission error!
```

**Správny význam:** File format nie je rozpoznaný Btrieve engine!

### 5. Diagnostic Scripts Created

- ✅ test_open_modes.py - testovanie open modes
- ✅ test_owner_names.py - testovanie owner names
- ✅ fix_btrieve_owner_name.py - owner name support
- ✅ test_file_version.py - file header analysis ← **READY TO RUN**

---

## Current Blocking Issue ⚠️

### Btrieve File Format Incompatibility

**Problem:**
Pervasive v11 vytvorené súbory → Pervasive v9 API ich nerozpoznáva

**Evidence:**
1. BUTIL (v9) dokáže čítať metadata → low-level access OK
2. BTRCALL API (v9) hlási "NOT_A_BTRIEVE_FILE" → engine validation fails
3. NEX Genesis funguje → používa iné API alebo special config
4. Všetky Python projekty status 30 → consistent failure

---

## Priority Actions for This Session

### Priority 1: File Version Diagnostics ⚡

**Spustiť file version analysis:**
```cmd
cd C:\Development\nex-automat
venv32\Scripts\python.exe scripts\test_file_version.py
```

**Očakávaný output:**
- File format version (Pervasive v9.x vs v11.x)
- Page size validation
- Header structure analysis
- Version compatibility check

**Cieľ:** Potvrdiť, že súbory sú v11 format.

### Priority 2: BUTIL File Rebuild Test

**Ak súbory sú v11 format, skúsiť BUTIL rebuild:**
```cmd
cd C:\NEX\YEARACT\STORES
BUTIL -create C:\TEMP\GSCAT_V9.BTR [params from -stat]
BUTIL -copy GSCAT.BTR C:\TEMP\GSCAT_V9.BTR
```

**ALEBO:**
```cmd
BUTIL -save GSCAT.BTR GSCAT.DAT
BUTIL -load GSCAT_NEW.BTR GSCAT.DAT [with v9 specs]
```

### Priority 3: NEX Genesis Investigation

**Zistiť ako NEX Genesis pristupuje k Btrieve:**

1. **Check Delphi code v nex-genesis-server:**
   ```pascal
   // BtrHand.pas - BtrOpen function
   // Používa špeciálne parametre?
   ```

2. **Test s Delphi BTRCALL:**
   - Funguje Delphi kód na Pervasive v9?
   - Ak áno, aký je rozdiel oproti Python?

3. **Check NEX Genesis config:**
   - Pervasive Control Center settings
   - Database registration
   - Special compatibility mode?

### Priority 4: Contact NEX Genesis Support

**Informácie na získanie:**
- Recommended Pervasive version
- File migration procedure
- Compatibility notes
- Support for v11 → v9 downgrade

---

## Alternative Solutions

### Option A: Stay on Pervasive v11

**Ak v11 Trial expiroval, získať v11 License:**
- Contact Actian/Pervasive
- Purchase v11 Licensed version
- Súbory budú kompatibilné

**Pros:** Žiadna file conversion potrebná  
**Cons:** Drahšie, možno nedostupné

### Option B: File Format Conversion

**Convert v11 files → v9 format:**
- BUTIL rebuild
- Export → Import
- Custom conversion tool

**Pros:** Zostaneme na v9 Licensed  
**Cons:** Risk of data loss, time consuming

### Option C: ODBC Alternative

**Use Pervasive ODBC driver instead of BTRCALL:**
```python
import pyodbc
conn = pyodbc.connect('DSN=PervasiveSQL;...')
```

**Pros:** Možno funguje aj s v11 files  
**Cons:** Iné API, treba prepísať repositories

### Option D: Direct File Parsing

**Parse Btrieve files directly (bez engine):**
- Implement Btrieve file format parser
- Based on BUTIL successful read

**Pros:** Nezávislé od Pervasive version  
**Cons:** Very complex, high risk

---

## Technical Details

### Pervasive Versions

**Pervasive v9:**
- File format version: 9.x
- Released: ~2009
- w3btrv7.dll location: C:\PVSW\bin

**Pervasive v11:**
- File format version: 11.x
- Released: ~2013
- w3btrv7.dll location: C:\Program Files (x86)\Pervasive Software\PSQL\bin

**Compatibility:** v11 files môžu byť backward incompatible!

### BUTIL vs BTRCALL

**BUTIL:**
- Direct file I/O
- Low-level metadata access
- Bypasses engine validation
- Works with "invalid" files

**BTRCALL API:**
- Uses Btrieve engine
- Strict version validation
- Requires compatible file format
- Status 30 if version mismatch

### File Header Structure

**Typical Btrieve file header:**
```
Offset  Size  Description
0-1     2     File marker (0x46 0x43 = 'FC')
2-3     2     Page size (512, 1024, 2048, 4096)
4-5     2     File version (major.minor)
8-11    4     Record count
16-17   2     File flags
...
```

---

## Available Resources

### Implemented Code (Blocked)

```
packages/nexdata/
└── nexdata/
    ├── btrieve/
    │   └── btrieve_client.py         ← Status 30 error
    ├── repositories/
    │   ├── gscat_repository.py       ← Cannot open
    │   ├── barcode_repository.py     ← Cannot open
    │   ├── mglst_repository.py       ← Cannot open
    │   ├── pab_repository.py         ← Cannot open
    │   ├── tsh_repository.py         ← Cannot open
    │   └── tsi_repository.py         ← Cannot open
    └── models/                       ← 6 models ready
```

### Diagnostic Scripts (Ready)

```
scripts/
├── test_open_modes.py           ← Tested (all mode = status 30)
├── test_owner_names.py          ← Tested (all owners = status 30)
├── fix_btrieve_owner_name.py    ← Applied (no change)
└── test_file_version.py         ← READY TO RUN ⚡
```

### Reference Projects

**nex-genesis-server:**
- Location: C:\Development\nex-genesis-server
- Status: ✅ WORKING with Pervasive v9
- Has Delphi source code for Btrieve access

**invoice-editor:**
- Location: C:\Development\invoice-editor
- Status: ❌ Status 30 (broken after v9 install)
- Was working on Pervasive v11 Trial

---

## When Issue Resolved - Next Steps

Po vyriešení status 30 problému:

### Step 1: Verify Implementation
```cmd
python scripts/04_test_config_lookup.py
```

**Expected:**
- ✅ Config Loading (test 1/4)
- ✅ Path Resolution (test 2/4)
- ✅ GSCAT Read (test 3/4)
- ✅ TSH Read (test 4/4)

### Step 2: Test All Repositories

```python
from nexdata.btrieve.btrieve_client import BtrieveClient
from nexdata.repositories import *

client = BtrieveClient("config/database.yaml")

# Test all repositories
gscat = GSCATRepository(client)
barcode = BARCODERepository(client)
# ... etc
```

### Step 3: Integration Testing

- Read operations
- Filtering
- Dynamic book_id
- Performance
- Error handling

### Step 4: Documentation & Release

- Update README
- Document solution
- Tag version
- Deploy

---

## Important Technical Notes

### Btrieve Status Codes Reference (Correct!)

```pascal
// From BtrConst.pas
B_NO_ERROR                = 0;   // SUCCESS
B_INVALID_FUNCTION        = 1;
B_IO_ERROR                = 2;
B_FILE_NOT_OPEN           = 3;
B_KEY_NOT_FOUND           = 4;
B_DUPLICATE_KEY           = 5;
...
B_NOT_A_BTRIEVE_FILE      = 30;  // ← OUR CURRENT PROBLEM
...
B_PERMISSION_ERROR        = 94;  // Different!
...
B_USER_COUNT_LIMIT_EXCEEDED = 161; // Was our old problem
```

### Environment

**System:**
- Python: 3.13.7 32-bit (venv32)
- Pervasive: v9 Licensed (downgrade from v11 Trial)
- DLL: w3btrv7.dll (C:\PVSW\bin)
- Service: psqlWGE ✅ Running
- OS: Windows

**Paths:**
- NEX: C:\NEX\YEARACT
- Project: C:\Development\nex-automat
- Data: C:\NEX\YEARACT\STORES\*.BTR

---

## Critical Reminders

### Code is NOT the Problem ✅

- Python implementation je správna
- Identická s fungujúcim invoice-editor
- Config lookup funguje
- Problem is external: file format compatibility

### Focus Areas

1. **File version verification** - test_file_version.py
2. **Conversion strategy** - BUTIL rebuild/migration
3. **NEX Genesis analysis** - how does it work?
4. **Support contact** - NEX Genesis / Actian Pervasive

### Do NOT

- ❌ Meniť Python kód (nie je to problém)
- ❌ Testovať ďalšie owner names (už otestované)
- ❌ Testovať ďalšie open modes (už otestované)
- ✅ Focus on file format compatibility!

---

## How to Start This Session

1. **Load SESSION_NOTES.md** for full history

2. **Run file version analysis:**
   ```cmd
   cd C:\Development\nex-automat
   venv32\Scripts\python.exe scripts\test_file_version.py
   ```

3. **Based on results:**
   - If v11 format → Plan conversion
   - If v9 format → Investigate further
   - If corrupted → Recovery strategy

4. **Contact NEX Genesis support** for guidance

---

## Expected Outcome

Po vyriešení file compatibility issue:
- ✅ Status 0 (SUCCESS) namiesto status 30
- ✅ Všetky testy prechádzajú (4/4)
- ✅ Čítanie z 6 tabuliek funguje
- ✅ Production ready

---

**Last Updated:** 2025-11-27 18:00  
**Version:** 1.0  
**Status:** 🔴 BLOCKED - File Format Incompatibility  
**Priority:** ⚡ CRITICAL - Blocking all Btrieve functionality