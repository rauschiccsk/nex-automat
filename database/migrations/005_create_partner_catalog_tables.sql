-- Migration 005: Partner Catalog tables (8 tables)
-- Normalized partner catalog with child tables for extensions, addresses,
-- contacts, texts, bank accounts, facilities, and category mappings.
--
-- NOTE: Existing 'partners' table (migration 003) is NOT touched.
--       These are new partner_catalog_* tables for the full catalog module.
--
-- Conventions (from ARCHITECTURE.md / DATABASE_PRINCIPLES.md):
--   PK: partner_id INTEGER (business key from Btrieve, NOT auto-increment)
--   Child PK: SERIAL (auto-increment)
--   Audit: created_at, created_by, updated_at, updated_by VARCHAR(50)
--   Soft delete: is_active BOOLEAN DEFAULT true
--   Ref integrity: CASCADE for child tables
--   Trigger: trigger_set_updated_at() reused from migration 001

BEGIN;

-- ============================================================
-- 1. PARTNER_CATALOG — hlavné údaje partnera
-- ============================================================
CREATE TABLE IF NOT EXISTS partner_catalog (
    partner_id      INTEGER      PRIMARY KEY,
    partner_code    VARCHAR(30)  NOT NULL UNIQUE,
    partner_name    VARCHAR(100) NOT NULL,
    reg_name        VARCHAR(100),

    -- Identifikácia
    company_id      VARCHAR(20),          -- IČO
    tax_id          VARCHAR(20),          -- DIČ
    vat_id          VARCHAR(20),          -- IČ DPH
    is_vat_payer    BOOLEAN      NOT NULL DEFAULT false,

    -- Typ partnera
    is_supplier     BOOLEAN      NOT NULL DEFAULT false,
    is_customer     BOOLEAN      NOT NULL DEFAULT true,

    -- Sídlo (registered address)
    street          VARCHAR(100),
    city            VARCHAR(100),
    zip_code        VARCHAR(20),
    country_code    VARCHAR(2)   DEFAULT 'SK',

    -- Denormalizované počítadlá
    bank_account_count INTEGER  NOT NULL DEFAULT 0,
    facility_count     INTEGER  NOT NULL DEFAULT 0,

    -- System
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50)  NOT NULL DEFAULT 'system'
);

CREATE INDEX idx_partner_catalog_code       ON partner_catalog(partner_code);
CREATE INDEX idx_partner_catalog_name       ON partner_catalog(partner_name);
CREATE INDEX idx_partner_catalog_company_id ON partner_catalog(company_id);
CREATE INDEX idx_partner_catalog_supplier   ON partner_catalog(is_supplier) WHERE is_supplier = true;
CREATE INDEX idx_partner_catalog_customer   ON partner_catalog(is_customer) WHERE is_customer = true;
CREATE INDEX idx_partner_catalog_active     ON partner_catalog(is_active);

CREATE TRIGGER set_updated_at_partner_catalog
    BEFORE UPDATE ON partner_catalog
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- ============================================================
-- 2. PARTNER_CATALOG_EXTENSIONS — rozšírené údaje (1:1)
-- ============================================================
CREATE TABLE IF NOT EXISTS partner_catalog_extensions (
    partner_id          INTEGER PRIMARY KEY
                        REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,

    -- Obchodné podmienky - predaj
    sale_payment_method_id    INTEGER,
    sale_transport_method_id  INTEGER,
    sale_payment_due_days     INTEGER      DEFAULT 14,
    sale_currency_code        VARCHAR(3)   DEFAULT 'EUR',
    sale_price_category       VARCHAR(50),
    sale_discount_percent     DECIMAL(5,2) DEFAULT 0,
    sale_credit_limit         DECIMAL(15,2) DEFAULT 0,

    -- Obchodné podmienky - nákup
    purchase_payment_method_id   INTEGER,
    purchase_transport_method_id INTEGER,
    purchase_payment_due_days    INTEGER      DEFAULT 14,
    purchase_currency_code       VARCHAR(3)   DEFAULT 'EUR',
    purchase_price_category      VARCHAR(50),
    purchase_discount_percent    DECIMAL(5,2) DEFAULT 0,

    -- Posledné transakcie (denormalizované)
    last_sale_date       DATE,
    last_purchase_date   DATE,

    -- System
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50)  NOT NULL DEFAULT 'system'
);

