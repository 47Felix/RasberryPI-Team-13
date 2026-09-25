# MQTT-Topic-Schema (Track B, #194)

Topics orientieren sich am bestehenden Muster aus der README (`team13-1/led/set`)
und an den Feldern, die `Challenge-I-Ice-Truck/Code/pi-backend/db.py` tatsächlich in
`readings` loggt: zwei Boards mit je einem KY-028-Rohwert + kalibrierter Temperatur
(`sensor_board_raw`/`sensor_board_temp_c`, `actor_board_raw`/`actor_board_temp_c`),
sowie die daraus abgeleiteten Aktor-Sollwerte `fan_pwm`/`valve_angle`
(siehe `rules.py`). Kein Feuchte-/Licht-/Taster-Sensor mehr - das alte Sensor-Modell
(`humidity_pct`, `ldr_raw`, `button`) gab es nur vor den Challenge-I-Hardware-Updates
und existiert in `db.py` nicht mehr.

Präfix: `team13-1/icetruck/`

## Publish (Pi → App), retained

| Topic | Payload | Quelle |
|---|---|---|
| `team13-1/icetruck/sensors/sensor_board_raw` | Ganzzahl, KY-028-Rohwert | `readings.sensor_board_raw` |
| `team13-1/icetruck/sensors/sensor_board_temp_c` | Zahl, °C (z.B. `6.8`) | `readings.sensor_board_temp_c` (kalibriert, `calibration.py: sensor_board_celsius()`) |
| `team13-1/icetruck/sensors/sensor_board_digital` | `0`/`1`, KY-028-D0-Schwellwert | `readings.sensor_board_digital` |
| `team13-1/icetruck/sensors/actor_board_raw` | Ganzzahl, KY-028-Rohwert (2. Sensor) | `readings.actor_board_raw` |
| `team13-1/icetruck/sensors/actor_board_temp_c` | Zahl, °C | `readings.actor_board_temp_c` (kalibriert, `calibration.py: actor_board_celsius()`) |
| `team13-1/icetruck/actuators/fan_pwm` | Ganzzahl 0-255 | `readings.fan_pwm` (Regellogik-Sollwert aus `rules.py`, berechnet aus dem Mittelwert beider kalibrierter Temperaturen) |
| `team13-1/icetruck/actuators/valve_angle` | Ganzzahl 0-180 | `readings.valve_angle` |
| `team13-1/icetruck/status` | JSON, alle Felder + `timestamp_utc` in einem Payload | komplette letzte Zeile aus `readings`, für ein einzelnes Dashboard-Widget in MQTT Dash |

Einzelwert-Topics = einfache Zahl als Plain-Text-Payload (kein JSON), damit MQTT
Dash sie direkt in numerische Widgets/Gauges packen kann. `status` zusätzlich als
JSON für alle, die lieber ein Widget mit Rohdaten wollen (z.B. MQTT Explorer).

Retained, damit ein neu verbundenes Handy sofort den letzten Stand sieht, statt
bis zum nächsten Poll-Zyklus (5s, siehe `app.py: POLL_INTERVAL_SECONDS`) zu warten.

## Subscribe (App → Pi), Aktor-Fernsteuerung

| Topic | Payload | Bedeutung |
|---|---|---|
| `team13-1/icetruck/control/mode/set` | `auto` \| `manual` | Umschalten zwischen automatischer Regellogik (`rules.py`) und manueller Steuerung übers Handy |
| `team13-1/icetruck/control/fan_pwm/set` | Ganzzahl 0-255 | nur wirksam wenn `mode = manual` |
| `team13-1/icetruck/control/valve_angle/set` | Ganzzahl 0-180 | nur wirksam wenn `mode = manual` |

**Status (23.09.2026):** Issue [#180](https://github.com/47Felix/RasberryPI-Team-13/issues/180)
ist erledigt - `hardware.py: write_actor_setpoints()` schreibt die Sollwerte seit dem
I2C-Bugfix vom 18.09. tatsächlich per I2C an den Aktor-Arduino (siehe
`Challenge-I-Ice-Truck/Code/README.md`, Hardware-Update 6). Die MQTT-Verdrahtung ist
jetzt fertig: Der Node-RED-Flow (Track C, #195) validiert `control/*`-Befehle, loggt
sie weiterhin nach `control_log.ndjson` und ruft zusätzlich per Exec-Node
`pi-backend/set_control.py` auf, das `pi-backend/control_state.json` schreibt.
`app.py` (Challenge-I-Regelkreis) liest diesen Zustand jeden Poll-Zyklus (5s) und
verwendet bei `mode == "manual"` die manuellen `fan_pwm`/`valve_angle`-Werte statt der
`rules.py`-Sollwerte. Noch **nicht** auf dem Pi importiert/gegen echte Hardware
getestet - siehe `Code/README.md`, Abschnitt "Was noch fehlt".

## Beispiel-Payload für `status`

```json
{
  "timestamp_utc": "2026-09-23T09:12:03+00:00",
  "sensor_board_raw": 612,
  "sensor_board_temp_c": 6.8,
  "sensor_board_digital": 1,
  "actor_board_raw": 598,
  "actor_board_temp_c": 7.1,
  "fan_pwm": 96,
  "valve_angle": 0
}
```
