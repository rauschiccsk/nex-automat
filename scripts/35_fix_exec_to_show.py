#!/usr/bin/env python3
"""
Script 35: Fix exec_() to show() in main_window.py
Zmení modálny exec_() na show() pre QMainWindow
"""

from pathlib import Path


def fix_exec_call():
    """Zmení exec_() na show() v main_window.py"""

    main_window_path = Path("apps/supplier-invoice-editor/src/ui/main_window.py")

    if not main_window_path.exists():
        print(f"❌ File not found: {main_window_path}")
        return False

    content = main_window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("SEARCHING FOR exec_() CALL")
    print("=" * 80)

    # Nájdi exec_() volanie
    for i, line in enumerate(lines, 1):
        if 'detail_window.exec_()' in line:
            print(f"\nFound at line {i}:")
            # Zobraz okolie
            for j in range(max(0, i - 10), min(len(lines), i + 5)):
                marker = ">>>" if j == i - 1 else "   "
                print(f"{marker} {j + 1:4d}: {lines[j]}")

    # Zmeniť exec_() na show()
    old_code = "detail_window.exec_()"
    new_code = "detail_window.show()"

    if old_code in content:
        content = content.replace(old_code, new_code)

        main_window_path.write_text(content, encoding='utf-8')

        print("\n✅ Changed exec_() to show()")
        print("\n📝 EXPLANATION:")
        print("  - QDialog.exec_() = modal (blocks until closed)")
        print("  - QMainWindow.show() = non-modal (doesn't block)")
        print("  - Detail window will now open as separate window")

        return True
    else:
        print("❌ exec_() not found")
        return False


if __name__ == "__main__":
    success = fix_exec_call()
    if success:
        print("\n" + "=" * 80)
        print("TEST AGAIN")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")