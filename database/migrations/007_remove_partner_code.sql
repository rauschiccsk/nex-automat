-- Migration 007: Remove redundant partner_code column
-- partner_code was always identical to partner_id (cast to text).
-- partner_id is the PK and business key; partner_code is redundant.
-- ============================================================

BEGIN;

-- 1. Drop the versioning trigger that references partner_code in its WHEN clause
DROP TRIGGER IF EXISTS trg_partner_catalog_versioning ON partner_catalog;

-- 2. Drop indexes on partner_code
DROP INDEX IF EXISTS idx_partner_catalog_code;

-- 3. Drop the UNIQUE constraint (which also removes its backing index)
ALTER TABLE partner_catalog DROP CONSTRAINT IF EXISTS partner_catalog_partner_code_key;

-- 4. Drop the column from partner_catalog
ALTER TABLE partner_catalog DROP COLUMN IF EXISTS partner_code;

-- 5. Drop the column from partner_catalog_history
ALTER TABLE partner_catalog_history DROP COLUMN IF EXISTS partner_code;

-- 6. Recreate the versioning trigger WITHOUT partner_code in the WHEN clause
CREATE OR REPLACE FUNCTION partner_catalog_versioning()
RETURNS trigger AS $$
BEGIN
    -- Close current version
    UPDATE partner_catalog_history
    SET valid_to = now()
    WHERE partner_id = OLD.partner_id AND valid_to IS NULL;

    -- Increment modify_id
    NEW.modify_id := OLD.modify_id + 1;

    -- Create new version snapshot
    INSERT INTO partner_catalog_history (
        partner_id, modify_id,
        partner_name, reg_name,
        company_id, tax_id, vat_id, is_vat_payer,
        is_supplier, is_customer,
        street, city, zip_code, country_code,
        partner_class,
        valid_from, changed_by
    ) VALUES (
        NEW.partner_id, NEW.modify_id,
        NEW.partner_name, NEW.reg_name,
        NEW.company_id, NEW.tax_id, NEW.vat_id, NEW.is_vat_payer,
        NEW.is_supplier, NEW.is_customer,
        NEW.street, NEW.city, NEW.zip_code, NEW.country_code,
        NEW.partner_class,
        now(), NEW.updated_by
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_partner_catalog_versioning
    BEFORE UPDATE ON partner_catalog
    FOR EACH ROW
    WHEN (
        (OLD.partner_name)::text IS DISTINCT FROM (NEW.partner_name)::text
        OR (OLD.reg_name)::text IS DISTINCT FROM (NEW.reg_name)::text
        OR (OLD.company_id)::text IS DISTINCT FROM (NEW.company_id)::text
        OR (OLD.tax_id)::text IS DISTINCT FROM (NEW.tax_id)::text
        OR (OLD.vat_id)::text IS DISTINCT FROM (NEW.vat_id)::text
        OR OLD.is_vat_payer IS DISTINCT FROM NEW.is_vat_payer
        OR OLD.is_supplier IS DISTINCT FROM NEW.is_supplier
        OR OLD.is_customer IS DISTINCT FROM NEW.is_customer
        OR (OLD.street)::text IS DISTINCT FROM (NEW.street)::text
        OR (OLD.city)::text IS DISTINCT FROM (NEW.city)::text
        OR (OLD.zip_code)::text IS DISTINCT FROM (NEW.zip_code)::text
        OR (OLD.country_code)::text IS DISTINCT FROM (NEW.country_code)::text
        OR (OLD.partner_class)::text IS DISTINCT FROM (NEW.partner_class)::text
    )
    EXECUTE FUNCTION partner_catalog_versioning();

-- 7. Recreate init_version function WITHOUT partner_code
CREATE OR REPLACE FUNCTION partner_catalog_init_version()
RETURNS trigger AS $$
BEGIN
    INSERT INTO partner_catalog_history (
        partner_id, modify_id,
        partner_name, reg_name,
        company_id, tax_id, vat_id, is_vat_payer,
        is_supplier, is_customer,
        street, city, zip_code, country_code,
        partner_class,
        valid_from, changed_by
    ) VALUES (
        NEW.partner_id, 0,
        NEW.partner_name, NEW.reg_name,
        NEW.company_id, NEW.tax_id, NEW.vat_id, NEW.is_vat_payer,
        NEW.is_supplier, NEW.is_customer,
        NEW.street, NEW.city, NEW.zip_code, NEW.country_code,
        NEW.partner_class,
        now(), NEW.created_by
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMIT;
