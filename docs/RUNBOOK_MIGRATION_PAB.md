# Runbook: PAB migration from NEX Genesis to NEX Automat

**Last updated:** 2026-04-27
**Owner:** ICC operator (Director / on-call engineer)
**Context:** Phase G.1 — first per-customer data migration. This runbook covers the **PAB (Partner Catalog)** migration. Other categories follow the same pattern once their extractors/loaders land.

## Prerequisites

- Customer's NEX Manager container is **deployed** (per Phase D — see DECISIONS.md D-024) and accessible at `https://<slug>.isnex.eu`.
- Customer's `<slug>` exists in `/opt/customers/<slug>/` on ANDROS, with `migration/` subdir auto-created by onboard script (Phase G.1.1).
- Customer's NEX Genesis Windows machine is reachable (RDP, onsite, or VPN).
- Operator has SSH access to ANDROS (`andros@100.107.134.104`) and admin login on `https://<slug>.isnex.eu`.

## Time budget

- First customer: **~60 minutes** (includes one-time Python install on Windows)
- Repeat / re-run: **~5-10 minutes**

## Phase 1 — Set up extractor on customer Windows machine (one-time per machine)

Skip this phase on subsequent runs for the same customer.

### 1.1 Install Python 3.11 32-bit on Windows

> **Why 32-bit:** the Btrieve runtime DLL shipped with NEX Genesis is 32-bit. Python `ctypes` requires same-bitness DLLs, so 64-bit Python cannot load it.

1. Download the **32-bit** Windows installer: https://www.python.org/downloads/release/python-3110/ → "Windows installer (32-bit)"
2. Run installer:
   - ☑ Add Python to PATH
   - Customize install path (e.g. `C:\Python311-32`) so it doesn't collide with any 64-bit Python you already have
3. Verify in Command Prompt:
   ```cmd
   python --version
   python -c "import struct; print(struct.calcsize('P')*8)"
   ```
   Must show `Python 3.11.x` and `32`.

### 1.2 Copy extractor bundle to Windows machine

The bundle is in `scripts/windows-extractor/` of the `nex-automat` repo. Two options:

**Option A — git clone (preferred if Windows has git installed):**
```cmd
cd C:\
git clone https://github.com/rauschiccsk/nex-automat.git
cd nex-automat\scripts\windows-extractor
```

**Option B — download zip:**
1. Open https://github.com/rauschiccsk/nex-automat/archive/refs/heads/develop.zip in browser
2. Save + extract to `C:\nex-automat-develop\`
3. `cd C:\nex-automat-develop\scripts\windows-extractor`

### 1.3 Run install script

```cmd
install.bat
```

Expected output (excerpt):
```
[install] Python 3.11 32-bit OK.
[install] Creating venv32...
[install] Installing dependencies...
[install] Installing nexdata from local source...
[install] w3btrv7.dll OK.
═══════════════════════════════════════════════════════════════
 Installation complete.
═══════════════════════════════════════════════════════════════
```

Troubleshooting: see `scripts/windows-extractor/README.md` "Troubleshooting" section.

## Phase 2 — Run extract for one customer

### 2.1 Identify customer's NEX Genesis data root

The path varies per customer. Verify the PAB Btrieve file exists:

```cmd
dir C:\ICC\NEX\YEARACT\DIALS\PAB00000.BTR
```

(Replace `C:\ICC` with the actual customer path: `C:\ANDROS`, `C:\MAGER`, etc.)

### 2.2 Run PAB extract

```cmd
cd C:\nex-automat\scripts\windows-extractor
extract-pab.bat C:\ICC\NEX
```

Expected output:
```
[extract] Running PAB extraction...
  data-root: C:\ICC\NEX
  output:    C:\nex-automat\scripts\windows-extractor\output\PAB\PAB.json

PABExtractor: <N>/<N> records → C:\...\output\PAB\PAB.json
═══════════════════════════════════════════════════════════════
 Extract complete.
