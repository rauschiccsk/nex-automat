"""
Migrate n8n database from user profile to LocalSystem profile
"""
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd, check=True):
    """Run PowerShell command"""
    result = subprocess.run(
        ["powershell", "-Command", cmd],
        capture_output=True,
        text=True,
        check=check
    )
    return result.stdout.strip(), result.stderr.strip()


def check_admin():
    """Check if running as administrator"""
    cmd = "([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"
    stdout, _ = run_command(cmd)
    return stdout.lower() == "true"


def stop_service():
    """Stop n8n service"""
    print("\n" + "=" * 80)
    print("STEP 1: Stopping n8n-service...")
    print("=" * 80)

    stdout, stderr = run_command("Get-Service n8n-service | Select-Object -ExpandProperty Status")

    if "Running" in stdout:
        print("   Stopping service...")
        run_command("Stop-Service n8n-service -Force")
        import time
        time.sleep(3)
        print("   ✅ Service stopped")
    else:
        print("   ✅ Service already stopped")


def start_service():
    """Start n8n service"""
    print("\n" + "=" * 80)
    print("STEP 4: Starting n8n-service...")
    print("=" * 80)

    print("   Starting service...")
    run_command("Start-Service n8n-service")
    import time
    time.sleep(5)

    stdout, _ = run_command("Get-Service n8n-service | Select-Object -ExpandProperty Status")

    if "Running" in stdout:
        print("   ✅ Service started")
        return True
    else:
        print("   ❌ Failed to start service!")
        return False


def migrate_database():
    """Main migration function"""
    print("=" * 80)
    print("n8n DATABASE MIGRATION")
    print("=" * 80)

    # Check admin
    if not check_admin():
        print("\n❌ CHYBA: Script musí bežať ako Administrator!")
        print("   Otvor PowerShell as Administrator a spusti:")
        print("   python scripts/migrate_n8n_database.py")
        sys.exit(1)

    print("\n✅ Running as Administrator")

    # Paths
    source_db = Path(r"C:\Users\ZelenePC\.n8n\database.sqlite")
    target_dir = Path(r"C:\Windows\System32\config\systemprofile\.n8n")
    target_db = target_dir / "database.sqlite"
    backup_db = target_dir / f"database.sqlite.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # Validate source
    print("\n📂 SOURCE DATABASE:")
    if not source_db.exists():
        print(f"   ❌ Nenájdená: {source_db}")
        sys.exit(1)

    source_size = source_db.stat().st_size / 1024 / 1024
    print(f"   Path: {source_db}")
    print(f"   Size: {source_size:.2f} MB")
    print("   ✅ Exists")

    # Validate target directory
    print("\n📂 TARGET DIRECTORY:")
    if not target_dir.exists():
        print("   ⚠️  Directory neexistuje, vytváram...")
        target_dir.mkdir(parents=True, exist_ok=True)
    print(f"   Path: {target_dir}")
    print("   ✅ Ready")

    # Check service
    print("\n🔧 n8n SERVICE:")
    stdout, _ = run_command("Get-Service n8n-service | Select-Object -ExpandProperty Status")
    print(f"   Status: {stdout}")

    # Confirmation
    print("\n" + "=" * 80)
    print("⚠️  MIGRATION PLAN:")
    print("=" * 80)
    print("\n1. Stop n8n-service")

    if target_db.exists():
        target_size = target_db.stat().st_size / 1024 / 1024
        print(f"2. Backup current database ({target_size:.2f} MB)")
    else:
        print("2. No current database to backup")

    print(f"3. Copy source database ({source_size:.2f} MB)")
    print("4. Start n8n-service")
    print("5. Verify workflows visible")

    print("\n⚠️  WARNING: n8n bude nedostupné počas migrácie (~30 sekúnd)")

    confirm = input("\nPokračovať? (yes/no): ")
    if confirm.lower() != "yes":
        print("\n❌ Migration cancelled by user")
        sys.exit(0)

    # Step 1: Stop service
    stop_service()

    # Step 2: Backup
    print("\n" + "=" * 80)
    print("STEP 2: Backup current database...")
    print("=" * 80)

    if target_db.exists():
        print(f"   Creating backup: {backup_db.name}")
        shutil.copy2(target_db, backup_db)

        if backup_db.exists():
            backup_size = backup_db.stat().st_size / 1024
            print(f"   ✅ Backup created ({backup_size:.2f} KB)")
            print(f"   Location: {backup_db}")
        else:
            print("   ❌ Backup failed!")
            start_service()
            sys.exit(1)
    else:
        print("   ⚠️  No current database to backup")

    # Step 3: Copy database
    print("\n" + "=" * 80)
    print("STEP 3: Copying source database...")
    print("=" * 80)

    print(f"   Source: {source_db}")
    print(f"   Target: {target_db}")
    print("   Copying...")

    try:
        shutil.copy2(source_db, target_db)

        if target_db.exists():
            new_size = target_db.stat().st_size / 1024 / 1024
            print(f"   ✅ Database copied ({new_size:.2f} MB)")
        else:
            print("   ❌ Copy failed!")

            # Restore backup
            if backup_db.exists():
                print("   ⚠️  Restoring backup...")
                shutil.copy2(backup_db, target_db)

            start_service()
            sys.exit(1)
    except Exception as e:
        print(f"   ❌ Error: {e}")

        # Restore backup
        if backup_db.exists():
            print("   ⚠️  Restoring backup...")
            shutil.copy2(backup_db, target_db)

        start_service()
        sys.exit(1)

    # Step 4: Start service
    if not start_service():
        sys.exit(1)

    # Success
    print("\n" + "=" * 80)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 80)

    print("\n📊 SUMMARY:")
    print(f"   Source DB: {source_size:.2f} MB with 24 workflows")
    print(f"   Target DB: {new_size:.2f} MB")
    print(f"   Backup: {backup_db}")
    print("   Service: Running")

    print("\n🌐 NEXT STEPS:")
    print("   1. Open: http://localhost:5678")
    print("   2. Login: automation@isnex.ai")
    print("   3. Check workflows are visible (should be 24)")
    print("   4. Verify n8n-SupplierInvoiceEmailLoader exists")

    print("\n⚠️  ROLLBACK (ak nieco nefunguje):")
    print("   Stop-Service n8n-service")
    print(f"   Copy-Item '{backup_db}' '{target_db}' -Force")
    print("   Start-Service n8n-service")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        migrate_database()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)