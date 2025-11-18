-- ============================================================================
-- Invoice Editor - PostgreSQL Staging Database Schema
-- ============================================================================
-- Project: invoice-editor
-- Purpose: Staging database for ISDOC invoice approval workflow
-- Target: PostgreSQL 12+
-- Created: 2025-11-12
-- Session: 2
-- ============================================================================

-- Drop existing tables (for clean reinstall)
DROP TABLE IF EXISTS invoice_log CASCADE;
DROP TABLE IF EXISTS invoice_items_pending CASCADE;
DROP TABLE IF EXISTS invoices_pending CASCADE;
DROP TABLE IF EXISTS barcodes_staging CASCADE;
DROP TABLE IF EXISTS products_staging CASCADE;
DROP TABLE IF EXISTS categories_cache CASCADE;

-- ============================================================================
-- STAGING TABLES - Invoice Workflow
-- ============================================================================

-- ----------------------------------------------------------------------------
-- invoices_pending - Invoice Headers Awaiting Approval
-- ----------------------------------------------------------------------------
-- Purpose: Store ISDOC invoices from supplier_invoice_loader
-- Source: Email processing workflow
-- Target: NEX Genesis (TSH/TSI) after approval
-- ----------------------------------------------------------------------------
CREATE TABLE invoices_pending (
    -- Primary Key
    id                      SERIAL PRIMARY KEY,

    -- Supplier Information
    supplier_ico            VARCHAR(20) NOT NULL,
    supplier_name           VARCHAR(200),
    supplier_dic            VARCHAR(20),

    -- Invoice Header
    invoice_number          VARCHAR(50) NOT NULL,
    invoice_date            DATE NOT NULL,
    due_date                DATE,
    currency                VARCHAR(3) DEFAULT 'EUR',

    -- Amounts
    total_amount            NUMERIC(12,2) NOT NULL,
    total_vat               NUMERIC(12,2),
    total_without_vat       NUMERIC(12,2),

    -- Original ISDOC XML
    isdoc_xml               TEXT,

    -- Workflow Status
    status                  VARCHAR(20) NOT NULL DEFAULT 'pending',
                            -- Values: pending, approved, rejected, imported, error
    created_at              TIMESTAMP NOT NULL DEFAULT NOW(),
    approved_by             VARCHAR(50),
    approved_at             TIMESTAMP,
    imported_at             TIMESTAMP,
    rejected_at             TIMESTAMP,
    rejection_reason        TEXT,

    -- NEX Genesis Reference (after import)
    nex_doc_number          VARCHAR(50),    -- TSH document number
    nex_pab_code            INTEGER,        -- PAB code of supplier
    nex_book                VARCHAR(10),    -- Book ID (e.g., "001")
    nex_book_type           VARCHAR(1),     -- Book type (e.g., "A")

    -- Error Handling
    error_message           TEXT,
    retry_count             INTEGER DEFAULT 0,

    -- Constraints
    CONSTRAINT invoices_pending_unique_invoice
        UNIQUE(supplier_ico, invoice_number),
    CONSTRAINT invoices_pending_status_check
        CHECK (status IN ('pending', 'approved', 'rejected', 'imported', 'error')),
    CONSTRAINT invoices_pending_currency_check
        CHECK (currency IN ('EUR', 'CZK', 'USD'))
);

-- Indexes for Performance
CREATE INDEX idx_invoices_status ON invoices_pending(status);
CREATE INDEX idx_invoices_supplier ON invoices_pending(supplier_ico);
CREATE INDEX idx_invoices_date ON invoices_pending(invoice_date);
CREATE INDEX idx_invoices_created ON invoices_pending(created_at);

COMMENT ON TABLE invoices_pending IS 'Invoice headers awaiting operator approval';
COMMENT ON COLUMN invoices_pending.status IS 'pending=new, approved=ready for import, rejected=declined, imported=done, error=failed';
COMMENT ON COLUMN invoices_pending.nex_doc_number IS 'TSH document number after successful import to NEX Genesis';

