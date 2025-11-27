"""
Update dependencies: Add nex-shared, remove invoice-shared
"""

from pathlib import Path

# Apps to update
APPS = [
    "apps/supplier-invoice-loader",
    "apps/supplier-invoice-editor"
]

def update_dependencies(pyproject_path: Path) -> bool:
    """Update dependencies in pyproject.toml"""

    print(f"\n📄 {pyproject_path.parent.name}/pyproject.toml")
    print("-" * 60)

    if not pyproject_path.exists():
        print(f"❌ File not found: {pyproject_path}")
        return False

    # Read file
    with open(pyproject_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Track changes
    changed = False
    new_lines = []
    in_dependencies = False
    nex_shared_exists = False

    for line in lines:
        # Check if we're in dependencies section
        if line.strip() == "dependencies = [":
            in_dependencies = True
            new_lines.append(line)
            continue

        # End of dependencies
        if in_dependencies and line.strip() == "]":
            # Add nex-shared if not exists
            if not nex_shared_exists:
                new_lines.append('    "nex-shared",\n')
                print("➕ Added: nex-shared")
                changed = True
            in_dependencies = False
            new_lines.append(line)
            continue

        # Process dependency lines
        if in_dependencies:
            # Skip invoice-shared
            if '"invoice-shared"' in line:
                print("🗑️  Removed: invoice-shared")
                changed = True
                continue

            # Check for nex-shared
            if '"nex-shared"' in line:
                nex_shared_exists = True
                print("✅ Already present: nex-shared")

        new_lines.append(line)

    if not changed:
        print("✅ No changes needed")
        return True

    # Write back
    with open(pyproject_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("✅ File updated")

    # Show dependencies
    print("\n📋 Updated dependencies section:")
    in_deps = False
    for line in new_lines:
        if line.strip() == "dependencies = [":
            in_deps = True
        if in_deps:
            print(f"   {line.rstrip()}")
        if in_deps and line.strip() == "]":
            break

    return True

def main():
    print("=" * 60)
    print("UPDATE DEPENDENCIES: Add nex-shared")
    print("=" * 60)

    success_count = 0
    error_count = 0

    for app_path in APPS:
        pyproject_path = Path(app_path) / "pyproject.toml"

        if update_dependencies(pyproject_path):
            success_count += 1
        else:
            error_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Failed:  {error_count}")
    print(f"  📊 Total:   {len(APPS)}")
    print("=" * 60)

    if success_count > 0:
        print("\n📝 Next step:")
        print("   pip install -e apps/supplier-invoice-loader")
        print("   pip install -e apps/supplier-invoice-editor")

    return error_count == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)