"""
Script 04: Fix config.py - Add NEX Genesis config inside Config class
Phase 4: Integration fix
"""

from pathlib import Path


def main():
    """Fix config.py to add NEX Genesis settings inside Config class"""

    # Paths
    dev_root = Path(r"C:\Development\nex-automat")
    config_py = dev_root / "apps" / "supplier-invoice-loader" / "src" / "utils" / "config.py"

    if not config_py.exists():
        print(f"❌ File not found: {config_py}")
        return False

    print(f"📝 Reading: {config_py}")
    content = config_py.read_text(encoding='utf-8')

    # Remove incorrectly added config (if exists)
    # Remove lines added by script 02
    lines = content.split('\n')
    filtered_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        # Skip incorrectly added NEX config section
        if '# NEX Genesis Integration' in line:
            # Skip this comment and next 2 lines (the config lines)
            skip_next = 2
            continue

        if skip_next > 0:
            skip_next -= 1
            continue

        filtered_lines.append(line)

    content = '\n'.join(filtered_lines)

    # Now find the Config class and add NEX Genesis settings properly
    # Look for last attribute in Config class (before any method or end of class)

    # Strategy: Find "class Config:" and then find the last attribute definition
    # Usually LOG_LEVEL or similar, then add our config there

    # Find a good insertion point - look for last config attribute before any methods
    # Common pattern: attribute: type = value

    # Let's find the line with class Config and then find good insertion point
    lines = content.split('\n')
    config_class_idx = None
    last_attr_idx = None

    for i, line in enumerate(lines):
        if 'class Config' in line:
            config_class_idx = i

        # After finding class Config, look for attribute definitions
        if config_class_idx is not None and i > config_class_idx:
            # Check if this is an attribute line (has : and =)
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('def '):
                if ': ' in stripped and '=' in stripped:
                    last_attr_idx = i

    if last_attr_idx is None:
        print("❌ Could not find insertion point in Config class")
        return False

    print(f"✅ Found insertion point after line {last_attr_idx}")

    # Insert NEX Genesis config after last attribute
    nex_config_lines = [
        '',
        '    # NEX Genesis Integration',
        "    NEX_GENESIS_ENABLED: bool = os.getenv('NEX_GENESIS_ENABLED', 'true').lower() == 'true'",
        "    NEX_DATA_PATH: str = os.getenv('NEX_DATA_PATH', 'C:/NEX/YEARACT/STORES')"
    ]

    # Insert lines
    new_lines = lines[:last_attr_idx + 1] + nex_config_lines + lines[last_attr_idx + 1:]
    content = '\n'.join(new_lines)

    # Write modified content
    print(f"💾 Writing fixed file...")
    config_py.write_text(content, encoding='utf-8')

    print("✅ SUCCESS: config.py fixed")
    print("\nAdded NEX Genesis config inside Config class:")
    print("  - NEX_GENESIS_ENABLED: bool")
    print("  - NEX_DATA_PATH: str")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)