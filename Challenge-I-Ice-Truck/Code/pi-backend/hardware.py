"""I2C-Zugriff fuer Challenge I Track C+E, real und gemockt.

Der reale Bus (RealI2CBus) braucht smbus2 und ein tatsaechliches I2C-Geraet
unter /dev/i2c-1. MockI2CBus liefert stattdessen fest einprogrammierte/
aenderbare Werte, analog zum socat-Mock-Muster aus
Tresor-Kurzprojekt/Code/pi-dashboard.

Zwei-Board-Aufbau (siehe README "Hardware-Update 4"), zwei I2C-Adressen:
  - SENSOR_ARDUINO_ADDRESS (0x08, sensor_arduino.ino): KY-028-Rohwert
    (analog, unkalibriert) + Tuerkontakt. Lese-Format 3 Bytes.
  - ACTOR_ARDUINO_ADDRESS (0x09, actor_arduino.ino): DHT22 Temperatur/
    Feuchte (dort haengt der Sensor physisch, nicht am Sensor-Board) und
    nimmt Luefter-/Ventil-Sollwerte entgegen. Lese-Format 4 Bytes
    (Temperatur/Feuchte, je int16 Zehntel), Schreib-Format 3 Bytes.

Schreib-Format (3 Bytes) entspricht receiveActorSetpoints() im
actor_arduino.ino: ein ungenutztes Platzhalter-"Register"-Byte (Artefakt
von smbus2.write_i2c_block_data(), das immer ein Register vor den Daten
erwartet - der Arduino hat keine echten Register), dann fan_pwm (0-255)
und valve_angle (0-180).
"""

from __future__ import annotations

import time

SENSOR_ARDUINO_ADDRESS = 0x08
ACTOR_ARDUINO_ADDRESS = 0x09

# I2C-Lesefehler (OSError, z.B. Errno 121 "Remote I/O error") kommen bei
# dieser Verkabelung gelegentlich vor - beobachtet z.B. sobald Luefter/Servo
# aktiv sind (Vibration auf einer noch nicht fest verbundenen SDA/SCL-
# Leitung, siehe README "I2C-Verkabelung ... pruefen"). Kurzer Retry statt
# sofortigem Absturz, bis die Verkabelung/Pull-ups fest sitzen.
I2C_READ_RETRIES = 3
I2C_RETRY_DELAY_SECONDS = 0.05


class I2CBus:
    def read_sensor_board(self) -> tuple[int, int]:
        raise NotImplementedError

    def read_actor_board_climate(self) -> tuple[float, float]:
        raise NotImplementedError

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        raise NotImplementedError


class RealI2CBus(I2CBus):
    def __init__(self, bus_number: int = 1) -> None:
        import smbus2

        self._bus = smbus2.SMBus(bus_number)

    def _read_block_with_retry(self, address: int, length: int) -> list[int]:
        last_error: OSError | None = None
        for attempt in range(1, I2C_READ_RETRIES + 1):
            try:
                return self._bus.read_i2c_block_data(address, 0, length)
            except OSError as exc:
                last_error = exc
                if attempt < I2C_READ_RETRIES:
                    time.sleep(I2C_RETRY_DELAY_SECONDS)
        assert last_error is not None
        raise last_error

    def read_sensor_board(self) -> tuple[int, int]:
        data = self._read_block_with_retry(SENSOR_ARDUINO_ADDRESS, 3)
        analog_raw = (data[0] << 8) | data[1]
        door_open = data[2]
        return analog_raw, door_open

    def read_actor_board_climate(self) -> tuple[float, float]:
        data = self._read_block_with_retry(ACTOR_ARDUINO_ADDRESS, 4)
        temperature_c = _signed16(data[0], data[1]) / 10.0
        humidity_pct = _signed16(data[2], data[3]) / 10.0
        return temperature_c, humidity_pct

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        # receiveActorSetpoints() in actor_arduino.ino erwartet genau 3
        # Bytes; das fuehrende 0 ist nur das von write_i2c_block_data()
        # erzwungene Register-Byte, wird ignoriert.
        self._bus.write_i2c_block_data(ACTOR_ARDUINO_ADDRESS, 0, [fan_pwm, valve_angle])


def _signed16(high_byte: int, low_byte: int) -> int:
    value = (high_byte << 8) | low_byte
    return value - 0x10000 if value >= 0x8000 else value


class MockI2CBus(I2CBus):
    def __init__(
        self,
        temperature_c: float = 20.0,
        humidity_pct: float = 50.0,
        analog_raw: int = 0,
        door_open: int = 0,
    ) -> None:
        self.temperature_c = temperature_c
        self.humidity_pct = humidity_pct
        self.analog_raw = analog_raw
        self.door_open = door_open
        self.last_actor_setpoints: tuple[int, int] | None = None

    def read_sensor_board(self) -> tuple[int, int]:
        return self.analog_raw, self.door_open

    def read_actor_board_climate(self) -> tuple[float, float]:
        return self.temperature_c, self.humidity_pct

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        self.last_actor_setpoints = (fan_pwm, valve_angle)
