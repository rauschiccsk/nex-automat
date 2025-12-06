#!/usr/bin/env python3
"""
Script 06: Show WindowSettingsDB.save() method
Zobrazí implementáciu save() metódy, ktorá možno prepisuje rozmery
"""

from pathlib import Path


def show_db_save_method():
    """Zobrazí WindowSettingsDB.save() implementáciu"""

    db_file = Path("packages/nex-shared/database/window_settings_db.py")

    if not db_file.exists():
        print(f"❌ File not found: {db_file}")
        return

    content = db_file.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Nájdi save() metódu
    in_method = False
    method_lines = []
    indent_level = None

    for i, line in enumerate(lines, 1):
        if 'def save(self' in line and 'window_name' in line:
            in_method = True
            indent_level = len(line) - len(line.lstrip())
            method_lines.append(f"{i:4d}: {line}")
            continue

        if in_method:
            current_indent = len(line) - len(line.lstrip())

            # Koniec metódy
            if line.strip() and current_indent <= indent_level and 'def ' in line:
                break

            method_lines.append(f"{i:4d}: {line}")

    if method_lines:
        print("=" * 80)
        print("WindowSettingsDB.save() METHOD")
        print("=" * 80)
        for line in method_lines:
            print(line)
        print("=" * 80)

        # Analýza
        code = '\n'.join(method_lines)
        print("\n📊 ANALYSIS:")

        # Hľadaj SQL INSERT/UPDATE statement
        if "INSERT" in code or "UPDATE" in code:
            print("✓ Contains SQL INSERT/UPDATE statement")

            # Hľadaj či width/height sú v SQL
            if "width" in code.lower() and "height" in code.lower():
                print("✓ SQL statement includes width and height columns")
            else:
                print("❌ SQL statement MISSING width/height columns!")

        # Hľadaj parameter binding
        if "?" in code or ":" in code:
            print("✓ Uses parameter binding")

            # Spočítaj parametre
            param_count = code.count("?") + code.count(":width") + code.count(":height")
            print(f"  Parameters found: {param_count}")
    else:
        print("❌ Method save() not found!")


if __name__ == "__main__":
    show_db_save_method()