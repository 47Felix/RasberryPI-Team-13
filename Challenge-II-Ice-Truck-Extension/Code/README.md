# Challenge II – Ice Truck Extension: Code-Überblick

Anleitung/Erklärung zu dem, was ohne Hardware-Zugriff (15.09.2026) entworfen
wurde. Bezieht sich auf [[Challenge II - Ice Truck Extension]] (#193–#196),
baut auf dem bereits real verkabelten Challenge-I-Aufbau auf (siehe
`Challenge-I-Ice-Truck/Code/README.md`).

## Architektur

```
Challenge-I-Ice-Truck/Code/pi-backend/challenge_i.db (SQLite)
              │  alle 5s per SQL-Query gelesen
              ▼
   Node-RED-Flow (Track C, #195, node-red/flows.json)
              │  publiziert auf team13-1/icetruck/... (Track B, #194)
              ▼
        MQTT-Broker (Mosquitto lokal oder ITECH-Broker, Track A, #193)
              │
              ▼
   Handy/Tablet mit MQTT Dash oder MQTT Explorer (Track D, #196)
   (keine Eigenbau-App noetig - Aufgabenstellung nennt beide explizit)
```

Rueckweg (Fernsteuerung der Aktoren) laeuft ueber dieselbe Bruecke, aber siehe
"Was noch fehlt" - das eigentliche I2C-Schreiben an den Aktor-Arduino ist noch
nicht angebunden (Issue #180, Teil von Challenge I).

## Was existiert

| Datei | Track(s) | Inhalt |
|---|---|---|
| `mqtt-topics.md` | B (#194) | Vollständiges Topic-Schema: welche Werte werden publiziert, welche Control-Topics nimmt der Pi entgegen |
| `node-red/flows.json` | C (#195) | Node-RED-Flow: liest alle 5s die letzte Zeile aus `challenge_i.db`, publiziert sie auf die Topics aus `mqtt-topics.md`; nimmt `control/#`-Befehle entgegen, validiert sie und loggt sie nach `control_log.ndjson` |

## Node-RED-Flow importieren

1. Node-RED-Palette `node-red-node-sqlite` installieren (Menü → Palette verwalten → Installieren)
2. `node-red/flows.json` über Menü → Import einlesen
3. Im `sqlitedb`-Konfigurationsknoten (`challenge_i.db`) den Pfad an den tatsächlichen Speicherort von `challenge_i.db` auf dem Pi anpassen (aktuell als Platzhalter `/home/pi/RasberryPI-Team-13/Challenge-I-Ice-Truck/Code/pi-backend/challenge_i.db` eingetragen)
4. Im `mqtt-broker`-Konfigurationsknoten prüfen, ob lokaler Mosquitto (`localhost:1883`) oder der ITECH-Broker verwendet werden soll (Track A, #193)

## Was noch fehlt (braucht Hardware-Zugriff bzw. Issue #180)

- **Broker-Entscheidung testen** (Track A, #193): ITECH-Broker-Zugangsdaten oder lokaler Mosquitto – beides technisch vorbereitet, noch nicht verifiziert
- **Echter End-to-End-Test** des Flows gegen die laufende `challenge_i.db` und einen echten Broker
- **Aktor-Fernsteuerung tatsächlich wirksam machen**: `control_log.ndjson` wird aktuell nur geschrieben, aber nichts steuert davon ausgehend den Aktor-Arduino – das hängt an Issue [#180](https://github.com/47Felix/RasberryPI-Team-13/issues/180) (`hardware.py: write_actor_setpoints()` ist noch `NotImplementedError`, da auf der real verkabelten Hardware die Kühlstufe lokal auf dem Arduino berechnet wird). Sobald #180 steht, kann der Node-RED-Flow um einen Schritt erweitert werden, der `control_log.ndjson`/die MQTT-Befehle tatsächlich weiterreicht.
- **MQTT Dash / MQTT Explorer konfigurieren** (Track D, #196) – Screenshots/Kurzanleitung im Vault, sobald ein Gerät verfügbar ist

## Status

Topic-Schema und Node-RED-Flow sind fertig entworfen und committet, aber
**ungetestet** (kein Hardware-/Broker-Zugriff heute). Nächster Schritt bei
Zugriff: Broker-Zugangsdaten klären, Flow importieren + Pfade anpassen, gegen
die echte `challenge_i.db` testen.
