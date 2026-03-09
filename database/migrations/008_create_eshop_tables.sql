-- ============================================================================
-- ESHOP Modul — DB Schéma (multi-tenant)
-- Migrácia: 008_create_eshop_tables.sql
-- ============================================================================

-- 1. TENANTS
CREATE TABLE eshop_tenants (
    tenant_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    partner_id INTEGER REFERENCES partner_catalog(partner_id),
    domain VARCHAR(255) UNIQUE NOT NULL,
    brand_name VARCHAR(255) NOT NULL,
    logo_url VARCHAR(500),
    primary_color VARCHAR(7) DEFAULT '#2E7D32',
    api_token VARCHAR(255) UNIQUE NOT NULL,
    comgate_merchant_id VARCHAR(50),
    comgate_secret VARCHAR(255),
    comgate_test_mode BOOLEAN DEFAULT TRUE,
    fulfillment_provider VARCHAR(50) DEFAULT 'fullpost',
    mufis_api_key VARCHAR(255),
    mufis_webhook_url VARCHAR(500),
    smtp_from VARCHAR(255),
    admin_email VARCHAR(255),
    currency VARCHAR(3) DEFAULT 'EUR',
    vat_rate_default DECIMAL(5,2) DEFAULT 20.00,
    default_lang VARCHAR(2) DEFAULT 'sk',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. PRODUCTS
CREATE TABLE eshop_products (
    product_id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES eshop_tenants(tenant_id),
    sku VARCHAR(50) NOT NULL,
    barcode VARCHAR(50),
    name VARCHAR(255) NOT NULL,
    short_description VARCHAR(500),
    description TEXT,
    image_url VARCHAR(500),
    price DECIMAL(10,2) NOT NULL,
    price_vat DECIMAL(10,2) NOT NULL,
    vat_rate DECIMAL(5,2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    weight DECIMAL(8,3),
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tenant_id, sku)
);

CREATE INDEX idx_eshop_products_tenant ON eshop_products(tenant_id);
CREATE INDEX idx_eshop_products_sku ON eshop_products(tenant_id, sku);
CREATE INDEX idx_eshop_products_active ON eshop_products(tenant_id, is_active);

-- 3. ORDERS
CREATE TABLE eshop_orders (
    order_id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES eshop_tenants(tenant_id),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(50),
    lang VARCHAR(2) DEFAULT 'sk',
    billing_name VARCHAR(255) NOT NULL,
    billing_name2 VARCHAR(255) DEFAULT '',
    billing_street VARCHAR(255) NOT NULL,
    billing_city VARCHAR(255) NOT NULL,
    billing_zip VARCHAR(20) NOT NULL,
    billing_country VARCHAR(2) NOT NULL DEFAULT 'SK',
    shipping_name VARCHAR(255) DEFAULT '',
    shipping_name2 VARCHAR(255) DEFAULT '',
    shipping_street VARCHAR(255) DEFAULT '',
    shipping_city VARCHAR(255) DEFAULT '',
    shipping_zip VARCHAR(20) DEFAULT '',
    shipping_country VARCHAR(2) DEFAULT '',
    ico VARCHAR(20) DEFAULT '',
    dic VARCHAR(20) DEFAULT '',
    eu_vat_number VARCHAR(30) DEFAULT '',
    total_amount DECIMAL(10,2) NOT NULL,
    total_amount_vat DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'EUR',
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'pending',
    comgate_transaction_id VARCHAR(255),
    shipping_type VARCHAR(100) DEFAULT '',
    shipping_price DECIMAL(10,2) DEFAULT 0,
    delivery_point_group VARCHAR(50) DEFAULT '',
    delivery_point_id VARCHAR(100) DEFAULT '',
    tracking_number VARCHAR(500) DEFAULT '',
    tracking_link VARCHAR(500) DEFAULT '',
    multiple_packages BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'new',
    note TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_eshop_orders_tenant ON eshop_orders(tenant_id);
CREATE INDEX idx_eshop_orders_status ON eshop_orders(tenant_id, status);
CREATE INDEX idx_eshop_orders_number ON eshop_orders(order_number);
CREATE INDEX idx_eshop_orders_email ON eshop_orders(tenant_id, customer_email);
CREATE INDEX idx_eshop_orders_updated ON eshop_orders(updated_at DESC);
CREATE INDEX idx_eshop_orders_created ON eshop_orders(created_at DESC);

-- 4. ORDER ITEMS
CREATE TABLE eshop_order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES eshop_orders(order_id),
    product_id INTEGER REFERENCES eshop_products(product_id),
    sku VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    unit_price_vat DECIMAL(10,2) NOT NULL,
    vat_rate DECIMAL(5,2) NOT NULL,
    item_type VARCHAR(20) DEFAULT 'product'
);

CREATE INDEX idx_eshop_order_items_order ON eshop_order_items(order_id);

-- 5. ORDER STATUS HISTORY
CREATE TABLE eshop_order_status_history (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES eshop_orders(order_id),
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by VARCHAR(100),
    note TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_eshop_status_history_order ON eshop_order_status_history(order_id);

-- 6. TRIGGERS — auto-update updated_at
CREATE OR REPLACE FUNCTION eshop_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_eshop_tenants_updated
    BEFORE UPDATE ON eshop_tenants
    FOR EACH ROW EXECUTE FUNCTION eshop_update_timestamp();

CREATE TRIGGER trg_eshop_products_updated
    BEFORE UPDATE ON eshop_products
    FOR EACH ROW EXECUTE FUNCTION eshop_update_timestamp();

CREATE TRIGGER trg_eshop_orders_updated
    BEFORE UPDATE ON eshop_orders
    FOR EACH ROW EXECUTE FUNCTION eshop_update_timestamp();

-- 7. SEED DATA — ICC tenant (emcenter.sk)
INSERT INTO eshop_tenants (
    company_name, domain, brand_name, api_token,
    smtp_from, admin_email, currency, vat_rate_default, default_lang
) VALUES (
    'ICC s.r.o.',
    'emcenter.sk',
    'EM Center',
    'PUwzJQI-zB4tVrdUvjUJyuntN-SaFlRaZ_ZPopIb1ZU',
    'noreply@emcenter.sk',
    'odbyt@em-1.sk',
    'EUR',
    20.00,
    'sk'
);

INSERT INTO eshop_products (tenant_id, sku, name, short_description, price, price_vat, vat_rate, stock_quantity, is_active, sort_order)
VALUES
    (1, 'EM-500', 'OASIS EM-1 500ml', 'Trial balenie efektívnych mikroorganizmov', 8.25, 9.90, 20.00, 0, TRUE, 1),
    (1, 'EM-5L',  'OASIS EM-1 5L',    'Odporúčané balenie efektívnych mikroorganizmov', 33.25, 39.90, 20.00, 0, TRUE, 2);
