---
tags: [projekt, pi-dashboard, arduino, kurzprojekt]
---

# Erweiterung: Raspberry Pi Dashboard fuer den Digitalen Tresor

> [!info] Stand
> 28.08.2026 – **Echter Hardware-Test mit angeschlossenem Arduino durchgeführt** (nicht mehr nur Mock-Serial). Dabei zwei Bugs gefunden und gefixt: (1) Arduino meldete nach dem automatischen Wiederverriegeln kein Ereignis, Dashboard zeigte "offen" dauerhaft weiter an → neues `EVENT:LOCKED` ergänzt; (2) Dashboard aktualisierte sich nur bei manuellem Neuladen → neuer `/api/status`-JSON-Endpunkt + JS-Polling alle 2s. Siehe "Hardware-Test" unten. Vorher (27.08.2026): Software-Seite komplett per simuliertem Arduino (`socat`) end-to-end getestet, dabei einen Discord-Alarm-Bug gefixt (Cloudflare blockte den User-Agent).

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
- **`.env`-Änderungen wirken automatisch (seit 27.08.2026)**: `tresor-dashboard-env-reload.path` überwacht `~/tresor-dashboard/.env` und startet den Dashboard-Service automatisch neu, sobald die Datei geändert wird (systemd `EnvironmentFile` wird sonst nur beim Prozessstart gelesen – ohne diesen Watcher bräuchte jede `.env`-Änderung, z.B. ein neues Admin-Passwort, einen manuellen `systemctl restart`). Status prüfen: `systemctl status tresor-dashboard-env-reload.path`.

## Serial-Protokoll (selbst definiert, da vorher keins existierte)

| Richtung | Nachricht | Bedeutung |
|---|---|---|
| Arduino → Pi | `EVENT:READY` | Arduino gebootet/verbunden |
| Arduino → Pi | `EVENT:GRANTED` | Korrekter Code, Tresor offen |
| Arduino → Pi | `EVENT:DENIED:<n>` | Falscher Code, `<n>` = Versuchsnummer |
| Arduino → Pi | `EVENT:ALARM` | Max. Versuche erreicht, Alarm |
| Arduino → Pi | `EVENT:LOCKED` | Automatisch wieder verriegelt (4s nach `EVENT:GRANTED`) – seit 28.08.2026, siehe "Hardware-Test" |
| Arduino → Pi | `EVENT:CODE_UPDATED` | Bestaetigt neuen Code uebernommen |
| Pi → Arduino | `SETCODE:<code>` | Neuen Tresor-Code setzen (4-8 Ziffern) |

## Software-Test mit simuliertem Arduino (27.08.2026)

Da kein Arduino angeschlossen ist und Tinkercad keine Bridge nach aussen anbietet (geschlossene Browser-Sandbox, kein echter Serial-Port/keine Netzwerk-API), wurde stattdessen die **Pi-Software** komplett durchgetestet:

1. Virtuelles Serial-Port-Paar per `socat` gebaut (`/tmp/ttyMOCK-arduino` ↔ `/tmp/ttyMOCK-pi`), simuliert einen echten USB-Seriell-Port.
2. `app.py` per `DASHBOARD_MOCK_SERIAL_PORT`-Env-Var (neu, siehe Code) auf die Mock-Seite gezeigt.
3. Alle Events (`READY`, `DENIED:1-3`, `ALARM`, `GRANTED`) simuliert reingeschrieben → korrekt in SQLite geloggt, Live-Status im Dashboard stimmte.
4. `SETCODE` ueber das echte Web-Formular ausgeloest, auf der Mock-Arduino-Seite mitgelesen → korrekt angekommen.
5. **Bug gefunden**: Discord-Alarm-Meldung scheiterte mit HTTP 403 – Python's `urllib`-Standard-User-Agent wird von Discord/Cloudflare geblockt (identischer curl-Request mit demselben Token/Channel funktionierte). Gefixt durch expliziten `User-Agent`-Header, danach end-to-end verifiziert (Alarm-Event → automatische Discord-Nachricht kam an).
6. Alles wieder aufgeraeumt (Mock-Service gestoppt, Test-DB geleert, Test-Discord-Nachrichten geloescht, `.env` zurueckgesetzt) – Service laeuft wieder im Produktions-Zustand und wartet auf ein echtes Geraet.

