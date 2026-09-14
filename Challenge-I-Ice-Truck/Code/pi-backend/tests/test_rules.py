import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import rules


def test_below_light_threshold_everything_off():
    fan_pwm, valve_angle = rules.compute_setpoints(analog_raw=100, door_open=False)
    assert fan_pwm == 0
    assert valve_angle == 0


def test_light_stage_opens_valve_partially():
    fan_pwm, valve_angle = rules.compute_setpoints(analog_raw=700, door_open=False)
    assert 0 < valve_angle <= rules.LIGHT_STAGE_MAX_ANGLE


def test_strong_stage_opens_valve_further_than_light_stage():
    _, light_angle = rules.compute_setpoints(analog_raw=700, door_open=False)
    _, strong_angle = rules.compute_setpoints(analog_raw=1000, door_open=False)
    assert strong_angle > light_angle
    assert strong_angle > rules.LIGHT_STAGE_MAX_ANGLE


def test_max_reading_hits_max_valve_angle():
    _, valve_angle = rules.compute_setpoints(
        analog_raw=rules.ANALOG_MAX, door_open=False
    )
    assert valve_angle == rules.MAX_VALVE_ANGLE


def test_fan_pwm_still_computed_as_unwired_stub():
    fan_pwm, _ = rules.compute_setpoints(analog_raw=rules.ANALOG_MAX, door_open=False)
    assert fan_pwm == rules.MAX_FAN_PWM


def test_door_open_boosts_valve_but_not_beyond_max():
    closed_angle = rules.compute_setpoints(analog_raw=700, door_open=False)[1]
    open_angle = rules.compute_setpoints(analog_raw=700, door_open=True)[1]
    assert open_angle > closed_angle
    assert open_angle <= rules.MAX_VALVE_ANGLE


def test_door_open_with_valve_already_closed_stays_closed():
    _, valve_angle = rules.compute_setpoints(analog_raw=100, door_open=True)
    assert valve_angle == 0
