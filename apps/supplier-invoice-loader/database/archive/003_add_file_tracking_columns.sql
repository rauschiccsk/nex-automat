-- Migration: 003_add_file_tracking_columns.sql
-- Description: Add file tracking columns for new file organization system
-- Date: 2025-12-22
-- Author: Zoltán

-- ============================================================
-- PHASE A: Database changes for file reorganization
-- ============================================================

-- Add file tracking columns to invoices_pending
ALTER TABLE invoices_pending
ADD COLUMN IF NOT EXISTS file_basename VARCHAR(100),
ADD COLUMN IF NOT EXISTS file_status VARCHAR(20) DEFAULT 'received',
ADD COLUMN IF NOT EXISTS nex_invoice_doc_id VARCHAR(20),
ADD COLUMN IF NOT EXISTS nex_delivery_doc_id VARCHAR(20);

-- Add comments for documentation
COMMENT ON COLUMN invoices_pending.file_basename IS 'Base filename without extension (e.g., 20251222_125701_32506183)';
COMMENT ON COLUMN invoices_pending.file_status IS 'File lifecycle status: received, staged, archived';
COMMENT ON COLUMN invoices_pending.nex_invoice_doc_id IS 'NEX Genesis invoice document ID (e.g., DF2500100123)';
COMMENT ON COLUMN invoices_pending.nex_delivery_doc_id IS 'NEX Genesis delivery note document ID (e.g., DD2500100205)';

-- Add check constraint for file_status
ALTER TABLE invoices_pending
DROP CONSTRAINT IF EXISTS chk_file_status;

ALTER TABLE invoices_pending
ADD CONSTRAINT chk_file_status 
CHECK (file_status IN ('received', 'staged', 'archived'));

-- Create index for file_status queries
CREATE INDEX IF NOT EXISTS idx_ip_file_status ON invoices_pending(file_status);

-- ============================================================
-- Backfill existing records with file_basename from pdf_file_path
-- ============================================================
UPDATE invoices_pending
SET file_basename = regexp_replace(
    regexp_replace(pdf_file_path, '.*[/\\]', ''),
    '\.[^.]+$', ''
),
file_status = 'staged'
WHERE file_basename IS NULL AND pdf_file_path IS NOT NULL;
