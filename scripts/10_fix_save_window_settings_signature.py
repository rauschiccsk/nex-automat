#!/usr/bin/env python3
"""
Fix save_window_settings Signature
===================================
Session: 2025-12-05
Location: scripts/10_fix_save_window_settings_signature.py

Pridá window_state parameter do save_window_settings funkcie.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TARGET = PROJECT_ROOT / "apps/supplier-invoice-editor/src/utils/window_settings.py"


def fix_signature():
    """Opraví signatúru save_window_settings"""

    print("=" * 80)
    print("FIX SAVE_WINDOW_SETTINGS SIGNATURE")
    print("=" * 80)

    with open(TARGET, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Nájdi def save_window_settings riadok
    print("\n1. Hľadám funkciu save_window_settings()...")

    for i, line in enumerate(lines):
        if 'def save_window_settings(' in line:
            print(f"   ✅ Nájdené na riadku {i + 1}")

            # Nájdi koniec signatúry (končí na '):')
            sig_lines = [line]
            j = i + 1
            while j < len(lines):
                sig_lines.append(lines[j])
                # Kontroluj či už máme celú signatúru (obsahuje ') -> bool:')
                full_so_far = ''.join(sig_lines)
                if ') -> bool:' in full_so_far or '):' in full_so_far:
                    break
                j += 1

            current_sig = ''.join(sig_lines)
            print(f"\n   Aktuálna signatúra:")
            print(f"   {current_sig.strip()}")

            # Skontroluj či už má window_state
            if 'window_state' in current_sig:
                print("\n   ℹ️  window_state už je v signatúre")
                return True

            # Pridaj window_state pred user_id parameter
            print("\n2. Pridávam window_state parameter...")

            # Najprv zober celú signatúru do stringu
            full_sig = ''.join(sig_lines)

            print(f"   Debug - Celá signatúra:\n{full_sig}")

            # Teraz hľadaj pattern
            if 'height: int,' in full_sig:
                # Počítaj whitespace pred "user_id"
                indent = '                        '  # 24 medzier

                # Nahraď "height: int," za "height: int,\n{indent}window_state: int = 0,"
                new_sig = full_sig.replace(
                    'height: int,\n',
                    f'height: int,\n{indent}window_state: int = 0,\n'
                )

                print("   ✅ Parameter pridaný")

                # Ulož celý súbor s novou signatúrou
                print("\n3. Ukladám...")

                # Zostaň všetko pred funkciou + nová signatúra + všetko za funkciou
                before = ''.join(lines[:i])
                after = ''.join(lines[j + 1:])  # j je posledný riadok signatúry
                new_content = before + new_sig + after

                with open(TARGET, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print("   ✅ Uložené")

                print("\n" + "=" * 80)
                print("✅ HOTOVO - Signature Fixed")
                print("=" * 80)
                return True
            else:
                print(f"   ⚠️  Pattern 'height: int,' nenájdený")
                return False

    print("   ❌ Funkcia save_window_settings nenájdená")
    return False


if __name__ == "__main__":
    success = fix_signature()
    exit(0 if success else 1)