import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hardware import MockI2CBus
from rules import compute_setpoints


def test_mock_bus_roundtrip_through_rules():
    bus = MockI2CBus(temperature_c=15.0, humidity_pct=40.0, ldr_raw=300, button=1)
    temperature_c, humidity_pct, ldr_raw, button = bus.read_sensor_arduino()

    fan_pwm, valve_angle = compute_setpoints(temperature_c)
    bus.write_actor_setpoints(fan_pwm, valve_angle)

    assert (humidity_pct, ldr_raw, button) == (40.0, 300, 1)
    assert bus.last_actor_setpoints == (fan_pwm, valve_angle)
    assert valve_angle > 0
