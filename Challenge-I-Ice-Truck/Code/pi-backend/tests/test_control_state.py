import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import control_state


def test_read_state_defaults_to_auto_when_file_missing(tmp_path):
    state = control_state.read_state(path=str(tmp_path / "does_not_exist.json"))
    assert state == control_state.DEFAULT_STATE


def test_write_field_persists_and_merges(tmp_path):
    path = str(tmp_path / "control_state.json")
    control_state.write_field("mode", "manual", path=path)
    control_state.write_field("fan_pwm", 200, path=path)

    state = control_state.read_state(path=path)
    assert state == {"mode": "manual", "fan_pwm": 200, "valve_angle": 0}


def test_write_field_rejects_unknown_field(tmp_path):
    path = str(tmp_path / "control_state.json")
    try:
        control_state.write_field("fan_speed", 1, path=path)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_read_state_ignores_corrupt_file(tmp_path):
    path = tmp_path / "control_state.json"
    path.write_text("not json", encoding="utf-8")
    assert control_state.read_state(path=str(path)) == control_state.DEFAULT_STATE
