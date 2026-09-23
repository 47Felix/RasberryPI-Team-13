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
        MQTT-Broker (lokaler Mosquitto auf dem Pi, Track A, #193, siehe unten)
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
| `mqtt-topics.md` | B (#194) | Vollständiges Topic-Schema: welche Werte werden publiziert, welche Control-Topics nimmt der Pi entgegen (aktualisiert 23.09.2026 auf das echte `db.py`-Datenmodell, siehe unten) |
| `node-red/flows.json` | C (#195) | Node-RED-Flow: liest alle 5s die letzte Zeile aus `challenge_i.db`, publiziert sie auf die Topics aus `mqtt-topics.md` (`fn_format` seit 23.09.2026 auf die neuen Feldnamen umgestellt); nimmt `control/#`-Befehle entgegen, validiert sie und loggt sie nach `control_log.ndjson` (noch nicht auf dem Pi importiert/getestet) |
| `mosquitto/team13-icetruck.conf`, `mosquitto/acl` | A (#193) | Auf dem Pi installierte Mosquitto-Zusatzkonfiguration (externer Listener, Auth, ACL) - Spiegel dessen, was unter `/etc/mosquitto/conf.d/` bzw. `/etc/mosquitto/acl` liegt |

## Node-RED-Flow importieren

1. Node-RED-Palette `node-red-node-sqlite` installieren (Menü → Palette verwalten → Installieren)
2. `node-red/flows.json` über Menü → Import einlesen
3. Im `sqlitedb`-Konfigurationsknoten (`challenge_i.db`) den Pfad an den tatsächlichen Speicherort von `challenge_i.db` auf dem Pi anpassen (aktuell als Platzhalter `/home/pi/RasberryPI-Team-13/Challenge-I-Ice-Truck/Code/pi-backend/challenge_i.db` eingetragen)
4. Im `mqtt-broker`-Konfigurationsknoten `localhost:1883` mit den `team13-1`-Zugangsdaten eintragen (Broker läuft, siehe "Broker aufgesetzt und getestet" unten) - für einen Flow direkt auf dem Pi reicht `localhost`, für Zugriff von außerhalb die Tailscale-IP/den Hostnamen des Pi verwenden

## Broker aufgesetzt und getestet (Track A, #193, 23.09.2026)

Entscheidung: lokaler Mosquitto auf dem Pi (kein ITECH-Broker) - war laut
[[Installierte Services]] bereits installiert, lief aber nur auf
`127.0.0.1`/`::1` (Debian-Standardverhalten ohne eigene Config), also
erreichbar für Node-RED lokal, aber nicht für ein Handy/Tablet im
Schul-WLAN oder per Tailscale.

Neuer Listener via `mosquitto/team13-icetruck.conf` (installiert nach
`/etc/mosquitto/conf.d/`): bindet auf `0.0.0.0:1883`, verlangt
Passwort-Auth (`allow_anonymous false`) und beschränkt den einzigen
Nutzer `team13-1` per `mosquitto/acl` auf das Topic-Präfix `team13-1/#`.
Zugangsdaten für den `team13-1`-Nutzer stehen wie immer nicht im Repo,
siehe [[⚠️ Zugangsdaten - Hinweis]].

**Getestet (23.09.2026), alles wie erwartet:**
- Authentifizierter Publish/Subscribe-Roundtrip auf `team13-1/icetruck/test` gegen die Pi-Tailscale-IP funktioniert
- Anonyme Verbindung wird abgelehnt (`Connection Refused: not authorised`)
- Publish auf ein Topic außerhalb von `team13-1/#` wird von der ACL stillschweigend verworfen (kein Fehler beim Publisher, aber auch keine Zustellung - normales MQTT-ACL-Verhalten bei QoS 0)
- Port 1883 ist jetzt von außerhalb des Pi erreichbar (vorher „Connection refused“, jetzt offen)

**Nebenbei gefixt:** Der bestehende Node-RED-Flow „LED via MQTT“ (`team13-1/led/set`, aus dem August-Kurzprojekt) verband sich bisher anonym mit `localhost:1883` und wäre durch `allow_anonymous false` sofort abgerissen. Credentials für den `mqtt-broker`-Konfigurationsknoten wurden per Node-RED-Admin-API (`POST /flows`, inkl. `credentials`-Feld für den Knoten) nachgetragen und deployed - Flow läuft wieder, jetzt authentifiziert statt anonym.

## Was noch fehlt (braucht Hardware-Zugriff bzw. Issue #180)

- **Echter End-to-End-Test** des Node-RED-Bridge-Flows (`node-red/flows.json`, Track C #195) gegen die laufende `challenge_i.db` - der Flow ist inhaltlich auf das neue Schema umgestellt (siehe oben), aber noch nicht auf dem Pi importiert. Braucht direkten Zugriff auf die Node-RED-Instanz des Pi (Palette installieren, Import, `sqlitedb`-Pfad + `mqtt-broker`-Credentials im laufenden Node-RED eintragen, siehe "Node-RED-Flow importieren" oben) - das kann nicht aus diesem Repo-Checkout heraus erledigt werden, sondern muss jemand mit Pi-/Node-RED-Zugriff machen
- **Aktor-Fernsteuerung tatsächlich wirksam machen**: `control_log.ndjson` wird aktuell nur geschrieben, aber nichts steuert davon ausgehend den Aktor-Arduino. Der ursprüngliche Blocker (Issue [#180](https://github.com/47Felix/RasberryPI-Team-13/issues/180), `hardware.py: write_actor_setpoints()` war `NotImplementedError`) ist inzwischen erledigt - die I2C-Schreibfunktion funktioniert seit dem I2C-Bugfix vom 18.09. (siehe `Challenge-I-Ice-Truck/Code/README.md`, Hardware-Update 6). Der Node-RED-Flow muss also nur noch um den Schritt erweitert werden, der die MQTT-Befehle tatsächlich an `write_actor_setpoints()` weiterreicht.
- **MQTT Dash / MQTT Explorer konfigurieren** (Track D, #196) – Screenshots/Kurzanleitung im Vault, sobald ein Gerät verfügbar ist

## Status

Broker ist aufgesetzt, gesichert und end-to-end getestet (Track A, #193 -
siehe oben). Topic-Schema (Track B, #194) ist auf das echte `db.py`-
Datenmodell aktualisiert. Node-RED-Bridge-Flow (Track C, #195) ist
inhaltlich auf das neue Schema umgestellt, aber noch **nicht auf dem Pi
importiert und ungetestet** - nächster Schritt: jemand mit Zugriff auf die
Pi-Node-RED-Instanz importiert `flows.json`, trägt DB-Pfad + Broker-
Credentials ein (siehe "Node-RED-Flow importieren" oben) und testet gegen
die echte `challenge_i.db` und den jetzt laufenden Broker.
