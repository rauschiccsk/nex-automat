-- ============================================================================
-- SUPPLIER INVOICE STAGING - Complete Database Schema
-- Database: supplier_invoice_staging
-- Version: 1.0
-- Created: 2025-12-18
-- ============================================================================
--
-- KONVENCIE:
--   xml_*  = Polia z ISDOC XML (immutable, len ukladáme)
--   nex_*  = Polia z NEX Genesis (obohatenie/párovanie)
--
-- WORKFLOW STAVY:
--   pending   = Čaká na spracovanie
--   matched   = Položky napárované s NEX
--   approved  = Schválené operátorom
--   imported  = Importované do NEX Genesis
--
-- ============================================================================

-- Pomocná funkcia pre updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- SUPPLIER_INVOICE_HEADS - Hlavičky faktúr
-- ============================================================================

CREATE TABLE supplier_invoice_heads (
    id SERIAL PRIMARY KEY,

    -- XML POLIA (z ISDOC XML - IMMUTABLE)
    xml_invoice_number VARCHAR(50) NOT NULL,
    xml_variable_symbol VARCHAR(10),
    xml_issue_date DATE NOT NULL,
    xml_tax_point_date DATE,
    xml_due_date DATE,
    xml_currency VARCHAR(3) DEFAULT 'EUR',
    xml_supplier_ico VARCHAR(20) NOT NULL,
    xml_supplier_name VARCHAR(255),
    xml_supplier_dic VARCHAR(20),
    xml_supplier_ic_dph VARCHAR(20),
    xml_iban VARCHAR(34),
    xml_swift VARCHAR(20),
    xml_total_without_vat DECIMAL(15,2),
    xml_total_vat DECIMAL(15,2),
    xml_total_with_vat DECIMAL(15,2) NOT NULL,

    -- NEX POLIA (obohatenie)
    nex_supplier_id INTEGER,
    nex_supplier_modify_id INTEGER DEFAULT 0,
    nex_iban VARCHAR(34),
    nex_swift VARCHAR(20),
    nex_stock_id INTEGER,
    nex_book_num INTEGER,
    nex_payment_method_id INTEGER,
    nex_price_list_id INTEGER,

    -- WORKFLOW
    status VARCHAR(20) DEFAULT 'pending',
    item_count INTEGER DEFAULT 0,
    items_matched INTEGER DEFAULT 0,
    match_percent DECIMAL(5,2) DEFAULT 0,
    validation_status VARCHAR(20) DEFAULT 'pending',
    validation_errors TEXT,

    -- SÚBORY
    xml_file_path VARCHAR(500),
    pdf_file_path VARCHAR(500),

    -- AUDIT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    imported_at TIMESTAMP,
    nex_document_id BIGINT,

    CONSTRAINT uq_supplier_invoice UNIQUE (xml_supplier_ico, xml_invoice_number)
);

CREATE INDEX idx_sih_supplier_ico ON supplier_invoice_heads(xml_supplier_ico);
CREATE INDEX idx_sih_invoice_number ON supplier_invoice_heads(xml_invoice_number);
CREATE INDEX idx_sih_status ON supplier_invoice_heads(status);
CREATE INDEX idx_sih_issue_date ON supplier_invoice_heads(xml_issue_date);
CREATE INDEX idx_sih_nex_supplier ON supplier_invoice_heads(nex_supplier_id);

CREATE TRIGGER tr_sih_updated_at
    BEFORE UPDATE ON supplier_invoice_heads
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- ============================================================================
-- SUPPLIER_INVOICE_ITEMS - Položky faktúr
-- ============================================================================

