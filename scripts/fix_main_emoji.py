#!/usr/bin/env python3
"""Fix emoji characters in main.py for Windows service compatibility."""

from pathlib import Path
import re


def fix_emoji(file_path: Path):
    content = file_path.read_text(encoding='utf-8')

    # Replace emoji with ASCII alternatives
    replacements = {
        '\U0001f680': '[ROCKET]',  # 🚀
        '\U0001f4e6': '[PACKAGE]',  # 📦
        '\U0001f4c1': '[FOLDER]',  # 📁
        '\U0001f4be': '[DISK]',  # 💾
        '\U0001f50d': '[SEARCH]',  # 🔍
        '\U0001f4dd': '[MEMO]',  # 📝
        '\U0001f6d1': '[STOP]',  # 🛑
        '\u2705': '[OK]',  # ✅
        '\u274c': '[FAIL]',  # ❌
        '\u26a0': '[WARN]',  # ⚠️
    }

    original = content
    for emoji, replacement in replacements.items():
        content = content.replace(emoji, replacement)

    # Also remove any remaining emoji (4-byte unicode)
    content = re.sub(r'[\U00010000-\U0010ffff]', '', content)

    if content != original:
        file_path.write_text(content, encoding='utf-8')
        print(f"Fixed: {file_path}")
        return True
    else:
        print(f"No changes: {file_path}")
        return False


if __name__ == "__main__":
    main_py = Path("apps/supplier-invoice-loader/main.py")

    if not main_py.exists():
        print(f"ERROR: {main_py} not found")
        exit(1)

    fix_emoji(main_py)
    print("Done!")