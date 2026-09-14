import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import db


def test_log_reading_persists_row(tmp_path):
    conn = db.connect(str(tmp_path / "test.db"))
    db.log_reading(
        conn,
        temperature_c=15.5,
        humidity_pct=42.0,
        ldr_raw=512,
        button=1,
        fan_pwm=180,
        valve_angle=90,
    )

    row = conn.execute(
        "SELECT temperature_c, humidity_pct, ldr_raw, button, fan_pwm, valve_angle FROM readings"
    ).fetchone()
    assert row == (15.5, 42.0, 512, 1, 180, 90)


def test_connect_is_idempotent(tmp_path):
    db_path = str(tmp_path / "test.db")
    db.connect(db_path)
    conn = db.connect(db_path)
    db.log_reading(
        conn,
        temperature_c=0.0,
        humidity_pct=0.0,
        ldr_raw=0,
        button=0,
        fan_pwm=0,
        valve_angle=0,
    )
    count = conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
    assert count == 1
