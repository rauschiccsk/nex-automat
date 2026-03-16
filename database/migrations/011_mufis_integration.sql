-- Migration 011: MuFis integration fields + delivery method
-- Ri approved: 2026-03-16
-- Author: ICC Team
-- Description: Pridanie MuFis synchronizačných polí a delivery method do eshop_orders

-- MuFis integration fields
ALTER TABLE eshop_orders ADD COLUMN mufis_order_id VARCHAR(50);
ALTER TABLE eshop_orders ADD COLUMN mufis_status VARCHAR(50);
ALTER TABLE eshop_orders ADD COLUMN mufis_tracking_number VARCHAR(100);
ALTER TABLE eshop_orders ADD COLUMN mufis_tracking_url VARCHAR(500);
ALTER TABLE eshop_orders ADD COLUMN mufis_carrier VARCHAR(50);
ALTER TABLE eshop_orders ADD COLUMN mufis_synced_at TIMESTAMP;

-- Delivery method (courier = default, packeta_point, packeta_box)
ALTER TABLE eshop_orders ADD COLUMN delivery_method VARCHAR(20) DEFAULT 'courier';
ALTER TABLE eshop_orders ADD COLUMN packeta_point_id VARCHAR(20);
ALTER TABLE eshop_orders ADD COLUMN packeta_point_name VARCHAR(255);

-- Indexy pre performance
CREATE INDEX idx_eshop_orders_mufis_synced ON eshop_orders(mufis_synced_at) WHERE mufis_synced_at IS NULL;
CREATE INDEX idx_eshop_orders_status_paid ON eshop_orders(status) WHERE status = 'paid';
