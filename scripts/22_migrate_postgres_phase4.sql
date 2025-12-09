-- ============================================================================
-- NEX Automat v2.4 - Phase 4 Migration
-- NEX Genesis Product Enrichment
-- ============================================================================
-- Purpose: Add matched_by column for tracking product matching method
-- Target: Production (Mágerstav)
-- Created: 2025-12-09
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- 1. ADD MATCHED_BY COLUMN
-- ----------------------------------------------------------------------------
-- Tracks how product was matched in NEX Genesis database
-- Values: 'ean' | 'name' | 'manual' | NULL (not yet matched)
-- ----------------------------------------------------------------------------

ALTER TABLE invoice_items_pending
    ADD COLUMN IF NOT EXISTS matched_by VARCHAR(20);

COMMENT ON COLUMN invoice_items_pending.matched_by IS
    'Method used for NEX product matching: ean (barcode), name (fuzzy), manual (user selected)';

-- ----------------------------------------------------------------------------
-- 2. FIX VALIDATION_STATUS CHECK CONSTRAINT
-- ----------------------------------------------------------------------------
-- Original constraint had 'needs_review' which was never used
-- Phase 4 uses 'warning' instead
-- ----------------------------------------------------------------------------

-- Drop old constraint if exists
ALTER TABLE invoice_items_pending
    DROP CONSTRAINT IF EXISTS invoice_items_pending_validation_status_check;

-- Add updated constraint
ALTER TABLE invoice_items_pending
    ADD CONSTRAINT invoice_items_pending_validation_status_check
    CHECK (validation_status IN ('pending', 'valid', 'warning', 'error'));

COMMENT ON COLUMN invoice_items_pending.validation_status IS
    'Validation status: pending (not checked), valid (ok), warning (low confidence), error (failed)';

-- ----------------------------------------------------------------------------
-- 3. VERIFY NEX ENRICHMENT COLUMNS EXIST
-- ----------------------------------------------------------------------------
-- These columns should already exist from Phase 3 or earlier
-- This is just a safety check - script will fail if they don't exist
-- ----------------------------------------------------------------------------

DO $$
BEGIN
    -- Check nex_gs_code
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'invoice_items_pending'
        AND column_name = 'nex_gs_code'
    ) THEN
        RAISE EXCEPTION 'Column nex_gs_code does not exist! Database schema may be outdated.';
    END IF;

    -- Check nex_name
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'invoice_items_pending'
        AND column_name = 'nex_name'
    ) THEN
        RAISE EXCEPTION 'Column nex_name does not exist! Database schema may be outdated.';
    END IF;

    -- Check in_nex
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'invoice_items_pending'
        AND column_name = 'in_nex'
    ) THEN
        RAISE EXCEPTION 'Column in_nex does not exist! Database schema may be outdated.';
    END IF;

    RAISE NOTICE 'All required NEX enrichment columns verified OK';
END $$;

-- ----------------------------------------------------------------------------
-- 4. CREATE INDEX FOR MATCHED_BY QUERIES
-- ----------------------------------------------------------------------------
-- Useful for querying items by matching method
-- ----------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_invoice_items_pending_matched_by
    ON invoice_items_pending(matched_by)
    WHERE matched_by IS NOT NULL;

-- ----------------------------------------------------------------------------
-- 5. MIGRATION COMPLETE
-- ----------------------------------------------------------------------------

COMMIT;

-- Verify results
SELECT
    column_name,
    data_type,
    character_maximum_length,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'invoice_items_pending'
    AND column_name IN ('matched_by', 'nex_gs_code', 'nex_name', 'in_nex', 'validation_status')
ORDER BY column_name;

-- Display success message
DO $$
BEGIN
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Phase 4 Migration COMPLETE';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Added: matched_by column';
    RAISE NOTICE 'Fixed: validation_status constraint';
    RAISE NOTICE 'Verified: NEX enrichment columns exist';
    RAISE NOTICE 'Created: Index on matched_by';
    RAISE NOTICE '============================================================';
END $$;