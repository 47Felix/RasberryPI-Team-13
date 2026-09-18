import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import rules
from hardware import MockI2CBus
from rules import compute_setpoints


def test_mock_bus_roundtrip_through_rules():
    bus = MockI2CBus(sensor_board_raw=300, actor_board_raw=320)
    sensor_board_raw = bus.read_sensor_board()
    actor_board_raw = bus.read_actor_board()

    fan_pwm, valve_angle = compute_setpoints(temperature_c=rules.VALVE_ON_TEMP_C + 1.0)
    bus.write_actor_setpoints(fan_pwm, valve_angle)

    assert (sensor_board_raw, actor_board_raw) == (300, 320)
    assert bus.last_actor_setpoints == (fan_pwm, valve_angle)
    assert valve_angle > 0