═══════════════════════════════════════════════════════════════
```

**Sanity check:** open `output\PAB\PAB.json` in Notepad. Should contain a JSON object with `total_extracted`, `record_count`, and a non-empty `records` array.

If `total_source: 0` — verify `--data-root` and that NEX Genesis on this machine actually has data.

## Phase 3 — Transfer JSON to ANDROS

### 3.1 SCP from Windows to ANDROS

In a Command Prompt on Windows (or in PowerShell — both have built-in `scp`):

```cmd
scp output\PAB\PAB.json andros@100.107.134.104:/opt/customers/<SLUG>/migration/PAB/PAB.json
```

Replace `<SLUG>` with the actual customer slug (`icc`, `andros`, `mager`, ...).

If the destination directory doesn't exist (it should after onboard), create it first via SSH:
```bash
ssh andros@100.107.134.104 "mkdir -p /opt/customers/<SLUG>/migration/PAB"
```

### 3.2 Verify on ANDROS

```bash
ssh andros@100.107.134.104 "ls -la /opt/customers/<SLUG>/migration/PAB/"
```

Should show `PAB.json` with size > 0.

## Phase 4 — Trigger migration via NEX Manager UI

### 4.1 Login

1. Open `https://<slug>.isnex.eu` in browser
2. Log in with admin credentials (or any user with `MIG.can_create` permission)

### 4.2 Open Migration module

Sidebar → **Migration**

### 4.3 Run dry-run first (recommended)

1. Find category card **PAB — Katalóg partnerov**
2. Toggle **Dry run** ON
3. Click **Spustiť migráciu**
4. Verify: response shows `status: dry_run` + non-zero `target_count` (matches the partner count in NEX Genesis). No DB rows are inserted yet.

If dry-run shows `error_count > 0`, click **Errors** to see details. Fix on customer Windows side, re-run extract, re-transfer, re-dry-run.

### 4.4 Run the actual load

1. Toggle **Dry run** OFF
2. Click **Spustiť migráciu**
3. Wait for completion (small DBs <1s, large DBs up to ~30s)
4. Response shows `status: completed`, `target_count` = inserted+updated count.

### 4.5 Verify in DB

UI side: navigate to **Partneri** module — list should show real customer data with names, IČO, addresses.

Operator side (optional, for paranoia):
```bash
ssh andros@100.107.134.104 "docker exec <SLUG>-postgres psql -U postgres -d nex_automat -c 'SELECT COUNT(*) FROM partner_catalog'"
```

Count should match `target_count` from the run response.

## Phase 5 — Re-running

The migration is **idempotent**. If customer adds new partners in NEX Genesis tomorrow and wants them in NEX Automat:

1. Re-run `extract-pab.bat C:\ICC\NEX` on Windows
2. SCP the new `PAB.json` (overwrites previous)
3. Re-trigger via UI **Spustiť migráciu**

The loader uses UPSERT pattern via `migration_id_map` (matches Btrieve `pab_code` → existing `partner_catalog.id`). New records → insert. Existing records → update (changed fields).

**WARNING:** the loader does NOT delete partners that were removed from NEX Genesis. If a customer deletes a partner in NEX Genesis, that partner stays in NEX Automat unless manually removed. This is intentional — accidental deletes shouldn't propagate. If full sync (delete-orphan) is needed, raise it as a future enhancement.

## Common errors

| Error response (HTTP code) | Likely cause | Fix |
|---|---|---|
| 422 "PAB extract data not found at /migration/PAB/PAB.json" | JSON file not transferred or wrong path | Re-do Phase 3.1 with correct slug |
| 400 "Nesplnené závislosti" | PAB has no deps so this shouldn't happen for PAB; for later categories means parent (e.g. PAB) wasn't migrated yet | Migrate parent category first |
| 409 "už beží migrácia" | Concurrent request — another operator triggered a run | Wait for it to finish, check `/api/migration/batches` |
| 500 + transformer errors | Field mapping mismatch (NEX Genesis schema differs from expected) | Check error details in batch response; likely a field is renamed/missing |

## Audit trail

Every run is recorded in:
- `migration_batches` table — start/end time, status, source/target counts, error log
- `migration_id_map` table — Btrieve key → PostgreSQL UUID mapping (one row per migrated record per category)
- `audit_logs` table — user_id, action="migration_run_attempt", entity_id=category

Inspect via UI **Migration → History** or via SQL:
```sql
SELECT id, category, status, source_count, target_count, error_count, started_at, completed_at
FROM migration_batches ORDER BY id DESC LIMIT 10;
```

## Future improvements

- Pyinstaller-built `nex-extract.exe` so customer machines don't need Python install (G.2.a, planned)
- `/api/migration/upload` endpoint so JSON upload happens via authenticated REST instead of SCP (G.2.b, planned)
- Self-service flow in MIG module UI for non-technical customer admins (G.2.c, planned)
- Implement remaining 8 categories: GSC, STK, TSH, ICB, ISB, OBJ, DOD, PAYJRN (H.1, H.2)
