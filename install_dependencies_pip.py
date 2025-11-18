#!/usr/bin/env python3
"""
Inštalácia dependencies pomocou pip (kvôli 32-bit Python + Btrieve)
"""

import subprocess
import sys
from pathlib import Path

MONOREPO_ROOT = Path("C:/Development/nex-automat")


def run_command(cmd: list, cwd: Path = None):
    """Spustí príkaz a vypíše výstup"""
    print(f"\n▶️  {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=False,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Príkaz zlyhal s kódom {result.returncode}")
        return False
    return True


def main():
    print("=" * 70)
    print("📦 Inštalácia dependencies pomocou pip")
    print("=" * 70)
    print()
    print("ℹ️  Používame pip kvôli 32-bit Python (Btrieve requirement)")
    print()

    # 1. Upgrade pip
    print("📦 Aktualizujem pip...")
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"]):
        return

    # 2. Install invoice-shared (v editable mode)
    print("\n📦 Inštalujem invoice-shared...")
    if not run_command(
            [sys.executable, "-m", "pip", "install", "-e", "packages/invoice-shared"],
            cwd=MONOREPO_ROOT
    ):
        return

    # 3. Install supplier-invoice-loader (v editable mode)
    print("\n📦 Inštalujem supplier-invoice-loader...")
    if not run_command(
            [sys.executable, "-m", "pip", "install", "-e", "apps/supplier-invoice-loader"],
            cwd=MONOREPO_ROOT
    ):
        return

    # 4. Install supplier-invoice-editor (v editable mode)
    print("\n📦 Inštalujem supplier-invoice-editor...")
    if not run_command(
            [sys.executable, "-m", "pip", "install", "-e", "apps/supplier-invoice-editor"],
            cwd=MONOREPO_ROOT
    ):
        return

    # 5. Install dev dependencies
    print("\n📦 Inštalujem dev dependencies...")
    dev_deps = [
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "pytest-cov>=4.1.0",
        "black>=23.0.0",
        "ruff>=0.1.0",
    ]

    if not run_command(
            [sys.executable, "-m", "pip", "install"] + dev_deps,
            cwd=MONOREPO_ROOT
    ):
        return

    print("\n" + "=" * 70)
    print("✅ ÚSPEŠNE NAINŠTALOVANÉ!")
    print("=" * 70)
    print()
    print("📊 Nainštalované packages:")
    print("   ✅ invoice-shared (editable)")
    print("   ✅ supplier-invoice-loader (editable)")
    print("   ✅ supplier-invoice-editor (editable)")
    print("   ✅ pytest, black, ruff")
    print()
    print("🎯 Ďalší krok:")
    print("   cd apps/supplier-invoice-loader")
    print("   pytest")
    print()


if __name__ == "__main__":
    main()