**Fazit**: Die komplette Pi-Software-Logik ist verifiziert korrekt. Was fehlt, ist ausschliesslich die Arduino-Seite selbst.

## Hardware-Test mit echtem Arduino (28.08.2026)

Erster Test mit tatsaechlich per USB angeschlossenem Arduino (nicht mehr Mock-Serial). Dabei zwei Bugs gefunden und noch am selben Tag gefixt:

1. **Fehlendes Re-Lock-Event**: Der Arduino meldete nach dem automatischen Wiederverriegeln (4s nach `EVENT:GRANTED`) kein eigenes Ereignis – das Dashboard zeigte "offen" dauerhaft weiter an, auch nachdem der Tresor laengst wieder zu war. Fix: neues `EVENT:LOCKED` direkt nach dem Wiederverriegeln im Sketch ergaenzt.
2. **Kein Live-Update im Dashboard**: `dashboard.html` aktualisierte Status/Verlauf nur bei manuellem Neuladen. Fix: neuer `/api/status`-JSON-Endpunkt in `app.py` + JS-Polling alle 2s, aktualisiert Status-Badge, Ampel, Fehlversuche und Ereignis-Tabelle ohne Reload.

Siehe PR [#48](https://github.com/47Felix/RasberryPI-Team-13/pull/48).

## Was noch fehlt

- [ ] `SETCODE`-Timing pruefen: Wenn `checkSerialCommands()` mitten in einem `delay()` (z.B. waehrend `accessGranted()` 4 Sekunden wartet) aufgerufen werden soll, geht das mit dem aktuellen Sketch-Aufbau nicht (Arduino ist in dem Moment blockiert) – nur relevant, falls das im echten Betrieb stoert.
- [ ] Track #42 (Stretch) ist nur als Text-Ampel umgesetzt (gross, farbig), keine physische LED-Ampel-Hardware am Pi.

## Sicherheitshinweise

- Admin-Passwort ist **bewusst getrennt** vom Tresor-Code (Track J Anforderung) – wer das Dashboard bedienen darf, kennt nicht automatisch den Tresor-Code und umgekehrt.
- **Nebenbefund waehrend der Einrichtung (27.08.2026)**: Das bestehende `ttyd`-Web-Terminal auf dem Pi (Port 7681, siehe [[Pi Zugriff]]) hat **gar keine eigene Authentifizierung** – wer den Port erreicht, bekommt direkt eine `team13`-Shell. `team13` ist zudem passwortlos in der `sudo`-Gruppe. War schon vorher so (LAN-Reichweite), aber seit dem Tailscale-Setup (siehe [[Pi Zugriff]]) ist der Radius groesser. Empfehlung: ttyd mit Basic-Auth absichern oder per Tailscale-ACL einschraenken – siehe [[Offene Punkte]].

## Sonstiges

- Die Pi-Systemuhr ging beim Deployment falsch (zeigte 24.08. statt 27.08.) – vermutlich fehlende RTC-Batterie + NTP-Sync noch nicht durchgelaufen. Betrifft die Zeitstempel im Event-Log! Siehe [[Offene Punkte]].
- Ein Teammitglied hatte parallel schon eigene Debugging-Versuche mit `Serial.println(key)` unternommen (Notiz: "in der Serial kommt keine Zahl wenn ich auf dem Keypad drücke") – nicht geloescht, als Referenz stehen gelassen, liegt seit dem Sketch-Ordner-Cleanup (28.08.2026, PR [#47](https://github.com/47Felix/RasberryPI-Team-13/pull/47)) unter `Code/arduino-tresor/tresor_integration/debug-referenz/` (`tresor_integration_v2.ino`, Screenshot, `message.txt`) statt direkt im Sketch-Ordner – Grund: Arduino/`arduino-cli` kompiliert sonst alle `.ino`-Dateien im selben Ordner zusammen, was mit der zweiten `setup()`/`loop()`-Kopie fehlgeschlagen waere. Mein Ansatz loggt strukturierte Ereignisse statt Rohtasten, sollte das Problem umgehen, sobald der neue Sketch geflasht ist.

## Verwandte Notizen
- [[WS-Kurzprojekt Freitag]]
- [[Pi Zugriff]]
- [[Claude Discord Bot Setup]]
- [[Offene Punkte]]

#projekt #pi-dashboard #arduino #kurzprojekt
