r"""
CLI pre spustenie extrakcie.
Použitie: python run_extract.py --category PAB [--data-dir data] [--data-root C:\NEX]
MUSÍ bežať v venv32 na Windows!
"""

import argparse
import os
import sys


def setup_btrieve_dll_dir():
    """
    Make Btrieve runtime DLL findable by ctypes on Windows.

    Python 3.8+ tightened DLL search rules — bare WinDLL("w3btrv7.dll") fails
    even when the DLL exists in PATH unless we explicitly register the
    directory via os.add_dll_directory() (or pass an absolute path).

    Search order:
      1. BTRIEVE_DLL_DIR env var (operator override)
      2. C:\PVSW\bin (Pervasive PSQL 9 default)
      3. C:\Program Files (x86)\Actian\Zen\bin (Actian Zen 32-bit on 64-bit OS)
      4. C:\Program Files\Pervasive Software\PSQL\bin (older Pervasive layout)
    """
    if os.name != "nt":
        return  # not Windows — no-op

    candidates = [
        os.environ.get("BTRIEVE_DLL_DIR"),
        r"C:\PVSW\bin",
        r"C:\Program Files (x86)\Actian\Zen\bin",
        r"C:\Program Files\Pervasive Software\PSQL\bin",
    ]
    for path in candidates:
        if path and os.path.isdir(path):
            os.add_dll_directory(path)
            print(f"[run_extract] Btrieve DLL search dir registered: {path}")
            return
    print(
        "[run_extract] WARNING: No Btrieve DLL dir found. Set BTRIEVE_DLL_DIR "
        "env var if your install is in a non-standard location."
    )


def main():
    parser = argparse.ArgumentParser(description="NEX Migration — Extract from Btrieve")
    parser.add_argument(
        "--category", required=True, help="Migration category code (PAB, GSC...)"
    )
    parser.add_argument(
        "--data-dir", default="data", help="Output directory for JSON files"
    )
    parser.add_argument(
        "--data-root",
        default=r"C:\NEX",
        help=r"Base path to NEX Genesis data (e.g. C:\DEPTEST\NEX, C:\MAGER\NEX)",
    )
    args = parser.parse_args()

    setup_btrieve_dll_dir()

    category = args.category.upper()

    if category == "PAB":
        from extract.pab_extractor import PABExtractor

        extractor = PABExtractor(data_dir=args.data_dir, data_root=args.data_root)
    else:
        print(f"ERROR: No extractor implemented for category: {category}")
        sys.exit(1)

    stats = extractor.run()
    failed = sum(1 for c in stats.values() if c < 0)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
