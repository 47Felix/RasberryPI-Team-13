import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import rules


def test_below_fan_threshold_everything_off():
    fan_pwm, valve_angle = rules.compute_setpoints(analog_raw=100, door_open=False)
    assert fan_pwm == 0
    assert valve_angle == 0


def test_between_thresholds_fan_only():
    fan_pwm, valve_angle = rules.compute_setpoints(analog_raw=700, door_open=False)
    assert fan_pwm > 0
    assert valve_angle == 0


def test_above_valve_threshold_both_active():
    fan_pwm, valve_angle = rules.compute_setpoints(analog_raw=1000, door_open=False)
    assert fan_pwm > 0
    assert valve_angle > 0


def test_max_reading_hits_max_setpoints():
    fan_pwm, valve_angle = rules.compute_setpoints(
        analog_raw=rules.ANALOG_MAX, door_open=False
    )
    assert fan_pwm == rules.MAX_FAN_PWM
    assert valve_angle == rules.MAX_VALVE_ANGLE


def test_door_open_boosts_fan_but_not_beyond_max():
    closed_fan, _ = rules.compute_setpoints(analog_raw=700, door_open=False)
    open_fan, _ = rules.compute_setpoints(analog_raw=700, door_open=True)
    assert open_fan > closed_fan
    assert open_fan <= rules.MAX_FAN_PWM


def test_door_open_with_fan_already_off_stays_off():
    fan_pwm, _ = rules.compute_setpoints(analog_raw=100, door_open=True)
    assert fan_pwm == 0
