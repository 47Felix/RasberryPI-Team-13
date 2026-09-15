# MQTT-Topic-Schema (Track B, #194)

Topics orientieren sich am bestehenden Muster aus der README (`team13-1/led/set`)
und an den Feldern, die `Challenge-I-Ice-Truck/Code/pi-backend/db.py` bereits in
`readings` loggt (`temperature_c`, `humidity_pct`, `ldr_raw`, `button`, `fan_pwm`,
`valve_angle`).

Präfix: `team13-1/icetruck/`

## Publish (Pi → App), retained

| Topic | Payload | Quelle |
|---|---|---|
| `team13-1/icetruck/sensors/temperature_c` | Zahl, °C (z.B. `8.4`) | `readings.temperature_c` |
| `team13-1/icetruck/sensors/humidity_pct` | Zahl, % | `readings.humidity_pct` |
| `team13-1/icetruck/sensors/ldr_raw` | Ganzzahl 0-1023 | `readings.ldr_raw` |
| `team13-1/icetruck/sensors/button` | `0`/`1` | `readings.button` |
| `team13-1/icetruck/actuators/fan_pwm` | Ganzzahl 0-255 | `readings.fan_pwm` (aktueller Regellogik-Sollwert aus `rules.py`) |
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

**Status (15.09.2026):** Das tatsächliche Schreiben der Aktor-Sollwerte per I2C an
den Arduino ist noch nicht angebunden (`hardware.py: write_actor_setpoints()` wirft
aktuell `NotImplementedError` - Issue [#180](https://github.com/47Felix/RasberryPI-Team-13/issues/180),
die Kühlstufe wird bislang lokal auf dem Arduino berechnet). Der Node-RED-Flow
(Track C, #195) nimmt die `control/*`-Befehle schon entgegen und loggt sie, damit
Track D/App-Seite unabhängig davon entwickelt werden kann - das tatsächliche
Durchreichen an die Hardware folgt, sobald #180 steht.

## Beispiel-Payload für `status`

```json
{
  "timestamp_utc": "2026-09-15T09:12:03+00:00",
  "temperature_c": 6.8,
  "humidity_pct": 41.2,
  "ldr_raw": 512,
  "button": 0,
  "fan_pwm": 96,
  "valve_angle": 0
}
```
