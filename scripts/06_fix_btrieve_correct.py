#!/usr/bin/env python3
"""
Correctly add config lookup to BtrieveClient
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")

RESOLVE_METHOD = '''
    def _resolve_table_path(self, table_name_or_path: str) -> str:
        """
        Resolve table name to filesystem path using config

        Args:
            table_name_or_path: Either table name (e.g. 'gscat') or direct path

        Returns:
            Filesystem path to .BTR file
        """
        # Check if config has table mapping
        if self.config and 'nex_genesis' in self.config:
            tables = self.config.get('nex_genesis', {}).get('tables', {})

            if table_name_or_path in tables:
                # It's a table name - resolve from config
                path_template = tables[table_name_or_path]

                # Handle dynamic placeholders like {book_id}
                if '{book_id}' in path_template:
                    parts = table_name_or_path.split('-')
                    if len(parts) == 2:
                        book_id = parts[1]
                        return path_template.replace('{book_id}', book_id)

                return path_template

        # It's already a path, or no config - use as-is
        return table_name_or_path
'''


def fix_btrieve():
    """Add config lookup correctly"""

    print("=" * 70)
    print("Fix BtrieveClient - Correct Implementation")
    print("=" * 70)
    print()

    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return False

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    print(f"📄 Original file: {len(lines)} lines")
    print()

    # Find key positions
    init_start = -1
    load_dll_line = -1
    open_file_start = -1
    filename_bytes_line = -1

    for i, line in enumerate(lines):
        if 'def __init__(self' in line and init_start == -1:
            init_start = i

        if 'self._load_dll()' in line and load_dll_line == -1:
            load_dll_line = i

        if 'def open_file(self, filename: str' in line and open_file_start == -1:
            open_file_start = i

        if 'filename_bytes = filename.encode' in line and filename_bytes_line == -1:
            filename_bytes_line = i

    print(f"✓ Found __init__ at line {init_start + 1}")
    print(f"✓ Found _load_dll() call at line {load_dll_line + 1}")
    print(f"✓ Found open_file() at line {open_file_start + 1}")
    print(f"✓ Found filename_bytes at line {filename_bytes_line + 1}")
    print()

    if -1 in [init_start, load_dll_line, open_file_start, filename_bytes_line]:
        print("❌ Could not find all required positions")
        return False

    # Step 1: Insert _resolve_table_path after _load_dll() call
    print("🔧 Step 1: Insert _resolve_table_path after __init__...")
    lines.insert(load_dll_line + 1, RESOLVE_METHOD)
    print(f"  ✓ Inserted at line {load_dll_line + 2}")

    # Adjust positions after insertion
    open_file_start += 1  # Shifted by 1 insertion
    filename_bytes_line += 1

    # Step 2: Insert filepath resolution before filename_bytes
    print()
    print("🔧 Step 2: Insert filepath resolution in open_file()...")

    resolve_lines = [
        "        # Resolve table name to filepath using config",
        "        filepath = self._resolve_table_path(filename)",
        ""
    ]

    for idx, resolve_line in enumerate(resolve_lines):
        lines.insert(filename_bytes_line + idx, resolve_line)

    print(f"  ✓ Inserted 3 lines before line {filename_bytes_line + 1}")

    # Adjust filename_bytes_line position
    filename_bytes_line += len(resolve_lines)

    # Step 3: Update filename_bytes to use filepath
    print()
    print("🔧 Step 3: Update filename_bytes to use filepath...")
    lines[filename_bytes_line] = "        filename_bytes = filepath.encode('ascii') + b'\\x00'"
    print(f"  ✓ Updated line {filename_bytes_line + 1}")

    # Write back
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print()
    print(f"✅ Updated: {TARGET_FILE}")
    print(f"📄 New file: {len(lines)} lines (added {len(lines) - len(content.split(chr(10)))} lines)")
    print()
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = fix_btrieve()

    if success:
        print("✅ BtrieveClient fixed correctly!")
        print()
        print("Changes:")
        print("  ✓ Added _resolve_table_path() method")
        print("  ✓ Updated open_file() to use config lookup")
        print()
        print("Next: Test with script")
        print("  python scripts/04_test_config_lookup.py")
    else:
        print("❌ Fix failed!")

    print("=" * 70)