CREATE TRIGGER set_updated_at_partner_catalog_extensions
    BEFORE UPDATE ON partner_catalog_extensions
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- ============================================================
-- 3. PARTNER_CATALOG_CATEGORIES — mapovanie partner → skupiny (M:N)
-- ============================================================
CREATE TABLE IF NOT EXISTS partner_catalog_categories (
    id              SERIAL   PRIMARY KEY,
    partner_id      INTEGER  NOT NULL
                    REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    category_id     INTEGER  NOT NULL,
    category_type   VARCHAR(20) NOT NULL
                    CHECK (category_type IN ('supplier', 'customer')),

    -- System
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50)  NOT NULL DEFAULT 'system',

    UNIQUE (partner_id, category_id)
);

CREATE INDEX idx_pcc_partner_id  ON partner_catalog_categories(partner_id);
CREATE INDEX idx_pcc_category_id ON partner_catalog_categories(category_id);

CREATE TRIGGER set_updated_at_partner_catalog_categories
    BEFORE UPDATE ON partner_catalog_categories
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- ============================================================
-- 4. PARTNER_CATALOG_ADDRESSES — adresy (registered, correspondence, invoice)
-- ============================================================
CREATE TABLE IF NOT EXISTS partner_catalog_addresses (
    id              SERIAL       PRIMARY KEY,
    partner_id      INTEGER      NOT NULL
                    REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    address_type    VARCHAR(20)  NOT NULL
                    CHECK (address_type IN ('registered', 'correspondence', 'invoice')),

    street          VARCHAR(100),
    city            VARCHAR(100),
    zip_code        VARCHAR(20),
    country_code    VARCHAR(2)   DEFAULT 'SK',

    -- System
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50)  NOT NULL DEFAULT 'system',

    UNIQUE (partner_id, address_type)
);

CREATE INDEX idx_pca_partner_id ON partner_catalog_addresses(partner_id);

CREATE TRIGGER set_updated_at_partner_catalog_addresses
    BEFORE UPDATE ON partner_catalog_addresses
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- ============================================================
-- 5. PARTNER_CATALOG_CONTACTS — kontakty (univerzálna tabuľka)
-- ============================================================
CREATE TABLE IF NOT EXISTS partner_catalog_contacts (
    contact_id      SERIAL       PRIMARY KEY,
    partner_id      INTEGER      NOT NULL
                    REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    contact_type    VARCHAR(20)  NOT NULL
                    CHECK (contact_type IN ('address', 'person')),

    -- Osobné údaje
    title           VARCHAR(20),
    first_name      VARCHAR(50),
    last_name       VARCHAR(50),
    function_name   VARCHAR(100),

    -- Kontaktné údaje
    phone_work      VARCHAR(30),
    phone_mobile    VARCHAR(30),
    phone_private   VARCHAR(30),
    fax             VARCHAR(30),
    email           VARCHAR(100),

    -- Adresa (len ak contact_type='address')
    street          VARCHAR(100),
    city            VARCHAR(100),
    zip_code        VARCHAR(20),
    country_code    VARCHAR(2)   DEFAULT 'SK',

    -- System
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50)  NOT NULL DEFAULT 'system'
);

CREATE INDEX idx_pcct_partner_id   ON partner_catalog_contacts(partner_id);
CREATE INDEX idx_pcct_contact_type ON partner_catalog_contacts(contact_type);

CREATE TRIGGER set_updated_at_partner_catalog_contacts
    BEFORE UPDATE ON partner_catalog_contacts
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- ============================================================
-- 6. PARTNER_CATALOG_TEXTS — textové polia (univerzálna tabuľka)
-- ============================================================
CREATE TABLE IF NOT EXISTS partner_catalog_texts (
    text_id         SERIAL       PRIMARY KEY,
    partner_id      INTEGER      NOT NULL
                    REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,
    text_type       VARCHAR(20)  NOT NULL
                    CHECK (text_type IN ('owner_name', 'description', 'notice')),
    line_number     INTEGER      NOT NULL DEFAULT 1,
    language        VARCHAR(5)   NOT NULL DEFAULT 'sk',
    text_content    TEXT,

    -- System
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50)  NOT NULL DEFAULT 'system',

    UNIQUE (partner_id, text_type, line_number, language)
);

