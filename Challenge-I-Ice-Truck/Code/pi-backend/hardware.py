"""I2C-Zugriff fuer Challenge I Track C/E, real und gemockt.

Der reale Bus (RealI2CBus) braucht smbus2 und ein tatsaechliches I2C-Geraet
unter /dev/i2c-1 - beides in dieser Sandbox nicht vorhanden. MockI2CBus
liefert stattdessen fest einprogrammierte/aenderbare Werte, analog zum
socat-Mock-Muster aus Tresor-Kurzprojekt/Code/pi-dashboard (siehe
"Erweiterung - Raspberry Pi Dashboard.md", Abschnitt "Software-Test mit
simuliertem Arduino").
"""

from __future__ import annotations

SENSOR_ARDUINO_ADDRESS = 0x08
ACTOR_ARDUINO_ADDRESS = 0x09


class I2CBus:
    def read_sensor_arduino(self) -> tuple[int, bool]:
        raise NotImplementedError

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        raise NotImplementedError


class RealI2CBus(I2CBus):
    def __init__(self, bus_number: int = 1) -> None:
        import smbus2

        self._bus = smbus2.SMBus(bus_number)

    def read_sensor_arduino(self) -> tuple[int, bool]:
        data = self._bus.read_i2c_block_data(SENSOR_ARDUINO_ADDRESS, 0, 3)
        analog_raw = (data[0] << 8) | data[1]
        door_open = bool(data[2])
        return analog_raw, door_open

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        self._bus.write_i2c_block_data(
            ACTOR_ARDUINO_ADDRESS, 0, [fan_pwm, valve_angle]
        )


class MockI2CBus(I2CBus):
    def __init__(self, analog_raw: int = 0, door_open: bool = False) -> None:
        self.analog_raw = analog_raw
        self.door_open = door_open
        self.last_actor_setpoints: tuple[int, int] | None = None

    def read_sensor_arduino(self) -> tuple[int, bool]:
        return self.analog_raw, self.door_open

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        self.last_actor_setpoints = (fan_pwm, valve_angle)
