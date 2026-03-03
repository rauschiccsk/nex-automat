"""User management API endpoints — CRUD, password change, audit logging."""

import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth.dependencies import require_permission
from auth.service import hash_password
from database import get_db

from .schemas import (
    ChangePasswordRequest,
    CreateUserRequest,
    GroupInfo,
    UpdateUserRequest,
    UserListResponse,
    UserResponse,
)

router = APIRouter(prefix="/api/users", tags=["users"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _row_to_user(row: tuple, groups: list[GroupInfo] | None = None) -> UserResponse:
    """Map a database row to a UserResponse.

    Expected columns: user_id, login_name, full_name, email, is_active,
                      last_login_at, created_at, updated_at
    """
    return UserResponse(
        user_id=row[0],
        login_name=row[1],
        full_name=row[2],
        email=row[3],
        is_active=row[4],
        last_login_at=row[5],
        created_at=row[6],
        updated_at=row[7] if len(row) > 7 else None,
        groups=groups or [],
    )


_USER_COLUMNS = (
    "u.user_id, u.login_name, u.full_name, u.email, "
    "u.is_active, u.last_login_at, u.created_at, u.updated_at"
)


def _get_user_groups(cur, user_id: int) -> list[GroupInfo]:
    """Fetch group memberships for a user."""
    cur.execute(
        "SELECT g.group_id, g.group_name "
        "FROM user_groups ug "
        "JOIN groups g ON ug.group_id = g.group_id "
        "WHERE ug.user_id = %s AND g.is_active = true",
        (user_id,),
    )
    return [GroupInfo(group_id=r[0], group_name=r[1]) for r in cur.fetchall()]


def _write_audit_log(
    cur,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
    details: dict | None = None,
) -> None:
    """Insert an audit log entry."""
    cur.execute(
        "INSERT INTO audit_log (user_id, action, entity_type, entity_id, details) "
        "VALUES (%s, %s, %s, %s, %s)",
        (
            user_id,
            action,
            entity_type,
            entity_id,
            json.dumps(details) if details else None,
        ),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("", response_model=UserListResponse)
def list_users(
    group_id: Optional[int] = Query(None, description="Filter by group_id"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(
        None, description="Search in username, full_name, email"
    ),
    _current_user=Depends(require_permission("USR", "can_view")),
    db=Depends(get_db),
):
    """List all users with optional filters."""
    query = f"SELECT DISTINCT {_USER_COLUMNS} FROM users u "
    joins: list[str] = []
    conditions: list[str] = []
    params: list = []

    if group_id is not None:
        joins.append("JOIN user_groups ug ON u.user_id = ug.user_id")
        conditions.append("ug.group_id = %s")
        params.append(group_id)

    if is_active is not None:
        conditions.append("u.is_active = %s")
        params.append(is_active)

    if search is not None:
        conditions.append(
            "(u.login_name ILIKE %s OR u.full_name ILIKE %s OR u.email ILIKE %s)"
        )
        like_val = f"%{search}%"
        params.extend([like_val, like_val, like_val])

    if joins:
        query += " ".join(joins) + " "
    if conditions:
        query += "WHERE " + " AND ".join(conditions) + " "

    query += "ORDER BY u.user_id"

    cur = db.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()

    users = []
    for row in rows:
        groups = _get_user_groups(cur, row[0])
        users.append(_row_to_user(row, groups))

    return UserListResponse(users=users, total=len(users))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    _current_user=Depends(require_permission("USR", "can_view")),
    db=Depends(get_db),
):
    """Get a single user by ID."""
    cur = db.cursor()
    cur.execute(
        f"SELECT {_USER_COLUMNS} FROM users u WHERE u.user_id = %s",
        (user_id,),
    )
    row = cur.fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pou\u017e\u00edvate\u013e nebol n\u00e1jden\u00fd",
        )

    groups = _get_user_groups(cur, user_id)
    return _row_to_user(row, groups)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    body: CreateUserRequest,
    current_user=Depends(require_permission("USR", "can_create")),
    db=Depends(get_db),
):
    """Create a new user."""
    cur = db.cursor()

    # Check username uniqueness
    cur.execute(
        "SELECT user_id FROM users WHERE login_name = %s",
        (body.username,),
    )
    if cur.fetchone():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pou\u017e\u00edvate\u013esk\u00e9 meno u\u017e existuje",
        )

    # Hash password
    pw_hash = hash_password(body.password)

    # Insert user
    cur.execute(
        "INSERT INTO users (login_name, full_name, email, password_hash, is_active, created_by) "
        "VALUES (%s, %s, %s, %s, %s, %s) "
        "RETURNING user_id, login_name, full_name, email, is_active, "
        "last_login_at, created_at, updated_at",
        (
            body.username,
            body.full_name,
            body.email,
            pw_hash,
            body.is_active,
            current_user["login_name"],
        ),
    )
    new_row = cur.fetchone()
    new_user_id = new_row[0]

    # Assign groups
    groups: list[GroupInfo] = []
    if body.group_ids:
        for gid in body.group_ids:
            cur.execute(
                "INSERT INTO user_groups (user_id, group_id, created_by) "
                "VALUES (%s, %s, %s)",
                (new_user_id, gid, current_user["login_name"]),
            )
        groups = _get_user_groups(cur, new_user_id)

    # Audit log
    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="create",
        entity_type="USR",
        entity_id=new_user_id,
        details={"message": f"Created user: {body.username}"},
    )

    db.commit()
    return _row_to_user(new_row, groups)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    body: UpdateUserRequest,
    current_user=Depends(require_permission("USR", "can_edit")),
    db=Depends(get_db),
):
    """Update an existing user. Username is NOT editable."""
    cur = db.cursor()

    # Check user exists
    cur.execute(
        "SELECT login_name FROM users WHERE user_id = %s",
        (user_id,),
    )
    existing = cur.fetchone()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pou\u017e\u00edvate\u013e nebol n\u00e1jden\u00fd",
        )
    login_name = existing[0]

    # Build dynamic UPDATE
    set_parts: list[str] = []
    params: list = []

    if body.full_name is not None:
        set_parts.append("full_name = %s")
        params.append(body.full_name)
    if body.email is not None:
        set_parts.append("email = %s")
        params.append(body.email)
    if body.is_active is not None:
        set_parts.append("is_active = %s")
        params.append(body.is_active)

    if set_parts:
        set_parts.append("updated_by = %s")
        params.append(current_user["login_name"])
        params.append(user_id)
        cur.execute(
            f"UPDATE users SET {', '.join(set_parts)} WHERE user_id = %s",
            params,
        )

    # Update group assignments
    if body.group_ids is not None:
        cur.execute(
            "DELETE FROM user_groups WHERE user_id = %s",
            (user_id,),
        )
        for gid in body.group_ids:
            cur.execute(
                "INSERT INTO user_groups (user_id, group_id, created_by) "
                "VALUES (%s, %s, %s)",
                (user_id, gid, current_user["login_name"]),
            )

    # Audit log
    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="update",
        entity_type="USR",
        entity_id=user_id,
        details={"message": f"Updated user: {login_name}"},
    )

    db.commit()

    # Return updated user
    cur.execute(
        f"SELECT {_USER_COLUMNS} FROM users u WHERE u.user_id = %s",
        (user_id,),
    )
    row = cur.fetchone()
    groups = _get_user_groups(cur, user_id)
    return _row_to_user(row, groups)


@router.put("/{user_id}/password")
def admin_change_password(
    user_id: int,
    body: ChangePasswordRequest,
    current_user=Depends(require_permission("USR", "can_edit")),
    db=Depends(get_db),
):
    """Admin: change a user's password."""
    cur = db.cursor()

    # Check user exists
    cur.execute(
        "SELECT login_name FROM users WHERE user_id = %s",
        (user_id,),
    )
    existing = cur.fetchone()
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pou\u017e\u00edvate\u013e nebol n\u00e1jden\u00fd",
        )
    login_name = existing[0]

    # Hash and update
    pw_hash = hash_password(body.new_password)
    cur.execute(
        "UPDATE users SET password_hash = %s, updated_by = %s WHERE user_id = %s",
        (pw_hash, current_user["login_name"], user_id),
    )

    # Audit log
    _write_audit_log(
        cur,
        user_id=current_user["user_id"],
        action="password_change",
        entity_type="USR",
        entity_id=user_id,
        details={"message": f"Admin changed password for: {login_name}"},
    )

    db.commit()
    return {"message": "Heslo bolo \u00faspe\u0161ne zmenen\u00e9"}
