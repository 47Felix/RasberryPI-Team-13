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
- [#19](https://github.com/47Felix/RasberryPI-Team-13/issues/19) Track E – Box/Gehäuse bauen (bewusst nicht gebaut, benotungsfrei)

Details/Aufteilung siehe [[WS-Kurzprojekt Freitag]].

### Pi-Dashboard (Erweiterung, [[Erweiterung - Raspberry Pi Dashboard]])
- [#37](https://github.com/47Felix/RasberryPI-Team-13/issues/37) Track G – Arduino zu Pi Anbindung — Software fertig, seit 28.08.2026 per echtem Hardware-Test verifiziert (2 dabei gefundene Bugs gefixt, siehe [[Erweiterung - Raspberry Pi Dashboard]])
- [#38](https://github.com/47Felix/RasberryPI-Team-13/issues/38) Track H – Backend/Logging auf dem Pi — SQLite-Logging fertig, per HTTP + echtem Hardware-Test verifiziert
- [#39](https://github.com/47Felix/RasberryPI-Team-13/issues/39) Track I – Web-Dashboard Frontend — Flask-Dashboard fertig, läuft als systemd-Service, seit 28.08.2026 mit Live-Updates per Polling (kein manuelles Neuladen mehr nötig)
- [#40](https://github.com/47Felix/RasberryPI-Team-13/issues/40) Track J – Code/Passwort über Webinterface ändern — Formular fertig, eigenes Admin-Passwort
- [#41](https://github.com/47Felix/RasberryPI-Team-13/issues/41) Stretch – Discord-Bot meldet Alarm automatisch — implementiert (direkter API-Call bei EVENT:ALARM)
- [#42](https://github.com/47Felix/RasberryPI-Team-13/issues/42) Stretch – Live-Status-Anzeige + Versuchszähler — als Text-Ampel im Dashboard umgesetzt

Alle sechs noch **offen** in GitHub (Stand 28.08.2026), obwohl die Hardware-in-the-loop-Verifikation inzwischen erfolgt ist – siehe [[Erweiterung - Raspberry Pi Dashboard]] Abschnitt "Hardware-Test".

## ✅ Geschlossen (was wurde gemacht)

- **[#1](https://github.com/47Felix/RasberryPI-Team-13/issues/1) LED-Hardware auf Breadboard aufbauen** – LED + Vorwiderstand an GPIO4/Pin7 + Ground verkabelt, bestehender Node-RED-Flow erfolgreich getestet. Siehe [[Node-RED Flow - LED Test]].
- **[#2](https://github.com/47Felix/RasberryPI-Team-13/issues/2) Node-RED mit MQTT verknüpfen** – LED-Flow um Topic `team13-1/led/set` erweitert (Broker localhost:1883), Function-Node wandelt Payload in Boolean um, softwareseitig via `mosquitto_pub` getestet. Siehe [[Node-RED Flow - LED Test]].
- **[#3](https://github.com/47Felix/RasberryPI-Team-13/issues/3) Arduino + Elegoo-Kit Temperatursensor testen** – DHT11-Modul auf Breadboard mit Elegoo-UNO-R3 verkabelt, Arduino-Sketch mit DHT-Library geschrieben, Sensor liefert Werte (Kalibrierung/Wackelkontakt war noch ein Thema). Siehe [[Dogan - Brain Dump]].
- **[#10](https://github.com/47Felix/RasberryPI-Team-13/issues/10) Kleinteam bilden** – 4er-Team steht (ganzes Team 13).
- **[#11](https://github.com/47Felix/RasberryPI-Team-13/issues/11) Projektidee finden** – Entscheidung für "Digitaler Tresor / Escape-Box" (Keypad + Servo-Schloss + LCD + Buzzer/LED) aus dem Elegoo-UNO-R3-Kit. Siehe [[WS-Kurzprojekt Freitag]].
- **[#12](https://github.com/47Felix/RasberryPI-Team-13/issues/12) Kurzprojekt umsetzen (Hardware+Software)** – war zu grob geschnitten, aufgeteilt in die 6 parallelen Tracks #15-#20 (siehe oben).
- **[#15](https://github.com/47Felix/RasberryPI-Team-13/issues/15) Track A – Keypad-Eingabe + Code-Prüf-Logik** – 4x4-Keypad ausgelesen und mit fest hinterlegtem Code verglichen, Prüf-Logik erkennt richtigen/falschen Code zuverlässig. Teil des gemeinsamen Sketches `Code/arduino-tresor/tresor_integration/tresor_integration.ino` (PR [#30](https://github.com/47Felix/RasberryPI-Team-13/pull/30)).
- **[#16](https://github.com/47Felix/RasberryPI-Team-13/issues/16) Track B – Servo-Schließmechanismus** – Servo verkabelt und bewegt sich bei richtigem Code wie vorgesehen; Mechanik softwareseitig fertig, hängt aktuell nur an keiner echten Tür (siehe #19, Gehäuse bewusst nicht gebaut).
- **[#17](https://github.com/47Felix/RasberryPI-Team-13/issues/17) Track C – LCD1602-Statusanzeige** – LCD1602 verkabelt, zeigt Statustexte ("Code eingeben...", "Zugang gewährt", "Falscher Code", "Gesperrt!") wie geplant an.
- **[#18](https://github.com/47Felix/RasberryPI-Team-13/issues/18) Track D – Buzzer + LED Feedback und Alarm-Logik** – Rot/Grün-LED-Feedback und Buzzer-Töne (kurz = richtig, lang/tief = falsch) laufen wie gewollt, inkl. Alarm-Logik nach 3 Fehlversuchen (Dauerton + blinkende rote LED).
- **[#20](https://github.com/47Felix/RasberryPI-Team-13/issues/20) Track F – Gesamtintegration** – Keypad, Code-Prüfung, Servo, LCD und Buzzer/LED in einem gemeinsamen Sketch zusammengeführt, Pin-Konflikte aufgelöst, End-zu-End-Ablauf funktioniert. Danach noch zwei Nachbesserungen: fehlende Funktionsprototypen ergänzt (PR [#36](https://github.com/47Felix/RasberryPI-Team-13/pull/36)) und der Sketch-Ordner bereinigt, damit `arduino-cli` nur noch eine `.ino` kompiliert (PR [#47](https://github.com/47Felix/RasberryPI-Team-13/pull/47)). Offen blieb nur das physische Gehäuse (#19), kein Blocker für die Integration selbst.

## Verwandte Notizen
- [[WS-Kurzprojekt Freitag]]
- [[Offene Punkte]]
- [[Doku-Regeln]]

#github #issues #projekt
