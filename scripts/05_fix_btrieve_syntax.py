#!/usr/bin/env python3
"""
Fix syntax error in btrieve_client.py
Remove misplaced _resolve_table_path and insert it correctly
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")


def fix_syntax():
    """Fix the syntax error"""

    print("=" * 70)
    print("Fix BtrieveClient Syntax Error")
    print("=" * 70)
    print()

    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return False

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    print(f"📄 File has {len(lines)} lines")
    print()

    # Step 1: Remove misplaced _resolve_table_path (lines 66-94)
    print("🔧 Removing misplaced _resolve_table_path...")

    # Find the misplaced method
    start_remove = -1
    end_remove = -1

    for i, line in enumerate(lines):
        if i == 65 and 'def _resolve_table_path' in line:
            start_remove = i
            print(f"  ✓ Found misplaced method at line {i + 1}")

        if start_remove != -1 and i > start_remove:
            # Look for next line that's not part of this method
            if line.strip() and not line.startswith(' ' * 8) and not line.startswith(' ' * 4 + 'def'):
                end_remove = i
                print(f"  ✓ Method ends before line {i + 1}")
                break

    if start_remove != -1 and end_remove != -1:
        # Remove lines from start_remove to end_remove (exclusive)
        del lines[start_remove:end_remove]
        print(f"  ✓ Removed lines {start_remove + 1}-{end_remove}")
    else:
        print("  ⚠️  Could not find misplaced method to remove")

    # Step 2: Find correct position to insert (after __init__ ends)
    print()
    print("🔧 Finding correct position...")

    # After removal, find where __init__ ends (look for self._load_dll())
    correct_position = -1

    for i, line in enumerate(lines):
        if 'self._load_dll()' in line:
            correct_position = i + 1
            print(f"  ✓ Found _load_dll() at line {i + 1}")
            print(f"  ✓ Will insert after line {correct_position}")
            break

    if correct_position == -1:
        print("  ❌ Could not find insertion point")
        return False

    # Step 3: Insert _resolve_table_path at correct position
    print()
    print("🔧 Inserting _resolve_table_path at correct position...")

    resolve_method_lines = [
        '',
        '    def _resolve_table_path(self, table_name_or_path: str) -> str:',
        '        """',
        '        Resolve table name to filesystem path using config',
        '        ',
        '        Args:',
        '            table_name_or_path: Either table name (e.g. \'gscat\') or direct path',
        '            ',
        '        Returns:',
        '            Filesystem path to .BTR file',
        '        """',
        '        # Check if config has table mapping',
        '        if self.config and \'nex_genesis\' in self.config:',
        '            tables = self.config.get(\'nex_genesis\', {}).get(\'tables\', {})',
        '            ',
        '            if table_name_or_path in tables:',
        '                # It\'s a table name - resolve from config',
        '                path_template = tables[table_name_or_path]',
        '                ',
        '                # Handle dynamic placeholders like {book_id}',
        '                if \'{book_id}\' in path_template:',
        '                    parts = table_name_or_path.split(\'-\')',
        '                    if len(parts) == 2:',
        '                        book_id = parts[1]',
        '                        return path_template.replace(\'{book_id}\', book_id)',
        '                ',
        '                return path_template',
        '        ',
        '        # It\'s already a path, or no config - use as-is',
        '        return table_name_or_path',
    ]

    for line in resolve_method_lines:
        lines.insert(correct_position, line)
        correct_position += 1

    print(f"  ✓ Inserted {len(resolve_method_lines)} lines")

    # Step 4: Write back
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print()
    print(f"✅ Fixed: {TARGET_FILE}")
    print()
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = fix_syntax()

    if success:
        print("✅ Syntax error fixed!")
        print()
        print("Next: Run test script again")
        print("  python scripts/04_test_config_lookup.py")
    else:
        print("❌ Fix failed!")

    print("=" * 70)