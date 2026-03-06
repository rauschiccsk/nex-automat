-- Migration: Create migration tracking tables
-- Purpose: Track ETL migration from Btrieve to PostgreSQL

-- Batch tracking — každá migrácia je batch
CREATE TABLE IF NOT EXISTS migration_batches (
    id SERIAL PRIMARY KEY,
    category VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'running',
    source_count INTEGER DEFAULT 0,
    target_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    skipped_count INTEGER DEFAULT 0,
    started_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    error_log TEXT,
    metadata JSONB,
    created_by VARCHAR(50) DEFAULT 'migration'
);

CREATE INDEX IF NOT EXISTS idx_migration_batches_category ON migration_batches(category);
CREATE INDEX IF NOT EXISTS idx_migration_batches_status ON migration_batches(status);

-- ID Mapping — most medzi Btrieve kľúčmi a PostgreSQL UUID
CREATE TABLE IF NOT EXISTS migration_id_map (
    id SERIAL PRIMARY KEY,
    batch_id INTEGER NOT NULL REFERENCES migration_batches(id),
    category VARCHAR(10) NOT NULL,
    source_table VARCHAR(50) NOT NULL,
    source_key VARCHAR(255) NOT NULL,
    target_table VARCHAR(50) NOT NULL,
    target_id VARCHAR(255) NOT NULL,
    migrated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    UNIQUE(category, source_table, source_key)
);

CREATE INDEX IF NOT EXISTS idx_migration_id_map_source ON migration_id_map(source_table, source_key);
CREATE INDEX IF NOT EXISTS idx_migration_id_map_target ON migration_id_map(target_table, target_id);
CREATE INDEX IF NOT EXISTS idx_migration_id_map_category ON migration_id_map(category);
CREATE INDEX IF NOT EXISTS idx_migration_id_map_batch ON migration_id_map(batch_id);

-- Migration category status
CREATE TABLE IF NOT EXISTS migration_category_status (
    id SERIAL PRIMARY KEY,
    category VARCHAR(10) NOT NULL UNIQUE,
    last_batch_id INTEGER REFERENCES migration_batches(id),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    record_count INTEGER DEFAULT 0,
    first_migrated_at TIMESTAMP WITH TIME ZONE,
    last_migrated_at TIMESTAMP WITH TIME ZONE,
    notes TEXT
);

-- Pred-vyplniť kategórie
INSERT INTO migration_category_status (category, status) VALUES
    ('PAB', 'pending'),
    ('GSC', 'pending'),
    ('STK', 'pending'),
    ('TSH', 'pending'),
    ('ICB', 'pending'),
    ('ISB', 'pending'),
    ('OBJ', 'pending'),
    ('DOD', 'pending'),
    ('PAYJRN', 'pending')
ON CONFLICT (category) DO NOTHING;
