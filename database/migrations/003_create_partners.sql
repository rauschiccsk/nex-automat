-- Migration 003: Partners table for PAB module
-- Business partner catalog (suppliers, customers)
--
-- Conventions (from ARCHITECTURE.md / RAG Knowledge Base):
--   PK: UUID (gen_random_uuid)
--   Codes: *_code VARCHAR, unique
--   Names: *_name VARCHAR
--   Booleans: is_* DEFAULT true/false
--   Timestamps: *_at TIMESTAMPTZ DEFAULT NOW()
--   Audit: created_at, created_by, updated_at, updated_by VARCHAR(50)
--   Soft delete: is_active BOOLEAN DEFAULT true
--   Addresses: street VARCHAR(100), city VARCHAR(100), zip_code VARCHAR(20), country_code VARCHAR(2)

BEGIN;

CREATE TABLE IF NOT EXISTS partners (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code                VARCHAR(30)  NOT NULL UNIQUE,
    name                VARCHAR(100) NOT NULL,

    -- Typ partnera (boolean flags per RAG: is_supplier, is_customer)
    partner_type        VARCHAR(20)  NOT NULL DEFAULT 'customer'
                        CHECK (partner_type IN ('customer', 'supplier', 'both')),
    is_supplier         BOOLEAN      NOT NULL DEFAULT false,
    is_customer         BOOLEAN      NOT NULL DEFAULT true,

    -- Identifikácia (RAG naming: company_id, tax_id, vat_id)
    company_id          VARCHAR(20),     -- IČO
    tax_id              VARCHAR(20),     -- DIČ
    vat_id              VARCHAR(20),     -- IČ DPH
    is_vat_payer        BOOLEAN      NOT NULL DEFAULT false,

    -- Sídlo (RAG standard: street/city/zip_code/country_code)
    street              VARCHAR(100),
    city                VARCHAR(100),
    zip_code            VARCHAR(20),
    country_code        VARCHAR(2)   DEFAULT 'SK',

    -- Fakturačná adresa
    billing_street      VARCHAR(100),
    billing_city        VARCHAR(100),
    billing_zip_code    VARCHAR(20),
    billing_country_code VARCHAR(2),

    -- Dodacia adresa
    shipping_street     VARCHAR(100),
    shipping_city       VARCHAR(100),
    shipping_zip_code   VARCHAR(20),
    shipping_country_code VARCHAR(2),

    -- Kontakt
    phone               VARCHAR(50),
    mobile              VARCHAR(50),
    email               VARCHAR(255),
    website             VARCHAR(255),
    contact_person      VARCHAR(255),

    -- Obchodné podmienky
    payment_due_days    INTEGER      DEFAULT 14,
    credit_limit        NUMERIC(15, 2) DEFAULT 0,
    discount_percent    NUMERIC(5, 2)  DEFAULT 0,
    price_category      VARCHAR(50),
    payment_method      VARCHAR(50)  DEFAULT 'transfer'
                        CHECK (payment_method IN ('transfer', 'cash', 'cod')),
    currency            VARCHAR(3)   DEFAULT 'EUR',

    -- Banka (RAG naming: iban_code → kept as iban for simplicity in this module)
    iban                VARCHAR(34),
    bank_name           VARCHAR(255),
    swift_bic           VARCHAR(11),

    -- Poznámky
    notes               TEXT,

    -- System
    is_active           BOOLEAN      NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by          VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by          VARCHAR(50)  NOT NULL DEFAULT 'system'
);

-- Indexes
CREATE INDEX idx_partners_code       ON partners(code);
CREATE INDEX idx_partners_name       ON partners(name);
CREATE INDEX idx_partners_company_id ON partners(company_id);
CREATE INDEX idx_partners_type       ON partners(partner_type);
CREATE INDEX idx_partners_active     ON partners(is_active);
CREATE INDEX idx_partners_city       ON partners(city);

-- Trigger: auto-update updated_at (reuses existing function from 001)
CREATE TRIGGER set_updated_at_partners BEFORE UPDATE ON partners
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

COMMIT;
