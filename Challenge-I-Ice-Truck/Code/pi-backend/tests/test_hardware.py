import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hardware import MockI2CBus
from rules import compute_setpoints


def test_mock_bus_roundtrip_through_rules():
    bus = MockI2CBus(temperature_c=15.0, humidity_pct=40.0, analog_raw=300)
    analog_raw = bus.read_sensor_board()
    temperature_c, humidity_pct = bus.read_actor_board_climate()

    fan_pwm, valve_angle = compute_setpoints(temperature_c)
    bus.write_actor_setpoints(fan_pwm, valve_angle)

    assert (humidity_pct, analog_raw) == (40.0, 300)
    assert bus.last_actor_setpoints == (fan_pwm, valve_angle)
    assert valve_angle > 0
