"""Challenge I Track F: Gesamtintegration.

Liest periodisch den Sensor-Arduino per I2C (Track C), berechnet Fan-/
Ventil-Sollwerte (rules.py), schickt sie an den Aktor-Arduino (Track E)
und loggt jede Messung in SQLite (db.py).

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
    temperature_c, humidity_pct, ldr_raw, button = bus.read_sensor_arduino()
    fan_pwm, valve_angle = rules.compute_setpoints(temperature_c)
    # Kein bus.write_actor_setpoints(...) hier: die Kuehlstufe wird aktuell
    # noch lokal auf dem Arduino angewendet (siehe hardware.py), das ist
    # erst Issue #180. Wir lesen/loggen bereits mit, damit die Historie
    # steht, sobald die Aktorik umzieht.
    db.log_reading(conn, temperature_c, humidity_pct, ldr_raw, button, fan_pwm, valve_angle)
    return fan_pwm, valve_angle


def main() -> None:
    bus = RealI2CBus()
    conn = db.connect(DB_PATH)
    while True:
        run_once(bus, conn)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
