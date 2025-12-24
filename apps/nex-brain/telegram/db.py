"""
Database module pre Telegram Bot logging
"""
import os
import logging
from typing import Optional

import pg8000

logger = logging.getLogger(__name__)

# Database config
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "nex_automat_rag"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
}


def get_connection():
    """Získanie database connection"""
    try:
        conn = pg8000.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None


def log_query(
    user_id: int,
    username: Optional[str],
    tenant: str,
    question: str,
    answer: Optional[str] = None,
    sources: Optional[str] = None,
    response_time_ms: Optional[int] = None,
    feedback: Optional[str] = None
) -> Optional[int]:
    """Uloženie dotazu do databázy, vracia log_id"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO telegram_logs 
            (user_id, username, tenant, question, answer, sources, response_time_ms, feedback)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (user_id, username, tenant, question, answer, sources, response_time_ms, feedback)
        )
        result = cursor.fetchone()
        log_id = result[0] if result else None
        conn.commit()
        cursor.close()
        conn.close()
        return log_id
    except Exception as e:
        logger.error(f"Failed to log query: {e}")
        if conn:
            conn.close()
        return None


def update_feedback(log_id: int, feedback: str) -> bool:
    """Aktualizácia feedbacku pre existujúci log"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE telegram_logs SET feedback = %s WHERE id = %s",
            (feedback, log_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Failed to update feedback: {e}")
        if conn:
            conn.close()
        return False
