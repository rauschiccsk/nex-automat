"""Test for self-deactivation guard in update_user endpoint.

Regression: 2026-04-25 — admin user (id=1) self-deactivated via UI toggle,
locked out of system (get_current_user is_active check rejects all subsequent
requests with 401). Guard added in users/router.update_user to reject
PUT /api/users/{id} where id == current_user.user_id and is_active is False.
"""

from __future__ import annotations


def test_update_user_blocks_self_deactivation(client, fake_user):
    """PUT /api/users/{self} with is_active=false → 400 'Nemôžete deaktivovať vlastný účet'."""
    response = client.put(
        f"/api/users/{fake_user['user_id']}",
        json={"is_active": False},
    )
    assert response.status_code == 400
    assert "deaktivovať vlastný účet" in response.json()["detail"]