CREATE INDEX idx_pct_partner_id ON partner_catalog_texts(partner_id);
CREATE INDEX idx_pct_text_type  ON partner_catalog_texts(text_type);

CREATE TRIGGER set_updated_at_partner_catalog_texts
    BEFORE UPDATE ON partner_catalog_texts
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- ============================================================
-- 7. PARTNER_CATALOG_BANK_ACCOUNTS — bankové účty
-- ============================================================
CREATE TABLE IF NOT EXISTS partner_catalog_bank_accounts (
    account_id      SERIAL       PRIMARY KEY,
    partner_id      INTEGER      NOT NULL
                    REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,

    iban_code       VARCHAR(50),
    swift_code      VARCHAR(11),
    account_number  VARCHAR(30),
    bank_name       VARCHAR(100),
    bank_seat       VARCHAR(200),

    -- Variabilné symboly
    vs_sale         VARCHAR(20),
    vs_purchase     VARCHAR(20),

    is_primary      BOOLEAN      NOT NULL DEFAULT false,

    -- System
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50)  NOT NULL DEFAULT 'system'
);

CREATE INDEX idx_pcba_partner_id ON partner_catalog_bank_accounts(partner_id);
CREATE INDEX idx_pcba_iban       ON partner_catalog_bank_accounts(iban_code);

CREATE TRIGGER set_updated_at_partner_catalog_bank_accounts
    BEFORE UPDATE ON partner_catalog_bank_accounts
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- Trigger: ensure only one primary bank account per partner
CREATE OR REPLACE FUNCTION ensure_single_primary_bank_account()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_primary = true THEN
        UPDATE partner_catalog_bank_accounts
        SET is_primary = false
        WHERE partner_id = NEW.partner_id
          AND account_id != NEW.account_id
          AND is_primary = true;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_single_primary_bank_account
    BEFORE INSERT OR UPDATE ON partner_catalog_bank_accounts
    FOR EACH ROW EXECUTE FUNCTION ensure_single_primary_bank_account();

-- Trigger: update bank_account_count on partner_catalog
CREATE OR REPLACE FUNCTION update_partner_bank_account_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE partner_catalog
        SET bank_account_count = bank_account_count + 1
        WHERE partner_id = NEW.partner_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE partner_catalog
        SET bank_account_count = bank_account_count - 1
        WHERE partner_id = OLD.partner_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_partner_bank_account_count
    AFTER INSERT OR DELETE ON partner_catalog_bank_accounts
    FOR EACH ROW EXECUTE FUNCTION update_partner_bank_account_count();

-- ============================================================
-- 8. PARTNER_CATALOG_FACILITIES — prevádzkové jednotky
-- ============================================================
CREATE TABLE IF NOT EXISTS partner_catalog_facilities (
    facility_id     SERIAL       PRIMARY KEY,
    partner_id      INTEGER      NOT NULL
                    REFERENCES partner_catalog(partner_id) ON DELETE CASCADE,

    facility_name   VARCHAR(100) NOT NULL,
    street          VARCHAR(100),
    city            VARCHAR(100),
    zip_code        VARCHAR(20),
    country_code    VARCHAR(2)   DEFAULT 'SK',

    phone           VARCHAR(30),
    fax             VARCHAR(30),
    email           VARCHAR(100),

    transport_method_id INTEGER,

    -- System
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50)  NOT NULL DEFAULT 'system'
);

CREATE INDEX idx_pcf_partner_id ON partner_catalog_facilities(partner_id);

CREATE TRIGGER set_updated_at_partner_catalog_facilities
    BEFORE UPDATE ON partner_catalog_facilities
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- Trigger: update facility_count on partner_catalog
CREATE OR REPLACE FUNCTION update_partner_facility_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE partner_catalog
        SET facility_count = facility_count + 1
        WHERE partner_id = NEW.partner_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE partner_catalog
        SET facility_count = facility_count - 1
        WHERE partner_id = OLD.partner_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_partner_facility_count
    AFTER INSERT OR DELETE ON partner_catalog_facilities
    FOR EACH ROW EXECUTE FUNCTION update_partner_facility_count();

COMMIT;
