---
tags: [github, issues, projekt]
---

# GitHub Issues – Übersicht

Zusammenfassung aller GitHub-Issues des Repos, aufgeteilt nach offen/geschlossen. Bei geschlossenen Issues steht jeweils kurz, **was gemacht wurde** – nicht nur, dass es erledigt ist. Wird von Claude gepflegt, siehe [[Doku-Regeln]].

> [!important] Regel
> Sobald ein GitHub-Issue abgeschlossen/gemerged wird, trägt Claude hier einen kurzen Eintrag ein (2-4 Sätze, was gemacht wurde) und verschiebt ihn von "🟢 Offen" nach "✅ Geschlossen". Siehe [[Doku-Regeln]] Abschnitt "GitHub Issues".

## 🟢 Offen

Aktuell keine offenen Issues (Stand 29.08.2026) – das Kurzprojekt "Digitaler Tresor" inkl. Pi-Dashboard-Erweiterung und Präsentation ist komplett abgeschlossen, alle Tracks/Issues sind geschlossen.

## ✅ Geschlossen (was wurde gemacht)

- **[#37](https://github.com/47Felix/RasberryPI-Team-13/issues/37) Track G – Arduino zu Pi Anbindung** – Arduino sendet `EVENT:READY/GRANTED/DENIED/ALARM/LOCKED` per USB-Serial an den Pi, Autodetect + Reconnect verifiziert per echtem Hardware-Test (28.08.2026). Siehe [[Erweiterung - Raspberry Pi Dashboard]].
- **[#38](https://github.com/47Felix/RasberryPI-Team-13/issues/38) Track H – Backend/Logging auf dem Pi** – Flask-App liest Serial im Hintergrund-Thread, loggt alle Ereignisse mit UTC-Zeitstempel in SQLite (`tresor.db`), läuft als systemd-Service `tresor-dashboard`. Per Mock- und echtem Hardware-Test bestätigt.
- **[#39](https://github.com/47Felix/RasberryPI-Team-13/issues/39) Track I – Web-Dashboard Frontend** – Live-Ampel, Versuchszähler und Ereignis-Verlauf, seit dem Hardware-Test mit `/api/status`-Polling alle 2s ohne manuelles Neuladen. Erreichbar im WLAN und per Tailscale.
- **[#40](https://github.com/47Felix/RasberryPI-Team-13/issues/40) Track J – Code/Passwort über Webinterface ändern** – `/admin`-Formular mit eigenem Admin-Passwort (getrennt vom Tresor-Code) setzt per `SETCODE`-Serial-Befehl einen neuen Tresor-Code.
- **[#41](https://github.com/47Felix/RasberryPI-Team-13/issues/41) Stretch – Discord-Bot meldet Alarm automatisch** – bei `EVENT:ALARM` postet der Pi automatisch eine Discord-Nachricht in #pi-projekt per REST-API (User-Agent-Bug beim Testen gefunden und gefixt).
- **[#42](https://github.com/47Felix/RasberryPI-Team-13/issues/42) Stretch – Live-Status-Anzeige + Versuchszähler** – als Text-Ampel im Dashboard umgesetzt (groß, farbig) inkl. Versuchszähler, keine physische LED-Ampel-Hardware (bewusste Einschränkung, siehe "Was noch fehlt" in [[Erweiterung - Raspberry Pi Dashboard]]).

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
- **[#19](https://github.com/47Felix/RasberryPI-Team-13/issues/19) Track E – Box/Gehäuse bauen** – bewusst nicht umgesetzt, wie von Anfang an im Team vereinbart (benotungsfrei, kein Blocker für Servo-Mechanik #16 oder Integration #20). Am 28.08.2026 zusammen mit der Präsentation geschlossen.
- **[#13](https://github.com/47Felix/RasberryPI-Team-13/issues/13) Kurzpräsentation vorbereiten (10 Minuten)** – 10-Folien-Deck erstellt (`Praesentation/tresor-praesentation.md`, Marp) plus fertig gerenderte HTML-Version, deckt Aufgabe, Architektur, Team-Tracks, Pi-Dashboard-Erweiterung und Lessons Learned ab. Siehe [[WS-Kurzprojekt Freitag]].
- **[#14](https://github.com/47Felix/RasberryPI-Team-13/issues/14) Präsentation am Freitag halten** – Präsentation am 28.08.2026 wie geplant gehalten, Issue am selben Tag geschlossen.
- **[#37](https://github.com/47Felix/RasberryPI-Team-13/issues/37) Track G – Arduino zu Pi Anbindung** – Serial-Protokoll (`EVENT:READY/GRANTED/DENIED/ALARM/...`) definiert, Pi liest USB-Seriell mit Geräte-Autodetect und 5s-Reconnect. Am 28.08.2026 mit echtem angeschlossenem Arduino verifiziert; dabei ein fehlendes Re-Lock-Event nach dem Wiederverriegeln gefunden und als neues `EVENT:LOCKED` nachgerüstet. Siehe [[Erweiterung - Raspberry Pi Dashboard]].
- **[#38](https://github.com/47Felix/RasberryPI-Team-13/issues/38) Track H – Backend/Logging auf dem Pi** – jedes Ereignis wird mit UTC-Zeitstempel in SQLite (`tresor.db`) geloggt, per HTTP- und echtem Hardware-Test verifiziert.
- **[#39](https://github.com/47Felix/RasberryPI-Team-13/issues/39) Track I – Web-Dashboard Frontend** – Flask-Dashboard mit Live-Ampel, Versuchszähler und Verlauf der letzten 50 Ereignisse, läuft als systemd-Service (`tresor-dashboard`). Seit 28.08.2026 mit echten Live-Updates per `/api/status`-Endpunkt + 2s-JS-Polling statt manuellem Neuladen. Design am selben Tag zweimal überarbeitet (Grafana-artiger Monitoring-Look, siehe [[Erweiterung - Raspberry Pi Dashboard]]).
- **[#40](https://github.com/47Felix/RasberryPI-Team-13/issues/40) Track J – Code/Passwort über Webinterface ändern** – eigenes `/admin`-Formular mit vom Tresor-Code getrenntem Admin-Passwort, sendet `SETCODE:<code>` per Serial an den Arduino.
- **[#41](https://github.com/47Felix/RasberryPI-Team-13/issues/41) Stretch – Discord-Bot meldet Alarm automatisch** – bei `EVENT:ALARM` schickt der Pi direkt eine Discord-Nachricht per REST-API in `#pi-projekt`; dabei einen 403-Bug gefunden und gefixt (Discord/Cloudflare blockte Pythons Standard-`urllib`-User-Agent).
- **[#42](https://github.com/47Felix/RasberryPI-Team-13/issues/42) Stretch – Live-Status-Anzeige + Versuchszähler** – als große farbige Text-Ampel im Dashboard umgesetzt, keine eigene physische LED-Ampel-Hardware am Pi.

## Verwandte Notizen
- [[WS-Kurzprojekt Freitag]]
- [[Offene Punkte]]
- [[Doku-Regeln]]

#github #issues #projekt
