import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import db


def test_log_reading_persists_row(tmp_path):
    conn = db.connect(str(tmp_path / "test.db"))
    db.log_reading(
        conn,
        sensor_board_raw=512,
        sensor_board_temp_c=15.5,
        sensor_board_digital=1,
        actor_board_raw=480,
        actor_board_temp_c=16.0,
        fan_pwm=180,
        valve_angle=90,
    )

    row = conn.execute(
        "SELECT sensor_board_raw, sensor_board_temp_c, sensor_board_digital, actor_board_raw, "
        "actor_board_temp_c, fan_pwm, valve_angle FROM readings"
    ).fetchone()
    assert row == (512, 15.5, 1, 480, 16.0, 180, 90)


def test_connect_is_idempotent(tmp_path):
    db_path = str(tmp_path / "test.db")
    db.connect(db_path)
    conn = db.connect(db_path)
    db.log_reading(
        conn,
        sensor_board_raw=0,
        sensor_board_temp_c=0.0,
        sensor_board_digital=0,
        actor_board_raw=0,
        actor_board_temp_c=0.0,
        fan_pwm=0,
        valve_angle=0,
    )
    count = conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
    assert count == 1


def test_connect_migrates_pre_digital_schema(tmp_path):
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp_utc TEXT NOT NULL,
            sensor_board_raw INTEGER NOT NULL,
            sensor_board_temp_c REAL NOT NULL,
            actor_board_raw INTEGER NOT NULL,
            actor_board_temp_c REAL NOT NULL,
            fan_pwm INTEGER NOT NULL,
            valve_angle INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

    conn = db.connect(db_path)
    db.log_reading(
        conn,
        sensor_board_raw=1,
        sensor_board_temp_c=1.0,
        sensor_board_digital=1,
        actor_board_raw=1,
        actor_board_temp_c=1.0,
        fan_pwm=1,
        valve_angle=1,
    )
    row = conn.execute("SELECT sensor_board_digital FROM readings").fetchone()
    assert row == (1,)
