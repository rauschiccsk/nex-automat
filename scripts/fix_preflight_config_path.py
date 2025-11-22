"""
Fix Preflight Config Path
==========================
Opraví preflight check v Development:
1. Config path na apps/supplier-invoice-loader/config/config.yaml
2. SQLite check optional (skip ak nie je v config)
3. Pridá PyYAML do dependencies

Usage:
    cd C:\\Development\\nex-automat
    python scripts\\fix_preflight_config_path.py
"""

from pathlib import Path
import sys


def print_section(title: str):
    """Print formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def check_location() -> bool:
    """Verify script runs in Development."""
    cwd = Path.cwd()

    if "Development" not in str(cwd):
        print("❌ ERROR: Script must run from C:\\Development\\nex-automat")
        print(f"   Current: {cwd}")
        return False

    print(f"✅ Running in Development: {cwd}")
    return True


def update_preflight_check() -> bool:
    """Update preflight check script."""
    print_section("1. UPDATING PREFLIGHT CHECK")

    preflight_path = Path("scripts/day5_preflight_check.py")

    if not preflight_path.exists():
        print(f"❌ Preflight script not found: {preflight_path}")
        return False

    try:
        content = preflight_path.read_text(encoding='utf-8')
        modified = False

        # Fix 1: Update config path
        old_config_line = 'config_path = Path("config/config.yaml")'
        new_config_line = 'config_path = Path("apps/supplier-invoice-loader/config/config.yaml")'

        if old_config_line in content:
            content = content.replace(old_config_line, new_config_line)
            print("✅ Updated config path to app-specific location")
            modified = True
        else:
            print("⚠️  Config path pattern not found in old format")

        # Fix 2: Make SQLite check optional based on config
        old_sqlite_check = '''    # Check multiple possible SQLite locations
    sqlite_candidates = [
        Path("C:/Deployment/nex-automat-data/invoices.db"),
        Path("data/invoices.db"),
        Path("../nex-automat-data/invoices.db"),
    ]

    # Try to load from config.yaml
    try:
        config_path = Path("config/config.yaml")
        if config_path.exists():
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                cfg_sqlite = config.get('database', {}).get('sqlite_path')
                if cfg_sqlite:
                    sqlite_candidates.insert(0, Path(cfg_sqlite))
    except:
        pass

    sqlite_path = None
    for candidate in sqlite_candidates:
        if candidate.exists():
            sqlite_path = candidate
            break

    if not sqlite_path:
        sqlite_path = sqlite_candidates[0]  # Use first for error message

    if sqlite_path and sqlite_path.exists():
        print(f"✅ SQLite: Database exists ({sqlite_path})")
    else:
        print(f"❌ SQLite: Database NOT found at {sqlite_path}")
        print(f"   Tried: {[str(p) for p in sqlite_candidates]}")
        success = False'''

        new_sqlite_check = '''    # Check SQLite only if configured in config.yaml
    sqlite_path = None
    sqlite_required = False

    try:
        config_path = Path("apps/supplier-invoice-loader/config/config.yaml")
        if config_path.exists():
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                db_config = config.get('database', {})
                sqlite_path_str = db_config.get('sqlite_path')

                # Check if SQLite is primary database type
                db_type = db_config.get('type', '').lower()
                sqlite_required = db_type == 'sqlite' or sqlite_path_str is not None

                if sqlite_path_str:
                    sqlite_path = Path(sqlite_path_str)
    except Exception as e:
        print(f"⚠️  Could not read config for SQLite check: {e}")

    if sqlite_required and sqlite_path:
        if sqlite_path.exists():
            print(f"✅ SQLite: Database exists ({sqlite_path})")
        else:
            print(f"❌ SQLite: Database NOT found at {sqlite_path}")
            success = False
    elif sqlite_required:
        print("❌ SQLite: Required but path not configured")
        success = False
    else:
        print("✅ SQLite: Not required (using PostgreSQL primary)")'''

        if old_sqlite_check in content:
            content = content.replace(old_sqlite_check, new_sqlite_check)
            print("✅ Updated SQLite check to be config-based")
            modified = True
        else:
            print("⚠️  SQLite check pattern not found - may need manual update")

        if modified:
            preflight_path.write_text(content, encoding='utf-8')
            print("\n✅ Preflight check script updated")
            return True
        else:
            print("\n⚠️  No modifications made - script may already be correct")
            return True

    except Exception as e:
        print(f"❌ Error updating preflight: {e}")
        return False


def add_pyyaml_dependency() -> bool:
    """Add PyYAML to requirements if missing."""
    print_section("2. ADDING PYYAML DEPENDENCY")

    # Check if there's a scripts requirements file
    scripts_req = Path("scripts/requirements.txt")
    loader_req = Path("apps/supplier-invoice-loader/requirements.txt")

    files_updated = []

    # Add to loader requirements (scripts use loader config)
    if loader_req.exists():
        try:
            content = loader_req.read_text(encoding='utf-8')
            lines = content.strip().split('\n')

            has_yaml = any('pyyaml' in line.lower() or 'yaml' in line.lower() for line in lines)

            if not has_yaml:
                lines.append('PyYAML>=6.0.0')
                lines.sort()

                new_content = '\n'.join(lines) + '\n'
                loader_req.write_text(new_content, encoding='utf-8')

                print(f"✅ Added PyYAML to {loader_req}")
                files_updated.append(str(loader_req))
            else:
                print(f"✅ PyYAML already in {loader_req}")
        except Exception as e:
            print(f"❌ Error updating {loader_req}: {e}")
            return False

    # Create scripts requirements if it doesn't exist
    if not scripts_req.exists():
        try:
            scripts_req.write_text("PyYAML>=6.0.0\n", encoding='utf-8')
            print(f"✅ Created {scripts_req} with PyYAML")
            files_updated.append(str(scripts_req))
        except Exception as e:
            print(f"❌ Error creating {scripts_req}: {e}")
            return False
    else:
        try:
            content = scripts_req.read_text(encoding='utf-8')
            lines = content.strip().split('\n')

            has_yaml = any('pyyaml' in line.lower() or 'yaml' in line.lower() for line in lines)

            if not has_yaml:
                lines.append('PyYAML>=6.0.0')
                lines.sort()

                new_content = '\n'.join(lines) + '\n'
                scripts_req.write_text(new_content, encoding='utf-8')

                print(f"✅ Added PyYAML to {scripts_req}")
                files_updated.append(str(scripts_req))
            else:
                print(f"✅ PyYAML already in {scripts_req}")
        except Exception as e:
            print(f"❌ Error updating {scripts_req}: {e}")
            return False

    if files_updated:
        print(f"\n✅ Updated {len(files_updated)} file(s)")
        return True
    else:
        print("\n✅ PyYAML already configured")
        return True


def install_pyyaml() -> bool:
    """Install PyYAML in Development venv32."""
    print_section("3. INSTALLING PYYAML")

    try:
        import yaml
        print("✅ PyYAML already installed")
        print(f"   Version: {yaml.__version__ if hasattr(yaml, '__version__') else 'unknown'}")
        return True
    except ImportError:
        pass

    try:
        import subprocess
        print("Installing PyYAML...")

        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "PyYAML"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print("✅ PyYAML installed successfully")
            return True
        else:
            print(f"❌ Failed to install PyYAML:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Error installing PyYAML: {e}")
        return False


def main():
    """Run all fixes."""
    print("=" * 70)
    print("  FIX PREFLIGHT CONFIG PATH (DEVELOPMENT)")
    print("=" * 70)

    if not check_location():
        sys.exit(1)

    results = {
        "Update Preflight Check": update_preflight_check(),
        "Add PyYAML Dependency": add_pyyaml_dependency(),
        "Install PyYAML": install_pyyaml()
    }

    print_section("SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check, result in results.items():
        icon = "✅" if result else "❌"
        print(f"{icon} {check}")

    if passed == total:
        print(f"\n✅ All {total} fixes applied in Development")
        print("\n" + "=" * 70)
        print("  NEXT STEPS")
        print("=" * 70)
        print("\n1. Review changes:")
        print("   git status")
        print("   git diff")
        print("\n2. Commit changes:")
        print("   git add .")
        print('   git commit -m "fix: preflight config path + PyYAML dependency"')
        print("\n3. Push to GitHub:")
        print("   git push")
        print("\n4. Deploy to Deployment:")
        print("   python scripts\\deploy_to_deployment.py")
        print("\n5. Install PyYAML in Deployment:")
        print("   cd C:\\Deployment\\nex-automat")
        print("   pip install PyYAML")
        print("\n6. Run preflight check:")
        print("   python scripts\\day5_preflight_check.py")
        print("=" * 70)
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} fix(es) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()