-- ----------------------------------------------------------------------------
-- invoice_items_pending - Invoice Line Items (Editable)
-- ----------------------------------------------------------------------------
-- Purpose: Line items from ISDOC with operator edits
-- Workflow: Operator edits names, categories, prices, rabat
-- Target: NEX Genesis TSI items + GSCAT products
-- ----------------------------------------------------------------------------
CREATE TABLE invoice_items_pending (
    -- Primary Key
    id                      SERIAL PRIMARY KEY,
    invoice_id              INTEGER NOT NULL REFERENCES invoices_pending(id) ON DELETE CASCADE,
    line_number             INTEGER NOT NULL,

    -- Original Data from ISDOC
    original_name           VARCHAR(200) NOT NULL,
    original_quantity       NUMERIC(12,3) NOT NULL,
    original_unit           VARCHAR(20),
    original_price_per_unit NUMERIC(12,2) NOT NULL,
    original_ean            VARCHAR(50),
    original_vat_rate       NUMERIC(5,2),

    -- Operator Edits
    edited_name             VARCHAR(200),
    edited_mglst_code       INTEGER,        -- FK to categories_cache (MGLST)
    edited_price_buy        NUMERIC(12,2),  -- Nákupná cena
    edited_price_sell       NUMERIC(12,2),  -- Predajná cena
    edited_discount_percent NUMERIC(5,2) DEFAULT 0.00,  -- Rabat %
    edited_ean              VARCHAR(50),

    -- Calculated Fields (after rabat)
    final_price_buy         NUMERIC(12,2),  -- After rabat calculation
    final_price_sell        NUMERIC(12,2),

    -- Flags
    was_edited              BOOLEAN DEFAULT FALSE,
    validation_status       VARCHAR(20) DEFAULT 'pending',
                            -- Values: pending, valid, warning, error
    validation_message      TEXT,

    -- NEX Genesis Reference (after import)
    nex_gs_code             INTEGER,        -- Created/updated GsCode in GSCAT
    nex_barcode_created     BOOLEAN DEFAULT FALSE,

    -- Timestamps
    edited_at               TIMESTAMP,

    -- Constraints
    CONSTRAINT invoice_items_unique_line
        UNIQUE(invoice_id, line_number),
    CONSTRAINT invoice_items_quantity_positive
        CHECK (original_quantity > 0),
    CONSTRAINT invoice_items_price_positive
        CHECK (original_price_per_unit >= 0),
    CONSTRAINT invoice_items_discount_range
        CHECK (edited_discount_percent BETWEEN 0 AND 100),
    CONSTRAINT invoice_items_validation_check
        CHECK (validation_status IN ('pending', 'valid', 'warning', 'error'))
);

-- Indexes for Performance
CREATE INDEX idx_items_invoice ON invoice_items_pending(invoice_id);
CREATE INDEX idx_items_ean ON invoice_items_pending(original_ean);
CREATE INDEX idx_items_edited_ean ON invoice_items_pending(edited_ean);
CREATE INDEX idx_items_gs_code ON invoice_items_pending(nex_gs_code);
CREATE INDEX idx_items_validation ON invoice_items_pending(validation_status);

COMMENT ON TABLE invoice_items_pending IS 'Invoice line items with operator edits';
COMMENT ON COLUMN invoice_items_pending.edited_discount_percent IS 'Rabat % - automatically recalculates final prices';
COMMENT ON COLUMN invoice_items_pending.final_price_buy IS 'Calculated: original_price_per_unit * (1 - rabat/100)';

-- ----------------------------------------------------------------------------
-- invoice_log - Audit Trail
-- ----------------------------------------------------------------------------
-- Purpose: Complete audit trail of all invoice operations
-- Usage: Debugging, compliance, operator activity tracking
-- ----------------------------------------------------------------------------
CREATE TABLE invoice_log (
    id                      SERIAL PRIMARY KEY,
    invoice_id              INTEGER NOT NULL REFERENCES invoices_pending(id) ON DELETE CASCADE,

    -- Action Information
    action                  VARCHAR(50) NOT NULL,
                            -- CREATED, LOADED, EDITED, VALIDATED, APPROVED, REJECTED,
                            -- IMPORTED, ERROR, STATUS_CHANGED
    user_name               VARCHAR(50),
    timestamp               TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Details
    changes                 JSONB,          -- Structured change log
    notes                   TEXT,           -- Human-readable notes
    error_details           TEXT,           -- Error stack trace if applicable

    -- Context
    ip_address              VARCHAR(50),
    session_id              VARCHAR(100)
);

-- Indexes for Performance
CREATE INDEX idx_log_invoice ON invoice_log(invoice_id);
CREATE INDEX idx_log_action ON invoice_log(action);
CREATE INDEX idx_log_timestamp ON invoice_log(timestamp);
CREATE INDEX idx_log_user ON invoice_log(user_name);

COMMENT ON TABLE invoice_log IS 'Complete audit trail of invoice workflow actions';
COMMENT ON COLUMN invoice_log.changes IS 'JSON structure: {field: {old: value, new: value}}';

-- ============================================================================
-- CACHE TABLES - NEX Genesis Data
-- ============================================================================
-- Purpose: Read-only caches synchronized from NEX Genesis Btrieve
-- Update: Periodic sync (e.g., every 5 minutes or on-demand)
-- Usage: Product suggestions, validation, category dropdowns
-- ============================================================================

