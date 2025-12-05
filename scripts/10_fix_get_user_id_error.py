"""
FIX: get_user_id() error v save_window_settings()
"""
from pathlib import Path

WINDOW_SETTINGS_PATH = Path("apps/supplier-invoice-editor/src/utils/window_settings.py")


def main():
    print("=" * 80)
    print("FIX: get_user_id() error")
    print("=" * 80)

    # Načítaj súbor
    with open(WINDOW_SETTINGS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nájdi či existuje get_user_id() funkcia
    if 'def get_user_id(' in content:
        print("✅ Funkcia get_user_id() existuje v module")
    else:
        print("❌ Funkcia get_user_id() neexistuje - musíme použiť default hodnotu")

    # Nahraď "user_id = get_user_id()" za "user_id = 'Server'"
    # Toto je fix pre save_window_settings() funkciu

    old_code = """        if user_id is None:
            user_id = get_user_id()"""

    new_code = """        if user_id is None:
            user_id = 'Server'  # Default user ID"""

    if old_code in content:
        content = content.replace(old_code, new_code)
        print("✅ Nahradené: get_user_id() → 'Server'")
    else:
        print("⚠️  Starý kód nenájdený, hľadám alternatívu...")

        # Alternatívne hľadanie
        if 'get_user_id()' in content:
            content = content.replace('get_user_id()', "'Server'")
            print("✅ Nahradené všetky get_user_id() → 'Server'")

    # Ulož súbor
    with open(WINDOW_SETTINGS_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Súbor opravený: {WINDOW_SETTINGS_PATH}")

    print("\n" + "=" * 80)
    print("TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → zavri aplikáciu")
    print("  → python ..\\..\\scripts\\06_verify_db_immediately.py")
    print("     MUSÍ byť záznam v DB bez ERROR")
    print("=" * 80)


if __name__ == '__main__':
    main()