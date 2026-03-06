-- Migration 006: Partner Catalog versioning system
-- Adds partner_class, modify_id to partner_catalog and creates
-- partner_catalog_history table with INSERT/UPDATE triggers.
--
-- Conventions (consistent with migration 005):
--   VARCHAR with CHECK constraint (not ENUM)
--   Triggers for automatic versioning
--   Business fields copied to history on every change

BEGIN;

-- ============================================================
-- 1. ADD partner_class AND modify_id TO partner_catalog
-- ============================================================

ALTER TABLE partner_catalog
  ADD COLUMN IF NOT EXISTS partner_class VARCHAR(20) NOT NULL DEFAULT 'business'
    CHECK (partner_class IN ('business', 'retail', 'guest')),
  ADD COLUMN IF NOT EXISTS modify_id INTEGER NOT NULL DEFAULT 0;

CREATE INDEX IF NOT EXISTS idx_partner_catalog_class
  ON partner_catalog(partner_class);
CREATE INDEX IF NOT EXISTS idx_partner_catalog_class_active
  ON partner_catalog(partner_class, is_active);

-- ============================================================
-- 2. PARTNER_CATALOG_HISTORY — version history table
-- ============================================================
-- Contains ALL business fields from partner_catalog (excluding
-- system/audit fields: is_active, created_at, created_by,
-- updated_at, updated_by, bank_account_count, facility_count).

CREATE TABLE IF NOT EXISTS partner_catalog_history (
    history_id      SERIAL       PRIMARY KEY,
    partner_id      INTEGER      NOT NULL,
    modify_id       INTEGER      NOT NULL,

    -- Business fields (copied from partner_catalog)
    partner_code    VARCHAR(30)  NOT NULL,
    partner_name    VARCHAR(100) NOT NULL,
    reg_name        VARCHAR(100),

    company_id      VARCHAR(20),
    tax_id          VARCHAR(20),
    vat_id          VARCHAR(20),
    is_vat_payer    BOOLEAN      NOT NULL DEFAULT false,

    is_supplier     BOOLEAN      NOT NULL DEFAULT false,
    is_customer     BOOLEAN      NOT NULL DEFAULT true,

    street          VARCHAR(100),
    city            VARCHAR(100),
    zip_code        VARCHAR(20),
    country_code    VARCHAR(2)   DEFAULT 'SK',

    partner_class   VARCHAR(20)  NOT NULL DEFAULT 'business',

    -- Version metadata
    valid_from      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    valid_to        TIMESTAMPTZ,
    changed_by      VARCHAR(50),

    CONSTRAINT uq_partner_history_version UNIQUE (partner_id, modify_id),
    FOREIGN KEY (partner_id) REFERENCES partner_catalog(partner_id) ON DELETE CASCADE
);

CREATE INDEX idx_partner_history_partner
  ON partner_catalog_history(partner_id);
CREATE INDEX idx_partner_history_current
  ON partner_catalog_history(partner_id) WHERE valid_to IS NULL;

-- ============================================================
-- 3. INSERT TRIGGER — initialize version (modify_id = 0)
-- ============================================================