-- ----------------------------------------------------------------------------
-- categories_cache - Product Categories (MGLST)
-- ----------------------------------------------------------------------------
-- Source: NEX Genesis MGLST.BTR
-- Purpose: Category dropdown in UI, validation
-- ----------------------------------------------------------------------------
CREATE TABLE categories_cache (
    mglst_code              INTEGER PRIMARY KEY,
    mglst_name              VARCHAR(200) NOT NULL,
    parent_code             INTEGER,
    level                   INTEGER,
    full_path               VARCHAR(500),   -- Hierarchical path
    is_active               BOOLEAN DEFAULT TRUE,

    -- Sync Metadata
    last_sync               TIMESTAMP DEFAULT NOW(),

    -- Constraints
    CONSTRAINT categories_parent_fk
        FOREIGN KEY (parent_code) REFERENCES categories_cache(mglst_code)
);

-- Indexes
CREATE INDEX idx_categories_parent ON categories_cache(parent_code);
CREATE INDEX idx_categories_name ON categories_cache(mglst_name);
CREATE INDEX idx_categories_active ON categories_cache(is_active);

COMMENT ON TABLE categories_cache IS 'Read-only cache of MGLST (product categories) from NEX Genesis';

-- ----------------------------------------------------------------------------
-- products_staging - Product Catalog (GSCAT)
-- ----------------------------------------------------------------------------
-- Source: NEX Genesis GSCAT.BTR
-- Purpose: Product suggestions during invoice editing, EAN lookup
-- ----------------------------------------------------------------------------
CREATE TABLE products_staging (
    gs_code                 INTEGER PRIMARY KEY,
    gs_name                 VARCHAR(200) NOT NULL,
    gs_name2                VARCHAR(200),
    mglst_code              INTEGER,

    -- Prices
    price_buy               NUMERIC(12,2),
    price_sell              NUMERIC(12,2),
    vat_rate                NUMERIC(5,2),

    -- Stock
    stock_quantity          NUMERIC(12,3),
    unit                    VARCHAR(20),

    -- Flags
    is_active               BOOLEAN DEFAULT TRUE,
    allow_negative_stock    BOOLEAN DEFAULT FALSE,

    -- Sync Metadata
    last_sync               TIMESTAMP DEFAULT NOW(),

    -- Constraints
    CONSTRAINT products_category_fk
        FOREIGN KEY (mglst_code) REFERENCES categories_cache(mglst_code)
);

-- Indexes
CREATE INDEX idx_products_name ON products_staging(gs_name);
CREATE INDEX idx_products_category ON products_staging(mglst_code);
CREATE INDEX idx_products_active ON products_staging(is_active);

COMMENT ON TABLE products_staging IS 'Read-only cache of GSCAT (products) from NEX Genesis';

-- ----------------------------------------------------------------------------
-- barcodes_staging - Product Barcodes (BARCODE)
-- ----------------------------------------------------------------------------
-- Source: NEX Genesis BARCODE.BTR
-- Purpose: EAN lookup during invoice processing
-- ----------------------------------------------------------------------------
CREATE TABLE barcodes_staging (
    bar_code                VARCHAR(50) PRIMARY KEY,
    gs_code                 INTEGER NOT NULL,

    -- Sync Metadata
    last_sync               TIMESTAMP DEFAULT NOW(),

    -- Constraints
    CONSTRAINT barcodes_product_fk
        FOREIGN KEY (gs_code) REFERENCES products_staging(gs_code)
);

-- Indexes
CREATE INDEX idx_barcodes_gs_code ON barcodes_staging(gs_code);

