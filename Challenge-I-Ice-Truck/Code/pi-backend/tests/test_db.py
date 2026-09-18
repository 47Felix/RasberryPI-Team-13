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
        actor_board_raw=480,
        actor_board_temp_c=16.0,
        fan_pwm=180,
        valve_angle=90,
    )

    row = conn.execute(
        "SELECT sensor_board_raw, sensor_board_temp_c, actor_board_raw, actor_board_temp_c, "
        "fan_pwm, valve_angle FROM readings"
    ).fetchone()
    assert row == (512, 15.5, 480, 16.0, 180, 90)


def test_connect_is_idempotent(tmp_path):
    db_path = str(tmp_path / "test.db")
    db.connect(db_path)
    conn = db.connect(db_path)
    db.log_reading(
        conn,
        sensor_board_raw=0,
        sensor_board_temp_c=0.0,
        actor_board_raw=0,
        actor_board_temp_c=0.0,
        fan_pwm=0,
        valve_angle=0,
    )
    count = conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
    assert count == 1
