#!/usr/bin/env python
"""
Fix Worker Settings - pridanie extra='ignore' pre Pydantic.

Problém: .env obsahuje SMTP_FROM a REPORT_CUSTOMER_EMAIL,
ale Settings trieda ich nemá definované. Pydantic v2 defaultne
zakazuje extra fieldy.

Riešenie: Pridať extra='ignore' do Config triedy.
"""

import sys
from pathlib import Path

# Určenie root projektu
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

SETTINGS_FILE = PROJECT_ROOT / "apps" / "supplier-invoice-worker" / "config" / "settings.py"


def fix_settings():
    """Pridá extra='ignore' do Settings Config triedy."""
    if not SETTINGS_FILE.exists():
        print(f"[SKIP] Súbor neexistuje: {SETTINGS_FILE}")
        return False

    content = SETTINGS_FILE.read_text(encoding="utf-8")

    # Skontroluj či už je opravené
    if "extra = " in content or "extra=" in content:
        print("[SKIP] Settings už obsahuje 'extra' konfiguráciu")
        return False

    # Nahraď
    old = "case_sensitive = False"
    new = "case_sensitive = False\n        extra = 'ignore'"

    if old not in content:
        print("[ERROR] Nenašiel sa pattern 'case_sensitive = False'")
        return False

    content = content.replace(old, new)
    SETTINGS_FILE.write_text(content, encoding="utf-8")

    print(f"[OK] Opravený: {SETTINGS_FILE}")
    return True


def main():
    print("=" * 60)
    print("FIX WORKER SETTINGS")
    print("=" * 60)
    print()

    if fix_settings():
        print()
        print("✅ Hotovo. Commitni zmeny:")
        print("   git add -A")
        print("   git commit -m 'fix: worker settings extra=ignore for Pydantic v2'")
        print("   git push")
    else:
        print()
        print("⚠️ Žiadne zmeny neboli vykonané.")


if __name__ == "__main__":
    main()