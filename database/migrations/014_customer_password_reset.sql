-- Migration 014: Add password reset columns to eshop_customers
-- Required for forgot-password / reset-password flow

ALTER TABLE eshop_customers
    ADD COLUMN IF NOT EXISTS reset_token VARCHAR(64) DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP WITH TIME ZONE DEFAULT NULL;
