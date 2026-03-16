-- Migration 012: Status history source tracking
-- Allows tracking status change source (user/mufis/system) and original MuFis status

ALTER TABLE eshop_order_status_history ADD COLUMN source VARCHAR(20);
ALTER TABLE eshop_order_status_history ADD COLUMN mufis_original_status VARCHAR(100);

-- Add comment for clarity
COMMENT ON COLUMN eshop_order_status_history.source IS 'Change source: user, mufis, system';
COMMENT ON COLUMN eshop_order_status_history.mufis_original_status IS 'Original Hungarian status from MuFis (e.g. kézbesítve)';
