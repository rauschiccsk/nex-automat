-- ============================================================================
-- NEX Automat - Supplier Invoice Staging Schema
-- Verzia: 1.0.0 (Konsolidovaná)
-- Dátum: 2026-01-27
--
-- Konsolidácia z:
--   - 002_nex_staging_schema.sql (xml_*/nex_* konvencia)
--   - 002_add_nex_columns.sql (nex_plu, nex_name, nex_category, in_nex)
--   - 003_add_file_tracking_columns.sql (file_basename, file_status, doc IDs)
--   - 001_supplier_invoice_staging.sql (nové názvy, trigger)
-- ============================================================================

-- Funkcia pre automatickú aktualizáciu updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- SUPPLIER_INVOICE_HEADS - Hlavičky dodávateľských faktúr
-- ============================================================================
CREATE TABLE IF NOT EXISTS supplier_invoice_heads (
    id SERIAL PRIMARY KEY,

    -- Identifikácia zákazníka a dodávateľa
    customer_code VARCHAR(20) NOT NULL DEFAULT 'ANDROS',
    supplier_code VARCHAR(20) NOT NULL,

    -- XML/ISDOC polia (prefix xml_)
    xml_invoice_number VARCHAR(50) NOT NULL,
    xml_variable_symbol VARCHAR(20),
    xml_issue_date DATE,
    xml_due_date DATE,
    xml_tax_point_date DATE,
    xml_delivery_date DATE,

    xml_supplier_ico VARCHAR(20) NOT NULL,
    xml_supplier_dic VARCHAR(20),
    xml_supplier_ic_dph VARCHAR(20),
    xml_supplier_name VARCHAR(255),

    xml_iban VARCHAR(34),
    xml_swift VARCHAR(11),

    xml_total_without_vat DECIMAL(15,2) NOT NULL DEFAULT 0,
    xml_total_vat DECIMAL(15,2) NOT NULL DEFAULT 0,
    xml_total_with_vat DECIMAL(15,2) NOT NULL DEFAULT 0,
    xml_currency VARCHAR(3) DEFAULT 'EUR',

    -- NEX Genesis polia (prefix nex_)
    nex_supplier_id INTEGER,
    nex_supplier_modify_id INTEGER,
    nex_iban VARCHAR(34),
    nex_swift VARCHAR(11),
    nex_stock_id INTEGER,
    nex_book_num INTEGER,
    nex_payment_method_id INTEGER,
    nex_price_list_id INTEGER,
    nex_document_id INTEGER,
    nex_invoice_doc_id VARCHAR(20),
    nex_delivery_doc_id VARCHAR(20),

    -- Súborové informácie
    source_type VARCHAR(20) DEFAULT 'api',
    file_basename VARCHAR(100),
    file_status VARCHAR(20) DEFAULT 'received',
    pdf_file_path VARCHAR(500),
    xml_file_path VARCHAR(500),
    isdoc_xml TEXT,

    -- Matching štatistiky
    item_count INTEGER DEFAULT 0,
    items_matched INTEGER DEFAULT 0,
    match_percent DECIMAL(5,2) DEFAULT 0,

    -- Validácia a status
    status VARCHAR(20) DEFAULT 'pending',
    validation_status VARCHAR(20) DEFAULT 'pending',
    validation_errors JSONB,

    -- Časové značky
    fetched_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Unikátny constraint
    CONSTRAINT uq_supplier_invoice UNIQUE (xml_supplier_ico, xml_invoice_number)
);

-- Indexy pre supplier_invoice_heads
CREATE INDEX IF NOT EXISTS idx_sih_customer_code ON supplier_invoice_heads(customer_code);
CREATE INDEX IF NOT EXISTS idx_sih_supplier_code ON supplier_invoice_heads(supplier_code);
CREATE INDEX IF NOT EXISTS idx_sih_supplier_ico ON supplier_invoice_heads(xml_supplier_ico);
CREATE INDEX IF NOT EXISTS idx_sih_invoice_number ON supplier_invoice_heads(xml_invoice_number);
CREATE INDEX IF NOT EXISTS idx_sih_status ON supplier_invoice_heads(status);
CREATE INDEX IF NOT EXISTS idx_sih_validation_status ON supplier_invoice_heads(validation_status);
CREATE INDEX IF NOT EXISTS idx_sih_file_status ON supplier_invoice_heads(file_status);
CREATE INDEX IF NOT EXISTS idx_sih_issue_date ON supplier_invoice_heads(xml_issue_date);
CREATE INDEX IF NOT EXISTS idx_sih_created_at ON supplier_invoice_heads(created_at);

