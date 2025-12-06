"""
Opraví class MainWindow(QMainWindow) → class MainWindow(BaseWindow)
"""
from pathlib import Path

MAIN_WINDOW_PATH = Path("apps/supplier-invoice-editor/src/ui/main_window.py")


def main():
    print("=" * 80)
    print("FIX: class MainWindow base class")
    print("=" * 80)

    # Načítaj súbor
    with open(MAIN_WINDOW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi class MainWindow(QMainWindow):
    for i, line in enumerate(lines):
        if 'class MainWindow(QMainWindow):' in line:
            print(f"✅ Našiel na riadku {i + 1}: {line.strip()}")

            # Zmeniť QMainWindow na BaseWindow
            lines[i] = line.replace('QMainWindow', 'BaseWindow')

            print(f"   → Zmenené na: {lines[i].strip()}")
            break

    # Ulož súbor
    with open(MAIN_WINDOW_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\n✅ Súbor opravený: {MAIN_WINDOW_PATH}")

    print("\n" + "=" * 80)
    print("FINÁLNY TEST:")
    print("=" * 80)
    print("cd apps\\supplier-invoice-editor")
    print("python main.py")
    print("  → Aplikácia by sa MUSÍ spustiť")
    print("  → Maximize + zavri + spusti znova")
    print("  → MUSÍ byť maximalizované ✅")
    print("=" * 80)


if __name__ == '__main__':
    main()