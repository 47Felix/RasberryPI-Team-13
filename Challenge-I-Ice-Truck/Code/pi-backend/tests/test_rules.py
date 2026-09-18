import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import rules


def test_below_fan_threshold_everything_off():
    fan_pwm, valve_angle = rules.compute_setpoints(temperature_c=rules.FAN_ON_TEMP_C - 1.0)
    assert fan_pwm == 0
    assert valve_angle == 0


def test_fan_stage_runs_fan_but_not_valve():
    fan_pwm, valve_angle = rules.compute_setpoints(temperature_c=rules.FAN_ON_TEMP_C + 1.0)
    assert fan_pwm > 0
    assert valve_angle == 0


def test_valve_stage_opens_valve_and_keeps_fan_at_or_above_fan_stage():
    fan_pwm_light, _ = rules.compute_setpoints(temperature_c=rules.FAN_ON_TEMP_C + 1.0)
    fan_pwm_strong, valve_angle = rules.compute_setpoints(temperature_c=rules.VALVE_ON_TEMP_C + 1.0)
    assert valve_angle > 0
    assert fan_pwm_strong >= fan_pwm_light


def test_high_temperature_hits_max_setpoints():
    hottest_threshold = max(rules.FAN_ON_TEMP_C, rules.VALVE_ON_TEMP_C)
    fan_pwm, valve_angle = rules.compute_setpoints(temperature_c=hottest_threshold + rules.TEMP_SPAN_C + 1.0)
    assert fan_pwm == rules.MAX_FAN_PWM
    assert valve_angle == rules.MAX_VALVE_ANGLE


def test_fan_starts_at_minimum_just_above_threshold():
    fan_pwm, _ = rules.compute_setpoints(temperature_c=rules.FAN_ON_TEMP_C + 0.01)
    assert fan_pwm == rules.MIN_FAN_PWM_WHEN_ON


def test_valve_starts_at_minimum_just_above_threshold():
    _, valve_angle = rules.compute_setpoints(temperature_c=rules.VALVE_ON_TEMP_C + 0.01)
    assert valve_angle == rules.MIN_VALVE_ANGLE_WHEN_ON
