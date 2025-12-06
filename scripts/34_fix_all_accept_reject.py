#!/usr/bin/env python3
"""
Script 34: Fix ALL accept/reject references
Zmení VŠETKY výskyty self.accept a self.reject na self.close
"""

from pathlib import Path


def fix_all_dialog_refs():
    """Zmení všetky accept/reject na close"""

    window_path = Path("apps/supplier-invoice-editor/src/ui/invoice_detail_window.py")

    if not window_path.exists():
        print(f"❌ File not found: {window_path}")
        return False

    content = window_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    print("=" * 80)
    print("FINDING ALL accept/reject REFERENCES")
    print("=" * 80)

    # Nájdi všetky výskyty
    accept_refs = []
    reject_refs = []

    for i, line in enumerate(lines, 1):
        if 'self.accept' in line or '.accept(' in line:
            accept_refs.append((i, line.strip()))
        if 'self.reject' in line or '.reject(' in line:
            reject_refs.append((i, line.strip()))

    print(f"\nFound {len(accept_refs)} accept references:")
    for i, line in accept_refs:
        print(f"  {i:4d}: {line}")

    print(f"\nFound {len(reject_refs)} reject references:")
    for i, line in reject_refs:
        print(f"  {i:4d}: {line}")

    # Zmeniť všetky výskyty
    content = content.replace('self.reject', 'self.close')
    content = content.replace('self.accept', 'self.close')

    # Ulož súbor
    window_path.write_text(content, encoding='utf-8')

    print("\n✅ Changed ALL accept/reject to close")

    return True


if __name__ == "__main__":
    success = fix_all_dialog_refs()
    if success:
        print("\n" + "=" * 80)
        print("TEST AGAIN")
        print("=" * 80)
        print("cd apps/supplier-invoice-editor")
        print("python main.py")