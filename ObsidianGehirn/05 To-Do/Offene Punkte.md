---
tags: [todo, projekt]
---

# Offene Punkte / To-Do

- [ ] **Nächste Challenge starten – [[Challenge I - Ice Truck Problem]]:** Workshop-Woche ("Piece of Pi?") ist mit dem Kurzprojekt fertig, jetzt beginnt Challenge I (Signale & Bus-Systeme, Milestone [#2](https://github.com/47Felix/RasberryPI-Team-13/milestone/2), noch 0 Issues). Konkrete Aufgabenstellung noch dünn dokumentiert – hängt am Moodle-Kurs "Signale und Bussysteme" (Kurs-ID 1574), für den noch das Einschreibekennwort bei der Lehrkraft fehlt.
- [ ] **Vault-Sync-Cron auf Winterzeit umstellen:** Crontab läuft fest auf `45 4 * * *` (UTC), weil `CRON_TZ` auf dieser VM nicht funktioniert (siehe [[Claude Discord Bot Setup]]). Beim Wechsel auf CET (letzter Sonntag im Oktober 2026) manuell auf `45 5 * * *` ändern, sonst läuft der Sync ab dann eine Stunde zu früh (05:45 statt 06:45 Ortszeit).
- [ ] **Sicherheit (dringend):** ttyd auf dem Pi (Port 7681) hat keine eigene Authentifizierung, `team13` ist passwortlos in der sudo-Gruppe – seit Tailscale-Setup fürs ganze Tailnet erreichbar, nicht mehr nur LAN. Absichern (Basic-Auth oder Tailscale-ACL) → [[Pi Zugriff]]
- [ ] **Pi-Systemuhr falsch:** zeigte beim Dashboard-Deployment 24.08. statt 27.08. (vermutlich fehlende RTC-Batterie/NTP noch nicht durchgelaufen) – verfälscht Zeitstempel im Tresor-Event-Log → [[Erweiterung - Raspberry Pi Dashboard]]

## Erledigt ✅
- **Arduino + Elegoo-Kit: Temperatur-/Feuchtigkeitssensor getestet (Dogan):** DHT11-Modul mit Elegoo-UNO-R3 verkabelt, Arduino-Sketch mit DHT-Library liefert Werte (Kalibrierung/Wackelkontakt war noch ein Thema) → [[Dogan - Brain Dump]], GitHub-Issue: [#3](https://github.com/47Felix/RasberryPI-Team-13/issues/3) (closed)
- **Node-RED mit MQTT verknüpft (25.08.2026):** LED-Flow um Topic `team13-1/led/set` erweitert (mqtt-broker localhost:1883, Function-Node wandelt Payload in Boolean um), softwareseitig getestet via `mosquitto_pub` → [[Node-RED Flow - LED Test]], GitHub-Issue: [#2](https://github.com/47Felix/RasberryPI-Team-13/issues/2) (closed)
- ttyd-Web-Terminal läuft jetzt als systemd-Service, startet automatisch bei Boot/Absturz
- Claude-Skills fürs Projekt geprüft, siehe [[Skills Setup]]
- Neuer Bereich "Tagesplan" im Vault angelegt (Claude erstellt morgens beim Tagesstart eine kurze Standortbestimmung) → [[📅 Tagesplan - Übersicht]]
- **Discord-Bot Grundgerüst gebaut (26.08.2026):** Python-Bot (discord.py) mit Pro-User-Login über `CLAUDE_CONFIG_DIR`, erste Nachricht erfolgreich beantwortet, Test-Branch/Commit über den Bot verifiziert → [[Claude Discord Bot Setup]]
- **Discord-Server-Design-Feature getestet (26.08.2026):** Rollen (Team-Lead/Mitglied/Gast) und Kategorie+Kanäle für das Projekt existierten schon, Server-Icon per API geändert → [[Discord Verwaltung]]
- **main-Branch-Protection eingerichtet (26.08.2026):** Pull Request Pflicht auf `main`, kein Direkt-Push mehr, verifiziert per Testpush → [[Git Workflow]]
- **Pi-Dashboard Software gebaut (27.08.2026):** Flask-App auf dem Pi (Serial-Bridge, SQLite-Logging, Web-Dashboard, Code-Aendern-Formular, Discord-Alarm, Live-Ampel+Zaehler), per systemd-Service dauerhaft, per HTTP end-to-end getestet → [[Erweiterung - Raspberry Pi Dashboard]], GitHub-Issues #37-#42
- **Tailscale-VPN eingerichtet (27.08.2026):** Azure-VM und Pi im selben Tailnet, direkter SSH-Zugriff ohne Chrome-Umweg möglich → [[Pi Zugriff]]
- **Pi-Dashboard Hardware-Test durchgeführt (28.08.2026):** Arduino per USB an den Pi angeschlossen und Events live geprüft. Zwei Bugs gefunden und gefixt: fehlendes Re-Lock-Event nach dem Wiederverriegeln (neues `EVENT:LOCKED`) und fehlendes Live-Update im Dashboard (neuer `/api/status`-Endpunkt + 2s-Polling) → [[Erweiterung - Raspberry Pi Dashboard]], GitHub-Issues #37-#42 (weiterhin offen in GitHub trotz erfolgtem Test)
- **Tresor-Arduino-Sketch fertiggestellt (Tracks A, B, C, D, F, Issues #15-#18 + #20):** Keypad-Eingabe, Servo-Schloss, LCD-Statusanzeige und Buzzer/LED-Alarm in einem gemeinsamen Sketch zusammengeführt und getestet, danach fehlende Funktionsprototypen ergänzt und der Sketch-Ordner bereinigt → [[Issues - Übersicht]]
- **Präsentation für Freitag erstellt (27.08.2026):** 10-Folien Marp-Deck + gerenderte HTML-Version zum Digitalen Tresor (Aufgabe, Architektur, Pi-Dashboard-Erweiterung, Lessons Learned) → [[WS-Kurzprojekt Freitag]]
- **Kurzprojekt "Digitaler Tresor" abgeschlossen (28.08.2026):** Präsentation erfolgreich gehalten, lief gut. Alle Issues (#10-#20, #13-#14) und Milestone #1 geschlossen, GitHub aufgeräumt (8 durchgemergte Branches gelöscht). Pi-Dashboard-Erweiterung (Milestone #5) ebenfalls fertig und per echtem Hardware-Test verifiziert → [[WS-Kurzprojekt Freitag]], [[Erweiterung - Raspberry Pi Dashboard]]

#todo #projekt
