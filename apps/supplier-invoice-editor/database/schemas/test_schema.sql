-- ============================================================================
-- Schema Verification & Testing Queries
-- ============================================================================
-- Run these queries in pgAdmin4 Query Tool after schema installation
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. VERIFY ALL TABLES EXIST
-- ----------------------------------------------------------------------------
SELECT
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = t.table_name AND table_schema = 'public') as column_count
FROM information_schema.tables t
WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Expected: 6 tables
-- invoices_pending, invoice_items_pending, invoice_log,
-- categories_cache, products_staging, barcodes_staging

-- ----------------------------------------------------------------------------
-- 2. VERIFY TRIGGERS EXIST
-- ----------------------------------------------------------------------------
SELECT
    trigger_name,
    event_manipulation,
    event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;

-- Expected: 2 triggers
-- trg_calculate_final_prices on invoice_items_pending
-- trg_log_invoice_changes on invoices_pending

-- ----------------------------------------------------------------------------
-- 3. VERIFY VIEWS EXIST
-- ----------------------------------------------------------------------------
SELECT
    table_name as view_name,
    view_definition
FROM information_schema.views
WHERE table_schema = 'public';

-- Expected: 2 views
-- v_pending_invoices_summary
-- v_invoice_details

-- ----------------------------------------------------------------------------
-- 4. TEST DATA - Insert Sample Invoice
-- ----------------------------------------------------------------------------
-- Insert sample invoice
INSERT INTO invoices_pending (
    supplier_ico,
    supplier_name,
    invoice_number,
    invoice_date,
    currency,
    total_amount,
    total_vat,
    total_without_vat,
    isdoc_xml,
    status
) VALUES (
    '12345678',
    'Test Dodávateľ s.r.o.',
    'FAV-2025-001',
    '2025-11-12',
    'EUR',
    1200.00,
    200.00,
    1000.00,
    '<ISDOC>test xml</ISDOC>',
    'pending'
) RETURNING id;

-- Remember the returned ID for next steps!
-- Let's assume ID = 1 for following queries

-- ----------------------------------------------------------------------------
-- 5. TEST DATA - Insert Invoice Items
-- ----------------------------------------------------------------------------
-- Insert 3 items for the invoice (use actual ID from previous INSERT)
INSERT INTO invoice_items_pending (
    invoice_id,
    line_number,
    original_name,
    original_quantity,
    original_unit,
    original_price_per_unit,
    original_ean,
    original_vat_rate,
    edited_name,
    edited_mglst_code,
    edited_price_buy,
    edited_price_sell,
    edited_discount_percent
) VALUES
    -- Item 1: With 10% rabat
    (
        1,  -- CHANGE THIS to your actual invoice_id
        1,
        'Test Produkt 1',
        10.000,
        'ks',
        100.00,
        '8590123456789',
        20.00,
        'Test Produkt 1 - Upravený',
        1,
        100.00,
        150.00,
        10.00  -- 10% rabat
    ),
    -- Item 2: With 25% rabat
    (
        1,  -- CHANGE THIS to your actual invoice_id
        2,
        'Test Produkt 2',
        5.000,
        'ks',
        200.00,
        '8590123456790',
        20.00,
        'Test Produkt 2 - Upravený',
        1,
        200.00,
        300.00,
        25.00  -- 25% rabat
    ),
    -- Item 3: No rabat
    (
        1,  -- CHANGE THIS to your actual invoice_id
        3,
        'Test Produkt 3',
        20.000,
        'ks',
        50.00,
        '8590123456791',
        20.00,
        'Test Produkt 3 - Upravený',
        1,
        50.00,
        75.00,
        0.00  -- No rabat
    );

-- ----------------------------------------------------------------------------
-- 6. VERIFY TRIGGER: Auto-Calculate Final Prices
-- ----------------------------------------------------------------------------
-- Check if final prices were calculated correctly
SELECT
    line_number,
    original_name,
    edited_price_buy,
    edited_discount_percent,
    final_price_buy,
    edited_price_sell,
    final_price_sell,
    was_edited,
    edited_at,
    -- Manual calculation for verification
    ROUND(edited_price_buy * (1 - edited_discount_percent / 100.0), 2) as expected_final_buy,
    ROUND(edited_price_sell * (1 - edited_discount_percent / 100.0), 2) as expected_final_sell,
    -- Check if calculation is correct
    CASE
        WHEN final_price_buy = ROUND(edited_price_buy * (1 - edited_discount_percent / 100.0), 2)
        THEN '✅ OK'
        ELSE '❌ CHYBA'
    END as price_calculation_status
FROM invoice_items_pending
WHERE invoice_id = 1  -- CHANGE THIS to your actual invoice_id
ORDER BY line_number;

-- Expected results:
-- Line 1: 100.00 - 10% = 90.00, 150.00 - 10% = 135.00
-- Line 2: 200.00 - 25% = 150.00, 300.00 - 25% = 225.00
-- Line 3: 50.00 - 0% = 50.00, 75.00 - 0% = 75.00

-- ----------------------------------------------------------------------------
-- 7. TEST TRIGGER: Update Rabat and Verify Recalculation
-- ----------------------------------------------------------------------------
-- Change rabat from 10% to 20% on first item
UPDATE invoice_items_pending
SET edited_discount_percent = 20.00
WHERE invoice_id = 1 AND line_number = 1;

