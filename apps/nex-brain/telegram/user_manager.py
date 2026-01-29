"""
User Manager - správa používateľov a schvaľovanie
"""

import logging
from typing import Any

from db import get_connection

logger = logging.getLogger(__name__)


class UserManager:
    """Správa Telegram používateľov"""

    @staticmethod
    def get_user(user_id: int, tenant: str) -> dict[str, Any] | None:
        """Získanie používateľa podľa user_id a tenant"""
        conn = get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, user_id, username, first_name, tenant, status, 
                       requested_at, approved_at, approved_by
                FROM telegram_users 
                WHERE user_id = %s AND tenant = %s
                """,
                (user_id, tenant),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "username": row[2],
                    "first_name": row[3],
                    "tenant": row[4],
                    "status": row[5],
                    "requested_at": row[6],
                    "approved_at": row[7],
                    "approved_by": row[8],
                }
            return None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            if conn:
                conn.close()
            return None

    @staticmethod
    def is_approved(user_id: int, tenant: str) -> bool:
        """Kontrola či je používateľ schválený"""
        user = UserManager.get_user(user_id, tenant)
        return user is not None and user["status"] == "approved"

    @staticmethod
    def is_pending(user_id: int, tenant: str) -> bool:
        """Kontrola či používateľ čaká na schválenie"""
        user = UserManager.get_user(user_id, tenant)
        return user is not None and user["status"] == "pending"

    @staticmethod
    def request_access(user_id: int, username: str, first_name: str, tenant: str) -> bool:
        """Vytvorenie žiadosti o prístup"""
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO telegram_users (user_id, username, first_name, tenant, status)
                VALUES (%s, %s, %s, %s, 'pending')
                ON CONFLICT (user_id, tenant) DO NOTHING
                """,
                (user_id, username, first_name, tenant),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error requesting access: {e}")
            if conn:
                conn.close()
            return False

    @staticmethod
    def approve_user(user_id: int, tenant: str, approved_by: int) -> bool:
        """Schválenie používateľa"""
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE telegram_users 
                SET status = 'approved', approved_at = NOW(), approved_by = %s
                WHERE user_id = %s AND tenant = %s
                """,
                (approved_by, user_id, tenant),
            )
            affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            return affected > 0
        except Exception as e:
            logger.error(f"Error approving user: {e}")
            if conn:
                conn.close()
            return False

    @staticmethod
    def reject_user(user_id: int, tenant: str) -> bool:
        """Zamietnutie používateľa"""
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE telegram_users 
                SET status = 'rejected'
                WHERE user_id = %s AND tenant = %s
                """,
                (user_id, tenant),
            )
            affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            return affected > 0
        except Exception as e:
            logger.error(f"Error rejecting user: {e}")
            if conn:
                conn.close()
            return False

    @staticmethod
    def get_pending_users(tenant: str | None = None) -> list[dict[str, Any]]:
        """Získanie zoznamu čakajúcich používateľov"""
        conn = get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            if tenant:
                cursor.execute(
                    """
                    SELECT id, user_id, username, first_name, tenant, requested_at
                    FROM telegram_users 
                    WHERE status = 'pending' AND tenant = %s
                    ORDER BY requested_at
                    """,
                    (tenant,),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, user_id, username, first_name, tenant, requested_at
                    FROM telegram_users 
                    WHERE status = 'pending'
                    ORDER BY requested_at
                    """
                )

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            return [
                {
                    "id": row[0],
                    "user_id": row[1],
                    "username": row[2],
                    "first_name": row[3],
                    "tenant": row[4],
                    "requested_at": row[5],
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting pending users: {e}")
            if conn:
                conn.close()
            return []

    @staticmethod
    def get_approved_users(tenant: str | None = None) -> list[dict[str, Any]]:
        """Získanie zoznamu schválených používateľov"""
        conn = get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            if tenant:
                cursor.execute(
                    """
                    SELECT id, user_id, username, first_name, tenant, approved_at
                    FROM telegram_users 
                    WHERE status = 'approved' AND tenant = %s
                    ORDER BY approved_at DESC
                    """,
                    (tenant,),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, user_id, username, first_name, tenant, approved_at
                    FROM telegram_users 
                    WHERE status = 'approved'
                    ORDER BY approved_at DESC
                    """
                )

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            return [
                {
                    "id": row[0],
                    "user_id": row[1],
                    "username": row[2],
                    "first_name": row[3],
                    "tenant": row[4],
                    "approved_at": row[5],
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting approved users: {e}")
            if conn:
                conn.close()
            return []


class AdminManager:
    """Správa admin používateľov"""

    @staticmethod
    def is_admin(user_id: int) -> bool:
        """Kontrola či je používateľ admin"""
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM telegram_admins WHERE user_id = %s", (user_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return row is not None
        except Exception as e:
            logger.error(f"Error checking admin: {e}")
            if conn:
                conn.close()
            return False

    @staticmethod
    def add_admin(user_id: int, username: str) -> bool:
        """Pridanie admina"""
        conn = get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO telegram_admins (user_id, username)
                VALUES (%s, %s)
                ON CONFLICT (user_id) DO NOTHING
                """,
                (user_id, username),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding admin: {e}")
            if conn:
                conn.close()
            return False
