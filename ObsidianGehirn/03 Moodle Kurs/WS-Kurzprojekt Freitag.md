---
tags: [moodle, workshop, kurzprojekt, praesentation]
---

# "Thank god it's (NOT) Friday" – Kurzprojekt & Abschlusspräsentation

> [!important] Deadline: Freitag, 28.08.2026 (Uhrzeit noch TBA)
> Abschluss-Challenge der Workshop-Woche ("Piece of Pi?", siehe [[Kursstruktur]] Punkt 5 "Freies Kurzprojekt und Präsentation"). **Benotungsfrei** – es geht um Ruhm, Ehre, Spaß und ein bisschen Wettkampfgedanken, nicht um Schulnoten.

## Original-Aufgabenstellung (Moodle)
> Vor dem Wochenende erwartet euch noch eine kleine Challenge zum Abschluss dieser Workshop-Woche. Sattelt die Einhörner, illuminiert die Regenbögen und holt die Dosen mit Feenstaub aus dem Regal. Nichts geringeres als ein fulminantes Feuerwerk gilt es abzubrennen.
>
> Die Aufgabe für den heutigen Tag ist simpel wie kompliziert:
> - Findet euch in kleinen Teams zusammen (2 bis 3 Personen)
> - Überlegt euch ein kleines Projekt, dass ihr mit RasPi, Arduino, Sensorik und Co. umsetzen möchtet
> - Bereitet eine spektakuläre Kurzpräsentation vor (10 Minuten!)
> - Verzaubert das Publikum mit eurer Kreativität! (Präsentationsstart: Freitag, TBA Uhr)
>
> Diese Challenge ist benotungsfrei! Es geht nicht um Schulnoten, sondern um nichts geringeres als Ruhm, Ehre, Spaß an der Freude und ein kleines bisschen den Wettkampfgedanken.

## Team & Projektidee ✅ entschieden
- **Team:** 4 Personen (Team 13 komplett)
- **Projekt: 🔐 Digitaler Tresor / Escape-Box** – Elegoo UNO R3 Starter Kit: 4x4-Keypad zur Code-Eingabe, Servo als Schließmechanismus, LCD1602 für Status-Anzeige, Buzzer + LEDs für akustisches/visuelles Feedback und Alarm bei Fehlversuchen. Live-Showmoment: Publikum darf den Code knacken.

> [!tip] Warum so aufgeteilt?
> Damit alle 4 gleichzeitig arbeiten können (oder wahlweise zu zweit pro Track), ist die Umsetzung in unabhängige Arduino-Teilmodule ("Tracks") zerlegt. Jeder Track hat sein eigenes Mini-Sketch und braucht nichts von den anderen – erst am Schluss (Track F) wird alles in einem gemeinsamen Sketch zusammengeführt.

