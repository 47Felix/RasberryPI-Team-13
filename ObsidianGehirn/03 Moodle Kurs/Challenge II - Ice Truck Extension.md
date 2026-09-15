---
tags: [moodle, challenges]
---

# Challenge II: "The Ice Truck Extension"

**Schwerpunkt:** Kommunikationssysteme & Entwicklungswerkzeuge

## Szenario
Die Temperaturkontrolle soll während Fahrt- und Pausenzeiten nicht nur der Technik überlassen werden. Es soll eine App für mobile Endgeräte entwickelt werden, mit der man die Kühlung auch von außerhalb des Kühlraums überwachen/steuern kann.

→ Baut auf [[Challenge I - Ice Truck Problem]] auf und erweitert die technische Lösung um Kommunikation/App-Anbindung.

## Relevante Kursinhalte
- [[Kurs - MQTT]] – Kommunikation zwischen Geräten
- [[Kurs - Node-RED]], Kapitel F (HTTP Request)
- Fernzugriff-Konzepte: DynDNS, Apache-Webserver (siehe [[Technischer Fahrplan]] Punkt 10)

## Konkrete Aufgabenstellung (erhalten 15.09.2026)

> Weitere Probleme
> Aktuell wertet der Raspberry Pi die Sensordaten aus und steuert entsprechend die Kühlung des Trucks. Eine Kontrolle der Temperatur ist momentan nur durch Sichtkontakt der LEDs im Kühlraum möglich. Dafür muss eine Person aktiv den Kühlraum betreten und die LEDs kontrollieren. Dies ist natürlich mit sehr viel Aufwand verbunden und außerdem nur bei Stillstand des Fahrzeugs möglich.
>
> Erweiterung des Prototypen
> Ihr sollt einen Prototypen entwickeln, mit welchem Personen mit Hilfe mobiler Endgeräte, wie Handys oder Tablets, komfortabel die Informationen über die Temperaturen auch außerhalb des Kühlraumes erhalten können. Zusätzlich soll eine Möglichkeit zur Verfügung gestellt werden, über das mobile Endgerät Aktoren anzusteuern.
>
> Es besteht der ausdrückliche Wunsch der Unternehmensleitung, dass Optimierungen und Erweiterungen während der Entwicklungsphase vorgenommen werden. Bleibt also weiterhin kreativ!
>
> Die Produktidee als Ergebnis des erweiterten Brainstormings
>
> Für die Kommunikation zwischen Mobilen Endgeräten und dem Raspberry Pi wird das MQTT-Protokoll eingesetzt. (Als MQTT Broker stellt die ITECH einen hausinternen Broker zur Verfügung. Ihr könnt aber auch auf dem Raspberry selbst einen Broker installieren.)
>
> Um die Verbindung von Hardware, Schnittstellen und Services umzusetzen, verwendet ihr das Framework Node-RED.
>
> Geeignete Anwendungen sind beispielsweise MQTT Dash (Android) oder MQTT Explorer.
>
> Handlungen: MQTT verstehen und anwenden, Node-RED kennenlernen und erkunden, Szenario Challenge 1 erweitern.

**Kernanforderungen daraus:**
- Kein Eigenbau einer nativen App nötig – **MQTT Dash** (Handy/Tablet) oder **MQTT Explorer** sind explizit als ausreichende Endgeräte-Anwendung genannt
- **MQTT-Broker**: entweder der hausinterne ITECH-Broker oder ein lokaler Broker auf dem Pi (Mosquitto läuft laut README.md bereits)
- **Node-RED** ist das vorgeschriebene Integrations-Framework zwischen Hardware/Schnittstellen (I2C-Bus, SQL aus Challenge I) und den MQTT-Services
- Mobile Anzeige der Temperaturdaten + Fernsteuerung der Aktoren (Lüfter/Ventil aus Challenge I) über MQTT
- Ausdrücklicher Wunsch nach eigenen Optimierungen/Erweiterungen während der Umsetzung ("bleibt kreativ")

In 4 Tracks heruntergebrochen (#193-#196), siehe [[Issues - Übersicht]].

## Prüfungsbezug
Nach dieser Challenge: Kurztest (20%), siehe [[Leistungsnachweise]]

## Nächste Challenge
→ [[Challenge III - Ice Truck in Cloud]]

#moodle #challenges
