---
tags: [todo, projekt]
---

# Offene Punkte / To-Do

- [ ] **Hardware:** LED + Vorwiderstand (330–470 Ω) auf Breadboard bauen und an GPIO4/Pin7 + Ground anschließen, dann den bereits deployten Node-RED-Flow testen → [[Node-RED Flow - LED Test]], GitHub-Issue: [#1](https://github.com/47Felix/RasberryPI-Team-13/issues/1)
- [ ] Git-Repository auf dem Pi klonen (`git clone https://github.com/47Felix/RasberryPI-Team-13.git`) → [[Technischer Fahrplan]] Punkt 5
- [ ] **Arduino + Elegoo-Kit: Temperatur-/Feuchtigkeitssensor testen (heute Dogan):** Sensor aus dem Elegoo-Starterkit am Arduino aufbauen, über Arduino-IDE auslesen, Ergebnis in [[Dogan - Brain Dump]] festhalten, siehe [[2026-08-25]] (Tagesplan), GitHub-Issue: [#3](https://github.com/47Felix/RasberryPI-Team-13/issues/3)
- [ ] Später prüfen: Arduino-Sensordaten mit Pi/Node-RED zusammenführen (seriell oder MQTT)
- [ ] Einschreibekennwort für "Signale und Bussysteme" (Kurs-ID 1574) bei der Lehrkraft erfragen (allgemeiner "#Abrakadabra!"-Schlüssel hat nicht funktioniert) → [[Challenge I - Ice Truck Problem]]
- [ ] Einschreibekennwort für "Datenbankanbindung und ORM" (Kurs-ID 564) bei Bedarf erfragen → [[Challenge III - Ice Truck in Cloud]]
- [ ] Raspberry-Pi-Workshop-PDF ("Raspberry_Pi_WS.pdf") aus dem Downloads-Ordner in den Projektordner verschieben → [[WS-Präsentationen]]
- [ ] Arduino-Workshop-PDF ("260821_Arduino_PräseX.pdf") ist entgegen alter Notiz **nicht** im Repository auffindbar – tatsächlichen Ablageort klären und ins Repo legen → [[WS-Präsentationen]]
- [ ] Bereich "Einen Pitch planen und durchführen" (4.9) in Moodle noch ohne Inhalte – später erneut prüfen
- [ ] **Sicherheit (dringend):** Obsidian "Local REST API"-Plugin-Key war öffentlich im Repo committet – Anton muss den API-Key in Obsidian neu generieren (Plugin-Settings → Regenerate) → [[⚠️ Zugangsdaten - Hinweis]]
- [ ] **Kurzprojekt & Präsentation bis Freitag 28.08. (TBA Uhr):** Kleinteam (2-3 Personen) finden, kleines RasPi/Arduino/Sensorik-Projekt umsetzen, 10-Minuten-Präsentation vorbereiten – benotungsfrei → [[WS-Kurzprojekt Freitag]]
- [ ] **Discord-Bot:** Restliche Teammitglieder registrieren (eigener `claude login` per SSH + `!register <name>` im Discord-Kanal) → [[Claude Discord Bot Setup]]
- [ ] **Discord-Bot:** systemd-Service (`discord-claude-bot.service`) einrichten/prüfen, damit der Bot Neustarts und `Strg+C` übersteht → [[Claude Discord Bot Setup]]
- [ ] **Sicherheit:** Discord-Bot-Token wurde versehentlich im Klartext in einem Chat geteilt – im Developer Portal unter "Bot" → "Reset Token" rotieren und `.env` auf der VM aktualisieren
- [ ] **Discord-Bot:** Entscheiden, ob eine Claude-Session pro User+Thread statt nur pro User sinnvoller ist (aktuell teilen sich alle Threads eines Users dieselbe Konversation) → [[Claude Discord Bot Setup]]
- [ ] **Discord-Bot:** Prüfen, ob `--dangerously-skip-permissions` durch eine feinere Tool-Allowlist ersetzt werden soll → [[Claude Discord Bot Setup]]
- [ ] **Discord-Bot:** Server-Design-Feature (Rollen/Kanäle per Discord-API über `DISCORD_API.md`) erstmals testen, dabei Rollen-Hierarchie der Bot-Rolle prüfen → [[Claude Discord Bot Setup]]

## Erledigt ✅
- **Node-RED mit MQTT verknüpft (25.08.2026):** LED-Flow um Topic `team13-1/led/set` erweitert (mqtt-broker localhost:1883, Function-Node wandelt Payload in Boolean um), softwareseitig getestet via `mosquitto_pub` → [[Node-RED Flow - LED Test]], GitHub-Issue: [#2](https://github.com/47Felix/RasberryPI-Team-13/issues/2) (closed)
- ttyd-Web-Terminal läuft jetzt als systemd-Service, startet automatisch bei Boot/Absturz
- Claude-Skills fürs Projekt geprüft, siehe [[Skills Setup]]
- Neuer Bereich "Tagesplan" im Vault angelegt (Claude erstellt morgens beim Tagesstart eine kurze Standortbestimmung) → [[📅 Tagesplan - Übersicht]]
- **Discord-Bot Grundgerüst gebaut (26.08.2026):** Python-Bot (discord.py) mit Pro-User-Login über `CLAUDE_CONFIG_DIR`, erste Nachricht erfolgreich beantwortet, Test-Branch/Commit über den Bot verifiziert → [[Claude Discord Bot Setup]]

#todo #projekt
