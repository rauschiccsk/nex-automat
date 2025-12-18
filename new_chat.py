"""
Create new chat artifacts: SESSION archive, update ARCHIVE_INDEX, create INIT_PROMPT, run RAG update.
Run from: C:/Development/nex-automat
"""

import subprocess
from datetime import datetime
from pathlib import Path

SESSION_NAME = "supplier-invoice-staging-gui-testing"
SESSION_DATE = datetime.now().strftime("%Y-%m-%d")


def create_session_archive():
    """Create SESSION_*.md archive file."""
    content = f"""# Session: {SESSION_NAME}

**Dátum:** {SESSION_DATE}
**Projekt:** nex-automat
**Stav:** COMPLETED

---

## Prehľad Session

Testovanie a vylepšovanie GUI aplikácie supplier-invoice-staging (PySide6).

---

## Dokončené Úlohy

### 1. Klávesové skratky
- ✅ Enter v hlavičkách faktúr otvára položky
- ✅ ESC v položkách zatvára okno
- ✅ ESC v hlavičkách zatvára aplikáciu

### 2. Modálne okno položiek
- ✅ InvoiceItemsWindow je teraz ApplicationModal
- ✅ Len jedna faktúra môže byť otvorená naraz
- ✅ Jednotná pozícia okna pre všetky faktúry

### 3. Grid Settings Persistence
- ✅ save_grid_settings_now() volaný pri closeEvent oboch okien
- ✅ Nastavenia sa ukladajú pri zatvorení každého okna

### 4. Initial Row Selection
- ✅ BaseGrid.select_initial_row() - nová metóda
- ✅ Automatický výber prvého riadku po načítaní dát
- ✅ Focus na table_view v InvoiceItemsWindow

### 5. Header Context Menu (BaseGrid)
- ✅ Pravý klik na header → context menu
- ✅ "Premenovať '...'..." - dialóg pre vlastný názov stĺpca
- ✅ "Obnoviť pôvodný názov" - reset custom header
- ✅ "Stĺpce" submenu - checkbox pre viditeľnosť každého stĺpca
- ✅ Custom headers sa ukladajú a načítavajú zo settings
- ✅ Fix: Obnovenie šírky stĺpca pri set_column_visible(True)

### 6. BaseGrid.create_item() - Automatické formátovanie
- ✅ int → doprava zarovnané, bez desatinných miest
- ✅ float → doprava zarovnané, 2 desatinné miesta (vrátane 0.00)
- ✅ bool → ✓ (zelená) / ✗ (červená), centrované
- ✅ string → doľava zarovnané
- ✅ Použité v MainWindow a InvoiceItemsWindow

---

## Modifikované Súbory

### apps/supplier-invoice-staging/
- `ui/main_window.py` - Enter/ESC handlers, modal window, create_item
- `ui/invoice_items_window.py` - ESC handler, focus, create_item, test data floats

### packages/shared-pyside6/shared_pyside6/ui/
- `base_grid.py` - select_initial_row, header context menu, create_item, boolean icons, column visibility fix

---

## Vytvorené Skripty (scripts/)

| # | Skript | Popis |
|---|--------|-------|
| 01 | add_enter_key_handler.py | Enter otvára položky faktúry |
| 02 | add_esc_handler_items_window.py | ESC zatvára okno položiek |
| 03 | make_items_window_modal.py | Modálne okno položiek |
| 04 | fix_items_window_position.py | Jednotná pozícia okna |
| 05 | save_settings_on_close.py | Uloženie settings pri zatvorení |
| 06 | select_first_row_on_load.py | Výber prvého riadku (hlavičky) |
| 07 | select_first_row_items_window.py | Výber prvého riadku (položky) |
| 08 | move_select_row_to_base_grid.py | Presun do BaseGrid |
| 09 | fix_select_row_timing.py | Oprava timing |
| 10 | fix_items_window_active_column.py | Ukladanie aktívneho stĺpca |
| 11 | fix_items_window_focus.py | Focus na table_view |
| 12 | add_header_context_menu.py | Context menu na header |
| 13 | fix_load_custom_headers.py | Načítanie custom headers |
| 14 | fix_column_visibility.py | Oprava šírky pri zobrazení |
| 15 | add_create_item_to_base_grid.py | Automatické formátovanie |
| 16 | fix_zero_decimal_format.py | 0 ako 0.00 |
| 17 | fix_test_data_floats.py | Test dáta 0 → 0.0 |
| 18 | add_boolean_icons.py | ✓/✗ ikony pre boolean |
| 19 | add_esc_to_main_window.py | ESC v hlavnom okne |

---

## Ďalšie Kroky (Nový Chat)

### Priority #1: Connect to Real Data
- Aplikácia pobeží na **Mágerstav serveri**
- **Lokálna PostgreSQL** databáza `invoice_staging`
- Použiť existujúci `PostgresStagingClient` z `nex-shared`
- Nahradiť `_load_test_data()` a `_load_test_items()` reálnymi queries

### Potrebné:
1. Pridať database service do supplier-invoice-staging
2. Konfigurácia pripojenia (config.yaml)
3. Query pre načítanie faktúr z `invoices_pending`
4. Query pre načítanie položiek z `invoice_items_pending`

---

## Technické Poznámky

### Settings DB lokácie
- Development: `C:\\Users\\ZelenePC\\.nex-automat\\settings.db`
- App-specific: `apps/supplier-invoice-staging/data/settings.db`

### RAG Workflow
- Claude vypíše URL, user vloží do chatu, Claude fetchne
- Funguje spoľahlivo, nemeníme

---

**Session ukončená:** {SESSION_DATE}
"""

    archive_dir = Path("docs/archive/sessions")
    archive_dir.mkdir(parents=True, exist_ok=True)

    filename = f"SESSION_{SESSION_DATE}_{SESSION_NAME}.md"
    filepath = archive_dir / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"OK: Created {filepath}")
    return filename


