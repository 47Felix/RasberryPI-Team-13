"""I2C-Zugriff fuer Challenge I Track C+E, real und gemockt.

Der reale Bus (RealI2CBus) braucht smbus2 und ein tatsaechliches I2C-Geraet
unter /dev/i2c-1. MockI2CBus liefert stattdessen fest einprogrammierte/
aenderbare Werte, analog zum socat-Mock-Muster aus
Tresor-Kurzprojekt/Code/pi-dashboard.

Zwei-Board-Aufbau (siehe README "Hardware-Update 5"), zwei I2C-Adressen,
beide jetzt mit demselben Sensorprinzip (KY-028, unkalibrierter Analog-
wert - der DHT22 auf dem Aktor-Board gab nie eine gueltige Messung und
wurde durch ein zweites KY-028 ersetzt, siehe README):
  - SENSOR_ARDUINO_ADDRESS (0x08, sensor_arduino.ino): KY-028-Rohwert
    plus digitaler KY-028-Ausgang (D0, an D11 verkabelt, siehe README
    "Sensor-Board KY-028 D0"). Lese-Format 3 Bytes: highByte(raw),
    lowByte(raw), digital (0/1).
  - ACTOR_ARDUINO_ADDRESS (0x09, actor_arduino.ino): KY-028-Rohwert (2.
    Sensor) und nimmt Luefter-/Ventil-Sollwerte entgegen. Lese-Format 2
    Bytes, Schreib-Format 3 Bytes.

Die Umrechnung von Rohwert in Grad Celsius passiert in calibration.py,
nicht hier - hardware.py liefert nur die unkalibrierten Integer-Rohwerte.

Schreib-Format (2 Bytes) entspricht applySetpointsFromPi() im
actor_arduino.ino: fan_pwm (0-255), dann valve_angle (0-180) - keine
Registeradresse davor, der Arduino hat keine echten Register.

Bug gefunden 2026-09-18 (Felix, beim Live-Testen): write_i2c_block_data()
schickt IMMER ein fuehrendes Register-Byte vor den Daten (SMBus-
Konvention), also frueher tatsaechlich 3 Bytes [0, fan_pwm, valve_angle]
statt der von der Firmware erwarteten 2 - dadurch las der Arduino das
Register-Byte (0) als fanPwm (Luefter bekam immer 0) und den echten
fan_pwm-Wert als valveAngle (Servo bekam den falschen Wert, das echte
valve_angle wurde nie gelesen). Fix: i2c_msg.write() statt
write_i2c_block_data() - schickt exakt die uebergebenen Bytes ohne
Register-Praefix.

Gleicher Bug auch beim Lesen (gefunden 2026-09-18): read_i2c_block_data()
schickt vorab ein Register-Byte und erwartet als ERSTES gelesenes Byte
eine Laengenangabe (SMBus-Block-Read-Konvention), gefolgt von genau so
vielen Datenbytes. Unsere Arduinos senden aber einfach zwei rohe Bytes
(Wire.write(highByte); Wire.write(lowByte);) ohne dieses Protokoll -
das echte highByte wurde also als "Laenge" interpretiert und verworfen,
und data[0]/data[1] enthielten in Wahrheit das echte lowByte plus ein
Byte aus der naechsten Wire-Uebertragung. Fix: i2c_msg.read() statt
read_i2c_block_data() - liest exakt N rohe Bytes ohne Register-Praefix
und ohne Laengen-Interpretation, analog zum Schreib-Fix oben.
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

    def read_actor_board(self) -> int:
        raise NotImplementedError

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        raise NotImplementedError


class RealI2CBus(I2CBus):
    def __init__(self, bus_number: int = 1) -> None:
        import smbus2

        self._bus = smbus2.SMBus(bus_number)

    def _read_block_with_retry(self, address: int, length: int) -> list[int]:
        # Analog zum Schreib-Fix in write_actor_setpoints(): i2c_msg.read()
        # statt read_i2c_block_data(), das ein fuehrendes Register-Byte
        # schickt und das erste gelesene Byte als Laengenangabe interpretiert
        # (SMBus-Block-Read-Konvention). Unsere Arduinos senden zwei rohe
        # Bytes ohne dieses Protokoll (siehe Modul-Docstring, Bug vom
        # 2026-09-18) - i2c_msg.read() liest exakt `length` Bytes ohne
        # Register-Praefix und ohne Laengen-Interpretation.
        import smbus2

        last_error: OSError | None = None
        for attempt in range(1, I2C_READ_RETRIES + 1):
            try:
                msg = smbus2.i2c_msg.read(address, length)
                self._bus.i2c_rdwr(msg)
                return list(msg)
            except OSError as exc:
                last_error = exc
                if attempt < I2C_READ_RETRIES:
                    time.sleep(I2C_RETRY_DELAY_SECONDS)
        assert last_error is not None
        raise last_error

    def read_sensor_board(self) -> tuple[int, int]:
        data = self._read_block_with_retry(SENSOR_ARDUINO_ADDRESS, 3)
        return (data[0] << 8) | data[1], data[2]

    def read_actor_board(self) -> int:
        data = self._read_block_with_retry(ACTOR_ARDUINO_ADDRESS, 2)
        return (data[0] << 8) | data[1]

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        # applySetpointsFromPi() in actor_arduino.ino erwartet exakt 2
        # Bytes ohne Register-Praefix - i2c_msg.write() statt
        # write_i2c_block_data(), das immer ein zusaetzliches Register-Byte
        # voranstellt (siehe Modul-Docstring, Bug vom 2026-09-18).
        import smbus2

        self._bus.i2c_rdwr(smbus2.i2c_msg.write(ACTOR_ARDUINO_ADDRESS, [fan_pwm, valve_angle]))


class MockI2CBus(I2CBus):
    def __init__(
        self,
        sensor_board_raw: int = 300,
        actor_board_raw: int = 300,
        sensor_board_digital: int = 0,
    ) -> None:
        self.sensor_board_raw = sensor_board_raw
        self.actor_board_raw = actor_board_raw
        self.sensor_board_digital = sensor_board_digital
        self.last_actor_setpoints: tuple[int, int] | None = None

    def read_sensor_board(self) -> tuple[int, int]:
        return self.sensor_board_raw, self.sensor_board_digital

    def read_actor_board(self) -> int:
        return self.actor_board_raw

    def write_actor_setpoints(self, fan_pwm: int, valve_angle: int) -> None:
        self.last_actor_setpoints = (fan_pwm, valve_angle)
