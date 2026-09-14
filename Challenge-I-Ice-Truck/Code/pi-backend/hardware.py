"""I2C-Zugriff fuer Challenge I Track C, real und gemockt.

Der reale Bus (RealI2CBus) braucht smbus2 und ein tatsaechliches I2C-Geraet
unter /dev/i2c-1. MockI2CBus liefert stattdessen fest einprogrammierte/
aenderbare Werte, analog zum socat-Mock-Muster aus
Tresor-Kurzprojekt/Code/pi-dashboard.

Byte-Format (7 Bytes) entspricht sendSensorDataToPi() in
ice_truck_single_board.ino: Temperatur (int16, Zehntelgrad), Feuchte
(int16, Zehntelprozent), LDR-Rohwert (uint16), Taster-Zustand (uint8).
Das aeltere 3-Byte-Format (analog_raw, door_open) passte zum urspruenglichen
Zwei-Board-Entwurf (sensor_arduino.ino) und existiert auf der tatsaechlich
verkabelten Hardware nicht mehr.
"""

from __future__ import annotations

import time

SENSOR_ARDUINO_ADDRESS = 0x08

# I2C-Lesefehler (OSError, z.B. Errno 121 "Remote I/O error") kommen bei
# dieser Verkabelung gelegentlich vor - beobachtet z.B. sobald Luefter/Servo
# aktiv sind (Vibration auf einer noch nicht fest verbundenen SDA/SCL-
# Leitung, siehe README "I2C-Verkabelung ... pruefen"). Kurzer Retry statt
# sofortigem Absturz, bis die Verkabelung/Pull-ups fest sitzen.
I2C_READ_RETRIES = 3
I2C_RETRY_DELAY_SECONDS = 0.05

# Kalibrierungs-Offset fuer den DHT11 (konstant ca. 20-22 Grad zu niedrig,
# siehe README/ice_truck_single_board.ino) wird direkt in der Firmware
# angewendet (DHT11_TEMPERATURE_OFFSET_C im Sketch), nicht mehr hier - sonst
# wuerde er doppelt zaehlen. Die 7 Bytes von sendSensorDataToPi() enthalten
# bereits die kalibrierte Temperatur.


class I2CBus:
    def read_sensor_arduino(self) -> tuple[float, float, int, int]:
        raise NotImplementedError

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        raise NotImplementedError


class RealI2CBus(I2CBus):
    def __init__(self, bus_number: int = 1) -> None:
        import smbus2

        self._bus = smbus2.SMBus(bus_number)

    def read_sensor_arduino(self) -> tuple[float, float, int, int]:
        last_error: OSError | None = None
        for attempt in range(1, I2C_READ_RETRIES + 1):
            try:
                data = self._bus.read_i2c_block_data(SENSOR_ARDUINO_ADDRESS, 0, 7)
                break
            except OSError as exc:
                last_error = exc
                if attempt < I2C_READ_RETRIES:
                    time.sleep(I2C_RETRY_DELAY_SECONDS)
        else:
            assert last_error is not None
            raise last_error

        temperature_c = _signed16(data[0], data[1]) / 10.0
        humidity_pct = _signed16(data[2], data[3]) / 10.0
        ldr_raw = (data[4] << 8) | data[5]
        button = data[6]
        return temperature_c, humidity_pct, ldr_raw, button

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        # Auf der tatsaechlich verkabelten Hardware (EIN Arduino, siehe
        # ice_truck_single_board.ino) laeuft applyCoolingStage() lokal auf
        # dem Arduino - es gibt keinen zweiten Arduino/keine eigene
        # I2C-Adresse fuer Aktorik mehr, und der Sketch hat (noch) keinen
        # Wire.onReceive()-Handler, der Setpoints vom Pi entgegennehmen
        # wuerde. Bleibt Stub fuer Issue #180, bis das Firmware-seitig da ist.
        raise NotImplementedError(
            "Aktor-Setpoints per I2C schreiben ist noch nicht angebunden (Issue #180) - "
            "die Kuehlstufe wird aktuell lokal auf dem Arduino berechnet und angewendet."
        )


def _signed16(high_byte: int, low_byte: int) -> int:
    value = (high_byte << 8) | low_byte
    return value - 0x10000 if value >= 0x8000 else value


class MockI2CBus(I2CBus):
    def __init__(
        self,
        temperature_c: float = 20.0,
        humidity_pct: float = 50.0,
        ldr_raw: int = 0,
        button: int = 0,
    ) -> None:
        self.temperature_c = temperature_c
        self.humidity_pct = humidity_pct
        self.ldr_raw = ldr_raw
        self.button = button
        self.last_actor_setpoints: tuple[int, int] | None = None

    def read_sensor_arduino(self) -> tuple[float, float, int, int]:
        return self.temperature_c, self.humidity_pct, self.ldr_raw, self.button

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        self.last_actor_setpoints = (fan_pwm, valve_angle)
