"""Regellogik fuer Challenge I Track F: zwei Kuehlstufen aus der DHT11-Temperatur.

Port von computeCoolingStage()/applyCoolingStage() aus
ice_truck_single_board.ino (siehe "Naechste Schritte" dort, Issue #180) -
jetzt wo I2C zum Pi verkabelt ist, kann die Kuehlstufen-Entscheidung hier
statt lokal auf dem Arduino getroffen werden. Gleiche Schwellwerte wie im
Sketch - Platzhalter, haengen an der noch offenen Moodle-Aufgabenstellung
(Issue #167) und an der realen Sensor-Kalibrierung.

Das alte Zwei-Board-Modell (analog_raw ueber LDR + door_open) ist raus: der
LDR misst Licht, nicht Temperatur (siehe README), und es gibt in der
tatsaechlich verkabelten Hardware keinen Tuerkontakt mehr - nur einen
generischen Toggle-Taster ohne dokumentierten Bezug zur Kuehlung.
"""

from __future__ import annotations

FAN_ON_TEMP_C = 8.0
VALVE_ON_TEMP_C = 12.0
TEMP_SPAN_C = 6.0

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
