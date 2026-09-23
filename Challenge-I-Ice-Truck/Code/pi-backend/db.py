"""SQLite-Logging fuer Challenge I Track F, gleiches Muster wie tresor.db
in Tresor-Kurzprojekt/Code/pi-dashboard/app.py."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_utc TEXT NOT NULL,
    sensor_board_raw INTEGER NOT NULL,
    sensor_board_temp_c REAL NOT NULL,
    sensor_board_digital INTEGER NOT NULL,
    actor_board_raw INTEGER NOT NULL,
    actor_board_temp_c REAL NOT NULL,
    fan_pwm INTEGER NOT NULL,
    valve_angle INTEGER NOT NULL
);
"""


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(SCHEMA)
    # Bestehende readings-Tabellen von vor der KY-028-D0-Anbindung (siehe
    # sensor_arduino.ino) haben die Spalte noch nicht - CREATE TABLE IF NOT
    # EXISTS aendert eine bereits existierende Tabelle nicht, daher hier per
    # ALTER TABLE nachziehen statt die DB-Datei manuell umbenennen zu muessen.
    try:
        conn.execute(
            "ALTER TABLE readings ADD COLUMN sensor_board_digital INTEGER NOT NULL DEFAULT 0"
        )
    except sqlite3.OperationalError:
        pass
    conn.commit()
    return conn


def log_reading(
    conn: sqlite3.Connection,
    sensor_board_raw: int,
    sensor_board_temp_c: float,
    sensor_board_digital: int,
    actor_board_raw: int,
    actor_board_temp_c: float,
    fan_pwm: int,
    valve_angle: int,
) -> None:
    conn.execute(
        "INSERT INTO readings (timestamp_utc, sensor_board_raw, sensor_board_temp_c, "
        "sensor_board_digital, actor_board_raw, actor_board_temp_c, fan_pwm, valve_angle) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            datetime.now(timezone.utc).isoformat(),
            sensor_board_raw,
            sensor_board_temp_c,
            sensor_board_digital,
            actor_board_raw,
            actor_board_temp_c,
            fan_pwm,
            valve_angle,
        ),
    )
    conn.commit()
