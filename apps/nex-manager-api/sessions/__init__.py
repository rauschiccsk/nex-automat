"""Sessions module — per-device JWT lifecycle anchor (Track 1 Session Management).

See database/migrations/015_create_user_sessions.sql for schema.
Auth integration (login creates session, logout bumps token_version) is in
auth/router.py and auth/dependencies.py — Phase 1.2.
"""

from .router import router

__all__ = ["router"]
