"""
CLI pre spustenie transform + load.
Použitie: python run_load.py --category PAB [--data-dir data] [--dry-run]
Beží na Ubuntu CC (normálny Python).
"""

import argparse
import os
import sys

from nex_config.database import NEX_MIGRATION_DB_PORT


DB_CONFIG = {
    "host": os.environ.get("PG_HOST", "localhost"),
    "port": int(os.environ.get("PG_PORT", str(NEX_MIGRATION_DB_PORT))),
    "database": os.environ.get("PG_DATABASE", "andros"),
    "user": os.environ.get("PG_USER", "andros"),
    "password": os.environ.get("PG_PASSWORD", ""),
}


def main():
    parser = argparse.ArgumentParser(
        description="NEX Migration — Transform + Load to PostgreSQL"
    )
    parser.add_argument(
        "--category", required=True, help="Migration category code (PAB, GSC...)"
    )
    parser.add_argument(
        "--data-dir", default="data", help="Directory with extracted JSON files"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Transform only, no DB write"
    )
    args = parser.parse_args()

    category = args.category.upper()

    if category == "PAB":
        from transform.pab_transformer import PABTransformer
        from load.pab_loader import PABLoader

        transformer = PABTransformer(data_dir=args.data_dir)
    else:
        print(f"ERROR: No transformer/loader implemented for category: {category}")
        sys.exit(1)

    records, transform_stats = transformer.run()

    if not records:
        print("No valid records to load. Exiting.")
        sys.exit(1)

    if args.dry_run:
        print(f"DRY RUN: {len(records)} records would be loaded. Exiting.")
        sys.exit(0)

    if category == "PAB":
        loader = PABLoader(db_config=DB_CONFIG)

    load_stats = loader.run(records)
    sys.exit(1 if load_stats["errors"] > 0 else 0)


if __name__ == "__main__":
    main()
