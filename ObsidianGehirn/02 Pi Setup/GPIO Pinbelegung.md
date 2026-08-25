---
tags: [pi, hardware, gpio]
---

# GPIO-Pinbelegung (Raspberry Pi, 40-Pin-Header)

Referenzbild für Team13-1, erstellt am 25.08.2026. Zeigt die Standard-Pinbelegung des 40-Pin-GPIO-Headers (physische Pin-Nummern), inkl. Power/Ground/GPIO/Sonderfunktionen (I2C/SPI/UART).

![GPIO-Pinbelegung](assets/gpio-pinout-team13.png)

## Aktuell genutzt
- **Pin 7 / GPIO4** – LED-Test-Flow, siehe [[Node-RED Flow - LED Test]]
- **Ground (z.B. Pin 6 oder 9)** – für die LED-Rückleitung

## Hinweis
Bei weiteren Sensoren/Aktoren (z.B. Arduino/Elegoo-Kit-Sensoren, falls später am Pi statt am Arduino verkabelt) hier nachschlagen, welche Pins schon belegt sind bzw. welche sich für I2C/SPI eignen.

## Verwandte Notizen
- [[Node-RED Flow - LED Test]]
- [[Pi Zugriff]]
- [[Installierte Services]]
- [[Kurs - Elektrotechnik]]

#pi #hardware #gpio
