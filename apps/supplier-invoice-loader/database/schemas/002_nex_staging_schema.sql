-- ============================================================================
-- NEX Staging Schema - For nex-staging package
-- ============================================================================
-- This schema matches what the nex-staging package expects
-- Based on: packages/nex-staging/nex_staging/staging_client.py
--           packages/nex-staging/nex_staging/repositories/invoice_repository.py
-- ============================================================================

-- Drop existing tables (clean install)
DROP TABLE IF EXISTS invoice_items_pending CASCADE;
DROP TABLE IF EXISTS invoices_pending CASCADE;

-- ============================================================================
-- invoices_pending - Invoice Headers
-- ============================================================================
CREATE TABLE invoices_pending (
    -- Primary Key
    id                      SERIAL PRIMARY KEY,

    -- XML Data (from ISDOC)
    xml_invoice_number      VARCHAR(50),
    xml_variable_symbol     VARCHAR(50),
    xml_issue_date          DATE,
    xml_tax_point_date      DATE,
    xml_due_date            DATE,
    xml_currency            VARCHAR(3) DEFAULT 'EUR',

    -- Supplier from XML
    xml_supplier_ico        VARCHAR(20),
    xml_supplier_name       VARCHAR(200),
    xml_supplier_dic        VARCHAR(20),
    xml_supplier_ic_dph     VARCHAR(20),
    xml_iban                VARCHAR(50),
    xml_swift               VARCHAR(20),

    -- Amounts from XML
    xml_total_without_vat   NUMERIC(12,2),
    xml_total_vat           NUMERIC(12,2),
    xml_total_with_vat      NUMERIC(12,2),

    -- NEX Genesis References (after matching/import)
    nex_supplier_id         INTEGER,
    nex_supplier_modify_id  INTEGER,
    nex_iban                VARCHAR(50),
    nex_swift               VARCHAR(20),
    nex_stock_id            INTEGER,
    nex_book_num            VARCHAR(10),
    nex_payment_method_id   INTEGER,
    nex_price_list_id       INTEGER,
    nex_document_id         INTEGER,
    nex_invoice_doc_id      VARCHAR(20),
    nex_delivery_doc_id     VARCHAR(20),

    -- Workflow Status
    status                  VARCHAR(20) DEFAULT 'pending',
    file_status             VARCHAR(20) DEFAULT 'received',

    -- File Paths
    pdf_file_path           VARCHAR(500),
    xml_file_path           VARCHAR(500),
    file_basename           VARCHAR(100),

    -- Matching Statistics
    item_count              INTEGER DEFAULT 0,
    items_matched           INTEGER DEFAULT 0,
    match_percent           NUMERIC(5,2),

    -- Validation
    validation_status       VARCHAR(20),
    validation_errors       TEXT,

    -- Timestamps
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at            TIMESTAMP,
    imported_at             TIMESTAMP,

    -- Constraints
    CONSTRAINT invoices_pending_unique
        UNIQUE(xml_supplier_ico, xml_invoice_number),
    CONSTRAINT invoices_pending_status_check
        CHECK (status IN ('pending', 'matched', 'approved', 'rejected', 'imported', 'error')),
    CONSTRAINT invoices_pending_file_status_check
        CHECK (file_status IN ('received', 'staged', 'archived', 'deleted'))
);

-- Indexes
CREATE INDEX idx_ip_status ON invoices_pending(status);
CREATE INDEX idx_ip_file_status ON invoices_pending(file_status);
CREATE INDEX idx_ip_supplier_ico ON invoices_pending(xml_supplier_ico);
CREATE INDEX idx_ip_issue_date ON invoices_pending(xml_issue_date);
CREATE INDEX idx_ip_created_at ON invoices_pending(created_at);

COMMENT ON TABLE invoices_pending IS 'Invoice headers for staging workflow';

-- ============================================================================
-- invoice_items_pending - Invoice Line Items
-- ============================================================================
CREATE TABLE invoice_items_pending (
    -- Primary Key
    id                      SERIAL PRIMARY KEY,
    invoice_head_id         INTEGER NOT NULL REFERENCES invoices_pending(id) ON DELETE CASCADE,

    -- XML Data (from ISDOC)
    xml_line_number         INTEGER,
    xml_seller_code         VARCHAR(50),
    xml_ean                 VARCHAR(50),
    xml_product_name        VARCHAR(200),
    xml_quantity            NUMERIC(12,3),
    xml_unit                VARCHAR(20),
    xml_unit_price          NUMERIC(12,4),
    xml_unit_price_vat      NUMERIC(12,4),
    xml_total_price         NUMERIC(12,2),
    xml_total_price_vat     NUMERIC(12,2),
    xml_vat_rate            NUMERIC(5,2),

    -- NEX Genesis References (after matching)
    nex_product_id          INTEGER,
    nex_product_name        VARCHAR(200),
    nex_ean                 VARCHAR(50),
    nex_stock_code          VARCHAR(50),
    nex_stock_id            INTEGER,

    -- Matching Info
    matched                 BOOLEAN DEFAULT FALSE,
    matched_by              VARCHAR(20),  -- 'ean', 'name', 'code', 'manual'
    match_confidence        NUMERIC(5,2),

    -- Edits
    edited_unit_price       NUMERIC(12,4),

    -- Validation
    validation_status       VARCHAR(20),

    -- Timestamps
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT iip_unique_line UNIQUE(invoice_head_id, xml_line_number)
);

-- Indexes
CREATE INDEX idx_iip_invoice_head ON invoice_items_pending(invoice_head_id);
CREATE INDEX idx_iip_ean ON invoice_items_pending(xml_ean);
CREATE INDEX idx_iip_nex_product ON invoice_items_pending(nex_product_id);
CREATE INDEX idx_iip_matched ON invoice_items_pending(matched);

COMMENT ON TABLE invoice_items_pending IS 'Invoice line items for staging workflow';

-- ============================================================================
-- Trigger: auto update updated_at
-- ============================================================================
CREATE OR REPLACE FUNCTION trigger_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_invoices_pending_updated
    BEFORE UPDATE ON invoices_pending
    FOR EACH ROW
    EXECUTE FUNCTION trigger_update_timestamp();

CREATE TRIGGER trg_invoice_items_pending_updated
    BEFORE UPDATE ON invoice_items_pending
    FOR EACH ROW
    EXECUTE FUNCTION trigger_update_timestamp();

-- ============================================================================
-- Verify installation
-- ============================================================================
SELECT
    'Schema installed successfully' as status,
    (SELECT COUNT(*) FROM information_schema.tables
     WHERE table_schema = 'public' AND table_name IN ('invoices_pending', 'invoice_items_pending')) as table_count;
