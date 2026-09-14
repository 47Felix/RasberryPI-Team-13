"""Regellogik fuer Challenge I Track F: zwei Kuehlstufen aus Schwellwerten.

ANNAHME (Platzhalter, siehe README.md): hoeherer Analogwert = hoehere
Temperatur im Kuehlraum. Die konkreten Schwellwerte haengen an der
Kalibrierung des tatsaechlichen Sensors und an der noch ausstehenden
Moodle-Aufgabenstellung (Issue #167) - hier bewusst als benannte
Konstanten statt Magic Numbers, damit sie sich nach Klaerung von #167
an einer Stelle anpassen lassen, ohne die Logik selbst zu aendern.

Hardware-Update (Felix, 14.09., siehe Issue #179): kein Luefter/DC-Motor
vorhanden, nur der Servo. Beide Kuehlstufen laufen deshalb ueber
valve_angle (kleiner Winkel = leichte Kuehlung, groesserer Winkel =
starke Kuehlung). fan_pwm wird weiterhin berechnet und mitgeschickt -
vorbereitet fuer den Moment, wo ein Luefter beschafft wird - richtet
ohne verkabelten Transistor/H-Bruecke aber nichts aus.
"""

from __future__ import annotations

LIGHT_COOLING_THRESHOLD = 600
STRONG_COOLING_THRESHOLD = 850
ANALOG_MAX = 1023

MAX_FAN_PWM = 255
MAX_VALVE_ANGLE = 180
LIGHT_STAGE_MAX_ANGLE = 90

DOOR_OPEN_VALVE_BOOST = 30


def compute_setpoints(analog_raw: int, door_open: bool) -> tuple[int, int]:
    if analog_raw <= LIGHT_COOLING_THRESHOLD:
        fan_pwm = 0
    else:
        span = ANALOG_MAX - LIGHT_COOLING_THRESHOLD
        fan_pwm = round((analog_raw - LIGHT_COOLING_THRESHOLD) / span * MAX_FAN_PWM)
        fan_pwm = min(fan_pwm, MAX_FAN_PWM)

    if analog_raw <= LIGHT_COOLING_THRESHOLD:
        valve_angle = 0
    elif analog_raw <= STRONG_COOLING_THRESHOLD:
        span = STRONG_COOLING_THRESHOLD - LIGHT_COOLING_THRESHOLD
        valve_angle = round(
            (analog_raw - LIGHT_COOLING_THRESHOLD) / span * LIGHT_STAGE_MAX_ANGLE
        )
    else:
        span = ANALOG_MAX - STRONG_COOLING_THRESHOLD
        progress = (analog_raw - STRONG_COOLING_THRESHOLD) / span
        valve_angle = LIGHT_STAGE_MAX_ANGLE + round(
            progress * (MAX_VALVE_ANGLE - LIGHT_STAGE_MAX_ANGLE)
        )

    if door_open and valve_angle > 0:
        valve_angle = min(MAX_VALVE_ANGLE, valve_angle + DOOR_OPEN_VALVE_BOOST)

    return fan_pwm, min(valve_angle, MAX_VALVE_ANGLE)
