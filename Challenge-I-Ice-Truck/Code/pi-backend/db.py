"""SQLite-Logging fuer Challenge I Track F, gleiches Muster wie tresor.db
in Tresor-Kurzprojekt/Code/pi-dashboard/app.py."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc TEXT NOT NULL,
    analog_raw INTEGER NOT NULL,
    door_open INTEGER NOT NULL,
    fan_pwm INTEGER NOT NULL,
    valve_angle INTEGER NOT NULL
);
"""


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(SCHEMA)
    conn.commit()
    return conn


def log_reading(
    conn: sqlite3.Connection,
    analog_raw: int,
    door_open: bool,
    fan_pwm: int,
    valve_angle: int,
) -> None:
    conn.execute(
        "INSERT INTO readings (timestamp_utc, analog_raw, door_open, fan_pwm, valve_angle) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            datetime.now(timezone.utc).isoformat(),
            analog_raw,
            int(door_open),
            fan_pwm,
            valve_angle,
        ),
    )
    conn.commit()
