---
tags: [github, issues, projekt]
---

# GitHub Issues – Übersicht

Zusammenfassung aller GitHub-Issues des Repos, aufgeteilt nach offen/geschlossen. Bei geschlossenen Issues steht jeweils kurz, **was gemacht wurde** – nicht nur, dass es erledigt ist. Wird von Claude gepflegt, siehe [[Doku-Regeln]].

> [!important] Regel
> Sobald ein GitHub-Issue abgeschlossen/gemerged wird, trägt Claude hier einen kurzen Eintrag ein (2-4 Sätze, was gemacht wurde) und verschiebt ihn von "🟢 Offen" nach "✅ Geschlossen". Siehe [[Doku-Regeln]] Abschnitt "GitHub Issues".

## 🟢 Offen

Stand 14.09.2026 (per GitHub-API geprüft) – 8 offene Issues.

> [!note] Challenge I: echte Aufgabenstellung erhalten (14.09.2026)
> Die 11 bisherigen DTEW-Workshop-Issues (#92-#102) wurden geschlossen (siehe unten) - Workshop vorbei, Code/Deliverables archiviert (siehe [[Doku-Regeln]]). Einzige Ausnahme: #92 (Sicherheitsvorfall) bleibt offen. Für [[Challenge I - Ice Truck Problem]] ([Milestone #2](https://github.com/47Felix/RasberryPI-Team-13/milestone/2)) liegt jetzt der echte Aufgabentext vor (I2C-Bus, Sensoren versch. Formate, LED-Helligkeit pro Sensor, Lüfter/Ventil-Aktorik, SQL-Logging - siehe die Notiz für den vollen Text). Die 4 vorherigen Platzhalter-Issues #171-#174 (Node-RED/MQTT/Discord-Alarm-Ansatz) waren dadurch überholt und wurden geschlossen, #169 (Aufgabenstellung ableiten) ist damit erledigt. Ersetzt durch 6 Tracks nach demselben Muster wie beim Tresor-Kurzprojekt (#15-#20): #176-#181.

- [#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92) Supabase-Token widerrufen (Sicherheitsvorfall 04.09.) – weiterhin offen, braucht einen Menschen mit Supabase-Dashboard-Zugriff, keine automatisierte Session kann das lösen
- [#167](https://github.com/47Felix/RasberryPI-Team-13/issues/167) Moodle-Zugang zu "Signale und Bussysteme" (Kurs-ID 1574) einholen – Aufgabentext liegt zwar schon vor, offen ob der volle Kurs (I2C/SPI-Grundlagen) noch gebraucht wird, siehe Kommentar dort
- [#168](https://github.com/47Felix/RasberryPI-Team-13/issues/168) Git auf dem Pi einrichten und Repo klonen
- [#176](https://github.com/47Felix/RasberryPI-Team-13/issues/176) Track A – Sensor-Arduino: Sensoren unterschiedlicher Formate auslesen (analog/digital/Bus)
- [#177](https://github.com/47Felix/RasberryPI-Team-13/issues/177) Track B – Je Sensor eine LED mit Helligkeit proportional zum Messwert (PWM)
- [#178](https://github.com/47Felix/RasberryPI-Team-13/issues/178) Track C – I2C-Bus: Sensor-Arduino(s) an den Raspberry Pi
- [#179](https://github.com/47Felix/RasberryPI-Team-13/issues/179) Track D – Aktor-Arduino: Lüfter (Transistor/H-Brücke) + Ventil (Servo)
- [#180](https://github.com/47Felix/RasberryPI-Team-13/issues/180) Track E – I2C: Raspberry Pi steuert den Aktor-Arduino
- [#181](https://github.com/47Felix/RasberryPI-Team-13/issues/181) Track F – Pi-Backend: SQL-Logging + Regellogik (Gesamtintegration)

> [!note] Challenge I: Scaffold + reale Hardware-Verkabelung (seit 14.09.2026, PRs #183/#185/#186/#189/#190)
> Tracks A-F wurden als `Challenge-I-Ice-Truck/Code/` umgesetzt (Sensor-/Aktor-Arduino-Sketches, Pi-Backend `pi-backend/` mit `rules.py`/`db.py`/`hardware.py`/`app.py`, 9 grüne Tests). Reale Verkabelung ist **ein** Arduino Uno mit DHT11, Fotowiderstand, Taster, 3 LEDs, Lüfter-Transistor und Servo (`ice_truck_single_board/ice_truck_single_board.ino`), nicht die ursprünglich angenommenen zwei separaten Boards – Details siehe `Challenge-I-Ice-Truck/Code/README.md`. Zwei Punkte noch offen:

- [#184](https://github.com/47Felix/RasberryPI-Team-13/issues/184) Challenge I: Monitoring-Dashboard für die Kühlkette (Design) – Web-Dashboard fürs Kühlketten-Backend, analog zum Tresor-Dashboard, noch nicht umgesetzt
- [#191](https://github.com/47Felix/RasberryPI-Team-13/issues/191) Challenge I: DHT11 liefert konstant ~20°C zu wenig (Verkabelung/Pull-up prüfen) – Workaround per Offset aktiv, echte Kalibrierung/Reparatur noch offen

Das Kurzprojekt "Digitaler Tresor" (Issues #1-#42, siehe unten) ist weiterhin komplett abgeschlossen.

> [!note] Challenge II: echte Aufgabenstellung erhalten (15.09.2026)
> Für [[Challenge II - Ice Truck Extension]] ([Milestone #3](https://github.com/47Felix/RasberryPI-Team-13/milestone/3)) liegt der echte Aufgabentext vor: mobile Anzeige der Temperaturdaten + Fernsteuerung der Aktoren per MQTT, Node-RED als Integrations-Framework, MQTT Dash/Explorer statt Eigenbau-App. In 4 Tracks heruntergebrochen: #193-#196.

- [#193](https://github.com/47Felix/RasberryPI-Team-13/issues/193) Track A – MQTT-Broker: Verbindung zum ITECH-Broker oder lokalem Mosquitto sicherstellen
- [#194](https://github.com/47Felix/RasberryPI-Team-13/issues/194) Track B – MQTT-Topic-Schema für Sensordaten + Aktor-Befehle definieren
- [#195](https://github.com/47Felix/RasberryPI-Team-13/issues/195) Track C – Node-RED-Flow: Pi-Backend (I2C/SQL aus Challenge I) mit MQTT verbinden
- [#196](https://github.com/47Felix/RasberryPI-Team-13/issues/196) Track D – Mobile Anbindung: MQTT Dash / MQTT Explorer konfigurieren + Doku

## ✅ Geschlossen (was wurde gemacht)

- **[#169](https://github.com/47Felix/RasberryPI-Team-13/issues/169) Challenge I: Aufgabenstellung aus Moodle-Kurs ableiten und Team-Tasks planen** – Aufgabentext erhalten (14.09.), in 6 Tracks heruntergebrochen (#176-#181), siehe [[Challenge I - Ice Truck Problem]].
- **[#171](https://github.com/47Felix/RasberryPI-Team-13/issues/171) DHT11-Sensor fest verkabeln + Sketch auf strukturierte Ausgabe umstellen** – als überholt geschlossen (14.09.), Node-RED/MQTT-Ansatz passte nicht zur echten Aufgabenstellung (I2C-Bus, Aktorik, SQL). Ersetzt durch Track A/C (#176/#178).
- **[#172](https://github.com/47Felix/RasberryPI-Team-13/issues/172) Sensordaten per Node-RED einlesen und über MQTT veröffentlichen** – als überholt geschlossen (14.09.), gleicher Grund wie #171. Ersetzt durch Track C (#178).
- **[#173](https://github.com/47Felix/RasberryPI-Team-13/issues/173) Schwellwert-Überwachung + Alarm bei Kühlkettenbruch** – als überholt geschlossen (14.09.); die echte Aufgabe verlangt eine Regelschleife (Lüfter/Ventil ansteuern), keinen reinen Alarm. Ersetzt durch Track F (#181).
- **[#174](https://github.com/47Felix/RasberryPI-Team-13/issues/174) Kühlketten-Überwachung im Vault dokumentieren** – als überholt geschlossen (14.09.), Doku passiert jetzt im Rahmen von Track F (#181).
- **[#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100) Board-Zugriff der Nacht-Automation repariert** – bereits erledigt, nur nie geschlossen; mit Workshop-Ende (14.09.) formal geschlossen.
- **[#101](https://github.com/47Felix/RasberryPI-Team-13/issues/101) Vielfalts-Score im Feed-Prototyp umgesetzt** – bereits erledigt, nur nie geschlossen; mit Workshop-Ende (14.09.) formal geschlossen.
- **[#102](https://github.com/47Felix/RasberryPI-Team-13/issues/102) Feed-UI auf echtes Single-Feed-Layout umgebaut** – bereits erledigt, nur nie geschlossen; mit Workshop-Ende (14.09.) formal geschlossen.
- **[#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93) Prototyp-Arbeitstitel/Namen entscheiden** – als obsolet geschlossen (14.09.), DTEW-Workshop vorbei, Entscheidung nicht mehr relevant.
- **[#94](https://github.com/47Felix/RasberryPI-Team-13/issues/94) Social Business Model Canvas im Team abstimmen** – als obsolet geschlossen (14.09.).
- **[#95](https://github.com/47Felix/RasberryPI-Team-13/issues/95) Onboarding-Entwurf gegen aktuellen Prototyp-Code-Stand abgleichen** – als obsolet geschlossen (14.09.).
- **[#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96) Logo visuell gestalten** – als obsolet geschlossen (14.09.).
- **[#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97) Donnerstag (03.09.) rückwirkend dokumentieren** – als obsolet geschlossen (14.09.).
- **[#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98) Retrospektive vorbereiten (Sprint-Ende Montag 07.09.)** – als obsolet geschlossen (14.09.).
- **[#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99) Rollen im Team festlegen (Scrum Master / Product Owner)** – als obsolet geschlossen (14.09.), DTEW-spezifisch; für Challenge I bei Bedarf neu aufsetzen.

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
- **[#15](https://github.com/47Felix/RasberryPI-Team-13/issues/15) Track A – Keypad-Eingabe + Code-Prüf-Logik** – 4x4-Keypad ausgelesen und mit fest hinterlegtem Code verglichen, Prüf-Logik erkennt richtigen/falschen Code zuverlässig. Teil des gemeinsamen Sketches `Tresor-Kurzprojekt/Code/arduino-tresor/tresor_integration/tresor_integration.ino` (PR [#30](https://github.com/47Felix/RasberryPI-Team-13/pull/30)).
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
