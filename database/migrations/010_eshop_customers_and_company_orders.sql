-- Migration 010: Eshop customers table + company order fields
-- Ri approved: 2026-03-11

-- 1. New table: eshop_customers
CREATE TABLE eshop_customers (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES eshop_tenants(tenant_id),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    street VARCHAR(255),
    city VARCHAR(100),
    postal_code VARCHAR(10),
    country VARCHAR(2) DEFAULT 'SK',
    is_company BOOLEAN DEFAULT FALSE,
    company_name VARCHAR(255),
    company_ico VARCHAR(20),
    company_dic VARCHAR(20),
    company_ic_dph VARCHAR(20),
    email_verified BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE UNIQUE INDEX idx_eshop_customers_tenant_email
    ON eshop_customers(tenant_id, email) WHERE is_active = TRUE;

CREATE TRIGGER eshop_customers_update_timestamp
    BEFORE UPDATE ON eshop_customers
    FOR EACH ROW
    EXECUTE FUNCTION eshop_update_timestamp();

-- 2. New columns on eshop_orders for company purchases
ALTER TABLE eshop_orders ADD COLUMN is_company_order BOOLEAN DEFAULT FALSE;
ALTER TABLE eshop_orders ADD COLUMN company_name VARCHAR(255);
ALTER TABLE eshop_orders ADD COLUMN company_ico VARCHAR(20);
ALTER TABLE eshop_orders ADD COLUMN company_dic VARCHAR(20);
ALTER TABLE eshop_orders ADD COLUMN company_ic_dph VARCHAR(20);
ALTER TABLE eshop_orders ADD COLUMN IF NOT EXISTS billing_street VARCHAR(255);
ALTER TABLE eshop_orders ADD COLUMN IF NOT EXISTS billing_city VARCHAR(100);
ALTER TABLE eshop_orders ADD COLUMN billing_postal_code VARCHAR(10);
ALTER TABLE eshop_orders ADD COLUMN IF NOT EXISTS billing_country VARCHAR(2) DEFAULT 'SK';
ALTER TABLE eshop_orders ADD COLUMN customer_id INTEGER REFERENCES eshop_customers(id);
