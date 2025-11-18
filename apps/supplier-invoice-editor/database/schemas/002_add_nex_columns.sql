-- 002_add_nex_columns.sql
-- Pridanie stlpcov pre NEX Genesis lookup data

-- Pridaj NEX stlpce do invoice_items_pending
ALTER TABLE invoice_items_pending
ADD COLUMN IF NOT EXISTS nex_plu INTEGER,
ADD COLUMN IF NOT EXISTS nex_name VARCHAR(255),
ADD COLUMN IF NOT EXISTS nex_category INTEGER,
ADD COLUMN IF NOT EXISTS in_nex BOOLEAN DEFAULT FALSE;

-- Indexy pre rychlejsie vyhladavanie
CREATE INDEX IF NOT EXISTS idx_invoice_items_pending_in_nex ON invoice_items_pending(in_nex);
CREATE INDEX IF NOT EXISTS idx_invoice_items_pending_nex_plu ON invoice_items_pending(nex_plu);

-- Komentar
COMMENT ON COLUMN invoice_items_pending.nex_plu IS 'PLU cislo produktu z NEX Genesis GSCAT';
COMMENT ON COLUMN invoice_items_pending.nex_name IS 'Nazov produktu z NEX Genesis GSCAT';
COMMENT ON COLUMN invoice_items_pending.nex_category IS 'Tovarova skupina (MGLST) z NEX Genesis';
COMMENT ON COLUMN invoice_items_pending.in_nex IS 'Priznak ci produkt existuje v NEX Genesis';
