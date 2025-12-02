"""
Add LS_API_KEY environment variable to n8n-service
"""
import subprocess
import sys


def run_command(cmd):
    """Run PowerShell command"""
    result = subprocess.run(
        ["powershell", "-Command", cmd],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def add_api_key_env():
    """Add LS_API_KEY to NSSM service"""

    api_key = "magerstav-PWjoMerqzZc-EJZPuT0wN9iBzM8eK_t1Rh-HFZT4IbY"

    print("=" * 80)
    print("ADD LS_API_KEY TO n8n-service")
    print("=" * 80)

    # Check current env
    print("\n📋 Current environment variables:")
    try:
        env_str = run_command(
            "Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\n8n-service\\Parameters' | Select-Object -ExpandProperty AppEnvironmentExtra"
        )
        print(f"   {env_str}")
    except:
        print("   (none)")

    # Build new env string
    new_env = f"N8N_PORT=5678\nN8N_HOST=0.0.0.0\nLS_API_KEY={api_key}\n"

    print(f"\n✅ New environment variables:")
    print(f"   N8N_PORT=5678")
    print(f"   N8N_HOST=0.0.0.0")
    print(f"   LS_API_KEY={api_key}")

    # Confirm
    confirm = input("\nPridať LS_API_KEY do n8n-service? (yes/no): ")
    if confirm.lower() != "yes":
        print("\n❌ Cancelled")
        sys.exit(0)

    print("\n🔧 Updating NSSM environment...")

    # Stop service
    print("   Stopping service...")
    run_command("Stop-Service n8n-service")

    # Update registry
    print("   Updating registry...")
    cmd = f"""
    Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\n8n-service\\Parameters' -Name 'AppEnvironmentExtra' -Value '{new_env}'
    """
    run_command(cmd)

    # Verify
    print("   Verifying...")
    env_check = run_command(
        "Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\n8n-service\\Parameters' | Select-Object -ExpandProperty AppEnvironmentExtra"
    )

    if "LS_API_KEY" in env_check:
        print("   ✅ LS_API_KEY added successfully")
    else:
        print("   ❌ Failed to add LS_API_KEY")
        run_command("Start-Service n8n-service")
        sys.exit(1)

    # Start service
    print("   Starting service...")
    run_command("Start-Service n8n-service")

    import time
    time.sleep(5)

    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)

    print("\n📊 SUMMARY:")
    print(f"   Service: n8n-service (Running)")
    print(f"   Environment: LS_API_KEY added")
    print(f"   API Key: {api_key}")

    print("\n🌐 NEXT STEPS:")
    print("   1. Refresh n8n UI (Ctrl+Shift+R)")
    print("   2. Open workflow: n8n-SupplierInvoiceEmailLoader")
    print("   3. Check HTTP node - API key should now work")
    print("   4. Test workflow with sample email")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        add_api_key_env()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)