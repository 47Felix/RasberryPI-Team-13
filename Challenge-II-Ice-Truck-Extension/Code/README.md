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

## Node-RED-Flow importiert und teilgetestet (24.09.2026)

Per Node-RED-Admin-API (SSH + `curl` gegen `localhost:1880`, kein UI-Zugriff
noetig) auf dem Pi durchgefuehrt:

- `node-red-node-sqlite` per `POST /nodes` installiert (kein Neustart des
  `nodered`-Systemd-Service noetig, Node-RED laedt Palettenmodule selbst nach)
- `node-red/flows.json` importiert, dabei den mitgelieferten `broker1`-Knoten
  **weggelassen** und `mqtt_out1`/`mqtt_in1` stattdessen auf den bereits
  vorhandenen Broker-Knoten "Team13-1 Mosquitto (localhost)" umgehaengt (der
  hat schon Zugangsdaten hinterlegt, kein zweiter Broker-Knoten noetig)
- Deploy erfolgreich (`Started flows`), `sqlitedb` oeffnet
  `challenge_i.db` ohne Fehler, der `inject1`-Knoten liest per manuellem
  Trigger (`POST /inject/inject1`) tatsaechlich frische Zeilen (Backend
  loggt weiterhin alle 5s, verifiziert per `sqlite3 challenge_i.db`)

**Zwei echte Blocker dabei gefunden, beide brauchen jemanden mit
interaktivem Root-/Passwort-Zugriff auf den Pi (nicht per SSH-Key aus einer
Session heraus loesbar):**

1. **MQTT-Broker-Auth kaputt.** Der bestehende Broker-Knoten
   "Team13-1 Mosquitto (localhost)" haengt seit mindestens 24.09.2026 morgens
   in einer Reconnect-Schleife (`Connection Refused: not authorised`, alle
   15s im `nodered`-Journal) - und zwar schon *lokal auf dem Pi selbst*, das
   ist also kein Tailscale-/WLAN-Erreichbarkeitsproblem. `/etc/mosquitto/passwd`
   existiert noch mit Stand 23.09. (als der Roundtrip laut Track-A-Test noch
   funktionierte), aber irgendwas zwischen Node-RED-Credentials und Broker
   passt nicht mehr zusammen. Ohne das `team13-1`-Passwort (steht wie immer
   nicht im Repo, siehe [[⚠️ Zugangsdaten - Hinweis]]) und ohne
   passwortlosen `sudo` auf dem Pi kann das aus einer SSH-Key-Session heraus
   weder diagnostiziert (Logs/Passwd-Datei sind root-only) noch gefixt
   werden. **Braucht:** jemand mit dem `team13-1`-MQTT-Passwort oder mit dem
   interaktiven sudo-Passwort des Pi, der/die kurz `mosquitto_passwd` bzw.
   die Node-RED-Broker-Credentials neu setzt.
2. **`challenge-i-backend`-Service laeuft noch mit altem Code.** Der Pi ist
   heute (24.09., ca. 09:14 CEST) neu gestartet, der Service kam vor dem
   `git pull` dieser Aenderungen wieder hoch und haelt daher weiterhin die
   *alte* `app.py` im Prozessspeicher (ohne `control_state`-Unterstuetzung).
   Live verifiziert: `set_control.py mode manual` +
   `fan_pwm 111`/`valve_angle 45` gesetzt, `control_state.json` bestaetigt
   korrekt geschrieben, aber `challenge_i.db` loggte in den folgenden
   Poll-Zyklen weiterhin `fan_pwm=0`/`valve_angle=0` statt der manuellen
   Werte - der laufende Prozess kennt `control_state.py` schlicht nicht.
   Zustand sicherheitshalber zurueck auf `mode: auto` gesetzt, damit die
   veralteten manuellen Sollwerte (111/45) nicht unerwartet einmal
   uebernommen werden, sobald doch neu gestartet wird. `systemctl restart
   challenge-i-backend` verlangt interaktive Auth ("Interactive
   authentication required"), also auch hier: **braucht** jemanden mit dem
   sudo-Passwort, der den Service einmal neu startet.

- **MQTT Dash / MQTT Explorer konfigurieren** (Track D, #196) – noch offen, braucht ein physisches Gerät

## Status

Broker ist aufgesetzt und war end-to-end getestet (Track A, #193), ist aber
seit heute (24.09.) wieder kaputt - siehe Blocker 1 oben. Topic-Schema
(Track B, #194) ist auf das echte `db.py`-Datenmodell aktualisiert.
Node-RED-Bridge-Flow (Track C, #195) ist **jetzt auf dem Pi importiert und
deployed** (siehe oben), die DB-Lese-Seite funktioniert nachweislich mit
echten Live-Daten. Fernsteuerung (`control_state.json` → `app.py` → I2C)
ist inhaltlich fertig und per `pytest` getestet (16/16 gruen), aber auf dem
Pi noch nicht wirksam, weil der laufende Service den neuen Code noch nicht
geladen hat (Blocker 2). **Naechster Schritt braucht 5 Minuten mit dem
sudo-Passwort:** `sudo systemctl restart challenge-i-backend` (laedt den
neuen Code) und einmal `mosquitto_passwd`/die Node-RED-Broker-Credentials
fuer `team13-1` neu setzen (behebt die Auth-Schleife) - danach sollte der
komplette Pfad (Handy → MQTT → Node-RED → `set_control.py` → `app.py` →
I2C → Luefter/Servo) durchgetestet werden koennen.
