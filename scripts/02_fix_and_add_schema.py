"""
Script: Add database schema to supplier-invoice-staging
Run from: C:/Development/nex-automat
"""
from pathlib import Path

APP_ROOT = Path(r"C:/Development/nex-automat/apps/supplier-invoice-staging")

SCHEMA_SQL = '''-- =====================================================
-- SUPPLIER INVOICE STAGING - Database Schema
-- Database: supplier_invoice_staging
-- Version: 1.0
-- =====================================================

-- Hlavičky faktúr (READ-ONLY v GUI)
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,

    -- Dodávateľ
    supplier_ico VARCHAR(20) NOT NULL,
    supplier_name VARCHAR(255),
    supplier_dic VARCHAR(20),

    -- Faktúra
    invoice_number VARCHAR(50) NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE,
    variable_symbol VARCHAR(20),

    -- Sumy (z XML)
    total_without_vat DECIMAL(15,2),
    total_vat DECIMAL(15,2),
    total_amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',

    -- Súbory
    xml_path VARCHAR(500),
    pdf_path VARCHAR(500),
    isdoc_xml TEXT,

    -- Workflow status
    status VARCHAR(20) DEFAULT 'pending',
    -- pending -> processing -> matched -> exported -> error

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    exported_at TIMESTAMP,

    -- Unikátnosť: dodávateľ + číslo faktúry
    CONSTRAINT uq_invoice UNIQUE (supplier_ico, invoice_number)
);

-- Index pre rýchle vyhľadávanie
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_supplier ON invoices(supplier_ico);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);

-- Položky faktúr (EDITOVATEĽNÉ margin/selling_price)
CREATE TABLE invoice_items (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
    line_number INTEGER NOT NULL,

    -- ========== XML DÁTA (IMMUTABLE) ==========
    xml_ean VARCHAR(50),
    xml_name VARCHAR(255) NOT NULL,
    xml_quantity DECIMAL(15,3) NOT NULL,
    xml_unit VARCHAR(20),
    xml_unit_price DECIMAL(15,4) NOT NULL,  -- NC/MJ bez DPH
    xml_total_price DECIMAL(15,2),          -- NC celkom bez DPH
    xml_vat_rate DECIMAL(5,2),

    -- ========== NEX GENESIS ENRICHMENT ==========
    nex_product_id INTEGER,           -- GSCAT.GsCode
    nex_product_name VARCHAR(255),    -- GSCAT.GsName
    nex_ean VARCHAR(50),              -- GSCAT EAN
    nex_mglst_code VARCHAR(10),       -- Kategória
    in_nex BOOLEAN DEFAULT FALSE,
    matched_by VARCHAR(20),           -- 'ean', 'name', 'manual', NULL
    match_confidence DECIMAL(5,2),    -- 0-100%

    -- ========== EDITOVATEĽNÉ POLIA ==========
    edited_name VARCHAR(255),         -- Upravený názov
    edited_unit_price DECIMAL(15,4),  -- Upravená NC

    -- MARŽA A PREDAJNÁ CENA (hlavný účel aplikácie)
    margin_percent DECIMAL(5,2) DEFAULT 0,       -- Obchodná marža %
    selling_price_excl_vat DECIMAL(15,4),        -- PC bez DPH
    selling_price_incl_vat DECIMAL(15,4),        -- PC s DPH

    -- ========== VYPOČÍTANÉ POLIA ==========
    final_unit_price DECIMAL(15,4),   -- COALESCE(edited, xml)
    final_total_price DECIMAL(15,2),  -- final_unit_price * quantity

    -- ========== WORKFLOW ==========
    item_status VARCHAR(20) DEFAULT 'pending',
    -- pending -> matched -> priced -> exported -> error
    validation_errors TEXT,

    -- Audit
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_invoice_line UNIQUE (invoice_id, line_number)
);

-- Indexy pre položky
CREATE INDEX idx_items_invoice ON invoice_items(invoice_id);
CREATE INDEX idx_items_status ON invoice_items(item_status);
CREATE INDEX idx_items_ean ON invoice_items(xml_ean);
CREATE INDEX idx_items_nex_product ON invoice_items(nex_product_id);

-- =====================================================
-- TRIGGER: Auto-update updated_at
-- =====================================================
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

-- =====================================================
-- TRIGGER: Auto-calculate selling prices
-- =====================================================
CREATE OR REPLACE FUNCTION calculate_selling_price()
RETURNS TRIGGER AS $$
BEGIN
    -- Final unit price = edited alebo xml
    NEW.final_unit_price = COALESCE(NEW.edited_unit_price, NEW.xml_unit_price);

    -- Final total = unit * quantity
    NEW.final_total_price = NEW.final_unit_price * NEW.xml_quantity;

    -- Ak je zadaná marža, vypočítaj PC
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

-- =====================================================
-- VIEW: Invoice summary pre GUI
-- =====================================================
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
    schema_path = APP_ROOT / "database" / "schemas" / "001_staging_schema.sql"
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path.write_text(SCHEMA_SQL, encoding='utf-8')
    print(f"✅ Created: {schema_path}")

    print(f"\nNext steps:")
    print(f"  1. Create database:")
    print(f"     psql -U postgres -c \"CREATE DATABASE supplier_invoice_staging;\"")
    print(f"  2. Run schema:")
    print(f"     psql -U postgres -d supplier_invoice_staging -f \"{schema_path}\"")
    print(f"  3. Set environment variable:")
    print(f"     $env:POSTGRES_PASSWORD = 'your_password'")
    print(f"  4. Install shared-pyside6:")
    print(f"     pip install -e packages/shared-pyside6")
    print(f"  5. Run application:")
    print(f"     cd apps/supplier-invoice-staging")
    print(f"     python -m supplier_invoice_staging")


if __name__ == "__main__":
    main()