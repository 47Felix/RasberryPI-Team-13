---
tags: [moodle, mqtt]
---

# "MQTT verstehen und anwenden"

Kurs-ID 1298, bereits eingeschrieben.

IoT wird immer populärer, viele Geräte kommunizieren miteinander (Sensordaten wie Temperatur, Füllstände etc.). Bei vielen Geräten im Netzwerk entsteht große Datenlast → im IoT-Bereich werden komprimierte, leichtgewichtige Protokolle genutzt, MQTT ist eines davon.

## Kompetenzen
- IoT-Architektur erläutern
- MQTT-Protokoll & Funktionsweise verstehen
- Verschiedene MQTT-Broker kennen
- Eigene IoT-Projekte planen/durchführen

## Bezug zum eigenen Projekt
Mosquitto-Broker läuft bereits auf dem Pi (siehe [[Installierte Services]]) und ist seit 25.08.2026 mit Node-RED verknüpft (Kapitel D, siehe [[Kurs - Node-RED]] und [[Node-RED Flow - LED Test]]) – Topic `team13-1/led/set` steuert die LED. Relevant vor allem für [[Challenge II - Ice Truck Extension]] und [[Challenge III - Ice Truck in Cloud]].

## Grundlagen einfach erklärt (für Fachgespräch/Prüfung)

**Was ist MQTT?** Ein sehr leichtgewichtiges Nachrichtenprotokoll, speziell für IoT entwickelt – für Geräte mit wenig Rechenleistung und wackliger Verbindung. Statt dass Geräte sich direkt miteinander verbinden, läuft alles über einen zentralen Vermittler.

**Die drei Grundbegriffe:**
- **Broker:** der zentrale Vermittler. Bei uns Mosquitto, lokal auf dem Pi (Port 1883). Alle Geräte verbinden sich nur mit dem Broker, nie direkt miteinander.
- **Topic:** eine Art Kanal/Adresse für Nachrichten, z.B. `team13-1/led/set`. Wie ein Ordnerpfad zu lesen (`team13-1/temperatur/aktuell` usw.).
- **Publish/Subscribe:** Geräte können **publishen** (eine Nachricht an ein Topic senden) oder **subscriben** (ein Topic abonnieren und benachrichtigt werden). Sender kennt die Empfänger nicht und umgekehrt – beide reden nur mit dem Broker.

**Konkretes Beispiel aus unserem LED-Flow:** `mosquitto_pub -h localhost -t team13-1/led/set -m "on"` veröffentlicht die Nachricht "on" unter dem Topic `team13-1/led/set`. Der `mqtt in`-Node in Node-RED hat dieses Topic abonniert und bekommt die Nachricht automatisch zugestellt, der Flow wandelt sie in ein Boolean um und schaltet GPIO4.

**Warum wichtig fürs Projekt:** Genau dieses Prinzip ist die Basis für Challenge II (App von außerhalb steuern – die App müsste nur eine Nachricht an das Topic schicken, egal ob im selben Netz oder über DynDNS von außen) und oft auch für Challenge III (viele Cloud-IoT-Plattformen sprechen selbst MQTT).

#moodle #mqtt
