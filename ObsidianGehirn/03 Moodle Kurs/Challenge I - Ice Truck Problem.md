---
tags: [moodle, challenges]
---

# Challenge I: "The Ice Truck Problem"

**Schwerpunkt:** Signale & Bus-Systeme

## Szenario
Um gleichbleibende Qualität/Haltbarkeit von Lebensmitteln zu sichern, muss die gesetzlich vorgeschriebene Kühltemperatur (Kühlkette) durchgängig eingehalten werden – von Herstellung über Transport bis Lagerung im Einzelhandel.

→ Vertieft die Grundlagen aus dem Workshop anhand eines praktischen Beispiels.

## Relevante Kursinhalte
- [[Kurs - Elektrotechnik]] (Signale, Widerstände, Schaltungen)
- "Signale und Bussysteme" (Kurs-ID 1574) – passt inhaltlich genau, Einschreibekennwort seit 14.09.2026 besorgt (Issue #167), Kursmaterialien liegen unter `ObsidianGehirn/03 Moodle Kurs/Signale und Bussysteme/`

## Konkrete Aufgabenstellung (erhalten 14.09.2026)

> Der Kühlraum eines Transportes kann über zwei Mechanismen geregelt werden:
>
> Für einfache Kühlanforderungen sind im Kühlraum Lüfter vorhanden, die in ihrer Drehzahl geregelt werden können. Diese Lüfter werden von einem Arduino über einen Transistor oder eine H-Brücke angesteuert.
> Für höhere Anforderungen (niedrige Temperaturen) kann bei Bedarf kalte Luft über ein Ventil in den Kühlraum gelassen werden. Der Durchfluss des Ventils wird über einen Servomotor eingestellt, der ebenfalls an dem Arduino angeschlossen ist. Zur Ermittlung der Temperatur werden im Kühlraum mehrere Arduinos installiert, die die Daten der angeschlossenen Sensoren aufnehmen und an einen zentralen Raspberry Pi weiterleiten. Da mehrere Arduinos mit dem Raspberry Pi kommunizieren, bietet sich ein Busprotokoll wie I2C an.
>
> An den Arduinos ist je Sensor eine LED angeschlossen, die leuchtet, wenn Daten an den Sensoren gemessen werden. Die Helligkeit der LEDs ist ein Indikator für die Höhe der Messwerte des jeweiligen Sensors.
>
> Die angeschlossenen Sensoren liefern Daten unterschiedlichen Formats (analog, Digital 1/0 und über ein Bus-Protokoll, z.B. I2C, SPI, o.ä.).
>
> Die Messdaten werden in einer SQL-Datenbank auf dem Raspberry Pi protokolliert. Zudem wertet der Raspberry Pi die Sensordaten aus und steuert den Lüfter und das Ventil über den für die Aktoren zuständigen Arduino.

**Kernanforderungen daraus:**
- Mindestens ein **Sensor-Arduino** (mehrere im Original-Szenario) liest Sensoren unterschiedlicher Formate (analog, digital 1/0, Bus-Protokoll wie I2C/SPI) und steuert je Sensor eine LED, deren **Helligkeit (PWM) proportional zum Messwert** ist
- Ein **Aktor-Arduino** steuert Lüfter (Transistor/H-Brücke, drehzahlgeregelt) und Ventil (Servomotor)
- **I2C-Bus** zwischen (mehreren) Arduino(s) und dem Raspberry Pi
- Raspberry Pi: **SQL-Datenbank-Logging** der Messwerte + Auswertungslogik, die darüber den Lüfter/das Ventil über den Aktor-Arduino ansteuert (Regelkreis: Pi wertet aus → Pi entscheidet → Pi schickt Stellwert an Aktor-Arduino)

Damit ist das vorherige technische Vorgehen (Node-RED/MQTT/Discord-Alarm, Issues #171-#174) **überholt** - die echte Aufgabe verlangt I2C-Bus + SQL + Aktorik, kein reines Monitoring-Dashboard. Siehe [[Issues - Übersicht]] für den aktuellen Issue-Stand.

## Aktueller Hardware-Stand (17.09.2026)

Real verkabelt sind zwei Arduino Unos: Sensor-Board (I2C 0x08) trägt nur ein KY-028-Modul, Aktor-Board (I2C 0x09) trägt den DHT22 (Temp/Feuchte) plus Lüfter und Servo und meldet die Klimadaten mit an den Pi. Ein zwischenzeitlicher Ein-Board-Aufbau (14.-17.09.) und ein ursprünglich angenommener Türkontakt/Taster sind wieder entfallen. Details, Pinbelegung und offene Punkte (I2C-Verkabelung zum Pi, KY-028-Kalibrierung, DHT22-Verifikation) siehe `Challenge-I-Ice-Truck/Code/README.md` und [[Issues - Übersicht]] (#180, #184, #191).

Der DHT22 wurde inzwischen ersetzt (beide Boards senden jetzt einen KY-028-Rohwert, siehe README "Hardware-Update 5"). Am 18.09.2026 kam beim Live-Testen ein I2C-Protokollbug ans Licht: `smbus2`s `write_i2c_block_data()`/`read_i2c_block_data()` schicken ein zusätzliches SMBus-Register-/Längen-Byte, das die Arduino-Firmware nicht erwartet (sie sendet/erwartet rohe Bytes ohne Register-Präfix) - dadurch kamen sowohl die Aktor-Sollwerte am Arduino als auch die Sensor-Rohwerte am Pi verschoben/falsch an. Fix in beiden Richtungen: `smbus2.i2c_msg.write()`/`i2c_msg.read()` statt der Block-Data-Funktionen. Details siehe README "Hardware-Update 6" und Docstring in `pi-backend/hardware.py`.

Danach lief der Luefter trotz korrekter I2C-Sollwerte immer noch nicht: Ursache war ein Pin-/Timer-Konflikt in `actor_arduino.ino`, nicht I2C. Die `Servo`-Bibliothek belegt auf dem Arduino Uno fest Timer1 fuer ihre Pulserzeugung (unabhaengig davon, an welchem Pin der Servo haengt), Timer1 ist aber auch der Hardware-Timer hinter `analogWrite()` auf D9/D10 - sobald `valveServo.attach()` lief, gab D9 (der bisherige Luefter-Pin) kein sauberes PWM mehr aus. Fix (18.09.2026): Luefter-PWM von D9 auf **D3** (Timer2) verschoben. **Erfordert physisches Umstecken** des Luefter-Signalkabels von D9 auf D3 am Aktor-Board, sonst bleibt der Luefter aus. Details siehe README "Hardware-Update 7".

## Nächste Challenge
→ [[Challenge II - Ice Truck Extension]]

#moodle #challenges
