"""Auth configuration — thin wrapper over nex_config.security.

Other modules in nex-manager-api import from here for backward compatibility.
"""

from datetime import timedelta

from nex_config.security import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)

# Re-export as timedelta for backward compatibility
ACCESS_TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

# Also export the new names
ACCESS_TOKEN_EXPIRE_DELTA = ACCESS_TOKEN_EXPIRE
REFRESH_TOKEN_EXPIRE_DELTA = REFRESH_TOKEN_EXPIRE

__all__ = [
    "JWT_SECRET_KEY",
    "JWT_ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "REFRESH_TOKEN_EXPIRE_DAYS",
    "ACCESS_TOKEN_EXPIRE",
    "REFRESH_TOKEN_EXPIRE",
    "ACCESS_TOKEN_EXPIRE_DELTA",
    "REFRESH_TOKEN_EXPIRE_DELTA",
]
