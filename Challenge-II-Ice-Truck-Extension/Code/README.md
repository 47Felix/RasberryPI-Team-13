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

Rueckweg (Fernsteuerung der Aktoren) laeuft ueber dieselbe Bruecke: der
Node-RED-Flow ruft fuer jeden validierten `control/*`-Befehl per Exec-Node
`Challenge-I-Ice-Truck/Code/pi-backend/set_control.py` auf, das
`control_state.json` schreibt - `app.py` (Challenge-I-Regelkreis) liest das
jeden Poll-Zyklus und schreibt bei `mode == "manual"` die manuellen
Sollwerte tatsaechlich per I2C an den Aktor-Arduino (Issue #180 ist erledigt,
siehe unten). Noch nicht auf echter Hardware getestet - siehe "Was noch fehlt".

## Was existiert

| Datei | Track(s) | Inhalt |
|---|---|---|
| `mqtt-topics.md` | B (#194) | Vollständiges Topic-Schema: welche Werte werden publiziert, welche Control-Topics nimmt der Pi entgegen (aktualisiert 23.09.2026 auf das echte `db.py`-Datenmodell, siehe unten) |
| `node-red/flows.json` | C (#195) | Node-RED-Flow: liest alle 5s die letzte Zeile aus `challenge_i.db`, publiziert sie auf die Topics aus `mqtt-topics.md` (`fn_format` seit 23.09.2026 auf die neuen Feldnamen umgestellt); nimmt `control/#`-Befehle entgegen, validiert sie, loggt sie nach `control_log.ndjson` und reicht sie seit 23.09.2026 per Exec-Node (`exec1`) an `set_control.py` weiter, das den Aktor-Arduino tatsaechlich manuell fernsteuert (noch nicht auf dem Pi importiert/getestet) |
| `../../Challenge-I-Ice-Truck/Code/pi-backend/control_state.py`, `set_control.py` | C (#195) | Geteilter Zustand (`control_state.json`) zwischen Node-RED und `app.py`: `set_control.py` (vom Exec-Node aufgerufen) schreibt Modus/Sollwerte, `app.py` liest sie jeden Poll-Zyklus und wendet sie bei `mode == "manual"` per I2C an statt der `rules.py`-Sollwerte |
| `mosquitto/team13-icetruck.conf`, `mosquitto/acl` | A (#193) | Auf dem Pi installierte Mosquitto-Zusatzkonfiguration (externer Listener, Auth, ACL) - Spiegel dessen, was unter `/etc/mosquitto/conf.d/` bzw. `/etc/mosquitto/acl` liegt |

## Node-RED-Flow importieren

1. Node-RED-Palette `node-red-node-sqlite` installieren (Menü → Palette verwalten → Installieren)
2. `node-red/flows.json` über Menü → Import einlesen
3. Im `sqlitedb`-Konfigurationsknoten (`challenge_i.db`) prüfen, dass der Pfad zum tatsächlichen Speicherort von `challenge_i.db` auf dem Pi passt - eingetragen ist `/home/team13/RasberryPI-Team-13/Challenge-I-Ice-Truck/Code/pi-backend/challenge_i.db`, abgeglichen mit `WorkingDirectory` in `challenge-i-backend.service` (23.09.2026 korrigiert, vorher stand hier faelschlich ein `/home/pi/...`-Platzhalter)
4. Im `mqtt-broker`-Konfigurationsknoten `localhost:1883` mit den `team13-1`-Zugangsdaten eintragen (Broker läuft, siehe "Broker aufgesetzt und getestet" unten) - für einen Flow direkt auf dem Pi reicht `localhost`, für Zugriff von außerhalb die Tailscale-IP/den Hostnamen des Pi verwenden
5. Im `exec1`-Node (`set_control.py (I2C-Forwarding)`) prüfen, dass der `python3`, der `set_control.py` ausführt, dieselbe Umgebung/denselben `venv` wie `app.py` nutzt (siehe `challenge-i-backend.service: ExecStart`) - sonst könnte z.B. ein fehlendes Paket den Aufruf lautlos scheitern lassen (Fehler landen im `set_control.py Fehler`-Debug-Node)

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

## Was noch fehlt (braucht Hardware-/Pi-Zugriff)

- **Echter End-to-End-Test** des Node-RED-Bridge-Flows (`node-red/flows.json`, Track C #195) gegen die laufende `challenge_i.db` und den echten Aktor-Arduino - der Flow ist inhaltlich fertig (Publish + Fernsteuerung, siehe oben), aber noch nicht auf dem Pi importiert. Braucht direkten Zugriff auf die Node-RED-Instanz des Pi (Palette installieren, Import, `sqlitedb`-Pfad + `mqtt-broker`-Credentials im laufenden Node-RED eintragen, siehe "Node-RED-Flow importieren" oben) - das kann nicht aus diesem Repo-Checkout heraus erledigt werden, sondern muss jemand mit Pi-/Node-RED-Zugriff machen. Insbesondere ungetestet: ob der `exec1`-Node mit dem auf dem Pi installierten `python3` (und dessen `venv`, falls noetig - siehe `challenge-i-backend.service`) tatsaechlich `set_control.py` ausfuehren kann.
- **MQTT Dash / MQTT Explorer konfigurieren** (Track D, #196) – Screenshots/Kurzanleitung im Vault, sobald ein Gerät verfügbar ist

## Status

Broker ist aufgesetzt, gesichert und end-to-end getestet (Track A, #193 -
siehe oben). Topic-Schema (Track B, #194) ist auf das echte `db.py`-
Datenmodell aktualisiert. Node-RED-Bridge-Flow (Track C, #195) ist
inhaltlich fertig: Publish der Sensordaten UND Fernsteuerung (Handy →
`control_state.json` → `app.py` → I2C) sind verdrahtet, `set_control.py`/
`control_state.py` sind per `pytest` getestet (15/15 gruen). **Noch nicht
auf dem Pi importiert und nicht gegen echte Hardware getestet** - nächster
Schritt: jemand mit Zugriff auf die Pi-Node-RED-Instanz importiert
`flows.json`, trägt DB-Pfad + Broker-Credentials ein (siehe "Node-RED-Flow
importieren" oben) und testet gegen die echte `challenge_i.db`, den
laufenden Broker und den Aktor-Arduino (z.B. per MQTT Dash/Explorer
`control/mode/set` auf `manual` setzen, dann `fan_pwm`/`valve_angle`
schicken und pruefen ob Luefter/Servo reagieren).
