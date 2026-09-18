"""Regellogik fuer Challenge I Track F: zwei Kuehlstufen aus der Sensortemperatur.

Port von computeCoolingStage()/applyCoolingStage() aus
ice_truck_single_board.ino (siehe "Naechste Schritte" dort, Issue #180) -
jetzt wo I2C zum Pi verkabelt ist, kann die Kuehlstufen-Entscheidung hier
statt lokal auf dem Arduino getroffen werden.

Schwellwerte sind fuer Tischtests bei Raumtemperatur (~23-24C, 2026-09-17)
gewaehlt, damit man sie durch Anwaermen/Anfassen der KY-028-Sensoren live
durchfahren kann - noch nicht die eigentlichen Betriebs-Schwellwerte aus
der Moodle-Aufgabenstellung (Issue #167). Ueber Umgebungsvariablen ohne
Code-Aenderung anpassbar, z.B. fuers Live-Testen:
    FAN_ON_TEMP_C=26 VALVE_ON_TEMP_C=29 ./venv/bin/python app.py

Das alte Zwei-Board-Modell (analog_raw ueber LDR + door_open) ist raus: der
LDR misst Licht, nicht Temperatur (siehe README), und es gibt in der
tatsaechlich verkabelten Hardware keinen Tuerkontakt mehr - nur einen
generischen Toggle-Taster ohne dokumentierten Bezug zur Kuehlung.
"""

from __future__ import annotations

import os


def _env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    return default if value is None else float(value)


FAN_ON_TEMP_C = _env_float("FAN_ON_TEMP_C", 25.0)
VALVE_ON_TEMP_C = _env_float("VALVE_ON_TEMP_C", 28.0)
TEMP_SPAN_C = _env_float("TEMP_SPAN_C", 5.0)

MAX_FAN_PWM = 255
MAX_VALVE_ANGLE = 180

MIN_FAN_PWM_WHEN_ON = 40
MIN_VALVE_ANGLE_WHEN_ON = 30


def compute_setpoints(temperature_c: float) -> tuple[int, int]:
    if temperature_c < FAN_ON_TEMP_C:
        return 0, 0

    above_fan_threshold = min(max(temperature_c - FAN_ON_TEMP_C, 0.0), TEMP_SPAN_C)
    fan_pwm = round((above_fan_threshold / TEMP_SPAN_C) * MAX_FAN_PWM)
    fan_pwm = max(MIN_FAN_PWM_WHEN_ON, min(fan_pwm, MAX_FAN_PWM))

    if temperature_c < VALVE_ON_TEMP_C:
        return fan_pwm, 0

    above_valve_threshold = min(max(temperature_c - VALVE_ON_TEMP_C, 0.0), TEMP_SPAN_C)
    valve_angle = round((above_valve_threshold / TEMP_SPAN_C) * MAX_VALVE_ANGLE)
    valve_angle = max(MIN_VALVE_ANGLE_WHEN_ON, min(valve_angle, MAX_VALVE_ANGLE))

    return fan_pwm, valve_angle
