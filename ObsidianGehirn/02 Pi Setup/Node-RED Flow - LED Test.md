---
tags: [pi, nodered, hardware, mqtt]
---

# Node-RED Flow: LED-Test

## Aktueller Stand
Zwei Inject-Buttons **"LED an"** (`payload: boolean true`) und **"LED aus"** (`payload: boolean false`) → verbunden mit einem `rpi-gpio out`-Node namens **"LED"** auf **GPIO4 / physischer Pin 7**, Typ "Digitaler Ausgang". Deployed und aktiv (Status "OK").

## ✅ MQTT-Anbindung (erledigt 25.08.2026, GitHub-Issue #2)
Der Flow steuert die LED jetzt zusätzlich über MQTT:
- **`mqtt-broker`-Config:** `localhost:1883` (lokaler Mosquitto-Broker, siehe [[Installierte Services]])
- **`mqtt in`-Node "LED via MQTT":** Topic `team13-1/led/set`, QoS 0
- **Function-Node "MQTT -> Boolean":** wandelt den Payload (`"on"`/`"off"`/`"true"`/`"false"`/`"1"`/`"0"`, case-insensitive) in ein Boolean um
- Verkabelt: `LED via MQTT` → `MQTT -> Boolean` → bestehender `LED`-Node (zusätzlich zu den beiden Inject-Buttons)

**Getestet** über das ttyd-Terminal (`http://team13-1.local:7681`):
```bash
mosquitto_pub -h localhost -t team13-1/led/set -m "on"
mosquitto_pub -h localhost -t team13-1/led/set -m "off"
```
Node-Status wechselt dabei korrekt zwischen `true`/`false` (softwareseitig bestätigt – die physische LED kann erst nach dem Hardware-Aufbau unten wirklich leuchten sehen).

Das ist die Grundlage für die Fernsteuerung in [[Challenge II - Ice Truck Extension]].

## Offen – Hardware-Aufbau (Issue #1, Anton)
LED + Vorwiderstand (330–470 Ω) auf ein Breadboard bauen:
- längeres LED-Bein → über Widerstand → GPIO4 / Pin 7
- kürzeres Bein → Ground-Pin (z.B. Pin 6 oder 9)

![GPIO-Pinbelegung](assets/gpio-pinout-team13.png)
(siehe auch [[GPIO Pinbelegung]] für die volle Übersicht)

Danach im Node-RED-Editor (`http://team13-1.local:1880`) auf "LED an"/"LED aus" klicken oder per MQTT (`team13-1/led/set`) testen.

> [!note] Elektrotechnik-Grundlage
> Vorwiderstandsberechnung für LEDs wird im Kurs [[Kurs - Elektrotechnik]] behandelt (Kurs-ID 885).

## Verwandte Notizen
- [[Installierte Services]]
- [[Offene Punkte]]
- [[Kurs - MQTT]]
- [[Kurs - Node-RED]]

#pi #nodered #hardware #mqtt