CREATE OR REPLACE FUNCTION partner_catalog_init_version()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO partner_catalog_history (
        partner_id, modify_id,
        partner_code, partner_name, reg_name,
        company_id, tax_id, vat_id, is_vat_payer,
        is_supplier, is_customer,
        street, city, zip_code, country_code,
        partner_class,
        valid_from, changed_by
    ) VALUES (
        NEW.partner_id, 0,
        NEW.partner_code, NEW.partner_name, NEW.reg_name,
        NEW.company_id, NEW.tax_id, NEW.vat_id, NEW.is_vat_payer,
        NEW.is_supplier, NEW.is_customer,
        NEW.street, NEW.city, NEW.zip_code, NEW.country_code,
        NEW.partner_class,
        NOW(), NEW.created_by
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_partner_catalog_init_version
    AFTER INSERT ON partner_catalog
    FOR EACH ROW
    EXECUTE FUNCTION partner_catalog_init_version();

-- ============================================================
-- 4. UPDATE TRIGGER — versioning on business field changes
-- ============================================================

CREATE OR REPLACE FUNCTION partner_catalog_versioning()
RETURNS TRIGGER AS $$
BEGIN
    -- Close previous version
    UPDATE partner_catalog_history
    SET valid_to = NOW()
    WHERE partner_id = OLD.partner_id AND valid_to IS NULL;

    -- Increment modify_id
    NEW.modify_id := OLD.modify_id + 1;

    -- Insert new version
    INSERT INTO partner_catalog_history (
        partner_id, modify_id,
        partner_code, partner_name, reg_name,
        company_id, tax_id, vat_id, is_vat_payer,
        is_supplier, is_customer,
        street, city, zip_code, country_code,
        partner_class,
        valid_from, changed_by
    ) VALUES (
        NEW.partner_id, NEW.modify_id,
        NEW.partner_code, NEW.partner_name, NEW.reg_name,
        NEW.company_id, NEW.tax_id, NEW.vat_id, NEW.is_vat_payer,
        NEW.is_supplier, NEW.is_customer,
        NEW.street, NEW.city, NEW.zip_code, NEW.country_code,
        NEW.partner_class,
        NOW(), NEW.updated_by
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- WHEN condition: triggers ONLY on business field changes
-- EXCLUDES: is_active, updated_at, updated_by, created_at, created_by,
--           modify_id, bank_account_count, facility_count
CREATE TRIGGER trg_partner_catalog_versioning
    BEFORE UPDATE ON partner_catalog
    FOR EACH ROW
    WHEN (
        OLD.partner_code    IS DISTINCT FROM NEW.partner_code
        OR OLD.partner_name IS DISTINCT FROM NEW.partner_name
        OR OLD.reg_name     IS DISTINCT FROM NEW.reg_name
        OR OLD.company_id   IS DISTINCT FROM NEW.company_id
        OR OLD.tax_id       IS DISTINCT FROM NEW.tax_id
        OR OLD.vat_id       IS DISTINCT FROM NEW.vat_id
        OR OLD.is_vat_payer IS DISTINCT FROM NEW.is_vat_payer
        OR OLD.is_supplier  IS DISTINCT FROM NEW.is_supplier
        OR OLD.is_customer  IS DISTINCT FROM NEW.is_customer
        OR OLD.street       IS DISTINCT FROM NEW.street
        OR OLD.city         IS DISTINCT FROM NEW.city
        OR OLD.zip_code     IS DISTINCT FROM NEW.zip_code
        OR OLD.country_code IS DISTINCT FROM NEW.country_code
        OR OLD.partner_class IS DISTINCT FROM NEW.partner_class
    )
    EXECUTE FUNCTION partner_catalog_versioning();

-- ============================================================
-- 5. INITIALIZE HISTORY for existing records
-- ============================================================
-- Create initial history records (modify_id=0) for any existing
-- partner_catalog rows that do not yet have a history entry.

INSERT INTO partner_catalog_history (
    partner_id, modify_id,
    partner_code, partner_name, reg_name,
    company_id, tax_id, vat_id, is_vat_payer,
    is_supplier, is_customer,
    street, city, zip_code, country_code,
    partner_class,
    valid_from, changed_by
)
SELECT
    pc.partner_id, 0,
    pc.partner_code, pc.partner_name, pc.reg_name,
    pc.company_id, pc.tax_id, pc.vat_id, pc.is_vat_payer,
    pc.is_supplier, pc.is_customer,
    pc.street, pc.city, pc.zip_code, pc.country_code,
    pc.partner_class,
    COALESCE(pc.created_at, NOW()), pc.created_by
FROM partner_catalog pc
WHERE NOT EXISTS (
    SELECT 1 FROM partner_catalog_history h
    WHERE h.partner_id = pc.partner_id
);

COMMIT;
