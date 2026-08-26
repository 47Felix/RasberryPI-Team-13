---
tags: [todo, projekt]
---

# Offene Punkte / To-Do

- [ ] **Arduino + Elegoo-Kit: Temperatur-/Feuchtigkeitssensor testen (heute Dogan):** Sensor aus dem Elegoo-Starterkit am Arduino aufbauen, über Arduino-IDE auslesen, Ergebnis in [[Dogan - Brain Dump]] festhalten, siehe [[2026-08-25]] (Tagesplan), GitHub-Issue: [#3](https://github.com/47Felix/RasberryPI-Team-13/issues/3)
- [ ] **Kurzprojekt & Präsentation bis Freitag 28.08. (TBA Uhr):** Kleinteam (2-3 Personen) finden, kleines RasPi/Arduino/Sensorik-Projekt umsetzen, 10-Minuten-Präsentation vorbereiten – benotungsfrei → [[WS-Kurzprojekt Freitag]]

## Erledigt ✅
- **Node-RED mit MQTT verknüpft (25.08.2026):** LED-Flow um Topic `team13-1/led/set` erweitert (mqtt-broker localhost:1883, Function-Node wandelt Payload in Boolean um), softwareseitig getestet via `mosquitto_pub` → [[Node-RED Flow - LED Test]], GitHub-Issue: [#2](https://github.com/47Felix/RasberryPI-Team-13/issues/2) (closed)
- ttyd-Web-Terminal läuft jetzt als systemd-Service, startet automatisch bei Boot/Absturz
- Claude-Skills fürs Projekt geprüft, siehe [[Skills Setup]]
- Neuer Bereich "Tagesplan" im Vault angelegt (Claude erstellt morgens beim Tagesstart eine kurze Standortbestimmung) → [[📅 Tagesplan - Übersicht]]
- **Discord-Bot Grundgerüst gebaut (26.08.2026):** Python-Bot (discord.py) mit Pro-User-Login über `CLAUDE_CONFIG_DIR`, erste Nachricht erfolgreich beantwortet, Test-Branch/Commit über den Bot verifiziert → [[Claude Discord Bot Setup]]
- **Discord-Server-Design-Feature getestet (26.08.2026):** Rollen (Team-Lead/Mitglied/Gast) und Kategorie+Kanäle für das Projekt existierten schon, Server-Icon per API geändert → [[Discord Verwaltung]]
- **main-Branch-Protection eingerichtet (26.08.2026):** Pull Request Pflicht auf `main`, kein Direkt-Push mehr, verifiziert per Testpush → [[Git Workflow]]

#todo #projekt
