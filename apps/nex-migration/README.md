# NEX Migration — Btrieve → PostgreSQL ETL

Migračný modul pre presun dát z NEX Genesis (Btrieve) do NEX Automat (PostgreSQL).

## Architektúra

Dvojvrstvová ETL architektúra:

```
┌─────────────────────┐          ┌──────────────────────────────────┐
│   WINDOWS CC        │  JSON    │   UBUNTU CC                      │
│   (venv32, 32-bit)  │  files   │   (normálny Python 3.11+)        │
│                     │ ───────► │                                  │
│   run_extract.py    │          │   run_load.py                    │
│   ├─ BaseExtractor  │          │   ├─ BaseTransformer             │
│   └─ PABExtractor   │          │   ├─ PABTransformer              │
│                     │          │   ├─ BaseLoader                  │
│   Btrieve DLL       │          │   └─ PABLoader                   │
│   (w3btrv7.dll)     │          │                                  │
│                     │          │   PostgreSQL (pg8000)             │
└─────────────────────┘          └──────────────────────────────────┘
```

### Extract (Windows)
- Beží na Windows CC s venv32 (32-bit Python pre Btrieve DLL)
- Číta priamo z .BTR súborov cez nexdata repositories
- Výstup: JSON súbory v `data/{category}/`

### Transform + Load (Ubuntu)
- Beží na Ubuntu CC s normálnym Python 3.11+
- Transformuje JSON dáta na PostgreSQL-ready záznamy
- UPSERT do PostgreSQL cez pg8000 driver

## Dependency graf kategórií

```
Úroveň 0 (bez závislostí):
  PAB — Katalóg partnerov
  GSC — Katalóg produktov

Úroveň 1:
  STK — Skladové karty          ← závisí na GSC

Úroveň 2:
  TSH — Dodávateľské DDL        ← závisí na PAB, GSC, STK
  ICB — Odberateľské faktúry    ← závisí na PAB, GSC
  ISB — Dodávateľské faktúry    ← závisí na PAB, GSC
  OBJ — Objednávky              ← závisí na PAB, GSC
  DOD — Dodacie listy           ← závisí na PAB, GSC

Úroveň 3:
  PAYJRN — Platobný denník      ← závisí na ICB, ISB
```

## Požiadavky

### Extract (Windows CC)
- Python 3.11+ (32-bit) v `venv32`
- nexdata package (Btrieve client)
- Btrieve DLL (w3btrv7.dll alebo wbtrv32.dll)

### Transform + Load (Ubuntu CC)
- Python 3.11+
- pg8000 (PostgreSQL driver)
- Prístup k PostgreSQL databáze

## Použitie

### 1. Extract (na Windows CC)

```bash
# Aktivuj 32-bit venv
venv32\Scripts\activate

# Extrahuj PAB (partneri) — default data root C:\NEX
python run_extract.py --category PAB --data-dir data

# Extrahuj PAB s vlastným data root (napr. DEPTEST)
python run_extract.py --category PAB --data-root C:\DEPTEST\NEX
```

### Data root

Parameter `--data-root` určuje koreňový adresár NEX Genesis dát (Btrieve .BTR súbory).
Predvolená hodnota je `C:\NEX`.

| Prostredie | Data root            | Popis                        |
|------------|----------------------|------------------------------|
| ICC        | `C:\NEX`             | Produkcia ICC (default)      |
| DEPTEST    | `C:\DEPTEST\NEX`     | Testovacie prostredie        |
| MAGER      | `C:\MAGER\NEX`       | Produkcia MAGER              |
| ANDROS     | `C:\ANDROS\NEX`      | Produkcia ANDROS             |

Príklad použitia:
```bash
# ICC (default — netreba špecifikovať)
python run_extract.py --category PAB

# DEPTEST
python run_extract.py --category PAB --data-root C:\DEPTEST\NEX

# MAGER
python run_extract.py --category PAB --data-root C:\MAGER\NEX
```

### 2. Transfer JSON súborov

```bash
# SCP z Windows na Ubuntu (alebo zdieľaný adresár)
scp -r data/PAB/ ubuntu-cc:/opt/nex-automat-src/apps/nex-migration/data/PAB/
```

### 3. Transform + Load (na Ubuntu CC)

```bash
# Dry run — len transformácia, bez zápisu do DB
python run_load.py --category PAB --dry-run

# Ostrý beh — transform + UPSERT do PostgreSQL
python run_load.py --category PAB
```

## Príklad workflow pre PAB migráciu

```bash
# 1. Windows CC: Extract
python run_extract.py --category PAB
# → data/PAB/PAB.json, data/PAB/PAYLST.json, ...

# 2. Transfer na Ubuntu CC
scp -r data/PAB/ ubuntu:/opt/.../nex-migration/data/PAB/

# 3. Ubuntu CC: Dry run
python run_load.py --category PAB --dry-run
# → 2500 records would be loaded

# 4. Ubuntu CC: Load
python run_load.py --category PAB
# → Batch #1 started, 2500 records to load
# → Inserted: 2500, Updated: 0, Errors: 0
```

## DB tabuľky (migration tracking)

### migration_batches
Každý beh migrácie je jeden batch:
- `id` — auto-increment ID
- `category` — kód kategórie (PAB, GSC, ...)
- `status` — running / completed / failed
- `source_count` / `target_count` / `error_count`
- `started_at` / `completed_at`
- `error_log` — JSON s detailmi chýb

### migration_id_map
Most medzi Btrieve kľúčmi a PostgreSQL UUID:
- `source_table` + `source_key` → `target_table` + `target_id`
- UNIQUE constraint na (category, source_table, source_key)
- Umožňuje re-run migrácie (UPSERT)

### migration_category_status
Stav migrácie pre každú kategóriu:
- `category` — kód kategórie (UNIQUE)
- `status` — pending / completed / failed
- `record_count` — počet migrovaných záznamov
- `first_migrated_at` / `last_migrated_at`

## Adresárová štruktúra

```
apps/nex-migration/
├── __init__.py
├── README.md
├── run_extract.py              # CLI — Extract (Windows)
├── run_load.py                 # CLI — Transform + Load (Ubuntu)
├── config/
│   ├── __init__.py
│   ├── categories.py           # Dependency graf 9 kategórií
│   └── field_mappings.py       # PAB field mappings (Btrieve → PG)
├── extract/
│   ├── __init__.py
│   └── base_extractor.py       # Abstraktná trieda pre extractory
├── transform/
│   ├── __init__.py
│   ├── base_transformer.py     # Abstraktná trieda pre transformery
│   └── transforms.py           # Transformačné funkcie (strip, to_bool, ...)
├── load/
│   ├── __init__.py
│   └── base_loader.py          # Abstraktná trieda pre loadery
├── data/                       # JSON dáta (NIE v Git)
│   ├── .gitignore
│   ├── README.md
│   ├── PAB/
│   ├── GSC/
│   ├── STK/
│   ├── TSH/
│   ├── ICB/
│   └── ISB/
└── tests/
    └── __init__.py
```
