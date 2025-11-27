#!/usr/bin/env python3
"""
Update BtrieveClient to support config-based table name resolution
Adds _resolve_table_path() helper and modifies open_file() method
"""

from pathlib import Path

# Target file
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


def update_btrieve_client():
    """Add config lookup support to BtrieveClient"""

    print(f"📂 Reading: {TARGET_FILE}")

    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return False

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    print(f"📄 File has {len(lines)} lines")

    # STEP 1: Find all positions FIRST (before any modifications)
    init_start = -1
    init_end = -1
    open_file_start = -1
    buffer_init_line = -1
    file_spec_line = -1

    for i, line in enumerate(lines):
        if 'def __init__(self' in line:
            init_start = i
            print(f"✓ Found __init__ at line {i + 1}")

        if init_start != -1 and init_end == -1 and 'self.config = config' in line:
            init_end = i
            print(f"✓ Found config assignment at line {i + 1}")

        if 'def open_file(self, filename: str' in line:
            open_file_start = i
            print(f"✓ Found open_file() at line {i + 1}")

        if open_file_start != -1 and buffer_init_line == -1:
            if 'pos_block = ctypes.create_string_buffer(128)' in line:
                buffer_init_line = i
                print(f"✓ Found buffer initialization at line {i + 1}")

        if buffer_init_line != -1 and file_spec_line == -1:
            if 'filename_bytes = filename.encode' in line:
                file_spec_line = i
                print(f"✓ Found filename_bytes at line {i + 1}")

    # Validate all positions found
    if init_start == -1 or init_end == -1:
        print("❌ Could not find __init__ method")
        return False

    if open_file_start == -1:
        print("❌ Could not find open_file method")
        return False

    if buffer_init_line == -1:
        print("❌ Could not find buffer initialization in open_file")
        return False

    if file_spec_line == -1:
        print("❌ Could not find filename_bytes line")
        return False

    print()
    print("🔧 Applying modifications...")
    print()

    # STEP 2: Apply modifications from END to START (to preserve line numbers)

    # 2a. Update filename_bytes line
    lines[file_spec_line] = "        filename_bytes = filepath.encode('ascii') + b'\\x00'"
    print(f"✓ Updated filename_bytes to use filepath at line {file_spec_line + 1}")

    # 2b. Insert filepath resolution before buffer initialization
    resolve_lines = [
        "        # Resolve table name to filepath using config",
        "        filepath = self._resolve_table_path(filename)",
        ""
    ]

    for idx, resolve_line in enumerate(resolve_lines):
        lines.insert(buffer_init_line + idx, resolve_line)

    print(f"✓ Inserted filepath resolution before line {buffer_init_line + 1}")

    # 2c. Insert _resolve_table_path after __init__
    lines.insert(init_end + 1, RESOLVE_METHOD)
    print(f"✓ Inserted _resolve_table_path() after line {init_end + 1}")

    # Write back
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print(f"✅ Updated: {TARGET_FILE}")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("BtrieveClient Config Lookup Implementation")
    print("=" * 70)
    print()

    success = update_btrieve_client()

    print()
    if success:
        print("✅ BtrieveClient updated successfully!")
        print()
        print("Changes made:")
        print("  ✓ Added _resolve_table_path() method")
        print("  ✓ Updated open_file() to resolve table names")
        print("  ✓ Supports config-based path lookup")
        print()
        print("Next: Update repositories to use table names")
    else:
        print("❌ Update failed!")

    print()
    print("=" * 70)