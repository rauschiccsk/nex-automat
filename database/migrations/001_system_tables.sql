-- Migration 001: System tables for NEX Manager
-- Auth, RBAC, Module Registry, Audit Log
--
-- Conventions (from ARCHITECTURE.md):
--   PK: *_id (SERIAL/BIGSERIAL)
--   Codes: *_code VARCHAR, unique
--   Names: *_name VARCHAR
--   Booleans: is_* DEFAULT true
--   Timestamps: *_at TIMESTAMPTZ DEFAULT NOW()
--   Audit: created_at, created_by, updated_at, updated_by VARCHAR(50)
--   Soft delete: is_active BOOLEAN DEFAULT true
--   Ref integrity: RESTRICT master, CASCADE detail

BEGIN;

-- ============================================================
-- 1. USERS
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    user_id         SERIAL PRIMARY KEY,
    login_name      VARCHAR(50)  NOT NULL UNIQUE,
    full_name       VARCHAR(150) NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    email           VARCHAR(150),
    is_active       BOOLEAN      NOT NULL DEFAULT true,
    last_login_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by      VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50)  NOT NULL DEFAULT 'system'
);

CREATE INDEX idx_users_login_name ON users (login_name);
CREATE INDEX idx_users_is_active ON users (is_active);

-- ============================================================
-- 2. GROUPS (hierarchical)
-- ============================================================
CREATE TABLE IF NOT EXISTS groups (
    group_id    SERIAL PRIMARY KEY,
    group_name  VARCHAR(100) NOT NULL UNIQUE,
    parent_id   INTEGER      REFERENCES groups(group_id) ON DELETE RESTRICT,
    level       SMALLINT     NOT NULL DEFAULT 0,
    description VARCHAR(255),
    is_active   BOOLEAN      NOT NULL DEFAULT true,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_by  VARCHAR(50)  NOT NULL DEFAULT 'system',
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by  VARCHAR(50)  NOT NULL DEFAULT 'system'
);

CREATE INDEX idx_groups_parent_id ON groups (parent_id);
CREATE INDEX idx_groups_is_active ON groups (is_active);

-- ============================================================
-- 3. USER_GROUPS (M:N)
-- ============================================================
CREATE TABLE IF NOT EXISTS user_groups (
    user_group_id  SERIAL PRIMARY KEY,
    user_id        INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    group_id       INTEGER NOT NULL REFERENCES groups(group_id) ON DELETE RESTRICT,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by     VARCHAR(50) NOT NULL DEFAULT 'system',
    UNIQUE (user_id, group_id)
);

CREATE INDEX idx_user_groups_user_id ON user_groups (user_id);
CREATE INDEX idx_user_groups_group_id ON user_groups (group_id);

-- ============================================================
-- 4. MODULES
-- ============================================================
CREATE TYPE module_category AS ENUM ('base', 'stock', 'sales', 'purchase', 'accounting', 'pos', 'system');
CREATE TYPE module_type AS ENUM ('catalog', 'document', 'report', 'config');

CREATE TABLE IF NOT EXISTS modules (
    module_id    SERIAL PRIMARY KEY,
    module_code  VARCHAR(10)     NOT NULL UNIQUE,
    module_name  VARCHAR(100)    NOT NULL,
    category     module_category NOT NULL,
    icon         VARCHAR(50)     NOT NULL DEFAULT 'Package',
    module_type  module_type     NOT NULL DEFAULT 'catalog',
    is_mock      BOOLEAN         NOT NULL DEFAULT true,
    sort_order   SMALLINT        NOT NULL DEFAULT 0,
    is_active    BOOLEAN         NOT NULL DEFAULT true,
    created_at   TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by   VARCHAR(50)     NOT NULL DEFAULT 'system',
    updated_at   TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_by   VARCHAR(50)     NOT NULL DEFAULT 'system'
);

CREATE INDEX idx_modules_category ON modules (category);
CREATE INDEX idx_modules_is_active ON modules (is_active);

-- ============================================================
-- 5. GROUP_MODULE_PERMISSIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS group_module_permissions (
    permission_id  SERIAL PRIMARY KEY,
    group_id       INTEGER NOT NULL REFERENCES groups(group_id) ON DELETE CASCADE,
    module_id      INTEGER NOT NULL REFERENCES modules(module_id) ON DELETE CASCADE,
    can_view       BOOLEAN NOT NULL DEFAULT false,
    can_create     BOOLEAN NOT NULL DEFAULT false,
    can_edit       BOOLEAN NOT NULL DEFAULT false,
    can_delete     BOOLEAN NOT NULL DEFAULT false,
    can_print      BOOLEAN NOT NULL DEFAULT false,
    can_export     BOOLEAN NOT NULL DEFAULT false,
    can_admin      BOOLEAN NOT NULL DEFAULT false,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by     VARCHAR(50) NOT NULL DEFAULT 'system',
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by     VARCHAR(50) NOT NULL DEFAULT 'system',
    UNIQUE (group_id, module_id)
);

CREATE INDEX idx_gmp_group_id ON group_module_permissions (group_id);
CREATE INDEX idx_gmp_module_id ON group_module_permissions (module_id);

-- ============================================================
-- 6. AUDIT_LOG
-- ============================================================
CREATE TABLE IF NOT EXISTS audit_log (
    audit_id    BIGSERIAL PRIMARY KEY,
    user_id     INTEGER      REFERENCES users(user_id) ON DELETE SET NULL,
    action      VARCHAR(50)  NOT NULL,
    entity_type VARCHAR(50)  NOT NULL,
    entity_id   INTEGER,
    details     JSONB,
    ip_address  VARCHAR(45),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_log_user_id ON audit_log (user_id);
CREATE INDEX idx_audit_log_entity ON audit_log (entity_type, entity_id);
CREATE INDEX idx_audit_log_created_at ON audit_log (created_at);
CREATE INDEX idx_audit_log_action ON audit_log (action);

-- ============================================================
-- TRIGGER: auto-update updated_at
-- ============================================================
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at_users BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
CREATE TRIGGER set_updated_at_groups BEFORE UPDATE ON groups
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
CREATE TRIGGER set_updated_at_modules BEFORE UPDATE ON modules
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();
CREATE TRIGGER set_updated_at_gmp BEFORE UPDATE ON group_module_permissions
    FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

COMMIT;