-- Verify new calculation
SELECT
    line_number,
    edited_price_buy,
    edited_discount_percent,
    final_price_buy,
    -- Should be: 100.00 * (1 - 0.20) = 80.00
    CASE
        WHEN final_price_buy = 80.00 THEN '✅ Trigger works!'
        ELSE '❌ Trigger failed: ' || final_price_buy::text
    END as trigger_test
FROM invoice_items_pending
WHERE invoice_id = 1 AND line_number = 1;

-- ----------------------------------------------------------------------------
-- 8. TEST TRIGGER: Approve Invoice and Check Audit Log
-- ----------------------------------------------------------------------------
-- Approve the invoice
UPDATE invoices_pending
SET
    status = 'approved',
    approved_by = 'test_operator',
    approved_at = NOW()
WHERE id = 1;

-- Check if audit log was created automatically
SELECT
    il.id,
    il.action,
    il.user_name,
    il.timestamp,
    il.changes,
    i.status as current_invoice_status
FROM invoice_log il
JOIN invoices_pending i ON il.invoice_id = i.id
WHERE il.invoice_id = 1
ORDER BY il.timestamp DESC;

-- Expected: 2 log entries
-- 1. APPROVED with user_name = 'test_operator'
-- 2. STATUS_CHANGED with changes showing pending -> approved

-- ----------------------------------------------------------------------------
-- 9. TEST VIEW: Pending Invoices Summary
-- ----------------------------------------------------------------------------
-- First, create another pending invoice to see it in view
INSERT INTO invoices_pending (
    supplier_ico, supplier_name, invoice_number, invoice_date,
    currency, total_amount, status
) VALUES (
    '87654321', 'Dodávateľ 2 s.r.o.', 'FAV-2025-002',
    '2025-11-12', 'EUR', 500.00, 'pending'
);

-- Check the view (should show only pending invoices)
SELECT * FROM v_pending_invoices_summary;

-- Expected: 1 row (invoice 2), invoice 1 should NOT appear (status = approved)

-- ----------------------------------------------------------------------------
-- 10. TEST VIEW: Invoice Details
-- ----------------------------------------------------------------------------
SELECT
    invoice_number,
    supplier_name,
    status,
    line_number,
    edited_name,
    original_quantity,
    final_price_buy,
    final_price_sell,
    category_name
FROM v_invoice_details
WHERE id = 1
ORDER BY line_number;

-- Expected: 3 rows (3 items) with all calculated prices and category name

-- ----------------------------------------------------------------------------
-- 11. TEST FUNCTION: Manual Price Calculation
-- ----------------------------------------------------------------------------
SELECT
    calculate_final_price(100.00, 10.00) as test_10_percent,  -- Should be 90.00
    calculate_final_price(200.00, 25.00) as test_25_percent,  -- Should be 150.00
    calculate_final_price(50.00, 0.00) as test_0_percent,     -- Should be 50.00
    calculate_final_price(99.99, 33.33) as test_33_percent;   -- Should be 66.66

-- ----------------------------------------------------------------------------
-- 12. TEST CONSTRAINTS: Try Invalid Data
-- ----------------------------------------------------------------------------
-- This should FAIL (duplicate invoice)
INSERT INTO invoices_pending (
    supplier_ico, invoice_number, invoice_date,
    currency, total_amount, status
) VALUES (
    '12345678', 'FAV-2025-001', '2025-11-12',  -- Duplicate ICO + number
    'EUR', 100.00, 'pending'
);
-- Expected: ERROR - duplicate key value violates unique constraint

-- This should FAIL (invalid status)
UPDATE invoices_pending SET status = 'invalid_status' WHERE id = 1;
-- Expected: ERROR - new row for relation violates check constraint

-- This should FAIL (negative quantity)
INSERT INTO invoice_items_pending (
    invoice_id, line_number, original_name,
    original_quantity, original_price_per_unit
) VALUES (1, 999, 'Test', -5.0, 100.00);
-- Expected: ERROR - check constraint violation

-- This should FAIL (rabat > 100%)
UPDATE invoice_items_pending
SET edited_discount_percent = 150.00
WHERE id = 1;
-- Expected: ERROR - check constraint violation

-- ----------------------------------------------------------------------------
-- 13. PERFORMANCE TEST: Check Indexes
-- ----------------------------------------------------------------------------
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Expected: Multiple indexes on foreign keys and search columns

-- ----------------------------------------------------------------------------
-- 14. CLEANUP TEST DATA (Optional)
-- ----------------------------------------------------------------------------
-- Uncomment to clean up test data:
-- DELETE FROM invoice_log WHERE invoice_id IN (1, 2);
-- DELETE FROM invoice_items_pending WHERE invoice_id IN (1, 2);
-- DELETE FROM invoices_pending WHERE id IN (1, 2);

-- Or restart from scratch:
-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;
-- (then re-run 001_initial_schema.sql)

-- ============================================================================
-- SUMMARY OF EXPECTED RESULTS
-- ============================================================================
/*
✅ 6 tables created
✅ 2 triggers working (price calculation + audit log)
✅ 2 views functional
✅ 1 function working
✅ All constraints enforcing data integrity
✅ Indexes created for performance
✅ Automatic rabat → price recalculation
✅ Automatic audit logging

If all tests pass, schema is ready for application integration!
*/