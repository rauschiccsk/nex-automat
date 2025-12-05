"""
Pridá debug output do save_window_settings() funkcie
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("PRIDÁVANIE DEBUG OUTPUT")
    print("=" * 80)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi cursor.execute riadok
    execute_line = None
    for i, line in enumerate(lines):
        if 'cursor.execute("""' in line and 'INSERT OR REPLACE' in lines[i + 1] if i + 1 < len(lines) else False:
            execute_line = i
            break

    if execute_line is None:
        print("❌ cursor.execute() nenájdené")
        return

    print(f"✅ cursor.execute() nájdené na riadku {execute_line + 1}")

    # Nájdi commit riadok
    commit_line = None
    for i in range(execute_line, min(execute_line + 15, len(lines))):
        if 'conn.commit()' in lines[i]:
            commit_line = i
            break

    if commit_line:
        print(f"✅ conn.commit() nájdené na riadku {commit_line + 1}")

    # Pridaj debug pred cursor.execute
    indent = "        "  # 8 medzier
    debug_lines = [
        f"{indent}# DEBUG: Log parameters before save\n",
        f"{indent}logger = logging.getLogger(__name__)\n",
        f"{indent}logger.info(f\"DEBUG save_window_settings: window_name={{window_name}}, \"\n",
        f"{indent}            f\"x={{x}}, y={{y}}, width={{width}}, height={{height}}, \"\n",
        f"{indent}            f\"window_state={{window_state}}, user_id={{user_id}}\")\n",
        f"\n"
    ]

    # Vložíme debug pred cursor.execute
    new_lines = lines[:execute_line] + debug_lines + lines[execute_line:]

    # Pridaj debug po commit
    if commit_line:
        commit_line_adjusted = commit_line + len(debug_lines)
        debug_after_commit = [
            f"{indent}logger.info(f\"DEBUG: Database committed successfully\")\n"
        ]
        new_lines = new_lines[:commit_line_adjusted + 1] + debug_after_commit + new_lines[commit_line_adjusted + 1:]

    # Ulož súbor
    with open(WINDOW_SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✅ Debug output pridaný do: {WINDOW_SETTINGS_PATH}")
    print("\nPridané:")
    print("  1. Log parametrov pred cursor.execute()")
    print("  2. Log po commit()")

    # Skontroluj že je logging import
    has_logging = False
    for line in new_lines[:50]:  # Kontroluj prvých 50 riadkov
        if 'import logging' in line:
            has_logging = True
            break

    if not has_logging:
        print("\n⚠️  POZOR: Možno chýba 'import logging' na začiatku súboru")
        print("   Skontroluj imports manuálne")
    else:
        print("\n✅ import logging je prítomný")

    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("1. Spusti aplikáciu: cd apps\\supplier-invoice-editor && python main.py")
    print("2. Maximalizuj okno")
    print("3. Zavri aplikáciu")
    print("4. Skontroluj log súbor pre DEBUG výpisy")
    print("=" * 80)


if __name__ == '__main__':
    main()