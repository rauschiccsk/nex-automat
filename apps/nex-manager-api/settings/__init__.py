"""Settings module — runtime tunable parameters editable from Settings UI.

Database-backed key/value store (system_settings table, migration 016).
Backfill in Track 2 Phase 2.3 replaces hardcoded reads with get_setting().
"""

from .router import router
from .service import get_setting, get_setting_typed

__all__ = ["router", "get_setting", "get_setting_typed"]