-- Trigger pre updated_at
DROP TRIGGER IF EXISTS trg_sih_updated_at ON supplier_invoice_heads;
CREATE TRIGGER trg_sih_updated_at
    BEFORE UPDATE ON supplier_invoice_heads
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- ============================================================================
-- SUPPLIER_INVOICE_ITEMS - Položky dodávateľských faktúr
-- ============================================================================
CREATE TABLE IF NOT EXISTS supplier_invoice_items (
    id SERIAL PRIMARY KEY,
    head_id INTEGER NOT NULL REFERENCES supplier_invoice_heads(id) ON DELETE CASCADE,

    -- XML/ISDOC polia (prefix xml_)
    xml_line_number INTEGER,
    xml_seller_code VARCHAR(50),
    xml_ean VARCHAR(20),
    xml_product_name VARCHAR(255),
    xml_quantity DECIMAL(12,4) NOT NULL DEFAULT 0,
    xml_unit VARCHAR(10) DEFAULT 'PCE',
    xml_unit_price DECIMAL(12,4) NOT NULL DEFAULT 0,
    xml_unit_price_vat DECIMAL(12,4),
    xml_total_price DECIMAL(12,4) NOT NULL DEFAULT 0,
    xml_total_price_vat DECIMAL(12,4),
    xml_vat_rate DECIMAL(5,2) DEFAULT 20,

    -- NEX Genesis polia (prefix nex_)
    nex_product_id INTEGER,
    nex_product_modify_id INTEGER,
    nex_product_name VARCHAR(255),
    nex_product_category_id INTEGER,
    nex_ean VARCHAR(20),
    nex_plu INTEGER,
    nex_stock_code VARCHAR(50),
    nex_stock_id INTEGER,
    nex_facility_id INTEGER,
    nex_purchase_price DECIMAL(12,4),
    nex_sales_price DECIMAL(12,4),
    nex_category INTEGER,
    nex_name VARCHAR(255),
    in_nex BOOLEAN DEFAULT FALSE,

    -- Matching informácie
    matched BOOLEAN DEFAULT FALSE,
    matched_by VARCHAR(20),
    match_confidence DECIMAL(5,2),
    match_attempts INTEGER DEFAULT 0,
    matched_at TIMESTAMP WITH TIME ZONE,
    matched_by_user VARCHAR(50),

    -- Editované hodnoty (operátor)
    edited_product_name VARCHAR(255),
    edited_quantity DECIMAL(12,4),
    edited_unit_price DECIMAL(12,4),

    -- Časové značky
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexy pre supplier_invoice_items
CREATE INDEX IF NOT EXISTS idx_sii_head_id ON supplier_invoice_items(head_id);
CREATE INDEX IF NOT EXISTS idx_sii_ean ON supplier_invoice_items(xml_ean);
CREATE INDEX IF NOT EXISTS idx_sii_seller_code ON supplier_invoice_items(xml_seller_code);
CREATE INDEX IF NOT EXISTS idx_sii_nex_product_id ON supplier_invoice_items(nex_product_id);
CREATE INDEX IF NOT EXISTS idx_sii_nex_plu ON supplier_invoice_items(nex_plu);
CREATE INDEX IF NOT EXISTS idx_sii_matched ON supplier_invoice_items(matched);
CREATE INDEX IF NOT EXISTS idx_sii_in_nex ON supplier_invoice_items(in_nex);

-- Trigger pre updated_at
DROP TRIGGER IF EXISTS trg_sii_updated_at ON supplier_invoice_items;
CREATE TRIGGER trg_sii_updated_at
    BEFORE UPDATE ON supplier_invoice_items
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- ============================================================================
-- TRIGGER: Automatická aktualizácia štatistík v hlavičke
-- ============================================================================
CREATE OR REPLACE FUNCTION update_invoice_head_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE supplier_invoice_heads
    SET
        item_count = (SELECT COUNT(*) FROM supplier_invoice_items WHERE head_id = COALESCE(NEW.head_id, OLD.head_id)),
        items_matched = (SELECT COUNT(*) FROM supplier_invoice_items WHERE head_id = COALESCE(NEW.head_id, OLD.head_id) AND matched = TRUE),
        match_percent = (
            SELECT CASE
                WHEN COUNT(*) > 0 THEN ROUND(COUNT(*) FILTER (WHERE matched = TRUE) * 100.0 / COUNT(*), 2)
                ELSE 0
            END
            FROM supplier_invoice_items
            WHERE head_id = COALESCE(NEW.head_id, OLD.head_id)
        )
    WHERE id = COALESCE(NEW.head_id, OLD.head_id);

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_update_head_stats ON supplier_invoice_items;
CREATE TRIGGER trg_update_head_stats
    AFTER INSERT OR UPDATE OR DELETE ON supplier_invoice_items
    FOR EACH ROW EXECUTE FUNCTION update_invoice_head_stats();

-- ============================================================================
-- KOMENTÁRE
-- ============================================================================
COMMENT ON TABLE supplier_invoice_heads IS 'Hlavičky dodávateľských faktúr - staging pre NEX Genesis import';
COMMENT ON TABLE supplier_invoice_items IS 'Položky dodávateľských faktúr s product matching';

COMMENT ON COLUMN supplier_invoice_heads.status IS 'pending|validated|approved|rejected|imported|error';
COMMENT ON COLUMN supplier_invoice_heads.validation_status IS 'pending|valid|invalid';
COMMENT ON COLUMN supplier_invoice_heads.file_status IS 'received|staged|archived';
COMMENT ON COLUMN supplier_invoice_items.matched_by IS 'ean|seller_code|name|manual';
