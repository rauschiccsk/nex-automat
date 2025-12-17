"""
Script: Recreate schema with proper UTF-8 encoding
Run from: C:/Development/nex-automat
"""
from pathlib import Path

SCHEMA_PATH = Path(r"C:/Development/nex-automat/apps/supplier-invoice-staging/database/schemas/001_staging_schema.sql")

# Schema without Slovak diacritics in comments
SCHEMA_SQL = '''-- =====================================================
-- SUPPLIER INVOICE STAGING - Database Schema
-- Database: supplier_invoice_staging
-- Version: 1.0
-- =====================================================

-- Invoice headers (READ-ONLY in GUI)
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,

    -- Supplier
    supplier_ico VARCHAR(20) NOT NULL,
    supplier_name VARCHAR(255),
    supplier_dic VARCHAR(20),

    -- Invoice
    invoice_number VARCHAR(50) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE,
    variable_symbol VARCHAR(20),

    -- Amounts (from XML)
    total_without_vat DECIMAL(15,2),
    total_vat DECIMAL(15,2),
    total_amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',

    -- Files
    xml_path VARCHAR(500),
    pdf_path VARCHAR(500),
    isdoc_xml TEXT,

    -- Workflow status
    status VARCHAR(20) DEFAULT 'pending',

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    exported_at TIMESTAMP,

    CONSTRAINT uq_invoice UNIQUE (supplier_ico, invoice_number)
);

CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_supplier ON invoices(supplier_ico);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);

-- Invoice items (EDITABLE margin/selling_price)
CREATE TABLE invoice_items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    line_number INTEGER NOT NULL,

    -- XML DATA (IMMUTABLE)
    xml_ean VARCHAR(50),
    xml_name VARCHAR(255) NOT NULL,
    xml_quantity DECIMAL(15,3) NOT NULL,
    xml_unit VARCHAR(20),
    xml_unit_price DECIMAL(15,4) NOT NULL,
    xml_total_price DECIMAL(15,2),
    xml_vat_rate DECIMAL(5,2),

    -- NEX GENESIS ENRICHMENT
    nex_product_id INTEGER,
    nex_product_name VARCHAR(255),
    nex_ean VARCHAR(50),
    nex_mglst_code VARCHAR(10),
    in_nex BOOLEAN DEFAULT FALSE,
    matched_by VARCHAR(20),
    match_confidence DECIMAL(5,2),

    -- EDITABLE FIELDS
    edited_name VARCHAR(255),
    edited_unit_price DECIMAL(15,4),

    -- MARGIN AND SELLING PRICE
    margin_percent DECIMAL(5,2) DEFAULT 0,
    selling_price_excl_vat DECIMAL(15,4),
    selling_price_incl_vat DECIMAL(15,4),

    -- CALCULATED FIELDS
    final_unit_price DECIMAL(15,4),
    final_total_price DECIMAL(15,2),

    -- WORKFLOW
    item_status VARCHAR(20) DEFAULT 'pending',
    validation_errors TEXT,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_invoice_line UNIQUE (invoice_id, line_number)
);

CREATE INDEX idx_items_invoice ON invoice_items(invoice_id);
CREATE INDEX idx_items_status ON invoice_items(item_status);
CREATE INDEX idx_items_ean ON invoice_items(xml_ean);
CREATE INDEX idx_items_nex_product ON invoice_items(nex_product_id);

-- TRIGGER: Auto-update updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_invoices_updated
    BEFORE UPDATE ON invoices
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER tr_items_updated
    BEFORE UPDATE ON invoice_items
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- TRIGGER: Auto-calculate selling prices
CREATE OR REPLACE FUNCTION calculate_selling_price()
RETURNS TRIGGER AS $$
BEGIN
    NEW.final_unit_price = COALESCE(NEW.edited_unit_price, NEW.xml_unit_price);
    NEW.final_total_price = NEW.final_unit_price * NEW.xml_quantity;

    IF NEW.margin_percent IS NOT NULL AND NEW.margin_percent > 0 THEN
        NEW.selling_price_excl_vat = NEW.final_unit_price * (1 + NEW.margin_percent / 100);
        NEW.selling_price_incl_vat = NEW.selling_price_excl_vat * (1 + COALESCE(NEW.xml_vat_rate, 20) / 100);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_items_calc_price
    BEFORE INSERT OR UPDATE ON invoice_items
    FOR EACH ROW EXECUTE FUNCTION calculate_selling_price();

-- VIEW: Invoice summary for GUI
CREATE VIEW v_invoice_summary AS
SELECT 
    i.id,
    i.supplier_name,
    i.invoice_number,
    i.invoice_date,
    i.total_amount,
    i.currency,
    i.status,
    COUNT(it.id) AS item_count,
    SUM(CASE WHEN it.in_nex THEN 1 ELSE 0 END) AS matched_count,
    SUM(CASE WHEN it.margin_percent > 0 THEN 1 ELSE 0 END) AS priced_count,
    ROUND(100.0 * SUM(CASE WHEN it.in_nex THEN 1 ELSE 0 END) / NULLIF(COUNT(it.id), 0), 1) AS match_percent
FROM invoices i
LEFT JOIN invoice_items it ON i.id = it.invoice_id
GROUP BY i.id;
'''


def main():
    SCHEMA_PATH.write_text(SCHEMA_SQL, encoding='utf-8')
    print(f"Schema saved: {SCHEMA_PATH}")
    print()
    print("Run these commands:")
    print('  psql -U postgres -c "DROP DATABASE IF EXISTS supplier_invoice_staging;"')
    print('  psql -U postgres -c "CREATE DATABASE supplier_invoice_staging;"')
    print(f'  psql -U postgres -d supplier_invoice_staging -f "{SCHEMA_PATH}"')


if __name__ == "__main__":
    main()