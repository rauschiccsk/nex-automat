-- Pridanie stĺpca matched_by do invoice_items_pending

-- Skontrolovať či stĺpec už existuje
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'invoice_items_pending'
        AND column_name = 'matched_by'
    ) THEN
        -- Pridať stĺpec matched_by
        ALTER TABLE invoice_items_pending
        ADD COLUMN matched_by VARCHAR(20) NULL;

        RAISE NOTICE 'Stĺpec matched_by pridaný';

        -- Pridať komentár
        COMMENT ON COLUMN invoice_items_pending.matched_by IS
            'Metóda matchovania: ean, name, alebo NULL';
    ELSE
        RAISE NOTICE 'Stĺpec matched_by už existuje';
    END IF;
END $$;

-- Overiť štruktúru
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'invoice_items_pending'
    AND column_name IN ('nex_gs_code', 'nex_name', 'nex_category', 'in_nex', 'matched_by')
ORDER BY ordinal_position;