def update_archive_index(session_filename):
    """Update ARCHIVE_INDEX.md with new session."""
    index_path = Path("docs/archive/00_ARCHIVE_INDEX.md")

    if not index_path.exists():
        print(f"WARNING: {index_path} not found, skipping update")
        return

    content = index_path.read_text(encoding="utf-8")

    # Add new entry after the header row
    new_entry = f"| {SESSION_DATE} | {SESSION_NAME} | GUI testing, BaseGrid improvements, create_item | sessions/SESSION_{SESSION_DATE}_{SESSION_NAME}.md |"

    # Find the table and add entry
    if "| Dátum |" in content:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("| Dátum |"):
                # Insert after header and separator (i+2)
                lines.insert(i + 2, new_entry)
                break
        content = "\n".join(lines)
        index_path.write_text(content, encoding="utf-8")
        print(f"OK: Updated {index_path}")
    else:
        print(f"WARNING: Could not find table in {index_path}")


def create_init_prompt():
    """Create INIT_PROMPT_NEW_CHAT.md."""
    content = f"""# INIT PROMPT - NEX Automat Project

**Projekt:** nex-automat  
**Current Status:** supplier-invoice-staging v1.0 - CONNECT TO REAL DATA
**Developer:** Zoltán (40 rokov skúseností)  
**Jazyk:** Slovenčina  
**Previous Session:** {SESSION_NAME} ({SESSION_DATE})

---

## ⚠️ KRITICKÉ: COLLABORATION RULES

**MUSÍŠ dodržiavať pravidlá z memory_user_edits!**

Kľúčové pravidlá:
- **Rule #7:** CRITICAL artifacts pre všetky dokumenty/kód
- **Rule #8:** Step-by-step, confirmation pred pokračovaním
- **Rule #5:** Slovak language, presná terminológia projektov
- **Rule #19:** "novy chat" = 2 artifacts (new_chat.py + commit-message.txt)
- **Rule #23:** RAG Workflow - Claude vypíše URL, user vloží, Claude fetchne

---

## 🔄 DOKONČENÉ MINULÚ SESSION

### GUI Testing & Improvements
- ✅ Klávesové skratky (Enter, ESC) pre obe okná
- ✅ Modálne okno položiek faktúry
- ✅ Grid settings persistence pri zatvorení okna
- ✅ Header context menu (premenovanie stĺpcov, viditeľnosť)
- ✅ BaseGrid.create_item() - automatické formátovanie a zarovnanie
- ✅ Boolean ikony (✓/✗) s farbami
- ✅ Initial row selection a focus

---

## 🎯 IMMEDIATE NEXT STEPS

### Priority #1: Connect to Real PostgreSQL Data
- Aplikácia pobeží na **Mágerstav serveri**
- **Lokálna PostgreSQL** databáza `invoice_staging`
- Existujúci klient: `packages/nex-shared/database/postgres_staging.py`

### Úlohy:
1. Pridať database service do supplier-invoice-staging
2. Konfigurácia pripojenia (localhost, invoice_staging)
3. Nahradiť `_load_test_data()` → query z `invoices_pending`
4. Nahradiť `_load_test_items()` → query z `invoice_items_pending`

---

## 📂 KEY PATHS

```
apps/supplier-invoice-staging/          # Main app
packages/shared-pyside6/                # Shared UI components
packages/nex-shared/database/           # PostgresStagingClient
tools/rag/rag_update.py                 # RAG workflow
```

---

## 🗄️ DATABASE INFO

**Connection:**
```python
config = {{
    'host': 'localhost',
    'port': 5432,
    'database': 'invoice_staging',
    'user': 'postgres',
    'password': '<from_env_POSTGRES_PASSWORD>'
}}
```

**Tables:**
- `invoices_pending` - hlavičky faktúr
- `invoice_items_pending` - položky faktúr

---

## 🔍 RAG ACCESS

```
https://rag-api.icc.sk/search?query=...&limit=N
```

---

**Token Budget:** 190,000  
**Location:** C:\\Development\\nex-automat

---

**KONIEC INIT PROMPTU**
"""

    filepath = Path("INIT_PROMPT_NEW_CHAT.md")
    filepath.write_text(content, encoding="utf-8")
    print(f"OK: Created {filepath}")


def run_rag_update():
    """Run RAG update for new files."""
    import sys
    import os
    try:
        # Set UTF-8 encoding for subprocess
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            [sys.executable, "tools/rag/rag_update.py", "--new"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            print(f"OK: RAG update completed")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"WARNING: RAG update failed: {result.stderr}")
    except Exception as e:
        print(f"WARNING: Could not run RAG update: {e}")


def main():
    print("=== Creating New Chat Artifacts ===\n")

    session_filename = create_session_archive()
    update_archive_index(session_filename)
    create_init_prompt()
    run_rag_update()

    print("\n=== Done! ===")
    print("1. Commit changes")
    print("2. Start new chat with INIT_PROMPT_NEW_CHAT.md")


if __name__ == "__main__":
    main()