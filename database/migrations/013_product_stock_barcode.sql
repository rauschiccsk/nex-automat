-- Migration 013: Add stock_quantity and barcode to eshop_products
-- Required for MuFis API v1.2 getProduct/setProduct compliance

ALTER TABLE eshop_products
    ADD COLUMN IF NOT EXISTS stock_quantity INTEGER NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS barcode VARCHAR(100) DEFAULT NULL;
