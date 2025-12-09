#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script 22: PostgreSQL Migration - Phase 4 NEX Genesis Product Enrichment
Created: 2025-12-09
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import asyncpg
    import asyncio
except ImportError:
    print("[ERROR] Required package 'asyncpg' not installed")
    print("Install: pip install asyncpg")
    sys.exit(1)

# Migration SQL
MIGRATION_SQL = """
-- ============================================================================
-- NEX Automat v2.4 - Phase 4 Migration
-- NEX Genesis Product Enrichment
-- ============================================================================
BEGIN;

-- 1. ADD MATCHED_BY COLUMN
ALTER TABLE invoice_items_pending
    ADD COLUMN IF NOT EXISTS matched_by VARCHAR(20);

COMMENT ON COLUMN invoice_items_pending.matched_by IS 
    'Method used for NEX product matching: ean (barcode), name (fuzzy), manual (user selected)';

-- 2. FIX VALIDATION_STATUS CHECK CONSTRAINT
ALTER TABLE invoice_items_pending 
    DROP CONSTRAINT IF EXISTS invoice_items_pending_validation_status_check;

ALTER TABLE invoice_items_pending
    ADD CONSTRAINT invoice_items_pending_validation_status_check
    CHECK (validation_status IN ('pending', 'valid', 'warning', 'error'));

COMMENT ON COLUMN invoice_items_pending.validation_status IS 
    'Validation status: pending (not checked), valid (ok), warning (low confidence), error (failed)';

-- 3. VERIFY NEX ENRICHMENT COLUMNS EXIST
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoice_items_pending' 
        AND column_name = 'nex_gs_code'
    ) THEN
        RAISE EXCEPTION 'Column nex_gs_code does not exist! Database schema may be outdated.';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoice_items_pending' 
        AND column_name = 'nex_name'
    ) THEN
        RAISE EXCEPTION 'Column nex_name does not exist! Database schema may be outdated.';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoice_items_pending' 
        AND column_name = 'in_nex'
    ) THEN
        RAISE EXCEPTION 'Column in_nex does not exist! Database schema may be outdated.';
    END IF;

    RAISE NOTICE 'All required NEX enrichment columns verified OK';
END $$;

-- 4. CREATE INDEX FOR MATCHED_BY QUERIES
CREATE INDEX IF NOT EXISTS idx_invoice_items_pending_matched_by 
    ON invoice_items_pending(matched_by)
    WHERE matched_by IS NOT NULL;

COMMIT;
"""

VERIFY_SQL = """
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'invoice_items_pending'
    AND column_name IN ('matched_by', 'nex_gs_code', 'nex_name', 'in_nex', 'validation_status')
ORDER BY column_name;
"""


async def run_migration():
    """Run PostgreSQL migration"""
    print("=" * 70)
    print("NEX Automat v2.4 - Phase 4 Migration")
    print("=" * 70)

    # Get database credentials from environment
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = int(os.getenv('POSTGRES_PORT', '5432'))
    db_name = os.getenv('POSTGRES_DATABASE', 'invoice_staging')
    db_user = os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('POSTGRES_PASSWORD', '')

    if not db_password:
        print("[WARNING] POSTGRES_PASSWORD not set, using empty password")

    print(f"\nDatabase: {db_host}:{db_port}/{db_name}")
    print(f"User: {db_user}")
    print()

    try:
        # Connect to database
        print("[1/3] Connecting to PostgreSQL...")
        conn = await asyncpg.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        print("✅ Connected")

        # Run migration
        print("\n[2/3] Running migration...")
        print("-" * 70)
        await conn.execute(MIGRATION_SQL)
        print("-" * 70)
        print("✅ Migration executed successfully")

        # Verify schema
        print("\n[3/3] Verifying schema...")
        rows = await conn.fetch(VERIFY_SQL)

        if rows:
            print("\nColumns in invoice_items_pending:")
            print(f"{'Column':<20} {'Type':<15} {'Length':<10} {'Nullable':<10}")
            print("-" * 70)
            for row in rows:
                col_name = row['column_name']
                col_type = row['data_type']
                col_length = row['character_maximum_length'] or '-'
                col_nullable = 'YES' if row['is_nullable'] == 'YES' else 'NO'
                print(f"{col_name:<20} {col_type:<15} {str(col_length):<10} {col_nullable:<10}")

            # Check if matched_by exists
            has_matched_by = any(row['column_name'] == 'matched_by' for row in rows)
            if has_matched_by:
                print("\n✅ matched_by column successfully added")
            else:
                print("\n❌ matched_by column NOT found!")
                await conn.close()
                sys.exit(1)
        else:
            print("❌ No columns found - verification failed!")
            await conn.close()
            sys.exit(1)

        # Close connection
        await conn.close()

        # Success
        print("\n" + "=" * 70)
        print("✅ Phase 4 Migration COMPLETE")
        print("=" * 70)
        print("\nChanges:")
        print("  • Added: matched_by column")
        print("  • Fixed: validation_status constraint")
        print("  • Verified: NEX enrichment columns exist")
        print("  • Created: Index on matched_by")
        print("=" * 70)

    except asyncpg.exceptions.PostgresError as e:
        print(f"\n❌ PostgreSQL Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    try:
        asyncio.run(run_migration())
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user")
        sys.exit(1)


if __name__ == '__main__':
    main()