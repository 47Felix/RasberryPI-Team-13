# RasberryPI-Team-13 – Smart Systems Projekt (BH4ab)

Projekt-Repository für das Lernfeld **Smart Systems 2026** (ITECH), Team 13.

## Roter Faden: "Ice Truck" Kühlketten-Szenario

Über drei Challenges hinweg wird eine IoT-Lösung für ein Kühl-Truck-Szenario entwickelt:

1. **Challenge I – The Ice Truck Problem** (Signale & Bus-Systeme): Sensor-Arduino(s) lesen Temperatur/Feuchte/Licht/Taster (analog, digital, Bus-Protokoll) aus, je Sensor eine PWM-LED zeigt den Messwert an, ein Aktor-Arduino regelt Lüfter (Transistor/H-Brücke) und Ventil (Servo). Der Pi liest alles per I2C, loggt es in SQL und steuert die Aktorik.
2. **Challenge II – The Ice Truck Extension** (Kommunikationssysteme & Entwicklungswerkzeuge): Temperaturdaten anzeigen und Aktoren fernsteuern von mobilen Endgeräten aus – per MQTT (ITECH-Broker oder lokaler Mosquitto) und Node-RED als Integrationsschicht, mit MQTT Dash/MQTT Explorer statt einer selbstgebauten App.
3. **Challenge III – Ice Truck in Cloud** (IoT in Cloud): Daten in einer Cloud speichern und auswerten.

## Hardware

- Raspberry Pi (Hostname `Team13-1`, Raspberry Pi OS / Debian trixie, 64-bit)
- Node-RED zur grafischen Verknüpfung von GPIOs, MQTT, HTTP
- Mosquitto als lokaler MQTT-Broker
- LED-Testschaltung an GPIO4 (Pin 7), gesteuert über einen Node-RED-Flow mit zwei Inject-Buttons ("LED an" / "LED aus")
- Arduino Uno (Elegoo-Kit) für Challenge I: DHT22 (Temp/Feuchte), Fotowiderstand (LDR), Taster, 3 Status-LEDs, Lüfter über Transistor, Servo fürs Kühlraum-Ventil

## Challenges – Code & Stand

- **Challenge I** (Signale & Bus-Systeme): [`Challenge-I-Ice-Truck/Code/`](Challenge-I-Ice-Truck/Code/README.md) – Arduino-Sketch (Pinbelegung siehe dort) + Pi-Backend (SQLite-Logging, Regellogik), real verkabelt, siehe README für aktuellen Stand/offene Punkte
- **Challenge II** (Kommunikationssysteme & Entwicklungswerkzeuge): [`Challenge-II-Ice-Truck-Extension/Code/`](Challenge-II-Ice-Truck-Extension/Code/README.md) – MQTT-Topic-Schema + Node-RED-Bridge, mobile Anzeige/Steuerung per MQTT Dash/Explorer statt Eigenbau-App
- **Challenge III**: noch nicht begonnen

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
- [x] Hardware-Aufbau: LED + Vorwiderstand auf Breadboard verkabelt (Issue #1)
- [x] Node-RED mit MQTT verknüpft (Issue #2)
- [x] Challenge I: Arduino-Sketch (Sensoren + Aktoren auf einem Board) + Pi-Backend mit SQLite-Logging/Regellogik geschrieben, DHT11/DHT22-Bug gefixt (Issue #191, noch ungetestet)
- [ ] Challenge I: I2C-Verkabelung Arduino ↔ Pi (SDA/SCL aktuell noch unbeschaltet), danach Regellogik + Aktor-Ansteuerung über den Pi laufen lassen (Issue #180)
- [ ] Challenge II: MQTT-Topic-Schema + Node-RED-Bridge entworfen, noch nicht gegen echten Broker getestet
- [ ] Fernzugriff (DynDNS / Dashboard) für Challenge II

## Team

Team 13 – BH4ab, Smart Systems (ITECH)
