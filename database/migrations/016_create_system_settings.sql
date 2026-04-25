-- Migration 016: Create system_settings table for Settings UI (Track 2 Phase 2.2)
--
-- Purpose: DB-backed runtime tunables editable from System → Nastavenia UI.
-- Sensitive secrets (JWT_SECRET_KEY, POSTGRES_PASSWORD, SMTP_PASSWORD) stay
-- in .env per Q4 (Hybrid storage). Critical params (bcrypt_rounds, JWT_ALGO)
-- stay hardcoded per Q5 (hide from UI). This table holds runtime tunables only.
--
-- Convention:
--   setting_key — dotted snake_case (e.g. business.default_vat_rate_percent)
--   value       — JSONB allows int / string / bool / array values
--   scope       — global (default) | tenant:N | user:N (Phase 2.3+ if needed)
--   category    — UI grouping (auth, business, ui, integration, payment, ...)

CREATE TABLE IF NOT EXISTS system_settings (
    setting_key   VARCHAR(100) PRIMARY KEY,
    value         JSONB NOT NULL,
    scope         VARCHAR(50) NOT NULL DEFAULT 'global',
    category      VARCHAR(50) NOT NULL DEFAULT 'general',
    description   TEXT DEFAULT NULL,
    updated_by    VARCHAR(50) DEFAULT NULL,
    updated_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_system_settings_category ON system_settings(category);

COMMENT ON TABLE system_settings IS 'Runtime tunable parameters editable from Settings UI — Track 2 Phase 2.2';
COMMENT ON COLUMN system_settings.setting_key IS 'Dotted snake_case key (e.g. business.default_vat_rate_percent)';
COMMENT ON COLUMN system_settings.value IS 'JSONB — supports int/string/bool/array values';
COMMENT ON COLUMN system_settings.category IS 'UI grouping (auth, business, ui, integration, ...)';

-- ─────────────────────────────────────────────────────────────────────
-- Seed initial settings — defaults match current compile-time constants
-- (nex_config/business.py, nex_config/limits.py, nex_config/security.py,
-- src/lib/constants.ts). Phase 2.3 backfill will replace hardcoded reads
-- with get_setting() calls; these values become the active runtime config.
-- ─────────────────────────────────────────────────────────────────────

INSERT INTO system_settings (setting_key, value, category, description) VALUES
    -- Business rules
    ('business.default_payment_due_days', '14'::jsonb, 'business',
     'Predvolená lehota splatnosti pre nových partnerov (dni)'),
    ('business.default_vat_rate_percent', '20'::jsonb, 'business',
     'Predvolená sadzba DPH (%) pre XML export keď item-level rate chýba'),

    -- UI defaults
    ('ui.search_debounce_ms', '300'::jsonb, 'ui',
     'Debounce delay pre search inputy (ms)'),
    ('ui.toast_default_duration_ms', '4000'::jsonb, 'ui',
     'Štandardný čas zobrazenia toast notifikácie (ms)'),

    -- Auth
    ('auth.access_token_expiry_seconds', '1800'::jsonb, 'auth',
     'Platnosť access tokenu v sekundách (default 30 min)'),
    ('auth.refresh_token_expiry_days', '7'::jsonb, 'auth',
     'Platnosť refresh tokenu v dňoch (default 7)'),

    -- Payment integration
    ('payment.comgate_base_url', '"https://payments.comgate.cz/v1.0"'::jsonb, 'payment',
     'Comgate API base URL (prepnúť na test endpoint pre dev)'),

    -- MuFis integration
    ('integration.mufis_page_size', '50'::jsonb, 'integration',
     'Page size pre MuFis API getOrder/getProduct')
ON CONFLICT (setting_key) DO NOTHING;

-- ─────────────────────────────────────────────────────────────────────
-- Activate SET module (was 'planned' — now 'active' with Settings UI)
-- ─────────────────────────────────────────────────────────────────────

INSERT INTO modules (module_code, module_name, category, icon, module_type, is_mock, sort_order, is_active)
VALUES ('SET', 'Nastavenia', 'system', 'Settings', 'catalog', false, 130, true)
ON CONFLICT (module_code) DO UPDATE
   SET is_active = true, is_mock = false, icon = 'Settings';

INSERT INTO group_module_permissions
    (group_id, module_id, can_view, can_create, can_edit, can_delete, can_print, can_export, can_admin)
SELECT g.group_id, m.module_id, true, false, true, false, false, false, true
FROM groups g, modules m
WHERE g.group_name = 'Administrátori' AND m.module_code = 'SET'
ON CONFLICT (group_id, module_id) DO UPDATE
   SET can_view = true, can_edit = true, can_admin = true;
