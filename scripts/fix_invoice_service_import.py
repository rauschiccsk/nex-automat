#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix: Oprava importu v invoice_service.py
Location: C:/Development/nex-automat/fix_invoice_service_import.py
"""

from pathlib import Path

SERVICE_PATH = Path("/src/business/invoice_service.py")


def main():
    print("=" * 70)
    print("FIX: Oprava importu PostgresClient v invoice_service.py")
    print("=" * 70)
    print()

    if not SERVICE_PATH.exists():
        print(f"❌ Súbor neexistuje: {SERVICE_PATH}")
        return

    # Načítať obsah
    content = SERVICE_PATH.read_text(encoding='utf-8')
    print(f"✅ Načítaný: {SERVICE_PATH.relative_to(Path.cwd())}")
    print()

    # Opraviť import
    old_import = "from database.postgres_client import PostgresClient"
    new_import = "from src.database.postgres_client import PostgresClient"

    if old_import in content:
        content = content.replace(old_import, new_import)
        print(f"✅ Opravený import:")
        print(f"   PRED: {old_import}")
        print(f"   PO:   {new_import}")
    else:
        print("⚠️  Starý import nenájdený, možno už opravené?")
        print()
        # Skontrolovať či je nový import už tam
        if new_import in content:
            print("✅ Správny import už existuje")
            return
        else:
            print("❌ Ani starý ani nový import nenájdený!")
            return

    # Uložiť
    SERVICE_PATH.write_text(content, encoding='utf-8')

    print()
    print("=" * 70)
    print("✅ IMPORT OPRAVENÝ")
    print("=" * 70)
    print()
    print("Teraz:")
    print("1. python diagnose_editor_db.py  (overenie)")
    print("2. python e2e_test_workflow.py   (spustiť test znova)")
    print()


if __name__ == "__main__":
    main()