#!/usr/bin/env python
"""
Fix new_chat.py - INIT_PROMPT path to ROOT instead of docs/init_chat/
"""

from pathlib import Path

FILE_PATH = Path("C:/Development/nex-automat/new_chat.py")

OLD_LINE = 'INIT_CHAT_PATH = BASE_PATH / "docs" / "init_chat"'
NEW_LINE = 'INIT_CHAT_PATH = BASE_PATH  # ROOT - INIT_PROMPT_NEW_CHAT.md in project root'


def main():
    content = FILE_PATH.read_text(encoding="utf-8")

    if OLD_LINE not in content:
        print("⚠️ OLD_LINE not found - already fixed?")
        return

    new_content = content.replace(OLD_LINE, NEW_LINE)
    FILE_PATH.write_text(new_content, encoding="utf-8")

    print("✅ Fixed: INIT_CHAT_PATH now points to ROOT")
    print(f"   {NEW_LINE}")


if __name__ == "__main__":
    main()