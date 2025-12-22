-- Migration: 003_add_file_tracking_columns.sql
-- Description: Add file tracking columns for new file organization system
-- Date: 2025-12-22
-- Author: Zoltán

-- ============================================================
-- PHASE A: Database changes for file reorganization
-- ============================================================

-- Add file tracking columns to supplier_invoice_heads
ALTER TABLE supplier_invoice_heads
ADD COLUMN IF NOT EXISTS file_basename VARCHAR(100),
ADD COLUMN IF NOT EXISTS file_status VARCHAR(20) DEFAULT 'received',
ADD COLUMN IF NOT EXISTS nex_invoice_doc_id VARCHAR(20),
ADD COLUMN IF NOT EXISTS nex_delivery_doc_id VARCHAR(20);

-- Add comments for documentation
COMMENT ON COLUMN supplier_invoice_heads.file_basename IS 'Base filename without extension (e.g., 20251222_125701_32506183)';
COMMENT ON COLUMN supplier_invoice_heads.file_status IS 'File lifecycle status: received, staged, archived';
COMMENT ON COLUMN supplier_invoice_heads.nex_invoice_doc_id IS 'NEX Genesis invoice document ID (e.g., DF2500100123)';
COMMENT ON COLUMN supplier_invoice_heads.nex_delivery_doc_id IS 'NEX Genesis delivery note document ID (e.g., DD2500100205)';

-- Add check constraint for file_status
ALTER TABLE supplier_invoice_heads
DROP CONSTRAINT IF EXISTS chk_file_status;

ALTER TABLE supplier_invoice_heads
ADD CONSTRAINT chk_file_status 
CHECK (file_status IN ('received', 'staged', 'archived'));

-- Create index for file_status queries
CREATE INDEX IF NOT EXISTS idx_sih_file_status ON supplier_invoice_heads(file_status);

-- ============================================================
-- Backfill existing records with file_basename from pdf_file_path
-- ============================================================
UPDATE supplier_invoice_heads
SET file_basename = regexp_replace(
    regexp_replace(pdf_file_path, '.*[/\\]', ''),
    '\.[^.]+$', ''
),
file_status = 'staged'
WHERE file_basename IS NULL AND pdf_file_path IS NOT NULL;
