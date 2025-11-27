"""
Diagnose Site-Packages
Zisti prečo nex-shared nie je v Python path
"""

from pathlib import Path
import sys


def check_site_packages():
    """Skontroluj site-packages"""

    print("=" * 60)
    print("CHECKING SITE-PACKAGES")
    print("=" * 60)
    print()

    site_packages = Path("C:/Development/nex-automat/venv32/Lib/site-packages")

    # Find .pth files
    print("Looking for .pth files...")
    pth_files = list(site_packages.glob("*.pth"))

    if not pth_files:
        print("❌ No .pth files found!")
    else:
        for pth_file in pth_files:
            print(f"\n📄 {pth_file.name}")
            content = pth_file.read_text(encoding='utf-8')
            print(content)
            print("-" * 60)

    # Find .egg-link files
    print("\nLooking for .egg-link files...")
    egg_files = list(site_packages.glob("*.egg-link"))

    if not egg_files:
        print("No .egg-link files found")
    else:
        for egg_file in egg_files:
            print(f"\n📄 {egg_file.name}")
            content = egg_file.read_text(encoding='utf-8')
            print(content)
            print("-" * 60)

    # Find nex-shared related files
    print("\nLooking for nex-shared related files...")
    nex_files = []
    for pattern in ["*nex*", "*NEX*"]:
        nex_files.extend(site_packages.glob(pattern))

    if not nex_files:
        print("❌ No nex-shared files found!")
    else:
        for file in nex_files:
            print(f"  {file.name} ({'DIR' if file.is_dir() else 'FILE'})")


def compare_with_invoice_shared():
    """Porovnaj s invoice-shared ktorý funguje"""

    print("\n" + "=" * 60)
    print("COMPARING WITH INVOICE-SHARED")
    print("=" * 60)
    print()

    site_packages = Path("C:/Development/nex-automat/venv32/Lib/site-packages")

    # Check invoice-shared
    print("Invoice-shared setup:")
    invoice_pth = site_packages / "__editable___invoice_shared-0.1.0.pth"
    if invoice_pth.exists():
        print(f"✅ {invoice_pth.name}")
        print(invoice_pth.read_text(encoding='utf-8'))
    else:
        print("❌ No .pth file for invoice-shared")

    print("\n" + "-" * 60 + "\n")

    # Check nex-shared
    print("Nex-shared setup:")
    nex_pth = site_packages / "__editable___nex_shared-0.1.0.pth"
    if nex_pth.exists():
        print(f"✅ {nex_pth.name}")
        print(nex_pth.read_text(encoding='utf-8'))
    else:
        print("❌ No .pth file for nex-shared")

    # Alternative naming
    nex_pth_alt = site_packages / "__editable__.nex_shared-0.1.0.pth"
    if nex_pth_alt.exists():
        print(f"✅ {nex_pth_alt.name} (alternative)")
        print(nex_pth_alt.read_text(encoding='utf-8'))


def check_package_directories():
    """Skontroluj existenciu balíkov"""

    print("\n" + "=" * 60)
    print("CHECKING PACKAGE DIRECTORIES")
    print("=" * 60)
    print()

    packages_base = Path("C:/Development/nex-automat/packages")

    for package_name in ["invoice-shared", "nex-shared"]:
        package_path = packages_base / package_name
        print(f"\n{package_name}:")
        print(f"  Path: {package_path}")
        print(f"  Exists: {package_path.exists()}")

        if package_path.exists():
            # Check for Python package
            python_package = package_path / package_name.replace("-", "_")
            print(f"  Python package: {python_package}")
            print(f"  Exists: {python_package.exists()}")

            if python_package.exists():
                init_file = python_package / "__init__.py"
                print(f"  __init__.py: {init_file.exists()}")


def show_sys_path():
    """Zobraz sys.path"""

    print("\n" + "=" * 60)
    print("CURRENT SYS.PATH")
    print("=" * 60)
    print()

    for i, path in enumerate(sys.path, 1):
        marker = "✅" if "nex" in path.lower() else "  "
        print(f"{marker} {i:2}. {path}")


def main():
    """Main execution"""

    check_site_packages()
    compare_with_invoice_shared()
    check_package_directories()
    show_sys_path()

    print("\n" + "=" * 60)
    print("DIAGNOSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()