## Arbeitspakete (Tracks A–F)
Milestone: [Milestone #1 "WS-Kurzprojekt & Präsentation (Freitag)"](https://github.com/47Felix/RasberryPI-Team-13/milestone/1), fällig 28.08.2026.

| Track | Was | Abhängigkeit | Issue |
|---|---|---|---|
| A | Keypad-Eingabe + Code-Prüf-Logik | keine – sofort startbar | [#15](https://github.com/47Felix/RasberryPI-Team-13/issues/15) |
| B | Servo-Schließmechanismus | keine – sofort startbar (Absprache mit E wegen Mechanik) | [#16](https://github.com/47Felix/RasberryPI-Team-13/issues/16) |
| C | LCD1602-Statusanzeige | keine – sofort startbar | [#17](https://github.com/47Felix/RasberryPI-Team-13/issues/17) |
| D | Buzzer + LED Feedback/Alarm | keine – sofort startbar | [#18](https://github.com/47Felix/RasberryPI-Team-13/issues/18) |
| E | Box/Gehäuse bauen | keine – reine Handarbeit, parallel zu allem | [#19](https://github.com/47Felix/RasberryPI-Team-13/issues/19) |
| F | Gesamtintegration (alles zusammenführen) | **braucht A, B, C, D fertig** – guter gemeinsamer Sync-Punkt für alle 4 | [#20](https://github.com/47Felix/RasberryPI-Team-13/issues/20) |
| – | Kurzpräsentation vorbereiten (10 Min., Story/Skript) | keine – kann parallel starten, z.B. sobald jemand mit seinem Track fertig ist | [#13](https://github.com/47Felix/RasberryPI-Team-13/issues/13) |
| – | Präsentation Freitag halten (Uhrzeit TBA) | braucht F | [#14](https://github.com/47Felix/RasberryPI-Team-13/issues/14) |

**Vorschlag für 4 Personen:** je 1 Person auf Track A, B, C, D – dann gemeinsam Track E (nebenbei/wer zuerst fertig ist) und F (alle zusammen).
**Vorschlag für 2 Zweierteams:** Team 1 = Track A+C (Software/Anzeige), Team 2 = Track B+D (Hardware/Feedback) – Track E kann jeder zwischendurch übernehmen, F gemeinsam am Schluss.

### Fortschritt (26.08.2026)
Kombinierter Arduino-Sketch für Track A (Keypad+Code-Prüf-Logik), B (Servo), C (LCD1602) und D (LEDs, **ohne** Buzzer) gemerged: [`Code/arduino-tresor/tresor_integration/tresor_integration.ino`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/arduino-tresor/tresor_integration/tresor_integration.ino) (PR [#30](https://github.com/47Felix/RasberryPI-Team-13/pull/30)). Buzzer-Teil von Track D folgt noch (Pin D11 im Sketch reserviert), ebenso Track E (Gehäuse) und F (finale Gesamtintegration).

### Tracks A, B, C, D, F abgeschlossen (27.08.2026)
Buzzer-Feedback, Gesamtintegration und End-zu-End-Test abgeschlossen – Issues [#15](https://github.com/47Felix/RasberryPI-Team-13/issues/15), [#16](https://github.com/47Felix/RasberryPI-Team-13/issues/16), [#17](https://github.com/47Felix/RasberryPI-Team-13/issues/17), [#18](https://github.com/47Felix/RasberryPI-Team-13/issues/18) und [#20](https://github.com/47Felix/RasberryPI-Team-13/issues/20) geschlossen. Danach zwei Nachbesserungen am Sketch: fehlende Funktionsprototypen ergänzt (PR [#36](https://github.com/47Felix/RasberryPI-Team-13/pull/36)) und der Sketch-Ordner bereinigt (PR [#47](https://github.com/47Felix/RasberryPI-Team-13/pull/47)). Track E (Gehäuse, [#19](https://github.com/47Felix/RasberryPI-Team-13/issues/19)) bleibt bewusst ungebaut, benotungsfrei. Details siehe [[Issues - Übersicht]].

### Präsentation (27.08.2026)
10-Folien-Deck erstellt: [`Praesentation/tresor-praesentation.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Praesentation/tresor-praesentation.md) (Marp-Markdown) + fertig gerenderte [HTML-Version](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Praesentation/tresor-praesentation.html) zum direkten Präsentieren im Browser. Deckt Aufgabe/Idee/Hardware/Architektur/Team-Tracks/Pi-Dashboard/Lessons Learned ab, endet mit Ankündigung der Live-Demo. Siehe [[Erweiterung - Raspberry Pi Dashboard]] für die Dashboard-Details.

### Kurzprojekt abgeschlossen (28.08.2026)
Präsentation wie geplant gehalten, Issue [#14](https://github.com/47Felix/RasberryPI-Team-13/issues/14) geschlossen. Gehäuse/Box (Track E, [#19](https://github.com/47Felix/RasberryPI-Team-13/issues/19)) blieb wie von Anfang an vereinbart bewusst ungebaut (benotungsfrei). Damit ist Milestone #1 komplett erledigt – keine offenen Issues zum Kurzprojekt mehr, siehe [[Issues - Übersicht]].

### Erledigt ✅
- [x] Kleinteam bilden → [#10](https://github.com/47Felix/RasberryPI-Team-13/issues/10) (closed)
- [x] Projektidee finden → [#11](https://github.com/47Felix/RasberryPI-Team-13/issues/11) (closed)
- [x] Kurzpräsentation vorbereiten → [#13](https://github.com/47Felix/RasberryPI-Team-13/issues/13) (closed)
- [x] Präsentation Freitag halten → [#14](https://github.com/47Felix/RasberryPI-Team-13/issues/14) (closed)

## Verwandte Notizen
- [[Kursstruktur]]
- [[Offene Punkte]]
- [[Roter Faden - Ice Truck]] – falls das Kurzprojekt an unser Ice-Truck-Thema andockt

#moodle #workshop #kurzprojekt #praesentation
