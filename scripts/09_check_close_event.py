"""
Skontroluje closeEvent() implementáciu v main_window.py
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("CHECK: closeEvent() v main_window.py")
    print("=" * 80)

    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi closeEvent
    close_start = None
    for i, line in enumerate(lines):
        if 'def closeEvent(' in line:
            close_start = i
            break

    if close_start is None:
        print("❌ closeEvent() nenájdená")
        return

    print(f"✅ closeEvent() nájdená na riadku {close_start + 1}")

    # Zobraz celú funkciu (až po ďalšiu def alebo koniec)
    close_end = None
    for i in range(close_start + 1, len(lines)):
        if lines[i].strip() and not lines[i].startswith(' ') and lines[i].startswith('def '):
            close_end = i
            break
        if i == len(lines) - 1:
            close_end = i + 1

    print(f"✅ closeEvent() končí na riadku {close_end}")

    print("\n" + "=" * 80)
    print("CLOSEVENT() IMPLEMENTÁCIA:")
    print("=" * 80)

    for i in range(close_start, min(close_end, close_start + 50)):
        print(f"{i + 1:4d}: {lines[i]}", end='')

    # Kontroly
    print("\n" + "=" * 80)
    print("KONTROLA:")
    print("=" * 80)

    func_text = ''.join(lines[close_start:close_end])

    checks = {
        'volá save_window_settings()': 'save_window_settings(' in func_text,
        'používa isMaximized()': 'isMaximized()' in func_text,
        'používa normalGeometry()': 'normalGeometry()' in func_text,
        'window_state parameter': 'window_state=' in func_text,
        'volá event.accept()': 'event.accept()' in func_text or 'super().closeEvent(event)' in func_text
    }

    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")

    if not checks['volá save_window_settings()']:
        print("\n🔴 KRITICKÝ PROBLÉM: closeEvent() nevolá save_window_settings()!")
        print("   → Potrebné pridať volanie save_window_settings()")

    print("\n" + "=" * 80)


if __name__ == '__main__':
    main()