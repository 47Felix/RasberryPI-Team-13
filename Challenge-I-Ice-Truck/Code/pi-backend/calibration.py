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

Polaritaets-Fix Aktor-Board 2026-09-23 (Felix) - ZURUECKGENOMMEN, siehe
unten: erster Live-Test (kurze, unklare Beruehrung) sah nach umgekehrter
Richtung aus, deshalb wurde ACTOR_BOARD_CALIBRATION testweise mit
raw_high > raw_low (statt umgekehrt) versucht.

Korrektur 2026-09-23, zweiter Test (Felix): laengerer, eindeutiger
Live-Test (read_live.py) zeigt Aktor-Board-Rohwert klar FALLEND von ~214
(Ruhe, unberuehrt) auf ~177 (Fingerkuppe) - also doch dieselbe Richtung
wie urspruenglich 2026-09-18 gemessen und wie beim Sensor-Board. Der erste
Fix-Versuch oben war falsch (zu kurzer/uneindeutiger Testlauf). Zurueck zu
raw faellt mit steigender Temperatur, jetzt mit frischen Ankerpunkten aus
diesem Testlauf: Ruhewert ~214 -> 23.0C (Schaetzung, kein Thermometer),
Fingerkuppe ~177 -> 30.5C (etablierter Kontaktwert-Referenzpunkt).

Gleichzeitig faellt auf: beide Ruhewerte sind wieder von den 2026-09-22-
Ankerpunkten weggedriftet (Sensor-Board zeigte dort unberuehrt ~17.7C,
sollte ~23C sein; Aktor-Board zeigte ~30-31C in Ruhe, ebenfalls zu hoch).
Also wieder reiner Offset-Drift, keine Richtungsaenderung - Steigung wird
jeweils beibehalten, nur der Ruhe-Ankerpunkt auf den aktuell beobachteten
Rohwert verschoben:
  - Sensor-Board (0x08): 23.0C -> raw 199 (verschoben), 30.0C -> raw 147
    (hochgerechnet, gleiche Steigung wie zuvor)
  - Aktor-Board  (0x09): 23.0C -> raw 214 (frisch gemessen), 30.5C -> raw 177
    (frisch gemessen)

Weiterhin nur Schaetzungen ohne Referenzthermometer. Sobald eins verfuegbar
ist: frische 2-Punkt-Messung statt weiter nachzujustieren.

Sensor-Board-Nachkalibrierung 2026-09-23, dritter Test (Felix): Aktor-Board
bestaetigt jetzt korrekt (Ruhewert ~214-217, faellt sauber auf ~175-184
bei Fingerkuppe). Sensor-Board-Ruhewert war zu Testbeginn (~226 -> 19.4C)
schon wieder tiefer gedriftet als der 2026-09-23-Ankerpunkt (199 -> 23.0C)
annahm, und pendelt sich nach Loslassen bei ~180-182 ein statt zurueck auf
199 - also erneuter Offset-Drift, gleiches Muster wie beim Aktor-Board.
Ankerpunkte diesmal direkt aus diesem Testlauf uebernommen statt nur
verschoben (Ruhepunkt: settled-Wert am Testende; Kontaktpunkt: niedrigster
beobachteter Rohwert waehrend Fingerkuppen-Kontakt):
  - Sensor-Board (0x08): 23.0C -> raw 182 (Ruhe, settled am Testende),
    30.0C -> raw 149 (Fingerkuppe, Minimum im Testlauf)

Die Zwischenwerte beim Sensor-Board waren waehrend des Kontakts recht
unruhig (149-226 im Zickzack statt einer glatten Rampe wie beim
Aktor-Board) - moeglicherweise eine wackelige Verbindung. Kalibrierung
alleine kann das nicht beheben; falls es sich wiederholt, Verkabelung
pruefen statt nur nachzukalibrieren.

Sensor-Board-Nachkalibrierung 2026-09-23, vierter Test (Felix): Ruhewert
unberuehrt diesmal raw 170 -> 25.5C nach altem Ankerpunkt, waehrend das
Aktor-Board zur gleichen Zeit unberuehrt 22.0C zeigte (Kreuzvergleich, da
beide nebeneinander sitzen) - Sensor-Board also wieder zu warm kalibriert.
Ruhepunkt erneut verschoben, Steigung unveraendert:
  - Sensor-Board (0x08): 23.0C -> raw 170 (verschoben), 30.0C -> raw 137
    (hochgerechnet, gleiche Steigung wie beim letzten Mal: 33 Counts/7C)

Das ist jetzt die vierte Nachjustierung des Sensor-Board-Ruhewerts an einem
Tag - koennte echte Raumtemperaturschwankung im Tagesverlauf sein (dann ist
haeufiges Nachjustieren einfach normal und kein Fehler), koennte aber auch
zur oben vermuteten wackeligen Verbindung passen (instabiler Kontakt macht
den Ruhewert selbst instabil, nicht nur die Werte waehrend Beruehrung).
Falls das Nachjustieren so haeufig weitergeht: Verkabelung/Steckverbindung
am Sensor-Board-KY-028 physisch pruefen, nicht nur weiter Konstanten
anpassen.
"""

from __future__ import annotations

# (Rohwert, Temperatur in Grad C) je Referenzpunkt, niedriger und hoeherer
# Punkt.
SENSOR_BOARD_CALIBRATION = {
    "raw_low": 170.0,
    "temp_low_c": 23.0,
    "raw_high": 137.0,
    "temp_high_c": 30.0,
}

ACTOR_BOARD_CALIBRATION = {
    "raw_low": 214.0,
    "temp_low_c": 23.0,
    "raw_high": 177.0,
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
