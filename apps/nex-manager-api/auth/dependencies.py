"""FastAPI dependencies for authentication — JWT bearer token extraction."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from database import get_db
from .service import decode_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
):
    """Extract and validate user from JWT Bearer token.

    Returns dict with user_id, login_name, full_name, email, is_active.
    """
    token = credentials.credentials
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Neplatný typ tokenu")
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Neplatný alebo expirovaný token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    cur = db.cursor()
    cur.execute(
        "SELECT user_id, login_name, full_name, email, is_active "
        "FROM users WHERE user_id = %s",
        (user_id,),
    )
    user = cur.fetchone()

    if not user or not user[4]:  # is_active
        raise HTTPException(
            status_code=401, detail="Používateľ nebol nájdený alebo je neaktívny"
        )

    return {
        "user_id": user[0],
        "login_name": user[1],
        "full_name": user[2],
        "email": user[3],
        "is_active": user[4],
    }
