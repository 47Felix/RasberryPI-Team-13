"""Challenge I Track F: Gesamtintegration.

Liest periodisch den Sensor-Arduino (KY-028, Track C) und den
Aktor-Arduino (DHT22 Temp/Feuchte) per I2C, berechnet Fan-/Ventil-Sollwerte
aus der DHT22-Temperatur (rules.py), schickt sie an den Aktor-Arduino
(Track E) und loggt jede Messung in SQLite (db.py). Der KY-028-Rohwert ist
unkalibriert und fliesst aktuell nur ins Logging, nicht in die
Kuehlstufen-Entscheidung.

Ohne echte Hardware NICHT lauffaehig (RealI2CBus braucht smbus2 + einen
tatsaechlichen I2C-Bus) - fuer den echten Betrieb auf dem Pi siehe
README.md. Die Logik selbst (rules.py, db.py) ist ueber tests/ ohne
Hardware verifiziert.
"""

from __future__ import annotations

import time

import db
import rules
from hardware import I2CBus, RealI2CBus

POLL_INTERVAL_SECONDS = 5
DB_PATH = "challenge_i.db"


def run_once(bus: I2CBus, conn) -> tuple[int, int]:
    analog_raw = bus.read_sensor_board()
    temperature_c, humidity_pct = bus.read_actor_board_climate()
    fan_pwm, valve_angle = rules.compute_setpoints(temperature_c)
    bus.write_actor_setpoints(fan_pwm, valve_angle)
    db.log_reading(conn, temperature_c, humidity_pct, analog_raw, fan_pwm, valve_angle)
    return fan_pwm, valve_angle


def main() -> None:
    bus = RealI2CBus()
    conn = db.connect(DB_PATH)
    while True:
        run_once(bus, conn)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
