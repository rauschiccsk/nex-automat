-- Migration 015: Create user_sessions table for Session Management (Track 1)
-- Adapted from NEX Studio user_sessions pattern (D-021 reference, migration 021).
--
-- Purpose:
-- - Track active per-user JWT lifecycle anchors (multi-device support)
-- - Enable force-logout via token_version bump (invalidates all outstanding JWTs
--   that carry old tv claim)
-- - Enable "who is currently logged in" UI in System → Sessions module
--
-- Auth flow integration (Phase 1.2):
-- - login: INSERT row → JWT contains sid+tv claims
-- - get_current_user: SELECT WHERE session_id=sid AND token_version=tv
-- - logout: UPDATE token_version=token_version+1 (bumps tv → JWT no longer valid)
-- - last_seen_at: UPDATE NOW() throttled (only if older than 1 minute)

CREATE TABLE IF NOT EXISTS user_sessions (
    session_id      BIGSERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    token_version   INTEGER NOT NULL DEFAULT 0,
    user_agent      VARCHAR(500) DEFAULT NULL,
    ip_address      VARCHAR(45) DEFAULT NULL,  -- IPv4/IPv6 max length
    last_seen_at    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Lookups: list per user + recent activity ordering
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_last_seen_at ON user_sessions(last_seen_at DESC);

COMMENT ON TABLE user_sessions IS 'Per-device JWT lifecycle anchor — Track 1 Session Management';
COMMENT ON COLUMN user_sessions.token_version IS 'Monotonic counter; bumped on logout to invalidate outstanding JWTs (tv claim mismatch → 401)';
COMMENT ON COLUMN user_sessions.last_seen_at IS 'Last authenticated request timestamp; throttled to 1 minute updates';

-- ─────────────────────────────────────────────────────────────────────
-- Register SES module (Aktívne sessions) so frontend sidebar can show it
-- and permissions table can carry per-group access control.
-- ─────────────────────────────────────────────────────────────────────

INSERT INTO modules (module_code, module_name, category, icon, module_type, is_mock, sort_order, is_active)
VALUES ('SES', 'Aktívne sessions', 'system', 'Activity', 'catalog', false, 150, true)
ON CONFLICT (module_code) DO NOTHING;

-- Grant Administrátori full access to SES module.
INSERT INTO group_module_permissions
    (group_id, module_id, can_view, can_create, can_edit, can_delete, can_print, can_export, can_admin)
SELECT g.group_id, m.module_id, true, false, false, false, false, false, true
FROM groups g, modules m
WHERE g.group_name = 'Administrátori' AND m.module_code = 'SES'
ON CONFLICT (group_id, module_id) DO NOTHING;
