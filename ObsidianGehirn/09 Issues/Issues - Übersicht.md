---
tags: [github, issues, projekt]
---

# GitHub Issues – Übersicht

Zusammenfassung aller GitHub-Issues des Repos, aufgeteilt nach offen/geschlossen. Bei geschlossenen Issues steht jeweils kurz, **was gemacht wurde** – nicht nur, dass es erledigt ist. Wird von Claude gepflegt, siehe [[Doku-Regeln]].

> [!important] Regel
> Sobald ein GitHub-Issue abgeschlossen/gemerged wird, trägt Claude hier einen kurzen Eintrag ein (2-4 Sätze, was gemacht wurde) und verschiebt ihn von "🟢 Offen" nach "✅ Geschlossen". Siehe [[Doku-Regeln]] Abschnitt "GitHub Issues".

## 🟢 Offen

### Kurzprojekt "Digitaler Tresor" (Milestone [#1](https://github.com/47Felix/RasberryPI-Team-13/milestone/1), Deadline 28.08.2026)
- [#13](https://github.com/47Felix/RasberryPI-Team-13/issues/13) Kurzpräsentation vorbereiten (10 Minuten)
- [#14](https://github.com/47Felix/RasberryPI-Team-13/issues/14) Präsentation am Freitag halten
- [#15](https://github.com/47Felix/RasberryPI-Team-13/issues/15) Track A – Keypad-Eingabe + Code-Prüf-Logik (@47Felix)
- [#16](https://github.com/47Felix/RasberryPI-Team-13/issues/16) Track B – Servo-Schließmechanismus
- [#17](https://github.com/47Felix/RasberryPI-Team-13/issues/17) Track C – LCD1602-Statusanzeige
- [#18](https://github.com/47Felix/RasberryPI-Team-13/issues/18) Track D – Buzzer + LED Feedback und Alarm-Logik
- [#19](https://github.com/47Felix/RasberryPI-Team-13/issues/19) Track E – Box/Gehäuse bauen
- [#20](https://github.com/47Felix/RasberryPI-Team-13/issues/20) Track F – Gesamtintegration (braucht #15-#18 fertig)

Details/Aufteilung siehe [[WS-Kurzprojekt Freitag]].

## ✅ Geschlossen (was wurde gemacht)

- **[#1](https://github.com/47Felix/RasberryPI-Team-13/issues/1) LED-Hardware auf Breadboard aufbauen** – LED + Vorwiderstand an GPIO4/Pin7 + Ground verkabelt, bestehender Node-RED-Flow erfolgreich getestet. Siehe [[Node-RED Flow - LED Test]].
- **[#2](https://github.com/47Felix/RasberryPI-Team-13/issues/2) Node-RED mit MQTT verknüpfen** – LED-Flow um Topic `team13-1/led/set` erweitert (Broker localhost:1883), Function-Node wandelt Payload in Boolean um, softwareseitig via `mosquitto_pub` getestet. Siehe [[Node-RED Flow - LED Test]].
- **[#3](https://github.com/47Felix/RasberryPI-Team-13/issues/3) Arduino + Elegoo-Kit Temperatursensor testen** – DHT11-Modul auf Breadboard mit Elegoo-UNO-R3 verkabelt, Arduino-Sketch mit DHT-Library geschrieben, Sensor liefert Werte (Kalibrierung/Wackelkontakt war noch ein Thema). Siehe [[Dogan - Brain Dump]].
- **[#10](https://github.com/47Felix/RasberryPI-Team-13/issues/10) Kleinteam bilden** – 4er-Team steht (ganzes Team 13).
- **[#11](https://github.com/47Felix/RasberryPI-Team-13/issues/11) Projektidee finden** – Entscheidung für "Digitaler Tresor / Escape-Box" (Keypad + Servo-Schloss + LCD + Buzzer/LED) aus dem Elegoo-UNO-R3-Kit. Siehe [[WS-Kurzprojekt Freitag]].
- **[#12](https://github.com/47Felix/RasberryPI-Team-13/issues/12) Kurzprojekt umsetzen (Hardware+Software)** – war zu grob geschnitten, aufgeteilt in die 6 parallelen Tracks #15-#20 (siehe oben).

## Verwandte Notizen
- [[WS-Kurzprojekt Freitag]]
- [[Offene Punkte]]
- [[Doku-Regeln]]

#github #issues #projekt
