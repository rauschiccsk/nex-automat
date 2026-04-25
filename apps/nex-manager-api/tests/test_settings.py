"""Tests for settings module (Track 2 Phase 2.2) — list / get / update."""

from __future__ import annotations

from datetime import datetime, timezone


def test_list_settings_empty(client, fake_db):
    """GET /api/system/settings returns empty list when no rows."""
    fake_db.set_fetchall_sequence([[]])
    response = client.get("/api/system/settings")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["settings"] == []


def test_list_settings_with_rows(client, fake_db):
    """GET returns rows mapped to SettingResponse."""
    now = datetime(2026, 4, 25, 17, 0, 0, tzinfo=timezone.utc)
    fake_db.set_fetchall_sequence(
        [
            [
                (
                    "ui.search_debounce_ms",
                    300,
                    "global",
                    "ui",
                    "Search debounce",
                    None,
                    now,
                    now,
                ),
            ],
        ]
    )
    response = client.get("/api/system/settings")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["settings"][0]["setting_key"] == "ui.search_debounce_ms"
    assert body["settings"][0]["value"] == 300


def test_get_setting_not_found(client, fake_db):
    """GET /{key} returns 404 if missing."""
    fake_db.set_fetchone_sequence([None])
    response = client.get("/api/system/settings/nonexistent.key")
    assert response.status_code == 404
    assert "nebolo nájdené" in response.json()["detail"]


def test_update_setting_succeeds(client, fake_db):
    """PUT /{key} updates value and returns updated row."""
    now = datetime(2026, 4, 25, 17, 0, 0, tzinfo=timezone.utc)
    fake_db.set_fetchone_sequence(
        [
            (
                "ui.search_debounce_ms",
                500,
                "global",
                "ui",
                "Search debounce",
                "admin",
                now,
                now,
            ),
        ]
    )
    response = client.put(
        "/api/system/settings/ui.search_debounce_ms",
        json={"value": 500},
    )
    assert response.status_code == 200
    assert response.json()["value"] == 500
