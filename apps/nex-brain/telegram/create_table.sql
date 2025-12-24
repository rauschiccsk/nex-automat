
CREATE TABLE IF NOT EXISTS telegram_logs (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    username VARCHAR(100),
    tenant VARCHAR(50) DEFAULT 'icc',
    question TEXT NOT NULL,
    answer TEXT,
    sources TEXT,
    response_time_ms INTEGER,
    feedback VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_telegram_logs_user ON telegram_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_telegram_logs_tenant ON telegram_logs(tenant);
CREATE INDEX IF NOT EXISTS idx_telegram_logs_created ON telegram_logs(created_at);

-- Komentár pre prehľadnosť
COMMENT ON TABLE telegram_logs IS 'NEX Brain Telegram Bot - logging queries';
