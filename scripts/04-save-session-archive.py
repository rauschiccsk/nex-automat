#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Save Session Archive - NEX Automat
Location: C:/Development/nex-automat/scripts/04-save-session-archive.py

Uloží session archive a aktualizuje archive index.
Tento script sa spúšťa ručne po každej významnej session.
"""

from pathlib import Path
from datetime import datetime
import re

# Konfigurácia
MONOREPO_ROOT = Path("C:/Development/nex-automat")
ARCHIVE_DIR = MONOREPO_ROOT / "docs" / "archive" / "sessions"
ARCHIVE_INDEX = MONOREPO_ROOT / "docs" / "archive" / "00_ARCHIVE_INDEX.md"

# Session archive súbor (tu vlož obsah z artifactu)
# POZOR: Tento obsah musíš skopírovať z artifactu "project_archive_session_dec15"
SESSION_ARCHIVE_CONTENT = """[VLOŽ SEM OBSAH Z ARTIFACTU project_archive_session_dec15]"""


def extract_session_info(content: str) -> dict:
    """Extrahuje základné info zo session archive"""
    info = {
        'date': None,
        'title': None,
        'duration': None,
        'tokens': None
    }

    # Extract date
    date_match = re.search(r'\*\*Dátum:\*\* (\d{4}-\d{2}-\d{2})', content)
    if date_match:
        info['date'] = date_match.group(1)

    # Extract title
    title_match = re.search(r'\*\*Session:\*\* (.+)', content)
    if title_match:
        info['title'] = title_match.group(1).strip()

    # Extract duration
    duration_match = re.search(r'\*\*Duration:\*\* (.+)', content)
    if duration_match:
        info['duration'] = duration_match.group(1).strip()

    # Extract tokens
    tokens_match = re.search(r'\*\*Tokens:\*\* (.+)', content)
    if tokens_match:
        info['tokens'] = tokens_match.group(1).strip()

    return info


def update_archive_index(session_info: dict, filename: str):
    """Aktualizuje archive index s novou session"""

    # Načítaj existujúci index
    if ARCHIVE_INDEX.exists():
        content = ARCHIVE_INDEX.read_text(encoding='utf-8')
    else:
        print("   ⚠️  Archive index neexistuje!")
        return

    # Nájdi sekciu "Dostupné Sessions:"
    sessions_marker = "**Dostupné Sessions:**"

    if sessions_marker not in content:
        print("   ⚠️  Nemôžem nájsť 'Dostupné Sessions:' sekciu!")
        return

    # Vytvor entry pre novú session
    session_entry = f"""- [{session_info['date']}: {session_info['title']}](sessions/{filename})
  - {session_info['title']}
  - Duration: {session_info['duration']}, Tokens: {session_info['tokens']}
"""

    # Vlož novú session na začiatok zoznamu (po "Dostupné Sessions:")
    lines = content.split('\n')
    new_lines = []
    inserted = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if sessions_marker in line and not inserted:
            # Pridaj novú session hneď po tomto riadku
            new_lines.append(session_entry)
            inserted = True

    # Update štatistiku
    # Nájdi riadok so "Sessions archivovaných:"
    updated_content = '\n'.join(new_lines)
    updated_content = re.sub(
        r'\*\*Sessions archivovaných:\*\* \d+',
        lambda m: f"**Sessions archivovaných:** {int(re.search(r'\d+', m.group()).group()) + 1}",
        updated_content
    )

    # Update "Aktualizované:" dátum
    today = datetime.now().strftime('%Y-%m-%d')
    updated_content = re.sub(
        r'\*\*Aktualizované:\*\* \d{4}-\d{2}-\d{2}',
        f"**Aktualizované:** {today}",
        updated_content
    )

    # Ulož aktualizovaný index
    ARCHIVE_INDEX.write_text(updated_content, encoding='utf-8')
    print(f"   ✅ Archive index aktualizovaný")


def main():
    """Hlavná funkcia scriptu"""
    print("=" * 80)
    print("📋 ULOŽENIE SESSION ARCHIVE - NEX AUTOMAT")
    print("=" * 80)
    print()
    print(f"Archive dir: {ARCHIVE_DIR}")
    print()

    # Check či existuje obsah
    if "[VLOŽ SEM OBSAH" in SESSION_ARCHIVE_CONTENT:
        print("❌ CHYBA: Musíš najprv skopírovať obsah z artifactu!")
        print()
        print("Kroky:")
        print("1. Otvor artifact 'project_archive_session_dec15'")
        print("2. Skopíruj celý obsah")
        print("3. Vlož ho do SESSION_ARCHIVE_CONTENT v tomto scripte")
        print("4. Spusti script znova")
        print()
        return

    # Extract session info
    session_info = extract_session_info(SESSION_ARCHIVE_CONTENT)

    if not session_info['date']:
        print("❌ CHYBA: Nemôžem extrahovať dátum zo session archive!")
        return

    # Vytvor filename
    # Format: session-YYYY-MM-DD-short-title.md
    short_title = "documentation-structure"  # Môžeš customizovať
    filename = f"session-{session_info['date']}-{short_title}.md"
    filepath = ARCHIVE_DIR / filename

    print("1️⃣ Ukladanie session archive...")
    print("=" * 80)

    # Vytvor adresár ak neexistuje
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    # Ulož session archive
    filepath.write_text(SESSION_ARCHIVE_CONTENT, encoding='utf-8')
    print(f"   ✅ Uložené: {filepath.relative_to(MONOREPO_ROOT)}")
    print()

    # Aktualizuj archive index
    print("2️⃣ Aktualizácia archive indexu...")
    print("=" * 80)
    update_archive_index(session_info, filename)
    print()

    # Sumár
    print("=" * 80)
    print("✅ SESSION ARCHIVE ULOŽENÝ!")
    print("=" * 80)
    print()
    print(f"📄 Súbor: {filename}")
    print(f"📂 Umiestnenie: docs/archive/sessions/")
    print()
    print("🔄 Ďalší krok:")
    print("   git add docs/archive/")
    print(f'   git commit -m "docs: Add session archive {session_info["date"]}"')
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()