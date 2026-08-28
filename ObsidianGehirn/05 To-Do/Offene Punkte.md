---
tags: [todo, projekt]
---

# Offene Punkte / To-Do

- [ ] **Kurzprojekt & Präsentation bis Freitag 28.08. (TBA Uhr):** Kleinteam (2-3 Personen) finden, kleines RasPi/Arduino/Sensorik-Projekt umsetzen, 10-Minuten-Präsentation vorbereiten – benotungsfrei → [[WS-Kurzprojekt Freitag]]
- [ ] **Vault-Sync-Cron auf Winterzeit umstellen:** Crontab läuft fest auf `45 4 * * *` (UTC), weil `CRON_TZ` auf dieser VM nicht funktioniert (siehe [[Claude Discord Bot Setup]]). Beim Wechsel auf CET (letzter Sonntag im Oktober 2026) manuell auf `45 5 * * *` ändern, sonst läuft der Sync ab dann eine Stunde zu früh (05:45 statt 06:45 Ortszeit).
- [ ] **Sicherheit (dringend):** ttyd auf dem Pi (Port 7681) hat keine eigene Authentifizierung, `team13` ist passwortlos in der sudo-Gruppe – seit Tailscale-Setup fürs ganze Tailnet erreichbar, nicht mehr nur LAN. Absichern (Basic-Auth oder Tailscale-ACL) → [[Pi Zugriff]]
- [ ] **Pi-Systemuhr, Rest-Risiko:** Sync-Ursache gefixt (28.08., siehe Erledigt) – `timesyncd.conf` hatte nur private ITECH-NTP-Server, die außerhalb des Schul-WLANs nie erreichbar waren, jetzt mit oeffentlichen Servern als `FallbackNTP` ergaenzt. Grundproblem (keine RTC-Batterie, `RTC time: 1970-01-01` bei jedem Boot) bleibt aber bestehen – bei jedem Kaltstart ohne Internet zeigt die Uhr wieder falsch, bis NTP zum ersten Mal durchlaeuft. Langfristig: RTC-Modul/-Batterie nachruesten.
- [ ] **Discord-Bot-Token rotieren:** Der `DISCORD_BOT_TOKEN` (Admin-Rechte auf dem ganzen Server!) wurde am 28.08. versehentlich im Klartext in einen Chat gepostet (`.env`-Inhalt kopiert). Sicherheitshalber im Discord Developer Portal neu generieren und überall aktualisieren (Azure-VM-Bot + Pi-`.env`).
- [ ] **Dashboard-Admin-Passwort ändern:** Aktuell auf dem Pi `DASHBOARD_ADMIN_PASSWORD=team13` – sehr schwach/erratbar, sollte auf ein zufälliges Passwort geändert werden (siehe `.env`-Änderungen wirken automatisch, kein Neustart nötig).

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
- **Sketch vom Pi geflasht + Pi-Systemuhr-Sync gefixt (28.08.2026):** `arduino-cli` auf dem Pi eingerichtet (Install-Pfad-Falle, fehlende Keypad-/Servo-Libraries, "Device or resource busy" durch laufenden Dashboard-Service gefunden und umschifft), Sketch erfolgreich geflasht. NTP-Sync repariert: `timesyncd.conf` hatte nur nicht-oeffentliche ITECH-Server, oeffentliche `FallbackNTP`-Server ergaenzt → [[Erweiterung - Raspberry Pi Dashboard]]
- **Dashboard-Design überarbeitet (28.08.2026):** Monitoring-Look (Sidebar, Pill-Badges, Mini-Chart) angelehnt an ein Grafana-Referenzbild + deutlich dramatischerer Alarm (Vollbild-Strobe, Screen-Shake, Warnstreifen, Sirene, GIF) → [[Erweiterung - Raspberry Pi Dashboard]], PR #52/#54

#todo #projekt
