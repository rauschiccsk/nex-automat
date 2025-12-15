# Workflow Quick Reference

**Kategória:** Reference  
**Status:** 🟢 Complete  
**Vytvorené:** 2025-12-05  
**Aktualizované:** 2025-12-15  
**Related:** [GIT_WORKFLOW.md](../development/GIT_WORKFLOW.md), [SETUP_GUIDE.md](../development/SETUP_GUIDE.md)

---

## Obsah

- [Session Workflow](#session-workflow)
- [File Access Commands](#file-access-commands)
- [Quick Decision Tree](#quick-decision-tree)
- [Common Paths](#common-paths)
- [Output Format](#output-format)
- [Benefits](#benefits)
- [When NOT to use](#when-not-to-use)
- [Troubleshooting](#troubleshooting)

---

## Session Workflow

### 1️⃣ Session Start

**Priloženým manifestom** do chatu:
```
PROJECT_MANIFEST.json
```

**Účel:** Dať Claude prehľad o projekte

---

### 2️⃣ Active Development

**Claude píše:** "Potrebujem vidieť main_window.py"

**Ty píšeš:**
```powershell
python scripts\read_project_file.py apps/supplier-invoice-editor/src/ui/main_window.py
```

**Ty:**
- Copy-paste OUTPUT do chatu
- ✅ Hotovo!

---

### 3️⃣ Session End

**Git commit + push:**
```powershell
git add .
git commit -m "fix: ..."
git push origin develop
```

**Účel:** Verziovanie, backup, audit trail

---

## File Access Commands

### One File
```powershell
python scripts\read_project_file.py <relative_path>
```

**Example:**
```powershell
python scripts\read_project_file.py apps/supplier-invoice-editor/src/ui/main_window.py
```

---

### Multiple Files - Module
```powershell
python scripts\read_module_files.py --module <module_path>
```

**Example:**
```powershell
python scripts\read_module_files.py --module apps/supplier-invoice-editor/src/ui/widgets
```

---

### Multiple Files - Specific
```powershell
python scripts\read_module_files.py <file1> <file2> <file3>
```

**Example:**
```powershell
python scripts\read_module_files.py apps/supplier-invoice-editor/src/utils/window_settings.py apps/supplier-invoice-editor/src/utils/grid_settings.py
```

---

### Multiple Files - Pattern
```powershell
python scripts\read_module_files.py --pattern "<glob_pattern>"
```

**Example:**
```powershell
python scripts\read_module_files.py --pattern "apps/*/src/utils/*.py"
```

---

## Quick Decision Tree

```
Potrebujem...
│
├─ Prehľad projektu? 
│  └─ → Priložený PROJECT_MANIFEST.json
│
├─ 1 súbor?
│  └─ → python scripts\read_project_file.py <path>
│
├─ Celý modul?
│  └─ → python scripts\read_module_files.py --module <path>
│
├─ 2-5 súborov?
│  └─ → python scripts\read_module_files.py <file1> <file2> ...
│
└─ Súbory podľa pattern?
   └─ → python scripts\read_module_files.py --pattern "<pattern>"
```

---

## Common Paths

### Main Application
```
apps/supplier-invoice-editor/main.py
apps/supplier-invoice-editor/config/config.yaml
```

### UI Layer
```
apps/supplier-invoice-editor/src/ui/main_window.py
apps/supplier-invoice-editor/src/ui/invoice_detail_window.py
```

### Widgets Module
```
--module apps/supplier-invoice-editor/src/ui/widgets
```

### Utils Module
```
--module apps/supplier-invoice-editor/src/utils
```

### Business Logic
```
apps/supplier-invoice-editor/src/business/invoice_service.py
apps/supplier-invoice-editor/src/business/nex_lookup_service.py
```

### Database
```
apps/supplier-invoice-editor/src/database/postgres_client.py
```

---

## Output Format

**Script output vyzerá:**
```
================================================================================
READ PROJECT FILE
================================================================================

File: apps/supplier-invoice-editor/src/ui/main_window.py
Path: C:\Development\nex-automat\apps\...

✅ File loaded successfully
   Size: 9,156 bytes
   Lines: 269
   Encoding: utf-8

--------------------------------------------------------------------------------
CONTENT:
--------------------------------------------------------------------------------
[CELÝ OBSAH SÚBORU]
--------------------------------------------------------------------------------

================================================================================
```

**Ty copy-paste CELÝ output do chatu.**

---

## Benefits

✅ **Rýchle** - disk read vs web request  
✅ **Real-time** - vidíme uncommitted changes  
✅ **Spoľahlivé** - žiadne GitHub problémy  
✅ **Batch** - viacero súborov naraz  
✅ **Presné** - žiadne hľadanie v exploreri

---

## When NOT to use

❌ **Cross-machine work** - nie si na dev PC  
❌ **History review** - potrebuješ vidieť čo sa zmenilo medzi sessionami  
❌ **Audit** - potrebuješ Git history  

**V týchto prípadoch:** Použiť GitHub

---

## Troubleshooting

### Script nenájde súbor
```
ERROR: File does not exist
```

**Fix:**
- Over cestu (musí byť relatívna od project root)
- Over že súbor existuje
- Skús absolute path

### Python not found
```
'python' is not recognized
```

**Fix:**
```powershell
C:\Development\nex-automat\venv32\Scripts\python.exe scripts\read_project_file.py ...
```

---

**See Also:**
- [GIT_WORKFLOW.md](../development/GIT_WORKFLOW.md) - Git branching a commit workflow
- [SETUP_GUIDE.md](../development/SETUP_GUIDE.md) - Nastavenie vývojového prostredia
- [API_REFERENCE.md](API_REFERENCE.md) - API dokumentácia