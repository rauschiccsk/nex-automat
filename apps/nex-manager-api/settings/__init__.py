"""Settings module — runtime tunable parameters editable from Settings UI.

Database-backed key/value store (system_settings table, migration 016).
Backfill in Track 2 Phase 2.3 replaces hardcoded reads with get_setting().

Note: ``router`` is NOT exported here — dynamic loader imports it directly
via ``importlib.import_module('settings.router')``. Exporting from __init__
caused circular import (settings -> router -> auth.dependencies -> auth.service
-> settings.service while auth.service is still initializing).
``get_setting`` is safe to expose — service.py imports only from database.
"""

from .service import get_setting, get_setting_typed

__all__ = ["get_setting", "get_setting_typed"]
