import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import db


def test_log_reading_persists_row(tmp_path):
    conn = db.connect(str(tmp_path / "test.db"))
    db.log_reading(conn, analog_raw=812, door_open=True, fan_pwm=180, valve_angle=0)

    row = conn.execute(
        "SELECT analog_raw, door_open, fan_pwm, valve_angle FROM readings"
    ).fetchone()
    assert row == (812, 1, 180, 0)


def test_connect_is_idempotent(tmp_path):
    db_path = str(tmp_path / "test.db")
    db.connect(db_path)
    conn = db.connect(db_path)
    db.log_reading(conn, analog_raw=0, door_open=False, fan_pwm=0, valve_angle=0)
    count = conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
    assert count == 1
