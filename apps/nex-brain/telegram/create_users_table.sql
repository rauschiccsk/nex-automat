-- Tabuľka pre správu Telegram používateľov
CREATE TABLE IF NOT EXISTS telegram_users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    username VARCHAR(100),
    first_name VARCHAR(100),
    tenant VARCHAR(50) NOT NULL,  -- 'icc' alebo 'andros'
    status VARCHAR(20) DEFAULT 'pending',  -- pending/approved/rejected
    requested_at TIMESTAMP DEFAULT NOW(),
    approved_at TIMESTAMP,
    approved_by BIGINT,  -- admin user_id ktorý schválil
    notes TEXT,  -- poznámky admina
    UNIQUE(user_id, tenant)  -- jeden user môže byť v oboch tenantoch
);

-- Indexy
CREATE INDEX IF NOT EXISTS idx_telegram_users_user_id ON telegram_users(user_id);
CREATE INDEX IF NOT EXISTS idx_telegram_users_tenant ON telegram_users(tenant);
CREATE INDEX IF NOT EXISTS idx_telegram_users_status ON telegram_users(status);

-- Komentár
COMMENT ON TABLE telegram_users IS 'NEX Brain Telegram Bot - user management and approval';

-- Admin tabuľka - kto má admin práva
CREATE TABLE IF NOT EXISTS telegram_admins (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(100),
    added_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE telegram_admins IS 'NEX Brain Telegram Bot - admin users';
