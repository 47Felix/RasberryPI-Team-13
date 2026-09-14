"""Regellogik fuer Challenge I Track F: zwei Kuehlstufen aus Schwellwerten.

ANNAHME (Platzhalter, siehe README.md): hoeherer Analogwert = hoehere
Temperatur im Kuehlraum. Die konkreten Schwellwerte haengen an der
Kalibrierung des tatsaechlichen Sensors und an der noch ausstehenden
Moodle-Aufgabenstellung (Issue #167) - hier bewusst als benannte
Konstanten statt Magic Numbers, damit sie sich nach Klaerung von #167
an einer Stelle anpassen lassen, ohne die Logik selbst zu aendern.
"""

from __future__ import annotations

FAN_ON_THRESHOLD = 600
VALVE_ON_THRESHOLD = 850
ANALOG_MAX = 1023

MAX_FAN_PWM = 255
MAX_VALVE_ANGLE = 180

DOOR_OPEN_FAN_BOOST = 60


def compute_setpoints(analog_raw: int, door_open: bool) -> tuple[int, int]:
    if analog_raw <= FAN_ON_THRESHOLD:
        fan_pwm = 0
    else:
        span = ANALOG_MAX - FAN_ON_THRESHOLD
        fan_pwm = round((analog_raw - FAN_ON_THRESHOLD) / span * MAX_FAN_PWM)

    if door_open and fan_pwm > 0:
        fan_pwm = min(MAX_FAN_PWM, fan_pwm + DOOR_OPEN_FAN_BOOST)

    if analog_raw <= VALVE_ON_THRESHOLD:
        valve_angle = 0
    else:
        span = ANALOG_MAX - VALVE_ON_THRESHOLD
        valve_angle = round(
            (analog_raw - VALVE_ON_THRESHOLD) / span * MAX_VALVE_ANGLE
        )

    return min(fan_pwm, MAX_FAN_PWM), min(valve_angle, MAX_VALVE_ANGLE)