COMMENT ON TABLE barcodes_staging IS 'Read-only cache of BARCODE from NEX Genesis';

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Function: calculate_final_price
-- Purpose: Calculate final price after rabat discount
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION calculate_final_price(
    p_original_price NUMERIC,
    p_discount_percent NUMERIC
) RETURNS NUMERIC AS $$
BEGIN
    RETURN ROUND(p_original_price * (1 - p_discount_percent / 100.0), 2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION calculate_final_price IS 'Calculate price after rabat: price * (1 - discount/100)';

-- ----------------------------------------------------------------------------
-- Trigger: auto_calculate_final_prices
-- Purpose: Automatically update final prices when rabat changes
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION trigger_calculate_final_prices()
RETURNS TRIGGER AS $$
BEGIN
    -- Calculate final buy price
    IF NEW.edited_price_buy IS NOT NULL THEN
        NEW.final_price_buy := calculate_final_price(
            NEW.edited_price_buy,
            COALESCE(NEW.edited_discount_percent, 0)
        );
    END IF;

    -- Calculate final sell price
    IF NEW.edited_price_sell IS NOT NULL THEN
        NEW.final_price_sell := calculate_final_price(
            NEW.edited_price_sell,
            COALESCE(NEW.edited_discount_percent, 0)
        );
    END IF;

    -- Mark as edited
    IF NEW.edited_name IS NOT NULL
        OR NEW.edited_mglst_code IS NOT NULL
        OR NEW.edited_price_buy IS NOT NULL
        OR NEW.edited_price_sell IS NOT NULL
        OR NEW.edited_discount_percent IS NOT NULL THEN
        NEW.was_edited := TRUE;
        NEW.edited_at := NOW();
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_calculate_final_prices
    BEFORE INSERT OR UPDATE ON invoice_items_pending
    FOR EACH ROW
    EXECUTE FUNCTION trigger_calculate_final_prices();

COMMENT ON FUNCTION trigger_calculate_final_prices IS 'Auto-calculate final prices on insert/update';

-- ----------------------------------------------------------------------------
-- Trigger: auto_log_invoice_changes
-- Purpose: Automatically log invoice status changes
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION trigger_log_invoice_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- Log status changes
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO invoice_log (invoice_id, action, changes)
        VALUES (
            NEW.id,
            'STATUS_CHANGED',
            jsonb_build_object(
                'status', jsonb_build_object('old', OLD.status, 'new', NEW.status)
            )
        );
    END IF;

    -- Log approval
    IF NEW.status = 'approved' AND OLD.status != 'approved' THEN
        INSERT INTO invoice_log (invoice_id, action, user_name)
        VALUES (NEW.id, 'APPROVED', NEW.approved_by);
    END IF;

    -- Log rejection
    IF NEW.status = 'rejected' AND OLD.status != 'rejected' THEN
        INSERT INTO invoice_log (invoice_id, action, user_name, notes)
        VALUES (NEW.id, 'REJECTED', NEW.approved_by, NEW.rejection_reason);
    END IF;

    -- Log import
    IF NEW.status = 'imported' AND OLD.status != 'imported' THEN
        INSERT INTO invoice_log (invoice_id, action, changes)
        VALUES (
            NEW.id,
            'IMPORTED',
            jsonb_build_object(
                'nex_doc_number', NEW.nex_doc_number,
                'nex_pab_code', NEW.nex_pab_code
            )
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_invoice_changes
    AFTER UPDATE ON invoices_pending
    FOR EACH ROW
    EXECUTE FUNCTION trigger_log_invoice_changes();

COMMENT ON FUNCTION trigger_log_invoice_changes IS 'Auto-log invoice workflow changes';

-- ============================================================================
-- VIEWS - Convenient Data Access
-- ============================================================================

-- ----------------------------------------------------------------------------
-- View: v_pending_invoices_summary
-- Purpose: Dashboard view of pending invoices
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_pending_invoices_summary AS
SELECT
    i.id,
    i.invoice_number,
    i.invoice_date,
    i.supplier_name,
    i.supplier_ico,
    i.total_amount,
    i.currency,
    i.status,
    i.created_at,
    COUNT(ii.id) as item_count,
    SUM(CASE WHEN ii.was_edited THEN 1 ELSE 0 END) as edited_item_count,
    SUM(CASE WHEN ii.validation_status = 'error' THEN 1 ELSE 0 END) as error_count
FROM invoices_pending i
LEFT JOIN invoice_items_pending ii ON i.id = ii.invoice_id
WHERE i.status = 'pending'
GROUP BY i.id
ORDER BY i.created_at DESC;

COMMENT ON VIEW v_pending_invoices_summary IS 'Dashboard summary of pending invoices';

-- ----------------------------------------------------------------------------
-- View: v_invoice_details
-- Purpose: Complete invoice with items
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_invoice_details AS
SELECT
    i.*,
    ii.id as item_id,
    ii.line_number,
    ii.original_name,
    ii.original_quantity,
    ii.original_price_per_unit,
    ii.original_ean,
    ii.edited_name,
    ii.edited_mglst_code,
    ii.edited_price_buy,
    ii.edited_price_sell,
    ii.edited_discount_percent,
    ii.final_price_buy,
    ii.final_price_sell,
    ii.was_edited,
    ii.validation_status,
    c.mglst_name as category_name
FROM invoices_pending i
LEFT JOIN invoice_items_pending ii ON i.id = ii.invoice_id
LEFT JOIN categories_cache c ON ii.edited_mglst_code = c.mglst_code
ORDER BY i.id, ii.line_number;

COMMENT ON VIEW v_invoice_details IS 'Complete invoice details with all items';

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Sample category (will be replaced by sync from NEX Genesis)
INSERT INTO categories_cache (mglst_code, mglst_name, parent_code, level, full_path)
VALUES (1, 'Nezaradené', NULL, 0, 'Nezaradené')
ON CONFLICT (mglst_code) DO NOTHING;

-- ============================================================================
-- GRANTS (adjust based on your user setup)
-- ============================================================================
-- Example: GRANT ALL ON ALL TABLES IN SCHEMA public TO invoice_user;
-- Example: GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO invoice_user;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Verify installation
SELECT
    'Schema installation complete' as status,
    COUNT(*) as table_count
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE';