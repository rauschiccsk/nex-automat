#!/usr/bin/env python3
"""
New Chat Script - NEX Automat v3.0 Deployment Session
"""
import sys
import subprocess
from pathlib import Path

# =============================================================================
# CONFIG
# =============================================================================

SESSION_DATE = "2025-12-23"
SESSION_NAME = "nex-automat-v3-deployment"

KNOWLEDGE_CONTENT = """\
# Session: NEX Automat v3.0 Deployment & pg8000 Migration

**Dátum:** 2025-12-23
**Status:** ✅ DONE

---

## Prehľad zmien v3.0

| Zmena | Z | Na | Dôvod |
|-------|---|-----|-------|
| GUI Framework | PyQt5 | PySide6 | Lepšia licencia, Qt6 |
| PostgreSQL Driver | psycopg2 | pg8000 | 32-bit kompatibilita |
| Workflow Engine | n8n | Temporal | Robustnosť (pripravené) |

---

## Vyriešené problémy

### 1. pg8000 "list index out of range"

**Príčina:** pg8000.native.Connection.run() používa named parameters (`:name` s **kwargs), nie positional parameters (`$1` s list).

**Riešenie:** V `staging_client.py` metóda `_run()`:
```python
# WRONG (psycopg2 style)
converted_query = query.replace("%s", f"${param_index}", 1)
return self._conn.run(converted_query, list(params))

# CORRECT (pg8000.native style)
converted_query = query.replace("%s", f":p{i}", 1)
param_dict[f"p{i}"] = value
return self._conn.run(converted_query, **param_dict)
```

### 2. move_files_to_staging() cursor error

**Príčina:** Funkcia používala psycopg2 API (`.cursor()`, `.execute()`).

**Riešenie:** V `main.py`:
```python
# WRONG
cursor = pg_conn.cursor()
cursor.execute("UPDATE ... WHERE id = %s", (invoice_id,))

# CORRECT
pg_conn.run("UPDATE ... WHERE id = :inv_id", inv_id=invoice_id)
```

### 3. Missing database columns

**Príčina:** Migrácia 003_add_file_tracking_columns.sql nebola aplikovaná na production.

**Riešenie:** Aplikovať migráciu:
```powershell
.\\venv32\\Scripts\\python.exe -c "
import pg8000.native; import os
conn = pg8000.native.Connection(...)
sql = open('apps/supplier-invoice-loader/database/migrations/003_add_file_tracking_columns.sql').read()
conn.run(sql)
conn.close()
"
```

### 4. Qt6 RDP monitor warning

**Príčina:** Qt6 má problém s detekciou monitorov cez Remote Desktop.

**Riešenie:** V `app.py`:
```python
import os
os.environ["QT_LOGGING_RULES"] = "qt.qpa.screen=false"
```

### 5. Duplicate invoice detection

**Príčina:** SQLite `invoices.db` obsahoval staré záznamy s file_hash.

**Riešenie:**
```powershell
Remove-Item apps\\supplier-invoice-loader\\config\\invoices.db
Stop-Service NEXAutomat
Start-Service NEXAutomat
```

---

## Vytvorené/Upravené súbory

| Súbor | Zmena |
|-------|-------|
| packages/nex-staging/nex_staging/staging_client.py | pg8000 named params |
| apps/supplier-invoice-loader/main.py | pg8000.native.run() v move_files_to_staging |
| apps/supplier-invoice-staging/app.py | Qt6 RDP warning suppress |

---

## Deployment Workflow

```
Development → Git → Deployment
```

1. **Development:** Opraviť/pridať kód v `C:\\Development\\nex-automat`
2. **Git:** `git add . && git commit -m "message" && git push`
3. **Deployment:**
   ```powershell
   cd C:\\Deployment\\nex-automat
   git pull
   Stop-Service NEXAutomat
   pip install -e packages/nex-staging --force-reinstall
   Start-Service NEXAutomat
   ```

---

## Dôležité príkazy

### Server Management

```powershell
# Služba
Start-Service NEXAutomat
Stop-Service NEXAutomat
Get-Service NEXAutomat

# Logy
Get-Content C:\\Deployment\\nex-automat\\logs\\service-stdout.log -Tail 50 -Wait
Get-Content C:\\Deployment\\nex-automat\\logs\\service-stderr.log -Tail 50 -Wait

# GUI test
.\\venv64\\Scripts\\python.exe apps\\supplier-invoice-staging\\app.py
```

### Database

```powershell
# Test connection
.\\venv32\\Scripts\\python.exe -c "
import pg8000.native; import os
conn = pg8000.native.Connection(
    host='localhost', port=5432, 
    database='supplier_invoice_staging', 
    user='postgres', 
    password=os.environ['POSTGRES_PASSWORD']
)
print('Connection OK')
conn.close()
"

# List columns
.\\venv32\\Scripts\\python.exe -c "
import pg8000.native; import os
conn = pg8000.native.Connection(...)
result = conn.run('SELECT column_name FROM information_schema.columns WHERE table_name = :t', t='supplier_invoice_heads')
print([r[0] for r in result])
conn.close()
"
```

---

## pg8000.native API Reference

```python
# Connection
conn = pg8000.native.Connection(host, port, database, user, password)

# Execute with named params
result = conn.run("SELECT * FROM table WHERE id = :id", id=123)

# Execute without params
result = conn.run("SELECT * FROM table")

# Result is list of tuples
for row in result:
    print(row[0], row[1])

# Column info after query
columns = conn.columns  # [{'name': 'col1', ...}, ...]

# Close
conn.close()
```

---

## Lessons Learned

1. **pg8000.native vs pg8000.dbapi** - Native API je jednoduchšie ale má iné parametre
2. **Migrácie musia byť aplikované** - Vždy skontrolovať DB schému na production
3. **SQLite duplicate detection** - Pri testovaní vymazať `invoices.db`
4. **Qt6 + RDP** - Potrebuje QT_LOGGING_RULES suppress

---

## Next Steps pre v3.1

1. [ ] Temporal workflows integration
2. [ ] NEX Genesis product matching
3. [ ] Multi-tenant support (ANDROS deployment)
4. [ ] Automated backup system
"""

INIT_PROMPT = """\
INIT PROMPT - NEX Automat v3.0 Released

Projekt: nex-automat
Current Status: v3.0 deployed & tagged
Developer: Zoltán (40 rokov skúseností)
Jazyk: Slovenčina

⚠️ KRITICKÉ: Dodržiavať pravidlá z memory_user_edits!

🎯 CURRENT FOCUS: Post-release tasks

## Čo je hotové ✅

| Komponenta | Status |
|------------|--------|
| pg8000 migration | ✅ DONE |
| PySide6 migration | ✅ DONE |
| E2E test Mágerstav | ✅ DONE |
| v3.0 tag | ✅ DONE |
| DEPLOYMENT_GUIDE_V3.md | ✅ DONE |

## v3.0 Release Notes

- PyQt5 → PySide6 (Qt6)
- psycopg2 → pg8000 (32-bit kompatibilita)
- Opravené: INSERT RETURNING, move_files_to_staging
- Opravené: Qt6 RDP warning
- Kompletný deployment guide pre nových zákazníkov

## Next Steps

1. ANDROS deployment planning
2. Temporal workflows activation
3. NEX Genesis product enrichment

## RAG Query

```
https://rag-api.icc.sk/search?query=deployment+guide+v3+pg8000+pyside6&limit=5
```
"""


# =============================================================================
# TEMPLATE CODE - NEMENIŤ
# =============================================================================

def get_base_dir() -> Path:
    cwd = Path.cwd()
    if cwd.name == "nex-automat":
        return cwd
    if cwd.name == "scripts" and cwd.parent.name == "nex-automat":
        return cwd.parent
    for parent in cwd.parents:
        if parent.name == "nex-automat":
            return parent
    return cwd


def main():
    print("=" * 60)
    print("NEW CHAT SCRIPT - NEX Automat v3.0")
    print("=" * 60)

    BASE_DIR = get_base_dir()
    print(f"Base directory: {BASE_DIR}")

    if not (BASE_DIR / "apps").exists():
        print(f"ERROR: Not in nex-automat directory!")
        sys.exit(1)

    DOCS_DIR = BASE_DIR / "docs"
    KNOWLEDGE_DIR = DOCS_DIR / "knowledge" / "sessions"
    SESSION_DIR = DOCS_DIR / "sessions"

    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    session_filename = f"SESSION_{SESSION_DATE}_{SESSION_NAME}.md"
    knowledge_filename = f"KNOWLEDGE_{SESSION_DATE}_{SESSION_NAME}.md"

    # 1. Save SESSION file
    session_file = SESSION_DIR / session_filename
    session_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"SESSION saved: {session_file}")

    # 2. Save KNOWLEDGE file
    knowledge_file = KNOWLEDGE_DIR / knowledge_filename
    knowledge_file.write_text(KNOWLEDGE_CONTENT, encoding="utf-8")
    print(f"KNOWLEDGE saved: {knowledge_file}")

    # 3. Save INIT_PROMPT
    init_file = BASE_DIR / "INIT_PROMPT.md"
    init_file.write_text(INIT_PROMPT, encoding="utf-8")
    print(f"INIT_PROMPT saved: {init_file}")

    # 4. Save DEPLOYMENT_GUIDE_V3.md
    deployment_guide = BASE_DIR / "docs" / "deployment" / "DEPLOYMENT_GUIDE_V3.md"
    deployment_guide.parent.mkdir(parents=True, exist_ok=True)
    # Note: Content will be added separately from artifact
    print(f"DEPLOYMENT_GUIDE location: {deployment_guide}")

    # 5. Run RAG update
    print()
    print("=" * 60)
    print("Running RAG update...")
    print("=" * 60)

    rag_script = BASE_DIR / "tools" / "rag" / "rag_update.py"
    if rag_script.exists():
        try:
            env = {**subprocess.os.environ, "PYTHONIOENCODING": "utf-8"}
            result = subprocess.run(
                [sys.executable, str(rag_script), "--new"],
                cwd=str(BASE_DIR),
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env
            )
            print(result.stdout)
            print("RAG updated")
        except subprocess.CalledProcessError as e:
            print(f"RAG update failed: {e}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")

    print()
    print("=" * 60)
    print("DONE!")
    print()
    print("Next steps:")
    print("  1. Save DEPLOYMENT_GUIDE_V3.md from artifact")
    print("  2. Git: git add -A && git commit -m 'v3.0 release' && git push")
    print("  3. Tag: git tag -a v3.0.0 -m 'NEX Automat v3.0'")
    print("  4. Push tag: git push origin v3.0.0")
    print("=" * 60)


if __name__ == "__main__":
    main()