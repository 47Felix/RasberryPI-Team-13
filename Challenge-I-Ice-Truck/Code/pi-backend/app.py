"""Challenge I Track F: Gesamtintegration.

Liest periodisch den Sensor-Arduino und den Aktor-Arduino per I2C - beide
haben jetzt ein KY-028-Modul (der DHT22 auf dem Aktor-Board hat nie
funktioniert und wurde ersetzt, siehe README "Hardware-Update 5").
Rechnet beide Rohwerte per calibration.py in Grad Celsius um, berechnet
Fan-/Ventil-Sollwerte (rules.py) aus dem Mittelwert beider kalibrierter
Temperaturen, schickt die Sollwerte an den Aktor-Arduino (Track E) und
loggt jede Messung (beide Rohwerte + beide kalibrierte Temperaturen) in
SQLite (db.py).

Ohne echte Hardware NICHT lauffaehig (RealI2CBus braucht smbus2 + einen
tatsaechlichen I2C-Bus) - fuer den echten Betrieb auf dem Pi siehe
README.md. Die Logik selbst (rules.py, db.py) ist ueber tests/ ohne
Hardware verifiziert.

Fernsteuerung vom Handy (Challenge II, Track C, #195): control_state.py
haelt einen von der Node-RED-Bridge geschriebenen Modus (auto/manual) plus
manuelle Sollwerte. Bei mode == "manual" ueberschreiben diese die aus
rules.py berechneten Sollwerte, bevor sie per I2C geschrieben werden.
"""

from __future__ import annotations

import time

import calibration
import control_state
import db
import rules
from hardware import I2CBus, RealI2CBus

POLL_INTERVAL_SECONDS = 5
DB_PATH = "challenge_i.db"


def run_once(bus: I2CBus, conn) -> tuple[int, int]:
    sensor_board_raw, sensor_board_digital = bus.read_sensor_board()
    actor_board_raw = bus.read_actor_board()
    sensor_board_temp_c = calibration.sensor_board_celsius(sensor_board_raw)
    actor_board_temp_c = calibration.actor_board_celsius(actor_board_raw)

    average_temp_c = (sensor_board_temp_c + actor_board_temp_c) / 2
    auto_fan_pwm, auto_valve_angle = rules.compute_setpoints(average_temp_c)

    control = control_state.read_state()
    if control["mode"] == "manual":
        fan_pwm, valve_angle = control["fan_pwm"], control["valve_angle"]
    else:
        fan_pwm, valve_angle = auto_fan_pwm, auto_valve_angle
    bus.write_actor_setpoints(fan_pwm, valve_angle)

    print(
        f"DEBUG pi: sensor_raw={sensor_board_raw} ({sensor_board_temp_c:.1f}C) "
        f"sensor_digital={sensor_board_digital} "
        f"actor_raw={actor_board_raw} ({actor_board_temp_c:.1f}C) "
        f"avg={average_temp_c:.1f}C mode={control['mode']} "
        f"-> fan_pwm={fan_pwm} (should_run={'yes' if fan_pwm > 0 else 'no'}) "
        f"valve_angle={valve_angle}",
        flush=True,
    )

    db.log_reading(
        conn,
        sensor_board_raw,
        sensor_board_temp_c,
        sensor_board_digital,
        actor_board_raw,
        actor_board_temp_c,
        fan_pwm,
        valve_angle,
    )
    return fan_pwm, valve_angle


def main() -> None:
    bus = RealI2CBus()
    conn = db.connect(DB_PATH)
    while True:
        run_once(bus, conn)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
