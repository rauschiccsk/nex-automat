"""
Migrate nex-shared to nexdata package
Complete rename and restructure
"""

import shutil
from pathlib import Path

# Paths
OLD_PACKAGE = Path("packages/nex-shared")
NEW_PACKAGE = Path("packages/nexdata")

# Items to move into nexdata/ subfolder
ITEMS_TO_MOVE = [
    "models",
    "btrieve",
    "repositories",
    "auth",
    "database",
    "monitoring",
    "utils",
    "__init__.py",
]

# Apps to update
APPS = [
    "apps/supplier-invoice-loader",
    "apps/supplier-invoice-editor"
]


def migrate_package():
    print("=" * 60)
    print("MIGRATE: nex-shared → nexdata")
    print("=" * 60)

    # Step 1: Rename package directory
    print("\n📦 STEP 1: Rename package directory")
    print("-" * 60)

    if not OLD_PACKAGE.exists():
        print(f"❌ Source not found: {OLD_PACKAGE}")
        return False

    if NEW_PACKAGE.exists():
        print(f"⚠️  Target already exists: {NEW_PACKAGE}")
        print("   Skipping rename")
    else:
        try:
            OLD_PACKAGE.rename(NEW_PACKAGE)
            print(f"✅ Renamed: nex-shared → nexdata")
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    # Step 2: Create nexdata/ subfolder
    print("\n📁 STEP 2: Create nexdata/ subfolder")
    print("-" * 60)

    nexdata_dir = NEW_PACKAGE / "nexdata"
    nexdata_dir.mkdir(exist_ok=True)
    print(f"✅ Created: {nexdata_dir}")

    # Step 3: Move items into subfolder
    print("\n📋 STEP 3: Move items into nexdata/")
    print("-" * 60)

    moved = 0
    for item_name in ITEMS_TO_MOVE:
        source = NEW_PACKAGE / item_name
        target = nexdata_dir / item_name

        if not source.exists():
            print(f"⚠️  {item_name:<20} - Not found")
            continue

        if target.exists():
            print(f"⚠️  {item_name:<20} - Already in place")
            continue

        try:
            shutil.move(str(source), str(target))
            print(f"✅ {item_name:<20} - Moved")
            moved += 1
        except Exception as e:
            print(f"❌ {item_name:<20} - Error: {e}")

    print(f"\n   Total moved: {moved}/{len(ITEMS_TO_MOVE)}")

    # Step 4: Update pyproject.toml
    print("\n📄 STEP 4: Update pyproject.toml")
    print("-" * 60)

    pyproject = NEW_PACKAGE / "pyproject.toml"

    if not pyproject.exists():
        print("❌ pyproject.toml not found")
        return False

    with open(pyproject, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace name
    content = content.replace('name = "nex-shared"', 'name = "nexdata"')

    # Replace packages
    content = content.replace('packages = ["."]', 'packages = ["nexdata"]')
    content = content.replace('packages = ["nex_shared"]', 'packages = ["nexdata"]')

    with open(pyproject, "w", encoding="utf-8") as f:
        f.write(content)

    print('✅ Updated name: "nex-shared" → "nexdata"')
    print('✅ Updated packages: ["nexdata"]')

    # Step 5: Update app dependencies
    print("\n📝 STEP 5: Update app dependencies")
    print("-" * 60)

    updated_apps = 0
    for app_path in APPS:
        app_pyproject = Path(app_path) / "pyproject.toml"

        if not app_pyproject.exists():
            print(f"⚠️  {app_path} - pyproject.toml not found")
            continue

        with open(app_pyproject, "r", encoding="utf-8") as f:
            app_content = f.read()

        if '"nex-shared"' in app_content:
            app_content = app_content.replace('"nex-shared"', '"nexdata"')

            with open(app_pyproject, "w", encoding="utf-8") as f:
                f.write(app_content)

            print(f"✅ {Path(app_path).name:<30} - Updated")
            updated_apps += 1
        else:
            print(f"✅ {Path(app_path).name:<30} - Already correct")

    # Summary
    print("\n" + "=" * 60)
    print("MIGRATION SUMMARY:")
    print(f"  ✅ Package renamed")
    print(f"  ✅ Items moved: {moved}")
    print(f"  ✅ pyproject.toml updated")
    print(f"  ✅ Apps updated: {updated_apps}")
    print("=" * 60)

    # Show structure
    print(f"\n📁 New structure:")
    print(f"   packages/nexdata/")
    print(f"   ├── nexdata/              ← Python module")
    print(f"   │   ├── __init__.py")
    print(f"   │   ├── models/")
    print(f"   │   ├── btrieve/")
    print(f"   │   └── repositories/")
    print(f"   ├── pyproject.toml")
    print(f"   └── README.md")

    print("\n📝 Next steps:")
    print("   1. pip install -e packages/nexdata")
    print("   2. pip install -e apps/supplier-invoice-loader")
    print("   3. pip install -e apps/supplier-invoice-editor")
    print('   4. Test: python -c "from nexdata import *"')

    return True


if __name__ == "__main__":
    success = migrate_package()
    exit(0 if success else 1)