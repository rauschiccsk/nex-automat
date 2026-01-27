-- ANDROS Invoice Worker - Database Schema
-- Tables for storing supplier invoices

-- Invoice headers table
CREATE TABLE IF NOT EXISTS supplier_invoice_heads (
    id SERIAL PRIMARY KEY,

    -- Customer/Supplier identification
    customer_code VARCHAR(50) NOT NULL,          -- e.g., 'ANDROS'
    supplier_code VARCHAR(50) NOT NULL,          -- e.g., 'MARSO'
    supplier_id VARCHAR(50) NOT NULL,            -- e.g., 'marso'
    supplier_name VARCHAR(255),

    -- Invoice identification
    invoice_number VARCHAR(100) NOT NULL,
    external_invoice_id VARCHAR(100),

    -- Dates
    invoice_date TIMESTAMP,
    due_date TIMESTAMP,
    delivery_date TIMESTAMP,

    -- Amounts
    total_without_vat DECIMAL(15, 2),
    total_vat DECIMAL(15, 2),
    total_with_vat DECIMAL(15, 2),
    currency VARCHAR(3) DEFAULT 'EUR',

    -- Source and status
    source_type VARCHAR(20) DEFAULT 'api',       -- 'api' or 'pdf'
    status VARCHAR(50) DEFAULT 'pending',        -- pending, processed, acknowledged, error

    -- Supplier details
    supplier_ico VARCHAR(50),
    supplier_dic VARCHAR(50),
    supplier_ic_dph VARCHAR(50),

    -- Timestamps
    fetched_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,

    -- Unique constraint to prevent duplicates
    UNIQUE (customer_code, supplier_code, invoice_number)
);

-- Invoice items table
CREATE TABLE IF NOT EXISTS supplier_invoice_items (
    id SERIAL PRIMARY KEY,
    head_id INTEGER NOT NULL REFERENCES supplier_invoice_heads(id) ON DELETE CASCADE,

    -- Line identification
    line_number INTEGER NOT NULL,

    -- Product identification
    product_code VARCHAR(100),
    product_code_type VARCHAR(50),               -- 'ean', 'marso_code', etc.
    product_name VARCHAR(500),

    -- Quantities and prices
    quantity DECIMAL(15, 4),
    unit VARCHAR(20),
    unit_price DECIMAL(15, 4),
    total_price DECIMAL(15, 2),
    vat_rate DECIMAL(5, 2),
    vat_amount DECIMAL(15, 2),

    -- Alternative codes
    ean VARCHAR(50),
    supplier_product_code VARCHAR(100),

    -- NEX Genesis mapping (filled after product matching)
    nex_product_id VARCHAR(50),
    nex_product_code VARCHAR(100),
    match_confidence DECIMAL(5, 2),

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),

    -- Index for fast lookup
    UNIQUE (head_id, line_number)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_heads_customer_supplier
    ON supplier_invoice_heads(customer_code, supplier_code);

CREATE INDEX IF NOT EXISTS idx_heads_invoice_number
    ON supplier_invoice_heads(invoice_number);

CREATE INDEX IF NOT EXISTS idx_heads_status
    ON supplier_invoice_heads(status);

CREATE INDEX IF NOT EXISTS idx_heads_invoice_date
    ON supplier_invoice_heads(invoice_date);

CREATE INDEX IF NOT EXISTS idx_items_head_id
    ON supplier_invoice_items(head_id);

CREATE INDEX IF NOT EXISTS idx_items_product_code
    ON supplier_invoice_items(product_code);

CREATE INDEX IF NOT EXISTS idx_items_ean
    ON supplier_invoice_items(ean);

-- Comments
COMMENT ON TABLE supplier_invoice_heads IS 'Invoice headers from supplier APIs (MARSO, etc.)';
COMMENT ON TABLE supplier_invoice_items IS 'Invoice line items with product details';
COMMENT ON COLUMN supplier_invoice_heads.customer_code IS 'Customer identifier (e.g., ANDROS)';
COMMENT ON COLUMN supplier_invoice_heads.supplier_code IS 'Supplier identifier (e.g., MARSO)';
COMMENT ON COLUMN supplier_invoice_items.match_confidence IS 'Confidence score from product matching (0-100)';
