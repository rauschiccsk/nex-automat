# NEX Genesis → NEX Automat — Windows Extractor

Extracts data from NEX Genesis (Btrieve) on a Windows machine and produces
JSON files ready to be loaded into a NEX Automat per-customer PostgreSQL DB
on ANDROS.

## What this is for

NEX Genesis stores its data in 32-bit Btrieve `.BTR` files. NEX Automat
runs on Linux/Ubuntu and uses PostgreSQL. This extractor is the
**Windows-only** extract step of the two-layer ETL — it reads `.BTR` files
via the local Btrieve runtime DLL and writes structured JSON.

The JSON is then transferred to ANDROS and loaded into the customer's
container DB via the NEX Manager `/api/migration/run` endpoint.

## Prerequisites on the Windows machine

1. **NEX Genesis** is already installed and running (this means the
   Btrieve runtime DLL `w3btrv7.dll` or `wbtrv32.dll` is present).
2. **Python 3.11 32-bit** — must be **32-bit** because the Btrieve DLL is
   32-bit and Python ctypes can only call same-bitness DLLs.
   Download: https://www.python.org/downloads/release/python-3110/
   File: `Windows installer (32-bit)`. During install, tick "Add to PATH".
3. **Network access** to ANDROS (or just to `<slug>.isnex.eu`) for
   transferring the JSON output.

## Installation

Run this **once** on the Windows machine where NEX Genesis lives:

```cmd
cd C:\nex-extract
install.bat
```

This will:
- Create a 32-bit virtual environment in `C:\nex-extract\venv32`
- Install `nexdata` package (Btrieve client + repositories)
- Install the migration extract code
- Verify the Btrieve DLL is reachable

If `install.bat` fails with "32-bit Python not found", check `python --version`
and `python -c "import struct; print(struct.calcsize('P')*8)"` — must say
`3.11.x` and `32` respectively.

## Running an extract

```cmd
cd C:\nex-extract
extract-pab.bat C:\ICC\NEX
```

The argument is the **NEX Genesis data root** for the customer being
extracted. Examples:
- ICC s.r.o.: `C:\ICC\NEX`
- ANDROS s.r.o.: `C:\ANDROS\NEX`
- MAGERSTAV: `C:\MAGER\NEX`

Output: `C:\nex-extract\output\PAB\PAB.json` plus a console summary
(record count, errors).

## Transferring to ANDROS

Once the extract is done, the operator transfers `C:\nex-extract\output\PAB\PAB.json`
to ANDROS into the per-customer migration drop directory:

```bash
# On ANDROS (run from operator's terminal — your laptop, RDP host, or via SSH)
scp PAB.json andros@100.107.134.104:/opt/customers/icc/migration/PAB/PAB.json
```

For ICC: the path is `/opt/customers/icc/migration/PAB/PAB.json` (note the
`PAB/` subdir — the loader expects category-named subdirs).

## Triggering the load on NEX Manager

After PAB.json is on ANDROS, the customer admin (or operator) loads it via
the NEX Manager UI:

1. Open `https://icc.isnex.eu` and log in (admin or any user with `MIG.can_create`)
2. Go to **Migration** module
3. Select category **PAB — Katalóg partnerov**
4. Click **Run migration** (toggle Dry run first to validate)

Or via API:
```bash
curl -X POST https://icc.isnex.eu/api/migration/run \
     -H "Authorization: Bearer <JWT>" \
     -H "Content-Type: application/json" \
     -d '{"category":"PAB","dry_run":false}'
```

## Re-running

The migration is **idempotent** — re-running PAB extracts a fresh JSON,
transferring + loading does an UPSERT into `partner_catalog*` tables (matched
on Btrieve `pab_code` via `migration_id_map`). To re-run:

1. Run `extract-pab.bat C:\ICC\NEX` again
2. SCP the new `PAB.json` (overwrites previous)
3. Trigger `/api/migration/run` again

## What's included in this bundle

```
scripts/windows-extractor/
├── README.md                 # This file
├── install.bat               # One-time setup: creates venv32, installs deps
├── extract-pab.bat           # Run PAB extract (1 arg: NEX data root path)
└── requirements.txt          # Python dependencies (nexdata + transitive)
```

## Troubleshooting

**`ImportError: DLL load failed while importing _ctypes`** — Python is 64-bit;
reinstall 32-bit version.

**`Btrieve status code 11` / `12` / `48`** — Btrieve runtime not reachable.
Check that NEX Genesis still works on this machine; the runtime DLL must be
in `PATH` or `C:\Windows\SysWOW64\`.

**Empty `records: []` in PAB.json** — `--data-root` doesn't point to a
populated NEX Genesis install. Verify the path exists:
`dir C:\ICC\NEX\YEARACT\DIALS\PAB00000.BTR`

**Connection refused to ANDROS** — check ANDROS firewall (SSH port 22) and
your VPN if applicable.
