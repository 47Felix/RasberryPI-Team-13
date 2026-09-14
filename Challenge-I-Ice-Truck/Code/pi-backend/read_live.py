"""Manuelles Live-Auslesen des Sensor-Arduino ueber I2C, ohne DB/Regellogik.

Nuetzlich zum Pruefen der Verkabelung (z.B. DHT11-Werte gegen ein
Referenz-Thermometer), unabhaengig von app.py/rules.py/db.py.

Aufruf auf dem Pi:
    cd ~/RasberryPI-Team-13/Challenge-I-Ice-Truck/Code/pi-backend
    python3 read_live.py

Kein sudo noetig, solange der User in der i2c-Gruppe ist (getent group i2c).
Strg+C zum Beenden.
"""

from __future__ import annotations

import time

from hardware import RealI2CBus

POLL_INTERVAL_SECONDS = 2


def main() -> None:
    bus = RealI2CBus()
    print("Lese Sensor-Arduino (I2C 0x08), Strg+C zum Beenden...\n")
    while True:
        try:
            temperature_c, humidity_pct, ldr_raw, button = bus.read_sensor_arduino()
        except OSError as exc:
            print(f"I2C-Lesefehler, versuche es weiter: {exc}")
            time.sleep(POLL_INTERVAL_SECONDS)
            continue
        print(
            f"Temp: {temperature_c:5.1f} C  |  Feuchte: {humidity_pct:5.1f} %  |  "
            f"LDR: {ldr_raw:4d}  |  Taster: {button}"
        )
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
