---
tags: [projekt, pi-dashboard, arduino, kurzprojekt]
---

# Erweiterung: Raspberry Pi Dashboard fuer den Digitalen Tresor

> [!info] Stand
> 27.08.2026 – Software-Seite (Tracks G-J + beide Stretch-Ziele) gebaut, deployed und per HTTP getestet. **Hardware-in-the-loop NICHT getestet** – aktuell ist kein Arduino per USB am Pi angeschlossen, daher konnte die echte Serial-Kommunikation mit dem physischen/Tinkercad-Sketch nicht verifiziert werden. Siehe Abschnitt "Was noch fehlt" unten.

Setzt auf [[WS-Kurzprojekt Freitag]] auf: der Tresor-Arduino-Sketch (`Code/arduino-tresor/tresor_integration/tresor_integration.ino`) meldet seine Ereignisse jetzt per USB-Serial an den Pi, der sie loggt und über eine kleine Weboberfläche im WLAN anzeigt. Deckt GitHub-Issues #37-#42 ab (Tracks G-J + 2 Stretch-Ziele).

## Architektur

```
Arduino (Tresor-Sketch, Serial 9600 Baud)
   │  EVENT:READY / EVENT:GRANTED / EVENT:DENIED:<n> / EVENT:ALARM / EVENT:CODE_UPDATED
   │  <── SETCODE:<neuerCode> (vom Pi, zum Code aendern)
   ▼
Pi: ~/tresor-dashboard/app.py (Flask, systemd-Service "tresor-dashboard")
   ├─ Hintergrund-Thread: liest Serial, autodetect /dev/ttyACM0|1, /dev/ttyUSB0|1,
   │  reconnect alle 5s falls kein Geraet gefunden/Verbindung verloren
   ├─ SQLite (tresor.db): jedes Ereignis mit UTC-Zeitstempel geloggt
   ├─ Web-Dashboard "/" : Live-Ampel (offen/verschlossen/Alarm) + Versuchszaehler
   │  + Verlauf der letzten 50 Ereignisse
   ├─ "/admin" : eigenes Admin-Passwort (NICHT der Tresor-Code!), Formular zum
   │  Setzen eines neuen Tresor-Codes -> schickt SETCODE ueber Serial
   └─ bei EVENT:ALARM: Discord-Nachricht in #pi-projekt ueber die REST-API
      (gleiches Bot-Token wie beim Discord-Bot, siehe [[Claude Discord Bot Setup]])
```

## Wo was liegt

- **Code im Repo** (versioniert, `Code/pi-dashboard/`): `app.py`, `templates/*.html`, `requirements.txt`, `tresor-dashboard.service` — das ist die Referenzkopie, siehe [[Git Workflow]]/[[Branch-Strategie]] fuer Aenderungen daran (Branch+PR, nicht direkt deployen ohne Commit).
- **Live auf dem Pi**: `~/tresor-dashboard/` (App-Code identisch zum Repo, plus `venv/` und `.env` — beide NICHT versioniert, siehe `.gitignore`).
- **`.env` auf dem Pi enthaelt**: `DASHBOARD_ADMIN_PASSWORD` (zufaellig generiert, steht nicht hier im Vault – siehe [[⚠️ Zugangsdaten - Hinweis]]), `DASHBOARD_SECRET_KEY` (Flask-Session), `DISCORD_BOT_TOKEN` (Kopie vom gleichen Bot-Token, das auch die Azure-VM nutzt), `DISCORD_ALARM_CHANNEL_ID` (aktuell `pi-projekt`-Kanal).
- **Erreichbar unter**: `http://team13-1.local:5000` im Schul-WLAN, oder ueber Tailscale (`http://100.100.186.55:5000`) – siehe [[Pi Zugriff]] fuer den neuen Tailscale-Zugangsweg.
- **Service verwalten**: `sudo systemctl status/restart tresor-dashboard`, Logs: `sudo journalctl -u tresor-dashboard -f`.

