"""Manuelles Live-Auslesen beider Arduinos ueber I2C, ohne DB/Regellogik.

Nuetzlich zum Pruefen der Verkabelung und zum Kalibrieren (Rohwert gegen
ein Referenz-Thermometer ablesen, siehe calibration.py), unabhaengig von
app.py/rules.py/db.py.

Aufruf auf dem Pi:
    cd ~/RasberryPI-Team-13/Challenge-I-Ice-Truck/Code/pi-backend
    python3 read_live.py

Kein sudo noetig, solange der User in der i2c-Gruppe ist (getent group i2c).
Strg+C zum Beenden.
"""

from __future__ import annotations

import time

import calibration
from hardware import RealI2CBus

POLL_INTERVAL_SECONDS = 2


def main() -> None:
    bus = RealI2CBus()
    print("Lese Sensor-Arduino (0x08) + Aktor-Arduino (0x09), Strg+C zum Beenden...\n")
    while True:
        try:
            sensor_board_raw, sensor_board_digital = bus.read_sensor_board()
            actor_board_raw = bus.read_actor_board()
        except OSError as exc:
            print(f"I2C-Lesefehler, versuche es weiter: {exc}")
            time.sleep(POLL_INTERVAL_SECONDS)
            continue
        sensor_board_temp_c = calibration.sensor_board_celsius(sensor_board_raw)
        actor_board_temp_c = calibration.actor_board_celsius(actor_board_raw)
        print(
            f"Sensor-Board: raw={sensor_board_raw:4d}  temp={sensor_board_temp_c:6.1f} C  "
            f"digital={sensor_board_digital}  |  "
            f"Aktor-Board: raw={actor_board_raw:4d}  temp={actor_board_temp_c:6.1f} C"
        )
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
