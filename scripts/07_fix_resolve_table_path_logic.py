#!/usr/bin/env python3
"""
Fix _resolve_table_path logic to handle dynamic tables correctly
"""

from pathlib import Path

TARGET_FILE = Path("packages/nexdata/nexdata/btrieve/btrieve_client.py")

NEW_RESOLVE_METHOD = '''    def _resolve_table_path(self, table_name_or_path: str) -> str:
        """
        Resolve table name to filesystem path using config

        Args:
            table_name_or_path: Either table name (e.g. 'gscat', 'tsh-001') or direct path

        Returns:
            Filesystem path to .BTR file
        """
        # Check if config has table mapping
        if self.config and 'nex_genesis' in self.config:
            tables = self.config.get('nex_genesis', {}).get('tables', {})

            # First try direct lookup
            if table_name_or_path in tables:
                return tables[table_name_or_path]

            # Try dynamic table lookup (e.g., 'tsh-001' -> 'tsh')
            if '-' in table_name_or_path:
                parts = table_name_or_path.split('-')
                if len(parts) == 2:
                    base_name = parts[0]  # 'tsh' from 'tsh-001'
                    book_id = parts[1]     # '001' from 'tsh-001'

                    if base_name in tables:
                        path_template = tables[base_name]
                        # Replace {book_id} placeholder
                        return path_template.replace('{book_id}', book_id)

        # It's already a path, or no config - use as-is
        return table_name_or_path
'''


def fix_resolve_logic():
    """Fix _resolve_table_path logic"""

    print("=" * 70)
    print("Fix _resolve_table_path Logic")
    print("=" * 70)
    print()

    if not TARGET_FILE.exists():
        print(f"❌ File not found: {TARGET_FILE}")
        return False

    content = TARGET_FILE.read_text(encoding='utf-8')
    lines = content.split('\n')

    print(f"📄 File has {len(lines)} lines")
    print()

    # Find _resolve_table_path method
    method_start = -1
    method_end = -1

    for i, line in enumerate(lines):
        if 'def _resolve_table_path(self' in line:
            method_start = i
            print(f"✓ Found _resolve_table_path at line {i + 1}")

            # Find method end (next def at same indent level)
            indent = len(line) - len(line.lstrip())
            for j in range(i + 1, len(lines)):
                if lines[j].strip() and not lines[j].startswith(' ' * (indent + 4)):
                    method_end = j
                    print(f"✓ Method ends at line {j}")
                    break
            break

    if method_start == -1 or method_end == -1:
        print("❌ Could not find method")
        return False

    # Replace old method with new one
    print()
    print("🔧 Replacing method...")

    # Remove old method
    del lines[method_start:method_end]

    # Insert new method
    new_lines = NEW_RESOLVE_METHOD.split('\n')
    for idx, new_line in enumerate(new_lines):
        lines.insert(method_start + idx, new_line)

    print(f"  ✓ Removed old method ({method_end - method_start} lines)")
    print(f"  ✓ Inserted new method ({len(new_lines)} lines)")

    # Write back
    content = '\n'.join(lines)
    TARGET_FILE.write_text(content, encoding='utf-8')

    print()
    print(f"✅ Updated: {TARGET_FILE}")
    print()
    print("New logic:")
    print("  • Direct lookup: 'gscat' → config['tables']['gscat']")
    print("  • Dynamic lookup: 'tsh-001' → config['tables']['tsh'] with {book_id}='001'")
    print("  • Fallback: return as-is if not in config")
    print()
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = fix_resolve_logic()

    if success:
        print("✅ Logic fixed!")
        print()
        print("Next: Test again")
        print("  python scripts/04_test_config_lookup.py")
    else:
        print("❌ Fix failed!")

    print("=" * 70)