## Serial-Protokoll (selbst definiert, da vorher keins existierte)

| Richtung | Nachricht | Bedeutung |
|---|---|---|
| Arduino → Pi | `EVENT:READY` | Arduino gebootet/verbunden |
| Arduino → Pi | `EVENT:GRANTED` | Korrekter Code, Tresor offen |
| Arduino → Pi | `EVENT:DENIED:<n>` | Falscher Code, `<n>` = Versuchsnummer |
| Arduino → Pi | `EVENT:ALARM` | Max. Versuche erreicht, Alarm |
| Arduino → Pi | `EVENT:CODE_UPDATED` | Bestaetigt neuen Code uebernommen |
| Pi → Arduino | `SETCODE:<code>` | Neuen Tresor-Code setzen (4-8 Ziffern) |

## Was noch fehlt (bewusst offen, braucht physischen Zugriff)

- [ ] **Hardware-in-the-loop-Test**: Arduino per USB an den Pi anschliessen, pruefen ob `/dev/ttyACM0` (oder `ttyUSB0`) auftaucht, Dashboard beobachten ob Events ankommen. Ich (Claude, VM-Session) habe dafuer keinen physischen Zugriff.
- [ ] Sketch muss auf dem echten/Tinkercad-Arduino neu geflasht werden (die Serial-Erweiterung ist nur im Repo, noch nicht auf einem Geraet).
- [ ] `SETCODE`-Timing pruefen: Wenn `checkSerialCommands()` mitten in einem `delay()` (z.B. waehrend `accessGranted()` 4 Sekunden wartet) aufgerufen werden soll, geht das mit dem aktuellen Sketch-Aufbau nicht (Arduino ist in dem Moment blockiert) – nur relevant, falls das im echten Betrieb stoert.
- [ ] Track #42 (Stretch) ist nur als Text-Ampel umgesetzt (gross, farbig), keine physische LED-Ampel-Hardware am Pi.

## Sicherheitshinweise

- Admin-Passwort ist **bewusst getrennt** vom Tresor-Code (Track J Anforderung) – wer das Dashboard bedienen darf, kennt nicht automatisch den Tresor-Code und umgekehrt.
- **Nebenbefund waehrend der Einrichtung (27.08.2026)**: Das bestehende `ttyd`-Web-Terminal auf dem Pi (Port 7681, siehe [[Pi Zugriff]]) hat **gar keine eigene Authentifizierung** – wer den Port erreicht, bekommt direkt eine `team13`-Shell. `team13` ist zudem passwortlos in der `sudo`-Gruppe. War schon vorher so (LAN-Reichweite), aber seit dem Tailscale-Setup (siehe [[Pi Zugriff]]) ist der Radius groesser. Empfehlung: ttyd mit Basic-Auth absichern oder per Tailscale-ACL einschraenken – siehe [[Offene Punkte]].

## Sonstiges

- Die Pi-Systemuhr ging beim Deployment falsch (zeigte 24.08. statt 27.08.) – vermutlich fehlende RTC-Batterie + NTP-Sync noch nicht durchgelaufen. Betrifft die Zeitstempel im Event-Log! Siehe [[Offene Punkte]].
- Ein Teammitglied hatte parallel schon eigene Debugging-Versuche mit `Serial.println(key)` unternommen (liegt als `tresor_integration_v2.ino` + Tinkercad-Screenshot im selben Ordner, Notiz: "in der Serial kommt keine Zahl wenn ich auf dem Keypad drücke") – nicht geloescht, als Referenz stehen gelassen. Mein Ansatz loggt strukturierte Ereignisse statt Rohtasten, sollte das Problem umgehen, sobald der neue Sketch geflasht ist.

## Verwandte Notizen
- [[WS-Kurzprojekt Freitag]]
- [[Pi Zugriff]]
- [[Claude Discord Bot Setup]]
- [[Offene Punkte]]

#projekt #pi-dashboard #arduino #kurzprojekt
