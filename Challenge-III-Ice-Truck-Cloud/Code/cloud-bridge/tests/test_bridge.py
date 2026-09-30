import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(ROOT / "Challenge-I-Ice-Truck" / "Code" / "pi-backend"))

import bridge
import db


class FakeSender:
    def __init__(self, fail_after=None):
        self.messages = []
        self.fail_after = fail_after

    def send(self, body, properties):
        if self.fail_after is not None and len(self.messages) >= self.fail_after:
            raise ConnectionError("kein Netz")
        self.messages.append((json.loads(body), properties))


def _log(conn, temp=5.0, other=None, raw=600):
    db.log_reading(conn, raw, temp, 0, raw, temp if other is None else other, 0, 0)


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "challenge_i.db")


def test_first_start_now_skips_existing_rows(db_path, tmp_path):
    conn = db.connect(db_path)
    for _ in range(3):
        _log(conn)
    sender = FakeSender()
    state = str(tmp_path / "state.json")

    assert bridge.send_pending(conn, sender, state, start_from="now") == 0
    _log(conn)
    assert bridge.send_pending(conn, sender, state, start_from="now") == 1
    assert sender.messages[0][0]["rows"][0][0] == 4


def test_start_all_sends_backlog_in_batches(db_path, tmp_path):
    conn = db.connect(db_path)
    for _ in range(25):
        _log(conn)
    sender = FakeSender()
    sent = bridge.send_pending(
        conn, sender, str(tmp_path / "s.json"), max_rows=10, max_messages=5, start_from="all"
    )
    assert sent == 25
    assert [len(m[0]["rows"]) for m in sender.messages] == [10, 10, 5]
    body = sender.messages[0][0]
    assert body["cols"] == bridge.COLUMNS
    assert body["truck_id"] == bridge.TRUCK_ID


def test_max_messages_limits_catch_up(db_path, tmp_path):
    conn = db.connect(db_path)
    for _ in range(25):
        _log(conn)
    sender = FakeSender()
    state = str(tmp_path / "s.json")
    assert bridge.send_pending(conn, sender, state, max_rows=10, max_messages=1, start_from="all") == 10
    assert bridge.load_state(state)["last_sent_id"] == 10


def test_cursor_stays_on_failure_and_resends_later(db_path, tmp_path):
    conn = db.connect(db_path)
    for _ in range(20):
        _log(conn)
    state = str(tmp_path / "s.json")
    failing = FakeSender(fail_after=1)
    with pytest.raises(ConnectionError):
        bridge.send_pending(conn, failing, state, max_rows=10, start_from="all")
    assert bridge.load_state(state)["last_sent_id"] == 10

    ok = FakeSender()
    assert bridge.send_pending(conn, ok, state, max_rows=10, start_from="all") == 10
    assert ok.messages[0][0]["rows"][0][0] == 11


def test_health_flags(db_path):
    conn = db.connect(db_path)
    _log(conn, temp=30.0)
    _log(conn, temp=5.0, other=10.0)
    rows = bridge.fetch_batch(conn, 0, 10)
    body, props = bridge.build_message(rows, "t1", alarm_temp_c=28.0, mismatch_c=3.0)
    assert json.loads(body)["flags"] == ["temp_high", "sensor_mismatch"]
    assert props["alarm"] == "true"


def test_sensor_stuck_needs_full_batch(db_path):
    conn = db.connect(db_path)
    for _ in range(12):
        _log(conn, raw=600)
    rows = bridge.fetch_batch(conn, 0, 20)
    assert bridge.health_flags(rows, 28.0, 3.0) == ["sensor_stuck"]
    assert bridge.health_flags(rows[:5], 28.0, 3.0) == []


def test_no_flags_means_no_alarm(db_path):
    conn = db.connect(db_path)
    _log(conn, temp=4.0)
    body, props = bridge.build_message(bridge.fetch_batch(conn, 0, 10), "t1", 28.0, 3.0)
    assert props == {"schema": "icetruck-v1", "truck_id": "t1", "alarm": "false", "flags": ""}
    assert json.loads(body)["min_temp_c"] == 4.0


def test_open_db_is_read_only(db_path):
    db.connect(db_path).close()
    conn = bridge.open_db(db_path)
    with pytest.raises(Exception):
        conn.execute("DELETE FROM readings")
