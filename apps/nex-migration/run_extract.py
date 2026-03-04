r"""
CLI pre spustenie extrakcie.
Použitie: python run_extract.py --category PAB [--data-dir data] [--data-root C:\NEX]
MUSÍ bežať v venv32 na Windows!
"""

import argparse
import sys


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