CREATE TABLE supplier_invoice_items (
    id SERIAL PRIMARY KEY,
    invoice_head_id INTEGER NOT NULL REFERENCES supplier_invoice_heads(id) ON DELETE CASCADE,

    -- XML POLIA (z ISDOC XML - IMMUTABLE)
    xml_line_number INTEGER NOT NULL,
    xml_product_name VARCHAR(255) NOT NULL,
    xml_seller_code VARCHAR(50),
    xml_ean VARCHAR(20),
    xml_quantity DECIMAL(10,3) NOT NULL,
    xml_unit VARCHAR(10),
    xml_unit_price DECIMAL(12,4),
    xml_total_price DECIMAL(12,2),
    xml_unit_price_vat DECIMAL(12,4),
    xml_total_price_vat DECIMAL(12,2),
    xml_vat_rate DECIMAL(5,2),

    -- NEX POLIA (obohatenie)
    nex_product_id INTEGER,
    nex_product_modify_id INTEGER DEFAULT 0,
    nex_product_name VARCHAR(255),
    nex_product_category_id INTEGER,
    nex_ean VARCHAR(20),
    nex_stock_code VARCHAR(20),
    nex_stock_id INTEGER,
    nex_facility_id INTEGER,
    nex_purchase_price DECIMAL(12,4),
    nex_sales_price DECIMAL(12,4),

    -- MATCHING
    matched BOOLEAN DEFAULT FALSE,
    matched_by VARCHAR(20),
    match_confidence DECIMAL(5,2),
    match_attempts INTEGER DEFAULT 0,

    -- WORKFLOW
    validation_status VARCHAR(20) DEFAULT 'pending',
    validation_errors TEXT,
    edited_product_name VARCHAR(255),
    edited_quantity DECIMAL(10,3),
    edited_unit_price DECIMAL(12,4),

    -- AUDIT
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    matched_at TIMESTAMP,
    matched_by_user VARCHAR(50),

    CONSTRAINT uq_invoice_line UNIQUE (invoice_head_id, xml_line_number)
);

CREATE INDEX idx_sii_invoice_head ON supplier_invoice_items(invoice_head_id);
CREATE INDEX idx_sii_xml_ean ON supplier_invoice_items(xml_ean);
CREATE INDEX idx_sii_xml_seller_code ON supplier_invoice_items(xml_seller_code);
CREATE INDEX idx_sii_nex_product ON supplier_invoice_items(nex_product_id);
CREATE INDEX idx_sii_matched ON supplier_invoice_items(matched);

CREATE TRIGGER tr_sii_updated_at
    BEFORE UPDATE ON supplier_invoice_items
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Trigger pre aktualizáciu štatistík v hlavičke
CREATE OR REPLACE FUNCTION update_invoice_head_stats()
RETURNS TRIGGER AS $$
DECLARE
    v_head_id INTEGER;
BEGIN
    v_head_id := COALESCE(NEW.invoice_head_id, OLD.invoice_head_id);

    UPDATE supplier_invoice_heads SET
        item_count = (SELECT COUNT(*) FROM supplier_invoice_items WHERE invoice_head_id = v_head_id),
        items_matched = (SELECT COUNT(*) FROM supplier_invoice_items WHERE invoice_head_id = v_head_id AND matched = TRUE),
        match_percent = (
            SELECT CASE WHEN COUNT(*) = 0 THEN 0
                ELSE ROUND((COUNT(*) FILTER (WHERE matched = TRUE)::numeric / COUNT(*)::numeric) * 100, 1)
            END FROM supplier_invoice_items WHERE invoice_head_id = v_head_id
        )
    WHERE id = v_head_id;

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_sii_update_head_stats
    AFTER INSERT OR UPDATE OR DELETE ON supplier_invoice_items
    FOR EACH ROW EXECUTE FUNCTION update_invoice_head_stats();

-- ============================================================================
-- KOMENTÁRE
-- ============================================================================

COMMENT ON TABLE supplier_invoice_heads IS 'Staging - hlavičky dodávateľských faktúr';
COMMENT ON TABLE supplier_invoice_items IS 'Staging - položky dodávateľských faktúr';

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================