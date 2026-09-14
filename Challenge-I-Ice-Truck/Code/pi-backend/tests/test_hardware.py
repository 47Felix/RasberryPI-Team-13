import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hardware import MockI2CBus
from rules import compute_setpoints


def test_mock_bus_roundtrip_through_rules():
    bus = MockI2CBus(analog_raw=900, door_open=False)
    analog_raw, door_open = bus.read_sensor_arduino()
    fan_pwm, valve_angle = compute_setpoints(analog_raw, door_open)
    bus.write_actor_setpoints(fan_pwm, valve_angle)

    assert bus.last_actor_setpoints == (fan_pwm, valve_angle)
    assert valve_angle > 0
