"""Kalibrierung der beiden KY-028-Rohwerte (analog, unkalibriert) in Grad
Celsius, per einfacher 2-Punkt-linearer Interpolation.

Kalibriert am 2026-09-17 (Sensor-Board) bzw. 2026-09-18 (Aktor-Board,
Felix) mit einem Referenzthermometer, ueber read_live.py abgelesen.
Rohwert faellt bei beiden Sensoren mit steigender Temperatur (siehe
Kommentar in sensor_arduino.ino zur Spannungsteiler-Verschaltung).

Der Aktor-Board-Ruhewert driftet spuerbar mit der Zeit (vermutlich
Eigenerwaermung durch Luefter/Servo/LED auf derselben Platine) - die
erste Zwei-Punkt-Messung (24.0C -> raw 207) war nach kurzer Zeit schon
veraltet. Zweite Kalibrierung (18.09., spaeter): da Sensor- und
Aktor-Board nebeneinander sitzen, liefert das (schon verifiziert
korrekte) Sensor-Board die Ambient-Referenztemperatur fuer den
Aktor-Ruhewert; als zweiter Punkt wird weiter der zuvor per Thermometer
gemessene Fingerkuppen-Kontaktwert (30.5C) verwendet, da eine warme
Fingerkuppe physikalisch eine recht konstante Kontakttemperatur hat:
  - Sensor-Board (0x08): 23.0C -> raw 212, 30.0C -> raw 160
  - Aktor-Board  (0x09): 23.0C -> raw 174 (Ambient, via Sensor-Board-Proxy),
    30.5C -> raw 126 (Fingerkuppe)

Falls der Aktor-Ruhewert wieder spuerbar von ~174 abweicht, ist das
vermutlich wieder Drift, keine falsche Kalibrierung - am besten per
Sensor-Board-Proxy (s.o.) neu abgleichen statt nur die Konstanten zu
raten.

Neukalibrierung 2026-09-22 (Felix): beide Boards waren deutlich weg vom
erwarteten Ruhewert - Sensor-Board zeigte ~29C, Aktor-Board ~17C, bei
geschaetzter echter Raumtemperatur von ~22C (unberuehrt, kein Finger
drauf). Das ist bei BEIDEN Boards Drift, nicht nur beim Aktor-Board wie
bisher angenommen - vermutlich Alterung/Spannungsreferenz-Drift der
KY-028-Module seit der Erstkalibrierung, nicht Verkabelung (Rohwerte
sind stabil, kein Rauschen).

WICHTIG: 22.0C ist eine Schaetzung des Nutzers, KEINE Referenzthermometer-
Messung wie die urspruenglichen 23.0/30.0/30.5C-Punkte. Fix: pro Board
den Nullpunkt (raw_low/raw_high) so verschoben, dass der aktuelle
Ruhewert 22.0C ergibt, unter Beibehaltung der urspruenglich per
Thermometer gemessenen Steigung (Rohwert-Aenderung pro Grad) - die
Sensitivitaet des Thermistors sollte sich nicht aendern, nur der
Absolutwert (Offset-Drift ist bei diesen Modulen ueblicher als
Sensitivitaets-Drift). Die "hohen" Punkte (30.0C / 30.5C) sind damit
jetzt selbst wieder hochgerechnet, nicht frisch mit Finger+Thermometer
gemessen:
  - Sensor-Board (0x08): 23.0C -> raw 159.6 (verschoben), 30.0C -> raw 107.6
    (hochgerechnet)
  - Aktor-Board  (0x09): 23.0C -> raw 206.6 (verschoben), 30.5C -> raw 158.6
    (hochgerechnet)

Sobald wieder ein echtes Referenzthermometer verfuegbar ist, sollte das
hier durch eine frische 2-Punkt-Messung ersetzt werden statt sich auf
diese Schaetzung zu verlassen.
"""

from __future__ import annotations

# (Rohwert, Temperatur in Grad C) je Referenzpunkt, niedriger und hoeherer
# Punkt.
SENSOR_BOARD_CALIBRATION = {
    "raw_low": 159.6,
    "temp_low_c": 23.0,
    "raw_high": 107.6,
    "temp_high_c": 30.0,
}

ACTOR_BOARD_CALIBRATION = {
    "raw_low": 206.6,
    "temp_low_c": 23.0,
    "raw_high": 158.6,
    "temp_high_c": 30.5,
}


def raw_to_celsius(raw: int, raw_low: float, temp_low_c: float, raw_high: float, temp_high_c: float) -> float:
    if raw_high == raw_low:
        return temp_low_c
    fraction = (raw - raw_low) / (raw_high - raw_low)
    return temp_low_c + fraction * (temp_high_c - temp_low_c)


def sensor_board_celsius(raw: int) -> float:
    return raw_to_celsius(raw, **SENSOR_BOARD_CALIBRATION)


def actor_board_celsius(raw: int) -> float:
    return raw_to_celsius(raw, **ACTOR_BOARD_CALIBRATION)
