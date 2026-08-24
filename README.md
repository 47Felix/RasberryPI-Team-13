# RasberryPI-Team-13 – Smart Systems Projekt (BH4ab)

Projekt-Repository für das Lernfeld **Smart Systems 2026** (ITECH), Team 13.

## Roter Faden: "Ice Truck" Kühlketten-Szenario

Über drei Challenges hinweg wird eine IoT-Lösung für ein Kühl-Truck-Szenario entwickelt:

1. **Challenge I – The Ice Truck Problem** (Signale & Bus-Systeme): Kühlkette lückenlos überwachen.
2. **Challenge II – The Ice Truck Extension** (Kommunikationssysteme & Entwicklungswerkzeuge): mobile App zur Überwachung/Steuerung von außerhalb.
3. **Challenge III – Ice Truck in Cloud** (IoT in Cloud): Daten in einer Cloud speichern und auswerten.

## Hardware

- Raspberry Pi (Hostname `Team13-1`, Raspberry Pi OS / Debian trixie, 64-bit)
- Node-RED zur grafischen Verknüpfung von GPIOs, MQTT, HTTP
- Mosquitto als lokaler MQTT-Broker
- Aktuell in Arbeit: LED-Testschaltung an GPIO4 (Pin 7), gesteuert über einen Node-RED-Flow mit zwei Inject-Buttons ("LED an" / "LED aus")

## Wichtige Dienste auf dem Pi

| Dienst | Port | Zugriff |
|---|---|---|
| Node-RED Editor | 1880 | `http://team13-1.local:1880` |
| Web-Terminal (ttyd) | 7681 | `http://team13-1.local:7681` |
| Mosquitto (MQTT) | 1883 | intern |

Alle Dienste laufen als systemd-Services mit Autostart (`nodered.service`, `ttyd.service`, `mosquitto`).

## Setup / Erste Schritte

```bash
sudo apt update && sudo apt install git -y
git clone https://github.com/47Felix/RasberryPI-Team-13.git
```

Weiteres Setup (NTP, SSH, Node.js/Node-RED-Installation) siehe Moodle-Kurs "Einführung in die IoT-Programmierung mit Node-RED" (Kurs-ID 1248).

## Status / offene Punkte

- [x] Raspberry Pi OS aufgesetzt, SSH & WLAN vorkonfiguriert
- [x] NTP-Zeitsynchronisation mit ITECH-Servern eingerichtet
- [x] Node-RED + Mosquitto installiert und lauffähig
- [x] LED-Flow in Node-RED gebaut (softwareseitig)
- [ ] Hardware-Aufbau: LED + Vorwiderstand auf Breadboard verkabeln
- [ ] Node-RED mit MQTT verknüpfen
- [ ] Fernzugriff (DynDNS / Dashboard) für Challenge II

## Team

Team 13 – BH4ab, Smart Systems (ITECH)
