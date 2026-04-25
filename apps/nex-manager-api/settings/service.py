"""Settings service — DB-backed runtime config reads with helper functions.

Phase 2.2: simple read-through (no cache). Phase 2.3 backfill may add a
process-local cache with TTL or invalidation hooks if read frequency
becomes a concern.
"""

from __future__ import annotations

from typing import Any, TypeVar

from database import get_connection

T = TypeVar("T")


def get_setting(key: str, default: Any = None) -> Any:
    """Read a setting value from system_settings.

    Returns the JSONB-decoded value, or `default` if the key is absent.
    Use this in backend code to replace hardcoded constants:

        # Before:
        debounce_ms = 300
        # After:
        debounce_ms = get_setting("ui.search_debounce_ms", default=300)
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT value FROM system_settings WHERE setting_key = %s",
            (key,),
        )
        row = cur.fetchone()
        if row is None:
            return default
        return row[0]


def get_setting_typed(key: str, default: T) -> T:
    """Same as get_setting but with explicit type narrowing via `default`.

    Useful for type-checked code paths:

        page_size: int = get_setting_typed("integration.mufis_page_size", 50)
    """
    val = get_setting(key, default)
    return val  # type: ignore[return-value]
