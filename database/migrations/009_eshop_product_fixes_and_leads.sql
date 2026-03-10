-- ============================================================
-- 009: ESHOP Product Fixes + Lead Capture
-- ============================================================

-- A1: Oprav DPH sadzbu v tenantoch (20% → 23%)
UPDATE eshop_tenants SET vat_rate_default = 23.00;

-- A2: Oprav produkty — oba tenanty
UPDATE eshop_products
SET name = 'Oasis EM-1 - 500ml',
    description = 'Koncentrát efektívnych mikroorganizmov, 500ml balenie. Pôdna pomocná látka certifikovaná ÚKSÚP.',
    price = ROUND(9.90 / 1.23, 2),
    price_vat = 9.90,
    vat_rate = 23.00
WHERE sku = 'EM-500';

UPDATE eshop_products SET is_active = false WHERE sku = 'EM-5L';

INSERT INTO eshop_products (tenant_id, sku, name, description, price, price_vat, vat_rate, stock_quantity, barcode, is_active)
SELECT tenant_id, 'EM-500-3PACK', 'Oasis EM-1 - Akcia 2+1 zadarmo',
       '3x 500ml balenie za cenu dvoch. Koncentrát efektívnych mikroorganizmov certifikovaný ÚKSÚP.',
       ROUND(19.80 / 1.23, 2), 19.80, 23.00, 50, '8588000000003', true
FROM eshop_tenants WHERE is_active = true;

-- A3: Lead Capture tabuľka
CREATE TABLE eshop_leads (
    lead_id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES eshop_tenants(tenant_id),
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(50),
    discount_code VARCHAR(50) NOT NULL UNIQUE,
    discount_percentage NUMERIC(5,2) NOT NULL DEFAULT 50.00,
    registered_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    first_order_id INTEGER REFERENCES eshop_orders(order_id),
    reminder_count INTEGER NOT NULL DEFAULT 0,
    last_reminder_at TIMESTAMP WITH TIME ZONE,
    gdpr_consent BOOLEAN NOT NULL DEFAULT false,
    gdpr_consent_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_lead_tenant_email UNIQUE (tenant_id, email)
);

CREATE INDEX idx_eshop_leads_tenant ON eshop_leads(tenant_id);
CREATE INDEX idx_eshop_leads_email ON eshop_leads(email);
CREATE INDEX idx_eshop_leads_discount_code ON eshop_leads(discount_code);
CREATE INDEX idx_eshop_leads_expires ON eshop_leads(expires_at) WHERE is_active = true;

CREATE TRIGGER eshop_leads_update_timestamp
    BEFORE UPDATE ON eshop_leads
    FOR EACH ROW
    EXECUTE FUNCTION eshop_update_timestamp();
