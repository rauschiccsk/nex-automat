"""
Pridá import logging ak chýba v window_settings.py
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("KONTROLA A FIX IMPORT LOGGING")
    print("=" * 80)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skontroluj či existuje import logging
    has_logging = False
    for i, line in enumerate(lines[:30]):  # Kontroluj prvých 30 riadkov
        if 'import logging' in line and not line.strip().startswith('#'):
            has_logging = True
            print(f"✅ 'import logging' už existuje na riadku {i + 1}")
            break

    if not has_logging:
        print("❌ 'import logging' chýba - pridávam...")

        # Nájdi kde sú ostatné importy
        import_section_end = 0
        for i, line in enumerate(lines[:30]):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                import_section_end = i + 1

        if import_section_end == 0:
            # Ak nie sú žiadne importy, pridaj na začiatok po docstring/comments
            for i, line in enumerate(lines[:10]):
                if not line.strip().startswith('#') and not line.strip().startswith('"""') and line.strip():
                    import_section_end = i
                    break

        # Pridaj import logging
        lines.insert(import_section_end, 'import logging\n')

        # Ulož súbor
        with open(WINDOW_SETTINGS_PATH, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f"✅ 'import logging' pridané na riadok {import_section_end + 1}")

    print("\n" + "=" * 80)
    print("READY FOR TESTING")
    print("=" * 80)
    print("Teraz môžeš spustiť aplikáciu a testovať:")
    print("1. cd apps\\supplier-invoice-editor")
    print("2. python main.py")
    print("3. Maximalizuj okno")
    print("4. Zavri aplikáciu")
    print("5. Skontroluj log pre DEBUG výpisy")
    print("=" * 80)


if __name__ == '__main__':
    main()