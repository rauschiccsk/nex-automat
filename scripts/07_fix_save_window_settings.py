"""
FIX: Zmení INSERT OR REPLACE na DELETE + INSERT v save_window_settings()
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("FIX: save_window_settings() - DELETE + INSERT namiesto INSERT OR REPLACE")
    print("=" * 80)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi INSERT OR REPLACE block
    insert_start = None
    for i, line in enumerate(lines):
        if 'INSERT OR REPLACE INTO window_settings' in line:
            insert_start = i
            break

    if insert_start is None:
        print("❌ INSERT OR REPLACE nenájdené")
        return

    print(f"✅ INSERT OR REPLACE nájdené na riadku {insert_start + 1}")

    # Nájdi koniec INSERT statement (riadok s VALUES tuple)
    insert_end = None
    for i in range(insert_start, min(insert_start + 10, len(lines))):
        if 'VALUES (' in lines[i] and ')' in lines[i]:
            insert_end = i
            break

    if insert_end is None:
        print("❌ Koniec INSERT statement nenájdený")
        return

    print(f"✅ INSERT statement končí na riadku {insert_end + 1}")

    # Zisti indent
    indent = "        "  # 8 spaces

    # Vytvor nový kód: DELETE + INSERT
    new_code = [
        f"{indent}# First DELETE existing record to avoid INSERT OR REPLACE issues\n",
        f"{indent}cursor.execute(\"\"\"\n",
        f"{indent}    DELETE FROM window_settings\n",
        f"{indent}    WHERE user_id = ? AND window_name = ?\n",
        f"{indent}\"\"\", (user_id, window_name))\n",
        f"{indent}\n",
        f"{indent}# Then INSERT new record with all current values\n",
        f"{indent}cursor.execute(\"\"\"\n",
        f"{indent}    INSERT INTO window_settings\n",
        f"{indent}    (user_id, window_name, x, y, width, height, window_state, updated_at)\n",
        f"{indent}    VALUES (?, ?, ?, ?, ?, ?, ?, ?)\n",
        f"{indent}\"\"\", (user_id, window_name, x, y, width, height, window_state, datetime.now()))\n",
    ]

    # Nahraď starý kód novým (od cursor.execute do konca VALUES tuple)
    # Nájdeme začiatok cursor.execute
    cursor_exec_start = None
    for i in range(insert_start - 5, insert_start + 5):
        if i >= 0 and 'cursor.execute("""' in lines[i]:
            cursor_exec_start = i
            break

    if cursor_exec_start is None:
        print("❌ cursor.execute začiatok nenájdený")
        return

    print(f"✅ Nahradím riadky {cursor_exec_start + 1} až {insert_end + 1}")

    # Vytvor nové lines
    new_lines = lines[:cursor_exec_start] + new_code + lines[insert_end + 1:]

    # Ulož súbor
    with open(WINDOW_SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\n✅ Súbor upravený: {WINDOW_SETTINGS_PATH}")
    print("\nZmeny:")
    print("  ❌ Odstránené: INSERT OR REPLACE INTO...")
    print("  ✅ Pridané: DELETE WHERE user_id AND window_name")
    print("  ✅ Pridané: INSERT INTO...")

    print("\n" + "=" * 80)
    print("ĎALŠÍ KROK:")
    print("=" * 80)
    print("1. DELETE aktuálny záznam: python scripts\\05_delete_window_position.py")
    print("2. Spusti aplikáciu: cd apps\\supplier-invoice-editor && python main.py")
    print("3. Maximalizuj okno")
    print("4. Zavri aplikáciu")
    print("5. Overiť DB: python scripts\\06_verify_db_immediately.py")
    print("   → window_state MUSÍ byť = 2")
    print("=" * 80)


if __name__ == '__main__':
    main()